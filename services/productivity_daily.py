import logging
from typing import Any, Dict

from sqlalchemy.orm import Session

from repositories.productivity import ProductivityRepository

logger = logging.getLogger("services-productivity")

class ProductivityDailyService:
    def __init__(self, session: Session):
        self.session = session
        self.productivity_repo = ProductivityRepository(session)

    def get_available_dates(self) -> list:
        return self.productivity_repo.get_available_dates()

    def get_productivity_data(self, target_date: str) -> Dict[str, Any]:
        """
        Retorna todos los KPIs de productividad para una fecha específica (YYYY-MM-DD).
        """
        # Convertir YYYY-MM-DD a DD.MM.YYYY (formato de inventory_movements)
        try:
            import re
            # Si el formato es YYYY-MM-DD
            if re.match(r'^\d{4}-\d{2}-\d{2}$', target_date):
                parts = target_date.split('-')
                date_sap = f"{parts[2]}.{parts[1]}.{parts[0]}"
            # Si el formato es DD-MM-YYYY
            elif re.match(r'^\d{2}-\d{2}-\d{4}$', target_date):
                parts = target_date.split('-')
                date_sap = f"{parts[0]}.{parts[1]}.{parts[2]}"
            else:
                date_sap = target_date
        except Exception:
            date_sap = target_date

        logger.info(f"Calculando KPIs de productividad para la fecha: {date_sap}")

        summary = self.productivity_repo._get_daily_summary(date_sap)
        trend = self.productivity_repo._get_hourly_trend(date_sap)
        gaps = self.productivity_repo._get_inactivity_gaps(date_sap)
        heatmap = self.productivity_repo._get_activity_heatmap(date_sap)

        return {
            "target_date": target_date,
            "target_date_sap": date_sap,
            "summary": summary,
            "trend": trend,
            "gaps": gaps,
            "heatmap": heatmap
        }

    def get_user_movements_daily_summary(self, target_date: str, usuario: str) -> list:
        return self.productivity_repo.get_user_movements_daily_summary(target_date, usuario)

    def get_user_movements_daily_details(self, target_date: str, usuario: str, operacion: str) -> list:
        return self.productivity_repo.get_user_movements_daily_details(target_date, usuario, operacion)
