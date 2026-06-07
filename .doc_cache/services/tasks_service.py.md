## Archivo: ./services/tasks_service.py

### Resumen Funcional
El archivo `tasks_service.py` contiene la lógica del servicio para generar y gestionar el contexto analítico de las Operaciones Técnicas (OTs) en un sistema de monitoreo de almacén (WMS). Este servicio utiliza SQLAlchemy para interactuar con una base de datos SQLite, pandas para procesamiento de datos, y FastAPI para la gestión del estado.

### Catálogo de Funciones y Clases
- `TasksService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - **Propósito**: Proporciona métodos para obtener y gestionar el contexto analítico de las OTs.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `config_queries` (Lectura)
- **Columnas**:
  - `sql_text`, `visual_state` (Tabla `config_queries`)
- **Consultas SQL Crudas**:
  ```sql
  SELECT sql_text, visual_state FROM config_queries WHERE query_id = 'ots_list_pending'
  SELECT sql_text, visual_state FROM config_queries WHERE query_id = 'ots_kpi_pending'
  SELECT sql_text, visual_state FROM config_queries WHERE query_id = 'ots_kpi_users'
  SELECT sql_text, visual_state FROM config_queries WHERE query_id = 'ots_kpi_critical'
  ```

### Estado y Variables Globales
- **Ninguna**

### Dependencias y Flujo
- **Librerías Externas**:
  - `logging`
  - `datetime`
  - `pandas`
  - `sqlalchemy`
- **Archivos del Proyecto que Importan a Este Archivo**:
  - `core.state.get_cache_manager()`
  - `core.utils.sanitize_for_json()`
  - `repositories.TasksRepository`
- **Archivos del Proyecto que Este Archivo Importa**:
  - No aplica
- **Dirección del Flujo de Datos**:
  - Desde el servicio hasta la base de datos para leer y escribir datos.
  - Desde el servicio hasta los repositorios para obtener datos analíticos.
  - Desde los repositorios hasta pandas para procesar datos.
  - Desde pandas hasta el contexto final que se almacena en caché.

