## Archivo: ./routes/inventory.py

### Resumen Funcional
Este archivo contiene rutas y lógica para el análisis de inventario en un sistema de gestión de almacén (WMS). Ofrece una redirección a la página de analíticas de inventario y una API que devuelve datos de inventario optimizados.

### Catálogo de Funciones y Clases
- `analytics_inventory_redirect(request: Request)` - Redirige a la página de analíticas de inventario.
- `get_inventory_context(session: Session) -> Dict[str, Any]` - Obtiene el contexto completo del inventario.
- `analytics_inventory_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager), sync: SyncStateManager = Depends(get_sync_manager))` - API que devuelve datos de inventario optimizados.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas a la base de datos directamente.

### Estado y Variables Globales
- `logger` - Manejador de registros.
- `router` - Ruta FastAPI para el módulo de analíticas de inventario.

### Dependencias y Flujo
- **Dependencias Importadas**: 
  - `get_current_user`, `get_session_dep`, `get_cache_manager`, `get_sync_manager` (desde `core.auth`, `core.database`, `core.state`).
  - `InventoryService` (desde `services.inventory_service`).
  - `AnalyticsInventoryResponse` (desde `core.schemas`).

- **Dependencias Exportadas**: 
  - No se exportan dependencias.

- **Flujo de Datos**:
  - El archivo recibe una solicitud HTTP y utiliza dependencias para obtener el contexto del inventario.
  - Luego, intenta recuperar los datos desde la caché. Si no están en caché, obtiene los datos del servicio de inventario, limpia el contexto y lo almacena en caché antes de devolverlo.

Este archivo es parte del módulo de analíticas de inventario y se encarga de manejar las solicitudes para obtener datos optimizados del inventario.

