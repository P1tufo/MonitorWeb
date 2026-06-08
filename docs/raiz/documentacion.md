# Documentación Técnica - Directorio: raiz
Compilado el: 2026-06-07 18:34:58
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

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


---

## Archivo: ./config.py

### Resumen Funcional
Este archivo `config.py` configura y valida los parámetros de configuración del sistema de monitoreo de almacén (WMS). Define rutas y variables globales para el almacenamiento de datos, la base de datos, el servidor web y las fuentes externas. También incluye funciones para validar la configuración y asegurar la estructura del proyecto.

### Catálogo de Funciones y Clases
- `validate_config()` - Realiza comprobaciones de salud en la configuración.
- `ensure_project_structure()` - Crea los directorios necesarios para el funcionamiento de la app si no existen.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `BASE_DIR` - Directorio raíz del proyecto.
- `DB_PATH` - Ruta a la base de datos SQLite.
- `PDF_STORAGE` - Ruta para almacenar PDFs generados.
- `CLEANSED_DIR` - Ruta para archivos limpios.
- `TEMP_DIR` - Ruta para directorios temporales.
- `CACHE_DIR_NAME` - Nombre del directorio de caché.
- `CACHE_DIR` - Ruta al directorio de caché.
- `TUNNEL_URL_FILE` - Ruta al archivo que contiene la URL del túnel.
- `NGROK_BIN` - Ruta al binario de ngrok.
- `LOG_FILE` - Ruta al archivo de registro del servidor.
- `APP_HOST` - Host del servidor web.
- `APP_PORT` - Puerto del servidor web.
- `APP_RELOAD` - Indica si el servidor debe reiniciarse automáticamente.
- `DEFAULT_ONEDRIVE` - Ruta predeterminada para OneDrive.
- `ONEDRIVE_PATH` - Ruta a la carpeta de transacciones WMS en OneDrive.
- `DELIVERIES_DIR`, `STOCK_DIR`, `TASKS_DIR`, `INVENTORY_DIR`, `MB5B_DIR` - Subdirectorios dentro de OneDrive.

### Dependencias y Flujo
- **Dependencias**: `logging`, `os`, `pathlib`, `typing`.
- **Flujo de Datos**:
  - El archivo se importa por otros archivos del proyecto para obtener las configuraciones necesarias.
  - Otros archivos pueden importar este archivo para utilizar las variables globales y funciones definidas aquí.


---

## Archivo: ./main.py

### Resumen Funcional
El archivo `main.py` es el punto de entrada oficial del sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Inicializa y gestiona la ejecución del servidor web utilizando Uvicorn, configurando servicios adicionales como un túnel Ngrok para acceso remoto.

### Catálogo de Funciones y Clases
- `start_application()` - Configura e inicia los servicios de la plataforma, incluyendo el inicio del túnel Ngrok y el lanzamiento del servidor web con Uvicorn.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- `APP_HOST` - Dirección IP o nombre de host donde se ejecutará el servidor.
- `APP_PORT` - Puerto en el que se escuchará el servidor.
- `APP_RELOAD` - Indica si el servidor debe reiniciarse automáticamente al detectar cambios.

### Dependencias y Flujo
- **Dependencias Externas**: `uvicorn`, `logging`
- **Archivos Importados**:
  - `app` desde `app`
  - `start_tunnel` y `stop_tunnel` desde `services.tunnel`
- **Archivos que Importan a este Archivo**: Ninguno.
- **Flujo de Datos**: El archivo inicia el servidor web utilizando Uvicorn, configurando previamente un túnel Ngrok para acceso remoto.


---

