## Archivo: ./services/tasks_service.py

### Resumen Funcional
El archivo `tasks_service.py` contiene la lógica del servicio para gestionar y analizar las Operaciones Técnicas (OTs) en el sistema de monitoreo de almacén (WMS). Genera un contexto analítico que incluye resúmenes, tendencias, usuarios involucrados, tipos de OTs, movimientos no paletizados y KPIs dinámicos.

### Catálogo de Funciones y Clases
- `TasksService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `get_full_context()` - Genera y cachea el contexto analítico para la gestión de OTs.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: `config_queries`
    - Columnas: `sql_text`, `visual_state`, `query_id`
  - Tabla: No especificadas explícitamente, pero se usan consultas SQL crudas para leer datos.
- **Consultas SQL Crudas:** Se realizan consultas SQL para obtener resúmenes y KPIs dinámicos.

### Estado y Variables Globales
- **Variables Globales:** Ninguna.
- **Estado de Sesión:** Utiliza `get_app_state()` para acceder al estado de la aplicación, que incluye el caché.
- **Diccionarios Quemados:** Ninguno.

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `sqlalchemy`
  - `logging`
  - `datetime`
- **Archivos del Proyecto que Importa:**
  - `repositories/TasksRepository.py`
  - `core/state.py`
  - `core/utils.py`
- **Archivos del Proyecto que Son Importados por Este Archivo:**
  - Ninguno.
- **Dirección del Flujo de Datos:** El flujo de datos comienza con la solicitud de contexto, pasa a través del servicio para generar los datos necesarios y finalmente devuelve el contexto analítico.

