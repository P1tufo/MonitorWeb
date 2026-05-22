## Archivo: ./routes/inventory.py

### Resumen Funcional
Este archivo contiene rutas y lógica para el análisis de inventario. Define endpoints para redirigir a una página de análisis y proporcionar datos de inventario en formato JSON.

### Catálogo de Funciones y Clases
- `analytics_inventory_redirect(request: Request, state: AppState = Depends(get_app_state))` - Redirige a la página de análisis con el tab de inventario activo.
- `get_inventory_context(session: Session) -> Dict[str, Any]` - Obtiene el contexto completo del inventario.
- `analytics_inventory_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Endpoint para obtener datos de inventario en formato JSON.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `AppState` - Almacena el estado de la aplicación, incluyendo caché y sincronización.
- `InventoryService` - Servicio que maneja las operaciones del inventario.

### Dependencias y Flujo
- **Librerías Externas**: `logging`, `sqlalchemy`, `pandas`, `datetime`, `fastapi`, `core.auth`, `core.database`, `core.schemas`, `core.state`, `core.wms_config`, `repositories`, `routes.analytics_proyecciones`, `core.utils`, `services.inventory_service`.
- **Flujo Interno**: El archivo interactúa con el servicio de inventario para obtener y procesar datos, luego los devuelve en formato JSON. Utiliza un estado de aplicación para almacenar y recuperar datos en caché.

