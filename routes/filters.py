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

logger = logging.getLogger("routes-filters")
router = APIRouter()

# Expresión unificada para la fecha de carga (Usa fecha_carga -> fecha_sm_real -> creado_el)
DATE_EXPR = "COALESCE(NULLIF(v.fecha_carga, ''), NULLIF(v.fecha_sm_real, ''), v.creado_el)"

# Whitelist de estados OT permitidos como filtro. Solo estos valores pueden ser
# comparados contra la columna estado_wms. Declarado explícitamente para que
# cualquier auditoría de seguridad pueda verificar el contrato de entrada.
ALLOWED_OTS_STATES: frozenset = frozenset({'OT Abierta', 'NO Tratada'})

def _build_unified_where(date: str, area: str, centro: str, has_ots_filter: str, min_week: str):
    """
    Construye la cláusula WHERE a nivel de MATERIAL.

    ── Invariante de Seguridad (Anti SQL Injection) ──────────────────────────
    Esta función es segura contra inyección SQL porque:
      1. Todos los valores suministrados por el usuario (date, area, centro,
         has_ots_filter) se agregan SIEMPRE a `where_params` como bind params (?).
         Nunca se interpolan directamente en el string `where_clause`.
      2. Las únicas variables interpoladas en el string SQL son:
         - DATE_EXPR  → constante hardcodeada definida en el módulo (línea 19).
         - area_expr  → expresión CASE construida con literales hardcodeados,
                        sin ningún input del usuario dentro de la expresión.
         - placeholders → solo caracteres '?' separados por comas (ej: "?,?,?").
      3. has_ots_filter se valida contra ALLOWED_OTS_STATES (whitelist estática)
         antes de añadirse al WHERE. Si no está en la lista, se ignora.
    ──────────────────────────────────────────────────────────────────────────
    NOTA: Para filtros de área/centro, usamos una expresión que mapea el área del
    material actual basándose en su ubicacion_area o area_negocio individual.
    """
    where_clause = " WHERE 1=1"
    where_params = []

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

    # 1. Filtro de Fecha — valores del usuario → bind params (?)
    if not date or date.strip() == "":
        where_clause += " AND v.week_sort >= ?"
        where_params.append(min_week)
    else:
        date_list = [d.strip() for d in date.split(",") if d.strip()]
        if date_list:
            placeholders = ','.join(['?'] * len(date_list))
            where_clause += f" AND {DATE_EXPR} IN ({placeholders})"
            where_params.extend(date_list)
        else:
            where_clause += " AND v.week_sort >= ?"
            where_params.append(min_week)

    # 2. Filtro de Estado OT — validado contra whitelist estática antes de usarse
    if has_ots_filter and has_ots_filter.strip() in ALLOWED_OTS_STATES:
        where_clause += " AND v.estado_wms = ?"
        where_params.append(has_ots_filter)

    # 3. Filtro de Área — valores del usuario → bind params (?)
    if area and area.strip() != "":
        area_list = [a.strip() for a in area.split(",") if a.strip()]
        if area_list:
            placeholders = ','.join(['?'] * len(area_list))
            where_clause += f" AND {area_expr} IN ({placeholders})"
            where_params.extend(area_list)

    # 4. Filtro de Centro — valor del usuario → bind param (?)
    if centro and centro.strip() != "":
        where_clause += f" AND (CASE WHEN {area_expr} IN ('VIGAS', 'ASERRADERO', 'REMANUFACTURA') THEN 'Aserradero' ELSE 'Paneles' END) = ?"
        where_params.append(centro)

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
            where_clause += " AND (CAST(v.entrega AS TEXT) LIKE ? OR CAST(v.material AS TEXT) LIKE ?)"
            where_params.extend([f"%{entrega}%", f"%{entrega}%"])

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
        where_clause, where_params = _build_unified_where(date, area, centro, has_ots_filter, min_week)

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
        
        # KPI Anual (Separado porque tiene su propio filtro de tiempo)
        # Nota: Aquí no aplicamos el filtro de fecha/estado para mantener el total anual
        q_year = f"""
            SELECT COUNT(DISTINCT v.entrega) as kpi_year_deliveries, COUNT(v.material) as kpi_year_materials
            FROM outbound_deliveries v
            WHERE substr(v.week_sort, 1, 4) = ?
        """
        
        # Ejecución
        k_df = pd.read_sql(text(q_kpi), session.connection(), params=where_params).iloc[0]
        k_year = pd.read_sql(text(q_year), session.connection(), params=[str(iso_year)]).iloc[0]

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
