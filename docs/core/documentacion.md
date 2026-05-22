# Documentación Técnica - Directorio: core
Compilado el: 2026-05-22 16:53:13
Modelo: qwen2.5-coder:7b | Separado por Carpetas

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
El archivo `auth.py` proporciona funcionalidades de autenticación y seguridad utilizando JSON Web Tokens (JWT) y OAuth2, con soporte para roles de usuario ('admin' y 'viewer'). Incluye funciones para crear tokens, verificar usuarios, manejar dependencias FastAPI para proteger endpoints y gestionar la base de datos de usuarios.

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
- Motor: No aplica (No hay consultas SQL crudas o llamadas a ORM).
- Tablas: `User`
- Columnas: `id`, `username`, `password_hash`, `role`, `is_active`, `created_at`

### Estado y Variables Globales
- `SECRET_KEY`: Clave secreta para firmar JWT.
- `ALGORITHM`: Algoritmo de firma para JWT.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración del token JWT.

### Dependencias y Flujo
- Librerías externas: `bcrypt`, `jwt`, `fastapi`.
- Comunicaciones internas: No aplica (No se comunica con otros archivos del proyecto).


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
Este archivo `db_config_manager.py` es el administrador de configuraciones dinámicas SaaS. Se encarga de la inicialización, carga y mantenimiento de tablas en una base de datos utilizando SQLAlchemy, así como la inserción de valores por defecto si las tablas están vacías.

### Catálogo de Funciones y Clases
- `init_config_db()` - Crea las tablas de configuración SaaS via SQLAlchemy si no existen.
- `seed_initial_config()` - Inserta los valores por defecto si las tablas están vacías.

### Interacción con Base de Datos
- Motor: SQLAlchemy
- Tablas:
  - `StatusMapping`
  - `CostCenterMapping`
  - `AppSetting`
  - `Holiday`
  - `ConfigQuery`
- Columnas:
  - `StatusMapping.code`, `label`
  - `CostCenterMapping.center_code`, `business_area`
  - `AppSetting.key`, `value`, `type`
  - `Holiday.date_str`
  - `ConfigQuery.query_id`, `sql_text`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: SQLAlchemy, logging
- Comunicación con otros archivos del proyecto:
  - `database.py` (para obtener el motor de base de datos y la sesión)
  - `models.py` (para definir las clases de modelos)

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `db_config_manager.py` contiene configuraciones de consultas SQL y funciones para cargar estas configuraciones en una sesión de base de datos. También incluye funciones públicas para obtener diferentes tipos de configuración desde la base de datos.

### Catálogo de Funciones y Clases
- `ConfigQuery(query_id, sql_text, visual_state)` - Define una consulta con un ID único, texto SQL y estado visual.
- `initial_queries` - Lista de instancias de `ConfigQuery`.
- `load_config_to_memory(session=None)` - Carga las consultas iniciales en la sesión de base de datos. Esta función está obsoleta y no realiza ninguna operación.
- `_ensure_loaded()` - Función interna que no hace nada.
- `get_setting(key, default=None)` - Obtiene un valor de configuración basado en una clave, con un valor predeterminado opcional.
- `get_status_mapping()` - Devuelve un mapeo de códigos de estado a etiquetas.
- `get_cost_center_mapping()` - Devuelve un mapeo de códigos de centro de costo a áreas de negocio.
- `get_holidays()` - Devuelve una lista de fechas festivas.
- `get_query(query_id)` - Obtiene el texto SQL de una consulta basada en su ID.

### Interacción con Base de Datos
- Motor: No especificado (se infiere que es SQLAlchemy).
- Tablas:
  - `inventory_movements`
  - `warehouse_tasks`
  - `AppSetting`
  - `StatusMapping`
  - `CostCenterMapping`
  - `Holiday`
- Columnas:
  - `inventory_movements.cmv`, `inventory_movements.fe_contab`, `inventory_movements.material`, `inventory_movements.tipo_operacion`, `inventory_movements.registrado`
  - `warehouse_tasks.usuario`, `warehouse_tasks.fe_creac`, `warehouse_tasks.fecha_conf`
  - `AppSetting.key`, `AppSetting.typed_value()`
  - `StatusMapping.code`, `StatusMapping.label`
  - `CostCenterMapping.center_code`, `CostCenterMapping.business_area`
  - `Holiday.date_str`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas: SQLAlchemy.
