## Archivo: ./core/state.py

### Resumen Funcional
Gestión centralizada del estado mutable y la caché de la aplicación, implementando límites de seguridad para evitar fugas de memoria.

### Catálogo de Funciones y Clases
- `AppState()` - Gestiona el estado mutable y la caché de forma centralizada.
  - `__init__()`
  - `max_cache_size` (getter/setter) - Devuelve/Configura el límite máximo de entradas en caché.
  - `sync_lock` (getter) - Devuelve el lock de sincronización para operaciones atómicas.
  - `is_syncing` (getter/setter) - Verifica y actualiza el estado de sincronización (atómico).
  - `cache_size` (getter) - Devuelve el número actual de entradas en la caché.
  - `get_cache(key: str)` - Recupera un valor del caché.
  - `set_cache(key: str, value: Any)` - Guarda un valor en el caché, respetando los límites de tamaño.
  - `clear_cache(key: Optional[str] = None)` - Limpia una entrada específica o todo el caché.
  - `clear_cache_prefix(prefix: str)` - Limpia todas las entradas de caché que comiencen con el prefijo dado.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `global_state` - Instancia única de la clase `AppState`, almacenada globalmente para su acceso desde cualquier parte del proyecto.

### Dependencias y Flujo
- **Dependencias**: No importa ninguna librería externa.
- **Flujo de Datos**: El archivo no consume ni es consumido por otros archivos. Es un componente central que proporciona acceso a la instancia global de `AppState` para gestionar el estado y la caché de la aplicación.

