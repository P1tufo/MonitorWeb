# Documentación Técnica Global - MonitorWeb
Compilado el: 2026-06-07 18:34:58
Modelo: qwen2.5-coder:7b | Hardware: M1 Pro Optimized

---

## Análisis de Arquitectura Global

### Arquitectura General Detectada

La estructura del proyecto sugiere una arquitectura modular. La organización de los archivos y carpetas indica que el proyecto está dividido en diferentes módulos o componentes, cada uno con un propósito específico.

### Propósito Probable de las Carpetas Principales

- **`app.py`, `config.py`, `main.py`:** Estos archivos probablemente contienen la configuración inicial del aplicativo y su punto de entrada principal.
  
- **`core/`:** Este directorio contiene el código central del sistema, incluyendo componentes como autenticación, base de datos, modelos, utilidades y más. Es un lugar para los módulos que son fundamentales para la funcionalidad general del proyecto.

- **`bin/`:** Contiene archivos ejecutables o herramientas adicionales necesarias para el desarrollo o despliegue del proyecto.

- **`deploy/`:** Este directorio probablemente contiene archivos relacionados con el despliegue y configuración del entorno de producción, como Dockerfiles y scripts de configuración.

- **`docs/`:** Contiene la documentación del proyecto, dividida en diferentes secciones para facilitar su búsqueda y mantenimiento.

- **`repositories/`:** Este directorio probablemente contiene los repositorios o capas de acceso a datos, donde se definen las operaciones CRUD sobre la base de datos.

- **`routes/`:** Contiene los controladores o rutas del sistema, que manejan las solicitudes HTTP y interactúan con los servicios correspondientes.

- **`services/`:** Este directorio probablemente contiene los servicios de negocio, que encapsulan la lógica empresarial y se comunican con los repositorios y otros servicios.

### Organización Lógica de las Dependencias

La organización de las dependencias parece ser coherente y modular. Cada módulo tiene un propósito específico y interactúa con otros módulos a través de interfaces bien definidas. Por ejemplo:

- **`core/`:** Es el núcleo del sistema, proporcionando funcionalidades comunes que pueden ser utilizadas por todos los demás componentes.
  
- **`repositories/`:** Dependen de `core/database.py` para interactuar con la base de datos.

- **`services/`:** Dependen de `repositories/` y `core/security.py` para realizar operaciones de negocio complejas.

- **`routes/`:** Dependen de `services/` para manejar las solicitudes HTTP y devolver respuestas al cliente.

Esta estructura modular facilita el mantenimiento, la escalabilidad y la reutilización del código. Cada componente puede ser desarrollado, probado y depurado por separado, lo que mejora la eficiencia del desarrollo en equipo.


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

## Archivo: ./core/helpers/dynamic_executor.py

### Resumen Funcional
El archivo `dynamic_executor.py` contiene una función que toma un payload JSON crudo, lo valida y compila en una consulta SQL utilizando el módulo `query_engine`. Luego ejecuta la consulta en una base de datos SQLite y devuelve los resultados como un DataFrame de Pandas.

### Catálogo de Funciones y Clases
- `execute_visual_query(payload_dict: Dict, db: Session) -> pd.DataFrame` - Toma un payload JSON crudo, lo valida y compila usando el query_engine, y devuelve un DataFrame de Pandas directamente.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna (se espera que la consulta SQL genere los resultados necesarios).
- Consultas SQL Crudas o Llamadas a ORM: Sí, utiliza `pd.read_sql` para ejecutar la consulta SQL generada.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías Externas:
  - `pandas`
  - `sqlalchemy.orm.Session`
- Archivos del Proyecto que Importan a este Archivo: Ninguno
- Archivos del Proyecto que Este Archivo Importa:
  - `core.query_engine.build_sql_from_payload`
  - `core.schemas.VisualQueryBuilderPayload`

**Flujo de Datos:**
1. El archivo se importa en algún lugar dentro del proyecto.
2. Se llama a la función `execute_visual_query` con un payload JSON y una sesión de base de datos.
3. La función valida el payload, compila una consulta SQL usando `build_sql_from_payload`, ejecuta la consulta en la base de datos y devuelve los resultados como un DataFrame de Pandas.


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

## Archivo: ./core/seed_data/widgets.json

### Resumen Funcional
El archivo `widgets.json` contiene una lista de consultas y configuraciones para visualizaciones en un sistema de monitoreo de almacén (WMS). Cada consulta define cómo se deben obtener datos de la base de datos y cómo se deben presentar estos datos en gráficos.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **TABLAS**:
  - `inventory_movements`
  - `outbound_deliveries`
  - `warehouse_tasks`
- **COLUMNAS**:
  - `material`
  - `entrega`
  - `fecha_carga`
  - `dias_retraso`
  - `tipo_operacion`
  - `cmv`
  - `fe_contab`

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: Ninguna
- **Archivos que importan a este archivo**: Ninguno
- **Archivos que este archivo importa**: Ninguno


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

## Archivo: ./db/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./db/consolidator.py

### Resumen Funcional
El archivo `consolidator.py` es un orquestador que gestiona la consolidación de datos en una base de datos SQLite para un sistema de monitoreo de almacén (WMS). Realiza tareas como la lectura, procesamiento y almacenamiento de archivos WMS, así como el enriquecimiento de los datos con información adicional.

### Catálogo de Funciones y Clases
- `DataConsolidator(db_path: str)` - Gestiona la consolidación de archivos WMS en SQLite.
  - `__init__(self, db_path: str)` - Inicializa el objeto con la ruta a la base de datos.
  - `__enter__(self)` - Establece la conexión a la base de datos y devuelve el objeto.
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
- Columnas (no detalladas por brevedad):
  - Todas las columnas relevantes para cada tabla mencionada.
- Consultas SQL crudas o llamadas a ORM: Sí, se utilizan funciones como `_enrich_with_stock`, `_backfill_movements`, etc., que probablemente implican consultas SQL.

### Estado y Variables Globales
- `logger` - Variable global de logging.
- `TABLE_DELIVERIES` - Constante con el nombre de la tabla de entregas.
- `TABLE_STOCK` - Constante con el nombre de la tabla de niveles de stock.

### Dependencias y Flujo
- Librerías externas: `logging`, `os`, `re`, `sqlite3`, `datetime`, `pathlib`, `typing`.
- Archivos del proyecto que este archivo importa:
  - `services.etl.OutboundDeliveryAdapter`
  - `services.etl.StockLevelAdapter`
  - `db_enrichment.apply_author_learning`
  - `db_enrichment.learn_author_areas`
  - `db_enrichment.backfill_deliveries_from_movements`
  - `db_enrichment.backfill_material_texts`
  - `db_enrichment.enrich_deliveries_with_stock`
  - `db_enrichment.update_sla_with_tasks`
- Archivos del proyecto que importan a este archivo:
  - Ninguno
- Flujo de datos: El flujo de datos pasa por el objeto `DataConsolidator`, que se encarga de la conexión a la base de datos, el procesamiento de archivos y el enriquecimiento de los datos.


---

## Archivo: ./db/db_enrichment.py

### Resumen Funcional
El archivo `db_enrichment.py` contiene funciones para enriquecer los datos de la base de datos SQLite del sistema de monitoreo de almacén (WMS) mediante consultas SQL directas y manipulación de DataFrames con Pandas. Las funciones realizan tareas como rellenar columnas vacías, actualizar mapeos de frecuencia, aplicar aprendizaje basado en autores, enriquecer transacciones con datos de stock y movimientos, y sincronizar métricas de SLA.

### Catálogo de Funciones y Clases
- `backfill_deliveries_from_movements(conn: sqlite3.Connection, trans_table: str = "outbound_deliveries", movements_table: str = "inventory_movements")` - Rellena columnas vacías en Entregas (autor, ubicacion, textos) cruzando con Movimientos.
- `learn_author_areas(conn: sqlite3.Connection)` - Actualiza el mapeo de frecuencia Autor -> Área.
- `apply_author_learning(conn: sqlite3.Connection, table_name: str = "outbound_deliveries")` - Asigna áreas de negocio a transacciones 'OTRO' basadas en la memoria del autor.
- `enrich_deliveries_with_stock(conn: sqlite3.Connection, trans_table: str = "outbound_deliveries", stock_table: str = "stock_levels")` - Enriquece transacciones con descripciones y ubicaciones físicas de Stock.
- `backfill_material_texts(conn: sqlite3.Connection)` - Rellena descripciones y UMBs faltantes en Entregas usando Stock y Movimientos como fuentes de verdad.
- `update_sla_with_tasks(conn: sqlite3.Connection)` - Actualiza la métrica de SLA en outbound_deliveries cruzando con la fecha de confirmación real en Tareas.
- `enrich_movements_with_iw39(conn: sqlite3.Connection)` - Enriquece la tabla inventory_movements con ceco_resp y autor provenientes de iw39_orders.

### Interacción con Base de Datos
- **Motor:** SQLite
- **TABLAS**: 
  - `outbound_deliveries`
  - `inventory_movements`
  - `stock_levels`
  - `warehouse_tasks`
  - `iw39_orders`
- **COLUMNAS**:
  - `outbound_deliveries`: entrega, autor, centro_costo, denominacion
  - `inventory_movements`: orden, ceco_resp, autor
  - `stock_levels`: material, texto_breve_de_material, ubicacion_bin, stock_disp, umb
  - `warehouse_tasks`: entrega, fecha_conf
  - `iw39_orders`: orden, ceco_resp, autor

### Estado y Variables Globales
- **Variables Globales**: Ninguna
- **Sesión**: Ninguna
- **Entorno**: Ninguna
- **Diccionarios Quemados**: Ninguno

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`
  - `pandas`
  - `logging`
  - `numpy`
- **Archivos del Proyecto que IMPORTA (consume)**: Ninguno
- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno
- **Dirección del Flujo de Datos**: El flujo de datos pasa por la lectura y escritura directa en la base de datos SQLite, con el procesamiento intermedio realizado mediante Pandas.


---

## Archivo: ./db/predictive_engine.py

### Resumen Funcional
El archivo `predictive_engine.py` procesa los movimientos de inventario para generar modelos predictivos utilizando técnicas como el Análisis del Carrocería (Market Basket Analysis), la Relación Frecuencia-Volumen y el Índice MTBV con Semáforo de Desplanificación. El objetivo es identificar patrones, anomalías y tendencias en los datos de inventario para mejorar la gestión del almacén.

### Catálogo de Funciones y Clases
- `generate_predictions(db_path: str)` - Procesa movimientos de inventario para generar modelos predictivos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `inventory_movements`
- **Columnas:** 
  - `fe_contab` (Fecha)
  - `ce_coste` (Centro de Costo)
  - `material` (Material)
  - `texto_breve_material` (Texto breve del material)
  - `cantidad` (Cantidad)
  - `cmv` (Código Movimiento)

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `logging`
  - `os`
  - `sqlite3`
  - `sys`
  - `collections.Counter`
  - `datetime`
  - `itertools.combinations`
  - `numpy`
  - `pandas`

- **Archivos del Proyecto que Importan a este Archivo:**
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.wms_config.COST_CENTER_MAPPING`

- **Flujo de Datos:**
  - El archivo importa configuraciones y dependencias necesarias.
  - Llama a la función `generate_predictions` con el camino a la base de datos.
  - La función procesa los datos, realiza análisis predictivos y devuelve resultados.

### Notas Adicionales
- La función `generate_predictions` maneja excepciones y registra errores utilizando `logging`.
- El archivo incluye un bloque de prueba al final para ejecutar la función y mostrar el número de combos, puntos de dispersión y alertas generados.


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

## Archivo: ./repositories/__init__.py

### Resumen Funcional
Este archivo es el punto de entrada para la definición de repositorios en el sistema de monitoreo de almacén (WMS). Define funciones que proporcionan instancias de diferentes tipos de repositorios, cada uno asociado con una tabla específica en la base de datos.

### Catálogo de Funciones y Clases
- `get_db()` - Obtiene una sesión de base de datos utilizando el motor SQLAlchemy.
- `get_deliveries_repo(session: Session = Depends(get_db)) -> DeliveriesRepository` - Devuelve una instancia del repositorio para manejar operaciones relacionadas con las entregas.
- `get_inventory_repo(session: Session = Depends(get_db)) -> InventoryRepository` - Devuelve una instancia del repositorio para manejar operaciones relacionadas con el inventario.
- `get_tasks_repo(session: Session = Depends(get_db)) -> TasksRepository` - Devuelve una instancia del repositorio para manejar operaciones relacionadas con las tareas.
- `get_productivity_repo(session: Session = Depends(get_db)) -> ProductivityRepository` - Devuelve una instancia del repositorio para manejar operaciones relacionadas con la productividad.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas y Columnas:
  - **DeliveriesRepository**: No especificado en el fragmento.
  - **InventoryRepository**: No especificado en el fragmento.
  - **TasksRepository**: No especificado en el fragmento.
  - **ProductivityRepository**: No especificado en el fragmento.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- Librerías externas: `sqlite3`, `fastapi`
- Archivos del proyecto que IMPORTA a este archivo:
  - `core.database.get_session` (importada dentro de `get_db`)
- Archivos del proyecto que este archivo IMPORTA:
  - `repositories.base.BaseRepository`
  - `repositories.deliveries.DeliveriesRepository`
  - `repositories.inventory.InventoryRepository`
  - `repositories.productivity.ProductivityRepository`
  - `repositories.tasks.TasksRepository`

Flujo de datos: Este archivo proporciona instancias de repositorios que consumen una sesión de base de datos, lo que permite a los servicios y rutas acceder a la lógica de acceso a datos.


---

## Archivo: ./repositories/base.py

### Resumen Funcional
Clase base para todos los repositorios de datos en el sistema WMS. Proporciona métodos para interactuar con la sesión de SQLAlchemy y verificar el estado visual de consultas.

### Catálogo de Funciones y Clases
- `BaseRepository(session: Session)` - Inicializa una instancia del repositorio con una sesión de SQLAlchemy.
- `_sql(query_id: str, fallback: str) -> str` - Devuelve un texto SQL basado en el ID de la consulta o un valor de reemplazo (fallback).
- `_has_visual_state(query_id: str) -> bool` - Verifica si una consulta tiene un estado visual JSON almacenado.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos.

### Estado y Variables Globales
Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Dependencias**: `sqlalchemy.orm.Session`, `core.db_config_manager.get_query_visual_state`.
- **Flujo de Datos**: El archivo no consume ni produce datos externos. Se utiliza para proporcionar métodos comunes a los repositorios de datos en el sistema WMS.


---

## Archivo: ./repositories/dashboard.py

### Resumen Funcional
El archivo `dashboard.py` contiene funciones para obtener datos filtrados y estadísticas necesarios para el dashboard principal del sistema de monitoreo de almacén (WMS). Estas funciones interactúan con la base de datos SQLite para recuperar información sobre entregas, KPIs, gráficos de intensidad y selectores para el dashboard.

### Catálogo de Funciones y Clases
- `build_unified_where(date: Optional[str], area: Optional[str], centro: Optional[str], has_ots_filter: Optional[str], min_week: Optional[str])` - Construye una cláusula WHERE unificada basada en los filtros proporcionados.
- `get_filtered_transactions(date: Optional[str], entrega: Optional[str], area: Optional[str], centro: Optional[str], has_ots_filter: Optional[str], min_week: Optional[str]) -> list` - Obtiene transacciones filtradas y las devuelve como una lista de diccionarios.
- `get_filtered_kpis(date: Optional[str], area: Optional[str], centro: Optional[str], min_week: Optional[str], iso_year: int) -> dict` - Calcula KPIs basados en los filtros proporcionados y el año especificado.
- `get_weekly_intensity_chart(year: int) -> dict` - Prepara datos para un gráfico de intensidad semanal.
- `get_dashboard_selectors(min_week: str) -> dict` - Obtiene listas únicas de fechas, áreas, mapeos de autores y centros.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `outbound_deliveries`, `config_cost_center_mapping`, `autor_area_mapping`
- **Columnas:**
  - `outbound_deliveries`: `fecha_carga`, `fecha_sm_real`, `creado_el`, `entrega`, `material`, `estado_wms`, `dias_retraso`, `week_sort`, `area_negocio`, `centro_costo`, `ubicacion_bin_1`, `ubicacion_bin`
  - `config_cost_center_mapping`: `center_code`, `business_area`
  - `autor_area_mapping`: `autor`, `area_negocio`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `pandas`, `sqlalchemy`
- **Archivos del Proyecto que Importan a este Archivo:**
  - Ninguno
- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.macros` (importado en `build_unified_where`)
- **Dirección del Flujo de Datos:** El archivo consume datos de la base de datos y los procesa para devolver resultados al servicio o controlador que lo invoque.


---

## Archivo: ./repositories/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene métodos para interactuar con la base de datos SQLite y obtener registros relacionados con entregas en un sistema de monitoreo de almacén (WMS). Los métodos permiten consultar registros de entrega, realizar auditorías SLA, obtener detalles de entregas por lotes y recuperar información sobre áreas de negocio.

### Catálogo de Funciones y Clases
- `DeliveriesRepository(BaseRepository)` - Repositorio para el dominio de Entregas (outbound_deliveries).
  - `_sql(query_id: str, fallback: str) -> str` - Obtiene SQL desde config_queries con fallback explícito.
  - `_get_sla_threshold() -> int` - Retorna el umbral SLA configurado en la base de datos.
  - `get_sla_audit_records(year: str, late: bool = True, limit: int = 500, where_clause: Optional[str] = None, where_params: Optional[dict] = None) -> pd.DataFrame` - Obtiene registros de auditoría SLA para entregas.
  - `get_deliveries_for_bulk(date: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, entrega_query: Optional[str] = None) -> pd.DataFrame` - Obtiene detalles de entregas por lotes.
  - `get_area_lookup() -> pd.DataFrame` - Obtiene un mapeo de entregas a áreas de negocio.
  - `get_picking_items(entrega_ids: list) -> pd.DataFrame` - Obtiene los elementos de picking para una lista de entregas.
  - `get_delivery_by_id(entrega: str) -> pd.DataFrame` - Obtiene detalles de una entrega específica por su ID.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: `outbound_deliveries`
    - Columnas: `entrega`, `autor`, `area_negocio`, `creado_el`, `fecha_sm_real`, `material`, `denominacion`, `dias_retraso`, `estado_wms`, `ubicacion_bin`, `cantidad`, `umb`, `week_sort`.
  - Tabla: `warehouse_tasks`
    - Columnas: `entrega`.
  - Tabla: `DeliverySummary`
    - Columnas: `entrega_id`.

### Estado y Variables Globales
- **Variables Globales:** Ninguna.
- **Variables de Sesión:** Ninguna.
- **Diccionarios Quemados en Código:** Ninguno.

### Dependencias y Flujo
- **Librerías Externas:** pandas, sqlalchemy
- **Archivos del Proyecto que Importan a este Archivo:**
  - `core.db_config_manager`
  - `core.macros`
  - `repositories.base`
- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno.

**Flujo de Datos:** El archivo interactúa con la base de datos SQLite para ejecutar consultas SQL y devolver resultados en formato DataFrame.


---

## Archivo: ./repositories/inventory.py (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
Este archivo contiene métodos para interactuar con la base de datos SQLite y obtener información sobre movimientos de inventario y consumos. Los métodos incluyen consultas históricas, del mes actual, por materiales específicos y sugerencias de reabastecimiento.

### Catálogo de Funciones y Clases
- `get_consumos_ceco(ceco: str) -> dict`: Obtiene los consumos históricos y del mes actual para un centro de costo específico.
- `get_consumos_materiales(materiales: list) -> dict`: Obtiene los consumos históricos y del mes actual para una lista de materiales.
- `get_material_trend(material: str, area_negocio: str, ceco: str) -> dict`: Obtiene el trend de un material específico por área y centro de costo.
- `check_table_exists() -> bool`: Verifica si la tabla 'inventory_movements' existe en la base de datos.
- `get_cmv_summary(cmv_type: str, plan_type: str, year: Optional[str] = None) -> list`: Obtiene un resumen de movimientos según el tipo CMV y el tipo de planificación.
- `get_cmv_area_details(cmv_type: str, plan_type: str, area: str, mes: Optional[str] = None, year: Optional[str] = None) -> list`: Obtiene detalles de los movimientos por área y centro de costo.
- `get_replenishment_suggestions(freq: str) -> dict`: Genera sugerencias de reabastecimiento basadas en la frecuencia de consumo.
- `get_replenishment_export_data() -> tuple[pd.DataFrame, pd.DataFrame]`: Exporta datos para el reabastecimiento.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: 
  - `inventory_movements`
  - `outbound_deliveries`
  - `config_cost_center_mapping`
  - `mb5b_initial_stock`
- **Columnas**:
  - `inventory_movements`: material, texto_breve_material, umb, cantidad, importe_ml, cmv, fe_contab, ce_coste
  - `outbound_deliveries`: centro_costo, area_negocio
  - `config_cost_center_mapping`: center_code, business_area
  - `mb5b_initial_stock`: material, stock_inicial

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**: pandas
- **Archivos del Proyecto que Importan a este Archivo**:
  - Repositorio de servicios (Services)
  - Rutas (Routes)
- **Archivos del Proyecto que Este Archivo Importa**:
  - `core.utils.sanitize_for_json`
  - `base.BaseRepository`

El flujo de datos es desde el repositorio hacia los servicios y rutas, pasando por la base de datos SQLite para obtener y procesar los datos.


---

## Archivo: ./repositories/productivity.py

### Resumen Funcional
El archivo `productivity.py` contiene métodos para obtener resúmenes diarios y mensuales de la productividad de usuarios en un sistema de almacén, utilizando datos de movimientos de inventario y tareas del almacén. Los resultados se devuelven como listas de diccionarios.

### Catálogo de Funciones y Clases
- `_get_raw_activities_cte(is_monthly=False)`: Genera una Common Table Expression (CTE) con todos los eventos de actividad, unificando datos de movimientos de inventario y tareas del almacén.
- `get_available_dates()`: Devuelve una lista ordenada de fechas únicas en formato YYYY-MM-DD que tienen movimientos generados o confirmados.
- `get_all_users()`: Retorna la lista completa de usuarios con actividad para poblar filtros y agrupaciones.
- `_get_daily_summary(date_sap)`: Calcula el resumen diario de productividad por usuario, incluyendo movimientos generados, tareas confirmadas, tiempo total en minutos.
- `_get_hourly_trend(date_sap)`: Genera un trend horario de actividad por usuario.
- `_get_inactivity_gaps(date_sap)`: Identifica los huecos de inactividad por usuario.
- `_get_activity_heatmap(date_sap)`: Crea un mapa de calor de actividad por franja horaria y usuario.
- `get_user_movements_daily_summary(target_date, usuario)`: Devuelve el resumen diario de movimientos para un usuario específico.
- `get_user_movements_daily_details(target_date, usuario, operacion)`: Detalla los movimientos diarios para un usuario y una operación específica.
- `_get_monthly_summary(month_sap)`: Calcula el resumen mensual de productividad por usuario, incluyendo días trabajados y promedio de actividad diaria.
- `_get_monthly_shifts(month_sap)`: Genera un resumen de turnos (mañana, tarde, noche) por usuario y fecha.
- `_get_monthly_heatmap(month_sap)`: Crea un mapa de calor de actividad mensual por día de la semana y usuario.
- `get_user_movements_monthly_summary(target_month, usuario)`: Devuelve el resumen mensual de movimientos para un usuario específico.
- `get_user_movements_monthly_details(target_month, usuario, operacion)`: Detalla los movimientos mensuales para un usuario y una operación específica.
- `_format_date_sap(target_date)`: Formatea una fecha en formato SAP (DD.MM.YYYY).
- `_format_month_sap(target_month)`: Formatea un mes en formato SAP (MM.YYYY).

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `inventory_movements`
  - `warehouse_tasks`
- Columnas:
  - `inventory_movements`: `usuario`, `registrado`, `hora`, `doc_mat`, `tipo_operacion`, `texto_cab_documento`, `cmv`, `material`, `texto_breve_material`, `cantidad`
  - `warehouse_tasks`: `usuario_conf`, `fecha_conf`, `hor_conf`, `numero_ot`, `ctd_teor_dsd`

### Estado y Variables Globales
- No hay variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- Librerías externas: `logging`, `re`, `pandas`
- Archivos del proyecto que importa:
  - `core.macros`: `EXCLUDED_USERS_INACTIVITY`
  - `.base`: `BaseRepository`
- Archivos del proyecto que son importados por este archivo:
  - Ninguno
- Flujo de datos: El archivo consume datos de la base de datos y los procesa para devolver resultados en formato de lista de diccionarios.


---

## Archivo: ./repositories/tasks.py

### Resumen Funcional
El archivo `tasks.py` contiene métodos para obtener resúmenes y detalles de tareas en un sistema de almacén (WMS). Estos métodos interactúan con una base de datos SQLite para recuperar información sobre las tareas, incluyendo estadísticas de resumen, tendencias diarias, usuarios que realizan más tareas, tipos de movimiento, tareas recientes y movimientos no palletizados.

### Catálogo de Funciones y Clases
- `get_tasks_summary()` - Devuelve un DataFrame con el resumen de las tareas agrupadas por tipo.
- `get_tasks_trend()` - Devuelve un DataFrame con la tendencia diaria de creación y confirmación de tareas.
- `get_tasks_by_user()` - Devuelve un DataFrame con las tareas realizadas por cada usuario en el último mes.
- `get_tasks_by_type_dest()` - Devuelve un DataFrame con el resumen de las tareas agrupadas por tipo de movimiento.
- `get_recent_tasks()` - Devuelve un DataFrame con las tareas recientes que no han sido confirmadas.
- `get_non_palletized_movements()` - Devuelve un DataFrame con los movimientos no palletizados más recientes.
- `get_non_palletized_count()` - Devuelve el número de movimientos no palletizados.
- `get_non_palletized_summary()` - Devuelve un DataFrame con el resumen de los movimientos no palletizados, incluyendo la fecha más antigua y más reciente.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `warehouse_tasks`
  - `lx02_pendientes`
  - `inventory_movements`
- Columnas:
  - `cl_mov`, `clase_mov`, `COUNT(*)`, `SUM(ctd_teor_dsd)`, `fe_creac`, `fecha_conf`, `usuario`, `usuario_conf`, `numero_ot`, `material`, `texto_breve_material`, `ubic_proc`, `ubic_dest`, `hora`, `otcuanto`, `pos`, `stock_disp`, `alm`, `ce`, `cmv`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas: `pandas`
- Archivos del proyecto que importan a este archivo:
  - Ninguno
- Archivos del proyecto que este archivo importa:
  - `base.py` (clase base `BaseRepository`)
- Flujo de datos: El archivo consume métodos y funciones de la clase base para interactuar con la base de datos y procesar los resultados en DataFrames de pandas.


---

## Archivo: ./repositories/widgets.py

### Resumen Funcional
El archivo `widgets.py` contiene métodos para ejecutar visualizaciones de datos en un sistema de monitoreo de almacén (WMS). Los métodos procesan solicitudes de usuario, aplican filtros y generan gráficos basados en los datos del almacén.

### Catálogo de Funciones y Clases
- `execute_widget(query_id: str, visual_state: str, year: Optional[str], area: Optional[str], granularity: Optional[str]) -> Dict[str, Any]` - Ejecuta una consulta para generar un gráfico basado en los filtros proporcionados.
- `execute_drilldown(query_id: str, visual_state: str, segment: str, material: Optional[str], year: Optional[str]) -> list` - Realiza una exploración adicional de datos para obtener detalles más específicos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: `outbound_deliveries`
    - Columnas: `fecha_carga`, `entrega`, `pos_`, `cantidad`, `dias_retraso`, `material`, `denominacion`
  - Tabla: `tareas` (implícita en el código)
    - Columna: `dim_fecha`

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:** pandas, sqlalchemy, json, logging, datetime
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.helpers.dynamic_executor.execute_visual_query`
  - `core.query_engine.build_sql_from_payload`
  - `core.schemas.VisualQueryBuilderPayload`
  - `core.utils.sanitize_for_json`
  - `base.BaseRepository`