- Comunicación con otros archivos del proyecto:
  - No se menciona ninguna comunicación específica entre este archivo y otros.


---

## Archivo: ./core/models.py

### Resumen Funcional
Este archivo define modelos ORM SQLAlchemy para el esquema de configuración SaaS, incluyendo mapeos de estados WMS, centros de costo, parámetros globales, feriados y consultas SQL gestionadas via UI.

### Catálogo de Funciones y Clases
- `StatusMapping(code: str, label: str)` - Mapea códigos internos del WMS a etiquetas legibles por humanos.
- `CostCenterMapping(center_code: str, business_area: str)` - Asocia un código de centro de costo del WMS con un Área de Negocio.
- `AppSetting(key: str, value: str, type: str = "str")` - Parámetros de comportamiento del sistema.
  - `typed_value()` - Retorna el valor con el tipo Python correcto.
- `Holiday(date_str: str)` - Días no hábiles para el cálculo de SLA (días de retraso).
- `ConfigQuery(query_id: str, sql_text: str, visual_state: str = None)` - Almacena queries SQL nombradas para el dominio de inventario/entregas.

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
Este archivo contiene utilidades transversales y gestión de señales del sistema. Incluye funciones para configurar manejadores de señales, registrar mensajes de inicio y limpiar datos para su serialización JSON segura.

### Catálogo de Funciones y Clases
- `setup_signal_handlers()` - Configura los manejadores de señales (SIGINT, SIGTERM) para un cierre limpio.
- `log_startup_banner()` - Registra un mensaje de inicio del módulo de utilidades del sistema.
- `sanitize_for_json(data: Any) -> Any` - Limpia datos para su serialización JSON segura.
- `_get_bound_params_from_visual_state(visual_state_str: str) -> list` - Extrae parámetros limitados desde una cadena de estado visual.
- `_extract_metric_value(df, active_year: str = None) -> Any` - Extrae el valor numérico de la métrica de un DataFrame de forma segura.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `_handlers_registered` (boolean): Flag interno para evitar registros múltiples de manejadores de señales.

### Dependencias y Flujo
- `signal`: Para manejar señales del sistema.
- `sys`: Para salir del programa.
- `logging`: Para registrar mensajes.
- `pandas`: Para manipular datos en formato DataFrame.
- `math`: Para manejar valores numéricos especiales (NaN, Inf).
- `typing.Final`, `typing.Any`: Para anotaciones de tipos.


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
Este archivo contiene funciones utilitarias vectorizadas para transformación de datos WMS, incluyendo limpieza de datos, mapeos de negocio, normalización y cálculos métricos.

### Catálogo de Funciones y Clases
- `sanitize_string(text: str) -> str` - Normaliza un string para usarlo como encabezado de columna.
- `map_wms_status(df: pd.DataFrame) -> pd.DataFrame` - Concatena columnas de estado y mapea al valor legible de negocio.
- `apply_cost_center_mapping(df: pd.DataFrame) -> pd.DataFrame` - Clasifica ubicaciones WMS en áreas de negocio de forma vectorizada.
- `normalize_date_columns(df: pd.DataFrame) -> pd.DataFrame` - Estandariza formatos de fecha WMS a dd-mm-yyyy de forma eficiente.
- `calculate_sla_delays(df: pd.DataFrame) -> pd.DataFrame` - Calcula días hábiles de retraso usando lógica vectorizada de NumPy.
- `generate_time_labels(df: pd.DataFrame) -> pd.DataFrame` - Genera etiquetas de semana ISO para visualización y analítica.
- `is_file_changed(session: Session, file_path: Path) -> bool` - Verifica si un archivo ha cambiado desde la última sincronización.
- `mark_file_processed(session: Session, file_path: Path, row_count: Optional[int] = None)` - Marca un archivo como procesado exitosamente en el manifiesto.

### Interacción con Base de Datos
- Motor: SQLAlchemy ORM
- Tablas:
  - `sync_manifest`
- Columnas:
  - `file_path`, `last_modified`, `file_size`, `processed_at`, `row_count`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: `re`, `logging`, `numpy`, `pandas`, `datetime`, `pathlib`, `typing`
- Comunicación con otros archivos del proyecto:
  - `core.wms_config`: Para mapeos de estado y centro de costo.
  - `core.db_config_manager`: Para obtener feriados.


---

