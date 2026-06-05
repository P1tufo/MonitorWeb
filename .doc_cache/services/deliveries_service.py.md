## Archivo: ./services/deliveries_service.py

### Resumen Funcional
El archivo `deliveries_service.py` contiene la lógica del servicio de entregas para un sistema de monitoreo de almacén (WMS). Este servicio se encarga de generar el contexto completo para las entregas, incluyendo información sobre áreas de negocio y widgets configurados.

### Catálogo de Funciones y Clases
- `DeliveriesService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - **Propósito**: Prepara el servicio para interactuar con la base de datos proporcionada.
  
- `get_full_context() -> Dict[str, Any]` - Genera y devuelve un contexto completo para las entregas.
  - **Propósito**: Recopila y organiza información relevante desde la base de datos y otros servicios para proporcionar un contexto detallado.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `outbound_deliveries`
- **Columnas**:
  - `area_negocio`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**: 
  - `sqlalchemy.orm.Session`
  - `logging`
  - `typing.Dict`, `typing.Any`
  
- **Archivos del Proyecto que Importan a este Archivo**:
  - `routes.inventory.get_inventory_context`
  - `routes.tasks.get_tasks_context`
  - `routes.analytics_proyecciones.get_proyecciones_context`

- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno

- **Flujo de Datos**: 
  - El servicio recibe una sesión de base de datos y utiliza esta para consultar la tabla `outbound_deliveries`.
  - Luego, intenta cargar contextos adicionales desde otros servicios (`inventory`, `tasks`, `analytics_proyecciones`) y los combina en el contexto final.

