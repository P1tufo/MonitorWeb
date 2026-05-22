"""
core/pdf_queries.py — Consultas SQL robustas para generación de reportes PDF.
"""
import logging
import pandas as pd
import sqlite3
from typing import List, Optional, Any

# Configuración de Logging
logger = logging.getLogger("pdf-queries")

# Expresión unificada de área enriquecida (Sincronizada con el Dashboard y queries_deliveries.py)
AREA_EXPR = """CASE 
    WHEN (SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(COALESCE(NULLIF(v.ubicacion_area, ''), NULLIF(v.ubicacion_bin_1, ''), NULLIF(v.ubicacion_bin, '')), 1, 6)) IS NOT NULL 
    THEN (SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(COALESCE(NULLIF(v.ubicacion_area, ''), NULLIF(v.ubicacion_bin_1, ''), NULLIF(v.ubicacion_bin, '')), 1, 6))
    WHEN v.area_negocio IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.area_negocio
    WHEN v.ubicacion_area IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_area
    WHEN v.ubicacion_bin_1 IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin_1
    WHEN v.ubicacion_bin IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin
    ELSE 'S/N' 
END"""

def get_deliveries_for_bulk(
    conn: sqlite3.Connection, 
    date: Optional[str] = None, 
    area: Optional[str] = None, 
    centro: Optional[str] = None, 
    has_ots_filter: Optional[str] = None, 
    entrega_query: Optional[str] = None
) -> pd.DataFrame:
    """
    Construye y ejecuta la query dinámica para filtrar entregas en reportes masivos.
    Implementa validaciones de seguridad y manejo de errores.
    """
    query = "SELECT v.entrega, MAX(v.autor) as autor FROM outbound_deliveries v WHERE 1=1"
    params: List[Any] = []

    try:
        if date:
            date_list = [d.strip() for d in date.split(",") if d.strip()]
            if date_list:
                placeholders = ','.join(['?'] * len(date_list))
                query += f" AND COALESCE(NULLIF(v.fecha_carga, ''), NULLIF(v.fecha_sm_real, ''), v.creado_el) IN ({placeholders})"
                params.extend(date_list)

        if area:
            area_list = [a.strip() for a in area.split(",") if a.strip()]
            if area_list:
                placeholders = ','.join(['?'] * len(area_list))
                query += f" AND {AREA_EXPR} IN ({placeholders})"
                params.extend(area_list)

        if centro:
            query += f" AND (CASE WHEN {AREA_EXPR} IN ('VIGAS', 'ASERRADERO', 'REMANUFACTURA') THEN 'Aserradero' ELSE 'Paneles' END) = ?"
            params.append(centro)

        if has_ots_filter == '1':
            query += " AND EXISTS (SELECT 1 FROM warehouse_tasks l WHERE CAST(l.entrega AS INTEGER) = v.entrega)"
        elif has_ots_filter == '0':
            query += " AND NOT EXISTS (SELECT 1 FROM warehouse_tasks l WHERE CAST(l.entrega AS INTEGER) = v.entrega)"

        if entrega_query:
            query += " AND v.entrega LIKE ?"
            params.append(f"%{entrega_query}%")

        query += " GROUP BY v.entrega"
        return pd.read_sql(query, conn, params=params)

    except Exception as e:
        logger.error(f"Error construyendo query masiva de PDFs: {e}")
        return pd.DataFrame(columns=['entrega', 'autor'])

def get_area_lookup(conn: sqlite3.Connection) -> pd.DataFrame:
    """Obtiene el área de negocio dominante para cada entrega."""
    query = f"""
        SELECT 
            v.entrega, 
            MAX({AREA_EXPR}) as area_negocio 
        FROM outbound_deliveries v 
        GROUP BY v.entrega
    """
    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        logger.error(f"Error en lookup de áreas: {e}")
        return pd.DataFrame(columns=['entrega', 'area_negocio'])

def get_picking_items(conn: sqlite3.Connection, entrega_ids: List[str]) -> pd.DataFrame:
    """Obtiene materiales por entrega (desglosado) para el picking list, asegurando cantidades visibles."""
    if not entrega_ids:
        return pd.DataFrame()

    try:
        placeholders = ','.join(['?'] * len(entrega_ids))
        query = f"""
            SELECT
                v.pos_,
                COALESCE(NULLIF(v.ubicacion_bin, ''), '(Sin ubicacion)') as ubicacion,
                v.material,
                COALESCE(v.denominacion, '') as descripcion,
                v.cantidad as cantidad,
                COALESCE(v.umb, '') as umb,
                COALESCE({AREA_EXPR}, 'SIN ÁREA') as area,
                v.entrega
            FROM outbound_deliveries v
            WHERE v.entrega IN ({placeholders})
            ORDER BY area ASC, v.ubicacion_bin ASC, v.material ASC
        """

        df = pd.read_sql(query, conn, params=entrega_ids)
        
        # Sanitizar cantidad: convertir " " o "" a "0" para que no se vea en blanco
        def _sanitize_qty(val):
            if not val or str(val).strip() == "": return "0"
            return str(val).strip()

        df['cantidad'] = df['cantidad'].apply(_sanitize_qty)
        return df

    except Exception as e:
        logger.error(f"Error obteniendo items de picking desglosados: {e}")
        return pd.DataFrame()
