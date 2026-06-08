## Archivo: ./services/tasks_service.py

### Resumen Funcional
El archivo `tasks_service.py` contiene la lógica del servicio para generar el contexto analítico para la gestión de Operaciones Técnicas (OTs) en un sistema de monitoreo de almacén (WMS). Este servicio utiliza SQLAlchemy para interactuar con una base de datos SQLite y pandas para procesar los datos.

### Catálogo de Funciones y Clases
- `TasksService(session: Session)` - Inicializa el servicio con una sesión de la base de datos.
  - **Propósito**: Proporciona métodos para obtener diferentes conjuntos de datos relacionados con las OTs.

- `get_full_context()` - Genera el contexto analítico para la gestión de OTs.
  - **Propósito**: Recopila y procesa datos desde múltiples fuentes (tablas de la base de datos, consultas dinámicas) para generar un diccionario con información relevante.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `config_queries` - Almacena consultas y estados visuales configurados.
- **Columnas**:
  - `sql_text` - Texto de la consulta SQL.
  - `visual_state` - Estado visual de la consulta.
  - `query_id` - Identificador único de la consulta.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `pandas`
  - `sqlalchemy`
  - `logging`
  - `datetime`

- **Archivos del Proyecto que Importa a este Archivo (lo consumen)**:
  - `repositories/TasksRepository.py` - Para acceder a los datos de las OTs.

- **Archivos del Proyecto que Este Archivo IMPORTA**:
  - `core/cache_decorator.py`
  - `core/state.py`
  - `core/utils.py`

- **Dirección del Flujo de Datos**:
  - Desde el servicio (`TasksService`) se obtienen datos desde la base de datos y las tablas configuradas.
  - Los datos son procesados y transformados en un formato adecuado para su visualización o análisis.
  - El resultado final es un diccionario que contiene los datos procesados, que luego puede ser utilizado por otras partes del sistema.

