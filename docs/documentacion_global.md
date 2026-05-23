# Documentación Técnica Global - MonitorWeb
Compilado el: 2026-05-23 00:11:13
Modelo: qwen2.5-coder:7b | Hardware: M1 Pro Optimized

---

## Análisis de Arquitectura Global

### Arquitectura General Detectada

La estructura del proyecto sugiere una arquitectura **Modular**. Esto se debe a la organización de los módulos y carpetas que separan diferentes aspectos del sistema, como el código principal (`app.py`), las configuraciones (`config.py`), las rutas (`routes/`), los modelos (`core/models.py`), las tareas (`core/task_manager.py`), las pruebas (`tests/`), etc.

### Propósito Probable de las Carpetas Principales

- **`app.py`**: Punto de entrada principal del aplicativo.
- **`config.py`**: Archivo de configuración general del sistema.
- **`main.py`**: Posiblemente un archivo auxiliar para la ejecución principal del proyecto.
- **`test_deliveries.py`**: Pruebas específicas relacionadas con las entregas.
- **`core/`**: Contiene el código central y fundamental del sistema, incluyendo modelos, lógica de negocio, seguridad, etc.
  - **`models.py`, `models_auth.py`, `models_transaccional.py`**: Definen los modelos de datos.
  - **`auth.py`, `security.py`**: Manejo de autenticación y seguridad.
  - **`database.py`, `db_config_manager.py`**: Configuración y gestión de la base de datos.
  - **`pdf_engine.py`, `pdf_queries.py`, `pdf_reports.py`**: Generación de PDFs.
  - **`query_engine.py`**: Motor de consultas.
  - **`schemas.py`**: Esquemas para validaciones de datos.
  - **`state.py`**: Gestión del estado del sistema.
  - **`task_manager.py`**: Administrador de tareas.
  - **`utils.py`**: Funciones utilitarias.
  - **`wms_config.py`, `wms_utils.py`**: Configuración y utilidades específicas para el WMS (Warehouse Management System).
- **`bin/`**: Contiene herramientas binarias, como `ngrok`.
- **`deploy/`**: Archivos relacionados con la implementación del sistema.
  - **`Dockerfile`, `docker-compose.dev.yml`, `docker-compose.yml`**: Configuraciones para Docker y Compose.
- **`setup/`**: Contiene archivos de configuración y scripts para el entorno de desarrollo.
  - **`package-lock.json`, `package.json`, `pytest.ini`, `requirements.txt`, `run_tests.sh`**: Dependencias, configuración de pruebas y scripts de instalación.
- **`tests/`**: Archivos de prueba unitaria y de integración.
  - **`conftest.py`, `test_api.py`, `test_auth.py`, etc.**: Pruebas específicas para diferentes componentes del sistema.
- **`repositories/`**: Contiene la lógica de acceso a datos (DAOs).
  - **`base.py`, `deliveries.py`, `inventory.py`, `tasks.py`**: Implementaciones de DAOs.
- **`docs/`**: Documentación del proyecto y sus componentes.
  - **`documentacion_global.md`, `mejoras_global.md`, `plan_maestro.md`**: Documentación general.
  - **`core/`, `raiz/`, `tests/`, `repositories/`, etc.**: Documentación específica por módulo.
- **`DELIVERIES_cleansed/`**: Archivos limpios de entregas.
- **`static/`**: Recursos estáticos del frontend, como CSS y JavaScript.
  - **`css/`, `js/`**: Estilos y scripts.
- **`scripts/`**: Scripts auxiliares y procesos.
  - **`doc_generator.py`, `free_ram.py`, `main_processor.py`**: Scripts específicos para el proyecto.
- **`db/`**: Archivos relacionados con la base de datos.
  - **`consolidator.py`, `data.db`, `monitor.db`, etc.**: Scripts y archivos de base de datos.
- **`templates/`**: Plantillas HTML del frontend.
  - **`analytics_proyecciones.html`, `dashboard.html`, etc.**: Plantillas específicas para diferentes vistas.
  - **`partials/`**: Fragmentos de plantilla reutilizables.
- **`data/`**: Archivos de datos y backups.
  - **`wms_transactions.db`, `wms_transactions.db-shm`, etc.**: Archivos de base de datos del WMS.
- **`routes/`**: Definición de rutas y endpoints del API.
  - **`analytics_proyecciones.py`, `auth.py`, etc.**: Rutas específicas para diferentes funcionalidades.
- **`services/`**: Implementación de servicios de negocio.
  - **`dashboard_service.py`, `deliveries_service.py`, etc.**: Servicios específicos para diferentes partes del sistema.
  - **`etl/`**: Implementación de ETL (Extract, Transform, Load).

### Organización Lógica de las Dependencias

- **Dependencias Internas**:
  - El código dentro de `core/` depende de otros módulos dentro de la misma carpeta para su funcionamiento.
  - Los servicios (`services/`) utilizan los modelos y DAOs definidos en `core/`.
  - Las rutas (`routes/`) interactúan con los servicios.

- **Dependencias Externas**:
  - El proyecto utiliza bibliotecas externas como Flask para el framework web, SQLAlchemy para ORM, PyPDF2 para generación de PDFs, etc.
  - Dependencias gestionadas a través de `requirements.txt`.

- **Pruebas**:
  - Las pruebas (`tests/`) dependen del código principal y de las configuraciones definidas en `setup/`.
  - Utilizan bibliotecas como pytest para ejecutar pruebas unitarias y de integración.

La estructura modular permite una separación clara de responsabilidades, facilitando el mantenimiento y la escalabilidad del proyecto.


---

## Archivo: ./app.py

### Resumen Funcional
El archivo `app.py` es el punto de entrada para la configuración y ejecución de una aplicación FastAPI. Se encarga de montar rutas, recursos estáticos y gestionar el ciclo de vida de la aplicación, incluyendo la inicialización de bases de datos y la carga de snapshots.

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
- Librerías utilizadas: FastAPI, SQLAlchemy, pandas.
- Comunicación con otros archivos del proyecto:
  - `config.py`: Para configuraciones globales.
  - `core.app_instance`: Para la instancia de la aplicación FastAPI.
  - `routes.config`: Para el registro de rutas.
  - `core.auth`, `core.db_config_manager`, `core.state`, `core.task_manager`, `routes.tasks`, `services.deliveries_service`, `services.inventory_service`: Para la inicialización y gestión del estado global, tareas asíncronas y servicios.


---

## Archivo: ./config.py

### Resumen Funcional
Este archivo config.py define y gestiona las configuraciones globales del proyecto, incluyendo rutas de directorios, parámetros del servidor y variables de entorno. También realiza comprobaciones de salud en la configuración y asegura la estructura del proyecto al importar el módulo.

### Catálogo de Funciones y Clases
- `validate_config()` - Realiza comprobaciones de salud en la configuración.
- `ensure_project_structure()` - Crea los directorios necesarios para el funcionamiento de la app si no existen.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `BASE_DIR` - Directorio raíz del proyecto.
- `DB_PATH` - Ruta a la base de datos.
- `PDF_STORAGE` - Ruta para almacenar PDFs generados.
- `CLEANSED_DIR` - Ruta para archivos limpios.
- `TEMP_DIR` - Ruta para directorios temporales.
- `CACHE_DIR_NAME` - Nombre del directorio de caché.
- `CACHE_DIR` - Ruta al directorio de caché.
- `TUNNEL_URL_FILE` - Ruta al archivo que contiene la URL del túnel.
- `NGROK_BIN` - Ruta al binario de ngrok.
- `LOG_FILE` - Ruta al archivo de registro del servidor.
- `APP_HOST` - Host del servidor.
- `APP_PORT` - Puerto del servidor.
- `APP_RELOAD` - Indica si el servidor debe reiniciarse automáticamente.
- `DEFAULT_ONEDRIVE` - Ruta predeterminada a OneDrive.
- `ONEDRIVE_PATH` - Ruta a OneDrive.
- `DELIVERIES_DIR`, `STOCK_DIR`, `TASKS_DIR`, `INVENTORY_DIR` - Subdirectorios de transacciones WMS.

### Dependencias y Flujo
- Librerías utilizadas: `os`, `logging`, `typing`, `pathlib`.
- No comunica con otros archivos del proyecto.


---

## Archivo: ./core/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./core/app_instance.py

### Resumen Funcional
El archivo `app_instance.py` configura la instancia principal de una aplicación FastAPI, estableciendo su título, descripción, versión y URLs para la documentación. También configura el motor de plantillas Jinja2 con seguridad reforzada.

### Catálogo de Funciones y Clases
- `FastAPI()` - Crea una instancia de la clase FastAPI.
- `Jinja2Templates(directory=str(templates_path))` - Configura el motor de plantillas Jinja2 para renderizar vistas HTML.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `app: FastAPI` - Instancia principal de la aplicación FastAPI.
- `templates: Jinja2Templates` - Motor de plantillas Jinja2 configurado.

### Dependencias y Flujo
- `fastapi`: Librería para crear aplicaciones web API rápidas.
- `fastapi.templating`: Módulo para renderizar plantillas HTML con Jinja2.
- `config`: Módulo que contiene la configuración global de la aplicación, incluyendo el directorio base (`BASE_DIR`).


---

## Archivo: ./core/auth.py

### Resumen Funcional
El archivo `auth.py` proporciona funcionalidades de autenticación y seguridad utilizando JSON Web Tokens (JWT) y OAuth2, con soporte para roles de usuario ('admin' y 'viewer'). Incluye funciones para crear tokens, verificar contraseñas, manejar sesiones de usuarios y proteger endpoints en una aplicación FastAPI.

### Catálogo de Funciones y Clases
- `hash_password(plain: str) -> str` - Genera un hash bcrypt del password.
- `verify_password(plain: str, hashed: str) -> bool` - Verifica un password contra su hash bcrypt.
- `create_access_token(username: str, role: str) -> tuple[str, int]` - Crea un JWT firmado con HS256.
- `decode_token(token: str) -> Optional[dict]` - Decodifica y valida un JWT. Retorna None si es inválido o expirado.
- `get_current_user(token: Optional[str] = Depends(oauth2_scheme), request: Request = None, db: Session = Depends(get_session_dep)) -> User` - Dependencia que extrae el usuario del token JWT.
- `require_auth(user: User = Depends(get_current_user)) -> User` - Dependencia que EXIGE un usuario autenticado (no invitado).
- `require_admin(user: User = Depends(require_auth)) -> User` - Dependencia que EXIGE rol de administrador. Lanza 403 si no tiene permisos.
- `init_auth_db()` - Crea las tablas de autenticación si no existen.
- `ensure_admin_exists()` - Crea el usuario admin por defecto si no existe ningún usuario.

### Interacción con Base de Datos
- Motor: SQLAlchemy
- Tablas: `User`
- Columnas:
  - `id` (int)
  - `username` (str)
  - `password_hash` (str)
  - `role` (str)
  - `is_active` (bool)
  - `created_at` (datetime)

### Estado y Variables Globales
- `SECRET_KEY`: Clave secreta para firmar JWT.
- `ALGORITHM`: Algoritmo de firma para JWT.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración del token JWT.

### Dependencias y Flujo
- Librerías externas: `bcrypt`, `jwt`, `fastapi`
- Comunicaciones internas:
  - Conecta con el archivo `database.py` para obtener sesiones de base de datos.
  - Utiliza el modelo `User` definido en `models_auth.py`.


---

## Archivo: ./core/database.py

### Resumen Funcional
Este archivo define una fábrica de sesiones SQLAlchemy para interactuar con bases de datos SQLite y PostgreSQL. Proporciona funciones para obtener sesiones, realizar consultas y verificar la conectividad con la base de datos.

### Catálogo de Funciones y Clases
- `get_session()` - Devuelve un contexto manager que proporciona una sesión SQLAlchemy.
- `get_session_dep()` - Dependencia de FastAPI para inyección de sesiones en endpoints.
- `health_check()` - Verifica la conectividad con la base de datos.

### Interacción con Base de Datos
- **Motor**: SQLAlchemy
- **Tablas**: No aplica (no se especifican tablas directamente)
- **Columnas**: No aplica (no se especifican columnas directamente)
- **Consultas SQL Crudas**: `SELECT 1` para verificar conectividad

### Estado y Variables Globales
- `DATABASE_URL`: Variable de entorno que determina el motor de base de datos a usar.
- `_DEFAULT_URL`: URL por defecto si no se especifica `DATABASE_URL`.
- `_connect_args`: Argumentos adicionales para la conexión, dependiendo del tipo de base de datos.

### Dependencias y Flujo
- **Librerías Externas**: SQLAlchemy, logging, contextlib, typing.
- **Flujo Interno**: El archivo no interactúa con otros archivos directamente. Todas las funciones son independientes entre sí.


---

## Archivo: ./core/db_config_manager.py (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
Este archivo `db_config_manager.py` es el administrador de configuraciones dinámicas SaaS. Se encarga de la inicialización, semillas y carga de configuraciones en memoria para mejorar el rendimiento.

### Catálogo de Funciones y Clases
- `init_config_db()` - Crea las tablas de configuración SaaS via SQLAlchemy si no existen.
- `seed_initial_config()` - Inserta valores por defecto si las tablas están vacías.
- `load_config_to_memory()` - No definida en el fragmento.

### Interacción con Base de Datos
- Motor: SQLAlchemy
- Tablas:
  - `StatusMapping`
  - `CostCenterMapping`
  - `AppSetting`
  - `Holiday`
  - `ConfigQuery`
- Columnas:
  - `config_queries` → `visual_state`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas: SQLAlchemy, logging
- Comunicación con otros archivos del proyecto: No mencionado

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `db_config_manager.py` contiene configuraciones de consultas SQL y funciones para cargar estas configuraciones en una sesión de base de datos. También incluye funciones para recuperar diferentes tipos de configuración desde la base de datos.

### Catálogo de Funciones y Clases
- `ConfigQuery(query_id, sql_text, visual_state)` - Define una consulta con un ID único, texto SQL y estado visual.
- `initial_queries` - Lista de consultas iniciales a cargar en la sesión.
- `load_config_to_memory(session=None)` - Carga las configuraciones iniciales en la sesión. Esta función está obsoleta y no realiza ninguna operación.
- `_ensure_loaded()` - No hace nada, es una función auxiliar que no se utiliza.
- `get_setting(key: str, default: Any = None) -> Any` - Recupera un valor de configuración basado en su clave.
- `get_status_mapping() -> Dict[str, str]` - Devuelve un mapeo de códigos de estado a etiquetas.
- `get_cost_center_mapping() -> Dict[str, str]` - Devuelve un mapeo de códigos de centro de costo a áreas de negocio.
- `get_holidays() -> List[str]` - Devuelve una lista de fechas festivas.
- `get_query(query_id: str) -> str` - Recupera el texto SQL asociado a un ID de consulta. Esta función es obsoleta y se recomienda usar `get_query_visual_state()` en su lugar.
- `get_query_visual_state(query_id: str) -> str` - Recupera el estado visual JSON de una consulta.

### Interacción con Base de Datos
- Motor de base de datos: No especificado.
- Tablas:
  - `inventory_movements`
  - `warehouse_tasks`
  - `AppSetting`
  - `StatusMapping`
  - `CostCenterMapping`
  - `Holiday`
- Columnas:
  - `inventory_movements.cmv`, `inventory_movements.fe_contab`, `inventory_movements.material`, `inventory_movements.tipo_operacion`, `inventory_movements.registrado`
  - `warehouse_tasks.usuario`, `warehouse_tasks.fecha_conf`, `warehouse_tasks.fe_creac`
  - `AppSetting.key`, `AppSetting.typed_value()`
  - `StatusMapping.code`, `StatusMapping.label`
  - `CostCenterMapping.center_code`, `CostCenterMapping.business_area`
  - `Holiday.date_str`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas: No especificado.
- Comunicación con otros archivos del proyecto:
  - `get_session()` - Se utiliza para obtener una sesión de base de datos.


---

## Archivo: ./core/models.py

### Resumen Funcional
Este archivo define modelos ORM SQLAlchemy para el esquema de configuración SaaS, incluyendo mapeos de estados WMS a etiquetas visuales, centros de costo a áreas de negocio, parámetros de procesamiento configurables, feriados para cálculo de SLA y consultas SQL gestionadas via UI.

### Catálogo de Funciones y Clases
- `StatusMapping(code: str, label: str)` - Mapea códigos internos del WMS a etiquetas legibles por humanos.
- `CostCenterMapping(center_code: str, business_area: str)` - Asocia un código de centro de costo del WMS con un Área de Negocio.
- `AppSetting(key: str, value: str, type: str = "str")` - Parámetros de comportamiento del sistema.
- `Holiday(date_str: str)` - Días no hábiles para el cálculo de SLA.
- `ConfigQuery(query_id: str, sql_text: str = None, visual_state: str = None)` - Almacena el estado visual (JSON) de las consultas del Analytics Studio.

### Interacción con Base de Datos
- Motor: SQLAlchemy
- Tablas:
  - `config_status_mapping`
  - `config_cost_center_mapping`
  - `app_settings`
  - `config_holidays`
  - `config_queries`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencia única: `sqlalchemy`


---

## Archivo: ./core/models_auth.py

### Resumen Funcional
Este archivo define el modelo ORM para usuarios en un sistema de autenticación, incluyendo campos como nombre de usuario, contraseña hash, rol y estado de actividad.

### Catálogo de Funciones y Clases
- `User(Base)` - Define la tabla de usuarios del sistema con atributos como ID, nombre de usuario, contraseña hash, rol y estado de actividad.

### Interacción con Base de Datos
- Motor: SQLAlchemy (implícito a través de `Base`)
- Tablas: `auth_users`
- Columnas:
  - `id`: Integer, primary key, autoincrementable
  - `username`: String(50), único, no nulo, indexado
  - `password_hash`: String(255), no nulo
  - `role`: String(20), no nulo, valor por defecto "viewer"
  - `is_active`: Boolean, valor por defecto True
  - `created_at`: DateTime, valor por defecto la fecha y hora actual UTC

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas: SQLAlchemy (`from sqlalchemy import String, Boolean, DateTime, Integer`)
- No comunica con otros archivos del proyecto.


---

## Archivo: ./core/models_transaccional.py

### Resumen Funcional
Este archivo define clases que representan tablas en una base de datos relacional utilizando SQLAlchemy ORM. Cada clase corresponde a una tabla y contiene atributos que corresponden a las columnas de la tabla.

### Catálogo de Funciones y Clases
- `WarehouseTask` - Representa la tabla `warehouse_tasks`.
- `InventoryMovement` - Representa la tabla `inventory_movements`.
- `OutboundDelivery` - Representa la tabla `outbound_deliveries`.
- `StockLevel` - Representa la tabla `stock_levels`.
- `Lx02Pendiente` - Representa la tabla `lx02_pendientes`.
- `SyncManifest` - Representa la tabla `sync_manifest`.
- `AnalyticsSnapshot` - Representa la tabla `analytics_snapshots`.
- `AutorAreaMapping` - Representa la tabla `autor_area_mapping`.

### Interacción con Base de Datos
El archivo interactúa con una base de datos relacional utilizando SQLAlchemy ORM. Las tablas involucradas son:
- `warehouse_tasks`
- `inventory_movements`
- `outbound_deliveries`
- `stock_levels`
- `lx02_pendientes`
- `sync_manifest`
- `analytics_snapshots`
- `autor_area_mapping`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
Depende de la biblioteca SQLAlchemy para el ORM. No comunica con otros archivos del proyecto directamente, solo define clases que representan tablas en la base de datos.


---

## Archivo: ./core/pdf_engine.py

### Resumen Funcional
El archivo `pdf_engine.py` es un motor optimizado para la generación de documentos PDF en formato horizontal (landscape) utilizando el framework FPDF. El sistema se centra en la creación de reportes WMS (Warehouse Management System), incluyendo encabezados, tablas de materiales y códigos de barras.

