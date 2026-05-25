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
  - `get_cache(key: str)` - Recupera un valor del caché.
  - `set_cache(key: str, value: Any)` - Guarda un valor en el caché, respetando los límites de tamaño.
  - `clear_cache(key: Optional[str] = None)` - Limpia una entrada específica o todo el caché.
  - `clear_cache_prefix(prefix: str)` - Limpia todas las entradas de caché que comiencen con el prefijo dado.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `global_state` - Instancia única de `AppState`.

### Dependencias y Flujo
- Librerías externas utilizadas: `fastapi`, `logging`, `threading`.
- No comunica con otros archivos del proyecto.

