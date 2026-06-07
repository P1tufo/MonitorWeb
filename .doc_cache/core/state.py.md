## Archivo: ./core/state.py

### Resumen Funcional
Gestión de estado global y caché de la aplicación, incluyendo límites de seguridad para evitar fugas de memoria.

### Catálogo de Funciones y Clases
- `CacheManager()` - Gestor especializado en caché con métodos para obtener, establecer y limpiar el caché.
- `SyncStateManager()` - Gestor especializado en estados de sincronización con métodos para controlar el estado de sincronización.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `cache_manager` - Instancia global de `CacheManager`.
- `sync_manager` - Instancia global de `SyncStateManager`.

### Dependencias y Flujo
- **Dependencias**: No importa ninguna librería externa.
- **Flujo de Datos**: El archivo no consume ni produce datos desde otros archivos del proyecto.

