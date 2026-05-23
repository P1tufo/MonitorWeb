import pandas as pd
from typing import Final, Tuple
from sqlalchemy import text
from core.wms_config import get_setting
from .base import BaseRepository

class InventoryRepository(BaseRepository):
    """Repositorio para el dominio de Inventario (ex-Movimientos)."""

    # ── Constantes de CMV (configurables vía config_settings) ────────────────
    def get_cmv_prod(self) -> str:
        return get_setting("CMV_PROD", "201")

    def get_cmv_mant(self) -> str:
        return get_setting("CMV_MANT", "261")

    def get_cmv_consumos(self) -> Tuple[str, ...]:
        return (self.get_cmv_prod(), self.get_cmv_mant())

    def get_cmv_reversas(self) -> Tuple[str, ...]:
        rev_str = get_setting("CMV_REVERSAS", "202,262,102,302,304")
        return tuple(r.strip() for r in rev_str.split(","))

    def check_table_exists(self) -> bool:
        try:
            res = self.session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='inventory_movements'")).fetchone()
            return res is not None
        except Exception:
            return False

    # ── SQL de fallback: constantes privadas nombradas ────────────────────────
    # Si config_queries no tiene una query personalizada para el query_id dado,
    # se usa este SQL hardcodeado como fallback explícito.
    # El flujo es siempre: config_queries BD → fallback de constante de clase.
    # No hay dict intermedio ni override opaco de _sql().

    _SQL_VOLUMEN_STATS = (
        "SELECT tipo_operacion, COUNT(material) as total_qty, COUNT(*) as num_tx "
        "FROM inventory_movements GROUP BY tipo_operacion ORDER BY total_qty DESC"
    )

    _SQL_AREA_STATS_PROD = (
        "SELECT COALESCE(m.business_area, i.ce_coste, 'MIXTO') as area, COUNT(i.material) as num_tx, "
        "SUM(i.cantidad) as sum_qty, COUNT(DISTINCT i.fe_contab) as active_days "
        "FROM inventory_movements i "
        "LEFT JOIN config_cost_center_mapping m ON i.ce_coste LIKE m.center_code || '%' "
        "WHERE i.cmv = ? GROUP BY area ORDER BY num_tx DESC"
    )

    _SQL_CONSUMOS_ABC = (
        "SELECT COALESCE(m.business_area, i.ce_coste, 'MIXTO') as area, i.material as cod_mat, i.texto_breve_material as material, "
        "COUNT(i.material) as qty FROM inventory_movements i "
        "LEFT JOIN config_cost_center_mapping m ON i.ce_coste LIKE m.center_code || '%' "
        "WHERE i.cmv IN (?, ?) AND i.material IS NOT NULL AND i.material != '' "
        "GROUP BY area, cod_mat, material ORDER BY qty DESC"
    )

    _SQL_DOW_STATS = (
        "SELECT CAST(strftime('%w', substr(fe_contab, 7, 4) || '-' || "
        "substr(fe_contab, 4, 2) || '-' || substr(fe_contab, 1, 2)) AS INTEGER) as dow, "
        "COUNT(material) as qty FROM inventory_movements "
        "WHERE cmv IN (?, ?) AND length(fe_contab) >= 10 GROUP BY dow"
    )

    _SQL_PM_TYPE_RECORDS = (
        "SELECT CASE WHEN cmv = ? THEN 'Producción' ELSE 'Mantención' END as type, "
        "material as cod_mat, texto_breve_material as material, COUNT(material) as qty "
        "FROM inventory_movements WHERE cmv IN (?, ?) "
        "GROUP BY type, cod_mat, material ORDER BY qty DESC"
    )

    _SQL_AREA_MATERIAL_PROD = (
        "SELECT COALESCE(ce_coste, 'OTRO') as area, material as cod_mat, "
        "texto_breve_material as material, COUNT(*) as qty "
        "FROM inventory_movements WHERE cmv = ? "
        "GROUP BY area, cod_mat, material ORDER BY qty DESC"
    )

    _SQL_LOCATION_SUMMARY = (
        "SELECT COALESCE(alm, 'S/U') as ubi, material as cod_mat, "
        "texto_breve_material as material, COUNT(*) as total_qty "
        "FROM inventory_movements WHERE ubi != 'S/U' "
        "GROUP BY ubi, cod_mat, material ORDER BY total_qty DESC"
    )



    def get_volumen_stats(self) -> pd.DataFrame:
        return pd.read_sql(self._sql("inv_volumen_stats", self._SQL_VOLUMEN_STATS), self.session.connection().connection)

    def get_area_stats_prod(self) -> pd.DataFrame:
        return pd.read_sql(self._sql("inv_area_stats_prod", self._SQL_AREA_STATS_PROD), self.session.connection().connection, params=(self.get_cmv_prod(),))

    def get_material_consumos_abc(self) -> pd.DataFrame:
        return pd.read_sql(self._sql("inv_consumos_abc", self._SQL_CONSUMOS_ABC), self.session.connection().connection, params=self.get_cmv_consumos())

    def get_top_users(self, start_year: str = '2026') -> pd.DataFrame:
        query = f"""
            SELECT i.usuario as user, COALESCE(m.business_area, i.ce_coste, 'MIXTO') as area,
            SUM(CASE WHEN cmv IN (?, ?) THEN 1 ELSE 0 END) as qty,
            SUM(CASE WHEN cmv IN (?, ?, ?, ?, ?) 
                AND NOT (
                    UPPER(COALESCE(texto_cab_documento, '')) LIKE '%CIERRE%' OR
                    UPPER(COALESCE(texto_cab_documento, '')) LIKE '%REGU%' OR
                    UPPER(COALESCE(texto_cab_documento, '')) LIKE '%DEV%' OR
                    UPPER(COALESCE(texto_cab_documento, '')) LIKE '%ERROR%' OR
                    UPPER(COALESCE(texto_cab_documento, '')) LIKE '%ANUL%' OR
                    UPPER(COALESCE(referencia, '')) LIKE '%CIERRE%' OR
                    UPPER(COALESCE(referencia, '')) LIKE '%REGU%' OR
                    UPPER(COALESCE(referencia, '')) LIKE '%DEV%' OR
                    UPPER(COALESCE(referencia, '')) LIKE '%ERROR%' OR
                    UPPER(COALESCE(referencia, '')) LIKE '%ANUL%'
                ) THEN 1 ELSE 0 END) as anulaciones
            FROM inventory_movements i
            LEFT JOIN config_cost_center_mapping m ON i.ce_coste LIKE m.center_code || '%'
            WHERE usuario IS NOT NULL AND usuario != '' AND substr(fe_contab, 7, 4) >= ?
            AND NOT (
                UPPER(COALESCE(texto_cab_documento, '')) LIKE '%CIERRE%' OR
                UPPER(COALESCE(texto_cab_documento, '')) LIKE '%REGU%' OR
                UPPER(COALESCE(texto_cab_documento, '')) LIKE '%DEV%' OR
                UPPER(COALESCE(texto_cab_documento, '')) LIKE '%ERROR%' OR
                UPPER(COALESCE(texto_cab_documento, '')) LIKE '%ANUL%' OR
                UPPER(COALESCE(referencia, '')) LIKE '%CIERRE%' OR
                UPPER(COALESCE(referencia, '')) LIKE '%REGU%' OR
                UPPER(COALESCE(referencia, '')) LIKE '%DEV%' OR
                UPPER(COALESCE(referencia, '')) LIKE '%ERROR%' OR
                UPPER(COALESCE(referencia, '')) LIKE '%ANUL%'
            )
            GROUP BY user, COALESCE(m.business_area, i.ce_coste, 'MIXTO') HAVING qty > 0 ORDER BY qty DESC LIMIT 10
        """
        params = self.get_cmv_consumos() + self.get_cmv_reversas() + (start_year,)
        return pd.read_sql(query, self.session.connection(), params=params)

    def get_trend_stats(self, start_year: str = '2025') -> pd.DataFrame:
        query = """
            SELECT substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) as periodo,
            SUM(CASE WHEN cmv = '101' THEN 1 ELSE 0 END) as entradas,
            SUM(CASE WHEN cmv = ? THEN 1 ELSE 0 END) as salidas_prod,
            SUM(CASE WHEN cmv = ? THEN 1 ELSE 0 END) as salidas_mant
            FROM inventory_movements 
            WHERE length(fe_contab) >= 10 AND substr(fe_contab, 7, 4) >= ?
            GROUP BY periodo ORDER BY periodo ASC
        """
        return pd.read_sql(query, self.session.connection(), params=(self.get_cmv_prod(), self.get_cmv_mant(), start_year))

    def get_dow_stats(self) -> pd.DataFrame:
        return pd.read_sql(self._sql("inv_dow_stats", self._SQL_DOW_STATS), self.session.connection().connection, params=self.get_cmv_consumos())

    def get_pm_type_material_records(self) -> pd.DataFrame:
        return pd.read_sql(self._sql("inv_pm_type_records", self._SQL_PM_TYPE_RECORDS), self.session.connection().connection, params=(self.get_cmv_prod(), self.get_cmv_prod(), self.get_cmv_mant()))

    def get_area_material_mapping_201(self) -> pd.DataFrame:
        return pd.read_sql(self._sql("inv_area_material_prod", self._SQL_AREA_MATERIAL_PROD), self.session.connection().connection, params=(self.get_cmv_prod(),))

    def get_user_material_mapping(self, users: Tuple[str, ...]) -> pd.DataFrame:
        if not users: return pd.DataFrame()
        placeholders = ','.join(['?'] * len(users))
        query = f"""
            SELECT usuario as user, material as cod_mat, texto_breve_material as material, 
                   COUNT(*) as total_qty
            FROM inventory_movements WHERE usuario IN ({placeholders}) AND cmv IN (?, ?)
            GROUP BY user, cod_mat, material ORDER BY total_qty DESC
        """
        return pd.read_sql(query, self.session.connection(), params=users + self.get_cmv_consumos())

    def get_location_material_summary(self) -> pd.DataFrame:
        return pd.read_sql(self._sql("inv_location_summary", self._SQL_LOCATION_SUMMARY), self.session.connection().connection)

    def get_total_active_days(self) -> int:
        res = self.session.execute(text("SELECT COUNT(DISTINCT fe_contab) FROM inventory_movements")).fetchone()
        return res[0] if res else 1
