# Documentación Técnica - Directorio: core
Compilado el: 2026-06-05 14:46:00
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./core/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./core/app_instance.py

### Resumen Funcional
Este archivo configura la instancia principal de la aplicación FastAPI, incluyendo su título, descripción y versión. También establece las rutas para la documentación interactiva.

### Catálogo de Funciones y Clases
- `app: FastAPI` -> Instancia principal de la aplicación FastAPI.
- `templates_path: Path` -> Ruta al directorio de plantillas.
- `templates: Jinja2Templates` -> Motor de plantillas configurado con seguridad reforzada.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
No aplica.

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- **Importa**: `pathlib`, `fastapi`, `fastapi.templating`, `config`.
- **Es importado por**: No hay archivos que importen este archivo directamente.
- **Flujo de datos**: Este archivo no consume ni produce datos, solo configura la instancia de FastAPI y el motor de plantillas.


---

## Archivo: ./core/auth.py

### Resumen Funcional
Este archivo `auth.py` contiene las funcionalidades de autenticación y seguridad JWT/OAuth2 para el sistema de monitoreo de almacén (WMS). Define modelos, esquemas, funciones de hashing de contraseñas, gestión de tokens JWT, dependencias FastAPI para proteger endpoints y lógica para crear y gestionar usuarios administradores.

### Catálogo de Funciones y Clases
- `hash_password(plain: str) -> str`: Genera un hash bcrypt del password.
- `verify_password(plain: str, hashed: str) -> bool`: Verifica un password contra su hash bcrypt.
- `create_access_token(username: str, role: str) -> tuple[str, int]`: Crea un JWT firmado con HS256 y retorna el token y la duración de expiración.
- `decode_token(token: str) -> Optional[dict]`: Decodifica y valida un JWT. Retorna None si es inválido o expirado.
- `get_current_user(token: Optional[str] = Depends(oauth2_scheme), request: Request = None, db: Session = Depends(get_session_dep)) -> User`: Dependencia que extrae el usuario del token JWT.
- `require_auth(user: User = Depends(get_current_user)) -> User`: Dependencia que EXIGE un usuario autenticado (no invitado).
- `require_admin(user: User = Depends(require_auth)) -> User`: Dependencia que EXIGE rol de administrador. Lanza 403 si no tiene permisos.
- `init_auth_db()`: Crea las tablas de autenticación si no existen.
- `ensure_admin_exists()`: Crea el usuario admin por defecto si no existe ningún usuario.

### Contratos de API / Endpoints
No aplica. Este archivo no define rutas HTTP.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Operaciones**:
  - **Tabla afectada**: `User`
  - **Tipo de operación**: SELECT/INSERT
  - **Columnas leídas o escritas**: `username`, `password_hash`, `role`, `is_active`, `created_at`

### Flujo de Datos y Pipeline
No aplica. Este archivo no procesa, transforma o mueve datos.

### Caché y Estado
- **Variables globales y de módulo**:
  - `SECRET_KEY`: Clave secreta para JWT.
  - `ALGORITHM`: Algoritmo de codificación JWT.
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Duración de expiración del token JWT.
- **Caché en memoria**: No aplica.
- **Caché persistente**: No aplica.
- **Mecanismos de invalidación de caché**: No aplica.
- **Variables de entorno o sesión utilizadas**:
  - `JWT_SECRET_KEY`: Clave secreta para JWT.
  - `JWT_EXPIRE_MINUTES`: Duración de expiración del token JWT.
  - `ADMIN_USERNAME`: Nombre de usuario administrador por defecto.
  - `ADMIN_PASSWORD`: Contraseña administrador por defecto.

### Lógica de Negocio y Reglas
- **Diccionarios o mapeos hardcoded**:
  - `roles`: Mapeo de roles disponibles (`admin`, `viewer`).
- **Constantes de negocio o umbrales**:
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Duración de expiración del token JWT.
- **Fórmulas de cálculo o reglas de validación**: No aplica.
- **Expresiones CASE/condicionales que implementan reglas de dominio**:
  - Verificación de rol en `require_admin`.
  - Creación de usuario invitado en `get_current_user`.

### Dependencias y Flujo
- **Librerías externas**:
  - `bcrypt`: Para hashing de contraseñas.
  - `jwt`: Para gestión de tokens JWT.
  - `fastapi.security.OAuth2PasswordBearer`: Para manejo de tokens OAuth2.
  - `sqlalchemy.orm.Session`: Para operaciones con la base de datos.
- **Archivos del proyecto que ESTE archivo IMPORTA (consume)**:
  - `core.database.get_session_dep`
  - `core.database.engine`
  - `core.database.Base`
  - `core.models_auth.User`
- **Archivos del proyecto que IMPORTAN a este archivo (lo consumen)**:
  - No aplica.

