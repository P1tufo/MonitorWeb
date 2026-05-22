"""
routes/analytics_deliveries.py — Rutas de analíticas Entregas optimizadas y seguras. [Reload Triggered]
"""
import logging
import sqlite3
import pandas as pd
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy import text

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse

from core.database import get_session_dep
from sqlalchemy.orm import Session
from core.state import AppState, get_app_state
from core.app_instance import templates
from core.schemas import AnalyticsDeliveriesResponse

from repositories import DeliveriesRepository
from routes.inventory import get_inventory_context
from routes.tasks import get_tasks_context
from routes.analytics_proyecciones import get_proyecciones_context
from core.auth import get_current_user
from core.utils import sanitize_for_json
from services.deliveries_service import DeliveriesService

logger = logging.getLogger("routes-analytics-deliveries")
router = APIRouter()

# ─── Dependencias ─────────────────────────────────────────────────────────────

def save_analytics_snapshot(session: Session, key: str, data: Dict[str, Any]):
    """Guarda una captura de las analíticas en la base de datos para carga instantánea."""
    try:
        session.execute(text("CREATE TABLE IF NOT EXISTS analytics_snapshots (key TEXT PRIMARY KEY, data TEXT, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"))
        # Limpiar request si existe por seguridad
        data_to_save = {k: v for k, v in data.items() if k != 'request'}
        json_data = json.dumps(data_to_save)
        session.execute(
            text("INSERT OR REPLACE INTO analytics_snapshots (key, data, updated_at) VALUES (:key, :data, CURRENT_TIMESTAMP)"),
            {"key": key, "data": json_data}
        )
        session.commit()
    except Exception as e:
        logger.error(f"Error guardando snapshot {key}: {e}")

def load_analytics_snapshot(session: Session, key: str) -> Optional[Dict[str, Any]]:
    """Recupera la última captura de analíticas desde la base de datos."""
    try:
        res = session.execute(text("SELECT data FROM analytics_snapshots WHERE key = :key"), {"key": key}).fetchone()
        if res:
            return json.loads(res[0])
    except Exception:
        pass
    return None

# ─── Rutas ───────────────────────────────────────────────────────────────────

@router.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state)):
    """Renderiza la página principal de analíticas con caché multinivel (Memoria -> DB -> Cálculo)."""
    # 1. Nivel 1: Memoria (Instantáneo)
    cached = state.get_cache("/analytics/deliveries")
    if cached and "wms_labels" in cached:
        logger.info("Sirviendo analíticas desde Caché de Memoria.")
        cached["request"] = request
        cached["user"] = user
        response = templates.TemplateResponse(request=request, name="deliveries.html", context=cached)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return response

    
    # 2. Nivel 2: Snapshot en BD (Muy rápido, persistente)
    year_str = datetime.now().strftime("%Y")
    month_str = datetime.now().strftime("%m")
    snapshot = load_analytics_snapshot(session, f"deliveries_{year_str}_{month_str}")
    if snapshot and "wms_labels" in snapshot:
        logger.info("Sirviendo analíticas desde Snapshot de Base de Datos.")
        state.set_cache("/analytics/deliveries", snapshot)
        snapshot["request"] = request
        snapshot["user"] = user
        response = templates.TemplateResponse(request=request, name="deliveries.html", context=snapshot)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return response


    # 3. Nivel 3: Cálculo (Lento, primera vez o tras limpieza)
    logger.info("Sin caché disponible. Iniciando cálculo completo...")
    context = DeliveriesService(session).get_full_context()
    context["request"] = request
    context["user"] = user
    
    response = templates.TemplateResponse(request=request, name="deliveries.html", context=context)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

