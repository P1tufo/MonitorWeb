from sqlalchemy.orm import Session
import pandas as pd
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.utils import sanitize_for_json
from core.state import get_app_state
from repositories import DeliveriesRepository

from core.query_engine import get_bound_params_from_visual_state, extract_metric_value

logger = logging.getLogger("services-deliveries")

class DeliveriesService:
    def __init__(self, session: Session):
        self.session = session
        self.conn = session.connection().connection

    def get_full_context(self) -> Dict[str, Any]:
        """Genera el contexto de datos completo para Entregas."""
        logger.debug("Iniciando generación de contexto Entregas...")
        state = get_app_state()
        
        try:
            # 1. Periodo dinámico
            res_p = self.conn.execute("SELECT substr(fecha_carga,4,2), substr(fecha_carga,7,4) FROM outbound_deliveries WHERE fecha_carga IS NOT NULL ORDER BY substr(fecha_carga,7,4) DESC, substr(fecha_carga,4,2) DESC LIMIT 1").fetchone()
            if res_p:
                month_part, year_part = res_p
                current_year = int(year_part)
                raw_year = year_part
                raw_month = month_part
                cm_label = f"{month_part}/{year_part}"
            else:
                now = datetime.now()
                current_year = now.year
                raw_year = str(current_year)
                raw_month = f"{now.month:02d}"
                cm_label = f"{raw_month}/{raw_year}"
            
            yr_mask = f"%{raw_year}"
            cm_mask = f"%-{raw_month}-{raw_year}"

            # 2. Cálculos
            area_stats_df = self._prepare_area_stats(yr_mask, cm_mask)
            total_dias = DeliveriesRepository(self.session).get_total_active_days(yr_mask)
            sla_df = DeliveriesRepository(self.session).get_sla_stats(yr_mask)
            kpis = self._calculate_kpis(sla_df, area_stats_df, total_dias)
            
            # Sobrescribir con KPIs dinámicos de la base de datos de configuración (Analytics Studio)
            val_total = self._execute_dynamic_kpi('vl_kpi_total', (yr_mask,), raw_year)
            if val_total is not None:
                kpis["kpi_total"] = int(val_total)
                if total_dias > 0:
                    kpis["kpi_avg"] = round(kpis["kpi_total"] / total_dias, 1)
                    
            val_eff = self._execute_dynamic_kpi('vl_kpi_eff', (yr_mask,), raw_year)
            if val_eff is not None:
                kpis["kpi_eff"] = round(val_eff, 1)
                
            val_ontime = self._execute_dynamic_kpi('vl_kpi_ontime', (yr_mask,), raw_year)
            if val_ontime is not None:
                kpis["kpi_ontime"] = int(val_ontime)
                
            val_late = self._execute_dynamic_kpi('vl_kpi_late', (yr_mask,), raw_year)
            if val_late is not None:
                kpis["kpi_late"] = int(val_late)
            
            authors = self._prepare_authors(yr_mask, cm_mask)
            locations = self._prepare_locations(yr_mask, cm_mask)
            materials = self._prepare_materials_by_area(yr_mask, cm_mask)
            
            # Gráficos
            dates_df = DeliveriesRepository(self.session).get_dates_counts(yr_mask)
            chart_labels_vl, chart_datasets_vl = [], []
            if not dates_df.empty:
                top_areas = area_stats_df.head(7)['area'].tolist() if not area_stats_df.empty else []
                dates_df['area_group'] = dates_df['area'].apply(lambda x: x if x in top_areas else 'OTROS')
                pivot_df = dates_df.pivot_table(index='fecha_carga', columns='area_group', values='count', aggfunc='sum').fillna(0)
                chart_labels_vl = pivot_df.index.tolist()
                colors = ["#5DBAA9", "#EA7600", "#3A5AAB", "#EAB308", "#EC4899", "#8B5CF6", "#10B981"]
                for i, area in enumerate(pivot_df.columns):
                    chart_datasets_vl.append({"label": area, "data": pivot_df[area].tolist(), "backgroundColor": colors[i % len(colors)]})

            # DOW Heatmap - Promedios Semanales
            weekdays_data = [0.0] * 5
            weekdays_data_cm = [0.0] * 5
            if not dates_df.empty:
                dates_df['dt'] = pd.to_datetime(dates_df['fecha_carga'], format='%d-%m-%Y', errors='coerce')
                dates_df = dates_df.dropna(subset=['dt'])
                dates_df['dow'] = dates_df['dt'].dt.dayofweek
                dates_df['dow_adj'] = dates_df['dow'].apply(lambda d: 0 if d >= 5 else d)
                
                # Promedios
                dow_stats = dates_df.groupby('dow_adj')['count'].mean().to_dict()
                cm_dates = dates_df[dates_df['fecha_carga'].str.contains(cm_mask.replace('%',''))]
                dow_stats_cm = cm_dates.groupby('dow_adj')['count'].mean().to_dict() if not cm_dates.empty else {}
                
                for d in range(5):
                    weekdays_data[d] = round(dow_stats.get(d, 0.0), 1)
                    weekdays_data_cm[d] = round(dow_stats_cm.get(d, 0.0), 1)
                    
                # Limpiar columna de Timestamp para evitar errores de serialización JSON
                dates_export_df = dates_df.drop(columns=['dt'])
            else:
                dates_export_df = dates_df.copy()


            # Mapeos detallados
            # Mapeos detallados (Sanitizados)
            ubic_map = sanitize_for_json(DeliveriesRepository(self.session).get_top_locations(yr_mask))
            area_map = sanitize_for_json(DeliveriesRepository(self.session).get_area_material_mapping(yr_mask))
            user_map = sanitize_for_json(DeliveriesRepository(self.session).get_user_material_mapping(yr_mask))
            areas_vl = area_stats_df['area'].unique().tolist() if not area_stats_df.empty else []

            # Evolución Mensual y Semanal
            monthly_df = DeliveriesRepository(self.session).get_monthly_evolution()
            if not monthly_df.empty:
                # El DataFrame ahora viene agrupado por (label, area). Agrupamos globalmente para compatibilidad.
                monthly_global = monthly_df.groupby('label')['entregas'].sum().reset_index()
                # Ordenar cronológicamente (label es YYYY-MM)
                monthly_global = monthly_global.sort_values('label')
                monthly_labels = monthly_global['label'].tolist()
                monthly_data = monthly_global['entregas'].tolist()
            else:
                monthly_labels, monthly_data = [], []
            monthly_raw_json = sanitize_for_json(monthly_df)
            weekly_df = DeliveriesRepository(self.session).get_weekly_evolution()
            if not weekly_df.empty:
                weekly_global = weekly_df.groupby('label')['entregas'].sum().reset_index()
                weekly_global = weekly_global.sort_values('label')
                weekly_labels = weekly_global['label'].tolist()
                weekly_data = weekly_global['entregas'].tolist()
            else:
                weekly_labels, weekly_data = [], []
            weekly_raw_json = sanitize_for_json(weekly_df)
            
            # Nuevos Análisis Avanzados
            wms_status_df = DeliveriesRepository(self.session).get_wms_status_distribution(yr_mask)
            wms_labels = wms_status_df['estado_wms'].tolist()
            wms_data = wms_status_df['cantidad'].tolist()
            
            sla_trend_df = DeliveriesRepository(self.session).get_sla_trend()
            sla_trend_labels = sla_trend_df['label'].tolist()
            sla_trend_data = [round(float(x), 1) for x in sla_trend_df['efficiency'].tolist()]
            sla_trend_count = sla_trend_df['material_count'].tolist() if 'material_count' in sla_trend_df.columns else []
            
            # Nuevas Métricas
            correlation_df = DeliveriesRepository(self.session).get_author_sla_correlation()
            correlation_data = sanitize_for_json(correlation_df) if not correlation_df.empty else []

            sla_area_df = DeliveriesRepository(self.session).get_sla_trend_by_area()
            sla_area_trend_raw_json = sanitize_for_json(sla_area_df)
            sla_area_labels = []
            sla_area_datasets = []
            if not sla_area_df.empty:
                # Usar mean para promediar porcentajes. 
                # IMPORTANTE: No usamos fillna(0) inmediatamente para poder calcular promedios reales ignorando semanas sin datos.
                pivot_sla = sla_area_df.pivot_table(index='label', columns='area', values='efficiency', aggfunc='mean')
                
                # Clip por seguridad
                pivot_sla = pivot_sla.clip(lower=0, upper=100.0)
                
                sla_area_labels = pivot_sla.index.tolist()
                colors = ["#5DBAA9", "#EA7600", "#3A5AAB", "#EAB308", "#EC4899", "#8B5CF6", "#10B981"]
                for i, area in enumerate(pivot_sla.columns):
                    # El promedio real se calcula sobre los datos existentes (Pandas ignora NaNs automáticamente)
                    avg_val = round(float(pivot_sla[area].mean()), 1) if not pivot_sla[area].isna().all() else 0
                    
                    # Para el gráfico, sí rellenamos con 0 para mostrar la inactividad
                    raw_data = [round(float(x), 1) for x in pivot_sla[area].fillna(0).tolist()]
                    
                    sla_area_datasets.append({
                        "label": area,
                        "avg_kpi": avg_val, 
                        "data": raw_data,
                        "borderColor": colors[i % len(colors)],
                        "backgroundColor": colors[i % len(colors)],
                        "fill": False,
                        "tension": 0.3
                    })
            
            # Promedios para KPIs
            if not monthly_df.empty:
                current_year_str = str(current_year)
                this_year_data = monthly_df[monthly_df['year'] == current_year_str]
                kpis['avg_mensual_año'] = round(this_year_data['entregas'].mean(), 1) if not this_year_data.empty else 0
                
                this_month_str = f"{current_year}-{month_part}"
                this_month_data = monthly_df[monthly_df['label'] == this_month_str]
                if not this_month_data.empty:
                    # Promedio diario del mes actual
                    entregas_mes = this_month_data.iloc[0]['entregas']
                    dias_mes = this_month_data.iloc[0]['dias_activos']
                    kpis['avg_diario_mes'] = round(entregas_mes / dias_mes, 1) if dias_mes > 0 else 0
                else:
                    kpis['avg_diario_mes'] = 0
            else:
                kpis['avg_mensual_año'] = 0
                kpis['avg_diario_mes'] = 0

            # TENDENCIA MENSUAL (VISTA ANUAL)
            sla_monthly_df = DeliveriesRepository(self.session).get_sla_monthly_trend()
            sla_monthly_labels = sla_monthly_df['label'].tolist() if not sla_monthly_df.empty else []
            sla_monthly_data = [round(float(x), 1) for x in sla_monthly_df['efficiency'].tolist()] if not sla_monthly_df.empty else []
            sla_monthly_count = sla_monthly_df['material_count'].tolist() if not sla_monthly_df.empty else []

            sla_area_monthly_df = DeliveriesRepository(self.session).get_sla_monthly_trend_by_area()
            sla_area_monthly_labels = []
            sla_area_monthly_datasets = []
            if not sla_area_monthly_df.empty:
                pivot_sla_m = sla_area_monthly_df.pivot_table(index='label', columns='area', values='efficiency', aggfunc='mean')
                pivot_sla_m = pivot_sla_m.clip(lower=0, upper=100.0)
                sla_area_monthly_labels = pivot_sla_m.index.tolist()
                colors = ["#5DBAA9", "#EA7600", "#3A5AAB", "#EAB308", "#EC4899", "#8B5CF6", "#10B981"]
                for i, area in enumerate(pivot_sla_m.columns):
                    avg_val = round(float(pivot_sla_m[area].mean()), 1) if not pivot_sla_m[area].isna().all() else 0
                    raw_data = [round(float(x), 1) for x in pivot_sla_m[area].fillna(0).tolist()]
                    sla_area_monthly_datasets.append({
                        "label": area,
                        "avg_kpi": avg_val, 
                        "data": raw_data,
                        "borderColor": colors[i % len(colors)],
                        "backgroundColor": colors[i % len(colors)],
                        "fill": False,
                        "tension": 0.3
                    })

            # Contextos secundarios
            from routes.inventory import get_inventory_context
            from routes.tasks import get_tasks_context
            from routes.analytics_proyecciones import get_proyecciones_context
            
            inventory_ctx = get_inventory_context(self.session)
            ots_ctx = get_tasks_context(self.session)
            proy_ctx = get_proyecciones_context()

            # Construir contexto final completo
            context = {
                "area_stats_json": sanitize_for_json(area_stats_df) if not area_stats_df.empty else [],
                "top_authors": authors,
                "top_locations": locations,
                "top_materials": materials,
                "areas_vl": areas_vl,
                "ubicaciones_mapping": ubic_map,
                "area_material_mapping": area_map,
                "user_material_mapping": user_map,
                "weekdays": ["Lun", "Mar", "Mie", "Jue", "Vie"],
                "weekdays_data": weekdays_data,
                "weekdays_data_cm": weekdays_data_cm,
                "chart_labels_vl": chart_labels_vl,
                "chart_datasets_vl": chart_datasets_vl,
                "weekday_mapping": {},
                "weekday_mapping_cm": {},
                "area_material_mapping_cm": {},
                "user_material_mapping_cm": {},
                "ubicaciones_mapping_cm": {},
                "weekday_raw_json": sanitize_for_json(dates_export_df) if not dates_export_df.empty else [],
                "total_dias_activos": total_dias,
                "periodo_actual": cm_label,
                "monthly_labels": monthly_labels,
                "monthly_data": monthly_data,
                "weekly_labels": weekly_labels,
                "weekly_data": weekly_data,
                "wms_labels": wms_labels,
                "wms_data": wms_data,
                "sla_trend_labels": sla_trend_labels,
                "sla_trend_data": sla_trend_data,
                "sla_trend_count": sla_trend_count,
                "sla_area_labels": sla_area_labels,
                "sla_area_datasets": sla_area_datasets,
                "sla_monthly_labels": sla_monthly_labels,
                "sla_monthly_data": sla_monthly_data,
                "sla_monthly_count": sla_monthly_count,
                "sla_area_monthly_labels": sla_area_monthly_labels,
                "sla_area_monthly_datasets": sla_area_monthly_datasets,
                "monthly_raw_json": monthly_raw_json,
                "weekly_raw_json": weekly_raw_json,
                "sla_area_monthly_raw_json": sanitize_for_json(sla_area_monthly_df) if not sla_area_monthly_df.empty else [],
                "sla_area_trend_raw_json": sla_area_trend_raw_json,
                "correlation_data": correlation_data,
                **kpis,
                **inventory_ctx,
                **ots_ctx,
                **proy_ctx
            }
            # Guardar en caché y snapshot de BD
            state.set_cache("/analytics/deliveries", context)
            # save_analytics_snapshot(self.conn, "deliveries", context)
            return context
        except Exception as e:
            logger.error(f"Error generando contexto Entregas: {e}", exc_info=True)
            return {}

    def _execute_dynamic_kpi(self, query_id: str, default_params: tuple, raw_year: str) -> Optional[float]:
        try:
            res = self.conn.execute(f"SELECT sql_text, visual_state FROM config_queries WHERE query_id = '{query_id}'").fetchone()
            if not res:
                return None
            sql_text, visual_state = res
            
            if visual_state:
                import json
                from core.schemas import VisualQueryBuilderPayload
                from core.query_engine import build_sql_from_payload
                vs_dict = json.loads(visual_state)
                payload = VisualQueryBuilderPayload(**vs_dict)
                sql_dyn, bound_params_dyn = build_sql_from_payload(payload, self.session)
                df = pd.read_sql(sql_dyn, self.conn, params=tuple(bound_params_dyn))
            elif sql_text:
                params = ()
                if sql_text.count("?") > 0:
                    params = default_params if len(default_params) == sql_text.count("?") else (default_params[0],) if sql_text.count("?") == 1 else ()
                df = pd.read_sql(sql_text, self.conn, params=params)
            else:
                return None
                
            if not df.empty:
                val = extract_metric_value(df, raw_year)
                if val is not None and not pd.isna(val):
                    return float(val)
            return None
        except Exception as e:
            logger.error(f"Error calculando KPI dinámico {query_id}: {e}")
            return None

    def _prepare_area_stats(self, year, month_str):
        """Prepara el DataFrame de estadísticas por área."""
        df_yr = DeliveriesRepository(self.session).get_area_stats(str(year))
        df_cm = DeliveriesRepository(self.session).get_area_stats(month_str)
        
        if df_yr.empty:
            return pd.DataFrame()
            
        df_yr['promedio_diario'] = (df_yr['total_entregas'] / df_yr['dias_activos'].replace(0, 1)).round(1)
        
        if not df_cm.empty:
            df_cm = df_cm.rename(columns={'total_entregas': 'total_entregas_cm', 'dias_activos': 'dias_activos_cm'})
            merged = pd.merge(df_yr, df_cm[['area', 'total_entregas_cm', 'dias_activos_cm']], on='area', how='left').fillna(0)
            merged['promedio_diario_cm'] = (merged['total_entregas_cm'] / merged['dias_activos_cm'].replace(0, 1)).round(1)
            return merged
        
        # Si no hay datos mensuales, añadir columnas vacías para evitar KeyError
        df_yr['total_entregas_cm'] = 0
        df_yr['dias_activos_cm'] = 0
        df_yr['promedio_diario_cm'] = 0.0
        return df_yr

    def _calculate_kpis(self, sla_df, area_stats_df, total_dias):
        """Calcula el diccionario de KPIs globales de forma segura."""
        kpi_ontime = kpi_late = kpi_eff = 0
        total_q = 0
        
        if not sla_df.empty:
            row = sla_df.iloc[0]
            total_q = int(row.get('total', 0) or 0)
            if total_q > 0:
                kpi_ontime = int(row.get('ontime', 0) or 0)
                kpi_late = int(row.get('late', 0) or 0)
                kpi_eff = round((kpi_ontime / total_q * 100), 1)
                
        kpi_total_entregas = 0
        kpi_best = "N/A"
        if not area_stats_df.empty and 'total_entregas' in area_stats_df.columns:
            kpi_total_entregas = int(area_stats_df['total_entregas'].fillna(0).sum())
            kpi_best = area_stats_df.iloc[0]['area'] if 'area' in area_stats_df.columns else "N/A"
        
        return {
            "kpi_total": kpi_total_entregas,
            "kpi_avg": round(kpi_total_entregas / total_dias, 1) if total_dias > 0 else 0.0,
            "kpi_best": kpi_best,
            "kpi_eff": kpi_eff,
            "kpi_ontime": kpi_ontime,
            "kpi_late": kpi_late,
            "total_dias_activos": total_dias
        }

    def _prepare_authors(self, year, month_str):
        """Obtiene ranking de autores con comparativa mensual."""
        top_yr = sanitize_for_json(DeliveriesRepository(self.session).get_top_authors(str(year)))
        top_cm = sanitize_for_json(DeliveriesRepository(self.session).get_top_authors(month_str))
        cm_map = {a['name']: a['entregas'] for a in top_cm}
        
        for a in top_yr:
            a['entregas_cm'] = cm_map.get(a['name'], 0)
        return top_yr

    def _prepare_locations(self, year, month_str):
        """Obtiene ranking de ubicaciones con comparativa mensual."""
        loc_yr = sanitize_for_json(DeliveriesRepository(self.session).get_top_locations(str(year)))
        loc_cm = sanitize_for_json(DeliveriesRepository(self.session).get_top_locations(month_str))
        cm_map = {l['ubicacion']: l['num_items'] for l in loc_cm}
        
        for l in loc_yr:
            l['num_items_cm'] = cm_map.get(l['ubicacion'], 0)
        return loc_yr

    def _prepare_materials_by_area(self, year, month_str):
        """Estructura el ranking de materiales por cada área de negocio."""
        df_yr = DeliveriesRepository(self.session).get_top_materials_by_area(str(year))
        df_cm = DeliveriesRepository(self.session).get_top_materials_by_area(month_str)
        
        cm_map = {}
        if not df_cm.empty:
            for _, row in df_cm.iterrows():
                cm_map[(row['area'], row['material'])] = row['frequency']
                
        results = {}
        if not df_yr.empty:
            for area, group in df_yr.groupby('area'):
                subset = group.head(10).to_dict(orient="records")
                for item in subset:
                    item['frequency_cm'] = cm_map.get((item['area'], item['material']), 0)
                results[area] = subset
        return results