import logging
from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from repositories.dashboard import DashboardRepository

logger = logging.getLogger("services-dashboard")

class DashboardService:
    """
    Orquestador del dashboard principal de Entregas (vista operativa).
    Refactorizado (Fase 4): Ahora delega toda la interacción de base de datos a DeliveriesRepository.
    """
    def __init__(self, session: Session):
        self.session = session
        self.repo = DashboardRepository(session)

    def get_full_context(self) -> Dict[str, Any]:
        iso_year, iso_week, _ = datetime.now().isocalendar()
        current_week_str = f"{iso_year}-{iso_week:02d}"
        min_week = current_week_str

        chart_data = self.repo.get_weekly_intensity_chart(iso_year)
        kpis = self.repo.get_filtered_kpis(None, None, None, min_week, iso_year)
        selectors = self.repo.get_dashboard_selectors(min_week)
        recent_tx = self.repo.get_filtered_transactions(None, None, None, None, None, min_week)

        # Formatear el diccionario tx a la lista que espera la vista
        tx_list = recent_tx.to_dict(orient='records') if hasattr(recent_tx, 'to_dict') else recent_tx

        # Alinear nombres de KPIs con el frontend antiguo si difieren
        kpis_mapped = {
            "kpi_deliveries": kpis.get("kpi_deliveries", "0"),
            "kpi_materials": kpis.get("kpi_materials", "0"),
            "kpi_year_deliveries": kpis.get("kpi_year_deliveries", "0"),
            "kpi_year_materials": kpis.get("kpi_year_materials", "0"),
            "sub_del_abierta": kpis.get("sub_del_abierta", "0"),
            "sub_del_no_tratada": kpis.get("sub_del_no_tratada", "0"),
            "sub_mat_abierta": kpis.get("sub_mat_abierta", "0"),
            "sub_mat_no_tratada": kpis.get("sub_mat_no_tratada", "0"),
            "sub_del_reunido": kpis.get("sub_del_reunido", "0"),
            "sub_mat_reunido": kpis.get("sub_mat_reunido", "0"),
            "sub_del_atrasado": kpis.get("sub_del_atrasado", "0"),
            "sub_mat_atrasado": kpis.get("sub_mat_atrasado", "0"),
            "sub_del_critico": kpis.get("sub_del_critico", "0"),
            "sub_mat_critico": kpis.get("sub_mat_critico", "0"),
        }

        return {
            "transactions": tx_list,
            **chart_data,
            **kpis_mapped,
            **selectors
        }