@router.get("/analytics/sla", response_class=HTMLResponse)
async def sla_details(
    request: Request, 
    type: str = "late", 
    session: Session = Depends(get_session_dep)
):
    """Vista detallada de auditoría SLA."""
    try:
        current_year = str(datetime.now().year)
        is_late = (type != "ontime")
        
        title = "Auditoría: Atrasadas (Peores 500)" if is_late else "Auditoría: A Tiempo (Últimos 500)"
        df = DeliveriesService(session).get_sla_audit_records(f"%{current_year}", late=is_late)
        
        # Limpieza de datos profunda para evitar errores de tipo en Jinja2 (NaN -> '')
        df['area_negocio'] = df['area_negocio'].fillna('S/N')
        df['texto_breve'] = df['texto_breve'].fillna('') # Crucial para evitar 'float not subscriptable'
        records = df.to_dict(orient="records")
        
        return templates.TemplateResponse(
            request=request, 
            name="sla_table.html", 
            context={"title": title, "type": type, "records": records}
        )
    except Exception as e:
        logger.error(f"Error en auditoría SLA: {e}")
        raise HTTPException(status_code=500, detail="No se pudo cargar la tabla de auditoría.")













@router.get("/api/non-palletized/details")
def get_non_palletized_details(
    user: str,
    clase_mov: str,
    db: Session = Depends(get_session_dep),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Obtiene el listado detallado (hasta 200) de movimientos no paletizados
    para un usuario y tipo de movimiento específicos.
    """
    try:
        query = """
            SELECT 
                p.otcuanto as doc_mat,
                COUNT(p.material) as pos,
                CASE WHEN COUNT(p.material) > 1 THEN 'Varios Materiales' ELSE MIN(p.material) END as material,
                CASE WHEN COUNT(p.material) > 1 THEN 'Selección agrupada (' || COUNT(p.material) || ' ítems)' ELSE MIN(p.denominacion) END as material_name,
                ROUND(SUM(CAST(REPLACE(p.stock_disp, ',', '.') AS REAL)), 2) as qty,
                MAX(m.alm) as source,
                MAX(m.ce) as dest,
                MAX(m.fe_contab || ' ' || m.hora) as created_at
            FROM lx02_pendientes p
            JOIN (
                SELECT doc_mat, usuario, cmv, MAX(alm) as alm, MAX(ce) as ce, MAX(fe_contab) as fe_contab, MAX(hora) as hora 
                FROM inventory_movements 
                GROUP BY doc_mat, usuario, cmv
            ) m ON p.otcuanto = m.doc_mat
            WHERE m.usuario = :user AND m.cmv = :cmv
              AND CAST(REPLACE(p.stock_disp, ',', '.') AS REAL) != 0
            GROUP BY p.otcuanto
            ORDER BY created_at DESC
            LIMIT 200
        """
        df = pd.read_sql(text(query), db.connection(), params={"user": user, "cmv": clase_mov})
        rows = sanitize_for_json(df.to_dict(orient="records"))
        return {"status": "success", "data": rows}

    except Exception as e:
        logger.error(f"Error cargando detalle no paletizado para {user} / {clase_mov}: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/api/v1/analytics/deliveries", response_model=AnalyticsDeliveriesResponse)
async def analytics_deliveries_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state)):
    """API JSON para analíticas de Entregas (Outbound Deliveries)."""
    
    # 1. Caché en Memoria
    cached = state.get_cache("/api/v1/analytics/deliveries")
    if cached:
        return AnalyticsDeliveriesResponse(data=cached, is_syncing=state.is_syncing)

    # 2. Snapshot en BD
    year_str = datetime.now().strftime("%Y")
    month_str = datetime.now().strftime("%m")
    snapshot = load_analytics_snapshot(session, f"deliveries_{year_str}_{month_str}")
    if snapshot and "wms_labels" in snapshot:
        clean_snapshot = {k: v for k, v in snapshot.items() if k not in ('request', 'user', 'is_syncing')}
        state.set_cache("/api/v1/analytics/deliveries", clean_snapshot)
        return AnalyticsDeliveriesResponse(data=clean_snapshot, is_syncing=state.is_syncing)

    # 3. Cálculo Completo
    try:
        from services.deliveries_service import DeliveriesService
        context = DeliveriesService(session).get_full_context()
        clean_context = {k: v for k, v in context.items() if k not in ('request', 'user', 'is_syncing')}
        
        state.set_cache("/api/v1/analytics/deliveries", clean_context)
        save_analytics_snapshot(session, f"deliveries_{year_str}_{month_str}", clean_context)
        
        return AnalyticsDeliveriesResponse(data=clean_context, is_syncing=state.is_syncing)
    except Exception as e:
        logger.error(f"Error cargando API analytics deliveries: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error calculando analíticas.")