Este archivo es fundamental para la seguridad y autenticación en el sistema de monitoreo de almacén, proporcionando mecanismos robustos para gestionar usuarios y proteger endpoints sensibles.


---

## Archivo: ./core/database.py

### Resumen Funcional
Este archivo es el punto de entrada para acceder a la capa ORM del sistema, utilizando SQLAlchemy. Soporta SQLite (desarrollo local) y PostgreSQL (producción SaaS) mediante la variable de entorno `DATABASE_URL`. Proporciona funciones para obtener sesiones de base de datos y realizar un chequeo de salud.

### Catálogo de Funciones y Clases
- `get_session() -> Generator[Session, None, None]`: Context manager que entrega una sesión SQLAlchemy. Garantiza commit en éxito y rollback automático en excepción.
- `get_session_dep() -> Generator[Session, None, None]`: Dependencia de FastAPI para inyección de sesiones en endpoints.
- `health_check() -> bool`: Verifica la conectividad con la base de datos. Retorna True si OK.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
- **Motor**: SQLite/Postgres (dependiendo de `DATABASE_URL`)
- **Operaciones**:
  - `SELECT` para verificar la salud de la base de datos (`health_check()`)

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
- **Variables globales y de módulo**: `engine`, `SessionLocal`
- **Caché en memoria**: No aplicable
- **Caché persistente**: No aplicable
- **Mecanismos de invalidación de caché**: No aplicable
- **Variables de entorno o sesión utilizadas**: `DATABASE_URL`

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- **Librerías externas**:
  - `sqlalchemy`
  - `logging`
  - `contextlib`
  - `typing`
  - `os`
- **Archivos del proyecto que ESTE archivo IMPORTA (consume)**: No aplicable
- **Archivos del proyecto que IMPORTAN a este archivo (lo consumen)**:
  - `config.py` (para `DB_PATH`)
  - Endpoints FastAPI que utilizan `get_session_dep()`


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

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `StatusMapping`
  - `CostCenterMapping`
  - `AppSetting`
  - `Holiday`
  - `ConfigQuery`
- Columnas:
  - `StatusMapping`: `code`, `label`
  - `CostCenterMapping`: `center_code`, `business_area`
  - `AppSetting`: `key`, `value`, `type`
  - `Holiday`: `date_str`
  - `ConfigQuery`: `query_id`, `visual_state`

### Estado y Variables Globales
- No hay variables globales, de sesión o de entorno explícitas.

### Dependencias y Flujo
- Importa: `logging`, `typing`, `sqlalchemy`, `os`.
- Exporta: Funciones públicas para acceder a la configuración.
- No depende de otros archivos del proyecto.


---

## Archivo: ./core/macros.py

### Resumen Funcional
El archivo `macros.py` centraliza reglas de negocio y macros SQL para ser utilizadas en múltiples capas de la aplicación, facilitando la expresión de lógicas complejas que deben inyectarse en el código SQL.

### Catálogo de Funciones y Clases
- `inject_macros(sql: str) -> str` - Inyecta todas las macros globales registradas en el string SQL proporcionado.

### Interacción con Base de Datos
Ninguna. El archivo no realiza ninguna operación directa sobre la base de datos.

### Estado y Variables Globales
Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- **Dependencias**: Ninguna.
- **Flujo de Datos**: El archivo no importa ni es importado por otros archivos dentro del proyecto. No hay interacción con otras partes del sistema a través de funciones o clases.


---

## Archivo: ./core/models.py

### Resumen Funcional
Este archivo define los modelos ORM SQLAlchemy para las tablas de configuración dinámica del sistema de monitoreo de almacén (WMS). Incluye mapeos de estados, centros de costo, parámetros globales, feriados y consultas SQL gestionadas via UI.

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
- Importa de `database.py`: `Base`
- No se importan archivos del proyecto que lo consuman.


---

## Archivo: ./core/models_auth.py

### Resumen Funcional
Este archivo define el modelo ORM para los usuarios del sistema de autenticación, incluyendo sus atributos y relaciones con la base de datos.

