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

def _build_unified_where(date: str, area: str, centro: str, has_ots_filter: str, min_week: Optional[str]):
    """
    Construye la cláusula WHERE a nivel de MATERIAL.

    ── Invariante de Seguridad (Anti SQL Injection) ───────────────────────────────
    Todos los valores del usuario se añaden como bind params nombrados
    (:p0, :p1, ...) devueltos como dict. Nunca se interpolan en el SQL.
    Las únicas variables en el string SQL son constantes del módulo.
    ──────────────────────────────────────────────────────────────────
    Retorna: (where_clause: str, where_params: dict)
    """
    where_clause = " WHERE 1=1"
    raw_params: List[Any] = []  # Lista interna; se convierte a dict al final

    # Expresión para obtener el área del material actual (v).
    # ⚠ SOLO contiene literales hardcodeados — ningún input del usuario.
    area_expr = """CASE 
        WHEN (SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(COALESCE(NULLIF(v.ubicacion_area, ''), NULLIF(v.ubicacion_bin_1, ''), NULLIF(v.ubicacion_bin, '')), 1, 6)) IS NOT NULL 
        THEN (SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(COALESCE(NULLIF(v.ubicacion_area, ''), NULLIF(v.ubicacion_bin_1, ''), NULLIF(v.ubicacion_bin, '')), 1, 6))
        WHEN v.area_negocio IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.area_negocio
        WHEN v.ubicacion_area IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_area
        WHEN v.ubicacion_bin_1 IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin_1
        WHEN v.ubicacion_bin IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin
        ELSE 'S/N' 
    END"""

    def _add_param(value) -> str:
        """Añade un valor a raw_params y devuelve el placeholder :pN."""
        key = f"p{len(raw_params)}"
        raw_params.append(value)
        return f":{key}"

    # 1. Filtro de Fecha — valores del usuario → bind params nombrados
    if not date or date.strip() == "":
        if min_week is not None:
            ph = _add_param(min_week)
            where_clause += f" AND v.week_sort >= {ph}"
    else:
        date_list = [d.strip() for d in date.split(",") if d.strip()]
        if date_list:
            phs = ", ".join(_add_param(d) for d in date_list)
            where_clause += f" AND {DATE_EXPR} IN ({phs})"
        else:
            if min_week is not None:
                ph = _add_param(min_week)
                where_clause += f" AND v.week_sort >= {ph}"

    # 2. Filtro de Estado OT — validado contra whitelist estática antes de usarse
    if has_ots_filter and has_ots_filter.strip() in ALLOWED_OTS_STATES:
        ph = _add_param(has_ots_filter)
        where_clause += f" AND v.estado_wms = {ph}"

    # 3. Filtro de Área — valores del usuario → bind params nombrados
    if area and area.strip() != "":
        area_list = [a.strip() for a in area.split(",") if a.strip()]
        if area_list:
            phs = ", ".join(_add_param(a) for a in area_list)
            where_clause += f" AND {area_expr} IN ({phs})"

    # 4. Filtro de Centro — valor del usuario → bind param nombrado
    if centro and centro.strip() != "":
        ph = _add_param(centro)
        where_clause += f" AND (CASE WHEN {area_expr} IN ('VIGAS', 'ASERRADERO', 'REMANUFACTURA') THEN 'Aserradero' ELSE 'Paneles' END) = {ph}"

    # Convertir lista interna a dict nombrado {:p0: v0, :p1: v1, ...}
    where_params = {f"p{i}": v for i, v in enumerate(raw_params)}
    return where_clause, where_params


# ─── Dependencias ─────────────────────────────────────────────────────────────



