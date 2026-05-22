import os
import logging
from typing import Final
from pathlib import Path

# Configuración de Logging para el módulo de configuración
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger("config")

# ─── PATHS BASE ────────────────────────────────────────────────────────────────
# Directorio raíz del proyecto usando Pathlib para mayor robustez
BASE_DIR: Final[Path] = Path(__file__).resolve().parent

# ─── BASES DE DATOS Y ALMACENAMIENTO ──────────────────────────────────────────
# Definición de rutas críticas para persistencia y caché
DB_PATH: Final[Path]         = Path(os.getenv("DB_PATH", BASE_DIR / "data" / "wms_transactions.db"))
PDF_STORAGE: Final[Path]     = Path(os.getenv("PDF_STORAGE", BASE_DIR / "PDFs_Generados"))
CLEANSED_DIR: Final[Path]    = Path(os.getenv("CLEANSED_DIR", BASE_DIR / "DELIVERIES_cleansed"))
TEMP_DIR: Final[Path]        = Path(os.getenv("TEMP_DIR", BASE_DIR / "Temp_Assets"))
CACHE_DIR_NAME: Final[str]   = os.getenv("CACHE_DIR", ".doc_cache")
CACHE_DIR: Final[Path]       = BASE_DIR / CACHE_DIR_NAME
TUNNEL_URL_FILE: Final[Path] = TEMP_DIR / "tunnel_url.txt"
NGROK_BIN: Final[Path]       = BASE_DIR / "bin" / "ngrok"
LOG_FILE: Final[Path]        = TEMP_DIR / "server.log"

# ─── CONFIGURACION DEL SERVIDOR ───────────────────────────────────────────────
APP_HOST: Final[str]   = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT: Final[int]   = int(os.getenv("APP_PORT", 8000))
APP_RELOAD: Final[bool] = os.getenv("APP_RELOAD", "true").lower() == "true"

# ─── ONEDRIVE Y FUENTES EXTERNAS ──────────────────────────────────────────────
# Se evita el hardcoding de rutas de usuario para permitir portabilidad
_home = Path.home()
DEFAULT_ONEDRIVE: Final[Path] = _home / "Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Transacciones"

ONEDRIVE_PATH: Final[Path] = Path(os.getenv("ONE_DRIVE_PATH", DEFAULT_ONEDRIVE))

# Subdirectorios de transacciones WMS (Agnóstico)
DELIVERIES_DIR: Final[Path] = ONEDRIVE_PATH / "VL06O"
STOCK_DIR: Final[Path]      = ONEDRIVE_PATH / "LX02"
TASKS_DIR: Final[Path]      = ONEDRIVE_PATH / "LT22"
INVENTORY_DIR: Final[Path]  = ONEDRIVE_PATH / "MB51"

# ─── VALIDACIONES Y UTILIDADES ────────────────────────────────────────────────
def validate_config():
    """Realiza comprobaciones de salud en la configuración."""
    if not NGROK_BIN.exists():
        logger.warning(f"Binario de ngrok no encontrado en: {NGROK_BIN}. El túnel público no funcionará.")
    
    if not ONEDRIVE_PATH.exists():
        logger.warning(f"Ruta de OneDrive no accesible: {ONEDRIVE_PATH}. La sincronización de datos podría fallar.")

def ensure_project_structure():
    """Crea los directorios necesarios para el funcionamiento de la app si no existen."""
    dirs = [PDF_STORAGE, TEMP_DIR, CLEANSED_DIR, CACHE_DIR]
    for d in dirs:
        try:
            d.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directorio verificado/creado: {d}")
        except PermissionError:
            logger.error(f"Fallo crítico: Sin permisos para crear el directorio {d}")
        except Exception as e:
            logger.error(f"Error inesperado creando {d}: {e}")

# ─── INICIALIZACIÓN AUTOMÁTICA ───────────────────────────────────────────────
# Se ejecuta al importar para garantizar que la estructura base exista siempre.
ensure_project_structure()
validate_config()

