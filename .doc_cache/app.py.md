## Archivo: ./app.py

### Resumen Funcional
El archivo `app.py` es el punto de entrada para la configuración y ejecución del servidor FastAPI. Define el ciclo de vida de la aplicación, registra las rutas y monta los recursos estáticos.

### Catálogo de Funciones y Clases
- `lifespan(fastapi_app: FastAPI)` -> `None`: Maneja el ciclo de vida de la aplicación, inicializando tablas, cargando snapshots, refrescando analíticas y gestionando tareas en segundo plano.
- `initialize_app(fastapi_app: FastAPI) -> None`: Configura y prepara la aplicación FastAPI, registrando rutas y recursos estáticos.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Operaciones**:
  - `SELECT` en tablas `analytics_snapshots`
  - `INSERT/UPDATE` en tablas no especificadas explícitamente

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
- **Caché en memoria**: Utiliza variables globales (`fastapi_app.state.global_state`) para almacenar el estado global de la aplicación.
- **Mecanismos de invalidación de caché**: No especificado.
- **Variables de entorno o sesión utilizadas**: No se usan variables de entorno explícitas.

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- **Librerías externas**:
  - `fastapi`
  - `sqlalchemy`
  - `pandas`
- **Archivos del proyecto que IMPORTA a este archivo**: 
  - `config`, `core.app_instance`, `routes.config`, `core.auth`, `core.db_config_manager`, `core.database`, `core.state`, `core.task_manager`, `routes.tasks`, `services.deliveries_service`, `services.inventory_service`
- **Archivos del proyecto que este archivo IMPORTA**: 
  - No aplica.

**Flujo de datos**: El archivo importa y utiliza varios módulos para configurar la aplicación, gestionar el ciclo de vida, registrar rutas y montar recursos estáticos.

