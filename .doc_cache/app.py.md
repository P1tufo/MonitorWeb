## Archivo: ./app.py

### Resumen Funcional
El archivo `app.py` es el punto de entrada para la configuración y ejecución de una aplicación FastAPI. Se encarga de montar rutas, recursos estáticos y gestionar el ciclo de vida de la aplicación, incluyendo la inicialización de bases de datos y la carga de snapshots.

### Catálogo de Funciones y Clases
- `lifespan(fastapi_app: FastAPI)` - Manejador del ciclo de vida de la aplicación, que se ejecuta al inicio y finalizar el servidor.
- `initialize_app(fastapi_app: FastAPI) -> None` - Configura y prepara la aplicación FastAPI.

### Interacción con Base de Datos
- Motor de BD: SQLite (implicado en las consultas SQL crudas).
- Tablas modificadas/leídas:
  - `analytics_snapshots`
- Columnas leídas/modificadas:
  - `data` en la tabla `analytics_snapshots`

### Estado y Variables Globales
- No aplica.

### Dependencias y Flujo
- Librerías utilizadas: `fastapi`, `logging`, `asyncio`, `sqlalchemy`.
- Comunicación con otros archivos del proyecto:
  - `config.py` (para configuraciones globales).
  - `core.app_instance` (para la instancia de FastAPI).
  - `routes.config` (para el registro de rutas).
  - `core.auth`, `core.db_config_manager`, `core.state`, `core.task_manager`, `routes.tasks`, `services.deliveries_service`, `services.inventory_service` (varias partes del sistema para inicialización y gestión).

