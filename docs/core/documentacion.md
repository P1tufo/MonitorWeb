# Documentación Técnica - Directorio: core
Compilado el: 2026-06-07 18:34:58
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./core/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./core/app_instance.py

### Resumen Funcional
Inicializa la instancia de la aplicación FastAPI con configuraciones específicas y establece el directorio para las plantillas Jinja2.

### Catálogo de Funciones y Clases
- `FastAPI()` - Crea una instancia de la aplicación FastAPI.
- `Jinja2Templates(directory=str(templates_path))` - Configura el motor de plantillas Jinja2 con el directorio especificado.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `app: FastAPI` - Instancia principal de la aplicación FastAPI.
- `templates_path: Path` - Ruta al directorio de las plantillas.
- `templates: Jinja2Templates` - Motor de plantillas configurado.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directamente importadas en este archivo.
- **Flujo de Datos**: Este archivo no consume ni produce datos. Es una configuración inicial para la aplicación FastAPI y el motor de plantillas Jinja2.


---

## Archivo: ./core/auth.py

### Resumen Funcional
Este archivo `auth.py` contiene las funcionalidades de autenticación y seguridad para el sistema de monitoreo de almacén (WMS). Implementa la gestión de usuarios, tokens JWT, roles de usuario y dependencias FastAPI para proteger endpoints.

### Catálogo de Funciones y Clases
- `hash_password(plain: str) -> str` - Genera un hash bcrypt del password.
- `verify_password(plain: str, hashed: str) -> bool` - Verifica un password contra su hash bcrypt.
- `create_access_token(username: str, role: str) -> tuple[str, int]` - Crea un JWT firmado con HS256.
- `decode_token(token: str) -> Optional[dict]` - Decodifica y valida un JWT. Retorna None si es inválido o expirado.
- `get_current_user(request: Request, token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_session_dep)) -> User` - Dependencia que extrae el usuario del token JWT.
- `require_auth(user: User = Depends(get_current_user)) -> User` - Dependencia que EXIGE un usuario autenticado (no invitado).
- `require_admin(user: User = Depends(require_auth)) -> User` - Dependencia que EXIGE rol de administrador. Lanza 403 si no tiene permisos.
- `init_auth_db()` - Crea las tablas de autenticación si no existen.
- `ensure_admin_exists()` - Crea el usuario admin por defecto si no existe ningún usuario.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `User` (columnas: id, username, password_hash, role, is_active, created_at)
- Consultas SQL crudas o llamadas a ORM: Sí, se usan consultas ORM para interactuar con la tabla `User`.

### Estado y Variables Globales
- Variables globales:
  - `SECRET_KEY`: Clave secreta para JWT.
  - `ALGORITHM`: Algoritmo de codificación JWT.
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración del token JWT.

### Dependencias y Flujo
- Librerías externas: `bcrypt`, `jwt`, `fastapi.security.OAuth2PasswordBearer`
- Archivos del proyecto que este archivo importa:
  - `core.database` (para `Base`, `engine`, `get_session_dep`)
  - `core.models_auth` (para `User`)
- Archivos del proyecto que importan a este archivo: Ninguno
- Flujo de datos: El flujo de datos pasa por las funciones de autenticación y seguridad, utilizando tokens JWT para la autenticación y roles para el control de acceso.


---

## Archivo: ./core/cache_decorator.py

### Resumen Funcional
El archivo `cache_decorator.py` contiene funciones y un decorador para implementar una caché multinivel en un sistema de monitoreo de almacén (WMS). El decorador permite almacenar y recuperar datos analíticos tanto en memoria como en una base de datos SQLite, utilizando un patrón de caché que prioriza la velocidad de acceso a los datos.