**Flujo de Datos:**
1. `widgets.py` importa funciones y clases necesarias.
2. Los métodos `execute_widget` y `execute_drilldown` procesan los datos según las solicitudes del usuario.
3. Utilizan `pandas` para leer y manipular los datos desde la base de datos SQLite.
4. Generan gráficos o listas de datos basados en los filtros aplicados.

Este archivo es crucial para el funcionamiento del sistema de monitoreo de almacén, proporcionando funcionalidades avanzadas de visualización y exploración de datos.


---

## Archivo: ./routes/__init__.py

### Resumen Funcional
El archivo `__init__.py` es el inicializador del paquete `routes`, encargado de cargar las rutas dinámicamente a través del archivo `config.py`.

### Catálogo de Funciones y Clases
Ninguna.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias directas en este archivo.
- **Flujo**: Este archivo no importa ni es importado por otros archivos dentro del proyecto. Es un inicializador de paquete que carga rutas dinámicamente a través de `config.py`.


---

## Archivo: ./routes/analytics_proyecciones.py

### Resumen Funcional
Este archivo define las rutas para obtener analíticas de proyecciones en un sistema de monitoreo de almacén (WMS). Permite refrescar los datos si es necesario y utiliza una caché para mejorar el rendimiento.

### Catálogo de Funciones y Clases
- `get_proyecciones_context()` - Obtiene el contexto de proyecciones, priorizando la caché.
- `get_analytics_proyecciones(request: Request, force_refresh: bool = False, cache: CacheManager = Depends(get_cache_manager))` - Retorna los datos de proyecciones en formato JSON.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna (el archivo no interactúa directamente con la base de datos).

### Estado y Variables Globales
- `DB_PATH` - Ruta a la base de datos SQLite.
- `CacheManager` - Gestor de caché utilizado para almacenar los resultados de las proyecciones.

### Dependencias y Flujo
- Librerías externas: FastAPI, SQLAlchemy, config.py, core.auth, core.state, db.predictive_engine.
- Archivos del proyecto que importan a este archivo: Ninguno.
- Archivos del proyecto que este archivo importa:
  - `config.py` - Para obtener la ruta de la base de datos.
  - `core/auth.py` - Para autenticar el usuario actual.
  - `core/state.py` - Para gestionar la caché.
  - `db/predictive_engine.py` - Para generar las predicciones.

El flujo de datos es: el cliente hace una solicitud a `/analytics/proyecciones`, que luego llama a `get_proyecciones_context()` para obtener los datos. Si `force_refresh` es True, se limpia la caché antes de obtener los nuevos datos. Los datos son generados por `generate_predictions(_DB)` y almacenados en caché si no hay errores. Finalmente, los datos se devuelven al cliente en formato JSON.


---

## Archivo: ./routes/auth.py

### Resumen Funcional
El archivo `auth.py` contiene endpoints para autenticación y gestión de usuarios en un sistema de monitoreo de almacén (WMS) utilizando FastAPI, SQLAlchemy y SQLite. Los endpoints permiten login con username/password, registro de nuevos usuarios (solo por administradores), obtención de información del usuario autenticado, cambio de contraseña y listado de todos los usuarios (también solo para administradores). Además, proporciona una vista HTML para el formulario de login.

### Catálogo de Funciones y Clases
- `login(response: Response, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session_dep))` - Autentica un usuario con username/password y retorna un JWT.
- `logout(response: Response)` - Limpia la cookie de autenticación.
- `get_me(user: User = Depends(require_auth))` - Retorna la información del usuario autenticado.
- `change_password(data: ChangePasswordRequest, db: DBSession, user: User = Depends(require_auth))` - Cambia la contraseña del usuario autenticado.
- `register_user(data: UserCreate, db: DBSession, admin: User = Depends(require_admin))` - Crea un nuevo usuario. Solo accesible por administradores.
- `list_users(db: DBSession, admin: User = Depends(require_admin))` - Lista todos los usuarios del sistema.
- `login_page(request: Request)` - Renderiza la página de login.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `User`
- **Columnas:** 
  - `id`
  - `username`
  - `password_hash`
  - `role`
  - `is_active`
  - `created_at`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - FastAPI
  - SQLAlchemy
  - Python Standard Library (logging, typing)

- **Archivos del Proyecto que Importan a este Archivo (`auth.py`):** Ninguno

- **Archivos del Proyecto que Este Archivo Importa (`auth.py`):**
  - `core.app_instance`
  - `core.auth`
  - `core.database`
  - `core.models_auth`

- **Flujo de Datos:**
  - El archivo importa dependencias necesarias y define endpoints para autenticación y gestión de usuarios.
  - Los endpoints interactúan con la base de datos a través de funciones definidas en otros módulos (`core.auth`, `core.database`, etc.).
  - La interacción con la base de datos se realiza mediante consultas SQL generadas por SQLAlchemy.

Este archivo es crucial para el manejo de autenticación y gestión de usuarios en el sistema WMS, asegurando que solo los usuarios autorizados puedan realizar ciertas acciones y proporcionando mecanismos seguros para el login y cambio de contraseña.


---

## Archivo: ./routes/config.py

### Resumen Funcional
El archivo `config.py` es un módulo que se encarga de registrar todos los routers de la aplicación FastAPI de forma centralizada. Incluye manejo de errores básico para evitar que un router mal configurado detenga el arranque completo del servidor.

### Catálogo de Funciones y Clases
- `register_routes(app: FastAPI) -> None` - Registra todos los routers de la aplicación de forma centralizada, incluyendo manejo de errores.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `ROUTER_MODULES: List[str]` - Lista declarativa de nombres de módulos de routers a importar dinámicamente.
- `ROUTERS: List[APIRouter]` - Lista que almacena los objetos `APIRouter` registrados.

### Dependencias y Flujo
- **Dependencias**: Importa `importlib`, `logging`, `typing.List` desde el módulo estándar de Python. Importa `FastAPI` y `APIRouter` desde `fastapi`.
- **Flujo**: El archivo importa dinámicamente los módulos de routers especificados en `ROUTER_MODULES`, intenta registrar cada router con la aplicación FastAPI, y registra errores si ocurren durante el proceso.


---

## Archivo: ./routes/consumos.py

### Resumen Funcional
Este archivo contiene endpoints para obtener datos de consumos en un sistema de almacén (WMS) utilizando FastAPI. Permite consultar los consumos agrupados por material y ceco, así como el consumo mensual de materiales específicos.

