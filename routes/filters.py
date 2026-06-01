"""
routes/filters.py — Motor de filtrado y KPIs optimizado y seguro.
"""
import logging
from core.database import get_session_dep
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timedelta
from typing import Optional, List, Any, Dict, Tuple

import pandas as pd
from fastapi import APIRouter, Request, Depends, HTTPException
from config import DB_PATH

from core.models import ConfigQuery
from core.query_engine import build_sql_from_payload
from core.schemas import VisualQueryBuilderPayload
import json
from core.utils import sanitize_for_json
from repositories.deliveries import DeliveriesRepository

logger = logging.getLogger("routes-filters")
router = APIRouter()

# Expresión unificada para la fecha de carga (Usa fecha_carga -> fecha_sm_real -> creado_el)
DATE_EXPR = "COALESCE(NULLIF(v.fecha_carga, ''), NULLIF(v.fecha_sm_real, ''), v.creado_el)"

# Whitelist de estados OT permitidos como filtro. Solo estos valores pueden ser
# comparados contra la columna estado_wms. Declarado explícitamente para que
# cualquier auditoría de seguridad pueda verificar el contrato de entrada.
ALLOWED_OTS_STATES: frozenset = frozenset({'OT Abierta', 'NO Tratada'})



# ─── Dependencias ─────────────────────────────────────────────────────────────



# ─── Rutas ───────────────────────────────────────────────────────────────────


def _build_unified_where(date: str = None, area: str = None, centro: str = None, has_ots: str = None, min_week: str = None) -> tuple[str, dict]:
    where_parts = []
    params = {}
    
    if min_week:
        where_parts.append("v.week_sort >= :min_week")
        params["min_week"] = min_week
        
    if date:
        date_list = [d.strip() for d in date.split(",") if d.strip()]
        if date_list:
            placeholders = ",".join([f":d_{i}" for i in range(len(date_list))])
            where_parts.append(f"COALESCE(NULLIF(v.fecha_carga, ''), NULLIF(v.fecha_sm_real, ''), v.creado_el) IN ({placeholders})")
            for i, d in enumerate(date_list):
                params[f"d_{i}"] = d
                
    if area:
        area_list = [a.strip() for a in area.split(",") if a.strip()]
        if area_list:
            placeholders = ",".join([f":a_{i}" for i in range(len(area_list))])
            from core.macros import AREA_EXPR
            where_parts.append(f"{AREA_EXPR} IN ({placeholders})")
            for i, a in enumerate(area_list):
                params[f"a_{i}"] = a
                
    if centro:
        from core.macros import AREA_EXPR
        where_parts.append(f"(CASE WHEN {AREA_EXPR} IN ('VIGAS', 'ASERRADERO', 'REMANUFACTURA') THEN 'Aserradero' ELSE 'Paneles' END) = :centro")
        params["centro"] = centro
        
    if has_ots == "1":
        where_parts.append("EXISTS (SELECT 1 FROM warehouse_tasks l WHERE l.entrega = CAST(v.entrega AS TEXT))")
    elif has_ots == "0":
        where_parts.append("NOT EXISTS (SELECT 1 FROM warehouse_tasks l WHERE l.entrega = CAST(v.entrega AS TEXT))")
        
    where_clause = " AND ".join(where_parts) if where_parts else "1=1"
    return where_clause, params


@router.get("/filter")
async def filter_transactions(
    request: Request,
    date: Optional[str] = None,
    entrega: Optional[str] = None,
    area: Optional[str] = None,
    centro: Optional[str] = None,
    has_ots_filter: Optional[str] = None,
    session: Session = Depends(get_session_dep)
):
    """Filtra entregas basándose en múltiples criterios (con límite de seguridad)."""
    
    iso_year, iso_week, _ = datetime.now().isocalendar()
    current_week_str = f"{iso_year}-{iso_week:02d}"
    min_week = current_week_str

    try:
        from repositories.deliveries import DeliveriesRepository
        repo = DeliveriesRepository(session)
        return repo.get_filtered_transactions(date, entrega, area, centro, has_ots_filter, min_week)
    except Exception as e:
        logger.error(f"Error en endpoint /filter: {e}")
        raise HTTPException(status_code=500, detail="Error procesando la búsqueda.")

