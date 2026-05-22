## Archivo: ./core/state.py

### Resumen Funcional
Gestión centralizada del estado mutable y la caché de la aplicación, implementando límites de seguridad para evitar fugas de memoria.

### Catálogo de Funciones y Clases
- `AppState()` - Gestiona el estado mutable y la caché de forma centralizada.
  - `__init__()`
  - `max_cache_size` (getter/setter)
  - `sync_lock` (getter)
  - `is_syncing` (getter/setter)
  - `cache_size` (getter)
  - `get_cache(key: str) -> Optional[Any]`
  - `set_cache(key: str, value: Any)`
  - `clear_cache(key: Optional[str] = None)`

### Interacción con Base de Datos
No aplica.

### Estado y Variables Globales
- `global_state` (variable global): Instancia única de `AppState`.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `fastapi`: Para inyección de dependencias.
  - `logging`: Para registro de eventos.
  - `threading.Lock`: Para sincronización.

- Comunicación con otros archivos del proyecto:
  - `get_app_state()`: Inyección de dependencias para FastAPI.

