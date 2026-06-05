# Documentación Técnica - Directorio: raiz
Compilado el: 2026-06-05 03:03:51
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

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


---

## Archivo: ./config.py

### Resumen Funcional
Este archivo `config.py` contiene configuraciones globales y variables de entorno necesarias para el sistema de monitoreo de almacén (WMS). Define rutas, parámetros del servidor, directorios de almacenamiento y realiza validaciones iniciales.

### Catálogo de Funciones y Clases
- `validate_config() -> None` - Realiza comprobaciones de salud en la configuración.
- `ensure_project_structure() -> None` - Crea los directorios necesarios para el funcionamiento de la app si no existen.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
- Variables globales y de módulo: `BASE_DIR`, `DB_PATH`, `PDF_STORAGE`, `CLEANSED_DIR`, `TEMP_DIR`, `CACHE_DIR_NAME`, `CACHE_DIR`, `TUNNEL_URL_FILE`, `NGROK_BIN`, `LOG_FILE`, `APP_HOST`, `APP_PORT`, `APP_RELOAD`, `_home`, `DEFAULT_ONEDRIVE`, `ONEDRIVE_PATH`, `DELIVERIES_DIR`, `STOCK_DIR`, `TASKS_DIR`, `INVENTORY_DIR`.
- Caché en memoria: No aplica.
- Caché persistente: No aplica.
- Mecanismos de invalidación de caché: No aplica.
- Variables de entorno o sesión utilizadas: `DB_PATH`, `PDF_STORAGE`, `CLEANSED_DIR`, `TEMP_DIR`, `CACHE_DIR_NAME`, `APP_HOST`, `APP_PORT`, `APP_RELOAD`, `ONE_DRIVE_PATH`.

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- Librerías externas: `os`, `logging`, `typing`, `pathlib`.
- Archivos del proyecto que ESTE archivo IMPORTA (consume): No aplica.
- Archivos del proyecto que IMPORTAN a este archivo (lo consumen): FastAPI, SQLAlchemy, SQLite.
- Dirección del flujo de datos: El archivo se ejecuta al importarse para configurar y validar el entorno del sistema.


---

## Archivo: ./main.py

### Resumen Funcional
El archivo `main.py` es el punto de entrada oficial del sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Su rol es configurar e iniciar los servicios de la plataforma, incluyendo la activación de un túnel remoto para acceso remoto y el lanzamiento del servidor web utilizando Uvicorn.

### Catálogo de Funciones y Clases
- `start_application() -> None` - Configura e inicia los servicios de la plataforma. Lanza excepciones específicas como `KeyboardInterrupt` y cualquier otra excepción crítica.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
- Variables globales y de módulo: `APP_HOST`, `APP_PORT`, `APP_RELOAD`.
- Mecanismos de invalidación de caché: No aplica.
- Variables de entorno o sesión utilizadas: No aplica.

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- Librerías externas:
  - `uvicorn`
  - `logging`
- Archivos del proyecto que este archivo importa (`app`, `config`, `services.tunnel`).
- Archivos del proyecto que importan a este archivo: No aplica.
- Dirección del flujo de datos: El archivo es el punto de entrada principal, no consume ni produce datos directamente.


---

