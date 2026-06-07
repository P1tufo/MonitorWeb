import logging

import pandas as pd
from sqlalchemy import text

logger = logging.getLogger(__name__)

from core.db_config_manager import get_setting
from core.macros import AREA_EXPR, inject_macros

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

    def _sql(self, query_id: str, fallback: str) -> str:
        """
        Obtiene SQL desde config_queries con fallback explícito.
        Si el SQL obtenido contiene {AREA_EXPR}, lo reemplaza con la constante
        de clase AREA_EXPR (hardcodeada, segura para interpolación).
        """
        sql = super()._sql(query_id, fallback)
        sql = inject_macros(sql)

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
            SELECT v.entrega, v.autor, {AREA_EXPR} as area_negocio, v.creado_el, v.fecha_sm_real as salida_mercancias, v.material,
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

    def get_deliveries_for_bulk(self, date: str = None, area: str = None, centro: str = None, has_ots_filter: str = None, entrega_query: str = None) -> pd.DataFrame:
        query = "SELECT v.entrega, MAX(v.autor) as autor FROM outbound_deliveries v WHERE 1=1"
        params = []
        try:
            if date:
                date_list = [d.strip() for d in date.split(",") if d.strip()]
                if date_list:
                    placeholders = ",".join(["?"] * len(date_list))
                    query += f" AND COALESCE(NULLIF(v.fecha_carga, ''), NULLIF(v.fecha_sm_real, ''), v.creado_el) IN ({placeholders})"
                    params.extend(date_list)
            else:
                from datetime import datetime
                iso_year, iso_week, _ = datetime.now().isocalendar()
                min_week = f"{iso_year}-{iso_week:02d}"
                query += " AND (v.week_sort >= ? OR v.week_sort IS NULL)"
                params.append(min_week)
            if area:
                area_list = [a.strip() for a in area.split(",") if a.strip()]
                if area_list:
                    placeholders = ",".join(["?"] * len(area_list))
                    from core.macros import AREA_EXPR
                    query += f" AND {AREA_EXPR} IN ({placeholders})"
                    params.extend(area_list)
            if centro:
                from core.macros import AREA_EXPR
                query += f" AND (CASE WHEN {AREA_EXPR} IN ('VIGAS', 'ASERRADERO', 'REMANUFACTURA') THEN 'Aserradero' ELSE 'Paneles' END) = ?"
                params.append(centro)
            if has_ots_filter in ('OT Abierta', 'NO Tratada'):
                query += " AND v.estado_wms = ?"
                params.append(has_ots_filter)
            if entrega_query:
                query += " AND v.entrega LIKE ?"
                params.append(f"%{entrega_query}%")
            query += " GROUP BY v.entrega"
            return pd.read_sql(query, self.session.connection().connection, params=tuple(params))
        except Exception as e:
            logger.error(f"Error en get_deliveries_for_bulk: {e}")
            return pd.DataFrame(columns=['entrega', 'autor'])

    def get_area_lookup(self) -> pd.DataFrame:
        from core.macros import AREA_EXPR
        query = f"SELECT v.entrega, MAX({AREA_EXPR}) as area_negocio FROM outbound_deliveries v GROUP BY v.entrega"
        try:
            return pd.read_sql(query, self.session.connection().connection)
        except Exception as e:
            logger.error(f"Error en get_area_lookup: {e}")
            return pd.DataFrame(columns=['entrega', 'area_negocio'])

    def get_picking_items(self, entrega_ids: list) -> pd.DataFrame:
        if not entrega_ids:
            return pd.DataFrame()
        try:
            from core.macros import AREA_EXPR
            placeholders = ",".join(["?"] * len(entrega_ids))
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
            df = pd.read_sql(query, self.session.connection().connection, params=tuple(entrega_ids))
            df['cantidad'] = df['cantidad'].apply(lambda val: "0" if not val or str(val).strip() == "" else str(val).strip())
            return df
        except Exception as e:
            logger.error(f"Error en get_picking_items: {e}")
            return pd.DataFrame()

    def get_delivery_by_id(self, entrega: str) -> pd.DataFrame:
        query = "SELECT * FROM outbound_deliveries WHERE entrega = :entrega"
        return pd.read_sql(text(query), self.session.connection(), params={"entrega": str(entrega)})
