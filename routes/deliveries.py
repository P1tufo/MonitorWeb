"""
routes/analytics_deliveries.py — Rutas de analíticas Entregas optimizadas y seguras. [Reload Triggered]
"""
import json
import logging
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.app_instance import templates
from core.auth import get_current_user
from core.database import get_session_dep
from core.schemas import AnalyticsDeliveriesResponse
from core.state import SyncStateManager, get_sync_manager
from core.utils import sanitize_for_json
from repositories import DeliveriesRepository
from services.deliveries_service import DeliveriesService

logger = logging.getLogger("routes-analytics-deliveries")
router = APIRouter()

# ─── Dependencias ─────────────────────────────────────────────────────────────

# ─── Rutas ───────────────────────────────────────────────────────────────────

@router.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep)):
    """Renderiza la página principal de analíticas con caché multinivel gestionado por decorador."""
    context = DeliveriesService(session).get_full_context()
    context["request"] = request
    context["user"] = user

    response = templates.TemplateResponse(request=request, name="deliveries.html", context=context)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response


from routes.filters import _build_unified_where


@router.get("/analytics/sla", response_class=HTMLResponse)
async def sla_details(
    request: Request,
    type: str = "late",
    date: Optional[str] = None,
    area: Optional[str] = None,
    centro: Optional[str] = None,
    has_ots_filter: Optional[str] = None,
    session: Session = Depends(get_session_dep)
):
    """Vista detallada de auditoría SLA."""
    try:
        current_year = str(datetime.now().year)
        is_late = (type != "ontime")

        # Si se usa un filtro de área, reflejarlo en el título
        area_title = f" ({area})" if area and area.strip() != "" else ""
        title = f"Auditoría{area_title}: Atrasadas (Peores 500)" if is_late else f"Auditoría{area_title}: A Tiempo (Últimos 500)"

        iso_year, iso_week, _ = datetime.now().isocalendar()

        # Generamos la cláusula WHERE usando las reglas unificadas (no limita la fecha si no se envía, para el año actual limitaremos más abajo)
        where_clause, where_params = _build_unified_where(date, area, centro, has_ots_filter, min_week=f"{current_year}-01")

        from repositories import DeliveriesRepository
        df = DeliveriesRepository(session).get_sla_audit_records(f"%{current_year}", late=is_late, where_clause=where_clause, where_params=where_params)

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
        logger.error(f"Error cargando detalle no paletizado para {user} / {clase_mov}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ha ocurrido un error interno procesando la solicitud.")



@router.get("/api/v1/analytics/deliveries", response_model=AnalyticsDeliveriesResponse)
async def analytics_deliveries_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), sync: SyncStateManager = Depends(get_sync_manager)):
    """API JSON para analíticas de Entregas (Outbound Deliveries) con caché multinivel gestionado por decorador."""
    try:
        from services.deliveries_service import DeliveriesService
        context = DeliveriesService(session).get_full_context()
        clean_context = {k: v for k, v in context.items() if k not in ('request', 'user', 'is_syncing')}
        return AnalyticsDeliveriesResponse(data=clean_context, is_syncing=sync.is_syncing)
    except Exception as e:
        logger.error(f"Error cargando API analytics deliveries: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error calculando analíticas.")
