"""
# Trigger uvicorn reload
main.py — Punto de entrada oficial de MonitorWeb Analytics.
"""
import sys
import uvicorn
import logging
from app import app
from config import APP_HOST, APP_PORT, APP_RELOAD
from services.tunnel import start_tunnel

# Configuración de logging unificada
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("startup")

def start_application():
    """Configura e inicia los servicios de la plataforma."""
    try:
        # 1. Iniciar Túnel Ngrok (Acceso Remoto)
        # Se inicia antes que uvicorn para tener la URL disponible
        logger.info("Activando servicio de túnel remoto...")
        start_tunnel()
        
        # 2. Lanzar Servidor Web
        # Uvicorn gestiona internamente la ocupación de puertos y el recargado.
        # Al no usar manejadores de señales externos, uvicorn puede procesar
        # Ctrl+C correctamente y elevar KeyboardInterrupt.
        logger.info(f"Iniciando MonitorWeb en http://{APP_HOST}:{APP_PORT} (Reload: {APP_RELOAD})")
        
        uvicorn.run(
            "app:app", 
            host=APP_HOST, 
            port=APP_PORT, 
            reload=APP_RELOAD,
            log_level="info",
            access_log=False # Evita ruido excesivo en consola por cada asset estático
        )
        
    except KeyboardInterrupt:
        logger.info("Cierre detectado por el usuario (Ctrl+C).")
    except Exception as e:
        logger.critical(f"Fallo crítico durante el arranque: {e}")
        sys.exit(1)
    finally:
        # Garantizar que el túnel se cierre al salir, independientemente de la causa
        logger.info("Finalizando procesos y cerrando túnel...")
        try:
            from services.tunnel import stop_tunnel
            stop_tunnel()
        except Exception as e:
            logger.error(f"Error durante la limpieza: {e}")
        logger.info("MonitorWeb cerrado correctamente.")
        import os
        os._exit(0)  # Forzar cierre absoluto matando cualquier hilo rebelde en segundo plano

if __name__ == "__main__":
    start_application()