### Catálogo de Funciones y Clases
- `WMS_Landscape_PDF(FPDF)` - Clase base para reportes WMS en formato horizontal.
  - `__init__()`: Inicializa la clase con configuraciones específicas para el formato horizontal.
  - `get_column_x(col: int) -> float`: Calcula la posición X de una columna específica.
  - `draw_dotted_line(x1: float, y: float, x2: float) -> None`: Dibuja una línea punteada sutil.

- `get_ots_for_delivery(entrega_id: str, conn: sqlite3.Connection) -> List[str]` - Consulta las OTs asociadas a una entrega y las devuelve como lista de strings.
  - Parámetros:
    - `entrega_id`: Identificador de la entrega.
    - `conn`: Conexión a la base de datos SQLite.
  - Retorna: Lista de números de OT.

- `_generate_barcode_stream(data: str, options: Optional[dict] = None) -> io.BytesIO` - Genera un código de barras en memoria (BytesIO).
  - Parámetros:
    - `data`: Datos a codificar en el código de barras.
    - `options`: Opciones adicionales para la generación del código de barras.
  - Retorna: Flujo de bytes con el código de barras.

- `draw_delivery_page(pdf: WMS_Landscape_PDF, header: pd.Series, items: pd.DataFrame, include_logo: bool = True, ots_list: Optional[List[str]] = None) -> None` - Dibuja una página de entrega completa utilizando sub-métodos modulares.
  - Parámetros:
    - `pdf`: Instancia de la clase `WMS_Landscape_PDF`.
    - `header`: Encabezado de la entrega en formato pandas Series.
    - `items`: Tabla de materiales en formato pandas DataFrame.
    - `include_logo`: Indica si se debe incluir el logo en el encabezado.
    - `ots_list`: Lista de números de OT.

- `_draw_page_header(pdf: WMS_Landscape_PDF, h: pd.Series, include_logo: bool)` - Dibuja el encabezado superior, logo y código de barras de la entrega.
  - Parámetros:
    - `pdf`: Instancia de la clase `WMS_Landscape_PDF`.
    - `h`: Encabezado de la entrega en formato pandas Series.
    - `include_logo`: Indica si se debe incluir el logo en el encabezado.

- `_draw_info_block(pdf: WMS_Landscape_PDF, h: pd.Series)` - Dibuja el bloque de información principal de la entrega.
  - Parámetros:
    - `pdf`: Instancia de la clase `WMS_Landscape_PDF`.
    - `h`: Encabezado de la entrega en formato pandas Series.

- `_draw_table(pdf: WMS_Landscape_PDF, items_df: pd.DataFrame)` - Dibuja la tabla de materiales con ordenamiento por ubicación.
  - Parámetros:
    - `pdf`: Instancia de la clase `WMS_Landscape_PDF`.
    - `items_df`: Tabla de materiales en formato pandas DataFrame.

- `_draw_ot_barcodes(pdf: WMS_Landscape_PDF, ots: List[str])` - Dibuja los códigos de barras de las OTs en el lateral derecho.
  - Parámetros:
    - `pdf`: Instancia de la clase `WMS_Landscape_PDF`.
    - `ots`: Lista de números de OT.

- `_draw_signature_block(pdf: WMS_Landscape_PDF)` - Dibuja los cuadros de firma al final de la página.
  - Parámetros:
    - `pdf`: Instancia de la clase `WMS_Landscape_PDF`.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQLite. Específicamente, realiza consultas a la tabla `warehouse_tasks` para obtener las OTs asociadas a una entrega.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: 
  - `io`, `logging`, `sqlite3`, `datetime`, `typing`, `pathlib`, `numpy`, `pandas`, `fpdf`, `barcode`
- **Flujo Interno**: El archivo se comunica con otros archivos del proyecto a través de la importación de módulos y funciones.


---

## Archivo: ./core/pdf_queries.py

### Resumen Funcional
Este archivo contiene funciones para construir y ejecutar consultas SQL en una base de datos SQLite, específicamente para generar reportes PDFs relacionados con entregas y materiales. Las funciones manejan filtros dinámicos y validaciones de seguridad.

### Catálogo de Funciones y Clases
- `get_deliveries_for_bulk(conn: sqlite3.Connection, date: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, entrega_query: Optional[str] = None) -> pd.DataFrame` - Construye y ejecuta la query dinámica para filtrar entregas en reportes masivos.
- `get_area_lookup(conn: sqlite3.Connection) -> pd.DataFrame` - Obtiene el área de negocio dominante para cada entrega.
- `get_picking_items(conn: sqlite3.Connection, entrega_ids: List[str]) -> pd.DataFrame` - Obtiene materiales por entrega (desglosado) para el picking list, asegurando cantidades visibles.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - `outbound_deliveries`
  - `warehouse_tasks`
- Columnas:
  - `entrega`, `autor`, `fecha_carga`, `fecha_sm_real`, `creado_el`, `ubicacion_area`, `ubicacion_bin_1`, `ubicacion_bin`, `area_negocio`, `material`, `denominacion`, `cantidad`, `umb`, `pos_`
- Consultas SQL crudas:
  - Consulta dinámica para filtrar entregas.
  - Consulta para obtener el área de negocio dominante.
  - Consulta para obtener materiales por entrega.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: `logging`, `pandas`, `sqlite3`
- Comunicación con otros archivos del proyecto:
  - No se menciona ninguna comunicación explícita con otros archivos.


---

## Archivo: ./core/pdf_reports.py

### Resumen Funcional
El archivo `pdf_reports.py` contiene funciones para construir secciones complejas de PDFs, específicamente para generar anexos y listas de picking. Estas funciones utilizan una biblioteca de PDF (no especificada en el fragmento) para crear documentos con tablas y texto formateado.

### Catálogo de Funciones y Clases
- `_parse_qty(val)` - Sanitiza y convierte a float valores de cantidad de WMS.
- `_fmt_qty(val)` - Formatea cantidades para mostrar en el PDF de forma legible.
- `draw_annex_table(pdf, grouped_data)` - Dibuja la tabla de índice (anexo) de entregas agrupadas.
- `draw_picking_list(pdf, picking_df)` - Dibuja la lista de picking desglosada por entrega pero con total consolidado.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencia directa: `from datetime import datetime`
Uso indirecto de una biblioteca de PDF (no especificada en el fragmento)


---

## Archivo: ./core/query_engine.py

### Resumen Funcional
Este archivo `query_engine.py` es el motor de construcción de consultas SQL seguras para el Analytics Studio. Centraliza la validación de identificadores (tablas y columnas) contra una lista blanca y construye consultas parametrizadas dinámicamente a partir de un `VisualQueryBuilderPayload`.

### Catálogo de Funciones y Clases
- `validate_identifier(name: str, db: Session)` - Valida que un identificador (tabla o tabla.columna) pertenezca a la lista blanca.
- `validate_column(table: str, column: str, db: Session)` - Valida que una columna pertenezca a una tabla permitida.
- `get_table_columns(table: str, db: Session)` - Retorna la lista de columnas de una tabla permitida.
- `get_bound_params_from_visual_state(visual_state_str: str)` - Extrae los bind params (?) de un visual_state JSON serializado.
- `extract_metric_value(df, active_year: str = None)` - Extrae el valor numérico principal de un DataFrame de resultado de query.
- `build_sql_from_payload(payload, db: Session)` - Compila un VisualQueryBuilderPayload validado en una tupla (sql_text, bound_params).

### Interacción con Base de Datos
- Motor de base de datos: SQLAlchemy
- Tablas permitidas:
  - `outbound_deliveries`
  - `stock_levels`
  - `warehouse_tasks`
  - `inventory_movements`
- Consultas SQL dinámicas que utilizan bind params para evitar inyección SQL.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas: `sqlalchemy`, `fastapi`
- Comunicación con otros archivos:
  - `routes/settings.py::api_build_sql` → llama a `build_sql_from_payload()`
  - `core/security.py::validate_table` → valida nombres de tabla en ETL (sin cambios)
  - `core/utils.py` → utilidades JSON y métricas (sin cambios)


---

## Archivo: ./core/schemas.py

### Resumen Funcional
Este archivo define esquemas de datos utilizando Pydantic para representar respuestas de diferentes endpoints en una aplicación. Cada esquema incluye un diccionario de datos y un indicador booleano que indica si la respuesta está sincronizando.

### Catálogo de Funciones y Clases
- `DashboardResponse(data: Dict[str, Any], is_syncing: bool)` - Representa la respuesta para el endpoint del panel de control.
- `AnalyticsDeliveriesResponse(data: Dict[str, Any], is_syncing: bool)` - Representa la respuesta para el endpoint de análisis de entregas.
- `AnalyticsInventoryResponse(data: Dict[str, Any], is_syncing: bool)` - Representa la respuesta para el endpoint de análisis de inventario.
- `AnalyticsTasksResponse(data: Dict[str, Any], is_syncing: bool)` - Representa la respuesta para el endpoint de análisis de tareas.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencia única:
- `pydantic` - Usada para definir los esquemas de datos.


---

## Archivo: ./core/security.py

### Resumen Funcional
Este archivo contiene utilidades centralizadas de seguridad y validación, específicamente para prevenir SQL Injection mediante la validación del nombre de las tablas contra una lista blanca.

### Catálogo de Funciones y Clases
- `validate_table(table_name: str) -> None` - Valida el nombre de la tabla contra la lista blanca para prevenir SQL Injection.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con bases de datos.

### Estado y Variables Globales
- `WHITELIST_TABLES: Final[Set[str]]` - Variable global que almacena una lista blanca de tablas permitidas para evitar SQL Injection.

### Dependencias y Flujo
No depende de ninguna librería externa. No comunica con otros archivos del proyecto.


---

## Archivo: ./core/state.py

### Resumen Funcional
Gestión centralizada del estado mutable y la caché de la aplicación, implementando límites de seguridad para evitar fugas de memoria.

### Catálogo de Funciones y Clases
- `AppState()` - Gestiona el estado mutable y la caché de forma centralizada.
  - `__init__()`
  - `max_cache_size` (getter/setter)
  - `sync_lock` (getter)
  - `is_syncing` (getter/setter)
  - `cache_size` (getter)
  - `get_cache(key: str) -> Optional[Any]`
  - `set_cache(key: str, value: Any)`
  - `clear_cache(key: Optional[str] = None)`

### Interacción con Base de Datos
No aplica.

### Estado y Variables Globales
- `global_state` (variable global): Instancia única de `AppState`.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `fastapi`: Para inyección de dependencias.
  - `logging`: Para registro de eventos.
  - `threading.Lock`: Para sincronización.

- Comunicación con otros archivos del proyecto:
  - `get_app_state()`: Inyección de dependencias para FastAPI.


---

## Archivo: ./core/task_manager.py

### Resumen Funcional
El archivo `task_manager.py` implementa un gestor de tareas en segundo plano utilizando un `ThreadPoolExecutor`. Permite encolar, rastrear y gestionar el estado de las tareas, manteniendo un historial limitado en memoria.

### Catálogo de Funciones y Clases
- **TaskStatus** - Enumeración que define los estados posibles de una tarea (PENDING, RUNNING, DONE, FAILED).
- **TaskRecord** - Clase de datos inmutable que registra la información de una tarea.
  - `task_id`: Identificador único de la tarea.
  - `name`: Nombre descriptivo de la tarea.
  - `status`: Estado actual de la tarea.
  - `created_at`, `started_at`, `finished_at`: Fechas de creación, inicio y finalización de la tarea.
  - `result`, `error`: Resultado o error de la tarea.
- **TaskManager** - Clase que gestiona el encolamiento y ejecución de tareas.
  - `submit_task(name: str, fn: Callable, *args, **kwargs) -> str`: Encola una nueva tarea para ejecución.
  - `get_task_status(task_id: str) -> Optional[Dict[str, Any]]`: Retorna el estado de una tarea por su ID.
  - `list_tasks(limit: int = 20) -> List[Dict[str, Any]]`: Lista las tareas más recientes.
  - `has_running_task(name: str) -> bool`: Verifica si hay una tarea con el nombre dado en estado RUNNING.
  - `_trim_history()`: Elimina las tareas completadas más antiguas si se supera el límite de historial.
  - `shutdown(wait: bool = True)`: Cierra gracefulmente el pool de threads.

### Interacción con Base de Datos
No aplica. El archivo no interactúa con ninguna base de datos.

### Estado y Variables Globales
- **task_manager**: Instancia global de la clase `TaskManager` con 3 workers por defecto.

### Dependencias y Flujo
- **Dependencias**: No utiliza librerías externas adicionales.
- **Flujo**: El archivo se comunica con otros archivos del proyecto a través de su API pública (`submit_task`, `get_task_status`, `list_tasks`).


---

## Archivo: ./core/utils.py

### Resumen Funcional
Este archivo contiene utilidades transversales y gestión de señales del sistema. Incluye funciones para configurar manejadores de señales, registrar un banner de inicio y limpiar datos para su serialización JSON segura.

### Catálogo de Funciones y Clases
- `setup_signal_handlers()` - Configura los manejadores de señales (SIGINT, SIGTERM) para un cierre limpio.
- `log_startup_banner()` - Registra un banner de inicio del módulo de utilidades del sistema.
- `sanitize_for_json(data: Any) -> Any` - Limpia datos para su serialización JSON segura.
- `_get_bound_params_from_visual_state(visual_state_str: str) -> list` - Alias de compatibilidad para obtener parámetros enlazados desde un estado visual.
- `_extract_metric_value(df, active_year: str = None) -> Any` - Alias de compatibilidad para extraer un valor métrico de un DataFrame.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `_handlers_registered` - Flag interno para evitar registros múltiples de manejadores de señales.

### Dependencias y Flujo
- `signal`, `sys`, `logging`, `pandas`, `math`
- Importa funciones desde `services.tunnel` y `core.query_engine`


---

## Archivo: ./core/wms_config.py

### Resumen Funcional
Este archivo contiene la configuración y las funciones de validación para los mapeos utilizados en la lógica de negocio del sistema WMS (SaaS Dinámico). Define funciones para cargar y validar mapeos como STATUS_MAPPING y COST_CENTER_MAPPING, así como soporte para carga dinámica de atributos.

### Catálogo de Funciones y Clases
- `validate_wms_maps()` - Valida la integridad de los mapeos definidos.
- `__getattr__(name: str) -> Any` - Soporta carga dinámica de atributos.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencia directa:
- `get_setting`, `get_status_mapping`, `get_cost_center_mapping`, `get_holidays`, `get_query` - Funciones desde el módulo `db_config_manager`.


---

## Archivo: ./core/wms_utils.py

### Resumen Funcional
Este archivo contiene funciones utilitarias vectorizadas para transformación de datos en un sistema WMS (Warehouse Management System). Incluye operaciones como limpieza de cadenas, mapeos de estados y centros de costo, normalización de fechas y cálculos de retraso.

### Catálogo de Funciones y Clases
- `sanitize_string(text: str) -> str` - Normaliza un string para usarlo como encabezado de columna.
- `map_wms_status(df: pd.DataFrame) -> pd.DataFrame` - Concatena columnas de estado y mapea al valor legible de negocio.
- `apply_cost_center_mapping(df: pd.DataFrame) -> pd.DataFrame` - Clasifica ubicaciones WMS en áreas de negocio de forma vectorizada.
- `normalize_date_columns(df: pd.DataFrame) -> pd.DataFrame` - Estandariza formatos de fecha WMS a dd-mm-yyyy de forma eficiente.
- `calculate_sla_delays(df: pd.DataFrame) -> pd.DataFrame` - Calcula días hábiles de retraso usando lógica vectorizada de NumPy.
- `generate_time_labels(df: pd.DataFrame) -> pd.DataFrame` - Genera etiquetas de semana ISO para visualización y analítica.
- `_manifest_execute(session_or_conn, sql: str, params: dict)` - Ejecuta una query de manifiesto sobre Session SQLAlchemy o sqlite3.Connection.
- `is_file_changed(session_or_conn, file_path: Path) -> bool` - Verifica si un archivo ha cambiado desde la última sincronización.
- `mark_file_processed(session_or_conn, file_path: Path, row_count: Optional[int] = None)` - Marca un archivo como procesado en el manifiesto.

### Interacción con Base de Datos
- Motor: SQLAlchemy (puede interactuar con SQLite o otras bases de datos compatibles).
- Tablas:
  - `sync_manifest` (Tabla utilizada para almacenar información sobre archivos procesados, incluyendo su ruta, tamaño, última modificación y número de filas procesadas).

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas: `re`, `logging`, `numpy`, `pandas`, `datetime`, `pathlib`, `typing`.
- Comunicación con otros archivos:
  - `core.wms_config`: Para mapeos de estados y centros de costo.
  - `core.db_config_manager`: Para obtener información sobre feriados.


---

## Archivo: ./db/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./db/consolidator.py

### Resumen Funcional
El archivo `consolidator.py` es un orquestador de consolidación de datos que opera sobre una base de datos SQLite. Se encarga de procesar archivos WMS, actualizar tablas con los datos más recientes y realizar diversas operaciones de enriquecimiento y sincronización.

### Catálogo de Funciones y Clases
- `DataConsolidator(db_path: str)` - Gestiona la consolidación de archivos WMS en SQLite.
  - `__init__(self, db_path: str)` - Inicializa el objeto con la ruta a la base de datos.
  - `__enter__(self)` - Establece la conexión a la base de datos.
  - `__exit__(self, exc_type, exc_val, exc_tb)` - Cierra la conexión a la base de datos.
  - `connect(self)` - Establece la conexión y configura optimizaciones de SQLite.
  - `_parse_file_date(self, file_path: Path) -> datetime` - Extrae la fecha del nombre del archivo (dd-mm-yyyy).
  - `consolidate_folder(self, folder_path: str, table_name: str = TABLE_DELIVERIES)` - Consolida archivos cronológicamente mediante lógica UPSERT.
  - `overwrite_with_latest(self, folder_path: str, table_name: str = TABLE_STOCK)` - Reemplaza la tabla con los datos del archivo más reciente.
  - `enrich_deliveries_with_stock(self)` - Enriquece las transacciones con información de stock actual.
  - `backfill_from_movements(self)` - Sincroniza datos faltantes desde la tabla Movimientos.
  - `backfill_texts(self)` - Sincroniza descripciones faltantes desde Stock y Movimientos.
  - `update_sla_with_tasks(self)` - Actualiza el SLA cruzando fechas con Tareas.
  - `close(self)` - Cierra la conexión de forma segura.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `outbound_deliveries`
  - `stock_levels`
- Columnas y Operaciones:
  - Lectura y escritura en las tablas mencionadas.
  - Uso de consultas SQL para procesar y actualizar datos.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías Externas: `sqlite3`, `logging`, `re`, `pathlib`, `datetime`, `typing`
- Comunicación con otros archivos:
  - `services.etl.OutboundDeliveryAdapter` y `services.etl.StockLevelAdapter` para procesar y guardar datos.
  - `db_enrichment` para funciones de enriquecimiento y sincronización.
  - `core.security.validate_table` para validar tablas.
  - `core.wms_utils.is_file_changed` y `core.wms_utils.mark_file_processed` para gestionar archivos procesados.


---

## Archivo: ./db/db_enrichment.py

### Resumen Funcional
El archivo `db_enrichment.py` contiene funciones que realizan el enriquecimiento de datos en una base de datos SQLite, utilizando SQL directo y pandas para manipular los datos. Las principales operaciones incluyen rellenar columnas vacías en tablas como `outbound_deliveries`, actualizar mapeos de frecuencia Autor -> Área, aplicar aprendizaje basado en autores a transacciones, enriquecer transacciones con datos de stock y rellenar descripciones de materiales faltantes.

