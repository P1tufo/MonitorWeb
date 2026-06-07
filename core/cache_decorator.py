import json
import logging
from datetime import datetime
from functools import wraps
from typing import Any, Dict, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger("core-cache-decorator")

def save_analytics_snapshot(session: Session, key: str, data: Dict[str, Any]):
    """Guarda una captura de las analíticas en la base de datos para carga instantánea."""
    try:
        session.execute(text("CREATE TABLE IF NOT EXISTS analytics_snapshots (key TEXT PRIMARY KEY, data TEXT, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"))
        data_to_save = {k: v for k, v in data.items() if k not in ('request', 'user', 'is_syncing')}
        json_data = json.dumps(data_to_save)
        session.execute(
            text("INSERT OR REPLACE INTO analytics_snapshots (key, data, updated_at) VALUES (:key, :data, CURRENT_TIMESTAMP)"),
            {"key": key, "data": json_data}
        )
        session.commit()
    except Exception as e:
        logger.error(f"Error guardando snapshot {key}: {e}")

def load_analytics_snapshot(session: Session, key: str) -> Optional[Dict[str, Any]]:
    """Recupera la última captura de analíticas desde la base de datos."""
    try:
        res = session.execute(text("SELECT data FROM analytics_snapshots WHERE key = :key"), {"key": key}).fetchone()
        if res:
            return json.loads(res[0])
    except Exception:
        pass
    return None

def analytics_cache(key_prefix: str):
    """
    Decorador que implementa el patrón de caché multinivel (Memoria -> DB Snapshot -> Cálculo).
    Debe aplicarse a métodos de clase (Servicios) que contengan `self.session` y devuelvan un dict.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            from core.state import get_cache_manager
            cache = get_cache_manager()
            session = getattr(self, "session", None)

            if not session:
                logger.warning(f"No se encontró 'self.session' en {self.__class__.__name__}. Caché omitida.")
                return func(self, *args, **kwargs)

            year_str = datetime.now().strftime("%Y")
            month_str = datetime.now().strftime("%m")
            db_key = f"{key_prefix}_{year_str}_{month_str}"
            mem_key = f"/analytics/{key_prefix}"

            # 1. Caché en Memoria
            cached = cache.get_cache(mem_key)
            if cached and "wms_labels" in cached:
                logger.info(f"Sirviendo {key_prefix} desde Caché de Memoria.")
                return cached.copy()

            # 2. Snapshot en BD
            snapshot = load_analytics_snapshot(session, db_key)
            if snapshot and "wms_labels" in snapshot:
                logger.info(f"Sirviendo {key_prefix} desde Snapshot de Base de Datos.")
                cache.set_cache(mem_key, snapshot)
                return snapshot.copy()

            # 3. Cálculo Completo
            logger.info(f"Sin caché para {key_prefix}. Iniciando cálculo completo...")
            result = func(self, *args, **kwargs)

            if isinstance(result, dict):
                clean_result = {k: v for k, v in result.items() if k not in ('request', 'user', 'is_syncing')}
                cache.set_cache(mem_key, clean_result)
                save_analytics_snapshot(session, db_key, clean_result)

            return result
        return wrapper
    return decorator
