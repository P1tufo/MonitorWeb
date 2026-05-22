from sqlalchemy.orm import Session
import pandas as pd
from sqlalchemy import text
import logging
from datetime import datetime
from core.state import get_app_state
from core.utils import sanitize_for_json
from repositories import TasksRepository

logger = logging.getLogger("services-tasks")

class TasksService:
    def __init__(self, session: Session):
        self.session = session

    def get_full_context(self) -> dict:
        """Genera y cachea el contexto analítico para la gestión de OTs."""
        try:
            state = get_app_state()
            logger.debug("Generando contexto de Gestión de OTs...")
            
            repo = TasksRepository(self.session)
            df_summary = repo.get_tasks_summary()
            df_trend = repo.get_tasks_trend()
            df_users = repo.get_tasks_by_user()
            df_types = repo.get_tasks_by_type_dest()
            df_recent = repo.get_recent_tasks()
            df_non_palletized = repo.get_non_palletized_movements()
            non_palletized_total_count = repo.get_non_palletized_count()
            df_non_palletized_summary = repo.get_non_palletized_summary()

            # Preparar datos para gráficos
            # 1. Resumen por Tipo Movimiento
            ots_summary = df_summary.to_dict(orient='records')
            
            # 2. Tendencia Diaria (Dual: Creadas vs Confirmadas)
            ots_trend_labels = df_trend['label'].tolist()
            ots_trend_created = df_trend['created'].tolist()
            ots_trend_confirmed = df_trend['confirmed'].tolist()
            
            # 3. Usuarios (Dual: Creadas vs Confirmadas)
            ots_user_labels = df_users['user'].tolist()
            ots_user_created = df_users['created'].tolist()
            ots_user_confirmed = df_users['confirmed'].tolist()
            
            # 4. Tipos Almacén
            ots_type_labels = df_types['type'].tolist()
            ots_type_data = df_types['count'].tolist()
            
            # Sobrescribir con listado dinámico de config_queries si existe
            try:
                res_list = self.session.execute(text("SELECT sql_text, visual_state FROM config_queries WHERE query_id = 'ots_list_pending'")).fetchone()
                if res_list:
                    sql_list, visual_state_list = res_list
                    if sql_list:
                        from core.utils import _get_bound_params_from_visual_state
                        params = ()
                        if sql_list.count("?") > 0:
                            params = tuple(_get_bound_params_from_visual_state(visual_state_list))
                        df_dyn_recent = pd.read_sql(sql_list, self.session.connection().connection, params=params)
                        if not df_dyn_recent.empty:
                            df_recent = df_dyn_recent
            except Exception as e_list:
                logger.error(f"Error al cargar listado dinámico ots_list_pending: {e_list}")

            # 5. Lista Recientes (con cálculo de SLA)
            now = datetime.now()
            ots_recent = []
            ots_critical_count = 0
            for row in df_recent.to_dict(orient='records'):
                try:
                    # Formato fe_creac: DD-MM-YYYY o created_at
                    created_at_val = row.get('created_at', row.get('created', ''))
                    creac_date_str = str(created_at_val).split(' ')[0]
                    creac_date = datetime.strptime(creac_date_str, "%d-%m-%Y")
                    diff_days = (now - creac_date).days
                    
                    if diff_days > 4:
                        row['sla_status'] = 'Crítico'
                        row['sla_color'] = '#ef4444' # Rojo
                        ots_critical_count += 1
                    elif diff_days > 2:
                        row['sla_status'] = 'Atrasada'
                        row['sla_color'] = '#f59e0b' # Ámbar
                    else:
                        row['sla_status'] = 'En Plazo'
                        row['sla_color'] = '#10b981' # Verde
                except Exception:
                    row['sla_status'] = 'N/A'
                    row['sla_color'] = '#94a3b8'
                ots_recent.append(row)

            ots_pending_count = len(ots_recent)
            ots_user_count = len(ots_user_labels) if ots_user_labels else 0

            # Sobrescribir con KPIs dinámicos de config_queries si existen
            try:
                from core.utils import _extract_metric_value, _get_bound_params_from_visual_state
                
                # KPI: Tareas Pendientes
                res_p = self.session.execute(text("SELECT sql_text, visual_state FROM config_queries WHERE query_id = 'ots_kpi_pending'")).fetchone()
                if res_p:
                    sql_p, vs_p = res_p
                    if sql_p:
                        params = ()
                        if sql_p.count("?") > 0:
                            params = tuple(_get_bound_params_from_visual_state(vs_p))
                        df_p = pd.read_sql(sql_p, self.session.connection().connection, params=params)
                        if not df_p.empty:
                            val = _extract_metric_value(df_p)
                            if val is not None and not pd.isna(val):
                                ots_pending_count = int(val)
                                
                # KPI: Usuarios Activos
                res_u = self.session.execute(text("SELECT sql_text, visual_state FROM config_queries WHERE query_id = 'ots_kpi_users'")).fetchone()
                if res_u:
                    sql_u, vs_u = res_u
                    if sql_u:
                        params = ()
                        if sql_u.count("?") > 0:
                            params = tuple(_get_bound_params_from_visual_state(vs_u))
                        df_u = pd.read_sql(sql_u, self.session.connection().connection, params=params)
                        if not df_u.empty:
                            val = _extract_metric_value(df_u)
                            if val is not None and not pd.isna(val):
                                ots_user_count = int(val)
                                
                # KPI: OTs Críticas
                res_c = self.session.execute(text("SELECT sql_text, visual_state FROM config_queries WHERE query_id = 'ots_kpi_critical'")).fetchone()
                if res_c:
                    sql_c, vs_c = res_c
                    if sql_c:
                        params = ()
                        if sql_c.count("?") > 0:
                            params = tuple(_get_bound_params_from_visual_state(vs_c))
                        df_c = pd.read_sql(sql_c, self.session.connection().connection, params=params)
                        if not df_c.empty:
                            val = _extract_metric_value(df_c)
                            if val is not None and not pd.isna(val):
                                ots_critical_count = int(val)
            except Exception as ex_kpis:
                logger.error(f"Error al cargar KPIs dinámicos de OTs: {ex_kpis}")

            context = {
                "ots_summary": ots_summary,
                "ots_trend_labels": ots_trend_labels,
                "ots_trend_created": ots_trend_created,
                "ots_trend_confirmed": ots_trend_confirmed,
                "ots_user_labels": ots_user_labels,
                "ots_user_created": ots_user_created,
                "ots_user_confirmed": ots_user_confirmed,
                "ots_type_labels": ots_type_labels,
                "ots_type_data": ots_type_data,
                "ots_recent": ots_recent,
                "ots_pending_count": ots_pending_count,
                "ots_user_count": ots_user_count,
                "ots_critical_count": ots_critical_count,
                "non_palletized_movements": df_non_palletized.to_dict(orient='records'),
                "non_palletized_total_count": non_palletized_total_count,
                "non_palletized_summary": df_non_palletized_summary.to_dict(orient='records'),
                "last_update_ots": datetime.now().strftime("%H:%M:%S")
            }

            # Sanitizar para JSON
            context = sanitize_for_json(context)
            
            # Cachear en memoria
            state.set_cache("/analytics/ots", context)
            
            # Opcional: Persistir en la base de datos de snapshots
            # (Por ahora solo memoria para velocidad)
            
            return context
        except Exception as e:
            logger.error(f"Error generando contexto de OTs: {e}", exc_info=True)
            return {}

