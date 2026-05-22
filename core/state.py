from fastapi import Request
"""
core/state.py — Gestión de estado global y caché de la aplicación.
"""
import logging
from threading import Lock
from typing import Dict, Any, Optional, Final

logger = logging.getLogger("app-state")

class AppState:
    """
    Clase para gestionar el estado mutable y la caché de forma centralizada.
    Implementa límites de seguridad para evitar fugas de memoria.
    """
    def __init__(self):
        self._sync_lock: Final[Lock] = Lock()
        self._is_syncing: bool = False
        self._cache: Dict[str, Any] = {}
        self._max_cache_size: int = 100  # Límite de entradas en caché

    @property
    def max_cache_size(self) -> int:
        """Devuelve el límite máximo de entradas en caché."""
        return self._max_cache_size

    @max_cache_size.setter
    def max_cache_size(self, value: int):
        """Configura el límite máximo de entradas en caché."""
        self._max_cache_size = value

    @property
    def sync_lock(self) -> Lock:
        """Devuelve el lock de sincronización para operaciones atómicas."""
        return self._sync_lock

    @property
    def is_syncing(self) -> bool:
        """Verifica si hay un proceso de sincronización activo (lectura rápida)."""
        return self._is_syncing

    @is_syncing.setter
    def is_syncing(self, value: bool):
        """Actualiza el estado de sincronización (atómico)."""
        self._is_syncing = value
        logger.debug(f"Estado de sincronización cambiado a: {value}")

    @property
    def cache_size(self) -> int:
        """Devuelve el número actual de entradas en la caché."""
        return len(self._cache)

    def get_cache(self, key: str) -> Optional[Any]:
        """Recupera un valor del caché."""
        return self._cache.get(key)

    def set_cache(self, key: str, value: Any):
        """Guarda un valor en el caché, respetando los límites de tamaño."""
        if len(self._cache) >= self._max_cache_size:
            # Estrategia de limpieza simple: vaciar caché si se supera el límite
            logger.warning("Límite de caché alcanzado. Limpiando para liberar memoria.")
            self.clear_cache()
        
        self._cache[key] = value

    def clear_cache(self, key: Optional[str] = None):
        """Limpia una entrada específica o todo el caché."""
        if key:
            self._cache.pop(key, None)
        else:
            self._cache.clear()
            logger.info("Caché global vaciado.")

global_state = AppState()

def get_app_state() -> AppState:
    """Inyección de dependencias para FastAPI."""
    return global_state
