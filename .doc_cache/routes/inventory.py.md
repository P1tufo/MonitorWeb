## Archivo: ./routes/inventory.py

### Resumen Funcional
El archivo `inventory.py` contiene rutas y lógica para el análisis de inventario en un sistema de gestión de almacén (WMS). Ofrece una redirección a la página de analíticas de inventario y una API que devuelve datos de inventario en formato JSON.

### Catálogo de Funciones y Clases
- `analytics_inventory_redirect(request: Request, state: AppState = Depends(get_app_state))` - Redirige a la página de analíticas de inventario.
- `get_inventory_context(session: Session) -> Dict[str, Any]` - Obtiene el contexto completo del inventario.
- `analytics_inventory_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - API que devuelve datos de inventario en formato JSON.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos.

### Estado y Variables Globales
- `AppState` - Almacena el estado del sistema, incluyendo caché y indicadores de sincronización.
- `COST_CENTER_MAPPING` - Mapeo de centros de costo.

### Dependencias y Flujo
- **Dependencias Importadas**: 
  - `fastapi`, `sqlalchemy`, `pandas`, `datetime`, `typing`.
  - `core.auth`, `core.database`, `core.schemas`, `core.state`, `core.wms_config`, `repositories`, `routes.analytics_proyecciones`, `core.utils`, `services.inventory_service`.

- **Dependencias Exportadas**: 
  - No exporta ninguna dependencia.

- **Flujo de Datos**:
  - El archivo recibe una solicitud HTTP y utiliza servicios para obtener datos de inventario.
  - Los datos son procesados y devueltos en formato JSON a través de la API.