### Catálogo de Funciones y Clases
- `get_consumos_ceco(ceco: str, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Obtiene los consumos agrupados por material para un CeCo específico.
- `get_consumos_materiales(req: MaterialesRequest, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Obtiene que CeCos han consumido una lista de materiales.
- `get_material_trend(req: MaterialTrendRequest, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Devuelve el consumo mensual de un material específico, filtrado por área de negocio.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `inventory_movements`
- Columnas:
  - `doc_mat`, `ej_mat`, `pos`

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `pandas`
  - `fastapi`
  - `pydantic`
  - `sqlalchemy`
- Archivos del proyecto que este archivo importa:
  - `core.auth.get_current_user`
  - `core.database.get_session_dep`
  - `repositories.inventory.InventoryRepository`
- Archivos del proyecto que importan a este archivo:
  - Ninguno

El flujo de datos es desde los endpoints hasta el repositorio, donde se realizan las consultas a la base de datos.


---

## Archivo: ./routes/dashboard.py

### Resumen Funcional
El archivo `dashboard.py` contiene rutas para el dashboard de un sistema de monitoreo de almacén (WMS). Ofrece endpoints para obtener ubicaciones de materiales y cargar la vista principal del dashboard con KPIs.

### Catálogo de Funciones y Clases
- `get_ubicaciones(material: str, user = Depends(get_current_user), session: Session = Depends(get_session_dep))` - Obtiene las ubicaciones de un material específico.
- `dashboard(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager), sync: SyncStateManager = Depends(get_sync_manager))` - Vista principal del Dashboard con KPIs y búsqueda rápida.
- `dashboard_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager), sync: SyncStateManager = Depends(get_sync_manager))` - API JSON para el Dashboard con KPIs y búsqueda rápida.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `stock_levels`, `warehouse_tasks`
- **Columnas:**
  - `stock_levels`: `ubicacion_bin`, `Ubicación`, `ubicacin`, `denominacion`, `Texto breve de material`, `stock_disp`, `umb`, `ubic_actual`
  - `warehouse_tasks`: `ubic_dest`, `fecha_conf`, `fe_creac`, `material`, `tp_dest`, `ubic_dest`

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `fastapi`
  - `sqlalchemy`
  - `logging`
- **Archivos del Proyecto que Importan a este Archivo (`dashboard.py`):** Ninguno
- **Archivos del Proyecto que Este Archivo Importa (`dashboard.py`):**
  - `core.app_instance.templates`
  - `core.auth.get_current_user`
  - `core.database.get_session_dep`
  - `core.schemas.DashboardResponse`
  - `core.state.CacheManager`, `core.state.SyncStateManager`
  - `core.db_config_manager.get_user_groups`
  - `services.dashboard_service.DashboardService`

**Flujo de Datos:**
1. **Entrada:** Requiere un usuario autenticado y una sesión de base de datos.
2. **Procesamiento:**
   - Para `get_ubicaciones`: Consulta la tabla `stock_levels` para obtener las ubicaciones del material especificado.
   - Para `dashboard` y `dashboard_api`: Utiliza el servicio `DashboardService` para obtener el contexto completo del negocio, que luego se almacena en caché.
3. **Salida:** Devuelve datos en formato JSON o HTML según la solicitud.

**Nota:** El archivo no realiza consultas SQL crudas directamente; en su lugar, utiliza SQLAlchemy ORM y pandas para manipular los datos.


---

## Archivo: ./routes/deliveries.py

### Resumen Funcional
Este archivo contiene rutas para el sistema de monitoreo de almacén (WMS) que proporcionan análisis y detalles sobre entregas. Incluye endpoints para renderizar páginas web con datos de entrega, obtener detalles detallados de movimientos no paletizados y proporcionar una API JSON con analíticas de entregas.

### Catálogo de Funciones y Clases
- `analytics(request: Request, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Renderiza la página principal de analíticas.
- `sla_details(request: Request, type: str="late", date: Optional[str]=None, area: Optional[str]=None, centro: Optional[str]=None, has_ots_filter: Optional[str]=None, session: Session=Depends(get_session_dep))` - Vista detallada de auditoría SLA.
- `get_non_palletized_details(user: str, clase_mov: str, db: Session=Depends(get_session_dep), current_user: Dict[str, Any]=Depends(get_current_user))` - Obtiene el listado detallado de movimientos no paletizados para un usuario y tipo de movimiento específicos.
- `analytics_deliveries_api(user=Depends(get_current_user), session: Session=Depends(get_session_dep), sync: SyncStateManager=Depends(get_sync_manager))` - API JSON para analíticas de Entregas con caché multinivel.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - `lx02_pendientes`: `otcuanto`, `material`, `stock_disp`
  - `inventory_movements`: `doc_mat`, `usuario`, `cmv`, `alm`, `ce`, `fe_contab`, `hora`

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `fastapi`
  - `sqlalchemy`
  - `logging`
  - `datetime`
  - `json`
  - `typing`

- **Archivos del Proyecto que Importan a este Archivo (lo consumen):** Ninguno

- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.app_instance.templates`
  - `core.auth.get_current_user`
  - `core.database.get_session_dep`
  - `core.schemas.AnalyticsDeliveriesResponse`
  - `core.state.SyncStateManager.get_sync_manager`
  - `core.utils.sanitize_for_json`
  - `repositories.DeliveriesRepository`
  - `services.deliveries_service.DeliveriesService`

- **Dirección del Flujo de Datos:**
  - Desde el endpoint hasta la base de datos para obtener los datos necesarios.
  - Desde la base de datos hasta el servicio para procesar y formatear los datos.
  - Desde el servicio hasta las vistas para renderizar la información.


---

## Archivo: ./routes/docs.py

### Resumen Funcional
El archivo `docs.py` proporciona endpoints para generar y obtener la documentación del sistema de monitoreo de almacén (WMS). Ofrece una vista jerárquica de los archivos del proyecto con indicadores de si tienen documentación, así como un endpoint para leer el contenido específico de las documentaciones.

### Catálogo de Funciones y Clases
- `get_docs_tree()` - Genera un árbol de archivos del proyecto indicando cuáles tienen documentación.
- `get_doc_content(path: str)` - Obtiene el contenido de la documentación (.md) para un archivo específico.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `BASE_DIR` - Directorio base del proyecto.
- `CACHE_DIR` - Directorio donde se almacenan las copias en caché de las documentaciones.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directamente importadas.
- **Flujo de Datos**:
  - `get_docs_tree()` genera un árbol jerárquico de archivos del proyecto, identificando cuáles tienen documentación.
  - `get_doc_content(path: str)` intenta leer el contenido de una documentación desde la carpeta real o desde el caché, y devuelve su contenido.

**Flujo detallado**:
1. **`get_docs_tree()`**:
   - Recorre los archivos del proyecto, ignorando ciertos directorios y extensiones.
   - Construye un árbol jerárquico con información sobre cada archivo/documentación.
   - Ordena el árbol primero por carpetas y luego por archivos, alfabéticamente.
   - Añade una opción destacada para la documentación global.

2. **`get_doc_content(path: str)`**:
   - Intenta leer el contenido de un archivo `.md` desde la carpeta real del proyecto.
   - Si no existe en la carpeta real, intenta leerlo desde el caché.
   - Devuelve el contenido del archivo si lo encuentra, o lanza una excepción `HTTPException` 404 si no se encuentra.


---

## Archivo: ./routes/filters.py

### Resumen Funcional
El archivo `filters.py` contiene endpoints para filtrar transacciones y calcular KPIs en un sistema de monitoreo de almacén (WMS) utilizando FastAPI, SQLAlchemy y SQLite. Ofrece funcionalidades para obtener datos filtrados por múltiples criterios y calcular indicadores clave de rendimiento (KPIs).

### Catálogo de Funciones y Clases
- `_build_unified_where(date: Optional[str], area: Optional[str], centro: Optional[str], has_ots: Optional[str], min_week: Optional[str]) -> tuple[str, dict]` - Construye una cláusula WHERE unificada basada en los criterios de filtro proporcionados.
- `filter_transactions(request: Request, date: Optional[str], entrega: Optional[str], area: Optional[str], centro: Optional[str], has_ots_filter: Optional[str], session: Session = Depends(get_session_dep))` - Filtra entregas según múltiples criterios y devuelve los resultados.
- `get_kpis(date: Optional[str], entrega: Optional[str], area: Optional[str], centro: Optional[str], has_ots_filter: Optional[str], session: Session = Depends(get_session_dep))` - Calcula KPIs dinámicos filtrados por área para el dashboard.
- `api_widget_data(query_id: str, request: Request, session: Session = Depends(get_session_dep))` - Endpoint de carga asíncrona para los componentes del Dashboard, lee visual_state, compila SQL y retorna los datos JSON directamente.

### Interacción con Base de Datos
- Motor de BD: SQLite.
- Tablas:
  - `warehouse_tasks`
  - `ConfigQuery`
- Columnas:
  - `v.fecha_carga`, `v.fecha_sm_real`, `v.creado_el` (de la tabla `v`)
  - `l.entrega` (de la tabla `warehouse_tasks`)
  - `v.week_sort` (de la tabla `v`)
  - `area_expr` (de la tabla `v`)
  - `entrega` (de la tabla `ConfigQuery`)
  - `visual_state` (de la tabla `ConfigQuery`)
- Consultas SQL crudas: Sí, se utilizan consultas SQL generadas dinámicamente.

### Estado y Variables Globales
- Variables globales:
  - `DATE_EXPR`: Expresión unificada para la fecha de carga.
  - `ALLOWED_OTS_STATES`: Conjunto de estados OT permitidos como filtro.

### Dependencias y Flujo
- Librerías externas: `pandas`, `fastapi`, `sqlalchemy`.
- Archivos del proyecto que importa:
  - `config.py`
  - `core.database`
  - `core.models`
  - `core.query_engine`
  - `core.schemas`
  - `core.utils`
  - `repositories.deliveries`
  - `repositories.dashboard`
- Archivos del proyecto que son importados por este archivo:
  - Ninguno.
- Flujo de datos: El flujo de datos pasa a través de los endpoints, donde se reciben parámetros de filtro, se construyen consultas SQL dinámicas y se ejecutan contra la base de datos SQLite. Los resultados se procesan y devuelven al cliente en formato JSON.


---

## Archivo: ./routes/inventory.py

### Resumen Funcional
El archivo `inventory.py` contiene rutas y lógica para el análisis de inventario en un sistema de gestión de almacén (WMS). Ofrece una redirección a la página de analíticas de inventario y una API que devuelve datos de inventario limpios.

### Catálogo de Funciones y Clases
- `analytics_inventory_redirect(request: Request)` - Redirige a la página de analíticas de inventario.
- `get_inventory_context(session: Session) -> Dict[str, Any]` - Obtiene el contexto completo del inventario.
- `analytics_inventory_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), sync: SyncStateManager = Depends(get_sync_manager))` - API que devuelve datos de inventario limpios.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: `pandas`, `fastapi`, `sqlalchemy`.
- **Archivos del Proyecto que IMPORTA**:
  - `core.auth.get_current_user`
  - `core.database.get_session_dep`
  - `core.schemas.AnalyticsInventoryResponse`
  - `core.state.SyncStateManager`
  - `core.utils.sanitize_for_json`
  - `core.wms_config.COST_CENTER_MAPPING`
  - `repositories.InventoryRepository`
  - `routes.analytics_proyecciones.get_proyecciones_context`
  - `services.inventory_service.InventoryService`
- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno.

**Flujo de Datos**:
1. El usuario accede a la ruta `/inventory`, lo cual es redirigido a `/analytics?tab=inventory`.
2. Para la API `/api/v1/analytics/inventory`, se obtiene el contexto del inventario utilizando `InventoryService` y se filtran los datos para eliminar campos no deseados (`'request', 'user', 'is_syncing'`). El resultado se devuelve como una respuesta JSON con el modelo `AnalyticsInventoryResponse`.


---

## Archivo: ./routes/pdf.py

### Resumen Funcional
Este archivo contiene rutas FastAPI para generar PDFs relacionados con el sistema de monitoreo de almacén (WMS). Ofrece dos endpoints: uno para generar un PDF individual y otro para generar un reporte masivo.

### Catálogo de Funciones y Clases
- `generate_pdf(entrega, include_logo, action, session)` - Genera un PDF para una única entrega.
- `generate_pdf_bulk(date, entrega_query, area, centro, has_ots_filter, include_logo, action, session)` - Genera un reporte masivo con índice y picking list.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:**
  - `DeliveriesRepository` interactúa con la tabla que contiene los detalles de las entregas.
- **Columnas:**
  - En `generate_pdf`, se accede a columnas como `entrega`, `include_logo`, `action`.
  - En `generate_pdf_bulk`, se acceden a columnas como `date`, `entrega_query`, `area`, `centro`, `has_ots_filter`.

### Estado y Variables Globales
- **Variables Globales:** Ninguna.
- **Sesiones de Usuario:** Ninguna.
- **Entorno:** Ninguna.
- **Diccionarios Quemados:** Ninguno.

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `fastapi`
  - `sqlalchemy`
  - `logging`
  - `io`

- **Archivos del Proyecto que Importa a este Archivo (Consumo):**
  - `config.py` (para constantes como `DB_PATH`, `PDF_STORAGE`)
  - `core.database.get_session_dep` (dependencia para obtener la sesión de base de datos)
  - `core.pdf_engine.WMS_Landscape_PDF`
  - `core.pdf_reports.draw_annex_table`
  - `core.pdf_reports.draw_picking_list`
  - `repositories.deliveries.DeliveriesRepository`

- **Archivos del Proyecto que este Archivo Importa (Lo Consumen):**
  - Ninguno.

**Flujo de Datos:**
1. El usuario accede a las rutas `/generate-pdf` o `/generate-pdf-bulk`.
2. Se inicia una sesión de base de datos.
3. Se obtienen los datos necesarios desde la base de datos usando `DeliveriesRepository`.
4. Se genera el PDF utilizando `WMS_Landscape_PDF` y funciones auxiliares (`draw_delivery_page`, `get_ots_for_delivery`, etc.).
5. El PDF se devuelve al usuario como una respuesta HTTP con tipo MIME `application/pdf`.


---

## Archivo: ./routes/productivity.py

### Resumen Funcional
El archivo `productivity.py` contiene endpoints para obtener datos de productividad diaria y mensual en un sistema de almacén (WMS) utilizando FastAPI. Los endpoints permiten consultar fechas disponibles, resúmenes diarios y mensuales de movimientos de usuarios, así como detalles específicos de estos movimientos.

### Catálogo de Funciones y Clases
- `get_available_dates(user: User, session: Session)` - Retorna las fechas disponibles para el análisis de productividad.
- `get_productivity_dashboard(date: str = Query(None), user: User, session: Session, cache: CacheManager, sync: SyncStateManager)` - Retorna los datos del dashboard de productividad para una fecha específica o por defecto "Ayer".
- `get_monthly_productivity(month: str = Query(None), user: User, session: Session, cache: CacheManager, sync: SyncStateManager)` - Retorna los KPIs mensuales de productividad.
- `get_user_movements_summary(date: str, usuario: str, user: User, session: Session)` - Retorna el resumen diario de movimientos de un usuario para una fecha específica.
- `get_user_movements_details(date: str, usuario: str, operacion: str, user: User, session: Session)` - Retorna los detalles diarios de movimientos de un usuario para una fecha específica y tipo de operación.
- `get_user_movements_monthly_summary(month: str, usuario: str, user: User, session: Session)` - Retorna el resumen mensual de movimientos de un usuario para un mes específico.
- `get_user_movements_monthly_details(month: str, usuario: str, operacion: str, user: User, session: Session)` - Retorna los detalles mensuales de movimientos de un usuario para un mes específico y tipo de operación.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQLite a través de SQLAlchemy. Las consultas específicas no están detalladas en el código proporcionado, pero se infiere que las funciones `get_available_dates`, `get_productivity_data`, `get_monthly_productivity_data`, `get_user_movements_daily_summary`, `get_user_movements_daily_details`, `get_user_movements_monthly_summary`, y `get_user_movements_monthly_details` realizan consultas a la base de datos para obtener los datos necesarios.

### Estado y Variables Globales
No se detectaron variables globales, de sesión o de entorno en el código proporcionado.

### Dependencias y Flujo
- **Dependencias**: El archivo importa dependencias desde `core.auth`, `core.database`, `services.productivity_daily`, y `services.productivity_monthly`.
- **Flujo de Datos**: Los datos fluyen a través del endpoint, se procesan en los servicios correspondientes (`ProductivityDailyService` y `ProductivityMonthlyService`), y luego se devuelven al cliente. El flujo incluye la obtención de datos desde la base de datos, su procesamiento y almacenamiento en caché si es necesario.

Este archivo es una parte integral del sistema de monitoreo de almacén, proporcionando endpoints para obtener diversos tipos de datos de productividad, con un enfoque en la eficiencia y el seguimiento de los movimientos de usuarios.


---

## Archivo: ./routes/settings.py

### Resumen Funcional
El archivo `settings.py` contiene endpoints para la gestión dinámica de configuraciones en un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Permite actualizar y gestionar configuraciones generales, grupos de usuarios, feriados, estados, costos centrales y consultas SQL.

### Catálogo de Funciones y Clases
- `invalidate_caches(db: Session)` - Limpia el caché global en memoria y elimina todos los snapshots de base de datos.
- `settings_view(request: Request, db: DBSession, repo: ProductivityRepository = Depends(get_productivity_repo))` - Renderiza el panel de control de configuraciones SaaS.
- `api_get_settings()` - Retorna las configuraciones generales.
- `api_update_setting(update: SettingUpdate, db: DBSession)` - Actualiza una configuración general.
- `api_upsert_status(update: StatusMappingUpdate, db: DBSession)` - Inserta o actualiza un estado.
- `api_delete_status(code: str, db: DBSession)` - Elimina un estado.
- `api_upsert_cost_center(update: CostCenterMappingUpdate, db: DBSession)` - Inserta o actualiza un centro de costo.
- `api_delete_cost_center(code: str, db: DBSession)` - Elimina un centro de costo.
- `api_upsert_user_group(update: UserGroupAdd, db: DBSession)` - Inserta o actualiza un grupo de usuarios.
- `api_delete_user_group(group_name: str, db: DBSession)` - Elimina un grupo de usuarios.
- `api_add_holiday(h: HolidayAdd, db: DBSession)` - Añade un feriado.
- `api_sync_holidays(db: DBSession)` - Sincroniza automáticamente los feriados nacionales (Chile).
- `api_delete_holiday(date_str: str, db: DBSession)` - Elimina un feriado.
- `api_get_query(query_id: str, db: DBSession)` - Retorna el estado visual de una consulta del Analytics Studio.
- `api_update_query(update: QueryUpdate, db: DBSession, cache: CacheManager = Depends(get_cache_manager))` - Persiste el estado visual de una consulta.
- `api_get_schema(db: DBSession)` - Retorna el catálogo semántico de datos para el editor.
- `api_preview_table(dataset_id: str, db: DBSession)` - Previsualiza una tabla.
- `api_query_preview(update: QueryUpdate, db: DBSession)` - Ejecuta una consulta temporal y retorna datos para previsualización.
- `api_build_sql(payload: VisualQueryBuilderPayload, db: DBSession)` - Compila el estado visual del constructor en SQL parametrizado seguro.
- `api_export_missing_orders(db: DBSession)` - Exporta órdenes sin ceco a un archivo Excel.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - `analytics_snapshots` (DELETE)
  - `app_settings`
  - `cost_center_mapping`
  - `holiday`
  - `status_mapping`
  - `user_group`

### Estado y Variables Globales
- No hay variables globales explícitas.

### Dependencias y Flujo
- **Dependencias Externas:** FastAPI, SQLAlchemy, Pandas, Holidays (librería de feriados)
- **Archivos del Proyecto que Importan a este Archivo:**
  - `core.auth.require_admin`
  - `core.database.get_session_dep`
  - `core.db_config_manager.*`
  - `core.models.*`
  - `core.state.CacheManager`
  - `core.utils.sanitize_for_json`
- **Archivos del Proyecto que Este Archivo Importa:**
  - `routes/settings.py` (se importa a sí mismo)
  - `repositories.get_productivity_repo`
  - `core.schemas.*`
  - `core.query_engine.build_sql_from_payload`

El flujo de datos es principalmente entre el endpoint, la base de datos y los modelos de datos.


---

## Archivo: ./routes/sync.py

### Resumen Funcional
Este archivo contiene rutas para la sincronización de datos en un sistema de monitoreo de almacén (WMS). Permite obtener la URL del túnel, el estado de la sincronización y iniciar procesos de sincronización. También proporciona endpoints para listar y consultar el estado de tareas.

### Catálogo de Funciones y Clases
- `get_tunnel_url()` - Retorna la URL pública del túnel (Ngrok).
- `get_sync_status(sync: SyncStateManager = Depends(get_sync_manager))` - Retorna el estado actual de la sincronización.
- `sync_data(sync: SyncStateManager = Depends(get_sync_manager), admin = Depends(require_auth))` - Inicia el proceso de sincronización de datos y lo encola en el TaskManager para ejecución trazable en segundo plano.
- `list_tasks(limit: int = 20, admin = Depends(require_auth))` - Lista las tareas recientes del sistema.
- `get_task(task_id: str, admin = Depends(require_auth))` - Consulta el estado de una tarea específica por su ID.
- `_run_sync_pipeline()` - Ejecuta el pipeline completo de limpieza y consolidación.

### Interacción con Base de Datos
- Motor: SQLite (indicado por `DB_PATH`)
- Tablas modificadas:
  - `analytics_snapshots` (se borra en caso de cambios)
- Columnas modificadas:
  - Todas las tablas que se procesan a través del `DataConsolidator`

### Estado y Variables Globales
- No hay variables globales explícitas mencionadas.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `logging`
  - `shutil`
  - `pathlib`
  - `typing`
  - `fastapi`
  
- **Archivos del Proyecto Importados**:
  - `config.py` (para constantes de rutas y archivos)
  - `core.auth` (para autenticación)
  - `core.state` (para gestionar estado de sincronización y caché)
  - `core.task_manager` (para manejo de tareas)
  - `db.consolidator` (para consolidación de datos)

- **Archivos del Proyecto que Importan a Este Archivo**:
  - `routes/transporte.py` (importado dentro de `_run_sync_pipeline` para sincronizar transporte)

El flujo de datos es desde el endpoint `/sync`, que inicia la tarea de sincronización, hasta la ejecución de `_run_sync_pipeline` en segundo plano mediante `TaskManager`. Este proceso incluye la lectura y procesamiento de archivos en varios directorios, la consolidación de datos en la base de datos SQLite, y la actualización del estado de las tareas.


---

## Archivo: ./routes/tasks.py

### Resumen Funcional
El archivo `tasks.py` contiene la definición de una ruta FastAPI para proporcionar analíticas sobre las tareas del almacén. La ruta permite a un usuario autenticado obtener datos detallados sobre las tareas, excluyendo ciertos campos sensibles.

### Catálogo de Funciones y Clases
- `get_tasks_context(session: Session) -> dict` - Obtiene el contexto completo de las tareas utilizando el servicio `TasksService`.
- `analytics_tasks_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), sync: SyncStateManager = Depends(get_sync_manager))` - Ruta FastAPI que devuelve analíticas sobre las tareas en formato JSON.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos. Utiliza el repositorio `TasksRepository` y el servicio `TasksService`, pero no interactúa explícitamente con la BD.

### Estado y Variables Globales
- Ninguna variable global, de sesión o diccionario quemado en código que almacene estado crítico.

### Dependencias y Flujo
- **Librerías externas**: `pandas`, `fastapi`, `sqlalchemy`.
- **Archivos del proyecto que IMPORTA (consume)**: 
  - `core.auth.get_current_user`
  - `core.database.get_session_dep`
  - `core.schemas.AnalyticsTasksResponse`
  - `core.state.SyncStateManager`
  - `core.utils.sanitize_for_json`
  - `repositories.TasksRepository`
  - `services.tasks_service.TasksService`
- **Archivos del proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno.
- **Dirección del flujo de datos**: El flujo comienza con la solicitud HTTP, pasa por el middleware de autenticación y dependencias, luego se procesa en `analytics_tasks_api`, donde se obtiene el contexto de las tareas y se devuelve como respuesta JSON.


---

## Archivo: ./routes/transporte.py

### Resumen Funcional
Este archivo contiene rutas para la sección de Transporte en un sistema de monitoreo de almacén (WMS). Permite la sincronización de datos desde una base de datos externa, consulta de datos consolidados, búsqueda y descarga de PDFs.

### Catálogo de Funciones y Clases
- `sync_transporte_logic(session: Session)` - Lógica core para sincronizar la base de datos externa a local.
- `sync_transporte(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta para sincronizar datos de transporte manualmente.
- `get_transporte_data(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Retorna los datos consolidados diarios ordenados cronológicamente.
- `search_transporte(q: str, session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Busca en la tabla cruda de transporte_entregas por OT, GD o OC.
- `serve_pdf(filename: str, user=Depends(get_current_user))` - Sirve el archivo PDF desde el disco.
- `get_pending_transporte(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Busca en transporte_entregas los documentos del año actual que NO han sido ingresados al inventario SAP.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `transporte_entregas`
    - Columnas: ot, proveedor, gd, oc, bulto, servicio, archivo, fecha
  - `transporte_diario`
    - Columnas: fecha, total_entregas, pdf_path
- Consultas SQL crudas y llamadas a ORM:
  - Creación de tablas si no existen.
  - Lectura de datos desde la base de datos externa.
  - Inserción de datos en `transporte_entregas`.
  - Consolidación de datos en `transporte_diario`.
  - Mapeo de PDFs.

### Estado y Variables Globales
- `EXTERNAL_DB_PATH` - Ruta a la base de datos externa SQLite.
- `PDF_DIR_PATH` - Directorio donde se almacenan los archivos PDF.

### Dependencias y Flujo
- Librerías externas: `logging`, `os`, `sqlite3`, `typing`.
- Archivos del proyecto que importan este archivo:
  - `core.auth`
  - `core.database`
- Archivos del proyecto que son importados por este archivo:
  - No aplica.
- Flujo de datos: El archivo consume y produce datos para las rutas definidas, interactuando con la base de datos SQLite y proporcionando respuestas en formato JSON.


---

## Archivo: ./routes/widgets.py

### Resumen Funcional
Este archivo contiene endpoints para obtener datos de widgets y sugerencias de reabastecimiento en un sistema de monitoreo de almacén (WMS). Los endpoints permiten consultar datos estructurados, ejecutar consultas personalizadas, y exportar sugerencias de pedido a formato Excel.

### Catálogo de Funciones y Clases
- `get_widget_data(query_id: str, year: Optional[str] = None, area: Optional[str] = None, granularity: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user), cache: CacheManager = Depends(get_cache_manager))` - Ejecuta una consulta visual y devuelve los datos estructurados.
- `get_widget_drilldown(query_id: str, segment: str, material: Optional[str] = None, year: Optional[str] = None, area: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user))` - Obtiene el detalle subyacente de un segmento de un widget.
- `get_cmv201_summary(plan_type: str = Query(..., description="Planificado o Desplanificado"), year: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user))` - Muestra la cantidad de materiales solicitados por área de negocio y mes para el CMV 201.
- `get_cmv201_area_details(plan_type: str = Query("planificado", description="'planificado' o 'desplanificado'"), area: str = Query(..., description="Area de negocio filtrada"), mes: str = Query(None, description="Mes en formato YYYY-MM. Si no se provee, no se filtra por mes."), year: str = Query(None, description="Año"), db: Session = Depends(get_session_dep))` - Muestra los detalles del CMV 201 para una área de negocio específica.
- `get_cmv261_summary(plan_type: str = Query("planificado", description="'planificado' o 'desplanificado'"), year: Optional[str] = None, db: Session = Depends(get_session_dep))` - Muestra la cantidad de materiales solicitados por área de negocio y mes para el CMV 261.
- `get_cmv261_area_details(plan_type: str = Query("planificado", description="'planificado' o 'desplanificado'"), area: str = Query(..., description="Area de negocio filtrada"), mes: str = Query(None, description="Mes en formato YYYY-MM. Si no se provee, no se filtra por mes."), year: str = Query(None, description="Año"), db: Session = Depends(get_session_dep))` - Muestra los detalles del CMV 261 para una área de negocio específica.
- `get_replenishment_suggestions(freq: str = Query("all", description="Filtro de frecuencia: all, 1, 3, 6, 12"), db: Session = Depends(get_session_dep))` - Calcula sugerencias de pedido basándose en el stock inicial MB5B y el ritmo de consumo.
- `export_replenishment_suggestions(db: Session = Depends(get_session_dep))` - Exporta todas las sugerencias de pedido (Autonomía < 1) a un archivo Excel.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `ConfigQuery`
- Columnas:
  - `query_id`, `visual_state`

### Estado y Variables Globales
- No hay variables globales, de sesión o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- Librerías externas: `pandas`
- Archivos del proyecto que IMPORTA:
  - `core.auth.get_current_user`
  - `core.database.get_session_dep`
  - `core.helpers.dynamic_executor.execute_visual_query`
  - `core.models.ConfigQuery`
  - `core.state.CacheManager.get_cache_manager`
  - `core.utils.sanitize_for_json`
- Archivos del proyecto que IMPORTAN a este archivo:
  - Ninguno
- Flujo de datos: Los endpoints consumen y producen datos estructurados, interactuando con la base de datos para obtener los datos necesarios.


---

## Archivo: ./scripts/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./scripts/bundler.py

### Resumen Funcional
El archivo `bundler.py` es un script que concatena múltiples archivos JavaScript en un solo archivo llamado `bundle.js`, lo cual se utiliza para la producción del frontend de un sistema de monitoreo de almacén (WMS).

### Catálogo de Funciones y Clases
- `bundle_js()` - Concatena múltiples archivos JS en un solo bundle.js para producción.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `JS_FILES_ORDER` - Una lista ordenada de nombres de archivos JavaScript que se concatenarán.
- `logger` - Un objeto de registro utilizado para registrar mensajes de información, advertencia y error.

### Dependencias y Flujo
- **Dependencias Externas**: `logging`, `os`, `pathlib`.
- **Archivos del Proyecto Importados por Este Archivo**: Ninguno.
- **Archivos del Proyecto que Importan a Este Archivo**: Ninguno.
- **Flujo de Datos**: El script lee archivos JavaScript desde un directorio específico, los concatena en un solo archivo `bundle.js`, y registra el proceso.


---

## Archivo: ./scripts/generate_graphify.py

### Resumen Funcional
El archivo `generate_graphify.py` es un script que prepara y ejecuta el proceso de generación de un mapa interactivo utilizando la herramienta `graphify`. El script limpia cualquier salida previa, ejecuta el CLI de `graphify`, traduce el HTML generado y lo mueve al directorio estático para su visualización en la aplicación web.

### Catálogo de Funciones y Clases
- `prepare_environment()` - Limpia el directorio anterior y prepara la configuración.
- `execute_graphify()` - Ejecuta el CLI de graphify.
- `process_and_move_html()` - Lee el HTML generado, lo traduce y lo guarda en su destino.
- `run_graphify()` - Inicia el escaneo con Graphify.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `ROOT_DIR` - Directorio raíz del proyecto.
- `OUT_DIR` - Directorio donde se genera la salida de `graphify`.
- `DEST_DIR` - Directorio donde se mueve el archivo HTML final.
- `TRANSLATIONS` - Diccionario con traducciones para elementos HTML.

### Dependencias y Flujo
- **Dependencias**: `shutil`, `subprocess`, `pathlib`.
- **Flujo de Datos**:
  - `generate_graphify.py` importa `shutil`, `subprocess` y `pathlib`.
  - `graphify-out` es el directorio donde se genera la salida de `graphify`.
  - El archivo HTML generado se mueve a `static/docs`.

El flujo comienza con la ejecución del script, que llama a `run_graphify()`, que en su turno llama a `prepare_environment()`, `execute_graphify()` y finalmente `process_and_move_html()`.


---

## Archivo: ./scripts/main_processor.py

### Resumen Funcional
El archivo `main_processor.py` es el punto de entrada del sistema de monitoreo de almacén (WMS). Ejecuta un pipeline completo que incluye la validación de directorios, análisis de carpetas, consolidación de datos, enriquecimiento y procesamiento de diferentes tipos de archivos (Entregas, Stock, Movimientos, IW39, MB5B) para actualizar una base de datos SQLite.

### Catálogo de Funciones y Clases
- `run_pipeline()` - Ejecuta el pipeline completo del WMS Analysis and Consolidation.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas Modificadas:**
  - `stock_levels`
  - `inventory_movements`
  - `iw39_orders`
  - `mb5b_initial_stock`
- **Columnas Modificadas:** Dependiendo del procesamiento, se insertan o actualizan filas en las tablas mencionadas.

### Estado y Variables Globales
- `PROJECT_ROOT` - Ruta al directorio raíz del proyecto.
- `DELIVERIES_DIR`, `STOCK_DIR`, `INVENTORY_DIR`, `IW39_DIR`, `MB5B_DIR`, `CLEANSED_DIR`, `DATABASE_PATH` - Rutas a los directorios y la base de datos.

### Dependencias y Flujo
- **Librerías Externas:** `logging`, `subprocess`, `sys`, `pathlib`
- **Archivos Importados:**
  - `config.py` (para configuraciones globales)
  - `db.consolidator.DataConsolidator` (para consolidación de datos)
  - `db.db_enrichment.enrich_deliveries_with_stock` y `db.db_enrichment.enrich_movements_with_iw39` (para enriquecimiento de datos)
  - `services.etl.movements.InventoryMovementAdapter` (para procesamiento de Movimientos)
  - `services.etl.iw39.IW39Processor` (para procesamiento de IW39)
  - `services.etl.mb5b.MB5BProcessor` (para procesamiento de MB5B)

**Flujo:**
1. `main_processor.py` importa configuraciones y dependencias.
2. Llama a `run_pipeline()`.
3. `run_pipeline()` ejecuta las fases del pipeline, que incluyen análisis de carpetas, consolidación de datos, enriquecimiento y procesamiento de diferentes tipos de archivos.
4. Los resultados se almacenan en la base de datos SQLite especificada.

Este archivo es el punto central para iniciar el proceso de análisis y consolidación en el sistema WMS, gestionando todas las fases del pipeline desde la validación de entrada hasta la actualización de la base de datos.


---

## Archivo: ./scripts/run_consolidator.py

### Resumen Funcional
El archivo `run_consolidator.py` es un script que ejecuta la consolidación de transacciones del almacén. Recibe como parámetro el camino a una carpeta y utiliza la clase `DataConsolidator` para procesar y consolidar los datos de las transacciones almacenados en una base de datos SQLite.

### Catálogo de Funciones y Clases
- `main()` - Función principal que verifica si se proporciona un argumento (camino a la carpeta) y luego llama al método `consolidate_folder` de la clase `DataConsolidator`.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna. La base de datos se especifica en el parámetro del constructor de `DataConsolidator`.
- Consultas SQL Crudas o ORM: Ninguna.

### Estado y Variables Globales
- Ninguna.

### Dependencias y Flujo
- Librerías Externas:
  - `pathlib`: Para manejar rutas de archivos.
  - `os`: Para manipular el sistema operativo.
- Archivos del Proyecto que Importan a este Archivo: Ninguno.
- Archivos del Proyecto que Este Archivo Importa:
  - `config.DB_PATH`: Ruta de la base de datos.
  - `db.consolidator.DataConsolidator`: Clase para la consolidación de datos.

**Flujo de Datos:**
1. El script se ejecuta desde la línea de comandos con un argumento que es el camino a una carpeta.
2. La función `main()` verifica si se proporciona el argumento necesario.
3. Se crea una instancia de `DataConsolidator` con la ruta a la base de datos SQLite.
4. El método `consolidate_folder` de `DataConsolidator` es llamado para procesar y consolidar los datos en la carpeta especificada.

Este flujo asegura que el script se comporte correctamente cuando se ejecuta desde la línea de comandos con el argumento adecuado.


---

## Archivo: ./services/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./services/background_tasks.py

### Resumen Funcional
El archivo `background_tasks.py` contiene una tarea de fondo que se encarga de refrescar las analíticas del sistema. Esta tarea ejecuta métodos de los servicios de entregas y inventario para recalcular su contexto completo.

### Catálogo de Funciones y Clases
- `refresh_analytics()` - Refresca las analíticas (ejecutado como tarea de fondo trazable).

### Interacción con Base de Datos
- Motor: SQLite
- Tablas modificadas:
  - Ninguna (se supone que los métodos llamados internamente interactúan directamente con la base de datos).
- Consultas SQL crudas o llamadas a ORM: Sí, se usan métodos de `DeliveriesService` y `InventoryService`, que probablemente contienen consultas SQL o llamadas a ORM.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `logging`
- Archivos del proyecto que importan a este archivo (`background_tasks.py`):
  - Ninguno
- Archivos del proyecto que este archivo importa (`background_tasks.py`):
  - `core.database.get_session`
  - `routes.tasks.get_tasks_context`
  - `services.deliveries_service.DeliveriesService`
  - `services.inventory_service.InventoryService`

**Flujo de datos:**
1. `refresh_analytics()` se ejecuta.
2. Se obtiene una sesión de base de datos usando `get_session()`.
3. Se crea una instancia de `DeliveriesService` y se llama a su método `get_full_context()`, que probablemente realiza consultas a la base de datos para recalcular el contexto de las entregas.
4. Se crea una instancia de `InventoryService` y se llama a su método `get_full_context()`, que probablemente realiza consultas a la base de datos para recalcular el contexto del inventario.
5. Se llama a `get_tasks_context(session)`, que también probablemente realiza consultas a la base de datos.
6. Si ocurre un error, se registra con nivel de error en el logger.

Este flujo asegura que todas las operaciones relacionadas con el refresco de analíticas interactúen directamente con la base de datos a través de los servicios correspondientes.


---

## Archivo: ./services/dashboard_service.py

### Resumen Funcional
El archivo `dashboard_service.py` contiene la lógica del servicio para el dashboard principal de entregas en un sistema de monitoreo de almacén (WMS). El servicio se encarga de obtener y formatear datos necesarios para mostrar en el dashboard, incluyendo gráficos de intensidad semanal, indicadores clave de rendimiento (KPIs), selectores y transacciones recientes.

### Catálogo de Funciones y Clases
- `DashboardService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - **Propósito**: Configura la instancia del servicio para interactuar con la base de datos a través del repositorio `DashboardRepository`.

- `get_full_context()` - Obtiene y formatea los datos necesarios para el contexto del dashboard.
  - **Propósito**: Recupera gráficos de intensidad semanal, KPIs filtrados, selectores y transacciones recientes, y los devuelve en un formato adecuado para la vista.

### Interacción con Base de Datos
- **Motor de BD**: SQLite
- **Tablas y Columnas**:
  - `get_weekly_intensity_chart(iso_year)` - Recupera datos para el gráfico de intensidad semanal.
    - Tabla: No especificada (implícita en la consulta SQL).
    - Columnas: No especificadas (implícitas en la consulta SQL).

  - `get_filtered_kpis(None, None, None, min_week, iso_year)` - Recupera KPIs filtrados por semana y año.
    - Tabla: No especificada (implícita en la consulta SQL).
    - Columnas: No especificadas (implícitas en la consulta SQL).

  - `get_dashboard_selectors(min_week)` - Recupera selectores para el dashboard.
    - Tabla: No especificada (implícita en la consulta SQL).
    - Columnas: No especificadas (implícitas en la consulta SQL).

  - `get_filtered_transactions(None, None, None, None, None, min_week)` - Recupera transacciones recientes filtradas por semana.
    - Tabla: No especificada (implícita en la consulta SQL).
    - Columnas: No especificadas (implícitas en la consulta SQL).

### Estado y Variables Globales
- **Variables Globales**: Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `logging`
  - `datetime`
  - `typing`

- **Archivos del Proyecto que Importan a este Archivo (lo consumen)**: Ninguno

