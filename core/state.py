from fastapi import Request

"""
core/state.py — Gestión de estado global y caché de la aplicación.
"""
import logging
from threading import Lock
from typing import Any, Dict, Final, Optional

logger = logging.getLogger("app-state")

class CacheManager:
    """
    Gestor especializado en caché.
    Implementa límites de seguridad para evitar fugas de memoria.
    """
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._max_cache_size: int = 100

    @property
    def max_cache_size(self) -> int:
        return self._max_cache_size

    @max_cache_size.setter
    def max_cache_size(self, value: int):
        self._max_cache_size = value

    @property
    def cache_size(self) -> int:
        return len(self._cache)

    def get_cache(self, key: str) -> Optional[Any]:
        return self._cache.get(key)

    def set_cache(self, key: str, value: Any):
        if len(self._cache) >= self._max_cache_size:
            logger.warning("Límite de caché alcanzado. Limpiando para liberar memoria.")
            self.clear_cache()
        self._cache[key] = value

    def clear_cache(self, key: Optional[str] = None):
        if key:
            self._cache.pop(key, None)
        else:
            self._cache.clear()
            logger.info("Caché global vaciado.")

    def clear_cache_prefix(self, prefix: str):
        keys_to_delete = [k for k in self._cache.keys() if k.startswith(prefix)]
        for k in keys_to_delete:
            self._cache.pop(k, None)
        logger.info(f"Caché limpiado para prefijo '{prefix}' ({len(keys_to_delete)} entradas).")


class SyncStateManager:
    """
    Gestor especializado en estados de sincronización.
    """
    def __init__(self):
        self._sync_lock: Final[Lock] = Lock()
        self._is_syncing: bool = False

    @property
    def sync_lock(self) -> Lock:
        return self._sync_lock

    @property
    def is_syncing(self) -> bool:
        return self._is_syncing

    @is_syncing.setter
    def is_syncing(self, value: bool):
        self._is_syncing = value
        logger.debug(f"Estado de sincronización cambiado a: {value}")


cache_manager = CacheManager()
sync_manager = SyncStateManager()


def get_cache_manager() -> CacheManager:
    return cache_manager


def get_sync_manager() -> SyncStateManager:
    return sync_manager
