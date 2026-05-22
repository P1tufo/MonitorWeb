"""
routes/dashboard.py — Ruta principal del dashboard optimizada.
"""
import logging
import sqlite3
import itertools
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from core.database import get_session_dep
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.state import AppState, get_app_state
from core.auth import get_current_user
from core.app_instance import templates
from services.dashboard_service import DashboardService
from core.wms_config import get_query
from core.schemas import DashboardResponse

logger = logging.getLogger("routes-dashboard")
router = APIRouter()

# ─── Dependencias ─────────────────────────────────────────────────────────────

# ─── Rutas ───────────────────────────────────────────────────────────────────

@router.get("/api/ubicaciones/{material}")
async def get_ubicaciones(material: str, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state)):
    # Always detect the actual column name in stock_levels (varies by import source)
    res = session.execute(text("PRAGMA table_info(stock_levels)"))
    stock_cols = {row[1] for row in res.fetchall()}
    ubi_col = (
        "ubicacion_bin" if "ubicacion_bin" in stock_cols
        else ("ubicacin" if "ubicacin" in stock_cols
        else "ubicacion")
    )
    desc_col = "denominacion" if "denominacion" in stock_cols else "texto_breve_de_material"

    query_db = get_query("inv_historial_ubicaciones")
    if query_db:
        # Substitute dynamic column names and normalise bind-params to SQLAlchemy style
        query = (
            query_db
            .replace("s.ubicacin", f"s.{ubi_col}")
            .replace("s.texto_breve_de_material", f"s.{desc_col}")
            .replace("{ubi_col}", ubi_col)
            .replace("{desc_col}", desc_col)
            .replace("?", ":mat")   # convierte posicionales sqlite3 → nombrados SQLAlchemy
        )
    else:
        query = f"""
        SELECT 
            l.ubicacion as ubic_dest,
            MAX(l.fecha) as fecha,
            MAX(l.texto_breve_material) as texto_breve_material,
            SUM(l.stock_disp) as stock_disp,
            MAX(l.umb) as umb,
            MAX(l.ubic_actual) as ubic_actual
        FROM (
            SELECT 
                w.ubic_dest as ubicacion, 
                COALESCE(w.fecha_conf, w.fe_creac) as fecha, 
                w.texto_breve_material as texto_breve_material,
                NULL as stock_disp,
                NULL as umb,
                NULL as ubic_actual
            FROM warehouse_tasks w
            WHERE UPPER(TRIM(w.material)) = :mat
              AND w.tp_dest NOT LIKE '9%'
              AND w.ubic_dest IS NOT NULL
              AND TRIM(w.ubic_dest) != ''

            UNION ALL

            SELECT 
                s.{ubi_col} as ubicacion,
                NULL as fecha,
                s.{desc_col} as texto_breve_material,
                CAST(REPLACE(s.stock_disp, ',', '.') AS REAL) as stock_disp,
                s.umb as umb,
                s.{ubi_col} as ubic_actual
            FROM stock_levels s
            WHERE UPPER(TRIM(s.material)) = :mat
              AND s.{ubi_col} IS NOT NULL
              AND TRIM(s.{ubi_col}) != ''
        ) l
        GROUP BY l.ubicacion
        ORDER BY fecha DESC
        """
    try:
        material_upper = material.strip().upper()
        # text() requiere parámetros nombrados (:param) y dict, no tupla con '?'
        df = pd.read_sql(text(query), session.connection(), params={"mat": material_upper})
        df = df.astype(object).where(pd.notnull(df), None)
        return df.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Error fetching ubicaciones for {material}: {e}")
        return []


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state)):
    """Vista principal del Dashboard con KPIs y búsqueda rápida."""
    
    # Intentar recuperar de caché
    cached_ctx = state.get_cache("/")
    if cached_ctx:
        cached_ctx["request"] = request
        cached_ctx["user"] = user
        cached_ctx["is_syncing"] = state.is_syncing
        return templates.TemplateResponse(request=request, name="dashboard.html", context=cached_ctx)

    try:
        iso_year, iso_week, _ = datetime.now().isocalendar()
        current_week_str = f"{iso_year}-{iso_week:02d}"
        
        # 0. Calcular semana de inicio (Semana actual)
        min_week = current_week_str

        # Usar el servicio para obtener todo el contexto de negocio
        service = DashboardService(session)
        service_context = service.get_full_context()
        
        # Construir contexto
        context = {
            "request": request,
            "user": user,
            "is_syncing": state.is_syncing,
            **service_context
        }
        
        state.set_cache("/", context.copy())
        return templates.TemplateResponse(request=request, name="dashboard.html", context=context)

    except Exception as e:
        logger.error(f"Error cargando dashboard: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error cargando los datos del dashboard.")

# ─── Funciones Auxiliares ────────────────────────────────────────────────────


@router.get("/api/v1/dashboard", response_model=DashboardResponse)
async def dashboard_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state)):
    """API JSON para el Dashboard con KPIs y búsqueda rápida."""
    
    # Intentar recuperar de caché (excluyendo el request)
    cached_ctx = state.get_cache("/api/v1/dashboard")
    if cached_ctx:
        return DashboardResponse(data=cached_ctx, is_syncing=state.is_syncing)

    try:
        # Usar el servicio para obtener todo el contexto de negocio
        service = DashboardService(session)
        service_context = service.get_full_context()
        
        # Filtrar objetos no serializables si los hay
        clean_context = {k: v for k, v in service_context.items() if k not in ('request', 'user', 'is_syncing')}
        
        state.set_cache("/api/v1/dashboard", clean_context.copy())
        return DashboardResponse(data=clean_context, is_syncing=state.is_syncing)

    except Exception as e:
        logger.error(f"Error cargando API dashboard: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error cargando los datos del dashboard.")
