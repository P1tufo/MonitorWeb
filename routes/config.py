import logging
from fastapi import FastAPI, APIRouter
from typing import List

# Importación de módulos de ruta
from . import (
    dashboard,
    deliveries,
    inventory,
    analytics_proyecciones,
    filters,
    pdf,
    sync,
    docs,
    settings,
    auth,
    tasks
)

logger = logging.getLogger(__name__)

def register_routes(app: FastAPI) -> None:
    """
    Registra todos los routers de la aplicación de forma centralizada.
    Incluye manejo de errores básico para evitar que un router mal configurado
    detenga el arranque completo del servidor.
    """
    
    # Lista declarativa de routers con tipado estático
    ROUTERS: List[APIRouter] = [
        auth.router,        # Auth primero para que /api/auth/login esté disponible
        dashboard.router,
        deliveries.router,
        inventory.router,
        analytics_proyecciones.router,
        filters.router,
        pdf.router,
        sync.router,
        docs.router,
        settings.router,
        tasks.router
    ]

    for router in ROUTERS:
        try:
            app.include_router(router)
            logger.debug(f"Router registrado con éxito: {router}")
        except Exception as e:
            logger.error(f"Error registrando router {router}: {e}")
            # En producción podríamos querer relanzar el error o simplemente omitir el router
            continue