# ─── Rutas ───────────────────────────────────────────────────────────────────

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
        where_clause, where_params = _build_unified_where(date, area, centro, has_ots_filter, min_week)

        # Filtro adicional de Entrega (solo para la tabla)
        if entrega:
            p_ent1 = f"p{len(where_params)}"
            where_params[p_ent1] = f"%{entrega}%"
            p_ent2 = f"p{len(where_params)}"
            where_params[p_ent2] = f"%{entrega}%"
            where_clause += f" AND (CAST(v.entrega AS TEXT) LIKE :{p_ent1} OR CAST(v.material AS TEXT) LIKE :{p_ent2})"

        q_base_join = """
            WITH BestArea AS (
                SELECT 
                    v.entrega,
                    CASE 
                        WHEN m.business_area IS NOT NULL THEN m.business_area
                        WHEN v.area_negocio IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.area_negocio
                        WHEN v.ubicacion_area IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_area
                        WHEN v.ubicacion_bin_1 IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin_1
                        WHEN v.ubicacion_bin IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin
                        ELSE 'S/N' 
                    END as area_val
                FROM outbound_deliveries v
                LEFT JOIN config_cost_center_mapping m ON SUBSTR(COALESCE(NULLIF(v.ubicacion_area, ''), NULLIF(v.ubicacion_bin_1, ''), NULLIF(v.ubicacion_bin, '')), 1, 6) = m.center_code
            ),
            DeliverySummary AS (
                SELECT CAST(entrega AS TEXT) as entrega_id, MAX(area_val) as area_negocio
                FROM BestArea GROUP BY entrega_id
            )
        """

        # 2. Consulta para la Tabla
        query = q_base_join + f"""
            SELECT v.entrega,
                   {DATE_EXPR} as fe_carga,
                   ds.area_negocio,
                   COALESCE(v.estado_wms, 'Pendiente') as estado_wms,
                   COUNT(v.material) as num_items,
                   CASE WHEN EXISTS (SELECT 1 FROM warehouse_tasks l WHERE CAST(l.entrega AS TEXT) = CAST(v.entrega AS TEXT)) THEN 1 ELSE 0 END as has_ots
            FROM outbound_deliveries v 
            LEFT JOIN DeliverySummary ds ON CAST(v.entrega AS TEXT) = ds.entrega_id
            {where_clause}
            GROUP BY v.entrega
            ORDER BY v.week_sort DESC, {DATE_EXPR} DESC, v.entrega DESC
            LIMIT 500
        """

        df = pd.read_sql(text(query), session.connection(), params=where_params)
        return df.to_dict(orient='records')

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
        # Pasamos None a has_ots_filter para que los KPIs NO se filtren por el estado de OT.
        # Esto permite que los indicadores siempre muestren el desglose real del Centro/Área,
        # mientras que la tabla de abajo sí se filtrará.
        where_clause, where_params = _build_unified_where(date, area, centro, None, min_week)

        # SQL para KPIs optimizado: Una sola pasada con agregación condicional
        # Eliminamos DeliverySummary de los KPIs para contar MATERIALES reales individualmente
        q_kpi = f"""
            SELECT 
                COUNT(DISTINCT v.entrega) as kpi_deliveries,
                COUNT(v.material) as kpi_materials,
                COUNT(DISTINCT CASE WHEN v.estado_wms = 'OT Abierta' THEN v.entrega END) as sub_del_abierta,
                COUNT(CASE WHEN v.estado_wms = 'OT Abierta' THEN v.material END) as sub_mat_abierta,
                COUNT(DISTINCT CASE WHEN v.estado_wms = 'NO Tratada' THEN v.entrega END) as sub_del_no_tratada,
                COUNT(CASE WHEN v.estado_wms = 'NO Tratada' THEN v.material END) as sub_mat_no_tratada,
                COUNT(DISTINCT CASE WHEN v.dias_retraso <= 2 AND v.estado_wms = 'Contabilizado' THEN v.entrega END) as sub_del_reunido,
                COUNT(CASE WHEN v.dias_retraso <= 2 AND v.estado_wms = 'Contabilizado' THEN v.material END) as sub_mat_reunido,
                COUNT(DISTINCT CASE WHEN v.dias_retraso > 2 AND v.estado_wms = 'Contabilizado' THEN v.entrega END) as sub_del_atrasado,
                COUNT(CASE WHEN v.dias_retraso > 2 AND v.estado_wms = 'Contabilizado' THEN v.material END) as sub_mat_atrasado,
                COUNT(DISTINCT CASE WHEN v.estado_wms = 'OT Abierta' AND v.dias_retraso > 2 THEN v.entrega END) as sub_del_critico,
                COUNT(CASE WHEN v.estado_wms = 'OT Abierta' AND v.dias_retraso > 2 THEN v.material END) as sub_mat_critico
            FROM outbound_deliveries v
            {where_clause}
        """
        
        # SQL anual (filtro propio de tiempo, sin filtros del usuario)
        q_year = f"""
            SELECT COUNT(DISTINCT v.entrega) as kpi_year_deliveries, COUNT(v.material) as kpi_year_materials
            FROM outbound_deliveries v
            WHERE substr(v.week_sort, 1, 4) = :yr
        """

        # Ejecución
        k_df   = pd.read_sql(text(q_kpi),  session.connection(), params=where_params).iloc[0]
        k_year = pd.read_sql(text(q_year), session.connection(), params={"yr": str(iso_year)}).iloc[0]

        def fmt(n): return f"{int(n or 0):,}".replace(",", ".")

        return {
            "kpi_deliveries": fmt(k_df['kpi_deliveries']),
            "kpi_materials": fmt(k_df['kpi_materials']),
            "kpi_year_deliveries": fmt(k_year['kpi_year_deliveries']),
            "kpi_year_materials": fmt(k_year['kpi_year_materials']),
            "sub_del_abierta": fmt(k_df['sub_del_abierta']),
            "sub_del_no_tratada": fmt(k_df['sub_del_no_tratada']),
            "sub_mat_abierta": fmt(k_df['sub_mat_abierta']),
            "sub_mat_no_tratada": fmt(k_df['sub_mat_no_tratada']),
            "sub_del_reunido": fmt(k_df['sub_del_reunido']),
            "sub_mat_reunido": fmt(k_df['sub_mat_reunido']),
            "sub_del_atrasado": fmt(k_df['sub_del_atrasado']),
            "sub_mat_atrasado": fmt(k_df['sub_mat_atrasado']),
            "sub_del_critico": fmt(k_df['sub_del_critico']),
            "sub_mat_critico": fmt(k_df['sub_mat_critico']),
        }

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