- **Archivos del Proyecto que Este Archivo Importa (consume)**:
  - `repositories.dashboard.DashboardRepository`

- **Dirección del Flujo de Datos**:
  - El servicio recibe una sesión de base de datos y utiliza el repositorio para obtener los datos necesarios.
  - Los datos obtenidos se formatean y devuelven en un diccionario que representa el contexto completo del dashboard.


---

## Archivo: ./services/deliveries_service.py

### Resumen Funcional
El archivo `deliveries_service.py` contiene la lógica de negocio para el servicio de entregas en un sistema de monitoreo de almacén (WMS). Este servicio se encarga de generar un contexto completo con metadatos ligeros, incluyendo áreas de negocio y widgets configurados.

### Catálogo de Funciones y Clases
- `DeliveriesService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - **Propósito**: Prepara el servicio para interactuar con la base de datos proporcionada.
  
- `get_full_context()` - Genera un contexto completo con metadatos ligeros.
  - **Propósito**: Recopila y devuelve información relevante como áreas de negocio, widgets configurados, y otros datos necesarios para el monitoreo del almacén.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `outbound_deliveries`
- **Columnas**:
  - `area_negocio`

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: 
  - `logging`, `typing`, `sqlalchemy.orm`
  
- **Archivos del Proyecto que Importan a este Archivo**:
  - `routes.analytics_proyecciones.get_proyecciones_context()`
  - `routes.inventory.get_inventory_context()`
  - `routes.tasks.get_tasks_context()`

- **Archivos del Proyecto que Este Archivo Importa**:
  - `core.cache_decorator.analytics_cache`
  - `core.models.ConfigQuery`
  
- **Dirección del Flujo de Datos**: 
  - El archivo importa funciones desde otros archivos y utiliza la sesión de base de datos para consultar información.


---

## Archivo: ./services/etl/__init__.py

### Resumen Funcional
Este archivo contiene funciones para procesar diferentes tipos de archivos y directorios relacionados con el inventario y las tareas del almacén. Utiliza adaptadores específicos para cada tipo de dato (inventario, tareas, entregas) y guarda los datos en una base de datos SQLite.

### Catálogo de Funciones y Clases
- `process_inventory_folder(folder_path: str, db_path: str, table_name: str = "inventory_movements", conn=None) -> int` - Procesa un directorio de archivos de inventario y guarda los datos en la base de datos.
- `process_inventory_file(file_path: str, db_path: str, table_name: str = "inventory_movements", conn=None) -> int` - Procesa un archivo de inventario y guarda los datos en la base de datos.
- `process_tasks_file(file_path: str, db_path: str, table_name: str = "warehouse_tasks", conn=None) -> int` - Procesa un archivo de tareas del almacén y guarda los datos en la base de datos.
- `process_lx02_pendientes(folder_path: str, db_path: str, table_name: str = "lx02_pendientes", conn=None) -> int` - Procesa un directorio de archivos pendientes relacionados con el LX02 y guarda los datos en la base de datos.
- `process_deliveries_file(file_path: str, db_path: str, table_name: str = "outbound_deliveries", conn=None) -> int` - Procesa un archivo de entregas y guarda los datos en la base de datos.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas modificadas:
  - `inventory_movements`
  - `warehouse_tasks`
  - `lx02_pendientes`
  - `outbound_deliveries`

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: No hay dependencias externas.
- **Archivos del Proyecto que Importan a este Archivo**:
  - `./services/etl/deliveries.py`
  - `./services/etl/movements.py`
  - `./services/etl/tasks.py`
  - `./services/etl/stock.py`
- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno

El flujo de datos es desde los archivos de entrada (directorios o archivos) hasta la base de datos SQLite, utilizando adaptadores específicos para cada tipo de dato.


---

## Archivo: ./services/etl/base.py

### Resumen Funcional
El archivo `base.py` define una clase abstracta `BaseWMSProcessor` que proporciona funcionalidades para procesar archivos WMS (TXT/CSV/XLSX) y cargarlos en una base de datos SQLite. Incluye métodos para validar archivos, leer y limpiar datos, realizar operaciones UPSERT atómicas, y procesar directorios de archivos.

### Catálogo de Funciones y Clases
- `BaseWMSProcessor(encodings=None, chunk_size=50000)` - Clase abstracta que define métodos para procesar archivos WMS.
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo es válido para este procesador.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y transforma un chunk de datos crudos (implementado por cada hijo).
  - `_detect_file_params(file_path: Path, required_columns: List[str]) -> Tuple[int, str]` - Detecta la fila de encabezado y codificación buscando columnas clave.
  - `read_and_clean_data(file_path: Path) -> pd.DataFrame` - Lee el archivo completo (para testing o archivos pequeños).
  - `_get_required_columns() -> List[str]` - Lista de strings que deben estar en el header para detectar el inicio. Por defecto vacía.
  - `_get_primary_keys() -> List[str]` - Devuelve las columnas que actúan como clave primaria para deduplicación. Por defecto vacía.
  - `process_and_save(file_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int` - Orquestador unificado de procesamiento Chunked + Upsert SQLite.
  - `_upsert_chunk(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str)` - Lógica de Upsert atómico por chunk.
  - `_post_process(conn: sqlite3.Connection, table_name: str)` - Hook opcional para crear índices o post-procesar tras un upsert.
  - `process_directory(folder_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int` - Escanea un directorio y procesa todos los archivos compatibles con Upsert acumulativo.

### Interacción con Base de Datos
- Motor: SQLite.
- Tablas: Ninguna (operaciones directas en la base de datos).
- Columnas: Ninguna (operaciones directas en la base de datos).

### Estado y Variables Globales
- `logger` - Variable global para el registro de eventos.

### Dependencias y Flujo
- Librerías externas:
  - `logging`
  - `sqlite3`
  - `abc`
  - `pathlib`
  - `typing`
  - `pandas`
- Archivos del proyecto que este archivo importa: Ninguno.
- Archivos del proyecto que importan a este archivo: Ninguno.
- Flujo de datos: El archivo procesa archivos WMS y carga los datos en una base de datos SQLite.


---

## Archivo: ./services/etl/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene una clase `OutboundDeliveryAdapter` que extiende `BaseWMSProcessor`. Esta clase se encarga de procesar archivos de entregas de salida (Deliveries) en un sistema de gestión de almacén (WMS). El proceso incluye la validación del archivo, la limpieza y transformación de los datos, así como la inserción o actualización de estos datos en una base de datos SQLite.

### Catálogo de Funciones y Clases
- `OutboundDeliveryAdapter(BaseWMSProcessor)` - Adaptador para procesar Entregas de Salida (Deliveries).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y tiene una extensión permitida.
  - `_get_required_columns() -> List[str]` - Devuelve las columnas requeridas en el DataFrame.
  - `_get_primary_keys() -> List[str]` - Devuelve las claves primarias utilizadas para la deduplicación.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y transforma el DataFrame de entrada.
  - `_sanitizar_nombres_columnas(columns: pd.Index) -> list` - Sanitiza los nombres de las columnas del DataFrame.
  - `_post_process(conn, table_name: str)` - Crea índices adicionales en la tabla especificada.
  - `_upsert_chunk(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str)` - Inserta o actualiza datos en la base de datos SQLite.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas modificadas:
  - `outbound_deliveries`
- Columnas modificadas:
  - Todas las columnas presentes en el DataFrame, incluyendo nuevas columnas dinámicas.
- Consultas SQL crudas:
  - `CREATE INDEX IF NOT EXISTS idx_out_ceco_upper ON outbound_deliveries(UPPER(TRIM(centro_costo)))`
  - `PRAGMA table_info({table_name})`

### Estado y Variables Globales
No se detectaron variables globales, de sesión o de entorno en este archivo.

### Dependencias y Flujo
- Librerías externas:
  - `sqlite3`
  - `pandas`
  - `pathlib`
  - `typing`
- Archivos del proyecto que importan a este archivo (`deliveries.py`):
  - No se detectaron archivos que importen directamente a `deliveries.py`.
- Archivos del proyecto que este archivo importa:
  - `core.wms_utils`: Contiene funciones utilitarias para el procesamiento de datos.
  - `.base.BaseWMSProcessor`: Clase base para procesadores de WMS.

**Flujo de Datos:**
1. **Entrada**: Archivo CSV, Excel o TXT con datos de entregas de salida.
2. **Procesamiento**:
   - Validación del archivo.
   - Extracción y limpieza de columnas requeridas.
   - Transformación de los datos utilizando funciones utilitarias (`map_wms_status`, `apply_cost_center_mapping`, etc.).
3. **Salida**: Inserción o actualización de los datos en la tabla `outbound_deliveries` de la base de datos SQLite.

Este flujo asegura que los datos de entregas de salida sean procesados y almacenados correctamente en el sistema de gestión de almacén.


---

## Archivo: ./services/etl/iw39.py

### Resumen Funcional
El archivo `iw39.py` contiene una clase `IW39Processor` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos en formato IW39, validando su contenido y limpiándolo para su uso en el sistema de monitoreo de almacén (WMS).

### Catálogo de Funciones y Clases
- **IW39Processor(BaseWMSProcessor)** - Adaptador específico para procesar el formato IW39 (Órdenes PM).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas para el procesamiento del IW39.
  - `_get_primary_keys() -> List[str]` - Devuelve la clave primaria utilizada en el procesamiento del IW39.
  - `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza un DataFrame de pandas, eliminando columnas vacías, renombrando columnas según un mapeo específico, filtrando filas sin clave primaria, y normalizando datos como fechas y cadenas.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: pandas.
- **Flujo**: El archivo no importa ni es importado por otros archivos dentro del proyecto.


---

## Archivo: ./services/etl/mb5b.py

### Resumen Funcional
El archivo `mb5b.py` contiene una clase `MB5BProcessor` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos en formato MB5B, que representan el stock inicial en un sistema de monitoreo de almacén (WMS). El proceso incluye la validación del archivo, la detección de columnas requeridas y la limpieza y transformación del DataFrame.

### Catálogo de Funciones y Clases
- `MB5BProcessor(BaseWMSProcessor)` - Adaptador específico para procesar el formato MB5B (Stock Inicial).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas para el formato MB5B.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias para el formato MB5B.
  - `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame` - Limpia y transforma el DataFrame del archivo.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**: `pandas`
- **Archivos Importados por Este Archivo**: Ninguno.
- **Archivos que Importan a Este Archivo**: Ninguno.
- **Flujo de Datos**: El archivo importa `BaseWMSProcessor` desde el módulo local y utiliza `pandas` para procesar los datos.


---

## Archivo: ./services/etl/movements.py

### Resumen Funcional
El archivo `movements.py` contiene una clase `InventoryMovementAdapter` que se encarga de procesar archivos CSV con movimientos del sistema WMS, validar su contenido, limpiar y transformar los datos para su almacenamiento en la base de datos SQLite.

### Catálogo de Funciones y Clases
- **Clase:** `InventoryMovementAdapter`
  - Propósito: Adaptador específico para procesar el formato WMS Movimientos.
  
- **Métodos:**
  - `validate_file(file_path: Path) -> bool`: Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]`: Devuelve una lista de columnas requeridas para el procesamiento.
  - `_get_primary_keys() -> List[str]`: Devuelve una lista de claves primarias utilizadas en la base de datos.
  - `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame`: Limpia y transforma el DataFrame, eliminando columnas innecesarias y normalizando los valores.
  - `_vectorized_classify(df: pd.DataFrame) -> pd.DataFrame`: Clasifica las operaciones según el valor de la columna `cmv`.
  - `_post_process(conn, table_name: str)`: Crea índices en la base de datos para mejorar el rendimiento de las consultas.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: `inventory_movements`
    - Columnas: `fe_contab`, `alm`, `ce`, `cmv`, `referencia`, `texto_cab_documento`, `texto_breve_material`, `material`, `cantidad`, `umb`, `doc_mat`, `ej_mat`, `registrado`, `hora`, `usuario`, `pedido`, `ce_coste`, `importe_ml`, `mon`, `proveedor`, `orden`, `pos`, `pos_extra`, `tipo_operacion`

### Estado y Variables Globales
- **Ninguna**

### Dependencias y Flujo
- **Librerías Externas:**
  - `numpy`
  - `pandas`
  
- **Archivos del Proyecto que Importan a este Archivo (lo consumen):**
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa (consume):**
  - `./services/etl/base.py`

- **Dirección del Flujo de Datos:**
  - El archivo recibe un archivo CSV, lo valida, limpia y transforma, luego lo almacena en la base de datos SQLite.


---

## Archivo: ./services/etl/stock.py

### Resumen Funcional
El archivo `stock.py` contiene una clase `StockLevelAdapter` que procesa archivos de inventario/stock en formato LX02, los limpia y carga en una base de datos SQLite. Realiza un REPLACE completo en la tabla especificada.

### Catálogo de Funciones y Clases
- `validate_file(file_path: Path) -> bool`: Valida si el archivo existe y contiene las columnas requeridas.
- `_get_required_columns() -> List[str]`: Devuelve las columnas clave del header SAP LX02.
- `read_and_clean_data(file_path: Path) -> pd.DataFrame`: Lee y limpia los datos del archivo de inventario.
- `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame`: Limpia el DataFrame eliminando filas y columnas vacías y normalizando los strings.
- `process_directory(folder_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int`: Procesa todos los archivos en un directorio, combina sus datos y carga el resultado en la base de datos.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna (se espera una tabla especificada por `table_name`).
- Columnas: Ninguna (se espera que la tabla tenga las columnas necesarias).

### Estado y Variables Globales
- No hay variables globales, de sesión o de entorno definidas en este archivo.

### Dependencias y Flujo
- Librerías externas:
  - `logging`
  - `os`
  - `sqlite3`
  - `datetime`
  - `pathlib`
  - `typing`
  - `pandas`
- Archivos del proyecto que importan a este archivo: Ninguno.
- Archivos del proyecto que este archivo importa: `./services/etl/base.py` (clase base `BaseWMSProcessor`).
- Flujo de datos:
  - El archivo lee archivos de inventario, los limpia y carga en una tabla de la base de datos SQLite.


---

## Archivo: ./services/etl/tasks.py

### Resumen Funcional
El archivo `tasks.py` contiene una clase `WarehouseTaskAdapter` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos en formato WMS Tareas (Órdenes de Transporte), validando su contenido, limpiándolo y preparándolo para ser utilizado en el sistema de monitoreo de almacén.

### Catálogo de Funciones y Clases
- `WarehouseTaskAdapter(BaseWMSProcessor)` - Adaptador específico para procesar el formato WMS Tareas (Órdenes de Transporte).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas para el procesamiento.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias utilizadas en el procesamiento.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza el DataFrame, eliminando duplicados y corrigiendo tipos de datos.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**: `pandas`
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno.
- **Archivos del Proyecto que Este Archivo Importa**: `./services/etl/base.py` (clase `BaseWMSProcessor`)
- **Flujo de Datos**: El archivo importa la clase base y utiliza pandas para procesar archivos CSV, lo cual implica un flujo de datos desde el archivo hasta la limpieza y preparación del DataFrame.


---

## Archivo: ./services/inventory_service.py

### Resumen Funcional
El archivo `inventory_service.py` contiene la lógica de negocio para el servicio de inventario en un sistema de gestión de almacén (WMS). Define una clase `InventoryService` que interactúa con la base de datos para obtener y procesar datos de movimientos de inventario, calculando estadísticas de eficiencia y generando un contexto completo para el dashboard.

### Catálogo de Funciones y Clases
- **Clase: InventoryService**
  - **Método:** `__init__(self, session: Session)`
    - **Propósito:** Inicializa la instancia con una sesión de base de datos.
  
  - **Método:** `fmt_num(self, val)`
    - **Propósito:** Formatea un número para mostrarlo como una cadena con separadores de miles y decimales.

  - **Método:** `_get_latest_data_period(self) -> Tuple[str, str]`
    - **Propósito:** Obtiene el período más reciente de datos disponibles en la base de datos.

  - **Método:** `_get_empty_context(self) -> Dict[str, Any]`
    - **Propósito:** Devuelve un contexto vacío con valores por defecto para las estadísticas y métricas del inventario.

  - **Método:** `get_full_context(self) -> Dict[str, Any]`
    - **Propósito:** Genera el contexto completo para el dashboard de Movimientos (Fase 3: SaaS), incluyendo estadísticas de eficiencia y datos históricos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `inventory_movements`
- **Columnas:** 
  - `fe_contab` (Fecha del movimiento)
  - `tipo_operacion` (Tipo de operación: Ingreso/Consumo)
  - `registrado` (Fecha de registro)

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:** 
  - `pandas`
  - `numpy`
  - `sqlalchemy`

- **Archivos del Proyecto que Importan a este Archivo:**
  - `repositories.InventoryRepository`

- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.cache_decorator.analytics_cache`
  - `core.state.get_cache_manager`
  - `core.utils.sanitize_for_json`
  - `core.wms_config.COST_CENTER_MAPPING`
  - `repositories.InventoryRepository`

**Flujo de Datos:** 
1. El archivo se importa por otros archivos del proyecto.
2. Se crea una instancia de `InventoryService` pasando una sesión de base de datos.
3. Llama al método `get_full_context()` para generar el contexto completo.
4. Este método interactúa con la base de datos para obtener y procesar los datos necesarios.
5. Los resultados se almacenan en caché para mejorar el rendimiento.

Este archivo es crucial para el funcionamiento del sistema de gestión de inventario, proporcionando las estadísticas y datos necesarios para el dashboard de Movimientos.


---

## Archivo: ./services/productivity_daily.py

### Resumen Funcional
El archivo `productivity_daily.py` contiene el servicio para gestionar los datos de productividad diaria en un sistema de almacén (WMS). Ofrece métodos para obtener fechas disponibles, datos de productividad por fecha específica y detalles de movimientos diarios de usuarios.

### Catálogo de Funciones y Clases
- `ProductivityDailyService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - `get_available_dates()` - Retorna las fechas disponibles para los KPIs de productividad.
  - `get_productivity_data(target_date: str) -> Dict[str, Any]` - Obtiene todos los KPIs de productividad para una fecha específica (YYYY-MM-DD).
  - `get_user_movements_daily_summary(target_date: str, usuario: str) -> list` - Retorna el resumen diario de movimientos de un usuario.
  - `get_user_movements_daily_details(target_date: str, usuario: str, operacion: str) -> list` - Retorna los detalles diarios de movimientos de un usuario para una operación específica.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas y Columnas:
  - `get_available_dates()`: No especifica consultas directas.
  - `get_productivity_data(target_date: str)`: Llama a `_get_daily_summary`, `_get_hourly_trend`, `_get_inactivity_gaps`, y `_get_activity_heatmap` en `ProductivityRepository`.
    - `_get_daily_summary(date_sap)`
    - `_get_hourly_trend(date_sap)`
    - `_get_inactivity_gaps(date_sap)`
    - `_get_activity_heatmap(date_sap)`
  - `get_user_movements_daily_summary(target_date: str, usuario: str)`: Llama a `get_user_movements_daily_summary` en `ProductivityRepository`.
  - `get_user_movements_daily_details(target_date: str, usuario: str, operacion: str)`: Llama a `get_user_movements_daily_details` en `ProductivityRepository`.

### Estado y Variables Globales
- No hay variables globales declaradas.

### Dependencias y Flujo
- Librerías externas:
  - `logging`
  - `typing`
  - `re` (módulo estándar de Python)
- Archivos del proyecto que importan a este archivo (`productivity_daily.py`):
  - Ninguna.
- Archivos del proyecto que este archivo importa (`productivity_daily.py`):
  - `repositories.productivity.ProductivityRepository`
- Flujo de datos:
  - El servicio recibe una sesión de base de datos y utiliza un repositorio para interactuar con la BD.
  - Los métodos devuelven datos estructurados en formato JSON.


---

## Archivo: ./services/productivity_monthly.py

### Resumen Funcional
El archivo `productivity_monthly.py` contiene servicios para calcular y obtener datos de productividad mensuales en un sistema de almacén (WMS). Ofrece métodos para obtener resúmenes y detalles de movimientos de usuarios por mes.

### Catálogo de Funciones y Clases
- `ProductivityMonthlyService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - `get_monthly_productivity_data(target_month: str) -> Dict[str, Any]` - Calcula y devuelve los KPIs de productividad para un mes específico (YYYY-MM).
  - `get_user_movements_monthly_summary(target_month: str, usuario: str) -> list` - Obtiene el resumen de movimientos mensuales por usuario.
  - `get_user_movements_monthly_details(target_month: str, usuario: str, operacion: str) -> list` - Obtiene los detalles de movimientos mensuales por usuario y operación.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - Ninguna (se asume que las consultas SQL están definidas en el repositorio `ProductivityRepository`)
- Consultas SQL Crudas o ORM:
  - `_get_monthly_summary(month_sap)`
  - `_get_monthly_shifts(month_sap)`
  - `_get_monthly_heatmap(month_sap)`
  - `get_user_movements_monthly_summary(target_month, usuario)`
  - `get_user_movements_monthly_details(target_month, usuario, operacion)`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías Externas:
  - `logging`
  - `typing`
  - `sqlalchemy.orm.Session`
- Archivos del Proyecto que Importan a este Archivo (lo Consumen):
  - Ninguno
- Archivos del Proyecto que Este Archivo Importa (consume):
  - `repositories.productivity.ProductivityRepository`

**Flujo de Datos:**
1. El servicio `ProductivityMonthlyService` se inicializa con una sesión de base de datos.
2. Los métodos `get_monthly_productivity_data`, `get_user_movements_monthly_summary`, y `get_user_movements_monthly_details` llaman a los métodos correspondientes del repositorio `ProductivityRepository`.
3. El repositorio ejecuta consultas SQL para obtener los datos de productividad y movimientos.
4. Los resultados se procesan y devuelven al servicio, que finalmente los devuelve al cliente.


---

## Archivo: ./services/tasks_service.py

### Resumen Funcional
El archivo `tasks_service.py` contiene la lógica del servicio para generar el contexto analítico para la gestión de Operaciones Técnicas (OTs) en un sistema de monitoreo de almacén (WMS). Este servicio utiliza SQLAlchemy para interactuar con una base de datos SQLite y pandas para procesar los datos.

### Catálogo de Funciones y Clases
- `TasksService(session: Session)` - Inicializa el servicio con una sesión de la base de datos.
  - **Propósito**: Proporciona métodos para obtener diferentes conjuntos de datos relacionados con las OTs.

- `get_full_context()` - Genera el contexto analítico para la gestión de OTs.
  - **Propósito**: Recopila y procesa datos desde múltiples fuentes (tablas de la base de datos, consultas dinámicas) para generar un diccionario con información relevante.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `config_queries` - Almacena consultas y estados visuales configurados.
- **Columnas**:
  - `sql_text` - Texto de la consulta SQL.
  - `visual_state` - Estado visual de la consulta.
  - `query_id` - Identificador único de la consulta.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `pandas`
  - `sqlalchemy`
  - `logging`
  - `datetime`

- **Archivos del Proyecto que Importa a este Archivo (lo consumen)**:
  - `repositories/TasksRepository.py` - Para acceder a los datos de las OTs.

- **Archivos del Proyecto que Este Archivo IMPORTA**:
  - `core/cache_decorator.py`
  - `core/state.py`
  - `core/utils.py`

- **Dirección del Flujo de Datos**:
  - Desde el servicio (`TasksService`) se obtienen datos desde la base de datos y las tablas configuradas.
  - Los datos son procesados y transformados en un formato adecuado para su visualización o análisis.
  - El resultado final es un diccionario que contiene los datos procesados, que luego puede ser utilizado por otras partes del sistema.


---

## Archivo: ./services/tunnel.py

### Resumen Funcional
El archivo `tunnel.py` contiene la implementación del servicio de túnel utilizando ngrok, que se utiliza para exponer el servidor local (escuchando en el puerto 8000) a Internet. El servicio es gestionado de manera segura y thread-safe mediante un singleton.

### Catálogo de Funciones y Clases
- `NgrokService(bin_path=NGROK_BIN, tunnel_file=TUNNEL_URL_FILE)` - Inicializa el objeto del servicio de ngrok.
  - Propósito: Configura las rutas del binario de ngrok y el archivo donde se guardará la URL pública.

- `_validate_bin()` - Valida si el binario de ngrok existe y tiene permisos de ejecución.
  - Propósito: Asegura que el binario de ngrok esté disponible y accesible.

- `_save_url(url)` - Guarda la URL pública en un archivo especificado.
  - Propósito: Almacena la URL del túnel público para su uso posterior.

- `_get_public_url()` - Obtiene la URL pública del túnel a través de la API de ngrok.
  - Propósito: Recupera la URL pública del túnel desde el servidor local de ngrok.

- `start()` - Inicia el servicio de ngrok en un hilo separado.
  - Propósito: Lanza el proceso de ngrok y espera hasta que se obtenga la URL pública.

- `stop()` - Detiene el servicio de ngrok.
  - Propósito: Termina el proceso de ngrok y limpia los recursos asociados.

- `_run_loop()` - Bucle principal del servicio de ngrok, encargado de iniciar y gestionar el túnel.
  - Propósito: Maneja la creación y reinicio del túnel hasta que se solicite su detención.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `_service_lock` - Lock para proteger el acceso al servicio global.
- `_global_service` - Variable global que almacena la instancia singleton del servicio de ngrok.

### Dependencias y Flujo
- **Librerías Externas**: `json`, `logging`, `os`, `subprocess`, `threading`, `time`, `urllib.request`.
- **Archivos Importados**: `config.py` (para constantes como `NGROK_BIN` y `TUNNEL_URL_FILE`).
- **Flujo de Datos**:
  - El archivo se importa por otros módulos para iniciar o detener el servicio de túnel.
  - Los métodos `_run_loop`, `start`, y `stop` manejan la creación, reinicio y finalización del proceso de ngrok en un hilo separado.


---

## Archivo: ./static/css/analytics_proyecciones.css

### Resumen Funcional
El archivo `analytics_proyecciones.css` contiene estilos CSS para la interfaz de usuario del módulo de análisis de proyecciones en el sistema de monitoreo de almacén (WMS). Define clases y estilos para contenedores, gráficos, tarjetas, tablas y modales.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna


---

## Archivo: ./static/css/deliveries.css

### Resumen Funcional
El archivo `deliveries.css` contiene estilos CSS para la interfaz de usuario del sistema de monitoreo de almacén (WMS). Define clases y estilos para elementos como contenedores, tarjetas estadísticas, gráficos, listas de clasificación, cuadrículas de materiales, tarjetas de área, modales y encabezados.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- Ninguna

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- No hay dependencias externas.
- Archivos del proyecto que importan a este archivo: Ninguno.
- Archivos del proyecto que este archivo importa: Ninguno.

El flujo de datos es unidireccional, con el CSS aplicando estilos a elementos HTML en la interfaz de usuario.


---

## Archivo: ./static/css/docs_explorer.css

### Resumen Funcional
El archivo `docs_explorer.css` define los estilos para la interfaz de usuario del explorador de documentación en un sistema de monitoreo de almacén (WMS). Incluye estilos para el contenedor principal, el sidebar del árbol y el visor de contenido.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas.
- **Flujo**: Este archivo no importa ni es importado por otros archivos. Es un recurso estático CSS que se utiliza en la interfaz de usuario del sistema.

El archivo `docs_explorer.css` solo contiene estilos CSS y no interactúa con ninguna base de datos, funciones o variables globales.


---

## Archivo: ./static/css/inventory.css

### Resumen Funcional
El archivo `inventory.css` contiene estilos CSS para la interfaz de usuario del sistema de monitoreo de almacén, incluyendo contenedores de análisis, tarjetas estadísticas, gráficos, listas de clasificación y elementos de encabezado.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna


---

## Archivo: ./static/css/sla_table.css

### Resumen Funcional
El archivo `sla_table.css` contiene estilos CSS para una tabla de monitoreo de almacén (WMS), incluyendo clases para el contenedor principal, controles del encabezado, wrapper de la tabla y elementos de la tabla como celdas y etiquetas.

### Catálogo de Funciones y Clases
- `.container` - Establece estilos para el contenedor principal.
- `.header-controls` - Define estilos para los controles del encabezado.
- `.table-wrapper` - Aplica estilos al wrapper de la tabla.
- `table` - Establece estilos generales para la tabla.
- `th` - Define estilos para las celdas de encabezado.
- `td` - Establece estilos para las celdas de datos.
- `.pill` - Define estilos para etiquetas (pill).
- `.pill.late` - Aplica estilos específicos para las etiquetas que indican retraso.
- `.pill.ontime` - Aplica estilos específicos para las etiquetas que indican cumplimiento a tiempo.
- `.area-badge` - Define estilos para los badges de área.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
Ninguna.


---

## Archivo: ./static/js/analytics_proyecciones.js

### Resumen Funcional
El archivo `analytics_proyecciones.js` contiene la lógica para renderizar y controlar los modales de alertas, combinaciones y gráficos de dispersión en una interfaz web. Utiliza funciones para filtrar y mostrar datos basados en criterios de búsqueda y selección.

### Catálogo de Funciones y Clases
- `renderAlerts()` - Renderiza la tabla de alertas.
- `renderCombos(filterText = "")` - Renderiza los combos de materiales.
- `renderScatter()` - Renderiza el gráfico de dispersión.
- `openModalAlerts()` - Abre el modal de alertas y carga los datos.
- `openModalCombos()` - Abre el modal de combinaciones y carga los datos.
- `openModalScatter()` - Abre el modal de gráficos de dispersión y carga los datos.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas a una base de datos.

### Estado y Variables Globales
No hay variables globales explícitas definidas en este archivo. Las variables utilizadas son principalmente para almacenar referencias a elementos del DOM y datos obtenidos mediante `getData`.

### Dependencias y Flujo
- **Dependencias**: El archivo depende de `core_ui.js` que proporciona funciones como `CoreUI.openModal`, `CoreUI.closeModal`, `CoreUI.populateAreaSelect` y `CoreUI.getData`.
- **Flujo de Datos**: 
  - Los datos se obtienen mediante `getData('data_alerts')`, `getData('data_combos')`, y `getData('data_scatter')`.
  - Los datos son filtrados y renderizados en los modales correspondientes.
  - El gráfico de dispersión se inicializa con datos obtenidos de `getData('data_scatter')`.

Este archivo es parte del frontend de un sistema WMS, donde la lógica de interfaz interactúa con el backend a través de funciones que obtienen y manipulan datos para su visualización en los modales y gráficos.


---

## Archivo: ./static/js/analytics_studio_config.js

### Resumen Funcional
Este archivo JavaScript define un manejador para el estado visual de gráficos en una aplicación de análisis. Permite obtener y establecer el estado visual de diferentes consultas, utilizando un patrón singleton para mantener la instancia única por consulta.

### Catálogo de Funciones y Clases
- `AnalyticsStudioManager.getVisualState(queryId)` - Obtiene el estado visual actualizado para una consulta específica.
- `AnalyticsStudioManager.setVisualState(queryId, state)` - Establece un nuevo estado visual para una consulta específica.

### Interacción con Base de Datos
Ninguna. El archivo no realiza ninguna operación directa en la base de datos.

### Estado y Variables Globales
- `studioChartInstance` - Variable global que almacena una instancia del gráfico.
- `currentSchema` - Objeto que contiene el esquema actual.
- `currentQueryId` - ID de la consulta actualmente seleccionada.
- `serverVisualState` - Estado visual almacenado en el servidor.
- `visualState` - Puntero al estado activo del modal.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas mencionadas.
- **Flujo de Datos**: El archivo no importa ni es importado por otros archivos. Es un módulo autónomo que gestiona el estado visual de los gráficos.


---

## Archivo: ./static/js/analytics_studio_renderer.js

### Resumen Funcional
La función `renderPreviewChart` se encarga de renderizar un gráfico o tabla en el navegador basado en los datos proporcionados. El tipo de visualización (gráfico, tabla, KPI) y sus configuraciones son determinadas por parámetros del usuario.

### Catálogo de Funciones y Clases
- `renderPreviewChart(payload)` - Renderiza un gráfico o tabla según el tipo de dato proporcionado en `payload`.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `studioChartInstance` - Variable global que almacena la instancia actual del gráfico renderizado.

### Dependencias y Flujo
- **Dependencias**: 
  - `window.Chart` - Librería para crear gráficos.
  
- **Flujo de Datos**:
  - El archivo se importa en otros archivos JavaScript dentro del proyecto.
  - Otros archivos JavaScript pueden llamar a la función `renderPreviewChart(payload)` con los datos necesarios para renderizar el gráfico o tabla.


---

## Archivo: ./static/js/analytics_studio_ui.js (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `analytics_studio_ui.js` contiene funciones y métodos para gestionar la interfaz de usuario del Studio de Análíticas, permitiendo la edición, visualización y publicación de consultas. Incluye funcionalidades para cargar esquemas de base de datos, previsualizar tablas, ejecutar consultas y manejar filtros y configuraciones visuales.

### Catálogo de Funciones y Clases
- `openEditQueryModal(queryId, chartTitle)` - Abre el modal para editar una consulta.
- `loadSchema()` - Carga el esquema de la base de datos.
- `previewTable(tableName, el)` - Previsualiza los datos de una tabla.
- `runPreview()` - Ejecuta una previsualización de la consulta actual.
- `closeEditQueryModal()` - Cierra el modal para editar una consulta.
- `showConfirmPublish()` - Muestra el overlay de confirmación para publicar una consulta.
- `hideConfirmPublish()` - Oculta el overlay de confirmación para publicar una consulta.
- `executePublishQuery()` - Publica la consulta actual.
- `initVisualQuery(queryId)` - Inicializa el Constructor Visual con los datos de la consulta.
- `onBaseTableChange()` - Maneja el cambio en la tabla base seleccionada.
- `getActiveTables()` - Devuelve las tablas activas.
- `getActiveColumns()` - Devuelve las columnas activas.
- `refreshQbColumns(forceState = false)` - Refresca los controles de columna para el Constructor Visual.
- `renderFilters()` - Renderiza los filtros en la interfaz de usuario.
- `addFilter()` - Añade un nuevo filtro.
- `updateFilterType(index, type)` - Actualiza el tipo de valor del filtro.
- `updateFilter(index)` - Actualiza los detalles del filtro seleccionado.
- `removeFilter(index)` - Elimina un filtro.
- `onSecondMetricToggle()` - Maneja el cambio en la activación de la Segunda Métrica.
- `onQbChange()` - Sincroniza los cambios en la configuración del Constructor Visual con el estado actual.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas:
  - **Tabla:** `queries`
    - **Columnas:** `id`, `visual_state`
  - **Tabla:** `studio_schema`
    - **Columnas:** `ds_id`, `label`

### Estado y Variables Globales
- `currentQueryId` - ID de la consulta actual.
- `serverVisualState` - Estado visual del servidor.
- `visualState` - Estado visual actual.
- `currentSchema` - Esquema actual de la base de datos.

### Dependencias y Flujo
- **Dependencias Externas:** `fetch`
- **Archivos Importados:**
  - Ninguno
- **Archivos Exportados:**
  - Ninguno


---

## Archivo: ./static/js/bundle.js (Procesado en 8 partes)

#### --- PARTE 1 de 8 ---

### Resumen Funcional
El archivo `bundle.js` contiene módulos de utilidades para la interfaz de usuario (UI) y lógica del backend para un sistema de monitoreo de almacén (WMS). Incluye funciones para manejar modales, renderizar materiales, llenar selectores con áreas, leer datos JSON embebidos en el DOM, así como funciones de API para interactuar con el backend.

### Catálogo de Funciones y Clases
- `CoreUI.openModal(id)` - Muestra un modal por su ID.
- `CoreUI.closeModal(id)` - Oculta un modal por su ID.
- `CoreUI.renderMaterialModal(opts)` - Rellena y abre un modal con una lista de materiales.
- `CoreUI.populateAreaSelect(selectId, data, key)` - Llena un `<select>` con áreas únicas de un array.
- `CoreUI.getData(id)` - Lee y parsea JSON embebido en el DOM.
- `DashboardAPI._fetch(url, options)` - Realiza una solicitud HTTP a la API.
- `DashboardAPI.fetchKPIs(params)` - Obtiene indicadores clave del negocio (KPIs).
- `DashboardAPI.fetchFilteredData(params)` - Obtiene datos filtrados.
- `DashboardAPI.sync()` - Sincroniza los datos con el backend.
- `DashboardAPI.checkSyncStatus()` - Verifica el estado de la sincronización.
- `DashboardAPI.logout()` - Cierra sesión y limpia el almacenamiento local.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `window.CoreUI` - Objeto que expone funciones comunes para la UI.
- `window.openModal`, `window.closeModal` - Aliases globales para compatibilidad con handlers inline.

### Dependencias y Flujo
- **Dependencias Externas**: `fetch`
- **Archivos Importados**: Ninguno
- **Archivos Exportados**: `bundle.js` es importado por otros archivos del proyecto, como `_logout.html`, `dashboard_core.js`, etc.

#### --- PARTE 2 de 8 ---

### Resumen Funcional
El archivo `bundle.js` contiene funciones para renderizar gráficos de líneas y trellis en un sistema de monitoreo de almacén. Utiliza Chart.js para crear visualizaciones dinámicas basadas en datos proporcionados.

### Catálogo de Funciones y Clases
- `renderSaaSChart(container, queryId, data)` - Renderiza un gráfico de líneas.
- `renderSaaSTrellis(container, queryId, data)` - Renderiza una grilla de gráficos trellis.
- `initSaaSWidgets(params = null, rootElement = document)` - Inicializa widgets SaaS en el DOM.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `window.saasChartInstances` - Almacena instancias de gráficos Chart.js.
- `window.saasChartInstancesV2` - Almacena instancias de gráficos Chart.js para la versión 2.

### Dependencias y Flujo
- **Dependencias Externas**: `Chart.js`, `ChartDataLabels`
- **Archivos Importados**: No se importan archivos adicionales.
- **Archivos Exportados**: No se exportan funciones adicionales.

**Flujo de Datos**:
1. `initSaaSWidgets` es llamado al cargar el DOM.
2. Busca elementos con la clase `.saas-widget-v2`.
3. Para cada widget, llama a `renderSaaSChart` o `renderSaaSTrellis` según los datos proporcionados.
4. Los gráficos se renderizan en los contenedores correspondientes.

**Flujo de Datos (Continuación)**:
- `renderSaaSChart` y `renderSaaSTrellis` procesan los datos y crean instancias de Chart.js para renderizar los gráficos.
- Los gráficos se actualizan dinámicamente según los parámetros proporcionados en `initSaaSWidgets`.

**Flujo de Datos (Continuación)**:
- Los widgets pueden interactuar con el usuario a través de eventos como clics, que pueden abrir modales o cargar datos adicionales.

#### --- PARTE 3 de 8 ---

### Resumen Funcional
El archivo `bundle.js` contiene funciones JavaScript que se utilizan para inicializar widgets de monitoreo en un sistema de almacén (WMS). Incluye la actualización de valores en el DOM, carga de sugerencias de reabastecimiento y manejo de modales con detalles específicos.

### Catálogo de Funciones y Clases
- `initSaaSWidgetsV2(queryId)` - Inicializa widgets V2 basados en el ID de la consulta.
- `loadReplenishmentSuggestions(freq='all')` - Carga sugerencias de reabastecimiento en función de la frecuencia seleccionada.
- `openDrilldownModal(queryId, segmentLabel, materialId=null)` - Abre un modal con detalles de drill-down para una consulta específica.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `window.initSaaSWidgetsV2` - Función global que inicializa widgets V2.
- `window.loadReplenishmentSuggestions` - Función global que carga sugerencias de reabastecimiento.
- `window.openDrilldownModal` - Función global para abrir modales de drill-down.

### Dependencias y Flujo
- **Dependencias Externas**: No se mencionan dependencias externas específicas en el fragmento proporcionado.
- **Archivos Importados**: No hay importaciones de archivos dentro del fragmento proporcionado.
- **Archivos Exportados**: El archivo no exporta ninguna función o variable.

El flujo de datos es principalmente entre funciones y el DOM, con llamadas a APIs para cargar datos.

#### --- PARTE 4 de 8 ---

### Resumen Funcional
Este archivo JavaScript (`bundle.js`) contiene lógica para cargar y mostrar datos en una interfaz web, utilizando funciones como `fetch` para obtener datos de un servidor, manipular el DOM para actualizar la vista y renderizar tablas con información sobre materiales y entregas.

### Catálogo de Funciones y Clases
- **getData(id)** - Obtiene datos desde el almacenamiento local.
- **openModalArea(name, isCurrentMonth = false)** - Abre un modal con detalles de una área.
- **openModalWeekday(dayName, isCurrentMonth = false)** - Abre un modal con detalles de un día.
- **openModalUbicacion(name)** - Abre un modal con detalles de ubicaciones.
- **openModalUser(name)** - Abre un modal con detalles de usuarios.
- **switchVLView(view)** - Cambia la vista entre operativa y histórica.
- **toggleMulti(id)** - Alterna la visibilidad de elementos.
- **updateDeliveriesAnalytics()** - Actualiza los KPIs y filtra listas según selección.
- **toggleChartSelectAll(isChecked)** - Maneja el estado del checkbox "Seleccionar todo".
- **handleSmartCheckbox(cb)** - Maneja la lógica inteligente de los checkboxes.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- `currentModalContext` - Almacena el contexto actual del modal.
- `window.slaTrendChart`, `window.slaAreaTrendChart`, etc. - Referencias a gráficos que se redibujan en ciertas acciones.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas mencionadas directamente en el código proporcionado.
- **Flujo de Datos**: El flujo de datos comienza con una solicitud `fetch` para obtener datos, luego se procesan y renderizan en la interfaz web. Los eventos como clics en checkboxes o botones desencadenan funciones que actualizan el estado y la vista.

#### --- PARTE 5 de 8 ---

### Resumen Funcional
El archivo `bundle.js` contiene funciones y lógica para manejar la visualización de gráficos, tablas y modales en un sistema de monitoreo de almacén (WMS). Incluye funcionalidades para cargar datos desde una API, renderizar gráficos utilizando Chart.js, gestionar el estado del usuario y mostrar información detallada en modales.

### Catálogo de Funciones y Clases
- `cerrarTendenciaMaterial()` - Cierra un modal de tendencia de material.
- `loadData()` - Carga datos de transporte desde una API y los renderiza en gráficos y tablas.
- `getMonday(dateStr)` - Calcula la fecha del lunes correspondiente a una fecha dada.
- `updateTransporteChartGroup(group)` - Actualiza el grupo de datos para el gráfico de transporte.
- `loadPendingData()` - Carga y muestra los datos pendientes de entrega en una tabla con agrupación por mes y fecha.
- `renderChart()` - Renderiza un gráfico de líneas utilizando Chart.js.
- `renderTable(data)` - Renderiza una tabla con los últimos 25 registros de transporte.
- `openPdfViewer(url)` - Abre un modal para visualizar un PDF.
- `closePdfViewer()` - Cierra el modal del PDF.
- `searchTransporte()` - Realiza una búsqueda en tiempo real de datos de transporte y muestra los resultados.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `_tendenciaChart` - Variable global que almacena la instancia del gráfico de tendencia.
- `chartInstance` - Variable global que almacena la instancia del gráfico de transporte.
- `allTransporteData` - Array global que almacena los datos de transporte cargados desde la API.
- `currentChartGroup` - Variable global que almacena el grupo actual de datos para el gráfico de transporte.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `fetch` (API web para hacer solicitudes HTTP)
  - `Chart.js` (biblioteca para renderizar gráficos)

- **Archivos del Proyecto que Importan a este Archivo**:
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa**:
  - `transporte.js`
  - `tasks.js`
  - `inventory.js`

- **Flujo de Datos**: 
  - El archivo se carga en el navegador y ejecuta las funciones necesarias para cargar y mostrar datos.
  - Los datos son cargados desde una API utilizando `fetch`.
  - Los datos son procesados y renderizados en gráficos y tablas utilizando Chart.js y DOM manipulation.

#### --- PARTE 6 de 8 ---

### Resumen Funcional
El archivo `bundle.js` contiene funciones JavaScript que se utilizan para actualizar y renderizar información en una interfaz de usuario web. Específicamente, maneja la carga de datos desde un servidor a través de peticiones AJAX, actualiza el contenido de tablas y elementos HTML basándose en los datos recibidos, y controla la interacción con modales y gráficos.

### Catálogo de Funciones y Clases
- `renderAlerts()` - Renderiza una tabla de alertas.
- `renderCombos(filterText)` - Renderiza una lista de combinaciones de materiales.
- `renderScatter()` - Renderiza un gráfico de dispersión.
- `openModalAlerts()` - Abre el modal de alertas y carga los datos.
- `openModalCombos()` - Abre el modal de combinaciones y carga los datos.
- `openModalScatter()` - Abre el modal de scatter y carga los datos.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `ubicTimer` - Variable global que almacena un temporizador para la actualización de datos.

### Dependencias y Flujo
Dependencias:
- `CoreUI` (vía `window.CoreUI`)
- `Chart.js`

Flujo:
1. **analytics_proyecciones.js**:
   - Carga los datos necesarios desde el almacenamiento local (`getData`) y los filtra según los criterios de búsqueda.
   - Renderiza las tablas y gráficos en función de los datos filtrados.

2. **docs_explorer.js**:
   - Llama a la API para cargar el árbol de documentos y renderiza el contenido del documento seleccionado.

3. **productivity_daily.js**:
   - No se muestra ninguna interacción con base de datos ni dependencias externas específicas en este fragmento.

El flujo general es que los componentes de la interfaz web interactúan con funciones JavaScript para cargar y mostrar datos, utilizando `fetch` para obtener información del servidor.

#### --- PARTE 7 de 8 ---

### Resumen Funcional
El archivo `bundle.js` contiene funciones y lógica relacionada con la interacción del usuario en una interfaz web de sistema de monitoreo de almacén (WMS). Permite cambiar entre diferentes pestañas, cargar datos de productividad diaria y mensual, y renderizar gráficos y tablas basados en esos datos.

### Catálogo de Funciones y Clases
- `changeProductivityDate(offset)` - Cambia la fecha seleccionada para el análisis de productividad.
- `changeProductivityMonth(offsetMonths)` - Cambia el mes seleccionado para el análisis de productividad mensual.
- `loadProductivityData()` - Carga los datos de productividad diaria y actualiza la interfaz web.
- `renderKPI1(summary)` - Renderiza el KPI 1 (resumen de movimientos diarios).
- `renderKPI2(trend)` - Renderiza el KPI 2 (tendencia de movimientos diarios).
- `renderKPI3(gaps)` - Renderiza el KPI 3 (baches en la productividad).
- `renderKPI4(heatmapData)` - Renderiza el KPI 4 (mapa de calor de productividad).

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `currentDailyData` - Almacena los datos de productividad diarios actuales.
- `selectedDailyUsers` - Lista de usuarios seleccionados para el análisis diario.
- `productivityTrendChartInst` - Instancia del gráfico de tendencia de movimientos diarios.
- `currentMonthlyData` - Almacena los datos de productividad mensuales actuales.
- `selectedMonthlyUsers` - Lista de usuarios seleccionados para el análisis mensual.
- `productivityMonthlyTrendChartInst` - Instancia del gráfico de tendencia de movimientos mensuales.

### Dependencias y Flujo
- **Dependencias Externas**: `fetch`, `Chart.js`
- **Archivos Importados**: Ninguno
- **Archivos Exportados**: Ninguno

El flujo de datos es el siguiente:
1. El usuario selecciona una pestaña (diaria o mensual).
2. Se llama a las funciones correspondientes (`changeProductivityDate`, `changeProductivityMonth`).
3. Estas funciones cargan los datos necesarios y llaman a las funciones de renderizado (`renderKPI1`, `renderKPI2`, etc.) para actualizar la interfaz web con los nuevos datos.

#### --- PARTE 8 de 8 ---

### Resumen Funcional
Este archivo JavaScript (`bundle.js`) contiene funciones para crear y actualizar tablas HTML dinámicamente basadas en datos de usuarios y sus movimientos. También incluye funciones para abrir y cerrar modales que muestran detalles diarios y mensuales de los movimientos de usuario.

### Catálogo de Funciones y Clases
- `getColor(val, max)` - Calcula un color RGB con opacidad basada en el valor proporcionado.
- `abrirDetalleUsuario(usuario)` - Abre el modal para mostrar los detalles diarios de un usuario.
- `cargarNivel2Diario(operacion)` - Carga los detalles del nivel 2 (detalles específicos) para una operación diaria.
- `volverNivel1Diario()` - Cierra el nivel 2 y vuelve al nivel 1 en el modal de movimientos diarios.
- `cerrarDetalleUsuario()` - Cierra el modal de movimientos diarios.
- `abrirDetalleMensualUsuario(usuario)` - Abre el modal para mostrar los detalles mensuales de un usuario.
- `cargarNivel2Mensual(operacion)` - Carga los detalles del nivel 2 (detalles específicos) para una operación mensual.
- `volverNivel1Mensual()` - Cierra el nivel 2 y vuelve al nivel 1 en el modal de movimientos mensuales.
- `cerrarDetalleMensualUsuario()` - Cierra el modal de movimientos mensuales.

### Interacción con Base de Datos
Ninguna. Este archivo no interactúa directamente con una base de datos. Los datos se obtienen a través de llamadas AJAX a endpoints de API (`/api/v1/analytics/productivity/user-movements-summary`, `/api/v1/analytics/productivity/user-movements-details`, etc.).

### Estado y Variables Globales
- `currentDailyUsuario` - Almacena el usuario seleccionado para los detalles diarios.
- `currentDailyDate` - Almacena la fecha seleccionada para los detalles diarios.
- `currentMonthlyUsuario` - Almacena el usuario seleccionado para los detalles mensuales.
- `currentMonthlyDate` - Almacena la fecha seleccionada para los detalles mensuales.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas específicas en este fragmento de código.
- **Flujo de Datos**:
  - El archivo `bundle.js` es consumido por otros archivos JavaScript que no se muestran aquí.
  - Los datos para las tablas y modales se obtienen a través de llamadas AJAX al backend FastAPI.

Este archivo es crucial para la interfaz de usuario del sistema, proporcionando una forma visual de interactuar con los datos de movimientos de usuarios en el sistema de monitoreo de almacén.


---

## Archivo: ./static/js/consumos.js

### Resumen Funcional
Este archivo JavaScript (`consumos.js`) es parte del sistema de monitoreo de almacén (WMS). Se encarga de manejar la interacción con el usuario, como buscar materiales por Centro de Costo (CeCo) o por lista de materiales ingresada en un textarea. También se encarga de renderizar tablas y mostrar tendencias mensuales de los materiales.

### Catálogo de Funciones y Clases
- `handlePaste(e)` - Obsoleto: Manejaba el pegado de múltiples líneas, pero ahora es obsoleto.
- `limpiarGrilla()` - Limpia la grilla y oculta el contenedor de resultados.
- `formatearDinero(valor)` - Formatea un valor numérico como dinero.
- `formatearNumero(valor)` - Formatea un valor numérico como número.
- `filterTable(tableId)` - Filtra una tabla según los valores ingresados en las celdas de filtro.
- `renderVanillaTable(tbodyId, data, columns, onRowClick = null)` - Renderiza una tabla usando JavaScript puro.
- `buscarPorCeCo()` - Busca materiales por Centro de Costo y muestra los resultados.
- `buscarPorMateriales()` - Busca materiales ingresados en un textarea y muestra los resultados.
- `abrirTendenciaMaterial(material, areaNegocio, descripcion, ceco = '')` - Abre el modal con la tendencia mensual del material.
- `cerrarTendenciaMaterial()` - Cierra el modal de tendencia.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos. Todas las consultas y operaciones se realizan a través de llamadas a la API FastAPI.

### Estado y Variables Globales
- `_tendenciaChart` - Variable global que almacena el estado del gráfico de tendencias mensuales.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas mencionadas.
- **Flujo de Datos**:
  - `consumos.js` importa y es importado por otros archivos JavaScript dentro del proyecto, pero no se especifican los detalles específicos en este fragmento.


---

## Archivo: ./static/js/core_ui.js

### Resumen Funcional
El archivo `core_ui.js` es un módulo de utilidades de interfaz de usuario compartido por todas las vistas del sistema de monitoreo de almacén (WMS). Proporciona funciones para mostrar y ocultar modales, renderizar modales de lista de materiales, poblar selectores con áreas únicas y leer datos JSON embebidos en el DOM.

### Catálogo de Funciones y Clases
- `CoreUI.openModal(id)` - Muestra un modal por su ID de elemento.
- `CoreUI.closeModal(id)` - Oculta un modal por su ID de elemento.
- `CoreUI.renderMaterialModal(opts)` - Rellena y abre un modal de lista de materiales con los ítems proporcionados.
- `CoreUI.populateAreaSelect(selectId, data, key)` - Rellena un elemento `<select>` con áreas únicas encontradas en un array de datos.
- `CoreUI.getData(id)` - Lee y parsea JSON embebido en el textContent de un elemento del DOM.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas.
- **Flujo de datos**: El archivo no importa ni es importado por otros archivos. Se utiliza directamente en el HTML a través de `<script>` tags.


---

## Archivo: ./static/js/dashboard_api.js

### Resumen Funcional
El archivo `dashboard_api.js` contiene la lógica de la API para el módulo del panel de control en un sistema de monitoreo de almacén (WMS). Define funciones para interactuar con endpoints de la API, como obtener indicadores clave de rendimiento (KPIs), datos filtrados y sincronizar los datos.

### Catálogo de Funciones y Clases
- `_fetch(url, options = {})` - Realiza una solicitud HTTP a la URL especificada con las opciones proporcionadas.
- `fetchKPIs(params)` - Obtiene KPIs basándose en los parámetros proporcionados.
- `fetchFilteredData(params)` - Obtiene datos filtrados según los parámetros proporcionados.
- `sync()` - Sincroniza los datos del almacén con el servidor.
- `checkSyncStatus()` - Verifica el estado de la sincronización actual.
- `logout()` - Cierra sesión y limpia el almacenamiento local.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- Ninguna variable global explícita está declarada en este archivo.

### Dependencias y Flujo
- **Dependencias**: `fetch` (API web para hacer solicitudes HTTP).
- **Archivos que importan a este archivo**: Ninguno.
- **Archivos que este archivo importa**: Ninguno.
- **Flujo de datos**: El flujo de datos se gestiona principalmente a través de las funciones `_fetch`, `fetchKPIs`, `fetchFilteredData`, `sync`, `checkSyncStatus` y `logout`. Los datos son solicitados y procesados en el cliente, y la interacción con el servidor se realiza mediante solicitudes HTTP.

Este archivo es una parte integral del frontend que interactúa con el backend a través de endpoints definidos para obtener y gestionar los datos necesarios para el panel de control.


---

## Archivo: ./static/js/dashboard_charts.js

### Resumen Funcional
Este archivo JavaScript (`dashboard_charts.js`) se encarga de inicializar y gestionar un gráfico de barras pilaado en el panel de control del sistema de monitoreo de almacén (WMS). El gráfico muestra datos agrupados por áreas y centros, con la capacidad de seleccionar/deseleccionar ciertas áreas o centros para mostrar u ocultar sus datos en el gráfico.

### Catálogo de Funciones y Clases
- `stackedTotalPlugin(id: string, afterDatasetsDraw: function)` - Plugin para calcular y mostrar el total acumulado en cada barra del gráfico.
  - Parámetros:
    - `id`: Identificador único del plugin.
    - `afterDatasetsDraw`: Función que se ejecuta después de dibujar los conjuntos de datos, calculando y mostrando el total acumulado.

- `initWeeklyChart(chartLabels: Array<string>, chartDatasets: Array<Object>)` - Inicializa el gráfico de barras pilaado.
  - Parámetros:
    - `chartLabels`: Etiquetas para los ejes X del gráfico.
    - `chartDatasets`: Conjuntos de datos que se mostrarán en el gráfico.

- `toggleChartSelectAll(isChecked: boolean)` - Función para seleccionar/deseleccionar todos los checkboxes relacionados con áreas y centros.
  - Parámetros:
    - `isChecked`: Valor booleano que indica si se debe seleccionar o deseleccionar todos los checkboxes.

- `updateChartVisibility()` - Actualiza la visibilidad de los conjuntos de datos del gráfico según las selecciones realizadas en los checkboxes.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `window.weeklyChart`: Variable global que almacena el objeto del gráfico inicializado.

### Dependencias y Flujo
- **Dependencias**: No se mencionan dependencias externas específicas.
- **Flujo de Datos**:
  - El archivo importa funciones y variables desde otros archivos del proyecto, pero no se muestra cómo estos archivos están estructurados o qué datos fluyen entre ellos.
  - Los eventos DOM (`DOMContentLoaded`, `change` en checkboxes) desencadenan la inicialización y actualización del gráfico.


---

## Archivo: ./static/js/dashboard_core.js

### Resumen Funcional
El archivo `dashboard_core.js` contiene funciones y métodos para renderizar filas de una tabla, ejecutar filtros en un panel de control de almacén, manejar la interacción con el usuario (como seleccionar checkboxes y ordenar tablas), generar PDFs y sincronizar datos.

### Catálogo de Funciones y Clases
- `renderTableRow(t)` - Renderiza una fila de tabla con los detalles del pedido.
- `executeFilters()` - Ejecuta los filtros aplicados por el usuario en la interfaz.
- `applyFilters()` - Aplica los filtros cuando se selecciona un checkbox o se cambia el estado de "Seleccionar todo".
- `getCheckboxValues(className)` - Obtiene los valores de los checkboxes con una clase específica.
- `toggleSelectAll(className, isChecked)` - Maneja la selección de todos los checkboxes en una categoría.
- `handleSmartCheckbox(cb, className, selectAllId, context)` - Maneja el comportamiento inteligente de los checkboxes.
- `filterTable()` - Filtra las filas de la tabla según los criterios de búsqueda ingresados por el usuario.
- `sortTable(idx)` - Ordena las filas de la tabla según una columna específica.
- `updateLogoVal(btn)` - Actualiza el valor del checkbox que indica si se debe incluir el logo en el PDF.
- `pdfSubmit(btn, frameTarget, preview)` - Envía un formulario para generar y descargar PDFs.
- `downloadBulk(action, btn)` - Genera y descarga PDFs en lote según los criterios de filtro.
- `syncData(e, onlyPoll = false)` - Inicia la sincronización de datos con el servidor y maneja el estado de carga.
- `startSyncPolling(btn)` - Comienza a sondear el estado de la sincronización.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales explícitas definidas en este archivo. Las funciones utilizan elementos del DOM para almacenar y recuperar estado, como checkboxes seleccionados y valores de entrada de usuario.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas.
- **Flujo de Datos**:
  - `dashboard_core.js` es consumido por el archivo que contiene la interfaz del usuario (no especificado en el fragmento).
  - El archivo consume funciones de `DashboardAPI`, lo que sugiere que existe un módulo separado para interactuar con el backend.
  - Los datos se obtienen a través de llamadas asíncronas (`Promise.all`) a `DashboardAPI.fetchKPIs` y `DashboardAPI.fetchFilteredData`.
  - Los resultados son utilizados para actualizar la interfaz del usuario, incluyendo la tabla de pedidos, los KPIs y las notificaciones.

Este archivo es crucial para el funcionamiento del panel de control en el sistema de monitoreo de almacén, proporcionando funcionalidades avanzadas como filtros dinámicos, generación de PDFs y sincronización de datos.


---

## Archivo: ./static/js/dashboard_saas.js

### Resumen Funcional
El archivo `dashboard_saas.js` es un componente del sistema de monitoreo de almacén (WMS) que inicializa y gestiona widgets interactivos en la interfaz de usuario. Estos widgets pueden mostrar gráficos y tablas dinámicas basadas en datos obtenidos a través de una API.

### Catálogo de Funciones y Clases
- `initSaaSWidgets(params = null)` - Inicializa los widgets SaaS, leyendo parámetros del DOM o proporcionados explícitamente.
- `renderSaaSChart(container, queryId, data)` - Renderiza un gráfico de líneas para el widget SaaS.
- `renderSaaSTrellis(container, queryId, data)` - Renderiza una trellis de gráficos para el widget SaaS.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos. Todas las operaciones de obtención de datos se realizan a través de una API (`DashboardAPI`).

### Estado y Variables Globales
- `window.saasChartInstances` - Almacena instancias de gráficos Chart.js renderizados.

### Dependencias y Flujo
- **Dependencias**: 
  - `ChartDataLabels` (plugin para Chart.js).
  - `DashboardAPI` (API personalizada para obtener datos del servidor).

- **Flujo**:
  - El archivo se carga en el DOM.
  - Al cargar, inicializa los widgets SaaS llamando a `initSaaSWidgets()`.
  - `initSaaSWidgets()` lee parámetros de filtros y solicita datos a través de la API.
  - Los datos recibidos se utilizan para renderizar gráficos o tablas en el DOM.

El flujo es unidireccional, con el archivo consumiendo datos de la API y generando contenido visual en el navegador.


---

## Archivo: ./static/js/deliveries.js

### Resumen Funcional
El archivo `deliveries.js` contiene la lógica para el monitoreo de entregas en un sistema de almacén (WMS). Implementa funciones para abrir modales con detalles de áreas, días de la semana y ubicaciones, así como controladores para cambiar entre vistas operativas e históricas. También inicializa gráficos y actualiza los KPIs según las selecciones del usuario.

### Catálogo de Funciones y Clases
- `openModalWeekday(dayName, isCurrentMonth = false)` - Abre un modal con detalles del día seleccionado.
- `openModalUbicacion(name)` - Abre un modal con detalles de la ubicación seleccionada.
- `openModalArea(name, isCurrentMonth = false)` - Abre un modal con detalles de la área seleccionada.
- `openModalUser(name)` - Abre un modal con detalles del usuario seleccionado.
- `switchVLView(view)` - Cambia entre las vistas operativas e históricas.
- `updateDeliveriesAnalytics()` - Recalcula y actualiza los KPIs y filtra los gráficos según las selecciones del usuario.
- `toggleMulti(id)` - Alterna la visibilidad de un elemento con el ID especificado.
- `toggleChartSelectAll(isChecked)` - Maneja la selección de todos los elementos en una lista de verificación.
- `handleSmartCheckbox(cb)` - Maneja la lógica inteligente para las casillas de verificación, asegurando que no se pueda seleccionar vacío.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `currentModalContext` - Almacena el contexto actual del modal (área o día de la semana).
- `window.intensidadChart` - Referencia al gráfico de intensidad de entregas.
- `window.slaTrendChart`, `window.slaAreaTrendChart`, etc. - Referencias a otros gráficos históricos.

### Dependencias y Flujo
- **Dependencias**: `core_ui.js`
- **Archivos que importan este archivo**: Ninguno
- **Archivos que este archivo importa**: Ninguno

El flujo de datos se inicia con el evento `DOMContentLoaded`, donde se inicializan los gráficos y se configuran los controladores para los modales y las vistas. Los eventos de usuario, como la selección de áreas o días, desencadenan la actualización de KPIs y filtros en los gráficos.


---

## Archivo: ./static/js/docs_explorer.js

### Resumen Funcional
El archivo `docs_explorer.js` es un componente del sistema de monitoreo de almacén (WMS) que se encarga de cargar y renderizar la estructura de documentos en un árbol visual, permitiendo expandir/colapsar carpetas y cargar el contenido de los archivos seleccionados.

### Catálogo de Funciones y Clases
- `initDocs()` - Inicializa el explorador de documentos, llamando a la API para obtener la estructura del árbol de documentos y renderizarla.
- `loadFile(path)` - Carga el contenido de un archivo específico en la vista principal.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- **Dependencias**: `fetch`, `marked` (si está disponible).
- **Flujo**:
  - El archivo se carga inicialmente (`DOMContentLoaded`).
  - Al hacer clic en la pestaña de "Docs", se ejecuta `initDocs()`.
  - `initDocs()` realiza una solicitud a `/api/docs/tree` para obtener la estructura del árbol y luego llama a `renderNodes(data, treeRoot)` para renderizarla.
  - Al seleccionar un archivo en el árbol, se ejecuta `loadFile(node.path)`, que carga el contenido del archivo en `#docs-content-view`.

El flujo de datos es unidireccional desde la API hasta el cliente y luego hacia la vista.


---

## Archivo: ./static/js/inventory.js

### Resumen Funcional
El archivo `inventory.js` contiene lógica para manejar movimientos en un sistema de monitoreo de almacén (WMS). Incluye funciones para abrir modales con información sobre ubicaciones y usuarios, así como una funcionalidad de búsqueda dinámica para mostrar el stock y historial de ubicaciones.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra mensajes en la consola.
- `parseFormattedInt(val)` - Convierte un valor a un entero formateado, eliminando caracteres no numéricos.
- `window.openModalUbicacion(name)` - Abre un modal con información sobre una ubicación específica.
- `window.openModalUserInv(name)` - Abre un modal con información sobre un usuario específico.
- `window.switchInventarioView(view)` - Cambia la vista del inventario según el tipo de visualización seleccionada.

### Interacción con Base de Datos
Ninguna. El archivo no realiza ninguna operación directa en una base de datos.

### Estado y Variables Globales
No hay variables globales explícitas definidas en este archivo.

### Dependencias y Flujo
- **Dependencias**: `core_ui.js` (provee funciones como `CoreUI.openModal`, `CoreUI.closeModal`, etc.)
- **Flujo de Datos**:
  - El archivo se carga cuando el DOM esté listo.
  - Llama a funciones de `core_ui.js` para abrir modales y renderizar contenido.
  - Realiza solicitudes AJAX al servidor para obtener datos de ubicaciones y stock, que luego se procesan y mostran en la interfaz.

Este archivo es parte del frontend de un sistema WMS, gestionando la interacción con el usuario a través de modales y búsqueda dinámica.


---

## Archivo: ./static/js/productivity_daily.js

### Resumen Funcional
Este archivo JavaScript (`productivity_daily.js`) se encarga de manejar la interacción del usuario con los gráficos y tablas de productividad diaria en el sistema de monitoreo de almacén (WMS). Permite filtrar usuarios, cargar datos según la fecha seleccionada, y renderizar diferentes KPIs como resúmenes, tendencias, baches y mapas de calor.

### Catálogo de Funciones y Clases
- `toggleDailyUserFilter()` - Muestra u oculta el filtro de usuarios diarios.
- `filterDailyUserList()` - Filtra la lista de usuarios según el texto ingresado en el campo de búsqueda.
- `renderDailyUserCheckboxes(summary)` - Renderiza los checkboxes para seleccionar usuarios, agrupados por grupos y individuales.
- `selectUserGroup(groupUsers)` - Selecciona todos los usuarios de un grupo específico.
- `toggleAllDailyUsers()` - Selecciona o deselecciona todos los usuarios.
- `onDailyUserCheckboxChange()` - Maneja el cambio en la selección de checkboxes de usuarios.
- `renderFilteredDaily()` - Renderiza los KPIs filtrados según los usuarios seleccionados.
- `changeProductivityDate(offset)` - Cambia la fecha seleccionada para cargar nuevos datos.
- `changeProductivityMonth(offsetMonths)` - Cambia el mes seleccionado para cargar nuevos datos.
- `loadProductivityData()` - Carga los datos de productividad diaria desde una API y renderiza los KPIs correspondientes.
- `renderKPI1(summary)` - Renderiza el resumen de movimientos diarios.
- `renderKPI2(trend)` - Renderiza la tendencia de movimientos diarios en un gráfico de líneas.
- `renderKPI3(gaps)` - Renderiza los baches de productividad diaria.
- `renderKPI4(heatmapData)` - Renderiza el mapa de calor de productividad diaria.

### Interacción con Base de Datos
Ninguna. El archivo no realiza ninguna consulta a una base de datos.

### Estado y Variables Globales
- `productivityTrendChartInst` - Instancia del gráfico de tendencias.
- `currentDailyData` - Datos actuales de productividad diaria.
- `selectedDailyUsers` - Usuarios seleccionados para el filtrado.
- `userGroupsCache` - Grupos de usuarios almacenados en caché.

### Dependencias y Flujo
Dependencias:
- `Chart.js` - Usado para renderizar gráficos.

Flujo:
- El archivo se carga cuando se abre la página.
- Se inicializan variables globales y eventos.
- Al seleccionar una fecha o cambiar de pestaña, se llama a `loadProductivityData()` para cargar los datos correspondientes.
- Los KPIs se renderizan según los datos cargados y las selecciones del usuario.


---

## Archivo: ./static/js/productivity_modals.js

### Resumen Funcional
Este archivo contiene funciones JavaScript para abrir y cargar detalles de movimientos diarios y mensuales de usuarios en un sistema de monitoreo de almacén. Utiliza una interfaz modal para mostrar los datos y realiza solicitudes a una API para obtener los datos necesarios.

### Catálogo de Funciones y Clases
- `abrirDetalleUsuario(usuario)` - Abre el modal de movimientos diarios del usuario especificado.
- `cargarNivel2Diario(operacion)` - Carga el nivel 2 de detalles para una operación específica en el nivel 1 de los movimientos diarios.
- `volverNivel1Diario()` - Vuelve al nivel 1 de los movimientos diarios.
- `cerrarDetalleUsuario()` - Cierra el modal de movimientos diarios.
- `abrirDetalleMensualUsuario(usuario)` - Abre el modal de resumen mensual del usuario especificado.
- `cargarNivel2Mensual(operacion)` - Carga el nivel 2 de detalles para una operación específica en el nivel 1 de los movimientos mensuales.
- `volverNivel1Mensual()` - Vuelve al nivel 1 de los movimientos mensuales.
- `cerrarDetalleMensualUsuario()` - Cierra el modal de resumen mensual del usuario.

### Interacción con Base de Datos
No se utiliza ninguna base de datos directamente en este archivo. Todas las operaciones de carga de datos se realizan a través de solicitudes HTTP a una API (`/api/v1/analytics/productivity/user-movements-summary`, `/api/v1/analytics/productivity/user-movements-details`, `/api/v1/analytics/productivity/user-movements-monthly-summary`, `/api/v1/analytics/productivity/user-movements-monthly-details`).

### Estado y Variables Globales
- `currentDailyUsuario` - Almacena el usuario seleccionado para los movimientos diarios.
- `currentDailyDate` - Almacena la fecha seleccionada para los movimientos diarios.
- `currentMonthlyUsuario` - Almacena el usuario seleccionado para el resumen mensual.
- `currentMonthlyDate` - Almacena la fecha seleccionada para el resumen mensual.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas en este archivo.
- **Flujo de Datos**:
  - El archivo es consumido por HTML que contiene los elementos DOM necesarios (modales, tablas, etc.).
  - Los datos se cargan a través de solicitudes HTTP a la API FastAPI definida en el proyecto.

Este archivo no interactúa con una base de datos directamente, sino que consume datos desde una API para mostrar detalles de movimientos diarios y mensuales de usuarios en un sistema de monitoreo de almacén.


---

## Archivo: ./static/js/productivity_monthly.js

### Resumen Funcional
Este archivo contiene la lógica para renderizar y gestionar los datos de productividad mensual en un sistema de almacén. Permite filtrar por usuarios, cargar datos desde una API, y visualizar KPIs como resúmenes de actividad, gráficos de tendencias y mapas de calor.

### Catálogo de Funciones y Clases
- `toggleMonthlyUserFilter()` - Alterna la visibilidad del filtro de usuarios.
- `renderMonthlyUserCheckboxes(summary)` - Renderiza los checkboxes para filtrar por usuarios.
- `toggleAllMonthlyUsers()` - Selecciona/deselecciona todos los usuarios en el filtro.
- `onMonthlyUserCheckboxChange()` - Maneja el cambio en el estado de los checkboxes de usuario.
- `renderFilteredMonthly()` - Filtra y renderiza los KPIs según los usuarios seleccionados.
- `loadMonthlyProductivityData()` - Carga los datos de productividad mensuales desde la API.
- `renderMonthlyKPI1(summary)` - Renderiza el primer KPI (resumen de actividad).
- `renderMonthlyKPI2(shifts)` - Renderiza el segundo KPI (tendencias por turno).
- `renderMonthlyKPI3(heatmapData)` - Renderiza el tercer KPI (mapa de calor).

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `productivityMonthlyTrendChartInst` - Instancia del gráfico de tendencias mensuales.
- `currentMonthlyData` - Datos actuales de productividad mensual.
- `selectedMonthlyUsers` - Usuarios seleccionados para el filtro.

### Dependencias y Flujo
- **Dependencias**: No se mencionan librerías externas específicas en este fragmento.
- **Flujo de Datos**:
  - El archivo es consumido por HTML (no se muestra aquí).
  - Importa funciones desde otros archivos JavaScript del proyecto, pero no se detalla cuáles son estos archivos.


---

## Archivo: ./static/js/saas_engine_core.js (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `saas_engine_core.js` es un script que inicializa widgets de gráficos y KPIs en una interfaz web, utilizando datos obtenidos a través de una API. Los widgets pueden mostrar diferentes tipos de gráficos (lineales, trellis, etc.) basándose en los parámetros proporcionados.

### Catálogo de Funciones y Clases
- `initSaaSWidgetsV2(params = null, rootElement = document)` - Inicializa los widgets SaaS V2.
- `loadReplenishmentSuggestions(freq = 'all')` - Carga sugerencias de abastecimiento en una tabla.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- `window.saasChartInstancesV2` - Almacena instancias de gráficos Chart.js para widgets trellis.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `fetch` (API web para hacer solicitudes HTTP).
  - `ChartDataLabels` (plugin para Chart.js que permite mostrar etiquetas en los gráficos).

- **Archivos del Proyecto Importados**:
  - Ninguno.

- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno.

- **Flujo de Datos**: 
  - El archivo se ejecuta al cargar el DOM (`DOMContentLoaded`).
  - Llama a `initSaaSWidgetsV2()` y `loadReplenishmentSuggestions()` con un pequeño retraso.
  - Los widgets son inicializados y actualizados según los parámetros proporcionados.

El flujo de datos es unidireccional, desde el archivo hasta la interfaz web y viceversa para las interacciones del usuario.


---

## Archivo: ./static/js/saas_engine_drilldown.js

### Resumen Funcional
El archivo `saas_engine_drilldown.js` contiene funciones para abrir modales de detalles y cargar tablas dinámicas con datos desde una API. Los modales incluyen detalles de materiales, áreas de negocio y estadísticas relacionadas.

### Catálogo de Funciones y Clases
- `window.openDrilldownModal(queryId, segmentLabel, materialId = null)` - Abre el modal de detalles para un área o material específico.
- `window.sortDrilldownTable(n)` - Ordena la tabla de detalles por una columna específica.
- `window.filterDrilldownTable()` - Filtra los datos de la tabla según los valores ingresados en los campos de búsqueda.
- `window.openCmv201Modal()` - Abre el modal para mostrar resúmenes de CMV 201.
- `window.loadCmv201Data(planType)` - Carga los datos del resumen de CMV 201 según el tipo de planificación seleccionado.
- `window.openCmv201AreaDetails(area)` - Abre el modal para mostrar detalles específicos de una área en CMV 201.
- `window.backToCmv201Summary()` - Vuelve al resumen general de CMV 201.
- `window.onCmv201MonthChange()` - Maneja el cambio de mes seleccionado en los modales de CMV 201 y CMV 261.
- `window.loadCmv201AreaDetails()` - Carga los detalles específicos de una área en CMV 201 según el mes seleccionado.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos. Los datos se cargan a través de llamadas a la API FastAPI.

### Estado y Variables Globales
- `window.currentCmv201PlanType` - Almacena el tipo de planificación seleccionado para CMV 201.
- `window.currentCmv201Area` - Almacena el área de negocio seleccionada en los modales de CMV 201 y CMV 261.
- `window.cmv201MonthsAvailable` - Almacena los meses disponibles para la visualización en los modales de CMV 201 y CMV 261.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas específicas.
- **Flujo de Datos**:
  - `saas_engine_drilldown.js` importa y es importado por otros archivos JavaScript dentro del proyecto, pero no hay intercambio explícito de datos entre ellos.


---

## Archivo: ./static/js/sla_table.js

### Resumen Funcional
El archivo `sla_table.js` contiene funciones relacionadas con la interacción de un usuario con una tabla de auditoría de SLA (Service Level Agreement) en un sistema de monitoreo de almacén. Las funciones permiten abrir y cerrar modales para visualizar PDFs, enviar formularios y manejar estados de botones.

### Catálogo de Funciones y Clases
- `openPdfModal()` - Abre el modal para mostrar un PDF.
- `closePdfModal()` - Cierra el modal y limpia el contenido del iframe.
- `pdfSubmit(btn, frameTarget, preview)` - Envía un formulario y maneja la interacción con un botón.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas.
- **Flujo**: El archivo no importa ni es importado por otros archivos. Las funciones están disponibles globalmente a través de `window.pdfSubmit` y `window.closePdfModal`.

El flujo de datos se realiza a través del formulario HTML, donde el usuario interactúa con un botón que invoca la función `pdfSubmit`. Esta función envía el formulario al servidor y maneja la interacción del usuario mientras el formulario se procesa.


---

## Archivo: ./static/js/tasks.js

### Resumen Funcional
El archivo `tasks.js` contiene la lógica para inicializar y configurar gráficos de tendencias y usuarios en una interfaz web utilizando la biblioteca Chart.js. Los datos necesarios se obtienen del DOM y se utilizan para crear gráficos de líneas y barras con opciones personalizadas.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra mensajes en la consola.
- `getData(id)` - Obtiene datos JSON desde elementos del DOM.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: 
  - `Chart.js` (incluye `ChartDataLabels`)
  
- **Flujo**:
  - El archivo se ejecuta cuando el DOM esté completamente cargado (`DOMContentLoaded`).
  - Llama a `getData()` para obtener datos de los elementos del DOM.
  - Utiliza estos datos para crear gráficos con Chart.js.

### Notas Adicionales
- El código utiliza la biblioteca Chart.js para crear gráficos interactivos en el navegador.
- Los gráficos se inicializan con opciones personalizadas, incluyendo colores, fuentes y estilos específicos.


---

## Archivo: ./static/js/transporte.js

### Resumen Funcional
El archivo `transporte.js` es un script JavaScript que se encarga de cargar y mostrar datos de transporte en una interfaz web. Realiza solicitudes a una API para obtener información sobre entregas, renderiza gráficos y tablas con estos datos, y permite la búsqueda y visualización de PDFs.

### Catálogo de Funciones y Clases
- `loadData()` - Carga los datos de transporte desde la API y actualiza la interfaz.
- `getMonday(dateStr)` - Calcula la fecha del lunes correspondiente a una fecha dada.
- `updateTransporteChartGroup(group)` - Actualiza el grupo de datos para el gráfico de transporte.
- `loadPendingData()` - Carga los datos pendientes de entrega y los muestra en una tabla con detalles agrupados por mes y fecha.
- `renderChart()` - Renderiza un gráfico de líneas mostrando las entregas y bultos según el grupo seleccionado (mensual o semanal).
- `renderTable(data)` - Renderiza una tabla con los últimos 25 registros de transporte.
- `openPdfViewer(url)` - Abre un modal para visualizar un PDF.
- `closePdfViewer()` - Cierra el modal y detiene la carga del PDF.
- `searchTransporte()` - Realiza una búsqueda en tiempo real de datos de transporte según un término ingresado.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos. Todas las operaciones de lectura y escritura se realizan a través de solicitudes HTTP a la API FastAPI.

### Estado y Variables Globales
- `chartInstance` - Almacena la instancia del gráfico actual.
- `allTransporteData` - Almacena todos los datos de transporte cargados desde la API.
- `currentChartGroup` - Almacena el grupo actual seleccionado para el gráfico (mensual o semanal).
- `transporteSearchTimeout` - Almacena un temporizador para el debouncing en la búsqueda.

### Dependencias y Flujo
- **Dependencias**: 
  - `fetch` - Para hacer solicitudes HTTP.
  - `Chart.js` y `ChartDataLabels` - Para renderizar gráficos.
  
- **Flujo de Datos**:
  - El archivo se carga en el DOM (`DOMContentLoaded`).
  - Llama a `loadData()` al cargar la página.
  - `loadData()` hace una solicitud a `/api/transporte/data` para obtener los datos de transporte y luego llama a `renderChart()`, `renderTable()`, y `loadPendingData()`.
  - `loadPendingData()` hace una solicitud a `/api/transporte/pending` para obtener los datos pendientes.
  - Los eventos de clic en los elementos del DOM (como botones, encabezados de tabla) invocan funciones como `updateTransporteChartGroup()`, `openPdfViewer()`, y `closePdfViewer()`.
  - La función `searchTransporte()` se ejecuta cuando el usuario ingresa texto en un campo de búsqueda.


---

## Archivo: ./templates/analytics_proyecciones.html

### Resumen Funcional
El archivo `analytics_proyecciones.html` es una plantilla HTML para la interfaz de usuario del módulo de análisis predictivo en el Sistema de Monitoreo de Almacén (WMS). Muestra información sobre alertas de desplanificación, un gráfico de dispersión y analisis de market basket.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada directamente en este archivo HTML. Todas las interacciones son a través de JavaScript y llamadas a funciones definidas en otros archivos.

### Interacción con Base de Datos
Ninguna. El archivo no contiene consultas SQL ni interacciones con una base de datos.

### Estado y Variables Globales
- `user`: Objeto que contiene información del usuario actual.
- `error_msg`: Mensaje de error a mostrar en la interfaz.
- `alerts`: Lista de alertas de desplanificación.
- `scatter_data`: Datos para el gráfico de dispersión.
- `combos`: Datos para el análisis de market basket.

### Dependencias y Flujo
- **Dependencias**: 
  - Chart.js: Para renderizar gráficos.
  
- **Archivos Importados**:
  - `_styles.html`: Archivo que contiene estilos CSS.
  - `analytics_proyecciones.css`: Hoja de estilo específica para esta página.
  - `_scripts.html`: Archivo que contiene scripts JavaScript generales.
  - `analytics_proyecciones.js`: Script específico para esta página.

- **Archivos Exporados**:
  - No se exportan funciones o clases desde este archivo HTML. Todas las interacciones son a través de eventos y llamadas a funciones en otros archivos JavaScript.

El flujo de datos es principalmente hacia la interfaz del usuario, donde los datos JSON (`data_scatter`, `data_alerts`, `data_combos`) son utilizados para alimentar gráficos y tablas.


---

## Archivo: ./templates/dashboard.html

### Resumen Funcional
El archivo `dashboard.html` es una plantilla HTML para el panel de control del sistema de monitoreo de almacén (WMS). Contiene la interfaz de usuario principal que incluye encabezado, indicadores clave (KPIs), menú lateral y tabla de datos.

### Catálogo de Funciones y Clases
Ninguna.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `INITIAL_USER_GROUPS`: Variable global que almacena los grupos de usuario en formato JSON.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas directamente en este archivo.
- **Archivos del Proyecto Importados**:
  - `partials/_styles.html`
  - `partials/_modals.html`
  - `partials/_sidebar.html`
  - `partials/_table.html`
  - `partials/_scripts.html`
- **Archivos que Importan a Este Archivo**: Ninguno.

El flujo de datos se realiza a través de la inclusión de parciales HTML, lo que permite modularizar el código y mantener una estructura organizada.


---

## Archivo: ./templates/deliveries.html (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para la interfaz de usuario del sistema de monitoreo de almacén (WMS). Proporciona una vista consolidada con varias secciones, como entregas, movimientos, consumos y más. Incluye funcionalidades para filtrar y ordenar datos, así como modales para detalles adicionales.

### Catálogo de Funciones y Clases
- `switchTab(tabId, btnElement)` - Cambia la pestaña activa.
- `switchSubTab(subTabId, btnElement)` - Cambia la subpestaña activa.
- `openNonPalletizedDetails(user, claseMov)` - Abre un modal con detalles no paletizados.
- `initTableFilters()` - Inicializa los filtros de tablas.
- `filterOTTable()` - Filtra la tabla de OTs según criterios seleccionados.
- `filterDiscrepancyTable()` - Filtra la tabla de discrepancias según criterios seleccionados.
- `sortTableDiscrepancy(columnIndex)` - Ordena la tabla de discrepancias.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- Variables globales no detectadas directamente en el código proporcionado.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `Chart.js`
  - `chartjs-plugin-datalabels`
  - `marked`
  - `font-awesome`

- **Archivos del Proyecto Importados**:
  - `partials/_styles.html`
  - `css/deliveries.css`, `css/inventory.css`, `css/analytics_proyecciones.css`
  - `js/bundle.js`
  - `partials/_modals.html`, `_deliveries_modals.html`, `_inventory_modals.html`, `_analytics_proyecciones_modals.html`, `_edit_query_modal.html`, `_quick_login_modal.html`, `_logout.html`

- **Archivos del Proyecto que Importan a Este Archivo**:
  - No detectados directamente en el código proporcionado.

El flujo de datos se realiza principalmente mediante JavaScript para interactuar con la interfaz y cargar datos dinámicamente.


---

## Archivo: ./templates/inventory.html

### Resumen Funcional
El archivo `inventory.html` es una plantilla HTML para la página de análisis del inventario en el sistema de monitoreo de almacén (WMS). Muestra gráficos y KPIs relacionados con las entradas, consumos, traspasos y otras métricas del inventario.

### Catálogo de Funciones y Clases
Ninguna.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `Chart.js`
  - `chartjs-plugin-datalabels`

- **Archivos del Proyecto Importados**:
  - `partials/_styles.html`
  - `css/inventory.css`
  - `partials/_inventory_modals.html`
  - `js/core_ui.js`
  - `js/saas_engine_core.js`
  - `js/saas_engine_drilldown.js`
  - `js/inventory.js`
  - `partials/_quick_login_modal.html`
  - `partials/_logout.html`

- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno.

El flujo de datos se realiza principalmente a través de la carga de scripts y estilos, así como el consumo de variables globales y funciones JavaScript definidas en los archivos importados.


---

## Archivo: ./templates/login.html

### Resumen Funcional
El archivo `login.html` es una página de inicio de sesión para el sistema de monitoreo de almacén (WMS). Permite a los usuarios ingresar sus credenciales y autenticarse en la aplicación.

### Catálogo de Funciones y Clases
- **handleLogin(event)** - Maneja el evento de envío del formulario de inicio de sesión, realiza una solicitud POST a la API para autenticar al usuario y maneja la respuesta.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- **localStorage** - Se utilizan variables globales en el almacenamiento local del navegador para guardar el token de acceso, nombre de usuario y rol del usuario autenticado.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas mencionadas.
- **Flujo**: El archivo `login.html` se importa por la vista correspondiente en FastAPI. La función `handleLogin` es llamada cuando el formulario de inicio de sesión se envía, lo que desencadena una solicitud POST a `/api/auth/login`. La respuesta del servidor maneja la autenticación y redirige al usuario según sea necesario.


---

## Archivo: ./templates/partials/_analytics_proyecciones_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para tres modales en una interfaz de usuario, cada uno con filtros y tablas para mostrar diferentes tipos de alertas y correlaciones de materiales. Los modales son utilizados para visualizar datos relacionados con desplanificación, correlaciones de materiales (basket) y listado frecuencia vs volumen.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna


---

## Archivo: ./templates/partials/_deliveries_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML que definen varios modales para una interfaz de usuario en un sistema de monitoreo de almacén (WMS). Cada modal muestra diferentes tipos de información, como el consumo específico, actividad del solicitador, desglose de ubicación, movimientos no paletizados y reportes mensuales de productividad.

### Catálogo de Funciones y Clases
No se detectaron funciones o clases definidas en este fragmento HTML. Todas las interacciones son realizadas a través de JavaScript y eventos del DOM.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: No se detectaron dependencias externas directamente en este fragmento.
- **Flujo**: Este archivo no importa ni es importado por otros archivos. Las interacciones con JavaScript son locales al contexto del HTML donde se incluyen estos modales.


---

## Archivo: ./templates/partials/_edit_query_modal.html

### Resumen Funcional
Este archivo contiene el código HTML para un modal de edición de consultas en el sistema de monitoreo de almacén (WMS). El modal incluye un constructor visual interactivo que permite configurar gráficos y KPIs, así como una vista previa del resultado.

### Catálogo de Funciones y Clases
No se detectaron funciones o clases específicas en este fragmento HTML. Todo el contenido es estructura HTML y CSS.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `editQueryId`: Un input oculto que almacena el ID de la consulta actualmente editada.

### Dependencias y Flujo
- **Dependencias**: No se importan bibliotecas externas ni archivos del proyecto en este fragmento.
- **Flujo**: Este archivo es consumido por otros archivos HTML o JavaScript para renderizar el modal de edición de consultas.


---

## Archivo: ./templates/partials/_inventory_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para varios modales en una interfaz de usuario de sistema de monitoreo de almacén (WMS). Cada modal muestra diferentes tipos de información, como consumo específico, actividad del asistente, materiales más movimientos, desglose de ubicación, curva ABC, materiales frecuentes y detalles de producción vs mantenimiento.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada directamente en este fragmento HTML. Todas las interacciones son realizadas a través del DOM y JavaScript.

### Interacción con Base de Datos
Ninguna interacción con la base de datos detectada en este archivo. Todas las listas y detalles se muestran dinámicamente mediante JavaScript.

### Estado y Variables Globales
Ninguna variable global, de sesión o de entorno detectada directamente en este fragmento HTML. Todas las variables y estados son gestionados por el JavaScript que interactúa con el DOM.

### Dependencias y Flujo
- **Librerías externas**: Ninguna librería externa importada.
- **Archivos del proyecto que IMPORTA a este archivo**: Ninguno.
- **Archivos del proyecto que este archivo IMPORTA (lo consume)**: Ninguno.
- **Flujo de datos**: El flujo de datos se gestiona completamente por JavaScript, que interactúa con el DOM para mostrar y ocultar modales y cargar contenido dinámicamente.


---

## Archivo: ./templates/partials/_logout.html

### Resumen Funcional
El archivo `_logout.html` contiene un fragmento de código JavaScript que se ejecuta cuando el usuario intenta cerrar sesión. Realiza una solicitud asíncrona al backend para notificar la salida del usuario y luego limpia los datos almacenados localmente, finalmente recarga la página para reflejar el cambio.

### Catálogo de Funciones y Clases
- `logout()` - Llama a la API para cerrar sesión y limpia los datos locales antes de recargar la página.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- No hay variables globales explícitas mencionadas en el código.

### Dependencias y Flujo
- **Dependencias**: Ninguna.
- **Flujo**: 
  - Este fragmento se ejecuta cuando el usuario intenta cerrar sesión.
  - Llama a la API `/api/auth/logout` para notificar al backend.
  - Limpia los datos de almacenamiento local (`localStorage.removeItem`) y luego recarga la página con `window.location.reload()`.

Este fragmento es parte del proceso de cierre de sesión en el sistema WMS, asegurando que tanto el backend como el frontend estén actualizados y seguros al cerrar una sesión.


---

## Archivo: ./templates/partials/_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para modales que se utilizan en el sistema de monitoreo de almacén (WMS). Los modales incluyen un visor de PDF, una tabla de mapeo de autores y áreas, y un modal de análisis detallado.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: Ninguna
- **Archivos Importados por Este Archivo**: Ninguno
- **Archivos que Importan a Este Archivo**: Ninguno


---

## Archivo: ./templates/partials/_quick_login_modal.html

### Resumen Funcional
El archivo `_quick_login_modal.html` es un fragmento de HTML que define una ventana modal para iniciar sesión rápidamente en el sistema de monitoreo de almacén (WMS). La ventana incluye campos para usuario y contraseña, y un botón para enviar los datos. Al enviar el formulario, se realiza una solicitud POST a la API de autenticación del sistema.

### Catálogo de Funciones y Clases
- `handleQuickLogin(event)` - Maneja el envío del formulario de inicio de sesión, realiza la autenticación y actualiza el estado del usuario en el almacenamiento local o recarga la página según sea necesario.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- `localStorage` - Se utilizan para almacenar el token de acceso, nombre de usuario y rol del usuario autenticado.
- `window.handleQuickLogin` - Variable global que expone la función `handleQuickLogin` al ámbito global.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directamente mencionadas en el código.
- **Flujo de Datos**:
  - El archivo se importa en otros archivos del proyecto (no especificados aquí).
  - Otros archivos pueden llamar a la función `handleQuickLogin` para iniciar sesión rápidamente.

El flujo de datos es unidireccional desde el HTML hasta el JavaScript, donde se maneja la autenticación y la actualización del estado del usuario.


---

## Archivo: ./templates/partials/_scripts.html

### Resumen Funcional
Este archivo contiene fragmentos de HTML que incluyen scripts para Chart.js, modales de inicio rápido y cierre, lógica del negocio y UI helpers para el panel de control, así como scripts específicos para la productividad diaria y mensual.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías externas**: Chart.js, chartjs-plugin-datalabels.
- **Archivos del proyecto que IMPORTA (consume)**: Ninguno.
- **Archivos del proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno.

El flujo de datos es unidireccional desde el HTML hacia los scripts externos y locales.


---

## Archivo: ./templates/partials/_sidebar.html

### Resumen Funcional
El archivo `_sidebar.html` es un fragmento de interfaz de usuario que contiene filtros y controles para interactuar con el sistema de monitoreo de almacén (WMS). Permite seleccionar fechas, áreas, centros, estados OT, realizar búsquedas y generar reportes PDF.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `dates`: Lista de fechas disponibles para filtrar.
- `default_dates`: Lista de fechas seleccionadas por defecto.
- `areas`: Lista de áreas disponibles para filtrar.
- `area_centro_map`: Diccionario que mapea áreas a centros.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directamente mencionadas en el código.
- **Flujo de Datos**:
  - El archivo se importa por otros archivos HTML para renderizar la interfaz del sidebar.
  - Los eventos de los controles (checkboxes, radios, input) invocan funciones JavaScript (`toggleSidebar`, `toggleMulti`, `handleSmartCheckbox`, `applyCentroFilter`, `applyFilters`, `downloadBulk`) que pueden interactuar con el backend a través de llamadas AJAX o directamente manipular el DOM.

Este fragmento es una parte integral del frontend, proporcionando la interfaz para los usuarios interactivos y controladores para manejar las acciones del usuario.


---

## Archivo: ./templates/partials/_styles.html

### Resumen Funcional
Este archivo contiene estilos CSS para el sistema de monitoreo de almacén (WMS). Define la apariencia visual del sitio web, incluyendo colores, fuentes, diseños de componentes y animaciones.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna


---

## Archivo: ./templates/partials/_tab_consumos.html

### Resumen Funcional
Este fragmento HTML corresponde a una pestaña dentro de un sistema de monitoreo de almacén (WMS) que permite analizar los consumos y costos de materiales. Permite buscar por Centro de Costo o por materiales específicos, mostrando históricos mensuales y anuales.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla `movimientos` (Mov. 201): 
    - `id`
    - `material_id`
    - `centro_costo_id`
    - `cantidad`
    - `precio_unitario`
    - `fecha`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Dependencias Externas:** Ninguna
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:** Ninguno
- **Flujo de Datos:** El archivo se utiliza para renderizar la interfaz de usuario y no interactúa directamente con el backend o base de datos.


---

## Archivo: ./templates/partials/_tab_deliveries.html

### Resumen Funcional
Este fragmento HTML es una pestaña dentro de un sistema de monitoreo de almacén (WMS) que muestra análisis y gráficos relacionados con las entregas. Permite seleccionar entre vistas anuales y semanales, mostrar estadísticas clave como volumen total de entregas y eficiencia de bodega, y filtrar los datos por áreas.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML. Todo el contenido es estructurado en elementos HTML y JavaScript.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `user.role`: Almacena el rol del usuario actual, utilizado para determinar si se muestran botones de edición de consultas SQL.
- `areas_vl`: Lista de áreas que pueden ser seleccionadas para filtrar los datos.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias directas en este fragmento HTML. Se utilizan elementos de JavaScript y CSS, pero no se importa ninguna biblioteca externa.
- **Flujo**: Este fragmento es consumido por la vista principal del sistema WMS. No importa a otros archivos ni es importado por otros archivos dentro del proyecto.


---

## Archivo: ./templates/partials/_tab_docs.html

### Resumen Funcional
Este archivo es un fragmento HTML que define una pestaña de interfaz de usuario en el sistema de monitoreo de almacén (WMS). Muestra un explorador de documentación con opciones para ver la estructura del proyecto y un mapa global generado por Graphify.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `fas fa-sitemap`, `fas fa-project-diagram`
- **Archivos del Proyecto que IMPORTA a este archivo (lo consumen)**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA (consume)**: Ninguno

**Flujo de Datos**: El fragmento HTML no consume ni produce datos. Es una vista estática que interactúa con el backend a través de eventos JavaScript para cargar contenido dinámicamente.


---

## Archivo: ./templates/partials/_tab_historial.html

### Resumen Funcional
Este fragmento HTML es una pestaña que muestra el historial de ubicaciones de un material en un sistema de monitoreo de almacén (WMS). Permite a los usuarios buscar un material y ver su stock actual y su historial de ubicaciones anteriores.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** Ninguna
- **Columnas:** Ninguna
- **Consultas SQL Crudas o Llamadas a ORM:** Ninguna

### Estado y Variables Globales
- `user.role`: Rol del usuario actual.

### Dependencias y Flujo
- **Librerías Externas:** Ninguna
- **Archivos Importados por este Archivo:** Ninguna
- **Archivos que Importan a este Archivo:** Ninguna

El flujo de datos es unidireccional, con el usuario interactuando con la interfaz y no habiendo intercambio de datos entre diferentes partes del sistema.


---

## Archivo: ./templates/partials/_tab_ia.html

### Resumen Funcional
Este fragmento HTML es una pestaña de la interfaz de usuario que muestra información sobre el análisis predictivo y los comportamientos de materiales en un sistema de monitoreo de almacén (WMS). Muestra semáforos de desplanificación, gráficos de frecuencia vs volumen y combos frecuentes.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **TABLAS:** Ninguna (El fragmento HTML no contiene consultas SQL ni llamadas a ORM directamente).
- **COLUMNAS:** Ninguna (No se accede a ninguna columna específica de la base de datos).

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas:** Ninguna
- **Archivos del Proyecto que IMPORTA:** Ninguno
- **Archivos del Proyecto que IMPORTAN a Este Archivo:** Ninguno
- **Flujo de Datos:** El fragmento HTML se renderiza en el cliente y no interactúa directamente con la base de datos o dependencias externas.


---

## Archivo: ./templates/partials/_tab_inventory.html

### Resumen Funcional
Este fragmento HTML es una pestaña de análisis de movimientos en el sistema de monitoreo de almacén (WMS). Muestra estadísticas clave como ingresos, consumos y traspasos, junto con gráficos que representan la eficiencia operativa y tendencias de consumo.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - No se especifican consultas SQL o llamadas a ORM en este fragmento HTML. Todas las estadísticas y datos son presentados directamente desde el contexto del backend.

### Estado y Variables Globales
- `user.role`: Rol del usuario actual.
- `ingresos_eff_stats`, `ingresos_eff_stats_weekly`: Datos de eficiencia operativa para ingresos (mensuales y semanales).
- `consumos_eff_stats`, `consumos_eff_stats_weekly`: Datos de eficiencia operativa para consumos (mensuales y semanales).
- `kpi_devoluciones`: Tasa de devoluciones.

### Dependencias y Flujo
- **Dependencias Externas:** Font Awesome (`fas fa-layer-group`, `fas fa-cog`, etc.)
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:** Ninguno

El flujo de datos es unidireccional, con el backend proporcionando los datos necesarios para renderizar la vista en el frontend.


---

## Archivo: ./templates/partials/_tab_ots.html (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
Este fragmento HTML corresponde a una pestaña dentro de un sistema de monitoreo de almacén (WMS) que muestra estadísticas y tablas interactivas relacionadas con las Ordenes de Transporte (OTs). Incluye gráficos, contadores y listados filtrables para visualizar el estado de las OTs pendientes, movimientos no paletizados y análisis de productividad.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML. Todo es contenido estático y dinámico generado por JavaScript.

### Interacción con Base de Datos
- **Motor**: SQLite
- **TABLAS**:
  - `inventory_movements` (Mencionada en la alerta operativa)
- **COLUMNAS**:
  - No se especifican columnas explícitas, pero el fragmento hace referencia a campos como `doc_mat`, `creator`, `clase_mov`, etc.

### Estado y Variables Globales
No se detectan variables globales o de sesión definidas en este fragmento HTML. Todo es contenido dinámico generado por JavaScript.

### Dependencias y Flujo
- **Librerías Externas**: No se mencionan librerías externas específicas.
- **Archivos del Proyecto que IMPORTA a este archivo**: Ninguno.
- **Archivos del Proyecto que ESTE archivo IMPORTA (consume)**: Ninguno.

El flujo de datos es principalmente entre el cliente y el servidor, con la generación dinámica de contenido HTML y JavaScript basado en los datos recuperados desde la base de datos.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
Este archivo contiene el código HTML para una interfaz de usuario que muestra detalles diarios y mensuales de movimientos en un sistema de almacén (WMS). Incluye tablas interactivas para visualizar los datos y botones para navegar entre diferentes niveles de detalle.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: No se mencionan dependencias específicas en el código proporcionado.
- **Flujo**: El archivo no importa ni es importado por otros archivos. Es un fragmento de HTML que se utiliza para renderizar la interfaz de usuario en una página web.

Este archivo solo contiene estructura HTML y CSS, sin interacción con base de datos o lógica de negocio.


---

## Archivo: ./templates/partials/_tab_replenishment.html

### Resumen Funcional
Este fragmento HTML es una interfaz de usuario para mostrar sugerencias de pedido en un sistema de monitoreo de almacén (WMS). Muestra una tabla con detalles sobre el material, su descripción, UMB, stock inicial y actual, consumo mensual, frecuencia de retiros, autonomía en meses y clasificación ABC. Incluye filtros para la frecuencia de pedido y un botón para exportar los datos a Excel.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** Ninguna (El fragmento HTML no interactúa directamente con una base de datos. Los datos se cargan desde un endpoint API).
- **Columnas:** Ninguna (No hay consultas SQL o ORM explícitas en el fragmento HTML).

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `fas fa-exclamation-triangle`, `fas fa-file-excel`
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno (Este archivo no importa otros archivos).
- **Archivos del Proyecto que Este Archivo Importa:** Ninguno (No hay imports en el fragmento HTML).

**Flujo de Datos:**
El fragmento HTML se carga en la interfaz del usuario. Los datos para llenar la tabla se obtienen a través de una solicitud GET al endpoint `/api/inventory/replenishment-suggestions/export`.


---

## Archivo: ./templates/partials/_tab_transporte.html

### Resumen Funcional
Este fragmento HTML es una sección de la interfaz de usuario para el sistema de monitoreo de almacén (WMS), que muestra gráficos y tablas relacionados con las entregas. Incluye un filtro por tiempo, un gráfico de líneas, alertas de OTs pendientes de ingreso en SAP, un buscador rápido de entregas y una tabla con los últimos 25 registros y reportes PDF.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:**
  - `transporte` (Tabla que almacena información sobre las entregas)
- **Columnas:**
  - `id`
  - `fecha`
  - `ot`
  - `gd`
  - `oc`
  - `bultos`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** Ninguna
- **Archivos del Proyecto que Importan a este Archivo:**
  - `routes.py` (Consumen el fragmento para mostrarlo en la interfaz de usuario)
- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno

El flujo de datos es unidireccional, con el archivo HTML consumido por otros componentes del sistema para renderizar la interfaz de usuario.


---

## Archivo: ./templates/partials/_table.html

### Resumen Funcional
Este fragmento HTML es una tabla que muestra transacciones en un sistema de monitoreo de almacén (WMS). La tabla incluye columnas para la entrega/OT, fecha, items, área y estado. Ofrece funcionalidades como ordenar las columnas, buscar registros y generar PDFs.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directamente mencionadas en este fragmento.
- **Flujo**: Este archivo es un fragmento HTML que se renderiza en una página web. No realiza ninguna operación de base de datos ni interactúa con variables globales. Se consume por vistas o componentes que lo incluyen en su plantilla.

Este fragmento es parte de la interfaz de usuario y no contiene lógica de negocio o acceso a bases de datos.


---

## Archivo: ./templates/settings.html (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `settings.html` es una interfaz de usuario para la configuración dinámica del sistema WMS. Permite gestionar parámetros globales, mapeos de estados de entrega y centros de costo a áreas de negocio, así como grupos de usuarios y feriados.

### Catálogo de Funciones y Clases
- `openPasswordModal()` - Abre el modal para cambiar la contraseña.
- `closePasswordModal()` - Cierra el modal para cambiar la contraseña.
- `changePassword()` - Maneja el cambio de contraseña a través de una API.
- `updateSetting(key)` - Actualiza un parámetro global.
- `updateStatus(code)` - Actualiza un mapeo de estado de entrega.
- `addStatus()` - Añade un nuevo mapeo de estado de entrega.
- `deleteStatus(code)` - Elimina un mapeo de estado de entrega.
- `updateCostCenter(code)` - Actualiza un mapeo de centro de costo a área de negocio.
- `addCostCenter()` - Añade un nuevo mapeo de centro de costo a área de negocio.
- `deleteCostCenter(code)` - Elimina un mapeo de centro de costo a área de negocio.
- `syncHolidays()` - Sincroniza los feriados nacionales de Chile.
- `addHoliday()` - Añade un nuevo feriado manual.
- `deleteHoliday(date_str)` - Elimina un feriado manual.
- `updateUserGroup(oldName, nameId, listId)` - Actualiza el nombre y usuarios de un grupo de usuarios.
- `addUserGroup()` - Añade un nuevo grupo de usuarios.
- `deleteUserGroup(name)` - Elimina un grupo de usuarios.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos. Todas las operaciones CRUD se realizan a través de llamadas a APIs.

### Estado y Variables Globales
No hay variables globales explícitas definidas en el código. Las variables utilizadas son principalmente para almacenar valores temporales como los valores de entrada del usuario o mensajes de toast.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas específicas.
- **Flujo de Datos**:
  - El archivo `settings.html` es consumido por el navegador del cliente.
  - Los scripts JavaScript realizan llamadas a APIs para interactuar con el backend (FastAPI).
  - Las respuestas de las API son utilizadas para actualizar la interfaz de usuario dinámicamente.

El flujo de datos va desde el frontend hacia el backend, donde se realizan operaciones CRUD y luego se reflejan los cambios en la interfaz de usuario.


---

## Archivo: ./templates/sla_table.html

### Resumen Funcional
El archivo `sla_table.html` es una plantilla HTML para mostrar una tabla de transacciones que cumplen con ciertos criterios en un sistema de monitoreo de almacén (WMS). La tabla incluye detalles como el número de entrega, autor/creador, área de negocio, días de retraso, fecha de creación y salida, y material involucrado. Además, proporciona opciones para generar y descargar PDFs relacionados con cada transacción.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías externas**: No se mencionan librerías externas específicas.
- **Archivos del proyecto que IMPORTA (consume)**: `partials/_styles.html`, `sla_table.css`, `_modals.html`, `sla_table.js`.
- **Archivos del proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno
- **Dirección del flujo de datos**: El archivo se renderiza en el navegador y no interactúa directamente con la base de datos o servicios externos.


---

## Archivo: ./tests/conftest.py

### Resumen Funcional
Este archivo `conftest.py` es un archivo de configuración para pruebas unitarias en un proyecto de Sistema de Monitoreo de Almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Define varias funciones de prueba que configuran la base de datos de pruebas, proporcionan clientes de prueba autenticados y aseguran el aislamiento entre las pruebas individuales.

### Catálogo de Funciones y Clases
- `skip_warmup()` - Desactiva un parche que fallaba durante el arranque.
- `session_db()` - Crea e inicializa la base de datos maestra compartida para toda la sesión de pruebas, incluyendo la creación de tablas y el esquema.
- `test_db(session_db)` - Proporciona aislamiento de datos entre pruebas individuales, vaciando las tablas antes de cada prueba.
- `client(test_db)` - Cliente de pruebas de FastAPI configurado para interactuar con la BD de sesión.
- `auth_client(client)` - Proporciona un cliente con token de administrador pre-autenticado.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `outbound_deliveries`
  - `inventory_movements`
  - `stock_levels`
  - `warehouse_tasks`
  - `autor_area_mapping`
  - `analytics_snapshots`
  - `auth_users`
- **Columnas**: Cada tabla tiene varias columnas, pero no se detalla cada una aquí.

### Estado y Variables Globales
- `TEST_SESSION_ID`: Identificador criptográficamente seguro para evitar colisiones.
- `MEMORY_DB_URI`: URI de la base de datos SQLite en memoria compartida.
- `os.environ["DATABASE_URL"]`: URL de la base de datos configurada para pruebas.
- `os.environ["TESTING"]`: Variable de entorno indicando que se está ejecutando un entorno de prueba.

### Dependencias y Flujo
- **Librerías Externas**: `secrets`, `sys`, `pathlib`, `sqlite3`, `unittest.mock`, `pytest`, `fastapi.testclient`.
- **Archivos del Proyecto Importados**:
  - `config`
  - `app`
  - `core.auth.init_auth_db`
  - `core.db_config_manager.init_config_db`
  - `core.db_config_manager.seed_initial_config`
- **Archivos que Importan a Este Archivo**: Ninguno.
- **Flujo de Datos**:
  - El archivo configura la base de datos de pruebas en memoria y proporciona clientes de prueba para interactuar con ella.
  - Las pruebas individuales utilizan el cliente autenticado para realizar operaciones en el sistema.


---

## Archivo: ./tests/test_api.py

### Resumen Funcional
El archivo `test_api.py` contiene pruebas unitarias para endpoints de una API de un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Las pruebas cubren la funcionalidad del dashboard principal, el acceso a la página de analíticas, la generación de consultas SQL, y la protección contra inyección SQL.

### Catálogo de Funciones y Clases
- `test_read_root(auth_client)` - Verifica que el dashboard principal responda con el título correcto.
- `test_get_tunnel_url(auth_client, tmp_path)` - Verifica que el endpoint `/url` devuelva la dirección del túnel ngrok.
- `test_post_sync_endpoint(auth_client)` - Verifica que el endpoint de sincronización inicie el pipeline correctamente.
- `test_analytics_page_access(auth_client)` - Verifica que la página de analíticas sea accesible.
- `test_build_sql_sla_efficiency(auth_client)` - Verifica que el generador de consultas SQL compile correctamente la métrica SLA_EFFICIENCY con desgloses y filtros.
- `test_analytics_sla_route(auth_client, test_db)` - Verifica que la ruta de auditoría SLA resuelva dinámicamente las áreas de negocio y que no muestre 'OTRO'.
- `test_api_query_preview_returns_json_and_no_sql(auth_client)` - Verifica el contrato JSON in/out para preview y la ausencia de texto SQL.
- `test_api_settings_query_rejects_raw_sql(auth_client)` - Verifica protección contra inyección y que el endpoint solo acepte visual_state.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `outbound_deliveries`
- Columnas:
  - `entrega`, `fecha_carga`, `centro_costo`, `area_negocio`, `dias_retraso`, `week_sort`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- Librerías externas: `pytest`, `unittest.mock`
- Archivos del proyecto que este archivo importa:
  - `core.state.SyncStateManager`
  - `routes.sync.TUNNEL_URL_FILE`
  - `routes.sync._run_sync_pipeline`
  - `routes.sync.task_manager`
- Archivos del proyecto que importan a este archivo: Ninguno.
- Flujo de datos: El archivo consume pruebas unitarias y verifica la funcionalidad de endpoints, interactuando con una base de datos SQLite para obtener y modificar datos.


---

## Archivo: ./tests/test_auth.py

### Resumen Funcional
Este archivo contiene pruebas unitarias para el módulo de autenticación JWT en un sistema de monitoreo de almacén (WMS). Las pruebas cubren la funcionalidad de inicio de sesión, registro de usuarios y gestión de perfiles de usuario.

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
Ninguna. Las pruebas se realizan utilizando un cliente de prueba (`TestClient`) proporcionado por FastAPI, sin acceso directo a una base de datos.

### Estado y Variables Globales
Ninguna. Todas las variables utilizadas son locales dentro de las funciones de prueba.

### Dependencias y Flujo
- **Dependencias**: `pytest`, `fastapi.testclient.TestClient`.
- **Flujo de Datos**:
  - El archivo importa `pytest` y `TestClient` desde `fastapi.testclient`.
  - No hay archivos del proyecto que importen a este archivo.
  - Las pruebas realizan solicitudes HTTP al servidor FastAPI utilizando el cliente de prueba, lo que implica un flujo de datos entre el cliente y el servidor.


---

## Archivo: ./tests/test_enrichment.py

### Resumen Funcional
El archivo `test_enrichment.py` contiene pruebas unitarias para funciones que enriquecen datos en una base de datos SQLite utilizada por un sistema de monitoreo de almacén (WMS). Las funciones se encargan de aprender mapeos de autor a áreas, rellenar información de entregas desde movimientos, enriquecer entregas con detalles de stock y actualizar el SLA basado en tareas de bodega.

### Catálogo de Funciones y Clases
- `db_with_data(test_db: sqlite3.Connection) -> sqlite3.Connection` - Prepara una base de datos SQLite con datos de prueba para los procesos de enriquecimiento.
- `test_learn_and_apply_author_logic(db_with_data: sqlite3.Connection) -> None` - Verifica que el sistema aprenda que USER_A pertenece a PRODUCCION y lo aplique.
- `test_backfill_from_movements(db_with_data: sqlite3.Connection) -> None` - Verifica que Entregas recupere el autor y centro de costo desde Movimientos.
- `test_enrichment_from_stock(db_with_data: sqlite3.Connection) -> None` - Verifica que se crucen las descripciones de material y ubicaciones desde el maestro de stock.
- `test_update_sla_with_tasks(db_with_data: sqlite3.Connection) -> None` - Verifica que el SLA se actualice correctamente usando las tareas de bodega.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas Modificadas/Leídas:**
  - `outbound_deliveries`: Campos modificados (`area_negocio`, `autor`, `centro_costo`, `material`, `dias_retraso`).
  - `inventory_movements`: Campos leídos (`usuario`, `ce_coste`, `referencia`).
  - `stock_levels`: Campos leídos (`material`, `denominacion`, `ubicacion_bin`, `stock_disp`, `umb`).

### Estado y Variables Globales
- Ninguna.

### Dependencias y Flujo
- **Librerías Externas:** `pytest`, `sqlite3`.
- **Archivos del Proyecto Importados:**
  - `db.db_enrichment`: Contiene las funciones que se prueban (`apply_author_learning`, `backfill_deliveries_from_movements`, `enrich_deliveries_with_stock`, `learn_author_areas`, `update_sla_with_tasks`).
- **Archivos del Proyecto Importados por:** Ninguno.
- **Dirección del Flujo de Datos:**
  - El archivo importa funciones desde `db.db_enrichment`.
  - Las pruebas crean y manipulan datos en una base de datos SQLite para verificar el comportamiento de las funciones.


---

## Archivo: ./tests/test_maintenance.py

### Resumen Funcional
El archivo `test_maintenance.py` contiene pruebas unitarias para funciones relacionadas con el mantenimiento del sistema, específicamente para cerrar aplicaciones y filtrar archivos en un generador de documentación.

### Catálogo de Funciones y Clases
- `test_quit_app_success()` - Verifica que la función `quit_app` retorne True cuando el comando de sistema tiene éxito.
- `test_quit_app_failure()` - Verifica que la función `quit_app` retorne False cuando ocurre un error de proceso o excepción.
- `test_doc_generator_filtering_logic(filename: str, filepath: str, expected: bool)` - Prueba la lógica de exclusión de archivos en el generador de documentación.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `subprocess`, `unittest.mock`
- **Archivos del Proyecto que IMPORTA a este archivo (lo consumen)**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA (consume)**: `scripts.doc_generator`, `scripts.free_ram`

**Flujo de Datos**:
1. El archivo importa las funciones `quit_app` y `should_process` desde otros módulos.
2. Se ejecutan pruebas unitarias para verificar el comportamiento de estas funciones.
3. Las pruebas utilizan mocks para simular llamadas a `subprocess.run` y validar los resultados.

**Nota**: La función `quit_app` utiliza `subprocess.run` para cerrar aplicaciones, lo que implica una interacción con el sistema operativo.


---

## Archivo: ./tests/test_pdf.py

### Resumen Funcional
Este archivo `test_pdf.py` contiene pruebas unitarias para validar la funcionalidad del módulo `pdf_engine`, que se encarga de generar documentos PDF en formato Landscape utilizando la orientación de papel Letter. Las pruebas cubren la creación de instancias de PDF, generación de códigos de barras, recuperación lógica de órdenes de transporte (OTs) y el dibujo de páginas de entrega.

### Catálogo de Funciones y Clases
- `pdf_instance() -> WMS_Landscape_PDF` - Proporciona una instancia limpia de la clase `WMS_Landscape_PDF`.
- `sample_header() -> pd.Series` - Genera datos ficticios para pruebas de renderizado de metadatos.
- `sample_items() -> pd.DataFrame` - Genera un listado de materiales ficticios para validar el cuerpo dinámico del PDF.
- `test_pdf_instantiation(pdf_instance: WMS_Landscape_PDF) -> None` - Verifica que la clase PDF se instancie con la orientación Landscape y dimensiones Letter.
- `test_barcode_generation(barcode_data: str) -> None` - Valida que la utilidad de códigos de barras produzca un stream binario válido.
- `test_get_ots_logic() -> None` - Verifica la lógica de recuperación de OTs filtrando valores inválidos (0 o nulos).
- `test_draw_delivery_page_generates_content(pdf_instance: WMS_Landscape_PDF, sample_header: pd.Series, sample_items: pd.DataFrame) -> None` - Valida que el motor de dibujo escriba contenido binario en el buffer del PDF.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas y Columnas:
  - `numero_ot`: Columna utilizada para recuperar OTs válidas.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `io`
  - `sqlite3`
  - `typing`
  - `unittest.mock`
  - `pandas`
  - `pytest`
- Archivos del proyecto que este archivo importa (consume):
  - `core.pdf_engine` (contiene las clases y funciones a probar)
- Archivos del proyecto que importan a este archivo (lo consumen):
  - Ninguno
- Flujo de datos:
  - El archivo se ejecuta como parte de pruebas unitarias, no tiene un flujo de entrada/salida directo con otros componentes del sistema.


---

## Archivo: ./tests/test_pipeline.py

### Resumen Funcional
El archivo `test_pipeline.py` contiene pruebas unitarias para el módulo de consolidación de datos en un sistema de monitoreo de almacén (WMS). Las pruebas cubren la validación de fechas, la protección contra nombres de tabla no seguros y la lógica de sobrescritura de archivos más recientes.

### Catálogo de Funciones y Clases
- `test_parse_file_date(consolidator)` - Verifica que el parsing de fechas desde nombres de archivo sea correcto.
- `test_validate_table_security(consolidator)` - Valida la protección contra nombres de tabla no permitidos.
- `test_overwrite_with_latest_logic(consolidator, tmp_path)` - Verifica que se tome el archivo más reciente para sobrescribir en la base de datos.

### Interacción con Base de Datos
- Motor: SQLite (indicado por la cadena de conexión `":memory:"`)
- Tablas:
  - `TABLE_DELIVERIES`
  - `TABLE_STOCK`
- Columnas: No se especifican explícitamente, pero se asume que las columnas coinciden con el esquema de las tablas en la base de datos.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `pandas`
  - `pytest`
- Archivos del proyecto que importa:
  - `core.security.validate_table`
  - `db.consolidator.DataConsolidator`
  - `db.consolidator.StockLevelAdapter.read_and_clean_data`
- Archivos del proyecto que son importados por este archivo:
  - Ninguno
- Flujo de datos: El archivo no realiza operaciones directas sobre archivos o bases de datos, sino que interactúa con objetos inyectados y mockeados para probar la lógica de negocio.


---

## Archivo: ./tests/test_services.py

### Resumen Funcional
El archivo `test_services.py` contiene pruebas unitarias para funciones y clases relacionadas con la gestión del estado de caché y el manejo de túneles en un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite.

### Catálogo de Funciones y Clases
- `cache_manager()` - Proporciona una instancia limpia de CacheManager configurada para pruebas.
- `sync_manager()` - Proporciona una instancia limpia de SyncStateManager.
- `cleanup_tunnel()` - Garantiza la limpieza del estado global del túnel tras cada test.
- `test_state_cache_respects_limits(cache_manager: CacheManager)` - Verifica que el gestor de estado respete los límites de memoria.
- `test_state_sync_flag_reactivity(sync_manager: SyncStateManager)` - Valida que la propiedad reactiva de sincronización cambie su estado de forma consistente.
- `test_start_tunnel_manages_singleton_instance(mock_access, mock_exists, mock_popen)` - Verifica que start_tunnel inicialice correctamente el servicio de túnel.
- `test_stop_tunnel_releases_global_reference(mock_run)` - Valida que stop_tunnel limpie las referencias globales de forma segura.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `TEST_MAX_CACHE_SIZE` - Constante que establece el límite de caché para pruebas.
- `cache_manager.max_cache_size` - Variable global que almacena el tamaño máximo de la caché.

### Dependencias y Flujo
- **Librerías Externas**: `unittest.mock`, `pytest`.
- **Archivos del Proyecto Importados**:
  - `core.state.CacheManager`
  - `core.state.SyncStateManager`
  - `services.tunnel.start_tunnel`
  - `services.tunnel.stop_tunnel`
- **Archivos que Importan a Este Archivo**: Ninguno.
- **Dirección del Flujo de Datos**: El flujo de datos se centra en la creación y gestión de instancias de clases, así como en las pruebas unitarias para validar su comportamiento.


---

## Archivo: ./tests/test_ui_smoke.py

### Resumen Funcional
El archivo `test_ui_smoke.py` contiene pruebas unitarias para verificar la funcionalidad y la interfaz de usuario (UI) de un sistema de monitoreo de almacén (WMS). Las pruebas incluyen verificación de la presencia de componentes UI críticos, manejo de errores para rutas inexistentes, y validación de componentes específicos en la página de análisis.

### Catálogo de Funciones y Clases
- `test_ui_smoke_components_presence(auth_client, path: str, markers: List[Tuple[str, str]])` - Prueba que verifica la presencia de componentes UI críticos en diferentes rutas.
- `test_ui_smoke_error_handling(client)` - Prueba que verifica el manejo de errores para rutas inexistentes.
- `test_ui_smoke_analytics_studio_modal_components(auth_client)` - Prueba que verifica la presencia de selectores visuales y asegura que no exista el textarea de SQL crudo.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: `pytest`
- **Archivos del Proyecto Importados**:
  - Ninguno.
- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno.


---

## Archivo: ./tests/test_utils.py

### Resumen Funcional
El archivo `test_utils.py` contiene pruebas unitarias para el módulo `utils` del proyecto WMS, específicamente para verificar que la función `setup_signal_handlers` funcione correctamente y de manera segura.

### Catálogo de Funciones y Clases
- `test_setup_signal_handlers_safety()` - Verifica que el registro de manejadores de señales sea seguro e idempotente.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: `pytest`, `core.utils`
- **Flujo**: El archivo no importa ni es importado por otros archivos dentro del proyecto.


---

