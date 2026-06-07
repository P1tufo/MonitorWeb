import importlib
import logging
from typing import List

from fastapi import APIRouter, FastAPI

logger = logging.getLogger(__name__)

def register_routes(app: FastAPI) -> None:
    """
    Registra todos los routers de la aplicación de forma centralizada.
    Incluye manejo de errores básico para evitar que un router mal configurado
    detenga el arranque completo del servidor.
    """

    # Lista declarativa de routers con tipado estático
    # Lista de nombres de módulos de routers a importar dinámicamente
    ROUTER_MODULES: List[str] = [
        "routes.auth",        # Auth primero para que /api/auth/login esté disponible
        "routes.dashboard",
        "routes.deliveries",
        "routes.inventory",
        "routes.analytics_proyecciones",
        "routes.filters",
        "routes.pdf",
        "routes.sync",
        "routes.docs",
        "routes.settings",
        "routes.tasks",
        "routes.widgets",
        "routes.consumos",
        "routes.transporte",
        "routes.productivity"
    ]

    ROUTERS: List[APIRouter] = []
    for module_name in ROUTER_MODULES:
        try:
            module = importlib.import_module(module_name)
            ROUTERS.append(module.router)
        except Exception as e:
            logger.error(f"Error importando módulo {module_name}: {e}")
            continue

    for router in ROUTERS:
        try:
            app.include_router(router)
            logger.debug(f"Router registrado con éxito: {router}")
        except Exception as e:
            logger.error(f"Error registrando router {router}: {e}")
            # En producción podríamos querer relanzar el error o simplemente omitir el router
            continue
