import logging
from typing import Dict, Any
from sqlalchemy.orm import Session
from repositories.tasks import TasksRepository

logger = logging.getLogger("services-productivity-monthly")

class ProductivityMonthlyService:
    def __init__(self, session: Session):
        self.session = session
        self.tasks_repo = TasksRepository(session)

    def get_monthly_productivity_data(self, target_month: str) -> Dict[str, Any]:
        """
        Retorna todos los KPIs de productividad para un mes específico (YYYY-MM).
        """
        try:
            parts = target_month.split('-')
            month_sap = f"{parts[1]}.{parts[0]}"
        except:
            month_sap = target_month

        logger.info(f"Calculando KPIs de productividad para el mes: {month_sap}")

        summary = self.tasks_repo._get_monthly_summary(month_sap)
        shifts = self.tasks_repo._get_monthly_shifts(month_sap)
        heatmap = self.tasks_repo._get_monthly_heatmap(month_sap)

        return {
            "target_month": target_month,
            "target_month_sap": month_sap,
            "summary": summary,
            "shifts": shifts,
            "heatmap": heatmap
        }

    def get_user_movements_monthly_summary(self, target_month: str, usuario: str) -> list:
        return self.tasks_repo.get_user_movements_monthly_summary(target_month, usuario)

    def get_user_movements_monthly_details(self, target_month: str, usuario: str, operacion: str) -> list:
        return self.tasks_repo.get_user_movements_monthly_details(target_month, usuario, operacion)
