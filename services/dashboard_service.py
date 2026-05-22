import logging
from sqlalchemy.orm import Session
import pandas as pd
from sqlalchemy import text
import itertools
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger("services-dashboard")

class DashboardService:
    """
    Orquestador del dashboard principal de Entregas (vista operativa).

    ── Rol en la arquitectura ────────────────────────────────────────────────
    Este servicio es el punto de entrada para cargar la página principal.
    A diferencia de DeliveriesService e InventoryService, sus KPIs son
    estáticos del sistema operativo (conteos de la BD) y NO se sobrescriben
    con queries del Analytics Studio (config_queries).

    Por este motivo, este servicio no consume core/query_engine ni
    config_queries directamente. Si en el futuro se quieren KPIs dinámicos
    en el dashboard principal, deben agregarse aquí siguiendo el patrón
    establecido en DeliveriesService._prepare_kpis.
    ──────────────────────────────────────────────────────────────────────────
    """
    def __init__(self, session: Session):
        self.session = session

    def get_full_context(self) -> Dict[str, Any]:
        """Orquesta la carga de todos los datos necesarios para el dashboard."""
        iso_year, iso_week, _ = datetime.now().isocalendar()
        current_week_str = f"{iso_year}-{iso_week:02d}"
        min_week = current_week_str

        chart_data = self._prepare_weekly_chart(iso_year)
        kpis = self._calculate_dashboard_kpis(min_week, str(iso_year))
        selectors = self._prepare_selectors(min_week)
        recent_tx = self._get_recent_transactions(min_week)

        return {
            "transactions": recent_tx,
            **chart_data,
            **kpis,
            **selectors
        }

    def _prepare_weekly_chart(self, year: int) -> Dict[str, Any]:
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

    def _calculate_dashboard_kpis(self, start_week: str, year_str: str) -> Dict[str, Any]:
        """Calcula los indicadores clave de rendimiento (KPIs) desde una semana base."""
        q_kpi = """
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
            WHERE v.week_sort >= ?
        """
        
        q_year = """
            SELECT COUNT(DISTINCT v.entrega) as kpi_year_deliveries, COUNT(v.material) as kpi_year_materials
            FROM outbound_deliveries v
            WHERE substr(v.week_sort, 1, 4) = ?
        """
        
        k_df = pd.read_sql(q_kpi, self.session.connection().connection, params=[start_week]).iloc[0]
        k_year = pd.read_sql(q_year, self.session.connection().connection, params=[year_str]).iloc[0]

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

    def _prepare_selectors(self, min_week: str) -> Dict[str, Any]:
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
                    WHEN v.ubicacion_area IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_area
                    WHEN v.ubicacion_bin_1 IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin_1
                    WHEN v.ubicacion_bin IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin
                    ELSE 'S/N' 
                END as area_negocio,
                v.centro
            FROM outbound_deliveries v
            LEFT JOIN config_cost_center_mapping m ON SUBSTR(COALESCE(NULLIF(v.ubicacion_area, ''), NULLIF(v.ubicacion_bin_1, ''), NULLIF(v.ubicacion_bin, '')), 1, 6) = m.center_code
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

    def _get_recent_transactions(self, week_str: str) -> List[Dict]:
        """Obtiene el listado de las últimas entregas para la tabla principal."""
        query = """
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
                SELECT entrega, MAX(area_val) as area_negocio
                FROM BestArea GROUP BY entrega
            )
            SELECT v.entrega,
                   COALESCE(NULLIF(v.fecha_carga, ''), NULLIF(v.fecha_sm_real, ''), v.creado_el) as fe_carga,
                   ds.area_negocio,
                   COALESCE(v.estado_wms, 'Pendiente') as estado_wms,
                   COUNT(v.material) as num_items,
                   CASE WHEN EXISTS (SELECT 1 FROM warehouse_tasks l WHERE CAST(l.entrega AS INTEGER) = v.entrega) THEN 1 ELSE 0 END as has_ots
            FROM outbound_deliveries v
            LEFT JOIN DeliverySummary ds ON v.entrega = ds.entrega
            WHERE v.week_sort >= ?
            GROUP BY v.entrega
            ORDER BY 
                     substr(fe_carga, 7, 4) DESC, 
                     substr(fe_carga, 4, 2) DESC, 
                     substr(fe_carga, 1, 2) DESC,
                     v.entrega DESC
            LIMIT 1000
        """
        df = pd.read_sql(query, self.session.connection().connection, params=(week_str,))
        return df.to_dict(orient='records')
