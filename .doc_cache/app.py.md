## Archivo: ./app.py

### Resumen Funcional
El archivo `app.py` es el punto de entrada para la configuración y ejecución del servidor FastAPI. Se encarga de montar las rutas, recursos estáticos y gestionar el ciclo de vida de la aplicación, incluyendo la inicialización de tablas de autenticación, carga de snapshots desde la base de datos y la ejecución de tareas en segundo plano.

### Catálogo de Funciones y Clases
- `lifespan(fastapi_app: FastAPI)` - Manejador del ciclo de vida de la aplicación, gestionando el arranque y cierre.
- `initialize_app(fastapi_app: FastAPI) -> None` - Configura y prepara la aplicación FastAPI.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - `analytics_snapshots`
- Columnas:
  - `data`
  - `key`

### Estado y Variables Globales
- No se detectan variables globales explícitas en el código proporcionado.

### Dependencias y Flujo
- **Dependencias Externas**: FastAPI, SQLAlchemy, pandas.
- **Archivos del Proyecto Importados**:
  - `config.py`
  - `core.app_instance`
  - `routes.config`
  - `core.auth`
  - `core.db_config_manager`
  - `scripts.bundler`
  - `core.database`
  - `core.state`
  - `core.task_manager`
  - `services.background_tasks`
  - `core.watcher`
- **Archivos del Proyecto que Importan a Este Archivo**: Ninguna.
- **Flujo de Datos**:
  - La aplicación se inicia y configura en el archivo `main.py`.
  - El ciclo de vida de la aplicación se gestiona mediante el contexto asincrónico `lifespan`.
  - Se registran rutas y recursos estáticos.
  - Se manejan excepciones globales, incluyendo redirecciones para autenticación.