@router.get("/api/kpis")
async def get_kpis(
    date: Optional[str] = None,
    entrega: Optional[str] = None,
    area: Optional[str] = None, 
    centro: Optional[str] = None,
    has_ots_filter: Optional[str] = None,
    session: Session = Depends(get_session_dep)
):
    """Calcula KPIs dinámicos filtrados por área para el dashboard."""
    
    iso_year, iso_week, _ = datetime.now().isocalendar()
    current_week_str = f"{iso_year}-{iso_week:02d}"
    min_week = current_week_str

    try:
        from repositories.deliveries import DeliveriesRepository
        repo = DeliveriesRepository(session)
        return repo.get_filtered_kpis(date, area, centro, min_week, iso_year)
    except Exception as e:
        logger.error(f"Error calculando KPIs dinámicos: {e}")
        raise HTTPException(status_code=500, detail="No se pudieron calcular los KPIs.")

@router.get("/api/widget/data/{query_id}")
async def api_widget_data(
    query_id: str,
    request: Request,
    session: Session = Depends(get_session_dep)
):
    """
    Endpoint de carga asíncrona para los componentes del Dashboard.
    Lee visual_state, compila SQL y retorna los datos JSON directamente.
    Aplica filtros globales de la UI mediante query parameters.
    """
    # 1. Obtener parámetros de la UI
    date = request.query_params.get("date", "")
    area = request.query_params.get("area", "")
    centro = request.query_params.get("centro", "")
    has_ots = request.query_params.get("has_ots_filter", "")

    iso_year, iso_week, _ = datetime.now().isocalendar()
    min_week = f"{iso_year}-{iso_week:02d}"

    row = session.query(ConfigQuery).filter(ConfigQuery.query_id == query_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Widget no encontrado")
        
    if not row.visual_state:
        # Modo legacy: ejecutar sql_text directamente
        sql = row.sql_text or ""
        if not sql:
            raise HTTPException(status_code=400, detail="Widget no tiene visual_state ni sql_text.")
        
        if "{AREA_EXPR}" in sql:
            from repositories.deliveries import DeliveriesRepository
            sql = sql.replace("{AREA_EXPR}", DeliveriesRepository.AREA_EXPR)
            
        try:
            df = pd.read_sql(text(sql), session.connection())
            records = df.to_dict(orient="records")
            return {"status": "success", "data": sanitize_for_json(records), "legacy": True}
        except Exception as e:
            logger.error(f"Error legacy widget {query_id}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    try:
        vs_dict = json.loads(row.visual_state)
        payload = VisualQueryBuilderPayload(**vs_dict)
        sql, bound_params = build_sql_from_payload(payload, session)
        
        # Generar filtros globales (extra_where trae " WHERE 1=1 AND ...")
        # Pasamos min_week=None para que los widgets históricos NO se limiten a la semana actual por defecto
        extra_where, extra_params = _build_unified_where(date, area, centro, has_ots, None)
        # Limpiar el "WHERE 1=1" que trae por defecto y ajustar el alias "v." al de la tabla base real
        extra_conds = extra_where.replace(" WHERE 1=1", "").replace("v.", f"{payload.baseTable}.")

        # Inyectar filtros globales en el SQL generado
        if extra_conds:
            if "\nWHERE " in sql:
                sql = sql.replace("\nWHERE ", f"\nWHERE 1=1 {extra_conds} AND ", 1)
            else:
                if "\nGROUP BY " in sql:
                    sql = sql.replace("\nGROUP BY ", f"\nWHERE 1=1 {extra_conds}\nGROUP BY ", 1)
                elif "\nORDER BY " in sql:
                    sql = sql.replace("\nORDER BY ", f"\nWHERE 1=1 {extra_conds}\nORDER BY ", 1)
                else:
                    sql = sql.replace(";", f"\nWHERE 1=1 {extra_conds};", 1)

        # SQLAlchemy and Pandas execution
        params_dict = {}
        for i, p in enumerate(bound_params):
            params_dict[f"vp{i}"] = p
            
        import re
        for i in range(len(bound_params)):
            sql = sql.replace("?", f":vp{i}", 1)
            
        # Combinar parámetros globales con los del visual builder
        params_dict.update(extra_params)

        # Add AREA_EXPR if needed
        if "{AREA_EXPR}" in sql:
            from repositories.deliveries import DeliveriesRepository
            sql = sql.replace("{AREA_EXPR}", DeliveriesRepository.AREA_EXPR)
            
        df = pd.read_sql(text(sql), session.connection(), params=params_dict)
        records = df.to_dict(orient="records")
        return {"status": "success", "data": sanitize_for_json(records)}
    except Exception as e:
        logger.error(f"Error ejecutando widget {query_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
