"""
MonitorWeb — Aplicación Principal
================================
Punto de entrada para la configuración de FastAPI, montaje de rutas y recursos estáticos.
La orquestación del servidor se realiza a través de main.py.
"""

import os
import logging
from contextlib import asynccontextmanager
import warnings

# Suppress harmless pandas warnings regarding SQLite DBAPI connection types
warnings.filterwarnings("ignore", category=UserWarning, message=".*pandas only supports SQLAlchemy connectable.*")
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

# Importaciones Locales
from config import BASE_DIR, validate_config, ensure_project_structure
from core.app_instance import app
from routes.config import register_routes

# Configuración de Logger
logger = logging.getLogger("app-core")

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """
    Manejador del ciclo de vida de la aplicación.
    Gestiona el arranque asíncrono y la limpieza de recursos.
    """
    # --- Lógica de Inicio (Startup) ---
    logger.info(">>> Iniciando ciclo de vida de la aplicación...")
    
    # Inicializar tablas de autenticación y asegurar que exista al menos un admin
    from core.auth import init_auth_db, ensure_admin_exists
    from core.db_config_manager import init_config_db, seed_initial_config, load_config_to_memory
    init_auth_db()
    ensure_admin_exists()
    init_config_db()
    seed_initial_config()
    load_config_to_memory()
    
    from core.database import get_session
    import asyncio
    from sqlalchemy.exc import SQLAlchemyError
    from core.state import AppState
    from core.task_manager import task_manager
    from routes.tasks import get_tasks_context
    from services.deliveries_service import DeliveriesService
    from services.inventory_service import InventoryService

    if not hasattr(fastapi_app.state, "global_state"):
        fastapi_app.state.global_state = AppState()
    state = fastapi_app.state.global_state

    async def load_snapshots_async():
        """Carga los snapshots desde la BD sin bloquear el event loop."""
        try:
            loop = asyncio.get_event_loop()
            def sync_db_work():
                def _load_snap(session, key):
                    try:
                        import json
                        from sqlalchemy import text
                        res = session.execute(text("SELECT data FROM analytics_snapshots WHERE key = :key"), {"key": key}).fetchone()
                        return json.loads(res[0]) if res else None
                    except: return None
                
                with get_session() as session:
                    vl = _load_snap(session, "deliveries")
                    mb = _load_snap(session, "inventory")
                    ots = _load_snap(session, "ots")
                    return vl, mb, ots
            
            vl_snap, inventory_snap, ots_snap = await loop.run_in_executor(None, sync_db_work)
            
            if vl_snap:
                state.set_cache("/analytics/deliveries", vl_snap)
                logger.info(">>> Snapshot Entregas restaurado exitosamente.")
            if inventory_snap:
                state.set_cache("/analytics/inventory", inventory_snap)
                logger.info(">>> Snapshot Movimientos restaurado exitosamente.")
            if ots_snap:
                state.set_cache("/analytics/ots", ots_snap)
                logger.info(">>> Snapshot OTs restaurado exitosamente.")
                
        except SQLAlchemyError as e:
            logger.error(f"Fallo de base de datos cargando snapshots: {e}")
        except Exception as e:
            logger.warning(f"Error no crítico en pre-carga: {e}")

    def _refresh_analytics():
        """Refresca las analíticas (ejecutado como tarea de fondo trazable)."""
        logger.debug(">>> Refrescando analíticas (Heavy recalculate)...")
        with get_session() as session:
            DeliveriesService(session).get_full_context()
            InventoryService(session).get_full_context()
            get_tasks_context(session)
        logger.debug(">>> Refresco de analíticas completado.")

    # Ejecutar carga de snapshots antes de permitir peticiones
    await load_snapshots_async()
    
    # Iniciar refresco pesado como tarea de fondo trazable (Pilar 4)
    task_manager.submit_task("refresh_analytics", _refresh_analytics)
    
    yield
    # --- Lógica de Cierre (Shutdown) ---
    # Forzar el cierre inmediato de las tareas en segundo plano en lugar de esperar
    task_manager.shutdown(wait=False)
    logger.info(">>> Finalizando ciclo de vida de la aplicación.")

def initialize_app(fastapi_app: FastAPI) -> None:
    """Configura y prepara la aplicación FastAPI."""
    try:
        # 1. Configurar Lifespan
        fastapi_app.router.lifespan_context = lifespan
        
        # 2. Registro Centralizado de Rutas
        register_routes(fastapi_app)
        logger.info("Rutas registradas exitosamente.")

        # 3. Configuración de Recursos Estáticos
        _static_path = os.path.join(BASE_DIR, "static")
        
        if not os.path.exists(_static_path):
            error_msg = f"Directorio crítico 'static' no encontrado en: {_static_path}"
            logger.error(error_msg)
            # No lanzamos SystemExit aquí para permitir que las APIs funcionen sin UI si es necesario,
            # pero notificamos el error grave.
        else:
            fastapi_app.mount(
                "/static", 
                StaticFiles(directory=_static_path, html=False, follow_symlink=False), 
                name="static"
            )
            logger.info(f"Recursos estáticos montados correctamente.")

        # 4. Manejo Global de Excepciones de Autenticación
        @fastapi_app.exception_handler(HTTPException)
        async def auth_exception_handler(request: Request, exc: HTTPException):
            """Redirige a /login si falla la autenticación en una petición de navegador."""
            if exc.status_code == status.HTTP_401_UNAUTHORIZED:
                accept = request.headers.get("accept", "")
                if "text/html" in accept:
                    next_url = request.url.path
                    if request.url.query:
                        next_url += f"?{request.url.query}"
                    return RedirectResponse(url=f"/login?next={next_url}")
            
            # Para peticiones JSON o errores no-401, comportamiento estándar
            from fastapi.exception_handlers import http_exception_handler
            return await http_exception_handler(request, exc)

    except Exception as e:
        logger.error(f"Fallo en la inicialización: {e}", exc_info=True)
        raise

# Ejecutar inicialización
initialize_app(app)

