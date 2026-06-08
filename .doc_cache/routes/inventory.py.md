## Archivo: ./routes/inventory.py

### Resumen Funcional
El archivo `inventory.py` contiene rutas y lógica para el análisis de inventario en un sistema de gestión de almacén (WMS). Ofrece una redirección a la página de analíticas de inventario y una API que devuelve datos de inventario limpios.

### Catálogo de Funciones y Clases
- `analytics_inventory_redirect(request: Request)` - Redirige a la página de analíticas de inventario.
- `get_inventory_context(session: Session) -> Dict[str, Any]` - Obtiene el contexto completo del inventario.
- `analytics_inventory_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), sync: SyncStateManager = Depends(get_sync_manager))` - API que devuelve datos de inventario limpios.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: `pandas`, `fastapi`, `sqlalchemy`.
- **Archivos del Proyecto que IMPORTA**:
  - `core.auth.get_current_user`
  - `core.database.get_session_dep`
  - `core.schemas.AnalyticsInventoryResponse`
  - `core.state.SyncStateManager`
  - `core.utils.sanitize_for_json`
  - `core.wms_config.COST_CENTER_MAPPING`
  - `repositories.InventoryRepository`
  - `routes.analytics_proyecciones.get_proyecciones_context`
  - `services.inventory_service.InventoryService`
- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno.

**Flujo de Datos**:
1. El usuario accede a la ruta `/inventory`, lo cual es redirigido a `/analytics?tab=inventory`.
2. Para la API `/api/v1/analytics/inventory`, se obtiene el contexto del inventario utilizando `InventoryService` y se filtran los datos para eliminar campos no deseados (`'request', 'user', 'is_syncing'`). El resultado se devuelve como una respuesta JSON con el modelo `AnalyticsInventoryResponse`.

