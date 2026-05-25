import pandas as pd
from sqlalchemy import text
from core.db_config_manager import get_setting
from .base import BaseRepository

class DeliveriesRepository(BaseRepository):
    """
    Repositorio para el dominio de Entregas (outbound_deliveries).

    ── Patrón de fallback SQL ────────────────────────────────────────────────
    Cada método que soporta personalización vía Analytics Studio usa:
      self._sql("query_id", fallback_sql_literal)

    El flujo es: config_queries BD → fallback_sql_literal (visible inline).
    No hay dict intermedio (_FALLBACK_QUERIES): el SQL de fallback está junto
    al método que lo consume, lo que facilita la auditoría y el mantenimiento.

    ── Seguridad de AREA_EXPR ────────────────────────────────────────────────
    El override _sql() de esta clase interpola {AREA_EXPR} en el SQL devuelto.
    AREA_EXPR es una constante de clase hardcodeada (no user input), por lo que
    la interpolación es segura. Los valores de usuario siempre van como bind params.
    ──────────────────────────────────────────────────────────────────────────
    """

    AREA_EXPR = """CASE 
        WHEN (SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(COALESCE(NULLIF(v.ubicacion_area, ''), NULLIF(v.ubicacion_bin_1, ''), NULLIF(v.ubicacion_bin, '')), 1, 6)) IS NOT NULL 
        THEN (SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(COALESCE(NULLIF(v.ubicacion_area, ''), NULLIF(v.ubicacion_bin_1, ''), NULLIF(v.ubicacion_bin, '')), 1, 6))
        WHEN v.area_negocio IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.area_negocio
        WHEN v.ubicacion_area IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_area
        WHEN v.ubicacion_bin_1 IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin_1
        WHEN v.ubicacion_bin IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin
        ELSE 'S/N' 
    END"""

    def _sql(self, query_id: str, fallback: str) -> str:
        """
        Obtiene SQL desde config_queries con fallback explícito.
        Si el SQL obtenido contiene {AREA_EXPR}, lo reemplaza con la constante
        de clase AREA_EXPR (hardcodeada, segura para interpolación).
        """
        sql = super()._sql(query_id, fallback)
        if sql and "{AREA_EXPR}" in sql:
            sql = sql.replace("{AREA_EXPR}", self.AREA_EXPR)
        return sql

    def _get_sla_threshold(self) -> int:
        return int(get_setting("SLA_THRESHOLD", 2))

    def get_sla_audit_records(self, year: str, late: bool = True, limit: int = 500, where_clause: str = None, where_params: dict = None) -> pd.DataFrame:
        try:
            self.session.execute(text("CREATE INDEX IF NOT EXISTS idx_warehouse_tasks_entrega ON warehouse_tasks(entrega)"))
        except Exception:
            pass

        operator = ">" if late else "<="
        
        # Incorporar where_clause y reemplazar el LEFT JOIN a DeliverySummary si se usa en where_clause
        join_ds = "LEFT JOIN DeliverySummary ds ON CAST(v.entrega AS TEXT) = ds.entrega_id" if where_clause and "ds." in where_clause else ""
        
        # Limpiar where_clause para evitar "AND WHERE"
        clean_where = where_clause.replace("WHERE ", "") if where_clause else ""
        
        query = f"""
            SELECT v.entrega, v.autor, {self.AREA_EXPR} as area_negocio, v.creado_el, v.fecha_sm_real as salida_mercancias, v.material,
            v.denominacion as texto_breve, v.dias_retraso, :sla_lim as sla_limit,
            CASE WHEN EXISTS(
                SELECT 1 FROM warehouse_tasks l 
                WHERE l.entrega = CAST(v.entrega AS TEXT)
            ) THEN 1 ELSE 0 END as has_ots
            FROM outbound_deliveries v 
            {join_ds}
            WHERE v.dias_retraso {operator} :sla_lim AND v.fecha_carga LIKE :year 
            {f"AND {clean_where}" if clean_where else ""}
            ORDER BY v.dias_retraso DESC 
            LIMIT :limit
        """
        
        params = {"sla_lim": self._get_sla_threshold(), "year": year, "limit": limit}
        if where_params:
            params.update(where_params)
            
        return pd.read_sql(text(query), self.session.connection(), params=params)