### Catálogo de Funciones y Clases
- `backfill_deliveries_from_movements(conn: sqlite3.Connection, trans_table: str = "outbound_deliveries", movements_table: str = "inventory_movements")` - Rellena columnas vacías en Entregas (autor, ubicacion, textos) cruzando con Movimientos.
- `learn_author_areas(conn: sqlite3.Connection)` - Actualiza el mapeo de frecuencia Autor -> Área.
- `apply_author_learning(conn: sqlite3.Connection, table_name: str = "outbound_deliveries")` - Asigna áreas de negocio a transacciones 'OTRO' basadas en la memoria del autor.
- `enrich_deliveries_with_stock(conn: sqlite3.Connection, trans_table: str = "outbound_deliveries", stock_table: str = "stock_levels")` - Enriquece transacciones con descripciones y ubicaciones físicas de Stock.
- `backfill_material_texts(conn: sqlite3.Connection)` - Rellena descripciones y UMBs faltantes en Entregas usando Stock y Movimientos como fuentes de verdad.
- `update_sla_with_tasks(conn: sqlite3.Connection)` - Actualiza la métrica de SLA en outbound_deliveries cruzando con la fecha de confirmación real en Tareas.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQLite. Las tablas y columnas específicas son:
- Tablas: `outbound_deliveries`, `inventory_movements`, `stock_levels`, `warehouse_tasks`.
- Columnas: `material`, `usuario`, `ce_coste`, `texto_breve_material`, `referencia`, `entrega`, `autor`, `centro_costo`, `denominacion`, `ubicacion_bin`, `umb`, `fecha_conf`, `creado_el`, `estado_wms`.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas: `logging`, `pandas`, `sqlite3`, `numpy`.
- Comunicación con otros archivos del proyecto:
  - `core.security.validate_table`
  - `core.db_config_manager.get_holidays`


---

## Archivo: ./db/predictive_engine.py

### Resumen Funcional
El archivo `predictive_engine.py` procesa datos de movimientos en una base de datos SQLite para generar modelos predictivos utilizando técnicas como el Análisis del Carrocería (Market Basket Analysis), la Relación Frecuencia-Volumen y la Estacionalidad Diaria Semana (DOW Bias). El objetivo es identificar patrones, anomalías y tendencias en los datos de inventario para mejorar la planificación y desplanificación.

### Catálogo de Funciones y Clases
- `generate_predictions(db_path: str)` - Procesa Movimientos Transactions para generar modelos predictivos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `inventory_movements`
- **Columnas:** 
  - `fe_contab`, `ce_coste`, `material`, `texto_breve_material`, `cantidad`, `cmv`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas:**
  - `sqlite3`
  - `pandas`
  - `numpy`
  - `datetime`
  - `logging`
  - `itertools`
  - `collections`
  - `sys`
  - `os`

- **Flujo Interno:** El archivo se comunica con el módulo `core.wms_config` para obtener una consulta específica y realiza operaciones de análisis y procesamiento en los datos leídos desde la base de datos SQLite.


---

## Archivo: ./main.py

### Resumen Funcional
El archivo `main.py` es el punto de entrada oficial para la aplicación MonitorWeb Analytics. Inicializa y configura los servicios necesarios, incluyendo el inicio de un túnel Ngrok para acceso remoto y el lanzamiento del servidor web utilizando Uvicorn.

### Catálogo de Funciones y Clases
- `start_application()` - Configura e inicia los servicios de la plataforma.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: `uvicorn`, `logging`
- **Flujo Interno**: El archivo se comunica con el módulo `app` para iniciar la aplicación web, con el módulo `config` para obtener configuraciones como host, puerto y modo de recarga, y con el módulo `services.tunnel` para gestionar el túnel Ngrok.


---

## Archivo: ./repositories/__init__.py

### Resumen Funcional
Este archivo es el punto de entrada para la configuración y la inyección de dependencias de los repositorios en una aplicación FastAPI que utiliza SQLite como base de datos.

### Catálogo de Funciones y Clases
- `get_db()` - Establece una conexión a la base de datos SQLite y la devuelve. La conexión se cierra automáticamente al finalizar el contexto.
- `get_deliveries_repo(conn: sqlite3.Connection = Depends(get_db))` - Crea e inicializa un repositorio para operaciones relacionadas con entregas.
- `get_inventory_repo(conn: sqlite3.Connection = Depends(get_db))` - Crea e inicializa un repositorio para operaciones relacionadas con el inventario.
- `get_tasks_repo(conn: sqlite3.Connection = Depends(get_db))` - Crea e inicializa un repositorio para operaciones relacionadas con tareas.

### Interacción con Base de Datos
- Motor de base de datos: SQLite
- Tablas y Columnas: No aplica (se asume que las tablas y columnas están definidas en los repositorios `DeliveriesRepository`, `InventoryRepository` y `TasksRepository`)
- Consultas SQL Crudas o ORM: Se utiliza el módulo `sqlite3` para interactuar con la base de datos.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `fastapi`: Para manejar las dependencias en FastAPI.
- Comunicación con otros archivos del proyecto:
  - Importa clases y funciones desde los módulos `base.py`, `deliveries.py`, `inventory.py` y `tasks.py`.


---

## Archivo: ./repositories/base.py

### Resumen Funcional
La clase `BaseRepository` proporciona una estructura base para interactuar con bases de datos mediante SQLAlchemy. Define métodos para obtener consultas SQL y verificar el estado visual de las mismas.

### Catálogo de Funciones y Clases
- `__init__(self, session: Session)` - Inicializa la instancia con una sesión de SQLAlchemy.
- `_sql(self, query_id: str, fallback: str) -> str` - Obtiene un SQL desde la base de datos de configuración o devuelve un fallback hardcodeado si no existe.
- `_has_visual_state(self, query_id: str) -> bool` - Verifica si una consulta tiene un estado visual JSON almacenado.