### Catálogo de Funciones y Clases
- `save_analytics_snapshot(session: Session, key: str, data: Dict[str, Any])` - Guarda una captura de las analíticas en la base de datos para carga instantánea.
- `load_analytics_snapshot(session: Session, key: str) -> Optional[Dict[str, Any]]` - Recupera la última captura de analíticas desde la base de datos.
- `analytics_cache(key_prefix: str)` - Decorador que implementa el patrón de caché multinivel (Memoria -> DB Snapshot -> Cálculo).

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - `analytics_snapshots`
    - Columnas:
      - `key` (TEXT, PRIMARY KEY)
      - `data` (TEXT)
      - `updated_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas: `json`, `logging`, `datetime`, `functools`, `typing`
- Archivos del proyecto que IMPORTA:
  - `core.state` (para `get_cache_manager`)
- Archivos del proyecto que IMPORTAN a este archivo:
  - Ninguno

**Flujo de Datos:**
1. **Entrada:** Llamada al método decorado con parámetros.
2. **Proceso:**
   - Verifica si existe una sesión (`self.session`).
   - Genera claves para caché en memoria y base de datos.
   - Intenta recuperar los datos desde la caché en memoria.
   - Si no está en caché, intenta recuperarlos desde el snapshot en la base de datos.
   - Si no están disponibles, ejecuta el cálculo completo del método decorado.
   - Almacena los resultados en la caché en memoria y en la base de datos si es un diccionario.
3. **Salida:** Devuelve los datos recuperados o calculados.

Este flujo asegura que los datos sean recuperados lo más rápido posible, utilizando el caché en memoria como primer recurso, seguido del snapshot en la base de datos, y finalmente ejecutando el cálculo completo si es necesario.


---

## Archivo: ./core/database.py

### Resumen Funcional
Este archivo define la fábrica de sesiones SQLAlchemy para el sistema de monitoreo de almacén (WMS). Proporciona funciones para obtener una sesión de base de datos y realizar un chequeo de salud de la base de datos.

### Catálogo de Funciones y Clases
- `get_session()` - Context manager que entrega una sesión SQLAlchemy, garantizando commit en éxito y rollback automático en excepción.
- `get_session_dep()` - Dependencia de FastAPI para inyección de sesiones en endpoints.
- `health_check()` - Verifica la conectividad con la base de datos. Retorna True si OK.

### Interacción con Base de Datos
- Motor de BD: SQLite (desarrollo local) y PostgreSQL (producción SaaS).
- Tablas: Ninguna (no se especifican tablas directamente en este archivo).
- Columnas: Ninguna (no se especifican columnas directamente en este archivo).

### Estado y Variables Globales
- `DATABASE_URL` - Variable de entorno que define la URL de la base de datos. Valor por defecto es SQLite local.
- `_connect_args` - Argumentos de conexión para SQLAlchemy, incluyendo `check_same_thread=False` para SQLite.

### Dependencias y Flujo
- Librerías externas: `sqlalchemy`, `logging`.
- Archivos del proyecto que importan a este archivo:
  - `config.py` (para `DB_PATH`)
- Archivos del proyecto que este archivo importa:
  - Ninguno

El flujo de datos es desde el archivo `database.py` hacia los endpoints de FastAPI que utilizan las dependencias `get_session_dep()` para obtener sesiones de base de datos.


---

## Archivo: ./core/db_config_manager.py

### Resumen Funcional
Este archivo gestiona la configuración dinámica del Sistema de Monitoreo de Almacén (WMS) en tiempo de ejecución, utilizando SQLAlchemy para interactuar con una base de datos SQLite. Incluye funciones para inicializar la base de datos, poblarla con valores por defecto y cargar la configuración en caché para un acceso rápido.

### Catálogo de Funciones y Clases
- `init_config_db()` - Crea las tablas de configuración SaaS via SQLAlchemy si no existen.
- `seed_initial_config()` - Inserta los valores por defecto si las tablas están vacías.
- `load_config_to_memory(session=None)` - Carga la configuración en caché (deprecated).
- `_ensure_loaded()` - No-op para compatibilidad hacia atrás.
- `get_setting(key: str, default: Any = None) -> Any` - Recupera un valor de configuración por clave.
- `get_status_mapping() -> Dict[str, str]` - Devuelve el mapeo de estados en formato diccionario.
- `get_cost_center_mapping() -> Dict[str, str]` - Devuelve el mapeo de centros de costo en formato diccionario.
- `get_holidays() -> List[str]` - Devuelve la lista de feriados.
- `get_query_visual_state(query_id: str) -> str` - Recupera el visual_state JSON de una consulta.
- `get_user_groups() -> Dict[str, List[str]]` - Devuelve un diccionario de grupos de usuarios.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - `app_setting`
  - `config_query`
  - `cost_center_mapping`
  - `holiday`
  - `status_mapping`
  - `user_group`
- Columnas:
  - `app_setting`: `key`, `value`, `type`
  - `config_query`: `query_id`, `visual_state`
  - `cost_center_mapping`: `center_code`, `business_area`
  - `holiday`: `date_str`
  - `status_mapping`: `code`, `label`
  - `user_group`: `group_name`, `users`

### Estado y Variables Globales
- No hay variables globales explícitas.

### Dependencias y Flujo
- Importa librerías internas del proyecto (`database.py`, `models.py`).
- No se importan archivos del proyecto que lo consuman.
- El flujo de datos es desde el archivo hacia la base de datos para lectura y escritura.


---

## Archivo: ./core/macros.py

### Resumen Funcional
El archivo `macros.py` centraliza reglas de negocio y macros SQL para ser utilizadas en múltiples capas de la aplicación, facilitando la expresión de lógicas complejas y reutilizables.

### Catálogo de Funciones y Clases
- `inject_macros(sql: str) -> str` - Inyecta todas las macros globales registradas en el string SQL proporcionado.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `AREA_EXPR` (Variable Global) - Expresión SQL que determina el área empresarial basada en los centros de costo o ubicaciones binarias.
- `EXCLUDED_USERS_INACTIVITY` (Variable Global) - Tupla con usuarios excluidos explícitamente de las métricas de inactividad.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directas.
- **Flujo de Datos**: El archivo no importa ni es importado por otros archivos dentro del proyecto. Es una capa central que puede ser utilizada por cualquier otro módulo que necesite inyectar macros SQL en sus consultas.

Este archivo actúa como un punto central para la gestión y reutilización de expresiones SQL complejas y lógicas de negocio, asegurando que estas puedan ser fácilmente aplicadas en diferentes partes de la aplicación sin duplicación de código.


---

## Archivo: ./core/models.py

### Resumen Funcional
Este archivo define los modelos ORM SQLAlchemy para las tablas de configuración dinámica del sistema WMS, incluyendo mapeos de estados, centros de costo, parámetros globales, feriados y consultas SQL gestionadas via UI.

### Catálogo de Funciones y Clases
- `StatusMapping(code: str, label: str)` - Mapea códigos internos del WMS a etiquetas legibles por humanos.
- `CostCenterMapping(center_code: str, business_area: str)` - Asocia un código de centro de costo con un Área de Negocio.
- `AppSetting(key: str, value: str, type: str = "str")` - Parámetros de comportamiento del sistema.
  - `typed_value()` - Retorna el valor con el tipo Python correcto.
- `Holiday(date_str: str)` - Días no hábiles para el cálculo de SLA.
- `ConfigQuery(query_id: str, visual_state: str = None)` - Almacena el estado visual de las consultas del Analytics Studio.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `config_status_mapping`
  - `config_cost_center_mapping`
  - `app_settings`
  - `config_holidays`
  - `config_queries`

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- Importa de `sqlalchemy` para definir los tipos de datos y ORM.
- Importa de `.database.Base` para la herencia de modelos.
- No importa a otros archivos del proyecto.


---

## Archivo: ./core/models_auth.py

### Resumen Funcional
Este archivo define el modelo ORM para los usuarios del sistema de autenticación, incluyendo campos como nombre de usuario, contraseña hash, rol y estado de actividad.

### Catálogo de Funciones y Clases
- `User` - Define la tabla de usuarios con sus atributos y métodos.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: `auth_users`
  - Columnas:
    - `id`: Entero, clave primaria, autoincremental.
    - `username`: Cadena (50 caracteres), único, no nulo, índice.
    - `password_hash`: Cadena (255 caracteres), no nula.
    - `role`: Cadena (20 caracteres), no nula, valor por defecto "viewer".
    - `is_active`: Booleano, valor por defecto True.
    - `created_at`: Fecha y hora UTC, valor por defecto la fecha actual.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- Importa: `Base` desde `core.database`.
- No importa a otros archivos del proyecto.
- Es consumido por los servicios de autenticación.


---

## Archivo: ./core/models_transaccional.py

### Resumen Funcional
Este archivo define modelos SQLAlchemy para representar tablas en una base de datos SQLite utilizada por el sistema de monitoreo de almacén (WMS). Cada clase corresponde a una tabla y contiene atributos que corresponden a las columnas de la tabla.

### Catálogo de Funciones y Clases
- `WarehouseTask` - Representa tareas en el almacén.
- `InventoryMovement` - Representa movimientos de inventario.
- `OutboundDelivery` - Representa entregas salientes.
- `StockLevel` - Representa niveles de stock.
- `Lx02Pendiente` - Representa pendientes de LX02.
- `SyncManifest` - Representa manifiestos de sincronización.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `warehouse_tasks`
  - `inventory_movements`
  - `outbound_deliveries`
  - `stock_levels`
  - `lx02_pendientes`
  - `sync_manifest`
- Columnas:
  - `warehouse_tasks`: `numero_ot`, `pos`, `material`, etc.
  - `inventory_movements`: `doc_mat`, `ej_mat`, `pos`, etc.
  - `outbound_deliveries`: `entrega`, `pos_`, `material`, etc.
  - `stock_levels`: `material`, `lote`, `alm_`, etc.
  - `lx02_pendientes`: `material`, `lote`, `alm_`, etc., `otcuanto`.
  - `sync_manifest`: `file_path`, `last_modified`, `file_size`, etc.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: SQLAlchemy, FastAPI.
- **Flujo de Datos**:
  - Archivos del proyecto que importan a este archivo: Ninguno.
  - Archivos del proyecto que este archivo importa: Ninguno.


---

## Archivo: ./core/pdf_engine.py

### Resumen Funcional
El archivo `pdf_engine.py` es un motor optimizado para la generación de documentos PDF en formato horizontal (landscape) para el sistema de monitoreo de almacén (WMS). Permite crear páginas de entrega que incluyen encabezados, información detallada, tablas de materiales y códigos de barras.

### Catálogo de Funciones y Clases
- `WMS_Landscape_PDF(FPDF)` - Clase base para reportes WMS en formato horizontal.
  - `__init__()`: Inicializa la clase con configuraciones específicas para PDFs horizontales.
  - `get_column_x(col: int) -> float`: Calcula la posición X de una columna específica.
  - `draw_dotted_line(x1: float, y: float, x2: float) -> None`: Dibuja una línea punteada sutil.

- `get_ots_for_delivery(entrega_id: str, conn: sqlite3.Connection) -> List[str]` - Consulta las OTs asociadas a una entrega.
  - Parámetros:
    - `entrega_id`: Identificador de la entrega.
    - `conn`: Conexión a la base de datos SQLite.
  - Retorna: Lista de números de OT.

- `_generate_barcode_stream(data: str, options: Optional[dict] = None) -> io.BytesIO` - Genera un código de barras en memoria (BytesIO).
  - Parámetros:
    - `data`: Datos a codificar en el código de barras.
    - `options`: Opciones adicionales para la generación del código de barras.
  - Retorna: Flujo de bytes con el código de barras.

- `draw_delivery_page(pdf: WMS_Landscape_PDF, header: pd.Series, items: pd.DataFrame, include_logo: bool = True, ots_list: Optional[List[str]] = None) -> None` - Dibuja una página de entrega completa.
  - Parámetros:
    - `pdf`: Instancia de la clase `WMS_Landscape_PDF`.
    - `header`: Encabezado de la entrega en formato pandas Series.
    - `items`: Tabla de materiales en formato pandas DataFrame.
    - `include_logo`: Indica si incluir el logo en el encabezado (opcional).
    - `ots_list`: Lista de números de OT (opcional).

- `_draw_page_header(pdf: WMS_Landscape_PDF, h: pd.Series, include_logo: bool)` - Dibuja el encabezado superior, logo y código de barras de la entrega.
  - Parámetros:
    - `pdf`: Instancia de la clase `WMS_Landscape_PDF`.
    - `h`: Encabezado de la entrega en formato pandas Series.
    - `include_logo`: Indica si incluir el logo en el encabezado.

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
- Motor de BD: SQLite
- Tablas y Columnas:
  - Tabla: `warehouse_tasks`
  - Columnas: `numero_ot`, `entrega`

### Estado y Variables Globales
- No hay variables globales declaradas explícitamente.

### Dependencias y Flujo
- Librerías externas:
  - `io`, `logging`, `sqlite3`, `datetime`, `pathlib`, `typing`, `numpy`, `pandas`, `barcode`, `FPDF`
- Archivos del proyecto que importan a este archivo (`pdf_engine.py`):
  - Ninguno
- Archivos del proyecto que este archivo importa:
  - `config`

Flujo de datos: El archivo se utiliza para generar PDFs, por lo tanto, consume datos desde la base de datos y genera flujos de bytes con los documentos PDF.


---

## Archivo: ./core/pdf_reports.py

### Resumen Funcional
Este archivo contiene la lógica para construir secciones complejas de PDFs en un sistema de monitoreo de almacén (WMS). Incluye funciones para formatear cantidades y dibujar tablas de anexos y listas de picking.

### Catálogo de Funciones y Clases
- `_parse_qty(val)` - Sanitiza y convierte a float valores de cantidad de WMS.
- `_fmt_qty(val)` - Formatea cantidades para mostrar en el PDF de forma legible.
- `draw_annex_table(pdf, grouped_data)` - Dibuja la tabla de índice (anexo) de entregas agrupadas.
- `draw_picking_list(pdf, picking_df)` - Dibuja la lista de picking desglosada por entrega pero con total consolidado.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: `datetime` (módulo estándar de Python).
- **Flujo**: Este archivo no importa ni es importado por otros archivos. Es una parte interna del módulo `core/pdf_reports.py`.


---

## Archivo: ./core/query_engine.py

### Resumen Funcional
Este archivo actúa como una fachada para el motor de SQL en un sistema de monitoreo de almacén (WMS). Proporciona funciones para construir consultas SQL a partir de payloads y validar identificadores.

### Catálogo de Funciones y Clases
- `build_sql_from_payload(payload)` - Construye una consulta SQL a partir del payload proporcionado.
- `extract_metric_value(metric_name, visual_state)` - Extrae el valor de una métrica específica del estado visual.
- `get_bound_params_from_visual_state(visual_state)` - Obtiene los parámetros limitados desde el estado visual.
- `validate_identifier(identifier)` - Valida un identificador según las reglas permitidas.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con la base de datos.

### Estado y Variables Globales
Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Dependencias Externas**: `core.query_builder`, `core.query_utils`, `core.query_validators`.
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno.
- **Archivos del Proyecto que Este Archivo Importa**: Ninguno.

El flujo de datos es simple: el archivo recibe payloads y estados visuales, los procesa y devuelve consultas SQL o valores de métricas según sea necesario.


---

## Archivo: ./core/query_utils.py

### Resumen Funcional
Este archivo contiene funciones utilitarias para el procesamiento de parámetros y métricas en un sistema de monitoreo de almacén (WMS). Las funciones extraen parámetros de estado visual y valores numéricos principales de DataFrames.

### Catálogo de Funciones y Clases
- `get_bound_params_from_visual_state(visual_state_str: str) -> list` - Extrae los bind params (?) de un visual_state JSON serializado.
- `extract_metric_value(df, active_year: Optional[str] = None)` - Extrae el valor numérico principal de un DataFrame de resultado de query.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: `json`
- **Flujo de Datos**:
  - `get_bound_params_from_visual_state` no consume ni produce datos externos.
  - `extract_metric_value` no consume ni produce datos externos.


---

## Archivo: ./core/query_validators.py

### Resumen Funcional
El archivo `query_validators.py` contiene funciones para validar identificadores (tablas y columnas) en el contexto de un sistema de monitoreo de almacén (WMS). Las funciones verifican si los nombres proporcionados están dentro de listas blancas predefinidas y, en caso de ser columnas, consultan la base de datos para asegurarse de su existencia.

### Catálogo de Funciones y Clases
- `validate_identifier(name: str, db: Session) -> bool` - Valida que un identificador (tabla o tabla.columna) pertenezca a la lista blanca. Si es una columna, consulta la base de datos para verificar su existencia.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna
- Columnas: Ninguna

### Estado y Variables Globales
- `ALLOWED_TABLES` - Conjunto inmutable de tablas permitidas.
- `ALLOWED_AGGREGATIONS` - Conjunto inmutable de agregaciones permitidas.
- `ALLOWED_GRANULARITIES` - Conjunto inmutable de granularidades permitidas.

### Dependencias y Flujo
- Librerías externas: `logging`, `typing`
- Archivos del proyecto que IMPORTA a este archivo:
  - `routes/settings.py`
  - `core/security.py`

Este archivo no importa archivos del proyecto, pero es consumido por otros archivos dentro del proyecto.


---

## Archivo: ./core/schemas.py

### Resumen Funcional
Este archivo define esquemas de datos (schemas) utilizando Pydantic para la validación y serialización de objetos en un sistema de monitoreo de almacén (WMS). Los esquemas incluyen respuestas para diferentes tipos de análisis y definiciones para consultas visuales.

### Catálogo de Funciones y Clases
- `DashboardResponse(data: Dict[str, Any], is_syncing: bool)` - Define la estructura de respuesta para el panel de control.
- `AnalyticsDeliveriesResponse(data: Dict[str, Any], is_syncing: bool)` - Define la estructura de respuesta para análisis de entregas.
- `AnalyticsInventoryResponse(data: Dict[str, Any], is_syncing: bool)` - Define la estructura de respuesta para análisis de inventario.
- `AnalyticsTasksResponse(data: Dict[str, Any], is_syncing: bool)` - Define la estructura de respuesta para análisis de tareas.
- `JoinDef(table: str, onLeft: str, onRight: str)` - Define una definición de unión (join) para consultas SQL.
- `FilterDef(column: str, operator: str, value: Optional[Any] = "", valueType: Optional[str] = "value", compareColumn: Optional[str] = None, offsetValue: Optional[str] = None, diffOp: Optional[str] = None)` - Define una definición de filtro para consultas SQL.
- `MetricCondition(column: str, operator: str, value: Any)` - Define una condición para métricas en consultas visuales.
- `MetricDef(column: str, aggregation: str, format: Optional[str] = "number", label: Optional[str] = "", condition: Optional[MetricCondition] = None, customExpr: Optional[str] = None)` - Define una definición de métrica para consultas visuales.
- `TimeAxisDef(column: Optional[str] = None, granularity: Optional[str] = "NONE")` - Define la configuración del eje temporal en consultas visuales.
- `SecondMetricDef(column: str = "", aggregation: str = "", label: str = "")` - Define una segunda métrica para consultas visuales.
- `VisualQueryBuilderPayload(baseTable: Optional[str] = None, datasetId: Optional[str] = None, joins: list[JoinDef] = [], filters: list[FilterDef] = [], metric: Optional[MetricDef] = None, timeAxis: Optional[TimeAxisDef] = None, breakdown: Optional[str] = None, secondMetric: Optional[SecondMetricDef] = None, metrics: list[MetricDef] = [], chartType: Optional[str] = "bar")` - Define el payload para consultas visuales.

### Interacción con Base de Datos
Ninguna. Este archivo no interactúa directamente con la base de datos.

### Estado y Variables Globales
Ninguna. No se definen variables globales, de sesión o de entorno en este archivo.

### Dependencias y Flujo
- **Dependencias**: `pydantic`
- **Archivos que importan a este archivo**: Ninguno.
- **Archivos que este archivo importa**: Ninguno.
- **Flujo de datos**: Este archivo define esquemas de datos que pueden ser utilizados por otros componentes del sistema, como los servicios o las rutas.


---

## Archivo: ./core/security.py

### Resumen Funcional
Este archivo contiene utilidades centralizadas de seguridad y validación, específicamente para validar el nombre de tablas en operaciones relacionales con la base de datos.

### Catálogo de Funciones y Clases
- `validate_table(table_name: str) -> None` - Valida el nombre de la tabla contra una lista blanca predefinida para evitar SQL Injection.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (La validación se realiza en memoria, no hay consultas a la base de datos).
- **Columnas**: Ninguna

### Estado y Variables Globales
- `WHITELIST_TABLES: Final[Set[str]]` - Variable global que almacena una lista blanca de tablas permitidas.

### Dependencias y Flujo
- **Dependencias Externas**: No hay dependencias externas.
- **Archivos Importados por Este Archivo**: Ninguno.
- **Archivos que Importan a Este Archivo**: Repositories, Services o cualquier otro componente que necesite validar el nombre de las tablas.

**Flujo de Datos**: El archivo `security.py` se importa en otros componentes del sistema para validar el nombre de las tablas antes de realizar operaciones relacionales con la base de datos.


---

## Archivo: ./core/semantic_layer.py

### Resumen Funcional
La capa `semantic_layer.py` proporciona una abstracción semántica sobre el esquema físico de la base de datos, permitiendo que el frontend acceda a los conjuntos de datos (datasets), dimensiones y métricas mediante identificadores semánticos en lugar de nombres físicos de tablas o columnas.

### Catálogo de Funciones y Clases
- `Dimension(id: str, label: str, physical_column: str, type: str = "string", description: str = "")` - Define una dimensión con su identificador, etiqueta, columna física y tipo.
- `Metric(id: str, label: str, physical_column: str, aggregation: str = "SUM", format: str = "number", is_complex_formula: bool = False, formula_template: Optional[str] = None, description: str = "")` - Define una métrica con su identificador, etiqueta, columna física, agregación y fórmula compleja si es necesario.
- `Dataset(id: str, label: str, physical_table: str, dimensions: List[Dimension] = field(default_factory=list), metrics: List[Metric] = field(default_factory=list))` - Define un conjunto de datos con su identificador, etiqueta, tabla física y listas de dimensiones y métricas.
- `DATASETS: Dict[str, Dataset]` - Catálogo global de conjuntos de datos.
- `_PHYSICAL_TABLE_TO_DATASET: Dict[str, str]` - Mapa inverso para mapear tablas físicas a sus respectivos conjuntos de datos.
- `get_frontend_schema() -> Dict[str, Any]` - Genera un diccionario semántico para exponer a la UI (Studio).
- `resolve_dataset_physical_table(dataset_id: str) -> str` - Devuelve la tabla física dado el ID del dataset.
- `resolve_physical_mapping(dataset_id: str, field_id: str) -> str` - Traduce un ID semántico a su columna física cualificada.
- `get_metric_formula(dataset_id: str, metric_id: str, table_alias: str = "", legacy_agg: str = "") -> Optional[str]` - Devuelve la fórmula compleja de una métrica si la tiene.
- `get_formula_by_physical_table(physical_table: str, aggregation: str, metric_col: str = "") -> Optional[str]` - Reverse-lookup para obtener la expresión SQL real basada en la tabla física y la agregación.

### Interacción con Base de Datos
- Motor de BD: SQLite.
- Tablas:
  - `outbound_deliveries`
  - `stock_levels`
  - `warehouse_tasks`
  - `inventory_movements`
- Columnas:
  - `area_negocio` (en `outbound_deliveries`)
  - `fecha_carga` (en `outbound_deliveries`)
  - `material` (en varias tablas)
  - `estado_wms` (en `outbound_deliveries`)
  - `centro_costo` (en varias tablas)
  - `autor` (en `outbound_deliveries`)
  - `entrega` (en `outbound_deliveries`)
  - `dias_retraso` (en varias tablas)
  - `cantidad` (en varias tablas)
  - `stock_disp` (en `stock_levels`)
  - `fe_creac` (en `warehouse_tasks`)
  - `fecha_conf` (en `warehouse_tasks`)
  - `numero_ot` (en `warehouse_tasks`)
  - `ctd_teor_dsd` (en `warehouse_tasks`)
  - `fe_contab` (en varias tablas)
  - `ce_coste` (en `inventory_movements`)
  - `cmv` (en varias tablas)
  - `tipo_operacion` (en varias tablas)
  - `texto_cab_documento` (en varias tablas)

### Estado y Variables Globales
- `DATASETS: Dict[str, Dataset]` - Almacena el catálogo de conjuntos de datos.
- `_PHYSICAL_TABLE_TO_DATASET: Dict[str, str]` - Mapa inverso para mapear tablas físicas a sus respectivos conjuntos de datos.

### Dependencias y Flujo
- Librerías externas: `dataclasses`, `typing`.
- Archivos del proyecto que importan a este archivo:
  - `services.py`
  - `repositories.py`
  - `db.py`
- Archivos del proyecto que este archivo importa:
  - Ninguno

El flujo de datos es unidireccional, con el archivo `semantic_layer.py` proporcionando funciones para obtener información semántica y mapeos entre IDs semánticos y físicos.


---

## Archivo: ./core/state.py

### Resumen Funcional
Gestión de estado global y caché de la aplicación, incluyendo límites de seguridad para evitar fugas de memoria.

### Catálogo de Funciones y Clases
- `CacheManager()` - Gestor especializado en caché con métodos para obtener, establecer y limpiar el caché.
- `SyncStateManager()` - Gestor especializado en estados de sincronización con métodos para controlar el estado de sincronización.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `cache_manager` - Instancia global de `CacheManager`.
- `sync_manager` - Instancia global de `SyncStateManager`.

### Dependencias y Flujo
- **Dependencias**: No importa ninguna librería externa.
- **Flujo de Datos**: El archivo no consume ni produce datos desde otros archivos del proyecto.


---

## Archivo: ./core/task_manager.py

### Resumen Funcional
El archivo `task_manager.py` implementa un gestor de tareas en segundo plano para un sistema de monitoreo de almacén (WMS). Permite encolar, rastrear y gestionar el estado de las tareas ejecutadas o en ejecución. Utiliza un pool de hilos (`ThreadPoolExecutor`) para evitar bloquear el event loop de FastAPI.

### Catálogo de Funciones y Clases
- `TaskStatus(str, Enum)` - Define los estados posibles de una tarea (PENDING, RUNNING, DONE, FAILED).
- `TaskRecord` - Registro inmutable de una tarea ejecutada o en ejecución.
  - `task_id`: ID único de la tarea.
  - `name`: Nombre descriptivo de la tarea.
  - `status`: Estado actual de la tarea.
  - `created_at`: Fecha y hora de creación de la tarea.
  - `started_at`: Fecha y hora de inicio de la tarea.
  - `finished_at`: Fecha y hora de finalización de la tarea.
  - `result`: Resultado de la tarea si se completó exitosamente.
  - `error`: Mensaje de error si la tarea falló.
- `TaskManager` - Gestor del pool de hilos para ejecutar tareas en segundo plano.
  - `MAX_HISTORY`: Máximo número de tareas completadas en memoria.
  - `__init__(max_workers: int = 3)`: Inicializa el gestor con un número configurable de trabajadores.
  - `submit_task(name: str, fn: Callable, *args, **kwargs) -> str`: Encola una tarea para ejecución en segundo plano y devuelve su ID.
  - `get_task_status(task_id: str) -> Optional[Dict[str, Any]]`: Retorna el estado de una tarea por su ID.
  - `list_tasks(limit: int = 20) -> List[Dict[str, Any]]`: Lista las tareas más recientes (más nueva primero).
  - `has_running_task(name: str) -> bool`: Verifica si hay una tarea con el nombre dado en estado RUNNING.
  - `_trim_history()`: Elimina las tareas completadas más antiguas si se supera el límite de historial.
  - `shutdown(wait: bool = True)`: Cierra graceful del pool de threads.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- `task_manager`: Instancia global de `TaskManager` con 3 trabajadores por defecto.

### Dependencias y Flujo
- **Dependencias**: 
  - `logging`
  - `uuid`
  - `concurrent.futures.ThreadPoolExecutor`
  - `dataclasses`
  - `datetime`
  - `enum.Enum`
  - `threading.Lock`
  - `typing.Any, Callable, Dict, List, Optional`

- **Flujo de Datos**:
  - El archivo no importa ni es importado por otros archivos dentro del proyecto.
  - Las funciones y métodos se utilizan internamente para gestionar el estado de las tareas y ejecutarlas en segundo plano.


---

## Archivo: ./core/utils.py

### Resumen Funcional
Este archivo contiene utilidades transversales y gestión de señales del sistema. Incluye funciones para configurar manejadores de señales, registrar un banner de inicio y limpiar datos para su serialización JSON segura.

### Catálogo de Funciones y Clases
- `setup_signal_handlers()` - Configura los manejadores de señales (SIGINT, SIGTERM) para un cierre limpio.
- `log_startup_banner()` - Registra un banner de inicio del módulo de utilidades del sistema.
- `sanitize_for_json(data: Any) -> Any` - Limpia datos para su serialización JSON segura de forma recursiva y exhaustiva.
- `_get_bound_params_from_visual_state(visual_state_str: str) -> list` - Alias de compatibilidad para obtener parámetros enlazados desde un estado visual.
- `_extract_metric_value(df, active_year: Optional[str] = None) -> Any` - Alias de compatibilidad para extraer un valor métrico de un DataFrame.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `_handlers_registered` (booleano): Flag interno para evitar registros múltiples de manejadores de señales.

### Dependencias y Flujo
- **Dependencias Externas**: `logging`, `math`, `signal`, `sys`, `pandas`.
- **Archivos del Proyecto que Importan a este Archivo**:
  - `services.tunnel.stop_tunnel()`
  - `core.query_engine.get_bound_params_from_visual_state(visual_state_str)`
  - `core.query_engine.extract_metric_value(df, active_year)`

Este archivo no importa archivos del proyecto.


---

## Archivo: ./core/watcher.py

### Resumen Funcional
El archivo `watcher.py` es un componente del sistema de monitoreo de almacén (WMS) que utiliza la biblioteca `watchdog` para observar cambios en archivos dentro de directorios específicos. El objetivo principal es detectar cuando los archivos se han estabilizado y, en ese caso, disparar una sincronización de datos.

### Catálogo de Funciones y Clases
- **AwaitWriteFinishHandler(stability_seconds=3.0, poll_interval=1.0)** - Maneja eventos de sistema de archivos para detectar cuando los archivos se han estabilizado.
  - `on_created(event)` - Llama a `_add_file` cuando un archivo es creado.
  - `on_modified(event)` - Llama a `_add_file` cuando un archivo es modificado.
  - `_should_track(path: str) -> bool` - Determina si un archivo debe ser rastreado basándose en su nombre y extensión.
  - `_add_file(path: str)` - Agrega o actualiza la información del archivo en `tracked_files`.
  - `_poll_files()` - Monitorea los archivos para detectar cambios estables y disparar la sincronización si es necesario.
  - `stop()` - Detiene el rastreo de archivos.

- **start_watcher()** - Inicia el observador de archivos y configura el manejador para comenzar a monitorear los directorios especificados.

- **stop_watcher()** - Detiene el observador de archivos y limpia las variables globales relacionadas.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- `_observer` - Instancia del `Observer` de `watchdog`.
- `_handler` - Instancia de `AwaitWriteFinishHandler`.

### Dependencias y Flujo
- **Dependencias**: 
  - `logging`
  - `os`
  - `threading`
  - `time`
  - `watchdog.events`
  - `watchdog.observers`

- **Flujo**:
  - `start_watcher()` importa a `AwaitWriteFinishHandler` y `Observer`, luego configura y inicia el observador.
  - `stop_watcher()` detiene el observador y limpia las variables globales.

El archivo `watcher.py` se encarga de monitorear cambios en archivos dentro de los directorios especificados, detectar cuando estos archivos se han estabilizado y disparar una sincronización de datos utilizando la biblioteca `watchdog`.


---

## Archivo: ./core/wms_config.py

### Resumen Funcional
Este archivo contiene la configuración y validación de los mapeos utilizados en el sistema de monitoreo de almacén (WMS). Define funciones para obtener mapeos como STATUS_MAPPING y COST_CENTER_MAPPING, y valida su integridad.

### Catálogo de Funciones y Clases
- `validate_wms_maps()` - Valida la integridad de los mapeos definidos.
- `__getattr__(name: str) -> Any` - Soporte para carga dinámica de atributos.

### Interacción con Base de Datos
Ninguna. No hay consultas SQL ni interacciones directas con una base de datos.

### Estado y Variables Globales
No se utilizan variables globales, de sesión o diccionarios quemados en el código que almacenen estado crítico.

### Dependencias y Flujo
- **Dependencias**: 
  - `get_cost_center_mapping()`, `get_holidays()`, `get_setting()`, `get_status_mapping()` (de `db_config_manager.py`).
  
- **Flujo de Datos**:
  - El archivo importa funciones desde `db_config_manager.py`.
  - No hay archivos que importen a este archivo.

Este archivo se encarga de la configuración y validación de mapeos utilizados en el sistema WMS, asegurando que los datos necesarios estén correctamente definidos y no vacíos.


---

## Archivo: ./core/wms_utils.py

### Resumen Funcional
Este archivo contiene funciones utilitarias vectorizadas para transformación de datos en un sistema de monitoreo de almacén (WMS). Las funciones se centran en la limpieza, mapeo y normalización de datos, así como en el cálculo de métricas y la gestión del estado de archivos.

### Catálogo de Funciones y Clases
- `sanitize_string(text: str) -> str` - Normaliza un string para usarlo como encabezado de columna (snake_case).
- `map_wms_status(df: pd.DataFrame) -> pd.DataFrame` - Concatena columnas de estado y mapea al valor legible de negocio.
- `apply_cost_center_mapping(df: pd.DataFrame) -> pd.DataFrame` - Clasifica ubicaciones WMS en áreas de negocio de forma vectorizada.
- `normalize_date_columns(df: pd.DataFrame) -> pd.DataFrame` - Estandariza formatos de fecha WMS a dd-mm-yyyy de forma eficiente.
- `calculate_sla_delays(df: pd.DataFrame) -> pd.DataFrame` - Calcula días hábiles de retraso usando lógica vectorizada de NumPy.
- `generate_time_labels(df: pd.DataFrame) -> pd.DataFrame` - Genera etiquetas de semana ISO para visualización y analítica.
- `_manifest_execute(session_or_conn, sql: str, params: dict)` - Ejecuta una query de manifiesto sobre Session SQLAlchemy o sqlite3.Connection.
- `is_file_changed(session_or_conn, file_path: Path) -> bool` - Verifica si un archivo ha cambiado desde la última sincronización.
- `mark_file_processed(session_or_conn, file_path: Path, row_count: Optional[int] = None)` - Marca un archivo como procesado en el manifiesto.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `sync_manifest`
- Columnas:
  - `file_path`, `last_modified`, `file_size`, `processed_at`, `row_count`

### Estado y Variables Globales
- Variables globales:
  - `logger` (Logger para el módulo)
- Diccionarios quemados en código:
  - `COST_CENTER_MAPPING`
  - `STATUS_MAPPING`

### Dependencias y Flujo
- Librerías externas:
  - `numpy`, `pandas`, `sqlalchemy`, `logging`, `re`, `datetime`, `pathlib`
- Archivos del proyecto que IMPORTA a este archivo (lo consumen):
  - `core.db_config_manager`
  - `core.wms_config`
- Archivos del proyecto que ESTE archivo IMPORTA (consume):
  - Ninguno
- Flujo de datos:
  - El flujo de datos pasa por las funciones para limpiar, mapear y normalizar los datos, y luego se almacenan en la base de datos o se utilizan para cálculos adicionales.


---

