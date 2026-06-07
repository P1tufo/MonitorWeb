import logging

from core.database import get_session
from routes.tasks import get_tasks_context
from services.deliveries_service import DeliveriesService
from services.inventory_service import InventoryService

logger = logging.getLogger("background-tasks")

def refresh_analytics():
    """Refresca las analíticas (ejecutado como tarea de fondo trazable)."""
    logger.debug(">>> Refrescando analíticas (Heavy recalculate)...")
    try:
        with get_session() as session:
            DeliveriesService(session).get_full_context()
            InventoryService(session).get_full_context()
            get_tasks_context(session)
        logger.debug(">>> Refresco de analíticas completado.")
    except Exception as e:
        logger.error(f"Error refrescando analíticas: {e}")
