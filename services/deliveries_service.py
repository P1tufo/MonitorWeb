from sqlalchemy.orm import Session
import logging
from typing import Dict, Any

logger = logging.getLogger("services-deliveries")

class DeliveriesService:
    def __init__(self, session: Session):
        self.session = session
        self.conn = session.connection().connection

    def get_full_context(self) -> Dict[str, Any]:
        """
        Fase 3: SaaS Dinámico.
        El backend ya no procesa DataFrames masivos. Solo entrega metadatos ligeros.
        """
        logger.debug("Iniciando generación de contexto Entregas (SaaS Asíncrono)...")
        from core.models import ConfigQuery
        
        widgets = self.session.query(ConfigQuery).filter(
            ConfigQuery.query_id.like("vl_%")
        ).all()
        widget_ids = [w.query_id for w in widgets]

        try:
            areas_res = self.conn.execute("SELECT DISTINCT area_negocio FROM outbound_deliveries WHERE area_negocio IS NOT NULL").fetchall()
            areas_vl = [a[0] for a in areas_res if str(a[0]).strip()]
        except Exception as e:
            areas_vl = ["ASERRADERO", "REMANUFACTURA", "LINEA 1", "LINEA 2", "VIGAS", "MOLDURAS", "RANURADO"]

        context = {
            "widget_ids": widget_ids,
            "areas_vl": areas_vl,
            # Fallbacks para evitar errores en Jinja durante la transición
            "kpi_total": "--",
            "kpi_eff": "--",
            "kpi_ontime": "--",
            "kpi_late": "--",
            "top_authors": [],
            "top_locations": [],
            "top_materials": {},
            "area_stats_json": [],
            "weekdays": [],
            "weekdays_data": [],
            "weekdays_data_cm": [],
            "chart_labels_vl": [],
            "chart_datasets_vl": [],
            "ubicaciones_mapping": {},
            "area_material_mapping": {},
            "user_material_mapping": {},
            "weekday_mapping": {},
            "weekday_mapping_cm": {},
            "area_material_mapping_cm": {},
            "user_material_mapping_cm": {},
            "ubicaciones_mapping_cm": {},
            "weekday_raw_json": [],
            "total_dias_activos": 0,
            "periodo_actual": "",
            "monthly_labels": [],
            "monthly_data": [],
            "weekly_labels": [],
            "weekly_data": [],
            "wms_labels": [],
            "wms_data": [],
            "sla_trend_labels": [],
            "sla_trend_data": [],
            "sla_trend_count": [],
            "sla_area_labels": [],
            "sla_area_datasets": [],
            "sla_monthly_labels": [],
            "sla_monthly_data": [],
            "sla_monthly_count": [],
            "sla_area_monthly_labels": [],
            "sla_area_monthly_datasets": [],
            "monthly_raw_json": [],
            "weekly_raw_json": [],
            "sla_area_monthly_raw_json": [],
            "sla_area_trend_raw_json": [],
            "correlation_data": []
        }
        
        try:
            from routes.inventory import get_inventory_context
            from routes.tasks import get_tasks_context
            from routes.analytics_proyecciones import get_proyecciones_context
            context.update(get_inventory_context(self.session))
            context.update(get_tasks_context(self.session))
            context.update(get_proyecciones_context())
        except Exception as e:
            logger.error(f"Error cargando contextos secundarios: {e}")
            
        return context