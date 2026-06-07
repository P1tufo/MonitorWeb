## Archivo: ./app.py

### Resumen Funcional
El archivo `app.py` es el punto de entrada para la configuración y ejecución del servidor FastAPI. Se encarga de montar las rutas, recursos estáticos y gestionar el ciclo de vida de la aplicación, incluyendo la inicialización de tablas de autenticación, carga de snapshots desde la base de datos y la ejecución de tareas en segundo plano.

### Catálogo de Funciones y Clases
- `lifespan(fastapi_app: FastAPI)` - Manejador del ciclo de vida de la aplicación, incluyendo inicialización y limpieza.
- `initialize_app(fastapi_app: FastAPI) -> None` - Configura y prepara la aplicación FastAPI.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `analytics_snapshots`
- **Columnas**:
  - `data`
  - `key`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `fastapi`
  - `sqlalchemy`
  - `logging`
  - `warnings`
  - `asyncio`
  - `json`
  - `os`
  - `contextlib`

- **Archivos del Proyecto Importados**:
  - `config`
  - `core.app_instance`
  - `routes.config`
  - `core.auth`
  - `core.db_config_manager`
  - `core.database`
  - `core.state`
  - `core.task_manager`
  - `scripts.bundler`
  - `services.background_tasks`
  - `core.watcher`

- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno

- **Dirección del Flujo de Datos**:
  - El archivo importa configuraciones y componentes necesarios para la inicialización y ejecución del servidor FastAPI.
  - Realiza tareas como la carga de snapshots desde la base de datos y el inicio de tareas en segundo plano.
  - Maneja el ciclo de vida de la aplicación, incluyendo la inicialización y limpieza.

