"""
routes/dashboard.py — Ruta principal del dashboard optimizada.
"""
import itertools
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.app_instance import templates
from core.auth import get_current_user
from core.database import get_session_dep
from core.schemas import DashboardResponse
from core.state import CacheManager, SyncStateManager, get_cache_manager, get_sync_manager
from core.db_config_manager import get_user_groups
from services.dashboard_service import DashboardService

logger = logging.getLogger("routes-dashboard")
router = APIRouter()

# ─── Dependencias ─────────────────────────────────────────────────────────────

# ─── Rutas ───────────────────────────────────────────────────────────────────

@router.get("/api/ubicaciones/{material}")
async def get_ubicaciones(material: str, user = Depends(get_current_user), session: Session = Depends(get_session_dep)):
    res = session.execute(text("PRAGMA table_info(stock_levels)"))
    stock_cols = {row[1] for row in res.fetchall()}

    if "ubicacion_bin" in stock_cols:
        ubi_col = "ubicacion_bin"
    elif "Ubicación" in stock_cols:
        ubi_col = '"Ubicación"'
    elif "ubicacin" in stock_cols:
        ubi_col = "ubicacin"
    else:
        ubi_col = "ubicacion"

    if "denominacion" in stock_cols:
        desc_col = "denominacion"
    elif "Texto breve de material" in stock_cols:
        desc_col = '"Texto breve de material"'
    else:
        desc_col = "texto_breve_de_material"

    mat_col = '"Material"' if "Material" in stock_cols else "material"
    umb_col = '"UMB"' if "UMB" in stock_cols else "umb"
    stock_col = '"Stock disp"' if "Stock disp" in stock_cols else "stock_disp"


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
                CAST(REPLACE(s.{stock_col}, ',', '.') AS REAL) as stock_disp,
                s.{umb_col} as umb,
                s.{ubi_col} as ubic_actual
            FROM stock_levels s
            WHERE UPPER(TRIM(s.{mat_col})) = :mat
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
async def dashboard(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager), sync: SyncStateManager = Depends(get_sync_manager)):
    """Vista principal del Dashboard con KPIs y búsqueda rápida."""

    # Intentar recuperar de caché
    cached_ctx = cache.get_cache("/")
    if cached_ctx:
        cached_ctx["request"] = request
        cached_ctx["user"] = user
        cached_ctx["is_syncing"] = sync.is_syncing
        return templates.TemplateResponse(request=request, name="dashboard.html", context=cached_ctx)

    try:
        iso_year, iso_week, _ = datetime.now().isocalendar()

        # 0. Calcular semana de inicio (Semana actual)

        # Usar el servicio para obtener todo el contexto de negocio
        service = DashboardService(session)
        service_context = service.get_full_context()

        # Construir contexto
        context = {
            "request": request,
            "user": user,
            "is_syncing": sync.is_syncing,
            "user_groups": get_user_groups(),
            **service_context
        }

        cache.set_cache("/", context.copy())
        return templates.TemplateResponse(request=request, name="dashboard.html", context=context)

    except Exception as e:
        logger.error(f"Error cargando dashboard: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error cargando los datos del dashboard.")

# ─── Funciones Auxiliares ────────────────────────────────────────────────────


@router.get("/api/v1/dashboard", response_model=DashboardResponse)
async def dashboard_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager), sync: SyncStateManager = Depends(get_sync_manager)):
    """API JSON para el Dashboard con KPIs y búsqueda rápida."""

    # Intentar recuperar de caché (excluyendo el request)
    cached_ctx = cache.get_cache("/api/v1/dashboard")
    if cached_ctx:
        return DashboardResponse(data=cached_ctx, is_syncing=sync.is_syncing)

    try:
        # Usar el servicio para obtener todo el contexto de negocio
        service = DashboardService(session)
        service_context = service.get_full_context()

        # Filtrar objetos no serializables si los hay
        clean_context = {k: v for k, v in service_context.items() if k not in ('request', 'user', 'is_syncing')}

        cache.set_cache("/api/v1/dashboard", clean_context.copy())
        return DashboardResponse(data=clean_context, is_syncing=sync.is_syncing)

    except Exception as e:
        logger.error(f"Error cargando API dashboard: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error cargando los datos del dashboard.")
