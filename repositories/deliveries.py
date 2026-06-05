import pandas as pd
from sqlalchemy import text
from core.db_config_manager import get_setting
from .base import BaseRepository
from core.macros import inject_macros, AREA_EXPR

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

    def build_unified_where(self, date: str, area: str, centro: str, has_ots_filter: str, min_week: str):
        where_clause = " WHERE 1=1"
        raw_params = []
        from core.macros import AREA_EXPR as area_expr
        DATE_EXPR = "COALESCE(NULLIF(v.fecha_carga, ''), NULLIF(v.fecha_sm_real, ''), v.creado_el)"

        def _add_param(value):
            key = f"p{len(raw_params)}"
            raw_params.append(value)
            return f":{key}"

        if not date or date.strip() == "":
            if min_week is not None:
                where_clause += f" AND v.week_sort >= {_add_param(min_week)}"
        else:
            date_list = [d.strip() for d in date.split(",") if d.strip()]
            if date_list:
                phs = ", ".join(_add_param(d) for d in date_list)
                where_clause += f" AND {DATE_EXPR} IN ({phs})"
            elif min_week is not None:
                where_clause += f" AND v.week_sort >= {_add_param(min_week)}"

        if has_ots_filter and has_ots_filter.strip() in {'OT Abierta', 'NO Tratada'}:
            where_clause += f" AND v.estado_wms = {_add_param(has_ots_filter.strip())}"

        if area and area.strip() != "":
            area_list = [a.strip() for a in area.split(",") if a.strip()]
            if area_list:
                phs = ", ".join(_add_param(a) for a in area_list)
                where_clause += f" AND {area_expr} IN ({phs})"

        if centro and centro.strip() != "":
            where_clause += f" AND (CASE WHEN {area_expr} IN ('VIGAS', 'ASERRADERO', 'REMANUFACTURA') THEN 'Aserradero' ELSE 'Paneles' END) = {_add_param(centro.strip())}"

        where_params = {f"p{i}": v for i, v in enumerate(raw_params)}
        return where_clause, where_params

    def get_filtered_transactions(self, date: str, entrega: str, area: str, centro: str, has_ots_filter: str, min_week: str) -> list:
        where_clause, where_params = self.build_unified_where(date, area, centro, has_ots_filter, min_week)
        DATE_EXPR = "COALESCE(NULLIF(v.fecha_carga, ''), NULLIF(v.fecha_sm_real, ''), v.creado_el)"
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
                        WHEN v.centro_costo IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.centro_costo
                        WHEN v.ubicacion_bin_1 IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin_1
                        WHEN v.ubicacion_bin IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin
                        ELSE 'S/N' 
                    END as area_val
                FROM outbound_deliveries v
                LEFT JOIN config_cost_center_mapping m ON SUBSTR(COALESCE(NULLIF(v.centro_costo, ''), NULLIF(v.ubicacion_bin_1, ''), NULLIF(v.ubicacion_bin, '')), 1, 6) = m.center_code
            ),
            DeliverySummary AS (
                SELECT CAST(entrega AS TEXT) as entrega_id, MAX(area_val) as area_negocio
                FROM BestArea GROUP BY entrega_id
            )
        """

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
        df = pd.read_sql(text(query), self.session.connection(), params=where_params)
        return df.to_dict(orient='records')

    def get_filtered_kpis(self, date: str, area: str, centro: str, min_week: str, iso_year: int) -> dict:
        where_clause, where_params = self.build_unified_where(date, area, centro, None, min_week)
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
        
        q_year = f"""
            SELECT COUNT(DISTINCT v.entrega) as kpi_year_deliveries, COUNT(v.material) as kpi_year_materials
            FROM outbound_deliveries v
            WHERE substr(v.week_sort, 1, 4) = :yr
        """

        k_df   = pd.read_sql(text(q_kpi),  self.session.connection(), params=where_params).iloc[0]
        k_year = pd.read_sql(text(q_year), self.session.connection(), params={"yr": str(iso_year)}).iloc[0]

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

    def get_delivery_by_id(self, entrega: str) -> pd.DataFrame:
        query = "SELECT * FROM outbound_deliveries WHERE entrega = :entrega"
        return pd.read_sql(text(query), self.session.connection(), params={"entrega": str(entrega)})


    def get_weekly_intensity_chart(self, year: int) -> dict:
        """Prepara los datos para el gráfico de intensidad semanal."""
        query = """
            SELECT week_sort, week_label, area_negocio, count(distinct entrega) as entregas
            FROM outbound_deliveries
            WHERE week_sort IS NOT NULL AND area_negocio IS NOT NULL
            AND CAST(substr(week_sort, 1, 4) AS INTEGER) >= ?
            GROUP BY week_sort, week_label, area_negocio
            ORDER BY week_sort
        """
        df = pd.read_sql(query, self.session.connection().connection, params=(year,))
        
        if df.empty:
            return {"chart_labels": [], "chart_datasets": []}

        weeks = df[['week_sort', 'week_label']].drop_duplicates()
        labels = weeks['week_label'].tolist()
        
        import itertools
        colors = ['#BFB800', '#EA7600', '#5DBAA9', '#B46A5F', '#5142f5', '#F3D01C']
        color_gen = itertools.cycle(colors)
        
        datasets = []
        for area in df['area_negocio'].unique():
            area_map = {r['week_label']: r['entregas'] for _, r in df[df['area_negocio'] == area].iterrows()}
            color = next(color_gen)
            datasets.append({
                "label": str(area),
                "data": [area_map.get(lbl, 0) for lbl in labels],
                "backgroundColor": color + "B3",
                "borderColor": color,
                "borderWidth": 1,
            })
        
        return {"chart_labels": labels, "chart_datasets": datasets}

    def get_dashboard_selectors(self, min_week: str) -> dict:
        """Obtiene listas únicas de fechas y áreas, además de mapeos de autores y centros."""
        dates_df = pd.read_sql("""
            SELECT DISTINCT COALESCE(NULLIF(fecha_carga, ''), NULLIF(fecha_sm_real, ''), creado_el) as fecha
            FROM outbound_deliveries 
            WHERE fecha IS NOT NULL
            ORDER BY substr(fecha, 7, 4) DESC, substr(fecha, 4, 2) DESC, substr(fecha, 1, 2) DESC
            LIMIT 500
        """, self.session.connection().connection)
        
        areas_df = pd.read_sql("""
            SELECT DISTINCT 
                CASE 
                    WHEN m.business_area IS NOT NULL THEN m.business_area
                    WHEN v.area_negocio IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.area_negocio
                    WHEN v.centro_costo IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.centro_costo
                    WHEN v.ubicacion_bin_1 IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin_1
                    WHEN v.ubicacion_bin IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin
                    ELSE 'S/N' 
                END as area_negocio,
                v.centro
            FROM outbound_deliveries v
            LEFT JOIN config_cost_center_mapping m ON SUBSTR(COALESCE(NULLIF(v.centro_costo, ''), NULLIF(v.ubicacion_bin_1, ''), NULLIF(v.ubicacion_bin, '')), 1, 6) = m.center_code
            WHERE area_negocio IS NOT NULL
        """, self.session.connection().connection)
        
        area_centro_map = {}
        for _, row in areas_df.iterrows():
            a, c = str(row['area_negocio']), row['centro']
            if not c or str(c).strip() in ["", "nan", "None"]:
                c = 'Aserradero' if a in ['VIGAS', 'ASERRADERO', 'REMANUFACTURA'] else 'Paneles'
            area_centro_map[a] = c

        try:
            autores_df = pd.read_sql("SELECT autor, area_negocio FROM autor_area_mapping ORDER BY frequency DESC", self.session.connection().connection)
            autores_map = autores_df.drop_duplicates(subset=['autor']).to_dict(orient='records')
        except:
            autores_map = []
        
        return {
            "dates": dates_df['fecha'].tolist(),
            "areas": [str(a) for a in areas_df['area_negocio'].tolist() if str(a).strip()],
            "area_centro_map": area_centro_map,
            "autores_map": autores_map,
            "default_dates": set(pd.read_sql("SELECT DISTINCT COALESCE(NULLIF(fecha_carga, ''), NULLIF(fecha_sm_real, ''), creado_el) as fecha FROM outbound_deliveries WHERE week_sort >= ?", self.session.connection().connection, params=(min_week,))['fecha'].tolist())
        }
