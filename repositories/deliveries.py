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

    def get_area_stats(self, year: str) -> pd.DataFrame:
        query = f"""
            SELECT 
                area,
                COUNT(DISTINCT entrega) as total_entregas,
                COUNT(DISTINCT fecha_carga) as dias_activos,
                SUM(CASE WHEN max_retraso <= ? THEN 1 ELSE 0 END) as ontime,
                SUM(CASE WHEN max_retraso > ? THEN 1 ELSE 0 END) as late
            FROM (
                SELECT 
                    {self.AREA_EXPR} as area,
                    v.entrega,
                    MAX(v.fecha_carga) as fecha_carga,
                    MAX(v.dias_retraso) as max_retraso
                FROM outbound_deliveries v
                WHERE v.fecha_carga LIKE ?
                GROUP BY area, v.entrega
            )
            WHERE area IS NOT NULL
            GROUP BY area
            ORDER BY total_entregas DESC
        """
        return pd.read_sql(query, self.session.connection(), params=(self._get_sla_threshold(), self._get_sla_threshold(), year))

    def get_total_active_days(self, year: str) -> int:
        query = "SELECT COUNT(DISTINCT fecha_carga) as d FROM outbound_deliveries WHERE fecha_carga LIKE ?"
        df = pd.read_sql(query, self.session.connection(), params=(year,))
        return int(df.iloc[0]['d']) if not df.empty else 0

    def get_sla_stats(self, year: str) -> pd.DataFrame:
        query = f"""
            SELECT
                SUM(CASE WHEN dias_retraso <= ? THEN 1 ELSE 0 END) as ontime,
                SUM(CASE WHEN dias_retraso > ?  THEN 1 ELSE 0 END) as late,
                COUNT(*) as total
            FROM (
                SELECT entrega, MAX(dias_retraso) as dias_retraso
                FROM outbound_deliveries
                WHERE dias_retraso IS NOT NULL AND fecha_carga LIKE ?
                GROUP BY entrega
            )
        """
        return pd.read_sql(query, self.session.connection(), params=(self._get_sla_threshold(), self._get_sla_threshold(), year))

    def get_top_authors(self, year: str) -> pd.DataFrame:
        fallback = f"""
            SELECT autor as name, COUNT(DISTINCT entrega) as entregas, COUNT(*) as num_lineas,
            (SELECT {self.AREA_EXPR} FROM outbound_deliveries v WHERE v.autor=outbound_deliveries.autor AND v.fecha_carga LIKE ?
             GROUP BY 1 ORDER BY COUNT(*) DESC LIMIT 1) as area
            FROM outbound_deliveries 
            WHERE fecha_carga LIKE ? 
            GROUP BY autor 
            ORDER BY entregas DESC 
            LIMIT 5
        """
        return pd.read_sql(self._sql("vl_top_authors", fallback), self.session.connection().connection, params=(year, year))

    def get_dates_counts(self, year: str) -> pd.DataFrame:
        query = f"SELECT {self.AREA_EXPR} as area, v.fecha_carga, COUNT(v.material) as count FROM outbound_deliveries v WHERE v.fecha_carga LIKE ? GROUP BY area, v.fecha_carga"
        return pd.read_sql(query, self.session.connection(), params=(year,))

    def get_top_locations(self, year: str) -> pd.DataFrame:
        fallback = f"""
            SELECT 
                {self.AREA_EXPR} as area, 
                v.ubicacion_bin as ubicacion, 
                v.material, 
                v.denominacion as texto_breve_de_material,
                COUNT(*) as num_items 
            FROM outbound_deliveries v
            WHERE v.ubicacion_bin IS NOT NULL AND v.ubicacion_bin != '' AND v.fecha_carga LIKE ?
            GROUP BY area, v.ubicacion_bin, v.material, texto_breve_de_material 
            HAVING area IS NOT NULL
            ORDER BY num_items DESC 
            LIMIT 100
        """
        return pd.read_sql(self._sql("vl_top_locations", fallback), self.session.connection().connection, params=(year,))

    def get_top_materials_by_area(self, year: str) -> pd.DataFrame:
        query = f"""
            SELECT {self.AREA_EXPR} as area,
            v.denominacion as material, COUNT(*) as frequency FROM outbound_deliveries v
            WHERE v.denominacion IS NOT NULL AND v.denominacion != '' AND v.fecha_carga LIKE ?
            GROUP BY area, material 
            HAVING area IS NOT NULL
            ORDER BY area, frequency DESC
        """
        return pd.read_sql(query, self.session.connection(), params=(year,))

    def get_area_material_mapping(self, year: str) -> pd.DataFrame:
        query = f"""
            SELECT {self.AREA_EXPR} as area, v.material as cod_mat,
            v.denominacion as material, COUNT(*) as qty FROM outbound_deliveries v
            WHERE v.denominacion IS NOT NULL AND v.denominacion != '' AND v.fecha_carga LIKE ?
            GROUP BY area, cod_mat, material 
            ORDER BY qty DESC
        """
        return pd.read_sql(query, self.session.connection(), params=(year,))

    def get_user_material_mapping(self, year: str) -> pd.DataFrame:
        query = """
            SELECT autor as user, material as cod_mat,
            denominacion as material, COUNT(*) as qty FROM outbound_deliveries
            WHERE denominacion IS NOT NULL AND denominacion != '' AND fecha_carga LIKE ?
            GROUP BY user, cod_mat, material 
            ORDER BY qty DESC
        """
        return pd.read_sql(query, self.session.connection(), params=(year,))

    def get_sla_audit_records(self, year: str, late: bool = True, limit: int = 500) -> pd.DataFrame:
        try:
            self.session.execute(text("CREATE INDEX IF NOT EXISTS idx_warehouse_tasks_entrega ON warehouse_tasks(entrega)"))
        except Exception:
            pass

        operator = ">" if late else "<="
        query = f"""
            SELECT v.entrega, v.autor, {self.AREA_EXPR} as area_negocio, v.creado_el, v.fecha_sm_real as salida_mercancias, v.material,
            v.denominacion as texto_breve, v.dias_retraso, {self._get_sla_threshold()} as sla_limit,
            CASE WHEN EXISTS(
                SELECT 1 FROM warehouse_tasks l 
                WHERE l.entrega = CAST(v.entrega AS TEXT)
            ) THEN 1 ELSE 0 END as has_ots
            FROM outbound_deliveries v 
            WHERE v.dias_retraso {operator} ? AND v.fecha_carga LIKE ? 
            ORDER BY v.dias_retraso DESC 
            LIMIT ?
        """
        return pd.read_sql(query, self.session.connection(), params=(self._get_sla_threshold(), year, limit))

    def get_monthly_evolution(self) -> pd.DataFrame:
        fallback = f"""
            SELECT 
                substr(v.fecha_carga,7,4) as year,
                substr(v.fecha_carga,4,2) as month,
                substr(v.fecha_carga,7,4) || '-' || substr(v.fecha_carga,4,2) as label,
                {self.AREA_EXPR} as area,
                COUNT(DISTINCT v.entrega) as entregas,
                COUNT(DISTINCT v.fecha_carga) as dias_activos
            FROM outbound_deliveries v
            WHERE v.fecha_carga IS NOT NULL AND v.fecha_carga != ''
            GROUP BY year, month, area
            ORDER BY year ASC, month ASC
        """
        return pd.read_sql(self._sql("vl_monthly_evolution", fallback), self.session.connection().connection)

    def get_weekly_evolution(self) -> pd.DataFrame:
        fallback = f"""
            SELECT 
                v.week_sort,
                MAX(v.week_label) as label,
                {self.AREA_EXPR} as area,
                COUNT(DISTINCT v.entrega) as entregas
            FROM outbound_deliveries v
            WHERE v.week_sort IS NOT NULL AND v.week_sort != ''
            GROUP BY v.week_sort, area
            ORDER BY v.week_sort ASC
        """
        return pd.read_sql(self._sql("vl_weekly_evolution", fallback), self.session.connection().connection)

    def get_wms_status_distribution(self, year: str) -> pd.DataFrame:
        query = """
            SELECT 
                estado_wms,
                COUNT(DISTINCT entrega) as cantidad
            FROM outbound_deliveries
            WHERE fecha_carga LIKE ? AND estado_wms IS NOT NULL AND estado_wms != ''
            GROUP BY estado_wms
            ORDER BY cantidad DESC
        """
        return pd.read_sql(query, self.session.connection(), params=(year,))

    def get_lead_time_by_area(self, year: str) -> pd.DataFrame:
        query = f"""
            SELECT 
                {self.AREA_EXPR} as area,
                AVG(v.dias_retraso) as avg_lead_time
            FROM outbound_deliveries v
            WHERE v.fecha_carga LIKE ? AND v.dias_retraso IS NOT NULL
            GROUP BY area
            ORDER BY avg_lead_time DESC
        """
        return pd.read_sql(query, self.session.connection(), params=(year,))

    def get_sla_trend(self) -> pd.DataFrame:
        fallback = f"""
            SELECT 
                v.week_sort,
                MAX(v.week_label) as label,
                COUNT(*) as material_count,
                (SUM(CASE WHEN v.dias_retraso <= ? THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as efficiency
            FROM outbound_deliveries v
            WHERE v.week_sort IS NOT NULL AND v.week_sort != ''
            GROUP BY v.week_sort
            ORDER BY v.week_sort ASC
        """
        return pd.read_sql(self._sql("vl_sla_trend", fallback), self.session.connection().connection, params=(self._get_sla_threshold(),))

    def get_author_sla_correlation(self) -> pd.DataFrame:
        query = f"""
            SELECT 
                v.autor as name,
                COUNT(DISTINCT v.entrega) as volume,
                AVG(v.dias_retraso) as avg_delay,
                {self.AREA_EXPR} as area
            FROM outbound_deliveries v
            WHERE v.autor IS NOT NULL AND v.dias_retraso IS NOT NULL
            GROUP BY v.autor
            HAVING volume > 2
            ORDER BY volume DESC
            LIMIT 50
        """
        return pd.read_sql(query, self.session.connection())

    def get_volume_delay_trend(self) -> pd.DataFrame:
        query = f"""
            SELECT 
                week_sort,
                MAX(week_label) as label,
                COUNT(material) as volume,
                (SUM(CASE WHEN dias_retraso <= ? THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as efficiency
            FROM outbound_deliveries
            WHERE week_sort IS NOT NULL AND week_sort != ''
            GROUP BY week_sort
            ORDER BY week_sort ASC
        """
        return pd.read_sql(query, self.session.connection(), params=(self._get_sla_threshold(),))

    def get_sla_trend_by_area(self) -> pd.DataFrame:
        fallback = f"""
            SELECT 
                v.week_sort,
                MAX(v.week_label) as label,
                {self.AREA_EXPR} as area,
                SUM(CASE WHEN v.dias_retraso <= ? THEN 1 ELSE 0 END) as ontime_count,
                COUNT(*) as total_count,
                (SUM(CASE WHEN v.dias_retraso <= ? THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as efficiency
            FROM outbound_deliveries v
            WHERE v.week_sort IS NOT NULL AND v.week_sort != ''
            GROUP BY v.week_sort, area
            ORDER BY v.week_sort ASC
        """
        return pd.read_sql(self._sql("vl_sla_area_trend", fallback), self.session.connection().connection, params=(self._get_sla_threshold(), self._get_sla_threshold()))

    def get_sla_monthly_trend(self) -> pd.DataFrame:
        sql = f"""
            SELECT 
                substr(fecha_carga,7,4) || '-' || substr(fecha_carga,4,2) as month_sort,
                MAX(substr(fecha_carga,4,2) || '-' || substr(fecha_carga,7,4)) as label,
                COUNT(DISTINCT entrega) as material_count,
                ROUND(SUM(CASE WHEN dias_retraso <= {self._get_sla_threshold()} THEN 1.0 ELSE 0.0 END) * 100.0 / NULLIF(COUNT(*), 0), 1) as efficiency
            FROM outbound_deliveries
            WHERE fecha_carga IS NOT NULL AND fecha_carga != ''
            GROUP BY month_sort
            ORDER BY month_sort ASC
        """
        return pd.read_sql(sql, self.session.connection())

    def get_sla_monthly_trend_by_area(self) -> pd.DataFrame:
        fallback = f"""
            SELECT 
                substr(v.fecha_carga,7,4) || '-' || substr(v.fecha_carga,4,2) as month_sort,
                MAX(substr(v.fecha_carga,4,2) || '-' || substr(v.fecha_carga,7,4)) as label,
                {self.AREA_EXPR} as area,
                SUM(CASE WHEN v.dias_retraso <= ? THEN 1 ELSE 0 END) as ontime_count,
                COUNT(*) as total_count,
                (SUM(CASE WHEN v.dias_retraso <= ? THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as efficiency
            FROM outbound_deliveries v
            WHERE v.fecha_carga IS NOT NULL AND v.fecha_carga != ''
            GROUP BY month_sort, area
            ORDER BY month_sort ASC
        """
        return pd.read_sql(self._sql("vl_sla_area_monthly_trend", fallback), self.session.connection().connection, params=(self._get_sla_threshold(), self._get_sla_threshold()))
