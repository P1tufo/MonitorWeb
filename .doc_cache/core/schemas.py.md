## Archivo: ./core/schemas.py

### Resumen Funcional
Este archivo define esquemas de datos utilizando Pydantic para representar respuestas de diferentes endpoints en una aplicación. Cada esquema incluye un diccionario de datos y un indicador booleano que indica si la respuesta está sincronizando.

### Catálogo de Funciones y Clases
- `DashboardResponse(data: Dict[str, Any], is_syncing: bool)` - Representa la respuesta para el endpoint del panel de control.
- `AnalyticsDeliveriesResponse(data: Dict[str, Any], is_syncing: bool)` - Representa la respuesta para el endpoint de análisis de entregas.
- `AnalyticsInventoryResponse(data: Dict[str, Any], is_syncing: bool)` - Representa la respuesta para el endpoint de análisis de inventario.
- `AnalyticsTasksResponse(data: Dict[str, Any], is_syncing: bool)` - Representa la respuesta para el endpoint de análisis de tareas.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencia única:
- `pydantic` - Usada para definir los esquemas de datos.

