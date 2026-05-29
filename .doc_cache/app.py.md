## Archivo: ./app.py

### Resumen Funcional
El archivo `app.py` es el punto de entrada para la configuración y ejecución de una aplicación FastAPI. Se encarga de montar rutas, recursos estáticos y gestionar el ciclo de vida de la aplicación, incluyendo la inicialización de bases de datos y servicios.

### Catálogo de Funciones y Clases
- `lifespan(fastapi_app: FastAPI)` - Manejador del ciclo de vida de la aplicación, que se ejecuta al iniciar y detener el servidor.
- `initialize_app(fastapi_app: FastAPI) -> None` - Configura y prepara la aplicación FastAPI.

### Interacción con Base de Datos
- Motor de BD: SQLite (implicado en las consultas SQL crudas).
- Tablas modificadas/leídas:
  - `analytics_snapshots`
- Columnas modificadas/leídas:
  - `data`

### Estado y Variables Globales
- No aplica.

### Dependencias y Flujo
- Librerías utilizadas: `fastapi`, `logging`, `contextlib`, `warnings`, `pandas`, `sqlalchemy`.
- Comunicación con otros archivos del proyecto:
  - `config.py`: Para configuraciones globales.
  - `core.app_instance`: Para la instancia de la aplicación FastAPI.
  - `routes.config`: Para el registro de rutas.
  - `core.auth`: Para la inicialización y gestión de autenticación.
  - `core.db_config_manager`: Para la configuración y semillas de bases de datos.
  - `core.database`: Para obtener sesiones de base de datos.
  - `core.state`: Para el estado global de la aplicación.
  - `core.task_manager`: Para la gestión de tareas en segundo plano.
  - `routes.tasks`: Para el contexto de tareas.
  - `services.deliveries_service` y `services.inventory_service`: Para servicios relacionados con entregas e inventario.
  - `core.watcher`: Para el monitor de cambios.