### Interacción con Base de Datos
- Motor: SQLAlchemy
- Tablas: `config_queries`
- Columnas: `query_id`, `sql_text`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sqlalchemy.orm.Session`
  - `core.wms_config.get_query`
  - `core.db_config_manager.get_query_visual_state`
- Comunicación con otros archivos del proyecto:
  - `core/query_engine.build_sql_from_payload()` (mencionado en la documentación, pero no implementado)


---

## Archivo: ./repositories/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene una clase `DeliveriesRepository` que proporciona métodos para obtener estadísticas y datos relacionados con las entregas (`outbound_deliveries`). Estos métodos realizan consultas SQL en una base de datos utilizando SQLAlchemy y pandas para procesar los resultados.

### Catálogo de Funciones y Clases
- `DeliveriesRepository(BaseRepository)` - Repositorio para el dominio de Entregas (outbound_deliveries).
  - `_sql(query_id: str, fallback: str) -> str` - Obtiene SQL desde config_queries con fallback explícito.
  - `_get_sla_threshold() -> int` - Retorna el umbral SLA configurado en las variables de entorno.
  - `get_area_stats(year: str) -> pd.DataFrame` - Obtiene estadísticas por área para un año dado.
  - `get_total_active_days(year: str) -> int` - Cuenta los días activos de entrega para un año dado.
  - `get_sla_stats(year: str) -> pd.DataFrame` - Obtiene estadísticas de SLA para un año dado.
  - `get_top_authors(year: str) -> pd.DataFrame` - Obtiene los autores con más entregas en un año dado.
  - `get_dates_counts(year: str) -> pd.DataFrame` - Obtiene el conteo de entregas por fecha y área para un año dado.
  - `get_top_locations(year: str) -> pd.DataFrame` - Obtiene las ubicaciones con más entregas en un año dado.
  - `get_top_materials_by_area(year: str) -> pd.DataFrame` - Obtiene los materiales con mayor frecuencia por área para un año dado.
  - `get_area_material_mapping(year: str) -> pd.DataFrame` - Mapea el material por área y cantidad para un año dado.
  - `get_user_material_mapping(year: str) -> pd.DataFrame` - Mapea el material por usuario y cantidad para un año dado.
  - `get_sla_audit_records(year: str, late: bool = True, limit: int = 500) -> pd.DataFrame` - Obtiene registros de auditoría de SLA para un año dado.
  - `get_monthly_evolution() -> pd.DataFrame` - Obtiene la evolución mensual de entregas y días activos.
  - `get_weekly_evolution() -> pd.DataFrame` - Obtiene la evolución semanal de entregas.
  - `get_wms_status_distribution(year: str) -> pd.DataFrame` - Distribución del estado WMS para un año dado.
  - `get_lead_time_by_area(year: str) -> pd.DataFrame` - Tiempo promedio de entrega por área para un año dado.
  - `get_sla_trend() -> pd.DataFrame` - Tendencia de SLA semanal.
  - `get_author_sla_correlation() -> pd.DataFrame` - Correlación entre el autor y el SLA.
  - `get_volume_delay_trend() -> pd.DataFrame` - Tendencia del volumen y retraso por semana.
  - `get_sla_trend_by_area() -> pd.DataFrame` - Tendencia de SLA semanal por área.
  - `get_sla_monthly_trend() -> pd.DataFrame` - Tendencia mensual de SLA.
  - `get_sla_monthly_trend_by_area() -> pd.DataFrame` - Tendencia mensual de SLA por área.

### Interacción con Base de Datos
- Motor: SQLAlchemy (no especificado el motor exacto).
- Tablas:
  - `outbound_deliveries`
  - `warehouse_tasks`
- Columnas:
  - `entrega`, `fecha_carga`, `dias_retraso`, `autor`, `material`, `denominacion`, `estado_wms`, `creado_el`, `fecha_sm_real`, `ubicacion_bin`, `business_area`, `week_sort`, `week_label`
- Consultas SQL crudas:
  - Todas las consultas SQL utilizan parámetros de enlace (`?`) para evitar inyecciones SQL.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas: pandas, sqlalchemy.
- Comunicación con otros archivos del proyecto:
  - `core.db_config_manager` (para obtener configuraciones de variables de entorno).


---

## Archivo: ./repositories/inventory.py

### Resumen Funcional
El archivo `inventory.py` contiene una clase `InventoryRepository` que se encarga de interactuar con la base de datos para obtener estadísticas y datos relacionados con el inventario, utilizando SQL queries y pandas DataFrames.

### Catálogo de Funciones y Clases
- **Clase:** `InventoryRepository`
  - **Métodos:**
    - `get_cmv_prod()`: Devuelve el valor configurado para CMV_PROD.
    - `get_cmv_mant()`: Devuelve el valor configurado para CMV_MANT.
    - `get_cmv_consumos()`: Devuelve una tupla con los valores de CMV_PROD y CMV_MANT.
    - `get_cmv_reversas()`: Devuelve una tupla con los valores configurados para CMV_REVERSAS.
    - `check_table_exists()`: Verifica si la tabla 'inventory_movements' existe en la base de datos.
    - `get_volumen_stats()`: Obtiene estadísticas de volumen del inventario.
    - `get_area_stats_prod()`: Obtiene estadísticas por área para el producto.
    - `get_material_consumos_abc()`: Obtiene estadísticas de materiales consumidos en ABC.
    - `get_top_users(start_year='2026')`: Obtiene los usuarios con más movimientos.
    - `get_trend_stats(start_year='2025')`: Obtiene tendencias de movimientos por período.
    - `get_dow_stats()`: Obtiene estadísticas diarias de movimiento.
    - `get_pm_type_material_records()`: Obtiene registros de tipo PM y material.
    - `get_area_material_mapping_201()`: Obtiene mapeo de área para el producto 201.
    - `get_user_material_mapping(users: Tuple[str, ...])`: Obtiene mapeo de usuario y material.
    - `get_location_material_summary()`: Obtiene resumen de materiales por ubicación.
    - `get_total_active_days()`: Obtiene el número total de días activos en los movimientos.

### Interacción con Base de Datos
- **Motor:** SQLite (inferred from the use of `sqlite_master`).
- **Tablas:** `inventory_movements`.
- **Columnas:**
  - `tipo_operacion`
  - `material`
  - `num_tx`
  - `business_area`
  - `ce_coste`
  - `cmv`
  - `fe_contab`
  - `alm`
  - `usuario`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- **Librerías Externas:** pandas, sqlalchemy.
- **Flujo Interno:** Utiliza métodos de la clase base `BaseRepository` para interactuar con la base de datos.


---

## Archivo: ./repositories/tasks.py

### Resumen Funcional
Este archivo contiene un repositorio de datos para el dominio de tareas de almacén, que proporciona métodos para obtener resúmenes y tendencias de las tareas, así como detalles específicos sobre las tareas.

### Catálogo de Funciones y Clases
- `get_tasks_summary()` - Obtiene un resumen de las tareas agrupadas por código y nombre.
- `get_tasks_trend()` - Obtiene una tendencia diaria de creación y confirmación de tareas.
- `get_tasks_by_user()` - Obtiene el número de tareas creadas y confirmadas por usuario.
- `get_tasks_by_type_dest()` - Obtiene un resumen de las tareas agrupadas por tipo de destino.
- `get_recent_tasks()` - Obtiene las tareas recientes que no han sido confirmadas.
- `get_non_palletized_movements()` - Obtiene los movimientos no paletizados más recientes.
- `get_non_palletized_count()` - Cuenta el número de movimientos no paletizados.
- `get_non_palletized_summary()` - Obtiene un resumen de los movimientos no paletizados, incluyendo detalles sobre la fecha más antigua y más reciente.

### Interacción con Base de Datos
- Motor: PostgreSQL (deducido del uso de SQLAlchemy).
- Tablas:
  - `warehouse_tasks`
  - `lx02_pendientes`
  - `inventory_movements`
- Columnas:
  - `cl_mov`, `clase_mov`, `COUNT(*)`, `SUM(ctd_teor_dsd)`, `fe_creac`, `fecha_conf`, `usuario`, `material`, `texto_breve_material`, `ubic_proc`, `ubic_dest`, `hora`, `otcuanto`, `pos`, `denominacion`, `stock_disp`, `alm`, `ce`, `doc_mat`, `cmv`, `usuario_conf`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas: `pandas`, `sqlalchemy`.
- No se comunica con otros archivos del proyecto.


---

## Archivo: ./routes/__init__.py

### Resumen Funcional
Este archivo es el punto de entrada para las rutas del proyecto, importando y registrando diferentes módulos que contienen endpoints para diversas funcionalidades como el panel de control, entregas, inventario, análisis proyecciones, filtros, PDFs, sincronización y configuraciones.

### Catálogo de Funciones y Clases
No se detectan funciones ni clases directamente en este archivo. Solo hay importaciones de módulos.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencia: No se especifican librerías externas específicas en este fragmento, pero los módulos importados pueden tener dependencias adicionales que no se muestran aquí. Comunicación con otros archivos del proyecto: Este archivo comunica con varios archivos dentro de la carpeta `routes`, cada uno probablemente contenga endpoints para diferentes funcionalidades del sistema.


---

## Archivo: ./routes/analytics_proyecciones.py

### Resumen Funcional
Este archivo define rutas para obtener analíticas de proyecciones utilizando FastAPI. Incluye una función que genera predicciones y las almacena en caché, así como una ruta GET que devuelve estos datos.

### Catálogo de Funciones y Clases
- `get_proyecciones_context()` - Obtiene el contexto de proyecciones, priorizando la caché.
- `get_analytics_proyecciones(request: Request, force_refresh: bool = False, state: AppState = Depends(get_app_state))` - Retorna los datos de proyecciones en formato JSON.

### Interacción con Base de Datos
- Motor: No aplica (No hay interacción directa con bases de datos).
- Tablas y Columnas: No aplica (No hay consultas SQL crudas o llamadas a ORM).

### Estado y Variables Globales
- `AppState` - Almacena el estado del sistema, incluyendo la caché.
- `_DB` - Ruta de la base de datos definida en `config`.

### Dependencias y Flujo
- Librerías externas: FastAPI, SQLAlchemy (a través de `db.predictive_engine`).
- Comunicación con otros archivos:
  - `core.auth.get_current_user` - Para autenticación.
  - `core.state.get_app_state` - Para obtener el estado del sistema.
  - `db.predictive_engine.generate_predictions(_DB)` - Para generar predicciones.


---

## Archivo: ./routes/auth.py

### Resumen Funcional
Este archivo contiene endpoints para autenticación y gestión de usuarios, incluyendo login, registro, cambio de contraseña, obtención de información del usuario autenticado y listado de usuarios (solo accesible por administradores). También proporciona una vista HTML para el formulario de login.

### Catálogo de Funciones y Clases
- `login(response: Response, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session_dep))` - Autentica un usuario con username/password y retorna un JWT.
- `logout(response: Response, state: AppState = Depends(get_app_state))` - Limpia la cookie de autenticación.
- `get_me(user: User = Depends(require_auth), state: AppState = Depends(get_app_state))` - Retorna la información del usuario autenticado.
- `change_password(data: ChangePasswordRequest, db: DBSession, user: User = Depends(require_auth))` - Cambia la contraseña del usuario autenticado.
- `register_user(data: UserCreate, db: DBSession, admin: User = Depends(require_admin), state: AppState = Depends(get_app_state))` - Crea un nuevo usuario. Solo accesible por administradores.
- `list_users(db: DBSession, admin: User = Depends(require_admin), state: AppState = Depends(get_app_state))` - Lista todos los usuarios del sistema.
- `login_page(request: Request, state: AppState = Depends(get_app_state))` - Renderiza la página de login.

### Interacción con Base de Datos
- Motor: SQLAlchemy ORM
- Tablas:
  - `User`
- Columnas:
  - `id`, `username`, `password_hash`, `role`, `is_active`, `created_at`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: FastAPI, SQLAlchemy ORM.
- Comunicación con otros archivos del proyecto:
  - `core.database.get_session_dep` para obtener la sesión de base de datos.
  - `core.models_auth.User` para definir el modelo de usuario.
  - `core.auth` para funciones de autenticación y gestión de usuarios.
  - `core.app_instance.templates` para renderizar vistas HTML.


---

## Archivo: ./routes/config.py

### Resumen Funcional
El archivo `config.py` es un módulo que se encarga de registrar todos los routers de una aplicación FastAPI. Incluye manejo básico de errores para evitar que un router mal configurado detenga el arranque completo del servidor.

### Catálogo de Funciones y Clases
- `register_routes(app: FastAPI) -> None` - Registra todos los routers de la aplicación de forma centralizada, incluyendo manejo de errores básico.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- `fastapi`: Se utiliza para crear y gestionar la aplicación FastAPI.
- `logging`: Se utiliza para registrar mensajes de depuración y error.
- Importa varios módulos de ruta (`dashboard`, `deliveries`, `inventory`, etc.) desde el mismo directorio.

El archivo no depende de ninguna base de datos ni variables globales.


---

## Archivo: ./routes/dashboard.py

### Resumen Funcional
El archivo `dashboard.py` define rutas para un panel de control (dashboard) que incluye endpoints para obtener ubicaciones de materiales y cargar la vista principal del dashboard con KPIs y búsqueda rápida. También proporciona una API JSON para el mismo propósito.

### Catálogo de Funciones y Clases
- `get_ubicaciones(material: str, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Obtiene las ubicaciones de un material específico.
- `dashboard(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Vista principal del dashboard con KPIs y búsqueda rápida.
- `dashboard_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - API JSON para el dashboard con KPIs y búsqueda rápida.

### Interacción con Base de Datos
- Motor de base de datos: SQLite
- Tablas:
  - `stock_levels`
  - `warehouse_tasks`
- Columnas:
  - `ubicacion_bin`, `ubicacin`, `ubicacion` (dependiendo del origen de la importación)
  - `denominacion`, `texto_breve_de_material`
  - `fecha_conf`, `fe_creac`, `material`, `tp_dest`, `ubic_dest`, `stock_disp`, `umb`, `ubic_actual`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `logging`
  - `sqlite3`
  - `itertools`
  - `pandas`
  - `datetime`
  - `timedelta`
  - `typing`
  - `fastapi`
  - `sqlalchemy`
  - `core.database`
  - `core.state`
  - `core.auth`
  - `core.app_instance`
  - `services.dashboard_service`
  - `core.wms_config`
  - `core.schemas`

- Flujo de comunicación:
  - El archivo interactúa con el servicio `DashboardService` para obtener el contexto de negocio.
  - Utiliza la sesión de base de datos (`Session`) proporcionada por `get_session_dep`.
  - Recupera y establece en caché los contextos del dashboard utilizando `AppState`.


---

## Archivo: ./routes/deliveries.py

### Resumen Funcional
Este archivo contiene rutas para el análisis de entregas optimizadas y seguras. Incluye endpoints para renderizar páginas web y proporcionar datos en formato JSON.

### Catálogo de Funciones y Clases
- `save_analytics_snapshot(session: Session, key: str, data: Dict[str, Any])` - Guarda una captura de las analíticas en la base de datos.
- `load_analytics_snapshot(session: Session, key: str) -> Optional[Dict[str, Any]]` - Recupera la última captura de analíticas desde la base de datos.
- `analytics(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Renderiza la página principal de analíticas con caché multinivel.
- `sla_details(request: Request, type: str = "late", session: Session = Depends(get_session_dep))` - Vista detallada de auditoría SLA.
- `get_non_palletized_details(user: str, clase_mov: str, db: Session = Depends(get_session_dep), current_user: Dict[str, Any] = Depends(get_current_user))` - Obtiene el listado detallado de movimientos no paletizados para un usuario y tipo de movimiento específicos.
- `analytics_deliveries_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - API JSON para analíticas de Entregas (Outbound Deliveries).

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `analytics_snapshots`
- Columnas:
  - `key`, `data`, `updated_at`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `logging`
  - `sqlite3`
  - `pandas`
  - `json`
  - `datetime`
  - `typing`
  - `sqlalchemy`
  - `fastapi`
  - `core.database`
  - `sqlalchemy.orm`
  - `core.state`
  - `core.app_instance`
  - `core.schemas`
  - `repositories`
  - `routes.inventory`
  - `routes.tasks`
  - `routes.analytics_proyecciones`
  - `core.auth`
  - `core.utils`
  - `services.deliveries_service`

- Flujo hacia otros archivos del proyecto:
  - `core.database.get_session_dep`
  - `core.state.get_app_state`
  - `templates.TemplateResponse`
  - `DeliveriesRepository`
  - `get_inventory_context`
  - `get_tasks_context`
  - `get_proyecciones_context`
  - `get_current_user`
  - `sanitize_for_json`
  - `DeliveriesService`


---

## Archivo: ./routes/docs.py

### Resumen Funcional
El archivo `docs.py` define dos endpoints para una API de documentación. El endpoint `/api/docs/tree` genera un árbol de archivos del proyecto indicando cuáles tienen documentación, mientras que el endpoint `/api/docs/content/{path:path}` obtiene el contenido de la documentación (.md) para un archivo específico.

### Catálogo de Funciones y Clases
- `get_docs_tree(state: AppState = Depends(get_app_state))` - Genera un árbol de archivos del proyecto indicando cuáles tienen documentación.
- `get_doc_content(path: str, state: AppState = Depends(get_app_state))` - Obtiene el contenido de la documentación (.md) para un archivo específico.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- `fastapi`: Para crear endpoints.
- `config`: Para acceder a variables de configuración como `BASE_DIR` y `CACHE_DIR`.
- `core.state`: Para acceder al estado global del sistema mediante la dependencia `get_app_state`.

El archivo interactúa con el sistema de archivos para leer directorios y archivos, y utiliza expresiones regulares para procesar contenido de archivos Markdown.


---

## Archivo: ./routes/filters.py

### Resumen Funcional
El archivo `filters.py` contiene funciones para filtrar y calcular KPIs basados en múltiples criterios. Ofrece endpoints para obtener datos filtrados de entregas y calcular indicadores clave de rendimiento (KPIs) dinámicos.

### Catálogo de Funciones y Clases
- `_build_unified_where(date: str, area: str, centro: str, has_ots_filter: str, min_week: str)` - Construye la cláusula WHERE a nivel de MATERIAL con seguridad contra SQL Injection.
- `filter_transactions(request: Request, date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Filtra entregas basándose en múltiples criterios y devuelve los resultados como un DataFrame.
- `get_kpis(date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Calcula KPIs dinámicos filtrados por área para el dashboard.

### Interacción con Base de Datos
- Motor de BD: No especificado.
- Tablas:
  - `outbound_deliveries`
  - `config_cost_center_mapping`
- Columnas:
  - `outbound_deliveries`: `entrega`, `fecha_carga`, `fecha_sm_real`, `creado_el`, `estado_wms`, `material`, `dias_retraso`.
  - `config_cost_center_mapping`: `center_code`, `business_area`.

### Estado y Variables Globales
- No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `logging`
  - `sqlalchemy`
  - `pandas`
  - `fastapi`
- Comunicación con otros archivos del proyecto:
  - Depende de `core.database.get_session_dep` para obtener una sesión de base de datos.


---

## Archivo: ./routes/inventory.py

### Resumen Funcional
Este archivo contiene rutas y lógica para el análisis de inventario. Define endpoints para redirigir a una página de análisis y proporcionar datos de inventario en formato JSON.

### Catálogo de Funciones y Clases
- `analytics_inventory_redirect(request: Request, state: AppState = Depends(get_app_state))` - Redirige a la página de análisis con el tab de inventario activo.
- `get_inventory_context(session: Session) -> Dict[str, Any]` - Obtiene el contexto completo del inventario.
- `analytics_inventory_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Endpoint para obtener datos de inventario en formato JSON.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `AppState` - Almacena el estado de la aplicación, incluyendo caché y sincronización.
- `InventoryService` - Servicio que maneja las operaciones del inventario.

### Dependencias y Flujo
- **Librerías Externas**: `logging`, `sqlalchemy`, `pandas`, `datetime`, `fastapi`, `core.auth`, `core.database`, `core.schemas`, `core.state`, `core.wms_config`, `repositories`, `routes.analytics_proyecciones`, `core.utils`, `services.inventory_service`.
- **Flujo Interno**: El archivo interactúa con el servicio de inventario para obtener y procesar datos, luego los devuelve en formato JSON. Utiliza un estado de aplicación para almacenar y recuperar datos en caché.


---

## Archivo: ./routes/pdf.py

### Resumen Funcional
Este archivo contiene rutas para generar reportes PDF en un sistema WMS (Warehouse Management System), incluyendo una versión individual y una versión masiva de entregas.

### Catálogo de Funciones y Clases
- `generate_pdf(entrega: str, include_logo: bool = False, action: str = "previsualizar", session: Session = Depends(get_session_dep))` - Genera un PDF para una única entrega.
- `generate_pdf_bulk(date: Optional[str] = None, entrega_query: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, include_logo: bool = False, action: str = "previsualizar", session: Session = Depends(get_session_dep))` - Genera un reporte masivo con índice y picking list.

### Interacción con Base de Datos
- Motor: SQLite (deducido del uso de `get_session_dep()` que probablemente se conecta a una base de datos SQLite).
- Tablas:
  - `outbound_deliveries`
  - `area_lookup`
- Columnas:
  - `entrega` en `outbound_deliveries`
  - `entrega`, `area_negocio`, `autor` en `area_lookup`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas: `pandas`, `fastapi`, `sqlalchemy`.
- Comunicación con otros archivos del proyecto:
  - `core.database.get_session_dep`
  - `core.pdf_engine.WMS_Landscape_PDF`
  - `core.pdf_queries.get_deliveries_for_bulk`, `get_area_lookup`, `get_picking_items`
  - `core.pdf_reports.draw_annex_table`, `draw_picking_list`


---

## Archivo: ./routes/settings.py

### Resumen Funcional
El archivo `settings.py` define una API para la gestión dinámica de configuraciones SaaS utilizando SQLAlchemy ORM. Permite crear, actualizar y eliminar configuraciones como estados, centros de costo y feriados, así como consultar y ejecutar consultas SQL.

### Catálogo de Funciones y Clases
- `invalidate_caches(db: Session)` - Limpia el caché global en memoria y elimina todos los snapshots de base de datos.
- `SettingUpdate(key: str, value: str)` - Modelo Pydantic para actualizar una configuración.
- `StatusMappingUpdate(code: str, label: str)` - Modelo Pydantic para actualizar un estado.
- `CostCenterMappingUpdate(center_code: str, business_area: str)` - Modelo Pydantic para actualizar un centro de costo.
- `HolidayAdd(date_str: str)` - Modelo Pydantic para agregar un feriado.
- `QueryUpdate(query_id: str, sql_text: Optional[str], params: Optional[List[Any]], visual_state: Optional[str])` - Modelo Pydantic para actualizar una consulta.
- `JoinDef(table: str, onLeft: str, onRight: str)` - Modelo Pydantic para definir una unión de tablas.
- `FilterDef(column: str, operator: str, value: Optional[str], valueType: Optional[str], compareColumn: Optional[str], offsetValue: Optional[str])` - Modelo Pydantic para definir un filtro.
- `MetricDef(column: str, aggregation: str, format: Optional[str])` - Modelo Pydantic para definir una métrica.
- `TimeAxisDef(column: str, granularity: str)` - Modelo Pydantic para definir el eje de tiempo.
- `SecondMetricDef(column: str = "", aggregation: str = "", label: str = "")` - Modelo Pydantic para definir una segunda métrica.
- `VisualQueryBuilderPayload(baseTable: str, joins: list[JoinDef], filters: list[FilterDef], metric: MetricDef, timeAxis: TimeAxisDef, breakdown: str | None, secondMetric: Optional[SecondMetricDef])` - Modelo Pydantic para definir el payload del constructor de consultas visuales.
- `settings_view(request: Request, db: DBSession, state: AppState = Depends(get_app_state))` - Vista que renderiza el panel de control de configuraciones SaaS.
- `api_get_settings(state: AppState = Depends(get_app_state))` - API para obtener las configuraciones generales.
- `api_update_setting(update: SettingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - API para actualizar una configuración.
- `api_upsert_status(update: StatusMappingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - API para insertar o actualizar un estado.
- `api_delete_status(code: str, db: DBSession, state: AppState = Depends(get_app_state))` - API para eliminar un estado.
- `api_upsert_cost_center(update: CostCenterMappingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - API para insertar o actualizar un centro de costo.
- `api_delete_cost_center(code: str, db: DBSession, state: AppState = Depends(get_app_state))` - API para eliminar un centro de costo.
- `api_add_holiday(h: HolidayAdd, db: DBSession, state: AppState = Depends(get_app_state))` - API para agregar un feriado.
- `api_sync_holidays(db: DBSession, state: AppState = Depends(get_app_state))` - API para sincronizar automáticamente los feriados nacionales (Chile).
- `api_delete_holiday(date_str: str, db: DBSession, state: AppState = Depends(get_app_state))` - API para eliminar un feriado.
- `api_get_query(query_id: str, db: DBSession, state: AppState = Depends(get_app_state))` - API para obtener el estado visual de una consulta del Analytics Studio.
- `api_update_query(update: QueryUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - API para actualizar el estado visual de una consulta.
- `api_get_schema(db: DBSession, state: AppState = Depends(get_app_state))` - API para obtener el listado de tablas y sus columnas para el editor.
- `api_query_preview(update: QueryUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - API para ejecutar una consulta temporal y retornar datos para previsualización.
- `api_build_sql(payload: VisualQueryBuilderPayload, db: DBSession, state: AppState = Depends(get_app_state))` - API para compilar el estado visual del constructor en SQL parametrizado seguro.

### Interacción con Base de Datos
El archivo interactúa con la base de datos utilizando SQLAlchemy ORM. Las tablas y columnas afectadas incluyen:
- `AppSetting`
- `StatusMapping`
- `CostCenterMapping`
- `Holiday`
- `ConfigQuery`

No hay consultas SQL crudas explícitas.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
Dependencias externas utilizadas:
- `fastapi`
- `pydantic`
- `sqlalchemy`
- `pandas`
- `holidays`

El archivo se comunica con otros archivos del proyecto a través de dependencias como `get_session_dep`, `require_admin`, `load_config_to_memory`, `get_setting`, `get_status_mapping`, `get_cost_center_mapping`, `get_holidays`, y `sanitize_for_json`.


---

## Archivo: ./routes/sync.py

### Resumen Funcional
El archivo `sync.py` contiene rutas para la gestión de sincronización de datos en una aplicación web. Permite iniciar y monitorear procesos de sincronización asíncrona utilizando un `TaskManager`, y proporciona endpoints para obtener la URL del túnel, el estado de la sincronización actual y detalles sobre las tareas en ejecución.

### Catálogo de Funciones y Clases
- `get_tunnel_url(state: AppState = Depends(get_app_state))` - Retorna la URL pública del túnel (Ngrok).
- `get_sync_status(state: AppState = Depends(get_app_state))` - Retorna el estado actual de la sincronización.
- `sync_data(state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Inicia el proceso de sincronización de datos y lo encola en el `TaskManager`.
- `list_tasks(limit: int = 20, state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Lista las tareas recientes del sistema.
- `get_task(task_id: str, state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Consulta el estado de una tarea específica por su ID.
- `_run_sync_pipeline()` - Ejecuta el pipeline completo de limpieza y consolidación.

### Interacción con Base de Datos
El archivo interactúa con la base de datos a través del módulo `db.consolidator.DataConsolidator`. Se realizan operaciones en las tablas `stock_levels` y otras dependiendo de los archivos procesados. No se especifica el motor de base de datos.

### Estado y Variables Globales
- `state.is_syncing`: Indica si la sincronización está en curso.
- `state.sync_lock`: Un bloqueo para evitar ejecuciones duplicadas de la sincronización.

### Dependencias y Flujo
- **Librerías Externas**: `fastapi`, `logging`, `shutil`, `pathlib`, `typing`.
- **Flujo Interno**: El archivo se comunica con otros módulos como `core.auth`, `config`, `core.state`, `core.task_manager`, `db.consolidator`, `core.database`, `core.wms_utils`, y `services.etl`.


---

## Archivo: ./routes/tasks.py

### Resumen Funcional
El archivo `tasks.py` define una ruta para obtener analíticas de tareas utilizando FastAPI. La función principal recupera el contexto completo de las tareas y lo devuelve en formato JSON.

### Catálogo de Funciones y Clases
- `get_tasks_context(session: Session) -> dict` - Obtiene el contexto completo de las tareas.
- `analytics_tasks_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Endpoint FastAPI para obtener analíticas de tareas.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción directa con una base de datos.

### Estado y Variables Globales
- `state.get_cache("/api/v1/analytics/tasks")` - Recupera el contexto de las tareas desde la caché.
- `state.set_cache("/api/v1/analytics/tasks", clean_context.copy())` - Almacena el contexto de las tareas en la caché.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `logging`: Para registro de errores.
  - `sqlalchemy.orm.Session`: Para manejar sesiones de base de datos.
  - `pandas`: No se usa directamente, pero podría estar presente en el código omitido.
  - `datetime`: Para manipulación de fechas y horas.
  - `fastapi`: Para definir endpoints y dependencias.
- **Dependencias Internas**:
  - `core.state.AppState` y `get_app_state()`: Para manejar el estado global de la aplicación.
  - `core.utils.sanitize_for_json`: Para sanitizar datos antes de devolverlos en JSON.
  - `repositories.TasksRepository`: No se usa directamente, pero podría estar presente en el código omitido.
  - `services.tasks_service.TasksService`: Servicio que proporciona métodos para obtener contexto de tareas.
- **Flujo**: 
  - La función `analytics_tasks_api` depende de `get_current_user`, `get_session_dep`, y `get_app_state`.
  - Intenta recuperar el contexto de las tareas desde la caché. Si no está disponible, lo recupera del servicio `TasksService`, limpia los datos innecesarios, y lo almacena en la caché antes de devolverlo.

Este archivo es una parte integral del backend que proporciona un endpoint para obtener analíticas de tareas, utilizando servicios y dependencias definidos en otros módulos del proyecto.


---

## Archivo: ./scripts/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./scripts/main_processor.py

### Resumen Funcional
El archivo `main_processor.py` es el punto de entrada para un proceso automatizado que realiza análisis y consolidación de datos en un sistema de gestión de almacenes (WMS). El script ejecuta una serie de fases, incluyendo la validación de directorios, la ejecución de scripts secundarios, la actualización de una base de datos y el procesamiento de movimientos.

### Catálogo de Funciones y Clases
- `run_pipeline()` - Ejecuta el proceso completo de análisis y consolidación de WMS.
  - **Propósito**: Orquesta todas las fases del proceso, desde la validación de directorios hasta el procesamiento final.

### Interacción con Base de Datos
- **Motor**: SQLite (deducido a partir del nombre del archivo de base de datos `.db`).
- **Tablas y Columnas**:
  - Tabla: `stock_levels`
    - Columnas: No especificadas explícitamente en el código, pero se refiere a la tabla donde se actualizan los niveles de stock.
- **Consultas SQL Crudas o Llamadas a ORM**: 
  - Se utiliza un objeto `DataConsolidator` para interactuar con la base de datos y actualizar la tabla `stock_levels`.
  - Se llama a una función `enrich_deliveries_with_stock` que probablemente realiza consultas SQL internamente.

### Estado y Variables Globales
- **Variables Globales**:
  - `PROJECT_ROOT`: Ruta al directorio raíz del proyecto.
  - `DELIVERIES_DIR`, `STOCK_DIR`, `INVENTORY_DIR`, `CLEANSED_DIR`, `DATABASE_PATH`, `ONEDRIVE_PATH`: Rutas a diferentes directorios y archivos, incluyendo la base de datos.

### Dependencias y Flujo
- **Librerías Externas**:
  - `subprocess` para ejecutar comandos externos.
  - `pathlib` para manejar rutas de archivos.
  - `logging` para registro de eventos.
- **Flujo Interno**:
  - El script importa configuraciones globales desde un archivo `config.py`.
  - Configura el registro de eventos con nivel de logging a INFO.
  - Ejecuta una serie de fases, cada una realizando tareas específicas como la validación de directorios, ejecución de scripts secundarios y actualización de la base de datos.


---

## Archivo: ./services/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./services/dashboard_service.py

### Resumen Funcional
Este archivo contiene el servicio `DashboardService` que se encarga de cargar la página principal del dashboard. Orquesta la carga de todos los datos necesarios para el dashboard, incluyendo gráficos, indicadores clave de rendimiento (KPIs) y listas únicas de fechas y áreas.

### Catálogo de Funciones y Clases
- `DashboardService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `get_full_context()` - Orquesta la carga de todos los datos necesarios para el dashboard.
- `_prepare_weekly_chart(year: int)` - Prepara los datos para el gráfico de intensidad semanal.
- `_calculate_dashboard_kpis(start_week: str, year_str: str)` - Calcula los indicadores clave de rendimiento (KPIs) desde una semana base.
- `_prepare_selectors(min_week: str)` - Obtiene listas únicas de fechas y áreas, además de mapeos de autores y centros.
- `_get_recent_transactions(week_str: str)` - Obtiene el listado de las últimas entregas para la tabla principal.

### Interacción con Base de Datos
- Motor: SQLite (inferred from `pd.read_sql`)
- Tablas:
  - `outbound_deliveries`
  - `config_cost_center_mapping`
  - `autor_area_mapping`
- Columnas:
  - `outbound_deliveries`: `week_sort`, `week_label`, `area_negocio`, `entrega`, `material`, `estado_wms`, `dias_retraso`, `fecha_carga`, `fecha_sm_real`, `creado_el`
  - `config_cost_center_mapping`: `center_code`, `business_area`
  - `autor_area_mapping`: `autor`, `area_negocio`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `logging`
  - `sqlalchemy.orm.Session`
  - `pandas as pd`
  - `itertools`
  - `typing`
  - `datetime`
- No comunica con otros archivos del proyecto directamente.


---

## Archivo: ./services/deliveries_service.py

### Resumen Funcional
El archivo `deliveries_service.py` contiene una clase `DeliveriesService` que se encarga de generar un contexto completo para las entregas, incluyendo estadísticas, KPIs y datos relacionados con autores, ubicaciones y materiales. Utiliza SQLAlchemy para interactuar con la base de datos y pandas para procesar los datos.

### Catálogo de Funciones y Clases
- `DeliveriesService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `get_full_context()` - Genera el contexto completo para las entregas, incluyendo estadísticas, KPIs y datos relacionados.
- `_prepare_area_stats(year, month_str)` - Prepara el DataFrame de estadísticas por área.
- `_calculate_kpis(sla_df, area_stats_df, total_dias)` - Calcula el diccionario de KPIs globales de forma segura.
- `_prepare_authors(year, month_str)` - Obtiene ranking de autores con comparativa mensual.
- `_prepare_locations(year, month_str)` - Obtiene ranking de ubicaciones con comparativa mensual.
- `_prepare_materials_by_area(year, month_str)` - Estructura el ranking de materiales por cada área de negocio.

### Interacción con Base de Datos
El archivo interactúa con una base de datos utilizando SQLAlchemy. Las tablas y columnas específicas son:
- Tabla: `outbound_deliveries`
  - Columna: `fecha_carga`
- Tabla: `config_queries`
  - Columnas: `query_id`, `sql_text`, `visual_state`
- Tabla: `area_stats`
  - Columnas: `area`, `total_entregas`, `dias_activos`
- Tabla: `top_authors`
  - Columnas: `name`, `entregas`
- Tabla: `top_locations`
  - Columnas: `ubicacion`, `num_items`
- Tabla: `top_materials_by_area`
  - Columnas: `area`, `material`, `frequency`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
Dependencias:
- `sqlalchemy.orm.Session` - Para la sesión de base de datos.
- `pandas` - Para procesar los datos.
- `logging` - Para el registro de errores.
- `datetime` - Para manejar fechas.
- `typing` - Para tipos de datos.
- `core.utils.sanitize_for_json` - Para sanitizar datos para JSON.
- `core.state.get_app_state` - Para obtener el estado de la aplicación.
- `repositories.DeliveriesRepository` - Para interactuar con la base de datos.
- `core.query_engine.get_bound_params_from_visual_state` - Para obtener parámetros de consulta.
- `core.query_engine.extract_metric_value` - Para extraer métricas de los resultados de consulta.

Flujo:
El archivo se comunica con otros archivos del proyecto a través de las siguientes importaciones:
- `routes.inventory.get_inventory_context`
- `routes.tasks.get_tasks_context`
- `routes.analytics_proyecciones.get_proyecciones_context`

Estas funciones son llamadas para obtener contextos adicionales que se incluyen en el contexto final.


---

## Archivo: ./services/etl/__init__.py

### Resumen Funcional
Este archivo contiene funciones para procesar diferentes tipos de archivos relacionados con inventario y entregas. Cada función utiliza un adaptador específico para interactuar con la base de datos y realizar operaciones como procesar directorios o archivos individuales.

### Catálogo de Funciones y Clases
- `OutboundDeliveryAdapter` - Adaptador para manejar operaciones relacionadas con las entregas.
- `InventoryMovementAdapter` - Adaptador para manejar movimientos de inventario.
- `WarehouseTaskAdapter` - Adaptador para manejar tareas del almacén.
- `StockLevelAdapter` - Adaptador para manejar niveles de stock.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: No se mencionan librerías externas específicas.
- **Flujo Interno**: Las funciones interactúan con adaptadores para procesar archivos o directorios, lo que implica una comunicación interna entre el archivo y los adaptadores definidos en otros módulos del proyecto.


---

## Archivo: ./services/etl/base.py

### Resumen Funcional
El archivo `base.py` define una clase abstracta `BaseWMSProcessor` que proporciona funcionalidades para procesar archivos WMS (TXT/CSV/XLSX) y cargarlos en una base de datos SQLite. Incluye métodos para validar archivos, leer y limpiar datos, realizar operaciones UPSERT atómicas, y procesar directorios de archivos.

### Catálogo de Funciones y Clases
- `BaseWMSProcessor(encodings=None, chunk_size=50000)` - Constructor que inicializa los parámetros de codificación y tamaño de chunk.
  - Propósito: Configura las opciones iniciales para el procesamiento del archivo.

- `validate_file(file_path)` - Método abstracto que verifica si el archivo es válido para este procesador.
  - Propósito: Implementado por cada hijo para validar archivos específicos.

- `_clean_dataframe(df)` - Método abstracto que limpia y transforma un chunk de datos crudos.
  - Propósito: Implementado por cada hijo para realizar la limpieza específica del archivo.

- `_detect_file_params(file_path, required_columns)` - Detecta la fila de encabezado y codificación buscando columnas clave.
  - Propósito: Identifica los parámetros necesarios para leer el archivo correctamente.

- `read_and_clean_data(file_path)` - Lee el archivo completo (para testing o archivos pequeños).
  - Propósito: Carga y limpia un archivo en su totalidad.

- `_get_required_columns()` - Devuelve una lista de columnas requeridas en el encabezado.
  - Propósito: Implementado por cada hijo para especificar las columnas necesarias.

- `_get_primary_keys()` - Devuelve las columnas que actúan como clave primaria para deduplicación.
  - Propósito: Implementado por cada hijo para especificar las claves primarias.

- `process_and_save(file_path, db_path, table_name, conn=None)` - Orquestador unificado de procesamiento Chunked + Upsert SQLite.
  - Propósito: Procesa archivos en chunks y realiza operaciones UPSERT atómicas en la base de datos.

- `_upsert_chunk(conn, df, table_name)` - Lógica de Upsert atómico por chunk.
  - Propósito: Realiza una operación UPSERT atómica para un chunk de datos.

- `process_directory(folder_path, db_path, table_name, conn=None)` - Escanea un directorio y procesa todos los archivos compatibles con Upsert acumulativo.
  - Propósito: Procesa múltiples archivos en un directorio y realiza operaciones UPSERT atómicas.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: No aplica (se espera que las tablas sean proporcionadas como parámetros)
- Columnas: No aplica (se espera que las columnas sean proporcionadas como parámetros)

### Estado y Variables Globales
- `logger` - Variable global para el registro de eventos.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas`
  - `pathlib`
  - `sqlite3`
  - `typing`
  - `logging`

- Flujo: El archivo interactúa con clases y funciones definidas en otros archivos del proyecto, como `core.security.validate_table`.


---

## Archivo: ./services/etl/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene una clase `OutboundDeliveryAdapter` que extiende `BaseWMSProcessor`. Esta clase se encarga de procesar archivos de entregas de salida (Deliveries) utilizando pandas y SQLite. El objetivo es validar el archivo, limpiar los datos, aplicar mapeos y cálculos necesarios, y finalmente insertar o actualizar los datos en una base de datos SQLite.

### Catálogo de Funciones y Clases
- `OutboundDeliveryAdapter(BaseWMSProcessor)` - Adaptador para procesar Entregas de Salida (Deliveries).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y tiene una extensión permitida.
  - `_get_required_columns() -> List[str]` - Devuelve las columnas requeridas en el DataFrame.
  - `_get_primary_keys() -> List[str]` - Devuelve las claves primarias utilizadas para la deduplicación.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza el DataFrame.
  - `_sanitizar_nombres_columnas(columns: pd.Index) -> list` - Sanitiza los nombres de las columnas eliminando caracteres no válidos y evitando duplicados.
  - `_upsert_chunk(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str)` - Inserta o actualiza datos en una tabla SQLite.

### Interacción con Base de Datos
- Motor de base de datos: SQLite.
- Tablas modificadas: No se especifican explícitamente las tablas, pero el método `_upsert_chunk` indica que interactúa con una tabla SQLite.
- Columnas modificadas: Dependiendo del contenido del DataFrame `df`, se pueden agregar nuevas columnas a la tabla.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas` - Para el procesamiento de datos.
  - `pathlib` - Para manejar rutas de archivos.
  - `typing` - Para definir tipos de variables.
  - `sqlite3` - Para interactuar con la base de datos SQLite.
- Flujo interno:
  - El archivo se comunica con el módulo `base.py` a través de la herencia de la clase `BaseWMSProcessor`.
  - Utiliza funciones auxiliares definidas en `core.wms_utils`, como `sanitize_string`, `map_wms_status`, etc.
  - Interactúa con archivos de entrada (Excel, TXT) y una base de datos SQLite.


---

## Archivo: ./services/etl/movements.py

### Resumen Funcional
El archivo `movements.py` contiene una clase `InventoryMovementAdapter` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos CSV relacionados con movimientos en un sistema WMS (Warehouse Management System), validando su contenido, limpiándolo y clasificándolo según ciertas reglas.

### Catálogo de Funciones y Clases
- **InventoryMovementAdapter(BaseWMSProcessor)** - Adaptador específico para procesar el formato WMS Movimientos.
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo CSV existe y cumple con los requisitos mínimos.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas en el archivo CSV.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias utilizadas para identificar registros.
  - `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza los datos del DataFrame, aplicando diversas transformaciones como la eliminación de columnas vacías, renombramiento de columnas, validación de valores y clasificación de operaciones según el tipo de movimiento.
  - `_vectorized_classify(df: pd.DataFrame) -> pd.DataFrame` - Clasifica las filas del DataFrame en función de los valores de ciertas columnas.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales, de sesión o de entorno en este archivo.

### Dependencias y Flujo
- **Librerías externas utilizadas**: `pandas`, `numpy`, `pathlib`.
- **Flujo interno**: El archivo interactúa con el objeto `BaseWMSProcessor` para procesar archivos CSV, utilizando métodos de limpieza y clasificación definidos en la clase `InventoryMovementAdapter`.


---

## Archivo: ./services/etl/stock.py

### Resumen Funcional
El archivo `stock.py` contiene una clase `StockLevelAdapter` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos de inventario/stock en formato LX02, validar su contenido, leer y limpiar los datos, y luego guardarlos en una base de datos SQLite.

### Catálogo de Funciones y Clases
- **StockLevelAdapter(BaseWMSProcessor)** - Adaptador para procesar Inventario/Stock LX02. Realiza REPLACE completo.
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve las columnas clave del header SAP LX02.
  - `read_and_clean_data(file_path: Path) -> pd.DataFrame` - Lee el archivo LX02/Stock, detectando la fila header automáticamente y limpia los datos.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia las filas y columnas vacías y limpia los strings de las columnas de tipo objeto.
  - `process_directory(folder_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int` - Combina todos los archivos en el directorio especificado, realiza la limpieza y guarda los datos en una base de datos SQLite.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: No aplica (No se mencionan tablas específicas).
- **Columnas**: No aplica (No se mencionan columnas específicas).

### Estado y Variables Globales
- **Variables Globales**: No aplica.

### Dependencias y Flujo
- **Librerías Externas**:
  - `pandas` - Para el procesamiento de datos.
  - `pathlib` - Para manejar rutas de archivos.
  - `typing` - Para definir tipos de variables.
  - `sqlite3` - Para interactuar con la base de datos SQLite.
  - `os` - Para operaciones del sistema.
  - `datetime` - Para obtener la fecha y hora actual.
  - `logging` - Para el registro de errores.

- **Flujo**: El archivo se comunica con otros archivos dentro del proyecto a través de importaciones relativas (`from .base import BaseWMSProcessor`).


---

## Archivo: ./services/etl/tasks.py

### Resumen Funcional
El archivo `tasks.py` contiene una clase `WarehouseTaskAdapter` que hereda de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos en formato WMS Tareas (Órdenes de Transporte), validando su contenido, obteniendo columnas requeridas y limpiando los datos.

### Catálogo de Funciones y Clases
- **WarehouseTaskAdapter(BaseWMSProcessor)** - Adaptador específico para procesar el formato WMS Tareas (Órdenes de Transporte).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas para el procesamiento.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias utilizadas en el procesamiento.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza los datos del DataFrame.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Dependencias**: `pandas`, `pathlib`
- **Flujo**: El archivo interactúa con el módulo `base.py` a través de la herencia de la clase `BaseWMSProcessor`. No realiza interacciones directas con bases de datos o variables globales.


---

## Archivo: ./services/inventory_service.py (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `inventory_service.py` contiene una clase `InventoryService` que proporciona métodos para calcular y preparar diversos KPIs (Indicadores Clave de Desempeño) relacionados con el inventario, incluyendo ingresos, consumos, traspasos, devoluciones y eficiencia de bodega. Utiliza una base de datos SQL para obtener los datos necesarios.

### Catálogo de Funciones y Clases
- `InventoryService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `_get_latest_data_period()` - Obtiene el período más reciente de datos disponibles en la tabla `inventory_movements`.
- `_prepare_volume_kpis(anio, mes)` - Calcula KPIs relacionados con los volúmenes de ingresos y consumos.
- `_prepare_abc_analytics(anio, mes)` - Realiza análisis ABC para determinar el impacto de diferentes materiales en el inventario.
- `_prepare_area_analytics(anio, mes)` - Calcula estadísticas de consumo por área con promedios diarios robustos.
- `_prepare_trend_analytics(anio, mes)` - Genera tendencias de movimientos de inventario a nivel semanal y mensual.
- `_prepare_user_location_analytics(anio, mes)` - Estadísticas detalladas de usuarios y ubicaciones con actividad mensual.
- `_prepare_planned_consumption_trend()` - Calcula la tendencia de consumos planificados vs desplanificados.

### Interacción con Base de Datos
- Motor: SQLite (inferred from the use of `text` for SQL queries)
- Tablas:
  - `inventory_movements`
- Columnas:
  - `fe_contab`, `cmv`, `tipo_operacion`, `material`, `qty`, `registrado`, `usuario`, `alm`, `texto_cab_documento`, `referencia`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sqlalchemy`
  - `pandas`
  - `logging`
  - `datetime`
  - `numpy`
- Comunicación con otros archivos del proyecto:
  - `repositories.InventoryRepository` (para obtener datos de inventario)
  - `core.utils.sanitize_for_json` (para sanitizar datos para JSON)
  - `core.state.get_app_state` (no se usa en este fragmento)
  - `core.wms_config.COST_CENTER_MAPPING` (no se usa en este fragmento)

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `inventory_service.py` contiene funciones para preparar y obtener el contexto de datos necesario para un dashboard de movimientos en una aplicación de inventario. Incluye la generación de indicadores clave (KPIs), análisis de volumen, área, ABC, usuarios, tendencias y proyecciones.

### Catálogo de Funciones y Clases
- `_prepare_planned_consumption_trend()` - Prepara los datos para el gráfico de consumo planificado.
- `_get_empty_context()` - Devuelve un contexto vacío con valores iniciales.
- `get_full_context()` - Genera el contexto completo para el dashboard, incluyendo KPIs, análisis y proyecciones.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Depende de la clase `InventoryRepository` para interactuar con la base de datos.
- Comunica con el archivo `routes.analytics_proyecciones.py` para obtener contexto de proyecciones.
- Utiliza funciones como `get_app_state()`, `set_cache()`, y `save_analytics_snapshot()` que no se muestran en el fragmento.


---

## Archivo: ./services/tasks_service.py

### Resumen Funcional
El archivo `tasks_service.py` contiene una clase `TasksService` que se encarga de generar y cachear el contexto analítico para la gestión de Operaciones Técnicas (OTs). Este contexto incluye datos resumidos, tendencias, usuarios, tipos de almacenamiento, movimientos no paletizados y KPIs dinámicos.

### Catálogo de Funciones y Clases
- `TasksService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `get_full_context() -> dict` - Genera y cachea el contexto analítico para la gestión de OTs.

### Interacción con Base de Datos
- **Motor:** SQLAlchemy
- **Tablas:** No aplica (se asume que las consultas SQL son ejecutadas directamente contra una base de datos compatible con SQLAlchemy).
- **Columnas:** No aplica (se asume que las consultas SQL son ejecutadas directamente contra una base de datos compatible con SQLAlchemy).

### Estado y Variables Globales
- `state` - Almacena el estado de la aplicación, utilizado para cachear el contexto analítico.

### Dependencias y Flujo
- **Librerías Externas:** 
  - `sqlalchemy`
  - `pandas`
  - `logging`
  - `datetime`
- **Flujo Interno:**
  - La clase `TasksService` depende de la sesión de base de datos para interactuar con el repositorio `TasksRepository`.
  - Utiliza funciones auxiliares como `_get_bound_params_from_visual_state`, `_extract_metric_value` y `sanitize_for_json` definidas en otros módulos (`core.utils`).
  - La clase no depende directamente de archivos específicos del proyecto, sino que interactúa con el repositorio para obtener datos y ejecuta consultas SQL dinámicas.


---

## Archivo: ./services/tunnel.py

### Resumen Funcional
El archivo `tunnel.py` define un servicio para iniciar y gestionar un túnel público utilizando el software ngrok. El servicio se ejecuta en un hilo separado y maneja la creación, reinicio y detención del túnel, guardando la URL pública generada en un archivo.

### Catálogo de Funciones y Clases
- `NgrokService(bin_path=NGROK_BIN, tunnel_file=TUNNEL_URL_FILE)` - Inicializa el servicio con el camino al binario de ngrok y el archivo donde se guarda la URL del túnel.
  - `_validate_bin()` - Valida si el binario de ngrok existe y tiene permisos de ejecución.
  - `_save_url(url)` - Guarda la URL del túnel en un archivo y establece los permisos adecuados.
  - `_get_public_url()` - Obtiene la URL pública del túnel a través de la API de ngrok.
  - `start()` - Inicia el servicio en un hilo separado.
  - `stop()` - Detiene el proceso del túnel y limpia los recursos.
  - `_run_loop()` - Bucle principal que gestiona la creación y reinicio del túnel.

- `start_tunnel()` - Función para iniciar el servicio de túnel de forma segura y thread-safe.
- `stop_tunnel()` - Función para detener el servicio de túnel de forma segura y thread-safe.

### Interacción con Base de Datos
No aplica. El archivo no interactúa con ninguna base de datos.

### Estado y Variables Globales
- `_service_lock` - Lock para proteger el acceso al servicio global.
- `_global_service` - Variable global que almacena la instancia del servicio de túnel.

### Dependencias y Flujo
- `os`, `subprocess`, `threading`, `time`, `urllib.request`, `json`, `logging`: Librerías estándar de Python utilizadas para el manejo de procesos, hilos, tiempo, red, logging, etc.
- `config.py`: Archivo que contiene las configuraciones globales del proyecto, específicamente los caminos al binario de ngrok y al archivo donde se guarda la URL del túnel.


---

## Archivo: ./static/css/analytics_proyecciones.css

### Resumen Funcional
El archivo `analytics_proyecciones.css` contiene estilos CSS para una interfaz de usuario que muestra proyecciones y alertas. Define clases para contenedores, gráficos, tarjetas combinadas, tablas de alertas y modales.

### Catálogo de Funciones y Clases
No se detectan funciones específicas en este archivo. Solo se definen clases CSS.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Este archivo no depende de ninguna librería externa ni comunica con otros archivos del proyecto.


---

## Archivo: ./static/css/deliveries.css

### Resumen Funcional
El archivo `deliveries.css` contiene estilos CSS para una interfaz de usuario que muestra estadísticas, gráficos y listas de materiales en un contexto de entregas o logística.

### Catálogo de Funciones y Clases
No aplica

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
No aplica


---

## Archivo: ./static/css/docs_explorer.css

### Resumen Funcional
El archivo `docs_explorer.css` define los estilos para una interfaz de usuario que permite explorar y visualizar documentación, con un diseño premium y responsive.

### Catálogo de Funciones y Clases
No aplica

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
No aplica


---

## Archivo: ./static/css/inventory.css

### Resumen Funcional
El archivo `inventory.css` contiene estilos CSS para una interfaz de usuario que muestra estadísticas y gráficos en un contenedor de inventario. Incluye clases para contenedores, tarjetas de estadísticas, listas de clasificación, encabezados y modales.

### Catálogo de Funciones y Clases
No aplica

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
No aplica


---

## Archivo: ./static/css/sla_table.css

### Resumen Funcional
El archivo `sla_table.css` define estilos CSS para una tabla de auditoría SLA (Service Level Agreement), incluyendo clases para el contenedor principal, los controles del encabezado, la tabla en sí y las celdas. También incluye estilos responsivos para pantallas pequeñas.

### Catálogo de Funciones y Clases
- `.container` - Establece el diseño general del contenedor.
- `.header-controls` - Define el estilo y la disposición de los controles del encabezado.
- `.table-wrapper` - Estilo para el envoltorio de la tabla.
- `table` - Estilos generales para la tabla.
- `th` - Estilos para las celdas de encabezado.
- `td` - Estilos para las celdas de datos.
- `.pill` - Estilo general para los elementos pill.
- `.pill.late` - Estilo específico para los elementos pill que indican retraso.
- `.pill.ontime` - Estilo específico para los elementos pill que indican cumplimiento a tiempo.
- `.area-badge` - Estilo para las etiquetas de área.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
No depende de ninguna librería externa ni comunica con otros archivos del proyecto.


---

## Archivo: ./static/js/analytics_proyecciones.js

### Resumen Funcional
El archivo `analytics_proyecciones.js` contiene lógica para renderizar y controlar modales de alertas, combinaciones y gráficos de dispersión en una interfaz web. Utiliza funciones para filtrar y mostrar datos basados en criterios de búsqueda y selección.

### Catálogo de Funciones y Clases
- `renderAlerts()` - Renderiza los datos de alertas en un modal.
- `renderCombos(filterText = "")` - Renderiza los datos de combinaciones en un modal, filtrando por texto.
- `renderScatter()` - Renderiza los datos de dispersión en un modal, filtrando por texto y categoría.
- `openModalAlerts()` - Abre el modal de alertas y carga los datos iniciales.
- `openModalCombos()` - Abre el modal de combinaciones y carga los datos iniciales.
- `openModalScatter()` - Abre el modal de dispersión y carga los datos iniciales.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencia: `core_ui.js` (carga previa para proporcionar funciones como `CoreUI.openModal`, `CoreUI.closeModal`, `CoreUI.populateAreaSelect`, y `CoreUI.getData`).


---

## Archivo: ./static/js/analytics_studio.js (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `analytics_studio.js` contiene funciones y variables para gestionar el estado del Studio de Análíticas, incluyendo la carga de esquemas de base de datos, visualización de consultas SQL y generación de gráficos.

### Catálogo de Funciones y Clases
- `openEditQueryModal(queryId, chartTitle)` - Abre un modal para editar una consulta.
- `loadSchema()` - Carga el esquema de la base de datos.
- `previewTable(tableName, el)` - Muestra una vista previa de una tabla en la interfaz.
- `runPreview()` - Ejecuta una consulta SQL y muestra su resultado en un gráfico o tabla.
- `renderPreviewChart(data)` - Renderiza el resultado de una consulta como un gráfico.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `studioChartInstance` - Instancia del gráfico actual.
- `currentSchema` - Esquema de la base de datos actual.
- `currentQueryId` - ID de la consulta actualmente seleccionada.
- `studioBoundParams` - Parámetros de la consulta actual.
- `serverVisualState` - Estado visual guardado en el servidor.
- `visualState` - Estado del constructor visual actual.
- `defaultVisualStates` - Mapeo predefinido para inicializar gráficos.

### Dependencias y Flujo
Dependencias:
- `Chart.js` - Librería para renderizar gráficos.

Flujo:
1. El usuario selecciona una consulta en el Studio de Análíticas.
2. Se abre un modal con la opción de editar la consulta.
3. La consulta se carga y se muestra en un editor de texto.
4. El usuario puede modificar la consulta y ejecutarla para obtener resultados.
5. Los resultados se renderizan como gráficos o tablas según el tipo de consulta.

El archivo interactúa con una API que proporciona los datos necesarios para cargar esquemas, ejecutar consultas y obtener visualizaciones.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `analytics_studio.js` contiene funciones y métodos para gestionar la creación, edición y publicación de consultas analíticas. Permite configurar gráficos, filtros y condiciones de búsqueda, y sincroniza estos cambios con un backend que genera y ejecuta consultas SQL.

### Catálogo de Funciones y Clases
- `closeEditQueryModal()` - Cierra el modal para editar una consulta.
- `showConfirmPublish()` - Muestra la ventana de confirmación para publicar una consulta.
- `hideConfirmPublish()` - Oculta la ventana de confirmación para publicar una consulta.
- `executePublishQuery()` - Ejecuta la publicación de una consulta y maneja la respuesta del backend.
- `initVisualQuery(queryId)` - Inicializa el estado visual de la consulta y carga los datos necesarios.
- `onBaseTableChange()` - Maneja el cambio en la tabla base seleccionada.
- `getActiveTables()` - Devuelve las tablas activas en la consulta.
- `getActiveColumns()` - Devuelve las columnas activas en la consulta.
- `refreshQbColumns(forceState = false)` - Refresca los selectores de columnas para los ejes y desglose.
- `renderJoins()` - Renderiza los controles de join en el formulario.
- `addJoin()` - Añade un nuevo join al estado visual.
- `updateJoin(index)` - Actualiza un join existente en el estado visual.
- `removeJoin(index)` - Elimina un join del estado visual.
- `renderFilters()` - Renderiza los controles de filtro en el formulario.
- `addFilter()` - Añade un nuevo filtro al estado visual.
- `updateFilterType(index, type)` - Actualiza el tipo de valor para un filtro.
- `updateFilter(index)` - Actualiza la configuración de un filtro existente.
- `removeFilter(index)` - Elimina un filtro del estado visual.
- `onSecondMetricToggle()` - Maneja el toggle de la segunda métrica.
- `onQbChange()` - Sincroniza los cambios en el formulario con el estado visual y genera SQL.
- `syncVisualToSQL()` - Envía el estado visual al backend para generar y ejecutar una consulta SQL.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `studioChartInstance` - Instancia del gráfico generado por Chart.js.
- `visualState` - Estado visual actual de la consulta, incluyendo tablas, joins, filtros, métricas, etc.
- `serverVisualState` - Estado visual proporcionado por el servidor.
- `defaultVisualStates` - Estados visuales predeterminados para diferentes consultas.
- `currentSchema` - Esquema de las tablas disponibles en la base de datos.
- `studioBoundParams` - Parámetros vinculados a la consulta SQL generada.

### Dependencias y Flujo
Dependencias:
- `Chart.js` - Usado para generar gráficos.
- `fetch` - Para hacer solicitudes HTTP al backend.

Flujo interno:
1. El usuario interactúa con el formulario de configuración de consultas (tablas, joins, filtros, métricas).
2. Los cambios en el formulario se reflejan en el estado visual (`visualState`).
3. Al cambiar algo en el formulario, se llama a `onQbChange()`, que sincroniza los cambios con el backend y genera SQL.
4. El backend devuelve la consulta SQL generada, que se muestra en un editor de texto.
5. Cuando el usuario publica una consulta, se envía el estado visual al backend para ejecutar la consulta.

Flujo externo:
- La función `executePublishQuery()` se comunica con el backend a través de una solicitud POST a `/api/settings/query` para publicar la consulta.
- La función `syncVisualToSQL()` se comunica con el backend a través de una solicitud POST a `/api/studio/build_sql` para generar y ejecutar la consulta SQL.


---

## Archivo: ./static/js/core_ui.js

### Resumen Funcional
El archivo `core_ui.js` es un módulo de utilidades de interfaz de usuario compartido por todas las vistas del proyecto. Proporciona funciones para mostrar y ocultar modales, renderizar modales de lista de materiales, poblar selectores con áreas únicas y leer datos JSON embebidos en el DOM.

### Catálogo de Funciones y Clases
- `CoreUI.openModal(id)` - Muestra un modal por su ID de elemento.
- `CoreUI.closeModal(id)` - Oculta un modal por su ID de elemento.
- `CoreUI.renderMaterialModal(opts)` - Rellena y abre un modal de lista de materiales con los ítems proporcionados.
- `CoreUI.populateAreaSelect(selectId, data, key)` - Rellena un elemento `<select>` con áreas únicas encontradas en un array de datos.
- `CoreUI.getData(id)` - Lee y parsea JSON embebido en el textContent de un elemento del DOM.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- No se mencionan dependencias externas específicas en este archivo.

Flujo:
- El módulo expone funciones útiles para la interfaz de usuario.
- Las funciones pueden ser llamadas directamente desde el DOM o a través de alias globales (`window.openModal` y `window.closeModal`).


---

## Archivo: ./static/js/dashboard.js

### Resumen Funcional
El archivo `dashboard.js` contiene la lógica principal del dashboard de MonitorWeb. Define funciones para interactuar con una API, manejar la interfaz de usuario (UI), aplicar filtros y ordenar tablas, generar PDFs, y sincronizar datos.

### Catálogo de Funciones y Clases
- `DashboardAPI._fetch(url, options)` - Realiza solicitudes HTTP a la API.
- `DashboardAPI.fetchKPIs(params)` - Obtiene los KPIs (Indicadores Clave de Desempeño) basados en los parámetros proporcionados.
- `DashboardAPI.fetchFilteredData(params)` - Obtiene datos filtrados según los parámetros proporcionados.
- `DashboardAPI.sync()` - Sincroniza los datos del cliente con el servidor.
- `DashboardAPI.checkSyncStatus()` - Verifica el estado de la sincronización actual.
- `DashboardAPI.logout()` - Cierra sesión y redirige al usuario a la página de inicio de sesión.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- `fetch` (navegador)
- `localStorage`

Flujo:
- El archivo interactúa con la API para obtener datos, renderizar tablas, aplicar filtros, generar PDFs y sincronizar datos.
- Utiliza funciones globales como `closePdfModal`, `toggleMulti`, `sortTable`, etc., que se definen en el mismo archivo y son accesibles globalmente a través de `window`.


---

## Archivo: ./static/js/dashboard_charts.js

### Resumen Funcional
Este archivo JavaScript se encarga de inicializar y gestionar un gráfico de barras pilaado en el panel de control, calculando y mostrando la suma total de los datos para cada categoría. También proporciona funcionalidades para seleccionar/deseleccionar todos los elementos del gráfico.

### Catálogo de Funciones y Clases
- `stackedTotalPlugin` - Plugin que agrega una etiqueta con el total acumulado en cada barra del gráfico.
  - Parámetros: `chart` (el contexto del gráfico).
  - Propósito: Calcula la suma total de los datos para cada categoría y muestra esta suma en la parte superior de las barras.

- `initWeeklyChart(chartLabels, chartDatasets)` - Inicializa el gráfico de barras pilaado.
  - Parámetros: `chartLabels` (etiquetas del eje X), `chartDatasets` (conjuntos de datos para el gráfico).
  - Propósito: Configura y muestra el gráfico con los datos proporcionados.

- `toggleChartSelectAll(isChecked)` - Función que selecciona/deselecciona todos los elementos del gráfico.
  - Parámetros: `isChecked` (booleano, indica si se debe seleccionar o deseleccionar).
  - Propósito: Actualiza el estado de selección de todos los checkboxes relacionados con el gráfico.

- `updateChartVisibility()` - Función que actualiza la visibilidad de los conjuntos de datos del gráfico según las selecciones.
  - Parámetros: Ninguno.
  - Propósito: Oculta o muestra los conjuntos de datos del gráfico según qué checkboxes están seleccionados.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
- `window.weeklyChart` - Variable global que almacena el contexto del gráfico inicializado.

### Dependencias y Flujo
- **Librerías Externas**: `Chart.js` (usado para crear y gestionar el gráfico).
- **Flujo Interno**: El archivo se comunica con otros elementos del DOM para obtener referencias a checkboxes y elementos de entrada, y también interactúa con la función `applyFilters` si está definida.


---

## Archivo: ./static/js/deliveries.js (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `deliveries.js` contiene la lógica para el análisis de entregas, incluyendo la interacción con componentes UI, controladores de modales, inicialización de gráficos y actualizaciones dinámicas del estado.

### Catálogo de Funciones y Clases
- `openModal(id)` - Abre un modal utilizando CoreUI.
- `closeModal(id)` - Cierra un modal utilizando CoreUI.
- `renderMaterialModal(opts)` - Renderiza un modal con opciones específicas.
- `getData(id)` - Obtiene datos desde una fuente externa.
- `toggleModalFilter(type, isCurrentMonth)` - Alternativa entre mostrar modales de área y día según el contexto actual.
- `openModalWeekday(dayName, isCurrentMonth = false)` - Abre un modal para mostrar detalles del día.
- `openModalUbicacion(name)` - Abre un modal para mostrar detalles de ubicación.
- `openModalArea(name, isCurrentMonth = false)` - Abre un modal para mostrar detalles de área.
- `openModalUser(name)` - Abre un modal para mostrar detalles de usuario.
- `switchVLView(view)` - Cambia la vista entre operativa y histórica.
- `toggleMulti(id)` - Alterna la visibilidad de elementos según su ID.
- `updateDeliveriesAnalytics()` - Actualiza los KPIs y filtra listas y gráficos según las áreas seleccionadas.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `currentModalContext` - Almacena el contexto actual del modal (área y día).
- `window.slaTrendChart`, `window.monthlyTrendChart`, etc. - Referencias a gráficos inicializados.

### Dependencias y Flujo
Depende de `core_ui.js` para funciones UI como `openModal`, `closeModal`, y `renderMaterialModal`. Utiliza `getData` para obtener datos desde fuentes externas.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `deliveries.js` contiene funciones para actualizar gráficos de rendimiento diario, semanal y mensual basados en datos seleccionados. Actualiza los datos de las gráficas de SLA (Service Level Agreement) y entrega semanal.

### Catálogo de Funciones y Clases
- `updateDeliveriesAnalytics()` - Actualiza los datos de las gráficas de rendimiento.
- `window.toggleChartSelectAll(isChecked)` - Maneja la selección de todos los elementos en un grupo de checkboxes.
- `window.handleSmartCheckbox(cb)` - Maneja la selección inteligente de elementos individuales en un grupo de checkboxes.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- `getData('data_weekly_raw_json')`
- `getData('data_sla_area_trend_raw_json')`

Flujo:
1. La función `updateDeliveriesAnalytics()` se ejecuta cuando se necesitan actualizar los datos de las gráficas.
2. Se filtran los datos según la selección del usuario (`selected`).
3. Los datos filtrados se agrupan y procesan para calcular SLA y entregas.
4. Los resultados se actualizan en las gráficas correspondientes.

La función `window.toggleChartSelectAll(isChecked)` maneja la selección de todos los elementos en un grupo de checkboxes, asegurando que no haya una selección vacía.

La función `window.handleSmartCheckbox(cb)` maneja la selección inteligente de elementos individuales, asegurando que si "Todos" está seleccionado y se selecciona uno individualmente, "Todos" se deselecciona.


---

## Archivo: ./static/js/docs_explorer.js

### Resumen Funcional
El archivo `docs_explorer.js` es un script que se encarga de cargar y renderizar una estructura de árbol de documentos en la interfaz web. Este árbol permite navegar por los archivos y carpetas, y al seleccionar un archivo, carga su contenido en el área de visualización.

### Catálogo de Funciones y Clases
- `initDocs()` - Inicializa la exploración de documentos, cargando la estructura del árbol desde una API y renderizando los nodos.
- `loadFile(path)` - Carga el contenido de un archivo específico en el área de visualización.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Dependencias**: El script utiliza la librería `fetch` para hacer solicitudes HTTP a una API. También depende de la librería `marked` si está disponible, para procesar el contenido del archivo como Markdown.
- **Flujo**: El flujo comienza con la carga del documento (`DOMContentLoaded`), luego se ejecuta `initDocs()`. Este método llama a `loadFile()` cuando se selecciona un archivo en el árbol.


---

## Archivo: ./static/js/inventory.js

### Resumen Funcional
El archivo `inventory.js` contiene lógica para el análisis de inventario, incluyendo la visualización de gráficos y la interacción con modales. Se utilizan Chart.js para crear gráficos de doughnut y lineas, y se manejan eventos de entrada para buscar ubicaciones dinámicamente.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra mensajes en la consola.
- `UI.openModal(id)` - Abre un modal utilizando CoreUI.
- `UI.closeModal(id)` - Cierra un modal utilizando CoreUI.
- `UI.renderMaterialModal(opts)` - Renderiza un modal de material utilizando CoreUI.
- `getData(id)` - Obtiene datos desde el DOM utilizando CoreUI.
- `parseFormattedInt(val)` - Convierte una cadena a un número entero, eliminando caracteres no numéricos.
- `window.openModalUbicacion(name)` - Abre un modal con información de ubicación.
- `window.openModalUserInv(name)` - Abre un modal con información de usuario.
- `window.switchInventarioView(view)` - Cambia la vista del gráfico de tendencias según el parámetro `view`.
- `window.toggleMultiInv(id)` - Alterna la visibilidad de un elemento según su ID.
- `window.toggleAllInvAreas(checkbox)` - Alterna la selección de todas las áreas y actualiza los KPIs.
- `window.updateInventoryAnalytics()` - Actualiza los KPIs y filtra listas según las áreas seleccionadas.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: Chart.js, CoreUI.
- **Flujo Interno**: El archivo interactúa con el DOM para obtener datos y renderizar gráficos. Utiliza funciones de CoreUI para abrir y cerrar modales.


---

## Archivo: ./static/js/sla_table.js

### Resumen Funcional
Este archivo contiene la lógica para manejar el comportamiento de una tabla de auditoría SLA en una aplicación web, incluyendo la interacción con un modal PDF y el envío de formularios.

### Catálogo de Funciones y Clases
- `openPdfModal()` - Abre el modal PDF.
- `closePdfModal()` - Cierra el modal PDF y limpia su contenido.
- `pdfSubmit(btn, frameTarget, preview)` - Envía un formulario y maneja la interacción con un iframe para mostrar una vista previa del PDF.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- No depende de ninguna librería externa.
- Se comunica con otros archivos a través de la ventana global (`window.pdfSubmit` y `window.closePdfModal`).


---

## Archivo: ./static/js/tasks.js

### Resumen Funcional
El archivo `tasks.js` contiene la lógica para inicializar y configurar dos gráficos de tendencia y usuarios utilizando la biblioteca Chart.js. Los datos necesarios se obtienen del DOM y se utilizan para renderizar los gráficos.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra un mensaje en la consola con opcionalmente datos adicionales.
- `getData(id)` - Obtiene y analiza el contenido JSON de un elemento del DOM identificado por su ID.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales en este archivo.

### Dependencias y Flujo
- **Librerías Externas**: `Chart.js`, `ChartDataLabels`.
- **Flujo Interno**: El archivo se ejecuta cuando el DOM esté completamente cargado (`DOMContentLoaded`). Luego, intenta obtener datos de elementos del DOM y usarlos para crear dos gráficos (uno de tipo línea y otro de tipo barras) utilizando Chart.js.


---

## Archivo: ./templates/analytics_proyecciones.html

### Resumen Funcional
El archivo `analytics_proyecciones.html` es una plantilla HTML para la interfaz de usuario de un módulo de análisis predictivo, que muestra información sobre desplanificaciones y predicciones de demanda. Incluye gráficos interactivos y tablas para visualizar datos relevantes.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo HTML.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `user.username`: Almacena el nombre de usuario actual.
- `error_msg`: Almacena un mensaje de error si ocurre algún problema.
- `alerts`: Lista de alertas de desplanificación.
- `scatter_data`: Datos para el gráfico de dispersión "Frecuencia vs Volumen".
- `combos`: Datos para la visualización de combinaciones frecuentes (Market Basket Analysis).

### Dependencias y Flujo
- **Librerías Externas**: 
  - `Chart.js` para crear gráficos interactivos.
- **Archivos del Proyecto**:
  - `_styles.html`: Incluye estilos CSS adicionales.
  - `_analytics_proyecciones_modals.html`: Contiene modales adicionales.
  - `_scripts.html`: Incluye scripts adicionales.
  - `analytics_proyecciones.js`: Script personalizado para el módulo de análisis predictivo.


---

## Archivo: ./templates/dashboard.html

### Resumen Funcional
El archivo `dashboard.html` es una plantilla HTML para el panel de control del proyecto Onedrive, que muestra indicadores clave (KPIs) y proporciona acceso a diferentes módulos y funciones.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo. Todo el contenido es estructura HTML y Jinja2 templating.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `is_syncing`: Variable que indica si la sincronización está en curso.
- `user.username`: Nombre del usuario actual.
- `user.role`: Rol del usuario actual.
- `kpi_deliveries`: Número total de entregas generadas.
- `sub_del_abierta`, `sub_del_no_tratada`, `sub_del_reunido`, `sub_del_atrasado`, `sub_del_critico`: Contadores para diferentes estados de entregas.
- `kpi_materials`: Número total de materiales solicitados.
- `sub_mat_abierta`, `sub_mat_no_tratada`, `sub_mat_reunido`, `sub_mat_atrasado`, `sub_mat_critico`: Contadores para diferentes estados de materiales.

### Dependencias y Flujo
- **Librerías externas**: No se detectan librerías externas específicas.
- **Flujo interno**: El archivo incluye varios parciales HTML (`_styles.html`, `_modals.html`, `_sidebar.html`, `_table.html`, `_scripts.html`) que probablemente contienen el contenido específico para estos elementos.


---

## Archivo: ./templates/deliveries.html (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para la interfaz de usuario del proyecto, que incluye elementos como encabezados, botones de pestañas y scripts JavaScript para manejar el comportamiento de las pestañas y cargar datos dinámicamente.

### Catálogo de Funciones y Clases
- `switchTab(tabId, btnElement)` - Cambia la pestaña activa.
- `openNonPalletizedDetails(user, claseMov)` - Abre un modal con detalles no paletizados.
- `initTableFilters()` - Inicializa los filtros de tablas.
- `filterOTTable()` - Filtra la tabla de OTs según los criterios seleccionados.
- `filterDiscrepancyTable()` - Filtra la tabla de Discrepancias según los criterios seleccionados.
- `sortTableDiscrepancy(columnIndex)` - Ordena la tabla de Discrepancias.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías externas**: 
  - Chart.js
  - Chartjs-plugin-datalabels
  - Font Awesome
  - marked
- **Archivos JavaScript**:
  - `core_ui.js`
  - `deliveries.js`
  - `inventory.js`
  - `analytics_proyecciones.js`
  - `docs_explorer.js`
- **Archivos CSS**:
  - Estilos definidos en el archivo y referencias a archivos externos
- **Datos JSON**: 
  - Datos inyectados desde variables de contexto del servidor (por ejemplo, `area_stats_json`, `weekdays`, etc.)


---

## Archivo: ./templates/inventory.html

### Resumen Funcional
El archivo `inventory.html` es una plantilla HTML para la interfaz de usuario del módulo de inventario, que muestra análisis y gráficos relacionados con las entradas, consumos y traspasos de materiales.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo. Todo el contenido es estructura HTML y JavaScript.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `user.username`: Nombre del usuario actual.
- `kpi_ingresos`: Total de ingresos.
- `kpi_consumos_prod`: Consumo de producción.
- `kpi_consumos_mant`: Consumo de mantenimiento.
- `rate_reabast`: Tasa de reabastecimiento.
- `kpi_traspasos`: Número de traspasos.
- `rate_devolucion`: Tasa de devoluciones.
- `kpi_devoluciones`: Cantidad de devoluciones.
- `volumen_data`: Datos de volumen.
- `area_stats_json`: Estadísticas por área.
- `trend_labels`: Etiquetas para gráficos de tendencia.
- `trend_entradas`: Datos de entradas para gráficos de tendencia.
- `trend_salidas_prod`: Datos de salidas de producción para gráficos de tendencia.
- `trend_salidas_mant`: Datos de salidas de mantenimiento para gráficos de tendencia.
- `abc_counts`: Conteo de elementos ABC.
- `abc_mapping`: Mapeo de elementos ABC.
- `kpi_consumos_prod`: Consumo de producción (repetido).
- `kpi_consumos_mant`: Consumo de mantenimiento (repetido).
- `dow_distribution`: Distribución diaria.
- `ubicaciones_mapping`: Mapeo de ubicaciones.
- `area_material_mapping`: Mapeo de materiales por área.
- `user_material_mapping`: Mapeo de materiales por usuario.
- `dow_material_mapping`: Mapeo de materiales por distribución diaria.
- `pm_material_mapping`: Mapeo de materiales para producción vs mantenimiento.

### Dependencias y Flujo
- **Librerías externas**: 
  - Chart.js
  - Chartjs-plugin-datalabels

- **Archivos JavaScript**:
  - `core_ui.js`
  - `inventory.js`

- **Modales y parciales HTML incluidos**:
  - `_styles.html`
  - `_inventory_modals.html`
  - `_quick_login_modal.html`
  - `_logout.html`


---

## Archivo: ./templates/login.html

### Resumen Funcional
El archivo `login.html` es una página de inicio de sesión para la aplicación MonitorWeb. Permite a los usuarios ingresar sus credenciales y autenticarse en el sistema.

### Catálogo de Funciones y Clases
- `handleLogin(event)` - Maneja el evento de envío del formulario de inicio de sesión, realiza la autenticación y redirige al usuario según sea necesario.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: No se utilizan librerías externas.
- **Flujo Interno**: El archivo interactúa con el backend a través de una solicitud POST a la ruta `/api/auth/login`. La respuesta del servidor es manejada para determinar si la autenticación fue exitosa o no, y en consecuencia, se redirige al usuario.


---

## Archivo: ./templates/partials/_analytics_proyecciones_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para tres modales: uno que muestra todas las alertas de desplanificación, otro que muestra correlaciones de materiales (combos), y otro que muestra un listado frecuencia vs volumen. Cada modal tiene filtros y una tabla que se llena dinámicamente a través de JavaScript.

### Catálogo de Funciones y Clases
- `closeModal(modalId)` - Cierra el modal especificado.
- `filterAlerts()` - Filtra las alertas según los criterios de búsqueda y selección.
- `filterCombos()` - Filtra los combos según los criterios de búsqueda.
- `filterScatter()` - Filtra el listado frecuencia vs volumen según los criterios de búsqueda y selección.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
No depende de ninguna librería externa ni comunica con otros archivos del proyecto.


---

## Archivo: ./templates/partials/_deliveries_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para varios modales que probablemente se utilizan en una interfaz web para mostrar detalles específicos sobre entregas, actividades de usuarios, desglose de ubicaciones y movimientos no paletizados.

### Catálogo de Funciones y Clases
- `toggleModalFilter(filterType, isMonth)` - Alterna el filtro del modal según el tipo (area o weekday) y si se selecciona el mes actual.
- `closeModal(modalId)` - Cierra el modal con el ID especificado.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- `jQuery` (usado para manipular el DOM)
- `FontAwesome` (usado para iconos)

Flujo: Este archivo no interactúa directamente con otros archivos del proyecto, solo proporciona estructura HTML y JavaScript básico para los modales.


---

## Archivo: ./templates/partials/_edit_query_modal.html

### Resumen Funcional
Este archivo contiene el código HTML para un modal de edición de consultas en Analytics Studio, que incluye un constructor visual interactivo y una vista previa del gráfico resultante.

### Catálogo de Funciones y Clases
No se detectaron funciones o clases definidas explícitamente en este fragmento de código.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directamente mencionadas.
- **Flujo**: El archivo se comunica con el backend a través de funciones JavaScript que interactúan con elementos del DOM, como `onBaseTableChange`, `addJoin`, `addFilter`, etc.


---

## Archivo: ./templates/partials/_inventory_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para varios modales de interfaz de usuario, cada uno con un título y una lista desordenada (`<ul>`) que se llena dinámicamente a través de JavaScript. Los modales son utilizados para mostrar información detallada sobre diferentes aspectos del inventario, como el consumo específico, actividad del asistente, materiales más movimientos, desglose de ubicación, curva ABC, días de la semana y producción vs mantenimiento.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo. Todas las interacciones son realizadas a través de HTML y JavaScript.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías externas utilizadas**: No se detectan librerías externas específicas.
- **Flujo hacia otros archivos del proyecto**: Este archivo no comunica directamente con otros archivos del proyecto. Las interacciones son internas a la interfaz de usuario y se realizan mediante JavaScript para cargar dinámicamente los datos en las listas desordenadas (`<ul>`).


---

## Archivo: ./templates/partials/_logout.html

### Resumen Funcional
Este fragmento de código HTML contiene un script que define una función `logout` asíncrona. La función se encarga de cerrar la sesión del usuario, notificando al backend y limpiando el almacenamiento local.

### Catálogo de Funciones y Clases
- `logout()` - Realiza el proceso de cierre de sesión.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales, de sesión o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- **Librerías externas utilizadas**: `fetch` (API web para hacer solicitudes HTTP).
- **Flujo hacia otros archivos del proyecto**: No se comunica con otros archivos específicos dentro del proyecto.


---

## Archivo: ./templates/partials/_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para dos modales: uno que muestra un visor de PDF y otro que presenta una tabla de usuarios y sus áreas asignadas.

### Catálogo de Funciones y Clases
No se detectan funciones ni clases definidas en este archivo.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `autores_map`: Una variable global o diccionario que contiene la información de los autores y sus áreas asignadas. Se utiliza para llenar la tabla en el modal "Tabla de usuarios y sus areas".

### Dependencias y Flujo
No se detectan dependencias externas ni llamadas a otros archivos del proyecto.


---

## Archivo: ./templates/partials/_quick_login_modal.html

### Resumen Funcional
El archivo `_quick_login_modal.html` define un modal de inicio rápido para la sesión, que permite a los usuarios iniciar sesión sin perder sus filtros actuales. El formulario envía las credenciales al servidor y maneja la respuesta para actualizar el estado del usuario en el almacenamiento local o recargar la página según sea necesario.

### Catálogo de Funciones y Clases
- `handleQuickLogin(event)` - Maneja el evento de envío del formulario de inicio rápido, realiza una solicitud POST a la API de autenticación y actualiza el estado del usuario según la respuesta.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: No se utilizan librerías externas.
- **Flujo Interno**: El archivo interactúa con el servidor a través de una solicitud POST al endpoint `/api/auth/login`. La respuesta del servidor se utiliza para actualizar el estado del usuario en el almacenamiento local (`localStorage`) y para determinar si la página debe recargarse o no.


---

## Archivo: ./templates/partials/_scripts.html

### Resumen Funcional
Este archivo contiene fragmentos de HTML que incluyen scripts para Chart.js, modales rápidos de inicio de sesión y cierre, así como lógica empresarial y ayudantes de interfaz de usuario para el panel de control.

### Catálogo de Funciones y Clases
No se detectaron funciones o métodos específicos en este fragmento de HTML. Solo se incluyen referencias a scripts externos.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: Chart.js (https://cdn.jsdelivr.net/npm/chart.js)
- **Archivos Internos**: 
  - `partials/_quick_login_modal.html`
  - `partials/_logout.html`
  - `js/core_ui.js` (versión 1)
  - `js/dashboard.js` (versión 7)

Este fragmento de HTML se encarga principalmente de incluir scripts y modales que son utilizados en diferentes partes del proyecto, pero no realiza ninguna operación específica relacionada con la base de datos o el estado global.


---

## Archivo: ./templates/partials/_sidebar.html

### Resumen Funcional
Este archivo contiene el código HTML para un panel lateral que incluye varios filtros y controles de búsqueda para una interfaz web. Permite filtrar por fecha, área, centro, estado OT (Estado WMS), buscar por número de OT o entrega, incluir un logo específico, y descargar reportes consolidados en formato PDF.

### Catálogo de Funciones y Clases
- `toggleSidebar()` - Cierra el panel lateral.
- `toggleMulti(id)` - Muestra u oculta los checkboxes dentro del multiselect.
- `toggleSelectAll(group, checked)` - Selecciona/deselecciona todos los checkboxes en un grupo.
- `handleSmartCheckbox(checkbox, group, allCheckboxId, table)` - Maneja el cambio de estado de los checkboxes inteligentes.
- `applyCentroFilter(value)` - Aplica el filtro por centro seleccionado.
- `applyFilters()` - Aplica los filtros según las selecciones del usuario.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- JavaScript (funciones como `toggleSidebar`, `toggleMulti`, etc.)
- Jinja2 templating (para iterar sobre variables como `dates` y `areas`)

Flujo: Este archivo se comunica con otros archivos JavaScript para manejar eventos de usuario, actualizar el estado del filtro y generar reportes.


---

## Archivo: ./templates/partials/_styles.html

### Resumen Funcional
El archivo `_styles.html` contiene estilos CSS para una interfaz web, definiendo colores, layout y animaciones.

### Catálogo de Funciones y Clases
No aplica

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
No aplica


---

## Archivo: ./templates/partials/_tab_deliveries.html

### Resumen Funcional
Este fragmento HTML muestra una pestaña de análisis de entregas con gráficos y KPIs, permitiendo a los usuarios cambiar entre vistas operativas y históricas. Incluye estadísticas como volumen total, eficiencia de bodega, entregadas a tiempo y atrasadas, así como gráficos interactivos para visualizar la evolución mensual y semanal del cumplimiento SLA.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML. Todas las interacciones son realizadas mediante JavaScript y eventos del DOM.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `kpi_total`: Volumen total de entregas (Año).
- `kpi_eff`: Eficiencia de bodega (%).
- `kpi_ontime`: Entregadas a tiempo.
- `kpi_late`: Entregadas atrasadas.
- `areas_vl`: Lista de áreas seleccionadas para el filtrado.
- `top_authors`: Top solicitadores con sus entregas y áreas.
- `top_materials`: Ranking de materiales repetitivos por área.

### Dependencias y Flujo
Dependencias:
- Font Awesome (para íconos).
- JavaScript (para interactividad).

Flujo:
Este fragmento interactúa con el backend a través de funciones JavaScript que pueden abrir modales para editar consultas SQL, cambiar vistas, filtrar datos, y actualizar gráficos. No realiza llamadas directas a una base de datos ni depende de variables globales definidas en otros archivos del proyecto.


---

## Archivo: ./templates/partials/_tab_docs.html

### Resumen Funcional
Este fragmento HTML es una pestaña de interfaz de usuario que muestra la estructura del proyecto y permite explorar los archivos de documentación. Incluye un panel lateral para navegar por el árbol de documentos y una sección principal donde se visualiza el contenido seleccionado.

### Catálogo de Funciones y Clases
No aplica

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas mencionadas.
- **Flujo**: Este fragmento no interactúa con otros archivos del proyecto ni realiza llamadas a funciones. Es una vista estática que muestra la estructura del proyecto y permite seleccionar archivos para visualizar su contenido.


---

## Archivo: ./templates/partials/_tab_historial.html

### Resumen Funcional
Este fragmento HTML es una pestaña que muestra el historial de ubicaciones de un material. Permite a los usuarios buscar un material y ver su stock actual y su historial de ubicaciones anteriores.

### Catálogo de Funciones y Clases
No se detectan funciones ni clases definidas en este fragmento HTML.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías externas utilizadas**: `FontAwesome` (referenciado por `<i class="fas fa-cog"></i>`).
- **Flujo hacia otros archivos del proyecto**: No se detecta interacción con otros archivos específicos dentro del proyecto.


---

## Archivo: ./templates/partials/_tab_ia.html

### Resumen Funcional
Este fragmento HTML es una pestaña que muestra información sobre el análisis de IA, incluyendo semáforos de desplanificación y cuadrantes de frecuencia vs volumen. Muestra alertas de materiales con alta probabilidad de solicitud inminente y combos frecuentes.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `error_msg`: Variable global que almacena un mensaje de error si ocurre algún problema.
- `alerts`: Lista de alertas que se muestran en el semáforo de desplanificación.
- `combos`: Lista de combos frecuentes que se muestran en la sección de Market Basket.

### Dependencias y Flujo
- **Librerías externas**: No se detectan librerías externas utilizadas específicamente en este fragmento HTML.
- **Flujo hacia otros archivos**: Este fragmento interactúa con JavaScript a través de funciones como `openEditQueryModal`, `openModalAlerts`, y `openModalScatter`.


---

## Archivo: ./templates/partials/_tab_inventory.html

### Resumen Funcional
Este fragmento HTML es una pestaña que muestra un análisis de movimientos en una interfaz web, incluyendo estadísticas clave y gráficos interactivos. Permite a los usuarios cambiar la vista entre "Vista Operativa (Anual)" y "Vista Semanal (Histórico)", y proporciona detalles sobre diferentes KPIs como ingresos, consumos de producción, mantenimiento, tasa de reabastecimiento, traspasos, devoluciones y eficiencia de bodega. También incluye gráficos que muestran la distribución de materiales según la curva ABC, tendencias de consumo, volumen operacional y carga semanal.

### Catálogo de Funciones y Clases
- `switchInventarioView(value)` - Cambia la vista del inventario según el valor seleccionado.
- `openEditQueryModal(id, title)` - Abre un modal para editar una consulta SQL específica.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `user.role` - Rol del usuario actual.
- `kpi_ingresos`, `kpi_consumos_prod`, `kpi_consumos_mant`, `rate_reabast`, `kpi_traspasos`, `rate_devolucion`, `rate_eficiencia` - Valores de KPIs calculados.
- `top_materials_quick` - Lista de materiales más consumidos.
- `top_users` - Lista de usuarios con mayor frecuencia de despachos.

### Dependencias y Flujo
- Librerías utilizadas: `FontAwesome` para iconos.
- Comunicación con otros archivos del proyecto:
  - `_tab_inventory.js` (posiblemente contiene la lógica detrás de las funciones `switchInventarioView` y `openEditQueryModal`).


---

## Archivo: ./templates/partials/_tab_ots.html

### Resumen Funcional
Este fragmento HTML muestra una pestaña de gestión de Ordenes de Transporte (OTs) con estadísticas, gráficos y tablas interactivas. Permite filtrar y visualizar OTs pendientes, movimientos no paletizados y detalles específicos.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML.

### Interacción con Base de Datos
- **Motor:** No aplica (el código no contiene consultas SQL ni interacciones directas con una base de datos).
- **Tablas:** No aplica.
- **Columnas:** No aplica.

### Estado y Variables Globales
No se detectan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Librerías Externas:** `FontAwesome` para iconos.
- **Flujo Interno:** El fragmento interactúa con JavaScript a través de eventos como `onclick`, que llaman funciones como `openEditQueryModal`, `filterOTTable`, `switchSubTab`, etc. No se indica interacción directa con otros archivos del proyecto en este fragmento.


---

## Archivo: ./templates/partials/_table.html

### Resumen Funcional
Este fragmento HTML define una tabla para mostrar transacciones, con columnas para entrega/OT, fecha, items, área y estado. Incluye funcionalidades de ordenación y búsqueda.

### Catálogo de Funciones y Clases
- `sortTable(column)` - Ordena la tabla según la columna especificada.
- `filterTable()` - Filtra las filas de la tabla según los valores de entrada en los campos de búsqueda.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- JavaScript (`sortTable`, `filterTable`)
- CSS (estilos para la tabla y elementos)

Flujo: Este fragmento se comunica con el backend a través de formularios que envían solicitudes POST al endpoint `/generate-pdf` para generar y previsualizar/descargar PDFs.


---

## Archivo: ./templates/settings.html

### Resumen Funcional
El archivo `settings.html` es una página web que permite la gestión dinámica de parámetros globales del sistema, mapeos de estados de entrega y centros de costo a áreas de negocio, así como la sincronización de feriados. La interfaz presenta tablas interactivas para editar y guardar cambios en estos elementos.

### Catálogo de Funciones y Clases
- `openPasswordModal()` - Abre el modal para cambiar la contraseña.
- `closePasswordModal()` - Cierra el modal para cambiar la contraseña.
- `changePassword()` - Maneja el cambio de contraseña, validando los campos y haciendo una solicitud a la API.
- `updateSetting(key)` - Actualiza un parámetro global en la base de datos.
- `updateStatus(code)` - Actualiza un mapeo de estado de entrega en la base de datos.
- `addStatus()` - Añade un nuevo mapeo de estado de entrega a la base de datos.
- `deleteStatus(code)` - Elimina un mapeo de estado de entrega de la base de datos.
- `updateCostCenter(code)` - Actualiza un mapeo de centro de costo a área de negocio en la base de datos.
- `addCostCenter()` - Añade un nuevo mapeo de centro de costo a área de negocio a la base de datos.
- `deleteCostCenter(code)` - Elimina un mapeo de centro de costo a área de negocio de la base de datos.
- `syncHolidays()` - Sincroniza los feriados nacionales de Chile para el año actual y el próximo.
- `addHoliday()` - Añade una nueva fecha de feriado manualmente.
- `deleteHoliday(date_str)` - Elimina una fecha de feriado de la base de datos.
- `updateQuery(id)` - No se menciona en el código proporcionado.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- `fetch` para hacer solicitudes HTTP a la API.
- `apiCall(url, method, data = null)` - Función auxiliar para manejar las solicitudes HTTP.

Flujo:
- La página interactúa con el backend a través de endpoints como `/api/auth/change-password`, `/api/settings/update`, `/api/settings/status`, etc., para realizar operaciones CRUD en los parámetros globales, mapeos y feriados.


---

## Archivo: ./templates/sla_table.html

### Resumen Funcional
El archivo `sla_table.html` es una plantilla HTML para mostrar una tabla de transacciones que cumplen con ciertos criterios, incluyendo detalles como el número de entrega, autor/creador, área de negocio, días de retraso, fecha de creación y salida de mercancias. La página también proporciona opciones para generar y descargar PDFs relacionados con cada transacción.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo HTML.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías externas utilizadas**: No hay librerías externas directamente importadas.
- **Flujo hacia otros archivos del proyecto**:
  - `partials/_styles.html`: Incluye estilos CSS adicionales.
  - `static/css/sla_table.css`: Archivo de estilo específico para esta página.
  - `partials/_modals.html`: Incluye modales adicionales.
  - `js/sla_table.js`: Script JavaScript asociado a esta página.

El archivo HTML interactúa con el backend a través de formularios que envían solicitudes POST a rutas como `/generate-pdf`, lo que implica que el backend debe manejar estas solicitudes para generar y devolver PDFs.


---

## Archivo: ./test_deliveries.py

### Resumen Funcional
El archivo `test_deliveries.py` es un script de prueba que interactúa con una base de datos para obtener y mostrar el contexto completo de entregas.

### Catálogo de Funciones y Clases
- `svc.get_full_context()` - Obtiene el contexto completo de entregas.

### Interacción con Base de Datos
- **Motor:** No especificado.
- **Tablas:** No aplica.
- **Columnas:** No aplica.
- **Consultas SQL Crudas/ORM:** Sí, utiliza `DeliveriesService` que probablemente realiza consultas a la base de datos.

### Estado y Variables Globales
- `db` - Variable global que almacena una instancia de la sesión de la base de datos.

### Dependencias y Flujo
- **Librerías Externas:** `sys`, `logging`.
- **Flujo Interno:** El script crea una instancia de `DeliveriesService`, obtiene el contexto completo de entregas, e imprime las claves del contexto. Si ocurre un error, se imprime la traza de excepción.

### Notas Adicionales
El archivo no realiza ninguna interacción directa con tablas o columnas específicas en la base de datos; en su lugar, utiliza un servicio para obtener el contexto completo de entregas.


---

## Archivo: ./tests/conftest.py

### Resumen Funcional
Este archivo `conftest.py` es un archivo de configuración para pruebas unitarias en un proyecto FastAPI. Define varias funciones y variables globales que se utilizan para configurar el entorno de prueba, incluyendo la creación de una base de datos SQLite en memoria compartida y la autenticación del usuario administrador.

### Catálogo de Funciones y Clases
- `TEST_SESSION_ID(secrets.token_hex(16))` - Genera un identificador único para evitar colisiones entre sesiones de prueba.
- `session_db()` - Crea e inicializa una base de datos SQLite en memoria compartida con esquema completo.
- `test_db(session_db)` - Proporciona aislamiento de datos entre pruebas individuales, vaciando las tablas antes de cada ejecución.
- `client(test_db)` - Configura un cliente de pruebas de FastAPI para interactuar con la base de datos de sesión.
- `auth_client(client)` - Proporciona un cliente pre-autenticado con el token del usuario administrador.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:**
  - `outbound_deliveries`
  - `inventory_movements`
  - `stock_levels`
  - `warehouse_tasks`
  - `autor_area_mapping`
  - `analytics_snapshots`
  - `auth_users`

### Estado y Variables Globales
- `TEST_SESSION_ID`: Identificador único para evitar colisiones entre sesiones de prueba.
- `MEMORY_DB_URI`: URI de la base de datos SQLite en memoria compartida.

### Dependencias y Flujo
- **Librerías Externas:** `secrets`, `pathlib`, `sqlite3`, `unittest.mock`, `pytest`, `fastapi.testclient`
- **Flujo Interno:** El archivo configura el entorno de prueba, incluyendo la creación de una base de datos SQLite en memoria compartida y la autenticación del usuario administrador.


---

## Archivo: ./tests/test_api.py

### Resumen Funcional
Este archivo contiene pruebas unitarias utilizando `pytest` para verificar el funcionamiento de varios endpoints y funcionalidades del sistema. Las pruebas cubren la lectura de un dashboard principal, la obtención de una URL de túnel, la iniciación de un proceso de sincronización, el acceso a una página de analíticas, la generación de consultas SQL para métricas SLA, y la resolución dinámica de áreas de negocio en rutas de auditoría.

### Catálogo de Funciones y Clases
- `test_read_root(auth_client)` - Verifica que el dashboard principal responda con el título correcto.
- `test_get_tunnel_url(auth_client, tmp_path)` - Verifica que el endpoint `/url` devuelva la dirección del túnel ngrok.
- `test_post_sync_endpoint(auth_client)` - Verifica que el endpoint de sincronización inicie el pipeline correctamente.
- `test_analytics_page_access(auth_client)` - Verifica que la página de analíticas sea accesible.
- `test_build_sql_sla_efficiency(auth_client)` - Verifica que el generador de consultas SQL compile correctamente la métrica SLA_EFFICIENCY con desgloses y filtros.
- `test_analytics_sla_route(auth_client, test_db)` - Verifica que la ruta de auditoría SLA resuelva dinámicamente las áreas de negocio y que no muestre 'OTRO'.

### Interacción con Base de Datos
- Motor: No aplica (No hay interacción directa con bases de datos en este archivo).
- Tablas: `outbound_deliveries`
- Columnas: `entrega`, `fecha_carga`, `ubicacion_area`, `area_negocio`, `dias_retraso`

### Estado y Variables Globales
- No aplica (No hay variables globales definidas en este archivo).

### Dependencias y Flujo
- Librerías externas utilizadas: `pytest`, `unittest.mock`.
- Comunicación con otros archivos del proyecto:
  - `core.state.AppState`
  - `routes.sync.TUNNEL_URL_FILE`
  - `routes.sync._run_sync_pipeline`
  - `routes.sync.task_manager`


---

## Archivo: ./tests/test_auth.py

### Resumen Funcional
Este archivo contiene pruebas unitarias para el módulo de autenticación JWT en una aplicación FastAPI, cubriendo casos como inicio de sesión exitoso y no exitoso, consulta del perfil de usuario, registro de nuevos usuarios y listado de usuarios.

### Catálogo de Funciones y Clases
- `test_login_page_renders(client)` - Verifica que la página de login sea accesible.
- `test_login_success(client)` - Verifica login exitoso con credenciales del admin por defecto.
- `test_login_wrong_password(client)` - Verifica que credenciales incorrectas retornen 401.
- `test_me_endpoint_without_token(client)` - Verifica que /me sin token retorne 401.
- `test_me_endpoint_with_token(client)` - Verifica que /me con token válido retorne el perfil del usuario.
- `test_register_requires_admin(client)` - Verifica que registrar un usuario requiera token de admin.
- `test_register_and_login_new_user(client)` - Verifica el flujo completo: admin registra usuario → nuevo usuario hace login.
- `test_list_users_admin_only(client)` - Verifica que listar usuarios requiera rol admin.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías externas utilizadas**: `pytest`, `fastapi.testclient.TestClient`
- **Flujo hacia otros archivos del proyecto**: No se mencionan interacciones específicas con otros archivos.


---

## Archivo: ./tests/test_enrichment.py

### Resumen Funcional
El archivo `test_enrichment.py` contiene pruebas unitarias para verificar la funcionalidad de enriquecimiento de datos en una base de datos SQLite. Las pruebas cubren el aprendizaje de áreas por autor, el rellenado de entregas desde movimientos, el enriquecimiento de entregas con stock y la actualización del SLA basada en tareas de bodega.

### Catálogo de Funciones y Clases
- `db_with_data(test_db: sqlite3.Connection) -> sqlite3.Connection` - Prepara una base de datos con datos de prueba para los procesos de enriquecimiento.
- `test_learn_and_apply_author_logic(db_with_data: sqlite3.Connection) -> None` - Verifica que el sistema aprenda que USER_A pertenece a PRODUCCION y lo aplique.
- `test_backfill_from_movements(db_with_data: sqlite3.Connection) -> None` - Verifica que Entregas recupere el autor y centro de costo desde Movimientos.
- `test_enrichment_from_stock(db_with_data: sqlite3.Connection) -> None` - Verifica que se crucen las descripciones de material y ubicaciones desde el maestro de stock.
- `test_update_sla_with_tasks(db_with_data: sqlite3.Connection) -> None` - Verifica que el SLA se actualice correctamente usando las tareas de bodega.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQLite. Las tablas y columnas involucradas son:
- Tablas: `outbound_deliveries`, `inventory_movements`, `stock_levels`, `autor_area_mapping`, `warehouse_tasks`
- Columnas: `entrega`, `autor`, `area_negocio`, `material`, `usuario`, `ce_coste`, `referencia`, `denominacion`, `ubicacion_bin`, `stock_disp`, `umb`, `creado_el`, `fecha_sm_real`, `dias_retraso`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas: `pytest`, `sqlite3`
- Comunicación con otros archivos del proyecto: No se menciona comunicación explícita con otros archivos, pero las funciones interactúan con módulos como `db_enrichment.py` que no están incluidos en el fragmento de código proporcionado.


---

## Archivo: ./tests/test_maintenance.py

### Resumen Funcional
El archivo `test_maintenance.py` contiene pruebas unitarias para verificar el comportamiento de dos funciones: `quit_app` y `should_process`. La función `quit_app` intenta cerrar una aplicación utilizando un comando de sistema, mientras que `should_process` determina si un archivo debe ser procesado en función de su nombre y ruta.

### Catálogo de Funciones y Clases
- `test_quit_app_success()` - Verifica que la función `quit_app` retorne True cuando el comando de sistema tiene éxito.
- `test_quit_app_failure()` - Verifica que la función `quit_app` retorne False cuando ocurre un error de proceso o excepción.
- `test_doc_generator_filtering_logic(filename: str, filepath: str, expected: bool)` - Prueba la lógica de exclusión de archivos en el generador de documentación.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- `pytest` - Framework para pruebas unitarias.
- `subprocess` - Módulo para ejecutar comandos del sistema.
- `unittest.mock` - Módulo para crear objetos simulados (mocks).
- `scripts.free_ram.quit_app` - Función que intenta cerrar una aplicación.
- `scripts.doc_generator.should_process` - Función que determina si un archivo debe ser procesado.


---

## Archivo: ./tests/test_pdf.py

### Resumen Funcional
Este archivo contiene pruebas unitarias para validar la funcionalidad del módulo `pdf_engine` que se encarga de generar documentos PDF en formato Landscape utilizando la orientación de papel Letter. Las pruebas cubren la creación de instancias de PDF, generación de códigos de barras, recuperación de órdenes de transporte (OTs) y el dibujo de páginas de entrega.

### Catálogo de Funciones y Clases
- `pdf_instance() -> WMS_Landscape_PDF` - Proporciona una instancia limpia de `WMS_Landscape_PDF`.
- `sample_header() -> pd.Series` - Genera datos de cabecera de entrega ficticios.
- `sample_items() -> pd.DataFrame` - Genera un listado de materiales ficticios para pruebas.
- `test_pdf_instantiation(pdf_instance: WMS_Landscape_PDF) -> None` - Verifica que la clase PDF se instancie con la orientación Landscape y dimensiones Letter.
- `test_barcode_generation(barcode_data: str) -> None` - Valida la generación de códigos de barras.
- `test_get_ots_logic() -> None` - Verifica la lógica de recuperación de OTs filtrando valores inválidos.
- `test_draw_delivery_page_generates_content(pdf_instance: WMS_Landscape_PDF, sample_header: pd.Series, sample_items: pd.DataFrame) -> None` - Valida que el motor de dibujo escriba contenido binario en el buffer del PDF.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas:
  - `get_ots_for_delivery("8000123", mock_conn)`:
    - Tabla: No especificada (mocked)
    - Columna: `numero_ot`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pytest`
  - `pandas`
  - `io`
  - `sqlite3`
  - `typing`
  - `unittest.mock`
- Comunicación con otros archivos del proyecto:
  - `core.pdf_engine` (clases y funciones)


---

## Archivo: ./tests/test_pipeline.py

### Resumen Funcional
El archivo `test_pipeline.py` contiene pruebas unitarias para el módulo de consolidación de datos, utilizando la biblioteca `pytest`. Las pruebas cubren la funcionalidad de análisis de fechas en archivos, validación de nombres de tablas y lógica de sobrescritura de archivos más recientes.

### Catálogo de Funciones y Clases
- `test_parse_file_date(consolidator)` - Verifica que el parsing de fechas sea correcto.
- `test_validate_table_security(consolidator)` - Verifica la protección contra nombres de tabla no permitidos.
- `test_overwrite_with_latest_logic(consolidator, tmp_path)` - Verifica que se tome el archivo más reciente para sobrescribir.

### Interacción con Base de Datos
- Motor: No aplica (No hay interacción directa con bases de datos).
- Tablas: No aplica (No hay consultas SQL crudas o llamadas a ORM).
- Columnas: No aplica (No se manipulan columnas específicas).

### Estado y Variables Globales
- No aplica (No se definen variables globales, de sesión, de entorno o diccionarios quemados en código que almacenen estado crítico).

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pytest`
  - `pathlib`
  - `datetime`
  - `pandas`
- Comunicación con otros archivos del proyecto:
  - `db.consolidator.DataConsolidator` (fixture)
  - `services.etl.OutboundDeliveryAdapter.read_and_clean_data` (mockeado)


---

## Archivo: ./tests/test_queries.py

### Resumen Funcional
El archivo `test_queries.py` contiene pruebas unitarias para funciones que interactúan con una base de datos SQLite, específicamente para contar días activos y calcular estadísticas por área de negocio.

### Catálogo de Funciones y Clases
- `test_get_total_active_days(test_db: sqlite3.Connection) -> None`: Verifica el conteo de días únicos con actividad filtrado por año usando fechas ISO.
- `test_get_total_active_days_empty(test_db: sqlite3.Connection) -> None`: Verifica que el conteo de días activos devuelva 0 cuando la tabla está vacía.
- `test_get_area_stats(test_db: sqlite3.Connection) -> None`: Verifica el cálculo de KPIs (ontime/late) agrupados por área de negocio.
- `test_area_expr_fallback_locations(test_db: sqlite3.Connection) -> None`: Verifica que el mapeo de área resuelva correctamente usando las columnas de fallback.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: `outbound_deliveries`
- **Columnas**:
  - `entrega`
  - `fecha_carga`
  - `area_negocio`
  - `dias_retraso`
  - `ubicacion_area`
  - `ubicacion_bin_1`
  - `ubicacion_bin`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- **Librerías Externas**: `pytest`, `sqlite3`, `pandas`
- **Flujo Interno**: El archivo interactúa con el módulo `core.queries_deliveries` para ejecutar consultas y validar resultados.


---

## Archivo: ./tests/test_services.py

### Resumen Funcional
El archivo `test_services.py` contiene pruebas unitarias para funciones y clases relacionadas con servicios de túnel y gestión del estado de la aplicación.

### Catálogo de Funciones y Clases
- `app_state()` - Proporciona una instancia limpia de AppState configurada con un límite de caché.
- `cleanup_tunnel()` - Garantiza la limpieza del estado global del túnel tras cada test.
- `test_state_cache_respects_limits(app_state: AppState)` - Verifica que el gestor de estado respete los límites de memoria.
- `test_state_sync_flag_reactivity(app_state: AppState)` - Valida que la propiedad reactiva de sincronización cambie su estado de forma consistente.
- `test_start_tunnel_manages_singleton_instance(mock_access, mock_exists, mock_popen)` - Verifica que start_tunnel inicialice correctamente el servicio de túnel.
- `test_stop_tunnel_releases_global_reference(mock_run)` - Valida que stop_tunnel limpie las referencias globales de forma segura.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías externas utilizadas**: `pytest`, `unittest.mock`
- **Flujo hacia otros archivos del proyecto**: Se comunica con `services.tunnel` para iniciar y detener servicios de túnel, y con `core.state` para gestionar el estado de la aplicación.


---

## Archivo: ./tests/test_ui_smoke.py

### Resumen Funcional
Este archivo contiene pruebas de humo (smoke tests) para verificar la presencia de componentes UI críticos en diferentes endpoints de una aplicación web. Las pruebas aseguran que los servidores respondan correctamente y que el HTML contenga los IDs necesarios para la inicialización de scripts frontend.

### Catálogo de Funciones y Clases
- `test_ui_smoke_components_presence(auth_client, path: str, markers: List[Tuple[str, str]])` - Prueba de humo parametrizada que verifica la presencia de componentes visuales críticos en diferentes endpoints.
- `test_ui_smoke_error_handling(client)` - Verifica que el servidor maneje correctamente las peticiones a rutas inexistentes.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías externas utilizadas**: `pytest`, `typing`
- **Flujo**: El archivo interactúa con un cliente autenticado (`auth_client`) para realizar peticiones a diferentes endpoints y verifica la presencia de componentes UI específicos en el HTML de las respuestas. También interactúa con un cliente no autenticado (`client`) para verificar el manejo de rutas inexistentes.


---

## Archivo: ./tests/test_utils.py

### Resumen Funcional
El archivo `test_utils.py` contiene pruebas unitarias para verificar el comportamiento seguro e idempotente del registro de manejadores de señales en una aplicación.

### Catálogo de Funciones y Clases
- `test_setup_signal_handlers_safety()` - Verifica que el registro de manejadores de señales sea seguro e idempotente, asegurando que llamadas repetidas no provoquen excepciones en el sistema de señales.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- `pytest` - Framework para pruebas unitarias.
- `core.utils.setup_signal_handlers()` - Función que se prueba.


---