### Catálogo de Funciones y Clases
- `User` (id: int, username: str, password_hash: str, role: str, is_active: bool, created_at: datetime) -> Mapped[User]
  - **Propósito**: Representa una tabla en la base de datos que almacena información sobre los usuarios del sistema.
  - **Métodos Principales**:
    - `__repr__`: Devuelve una representación legible del objeto.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Operaciones SQL/ORM Detectadas**:
  - **Tabla Afectada**: `auth_users`
  - **Tipo de Operación**: SELECT, INSERT, UPDATE
  - **Columnas Leídas o Escritas**:
    - id (Integer)
    - username (String(50))
    - password_hash (String(255))
    - role (String(20))
    - is_active (Boolean)
    - created_at (DateTime)

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
- **Variables Globales y de Módulo**: No aplica.
- **Caché en Memoria**: No aplica.
- **Caché Persistente**: No aplica.
- **Mecanismos de Invalidación de Caché**: No aplica.
- **Variables de Entorno o Sesión Utilizadas**: No aplica.

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlalchemy`
  - `datetime`
- **Archivos del Proyecto que IMPORTA a este archivo (lo consumen)**: No aplica.
- **Archivos del Proyecto que ESTE archivo IMPORTA**: 
  - `database.py` (importado como `from .database import Base`)
- **Dirección del Flujo de Datos**: Este archivo es un modelo ORM y no realiza operaciones directamente sobre la base de datos o el flujo de datos.


---

## Archivo: ./core/models_transaccional.py

### Resumen Funcional
Este archivo define modelos de datos para una base de datos SQLite utilizada en un sistema de monitoreo de almacén (WMS). Los modelos representan diferentes entidades como tareas de almacenamiento, movimientos de inventario, entregas salientes y niveles de stock.

### Catálogo de Funciones y Clases
- `WarehouseTask` - Representa una tarea de almacenamiento con varios campos.
- `InventoryMovement` - Representa un movimiento de inventario con detalles del material, cantidad y ubicación.
- `OutboundDelivery` - Representa una entrega saliente con información sobre el material, la ubicación y los tiempos de carga.
- `StockLevel` - Representa el nivel de stock para diferentes materiales y lotes.
- `Lx02Pendiente` - Representa pendientes en un sistema específico (LX02) con detalles del material y la ubicación.
- `SyncManifest` - Representa un manifiesto de sincronización con información sobre archivos procesados.
- `AnalyticsSnapshot` - Representa una instantánea de análisis con datos y tiempos de actualización.
- `AutorAreaMapping` - Representa el mapeo entre autores y áreas de negocio.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQLite. Las tablas definidas son:
- `warehouse_tasks`
- `inventory_movements`
- `outbound_deliveries`
- `stock_levels`
- `lx02_pendientes`
- `sync_manifest`
- `analytics_snapshots`
- `autor_area_mapping`

### Estado y Variables Globales
No hay variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
Dependencias:
- `sqlalchemy` - Para ORM y definición de modelos.
- `core.database.Base` - Clase base para todos los modelos.

Flujo:
- Este archivo es importado por otros archivos que necesitan interactuar con la base de datos, como servicios o repositorios.


---

## Archivo: ./core/pdf_engine.py

### Resumen Funcional
El archivo `pdf_engine.py` es un motor optimizado para la generación de documentos PDF en el sistema de monitoreo de almacén (WMS). Se encarga de crear reportes WMS en formato horizontal utilizando la biblioteca FPDF y otros componentes como pandas y barcode.

### Catálogo de Funciones y Clases
- `get_ots_for_delivery(entrega_id: str, conn: sqlite3.Connection) -> List[str]`
  - Consulta las OTs asociadas a una entrega y las devuelve como lista de strings.
  
- `_generate_barcode_stream(data: str, options: Optional[dict] = None) -> io.BytesIO`
  - Genera un código de barras en memoria (BytesIO).

- `draw_delivery_page(pdf: WMS_Landscape_PDF, header: pd.Series, items: pd.DataFrame, include_logo: bool = True, ots_list: Optional[List[str]] = None) -> None`
  - Dibuja una página de entrega completa utilizando sub-métodos modulares.

- `_draw_page_header(pdf: WMS_Landscape_PDF, h: pd.Series, include_logo: bool)`
  - Dibuja el encabezado superior, logo y código de barras de la entrega.
  
- `_draw_info_block(pdf: WMS_Landscape_PDF, h: pd.Series)`
  - Dibuja el bloque de información principal de la entrega.

- `_draw_table(pdf: WMS_Landscape_PDF, items_df: pd.DataFrame)`
  - Dibuja la tabla de materiales con ordenamiento por ubicación.
  
- `_draw_ot_barcodes(pdf: WMS_Landscape_PDF, ots: List[str])`
  - Dibuja los códigos de barras de las OTs en el lateral derecho.

- `_draw_signature_block(pdf: WMS_Landscape_PDF)`
  - Dibuja los cuadros de firma al final de la página.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Operaciones SQL:**
  - `SELECT DISTINCT numero_ot FROM warehouse_tasks WHERE ltrim(CAST(entrega AS TEXT), '0') = ?`

### Flujo de Datos y Pipeline
1. **Entrada:** Recibe un ID de entrega (`entrega_id`) y una conexión a la base de datos SQLite (`conn`).
2. **Transformaciones:**
   - Consulta las OTs asociadas a la entrega desde la tabla `warehouse_tasks`.
   - Genera códigos de barras para la entrega y las OTs.
3. **Salida:** Produce un documento PDF con la información de la entrega, los códigos de barras y una firma.

### Caché y Estado
No aplica.

### Lógica de Negocio y Reglas
- **Constantes de Diseño:**
  - Margen X e Y.
  - Posición inicial de la tabla.
  - Altura de las filas.
  - Número máximo de filas.
  - Dimensiones del código de barras.

### Dependencias y Flujo
- **Librerías Externas:** `numpy`, `pandas`, `fpdf`, `barcode`
- **Archivos Importados:**
  - `config.py` (para la configuración temporal)
- **Flujo de Datos:** El archivo se importa en otros archivos para generar PDFs, lo que indica que es un componente consumido por otros servicios o rutas del sistema.


---

## Archivo: ./core/pdf_reports.py

### Resumen Funcional
Este archivo contiene la lógica para construir secciones complejas de PDFs en un sistema de monitoreo de almacén (WMS). Específicamente, define funciones para dibujar tablas de anexos y listas de picking en documentos PDF.

### Catálogo de Funciones y Clases
- `_parse_qty(val) -> float` - Sanitiza y convierte a float valores de cantidad de WMS.
- `_fmt_qty(val) -> str` - Formatea cantidades para mostrar en el PDF de forma legible.
- `draw_annex_table(pdf, grouped_data)` - Dibuja la tabla de índice (anexo) de entregas agrupadas.
- `draw_picking_list(pdf, picking_df)` - Dibuja la lista de picking desglosada por entrega pero con total consolidado.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
1. **Entrada**: Recibe un objeto `pdf` (probablemente una instancia de una biblioteca como ReportLab) y datos agrupados (`grouped_data`) para la tabla de anexos, o un DataFrame (`picking_df`) para la lista de picking.
2. **Transformaciones**:
   - Para `_parse_qty`, limpia y convierte valores de cantidad a float.
   - Para `_fmt_qty`, formatea cantidades para mostrar en el PDF.
   - Para `draw_annex_table`, dibuja una tabla con los datos agrupados, incluyendo encabezado y filas.
   - Para `draw_picking_list`, calcula totales consolidados por área/material, limpia y formatea datos de picking, y dibuja la lista en el PDF.
3. **Salida**: Produce documentos PDF con las tablas de anexos y listas de picking.

### Caché y Estado
No aplica.

### Lógica de Negocio y Reglas
- No hay diccionarios o mapeos hardcoded, constantes de negocio o fórmulas de cálculo específicas en este archivo.

### Dependencias y Flujo
- **Dependencias**: Importa `datetime` desde el módulo estándar de Python.
- **Flujo**: Este archivo no importa a otros archivos del proyecto ni es importado por otros. Es una utilidad compartida dentro del sistema para construir PDFs.

Este archivo es un componente crucial para la generación de documentos PDF en el sistema WMS, proporcionando funciones específicas para crear tablas de anexos y listas de picking de manera eficiente y legible.


---

## Archivo: ./core/query_engine.py

### Resumen Funcional
Este archivo actúa como una fachada para el motor de SQL, proporcionando una interfaz para construir y ejecutar consultas SQL seguras y validadas en un sistema de monitoreo de almacén (WMS) utilizando FastAPI, SQLAlchemy y SQLite.

### Catálogo de Funciones y Clases
- `validate_identifier(identifier)` - Valida si el identificador proporcionado es válido.
- `validate_column(column_name, table_name)` - Valida si la columna pertenece a la tabla especificada.
- `get_table_columns(table_name)` - Obtiene las columnas de una tabla específica.
- `ALLOWED_TABLES` - Lista de tablas permitidas para consultas.
- `ALLOWED_AGGREGATIONS` - Lista de agregaciones permitidas en consultas.
- `ALLOWED_GRANULARITIES` - Lista de granularidades permitidas en consultas.
- `get_bound_params_from_visual_state(visual_state)` - Extrae los parámetros limitados desde el estado visual.
- `extract_metric_value(metric_data)` - Extrae el valor de una métrica de los datos proporcionados.
- `build_sql_from_payload(payload, area_expr_macro=AREA_EXPR_MACRO)` - Construye una consulta SQL a partir del payload proporcionado.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con la base de datos.

### Estado y Variables Globales
Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en el código que almacenen estado crítico.

### Dependencias y Flujo
- **Dependencias Externas**: `core.query_validators`, `core.query_utils`, `core.query_builder`.
- **Archivos del Proyecto Importados por Este Archivo**:
  - No aplica.
- **Archivos del Proyecto que Importan a Este Archivo**:
  - No aplica.

El flujo de datos es unidireccional, con este archivo proporcionando funciones y utilidades para construir consultas SQL seguras en el sistema WMS.


---

## Archivo: ./core/query_utils.py

### Resumen Funcional
Este archivo contiene funciones utilitarias para el procesamiento de parámetros y extracción de métricas desde datos en formato JSON y DataFrames.

### Catálogo de Funciones y Clases
- `get_bound_params_from_visual_state(visual_state_str: str) -> list` - Extrae los bind params (?) de un visual_state JSON serializado.
- `extract_metric_value(df, active_year: str = None)` - Extrae el valor numérico principal de un DataFrame de resultado de query.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: `json`
- **Flujo de Datos**:
  - `get_bound_params_from_visual_state` importa `json` para procesar el JSON serializado.
  - `extract_metric_value` no depende de ninguna librería externa.


---

## Archivo: ./core/query_validators.py

### Resumen Funcional
Este archivo contiene funciones para validar identificadores de tablas y columnas en un sistema de monitoreo de almacén (WMS) utilizando FastAPI, SQLAlchemy y SQLite. Las funciones garantizan que solo se acceda a tablas y columnas permitidas, evitando así inyecciones SQL.

### Catálogo de Funciones y Clases
- `validate_identifier(name: str, db: Session) -> bool` - Valida si un identificador (tabla o tabla.columna) pertenece a la lista blanca.
- `validate_column(table: str, column: str, db: Session) -> bool` - Valida si una columna pertenece a una tabla permitida.
- `get_table_columns(table: str, db: Session) -> List[str]` - Retorna la lista de columnas de una tabla permitida.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `outbound_deliveries`
  - `stock_levels`
  - `warehouse_tasks`
  - `inventory_movements`
- Columnas:
  - Consulta dinámica a través de `PRAGMA table_info(table_name)` para verificar la existencia de columnas.

### Estado y Variables Globales
- `ALLOWED_TABLES` (frozenset): Lista blanca de tablas permitidas.
- `ALLOWED_AGGREGATIONS` (frozenset): Conjunto de agregaciones permitidas.
- `ALLOWED_GRANULARITIES` (frozenset): Granularidades permitidas.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `sqlalchemy.orm.Session`
  - `sqlalchemy.text`
  - `typing.List`
  - `logging`

- **Archivos del Proyecto que Importan a este Archivo**:
  - No se mencionan archivos específicos.

- **Archivos del Proyecto que Este Archivo Importa**:
  - No se mencionan archivos específicos.

- **Flujo de Datos**: 
  - El archivo interactúa con la base de datos para validar identificadores y columnas, utilizando consultas SQL dinámicas.


---

## Archivo: ./core/schemas.py

### Resumen Funcional
Este archivo define esquemas de datos utilizando Pydantic para representar diferentes tipos de respuestas y payloads en un sistema de monitoreo de almacén (WMS). Los esquemas incluyen estructuras para respuestas del dashboard, análisis de entregas, inventario y tareas, así como definiciones para consultas visuales avanzadas.

### Catálogo de Funciones y Clases
- `DashboardResponse(data: Dict[str, Any], is_syncing: bool) -> None`: Representa la respuesta del dashboard.
- `AnalyticsDeliveriesResponse(data: Dict[str, Any], is_syncing: bool) -> None`: Representa la respuesta del análisis de entregas.
- `AnalyticsInventoryResponse(data: Dict[str, Any], is_syncing: bool) -> None`: Representa la respuesta del análisis de inventario.
- `AnalyticsTasksResponse(data: Dict[str, Any], is_syncing: bool) -> None`: Representa la respuesta del análisis de tareas.
- `JoinDef(table: str, onLeft: str, onRight: str) -> None`: Define una relación JOIN para consultas visuales avanzadas.
- `FilterDef(column: str, operator: str, value: Optional[Any] = "", valueType: Optional[str] = "value", compareColumn: Optional[str] = None, offsetValue: Optional[str] = None, diffOp: Optional[str] = None) -> None`: Define un filtro para consultas visuales avanzadas.
- `MetricCondition(column: str, operator: str, value: Any) -> None`: Define una condición de métrica para consultas visuales avanzadas.
- `MetricDef(column: str, aggregation: str, format: Optional[str] = "number", label: Optional[str] = "", condition: Optional[MetricCondition] = None, customExpr: Optional[str] = None) -> None`: Define una métrica para consultas visuales avanzadas.
- `TimeAxisDef(column: Optional[str] = None, granularity: Optional[str] = "NONE") -> None`: Define el eje de tiempo para consultas visuales avanzadas.
- `SecondMetricDef(column: str = "", aggregation: str = "", label: str = "") -> None`: Define una segunda métrica para consultas visuales avanzadas.
- `VisualQueryBuilderPayload(baseTable: Optional[str] = None, datasetId: Optional[str] = None, joins: list[JoinDef] = [], filters: list[FilterDef] = [], metric: Optional[MetricDef] = None, timeAxis: Optional[TimeAxisDef] = None, breakdown: Optional[str] = None, secondMetric: Optional[SecondMetricDef] = None, metrics: list[MetricDef] = [], chartType: Optional[str] = "bar") -> None`: Define el payload para consultas visuales avanzadas.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
No aplica.

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- **Librerías Externas**: `pydantic`, `typing`
- **Archivos del Proyecto que Importan a este Archivo**: No aplica.
- **Archivos del Proyecto que Este Archivo Importa**: No aplica.


---

## Archivo: ./core/security.py

### Resumen Funcional
Utilidades centralizadas de seguridad y validación, específicamente para validar el nombre de tablas contra una lista blanca para prevenir SQL Injection.

### Catálogo de Funciones y Clases
- `validate_table(table_name: str) -> None` - Valida el nombre de la tabla contra la lista blanca para prevenir SQL Injection. Lanza `ValueError` si la tabla no está permitida.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
- Motor: SQLite
- Operación: SELECT (implicada en la validación)
- Tabla afectada: Todas las tablas mencionadas en `WHITELIST_TABLES`
- Columnas leídas: Nombre de la tabla

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
- Variables globales y de módulo:
  - `WHITELIST_TABLES`: Conjunto inmutable de nombres de tablas permitidas.

### Lógica de Negocio y Reglas
- Constantes de negocio o umbrales:
  - `WHITELIST_TABLES`: Lista blanca de tablas permitidas para evitar SQL Injection.

### Dependencias y Flujo
- Librerías externas: `typing`
- Archivos del proyecto que IMPORTA a este archivo (lo consumen): No aplica.
- Archivos del proyecto que este archivo IMPORTA (consume): No aplica.


---

## Archivo: ./core/semantic_layer.py

### Resumen Funcional
La capa `semantic_layer.py` proporciona una abstracción semántica sobre el esquema físico de la base de datos, manteniendo un catálogo de conjuntos de datos (datasets), dimensiones y métricas. Ofrece funciones para resolver mapeos entre IDs semánticos y físicos, generar esquemas frontend, y recuperar fórmulas complejas de métricas.

### Catálogo de Funciones y Clases
- `Dimension(id: str, label: str, physical_column: str, type: str = "string", description: str = "")` - Define una dimensión con su ID, etiqueta, columna física y tipo.
- `Metric(id: str, label: str, physical_column: str, aggregation: str = "SUM", format: str = "number", is_complex_formula: bool = False, formula_template: Optional[str] = None, description: str = "")` - Define una métrica con su ID, etiqueta, columna física, agregación y fórmula compleja si es necesario.
- `Dataset(id: str, label: str, physical_table: str, dimensions: List[Dimension] = field(default_factory=list), metrics: List[Metric] = field(default_factory=list))` - Define un conjunto de datos con su ID, etiqueta, tabla física y listas de dimensiones y métricas.
- `DATASETS: Dict[str, Dataset]` - Catálogo global de conjuntos de datos.
- `_PHYSICAL_TABLE_TO_DATASET: Dict[str, str]` - Mapa inverso para mapear tablas físicas a IDs de conjuntos de datos.
- `get_frontend_schema() -> Dict[str, Any]` - Genera un diccionario semántico para exponer a la UI (Studio).
- `resolve_dataset_physical_table(dataset_id: str) -> str` - Devuelve la tabla física dado el ID del dataset.
- `resolve_physical_mapping(dataset_id: str, field_id: str) -> str` - Traduce un ID semántico a su columna física cualificada.
- `get_metric_formula(dataset_id: str, metric_id: str, table_alias: str = "", legacy_agg: str = "") -> Optional[str]` - Devuelve la fórmula compleja de una métrica si la tiene.
- `get_formula_by_physical_table(physical_table: str, aggregation: str, metric_col: str = "") -> Optional[str]` - Reverse-lookup para obtener la expresión SQL real basada en la tabla física y la agregación.

### Interacción con Base de Datos
No se utiliza ninguna base de datos explícita. Todas las operaciones relacionadas con la BD son indirectas a través de los mapeos y consultas que utilizan los IDs semánticos.

### Estado y Variables Globales
- `DATASETS: Dict[str, Dataset]` - Almacena el catálogo global de conjuntos de datos.
- `_PHYSICAL_TABLE_TO_DATASET: Dict[str, str]` - Mapa inverso para mapear tablas físicas a IDs de conjuntos de datos.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas adicionales.
- **Flujo de Datos**:
  - `get_frontend_schema()` genera un esquema semántico para la UI.
  - `resolve_dataset_physical_table(dataset_id: str)` resuelve el mapeo entre IDs de conjuntos de datos y tablas físicas.
  - `resolve_physical_mapping(dataset_id: str, field_id: str)` traduce IDs semánticos a columnas físicas.
  - `get_metric_formula(dataset_id: str, metric_id: str, table_alias: str = "", legacy_agg: str = "")` recupera fórmulas complejas de métricas.
  - `get_formula_by_physical_table(physical_table: str, aggregation: str, metric_col: str = "")` realiza un reverse-lookup para obtener expresiones SQL basadas en tablas físicas y agregaciones.


---

## Archivo: ./core/state.py

### Resumen Funcional
Gestión centralizada del estado mutable y la caché de la aplicación, implementando límites de seguridad para evitar fugas de memoria.

### Catálogo de Funciones y Clases
- `AppState()` - Gestiona el estado mutable y la caché de forma centralizada.
  - `__init__()`
  - `max_cache_size` (getter/setter) - Devuelve/Configura el límite máximo de entradas en caché.
  - `sync_lock` (getter) - Devuelve el lock de sincronización para operaciones atómicas.
  - `is_syncing` (getter/setter) - Verifica y actualiza el estado de sincronización (atómico).
  - `cache_size` (getter) - Devuelve el número actual de entradas en la caché.
  - `get_cache(key: str)` - Recupera un valor del caché.
  - `set_cache(key: str, value: Any)` - Guarda un valor en el caché, respetando los límites de tamaño.
  - `clear_cache(key: Optional[str] = None)` - Limpia una entrada específica o todo el caché.
  - `clear_cache_prefix(prefix: str)` - Limpia todas las entradas de caché que comiencen con el prefijo dado.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `global_state` - Instancia única de la clase `AppState`, almacenada globalmente para su acceso desde cualquier parte del proyecto.

### Dependencias y Flujo
- **Dependencias**: No importa ninguna librería externa.
- **Flujo de Datos**: El archivo no consume ni es consumido por otros archivos. Es un componente central que proporciona acceso a la instancia global de `AppState` para gestionar el estado y la caché de la aplicación.


---

## Archivo: ./core/task_manager.py

### Resumen Funcional
Este archivo define el `TaskManager`, un gestor de tareas en segundo plano para un sistema de monitoreo de almacén (WMS). Permite encolar, rastrear y gestionar el estado de las tareas ejecutadas en segundo plano.

### Catálogo de Funciones y Clases
- **submit_task(name: str, fn: Callable, *args, **kwargs) -> str**: Encola una tarea para ejecución en segundo plano.
- **get_task_status(task_id: str) -> Optional[Dict[str, Any]]**: Retorna el estado de una tarea por su ID.
- **list_tasks(limit: int = 20) -> List[Dict[str, Any]]**: Lista las tareas más recientes (más nueva primero).
- **has_running_task(name: str) -> bool**: Verifica si hay una tarea con el nombre dado en estado RUNNING.
- **_trim_history()**: Elimina las tareas completadas más antiguas si se supera el límite.
- **shutdown(wait: bool = True)**: Cierre graceful del pool de threads.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
1. **Entrada**: Recibe una función `fn` y sus argumentos.
2. **Transformación**: Crea un `TaskRecord` para la tarea, lo encola en el `ThreadPoolExecutor`, y actualiza su estado según el resultado de la ejecución.
3. **Salida**: No produce datos de salida directamente.

### Caché y Estado
- **Variables globales y de módulo**: `task_manager`
- **Caché en memoria**: Diccionarios `_tasks` y `_futures`
- **Mecanismos de invalidación de caché**: `_trim_history()`
- **Variables de entorno o sesión utilizadas**: No aplica.

### Lógica de Negocio y Reglas
- **Constantes de negocio**: `MAX_HISTORY = 50`
- **Reglas de validación**: Verifica si hay una tarea con el nombre dado en estado RUNNING (`has_running_task`).

### Dependencias y Flujo
- **Librerías externas**: `concurrent.futures`, `dataclasses`, `enum`, `typing`, `threading`, `logging`
- **Archivos del proyecto que este archivo importa (consume)**: No aplica.
- **Archivos del proyecto que importan a este archivo (lo consumen)**: `routes` (por ejemplo, `/api/tasks`)
- **Dirección del flujo de datos**: Desde las rutas hasta el `TaskManager`, y desde el `TaskManager` hasta la ejecución de tareas en segundo plano.


---

## Archivo: ./core/utils.py

### Resumen Funcional
Este archivo contiene utilidades transversales y gestión de señales del sistema. Se encarga de configurar manejadores de señales para un cierre limpio, registrar mensajes de inicio y sanitizar datos para su serialización JSON segura.

### Catálogo de Funciones y Clases
- `setup_signal_handlers() -> None` - Configura los manejadores de señales (SIGINT, SIGTERM) para un cierre limpio.
- `log_startup_banner() -> None` - Registra un mensaje de inicio del módulo de utilidades.
- `sanitize_for_json(data: Any) -> Any` - Limpia datos para serialización JSON segura de forma recursiva y exhaustiva.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
- Variables globales: `_handlers_registered` - Flag interno para evitar registros múltiples.
- Variables de entorno o sesión utilizadas: No aplica.

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- Librerías externas:
  - `signal`
  - `sys`
  - `logging`
  - `pandas`
  - `math`
  - `typing`

- Archivos del proyecto que IMPORTA a este archivo (lo consumen):
  - `services.tunnel.stop_tunnel()`
  - `core.query_engine.get_bound_params_from_visual_state(visual_state_str)`
  - `core.query_engine.extract_metric_value(df, active_year)`

- Archivos del proyecto que este archivo IMPORTA:
  - No aplica

El flujo de datos es desde las funciones hacia los archivos dependientes.


---

## Archivo: ./core/watcher.py

### Resumen Funcional
El archivo `watcher.py` implementa un observador de archivos que monitorea cambios en directorios especificados, como OneDrive y otro directorio local. Cuando detecta archivos estables (sin cambios durante 3 segundos), dispara una sincronización del almacén.

### Catálogo de Funciones y Clases
- `AwaitWriteFinishHandler(stability_seconds=3.0, poll_interval=1.0)` - Maneja eventos de sistema de archivos y monitorea estabilidad de los archivos.
  - `_should_track(path: str) -> bool` - Determina si un archivo debe ser rastreado.
  - `on_created(event)` - Llama a `_add_file` cuando se crea un nuevo archivo.
  - `on_modified(event)` - Llama a `_add_file` cuando se modifica un archivo existente.
  - `_add_file(path: str)` - Añade o actualiza la información del archivo en el diccionario `tracked_files`.
  - `_poll_files()` - Monitorea los archivos rastreados y dispara una sincronización si es necesario.
  - `stop()` - Detiene el observador y las operaciones de monitoreo.

- `start_watcher()` - Inicia el observador en los directorios especificados.
- `stop_watcher()` - Detiene el observador.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `_observer` - Instancia del observador de archivos.
- `_handler` - Instancia del manejador de eventos de archivos.

### Dependencias y Flujo
- **Librerías Externas**: `watchdog`, `logging`, `threading`.
- **Archivos Importados**:
  - `config.py`: Para obtener el camino de OneDrive.
  - `core.task_manager`: Para gestionar tareas asincrónicas.
  - `routes.sync`: Para ejecutar la sincronización del almacén.

El flujo de datos es el siguiente:
1. `start_watcher()` se llama para iniciar el observador en los directorios especificados.
2. El observador (`_observer`) monitorea los eventos de archivos en los directorios rastreados.
3. Cuando un archivo es modificado y alcanza la estabilidad requerida, `_poll_files()` detecta esto y dispara `task_manager.submit_task("sync_data", _run_sync_pipeline)`.
4. `stop_watcher()` se llama para detener el observador y las operaciones de monitoreo.

Este flujo asegura que los cambios en los archivos sean sincronizados con el almacén solo cuando estos son estables, evitando la sobrecarga del sistema con sincronizaciones innecesarias.


---

## Archivo: ./core/wms_config.py

### Resumen Funcional
Este archivo contiene la configuración y lógica de negocio para el mapeo WMS (SaaS Dinámico). Define funciones para validar los mapeos de estado, centro de costo y feriados. También proporciona soporte para cargar dinámicamente atributos como `STATUS_MAPPING` y `COST_CENTER_MAPPING`.

### Catálogo de Funciones y Clases
- `validate_wms_maps()` - Valida la integridad de los mapeos definidos.
- `__getattr__(name: str) -> Any` - Soporte para carga dinámica de atributos.

### Interacción con Base de Datos
Ninguna. No se realiza ninguna interacción directa con una base de datos en este archivo.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno definidas en este archivo.

### Dependencias y Flujo
- **Dependencias**: 
  - `get_setting`, `get_status_mapping`, `get_cost_center_mapping`, `get_holidays` (de `db_config_manager.py`)
  
- **Flujo de Datos**:
  - Este archivo es consumido por otros archivos que necesiten acceso a los mapeos WMS y la configuración dinámica.
  - Los atributos como `STATUS_MAPPING` y `COST_CENTER_MAPPING` se cargan dinámicamente cuando son accedidos.

Este archivo es crucial para mantener la integridad de los mapeos WMS y proporcionar acceso a estos mapeos de manera dinámica en el sistema.


---

## Archivo: ./core/wms_utils.py

### Resumen Funcional
Este archivo contiene funciones utilitarias vectorizadas para transformación de datos en un sistema de monitoreo de almacén (WMS). Las funciones se centran en la limpieza, mapeo y normalización de datos, así como en el cálculo de métricas y la gestión del estado de archivos.

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
- Motor: SQLite
- Tablas:
  - `sync_manifest`
- Columnas:
  - `file_path`, `last_modified`, `file_size`, `processed_at`, `row_count`

### Estado y Variables Globales
- `logger` - Objeto de logging para el módulo.

### Dependencias y Flujo
- Librerías externas: `re`, `logging`, `numpy`, `pandas`, `datetime`, `pathlib`, `typing`.
- Archivos del proyecto que importa:
  - `core.wms_config`
  - `core.db_config_manager`
- Archivos del proyecto que son importados por este archivo:
  - Ninguno
- Flujo de datos: El flujo principal es el procesamiento y transformación de DataFrames, con interacciones ocasionales con la base de datos para gestionar el estado de archivos.


---

