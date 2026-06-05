# Documentación Técnica Global - MonitorWeb
Compilado el: 2026-06-05 03:03:51
Modelo: qwen2.5-coder:7b | Hardware: M1 Pro Optimized

---

## Análisis de Arquitectura Global

### Arquitectura General Detectada

La estructura del proyecto sugiere una arquitectura **Modular**. Esto se debe a la organización de los módulos y carpetas que contienen funcionalidades específicas, como `core`, `repositories`, `tests`, `docs`, entre otras.

### Propósito Probable de las Carpetas Principales

1. **`app.py`**: Este archivo probablemente contiene el punto de entrada principal de la aplicación, donde se inicializa y ejecuta la aplicación.
2. **`config.py`**: Contiene configuraciones globales del proyecto, como variables de entorno, parámetros de conexión a bases de datos, etc.
3. **`core/`**: Esta carpeta contiene el código central de la aplicación, incluyendo componentes como autenticación (`auth.py`), base de datos (`database.py`), modelos (`models.py`), y utilidades generales (`utils.py`). También incluye subcarpetas para diferentes funcionalidades.
4. **`repositories/`**: Contiene clases que interactúan con la base de datos, proporcionando una capa de abstracción entre el modelo de dominio y la persistencia de datos.
5. **`tests/`**: Contiene los archivos de pruebas unitarias y de integración para asegurar que el código funcione correctamente.
6. **`docs/`**: Contiene documentación detallada del proyecto, incluyendo documentación de módulos específicos.
7. **`routes/`**: Define las rutas de la API web, asociando URLs con funciones de controlador.
8. **`services/`**: Contiene servicios que encapsulan lógica de negocio compleja y pueden interactuar con múltiples repositorios o otros servicios.

### Organización Lógica de las Dependencias

1. **Dependencias Internas**:
   - `app.py` depende de `config.py`, `core/`, `repositories/`, `routes/`, y `services/`.
   - `core/` depende de `database.py`, `models.py`, y otras subcarpetas.
   - `repositories/` dependen de `database.py` y modelos específicos.

2. **Dependencias Externas**:
   - El proyecto utiliza bibliotecas externas como `pytest` para pruebas, `Docker` para contenedores, y posiblemente otras dependencias listadas en `requirements.txt`.

3. **Documentación**:
   - La carpeta `docs/` contiene documentación detallada de cada módulo, lo que facilita el mantenimiento y la comprensión del código.

4. **Pruebas**:
   - El proyecto incluye una estructura completa para pruebas unitarias y de integración en la carpeta `tests/`, asegurando que el código funcione como se espera.

En resumen, esta arquitectura modular permite un mantenimiento eficiente del código, facilita la escalabilidad y mejora la comprensión del proyecto.


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

## Archivo: ./core/helpers/dynamic_executor.py

### Resumen Funcional
El archivo `dynamic_executor.py` contiene una función que toma un payload JSON crudo, lo valida y compila en una consulta SQL utilizando el módulo `query_engine`. Luego ejecuta la consulta en una base de datos SQLite y devuelve los resultados como un DataFrame de Pandas.

### Catálogo de Funciones y Clases
- `execute_visual_query(payload_dict: Dict, db: Session) -> pd.DataFrame` - Toma un payload JSON crudo, lo valida y compila usando el query_engine, y devuelve un DataFrame de Pandas directamente.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna (la consulta SQL se genera dinámicamente)
- Consultas SQL Crudas o Llamadas a ORM: Sí, utiliza `pd.read_sql` para ejecutar la consulta generada por `build_sql_from_payload`.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías Externas:
  - `pandas`
  - `logging`
  - `typing`
  - `sqlalchemy.orm.Session`
- Archivos del Proyecto que Importan a este archivo (lo consumen):
  - No aplica
- Archivos del Proyecto que Este Archivo Importa (consume):
  - `core.query_engine.build_sql_from_payload`
  - `core.schemas.VisualQueryBuilderPayload`

**Flujo de Datos:**
1. El frontend envía un payload JSON crudo.
2. `execute_visual_query` recibe el payload y lo valida contra el esquema `VisualQueryBuilderPayload`.
3. Utiliza `build_sql_from_payload` para generar una consulta SQL dinámica.
4. Ejecuta la consulta en la base de datos SQLite utilizando `pd.read_sql`.
5. Devuelve los resultados como un DataFrame de Pandas.

Este flujo permite que el sistema genere consultas SQL flexibles basadas en los criterios proporcionados por el usuario, lo que es crucial para un sistema de monitoreo de almacén dinámico y adaptable.


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

## Archivo: ./core/seed_data/widgets.json

### Resumen Funcional
El archivo `widgets.json` contiene una lista de consultas y configuraciones para visualizaciones en un sistema de monitoreo de almacén (WMS). Cada consulta define cómo se deben obtener datos de la base de datos y cómo se deben presentar gráficamente.

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
  - `dias_retraso`
  - `fecha_carga`
  - `tipo_operacion`
  - `area_negocio`
  - `warehouse_tasks.material`
  - `warehouse_tasks.entrega`

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: Ninguna
- **Archivos que importan a este archivo**: Ninguno
- **Archivos que este archivo importa**: Ninguno


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

## Archivo: ./db/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./db/consolidator.py

### Resumen Funcional
El archivo `consolidator.py` es un orquestador de consolidación de datos para un sistema de monitoreo de almacén (WMS) utilizando FastAPI, SQLAlchemy y SQLite. Gestiona la importación y procesamiento de archivos WMS en una base de datos SQLite, aplicando diversas operaciones como UPSERT, actualización de tablas, enriquecimiento de datos y sincronización.

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
- Columnas (no detalladas por brevedad):
  - Todas las columnas relevantes para cada tabla mencionada.
- Consultas SQL crudas o llamadas a ORM: Sí, se utilizan métodos de ORM y consultas SQL dentro de los métodos.

### Estado y Variables Globales
- `logger` - Variable global que almacena el objeto de registro.
- `TABLE_DELIVERIES` - Constante con el nombre de la tabla `outbound_deliveries`.
- `TABLE_STOCK` - Constante con el nombre de la tabla `stock_levels`.

### Dependencias y Flujo
- Librerías externas: `sqlite3`, `logging`, `re`, `pathlib`, `datetime`, `typing`.
- Archivos del proyecto que este archivo importa:
  - `services.etl.OutboundDeliveryAdapter`
  - `services.etl.StockLevelAdapter`
  - `db_enrichment` (varias funciones)
- Archivos del proyecto que importan a este archivo: Ninguno.
- Flujo de datos: El archivo se ejecuta como un script principal (`main`) que toma una carpeta como argumento y procesa los archivos dentro de ella utilizando la clase `DataConsolidator`.


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
  - `logging`
  - `pandas` (pd)
  - `sqlite3`
  - `numpy`
- **Archivos del Proyecto que IMPORTA**:
  - `core.security.validate_table`
  - `core.db_config_manager.get_holidays`
- **Archivos del Proyecto que IMPORTAN a Este Archivo**:
  - Ninguno
- **Dirección del Flujo de Datos**: El flujo de datos pasa por las funciones, realizando consultas SQL para leer y actualizar la base de datos SQLite.


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
  - `sqlite3`
  - `pandas`
  - `numpy`
  - `datetime`
  - `logging`
  - `itertools`
  - `collections`
  - `sys`
  - `os`

- **Archivos del Proyecto que Importan a este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.wms_config.COST_CENTER_MAPPING`

**Flujo de Datos:**
1. El archivo se ejecuta directamente (`if __name__ == "__main__"`).
2. Se importan las dependencias necesarias.
3. La función `generate_predictions` se invoca con la ruta a la base de datos SQLite.
4. Los movimientos de inventario son leídos desde la tabla `inventory_movements`.
5. El procesamiento y análisis de los datos ocurren dentro de la función.
6. Los resultados (combos, scatter data y alertas) se devuelven como un diccionario.

**Dirección del Flujo:**
- **Entrada:** Ruta a la base de datos SQLite.
- **Procesamiento:** Análisis de movimientos de inventario.
- **Salida:** Resultados en formato JSON.


---

## Archivo: ./graphify-out/cache/ast/00452bedb8e75d649f71f64e31759c0daf0372d27f59e7ca1d6b0298623dfa51.json

### Resumen Funcional
El archivo `iw39.py` contiene la implementación del procesador específico para el formato IW39, utilizado en el sistema de monitoreo de almacén (WMS). Este procesador hereda de una clase base y realiza operaciones como validación de archivos, obtención de columnas requeridas y limpieza de datos.

### Catálogo de Funciones y Clases
- **IW39Processor()** - Adaptador específico para procesar el formato IW39 (órdenes PM).
  - `.validate_file(path: Path) -> bool` - Valida si un archivo es válido según las reglas del formato IW39.
  - `._get_required_columns(required_columns: List[str]) -> None` - Obtiene las columnas requeridas para el procesamiento.
  - `._get_primary_keys(primary_keys: List[str]) -> None` - Obtiene las claves primarias necesarias.
  - `._clean_dataframe(dataframe: DataFrame) -> DataFrame` - Limpia y normaliza un DataFrame.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: pandas, pathlib, typing.
- **Archivos Importados por este Archivo**:
  - `users_christianykelly_desktop_monitorweb_services_etl_base_py` (BaseWMSProcessor)
- **Archivos que Importan a este Archivo**: Ninguno

El flujo de datos fluye desde el archivo principal hacia `IW39Processor`, donde se realizan las operaciones de validación, obtención de columnas y limpieza de datos.


---

## Archivo: ./graphify-out/cache/ast/022fcdc989a48317aa114587cfe71d8bc2562272154383999c6d2663a74c6320.json

### Resumen Funcional
El archivo `models.py` contiene definiciones de modelos ORM SQLAlchemy para el esquema de configuración SaaS del sistema de monitoreo de almacén (WMS). Estos modelos incluyen mapeos de códigos internos a etiquetas legibles, asociaciones de centros de costo con áreas de negocio, parámetros de comportamiento del sistema y días no hábiles para el cálculo de SLA.

### Catálogo de Funciones y Clases
- `StatusMapping` - Mapea códigos internos del WMS a etiquetas legibles por humanos.
- `CostCenterMapping` - Asocia un código de centro de costo del WMS con una área de Negocio.
- `AppSetting` - Parámetros de comportamiento del sistema. El campo `type` puede ser float, int, bool o str.
- `Holiday` - Días no hábiles para el cálculo de SLA (días de retraso).
- `ConfigQuery` - Almacena el estado visual (JSON) de las consultas del Analytics Studio.

### Interacción con Base de Datos
El archivo utiliza SQLAlchemy como ORM y SQLite como motor de base de datos. No hay consultas SQL crudas explícitas mencionadas en este fragmento, pero se asume que los modelos interactúan con la base de datos a través de las capas de Repositories y Services.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno quemadas en el código.

### Dependencias y Flujo
- **Dependencias**: 
  - `sqlalchemy`
  - `sqlalchemy_orm`
  - `users_christianykelly_desktop_monitorweb_core_database_py`

- **Flujo de Datos**:
  - El archivo `models.py` importa dependencias necesarias y define clases que representan los modelos ORM.
  - Estas clases son utilizadas por las capas superiores del sistema (Services, Repositories) para interactuar con la base de datos.

Este análisis proporciona una visión detallada de la estructura y funcionalidad del archivo `models.py` en el contexto del proyecto WMS.


---

## Archivo: ./graphify-out/cache/ast/06ebe39d7fb10fcd5acb5d80ec20f5fff5d8a35bf9258e9777a900ac3be93b71.json

### Resumen Funcional
El archivo `test_services.py` contiene pruebas unitarias para el módulo de servicios del sistema de monitoreo de almacén (WMS). Las pruebas cubren la creación y gestión de un estado global (`AppState`), la limpieza del estado después de cada prueba, y las funciones relacionadas con el manejo de túneles.

### Catálogo de Funciones y Clases
- `app_state()` - Devuelve una instancia limpia de `AppState`.
- `cleanup_tunnel()` - Limpia el estado global del túnel tras cada test.
- `test_state_cache_respects_limits(appstate)` - Verifica que el gestor de estado respete los límites de memoria.
- `test_state_sync_flag_reactivity(appstate)` - Valida que la propiedad reactiva de sincronización cambie su estado de forma correcta.
- `test_start_tunnel_manages_singleton_instance()` - Asegura que `start_tunnel` inicialice correctamente el servicio de túnel.
- `test_stop_tunnel_releases_global_reference()` - Valida que `stop_tunnel` limpie las referencias globales de forma segura.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `appstate` - Variable global que almacena el estado del sistema.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `pytest`
  - `unittest.mock`
  - `services_tunnel`
  - `core_state`

- **Flujo de Datos**:
  - El archivo `test_services.py` importa varios módulos y utiliza funciones para probar el comportamiento del sistema.
  - Las pruebas utilizan mocks y patches para simular comportamientos específicos durante las pruebas.
  - La función `app_state()` devuelve una instancia limpia de `AppState`, que es utilizada en algunas de las pruebas.

Este archivo se encuentra en la carpeta `tests/test_services.py` y es parte del proceso de prueba unitaria del sistema WMS.


---

## Archivo: ./graphify-out/cache/ast/0833fe33af9c0adc841e3fc694eddf131177b50ee7375fdfbc4a1dd23bb78d82.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
Clase abstracta unificada para procesar archivos WMS (TXT/CSV/XLSX). Implementa métodos para validar archivos, limpiar y transformar datos, detectar parámetros de archivo, leer y limpiar datos, obtener columnas requeridas y primarias, procesar y guardar datos, realizar upserts en SQLite, y procesar directorios.

### Catálogo de Funciones y Clases
- **BaseWMSProcessor**
  - `__init__(self, file_path: str, chunk_size: int = 1000)`
    - Inicializa el procesador con la ruta del archivo y el tamaño del chunk.
  - `validate_file(self) -> bool`
    - Verifica si el archivo es válido para este procesador.
  - `_clean_dataframe(self, dataframe: DataFrame) -> DataFrame`
    - Limpia y transforma un chunk de datos crudos (Implementado por cada hijo).
  - `_detect_file_params(self, file_path: Path) -> Tuple[str, str]`
    - Detecta la fila de encabezado y codificación buscando columnas clave.
  - `read_and_clean_data(self) -> DataFrame`
    - Lee el archivo completo (para testing o archivos pequeños).
  - `_get_required_columns(self, file_path: Path) -> List[str]`
    - Devuelve las columnas que actúan como clave primaria para deduplicación. Por defecto, devuelve una lista de strings que deben estar en el header.
  - `_get_primary_keys(self, file_path: Path) -> List[str]`
    - Devuelve las columnas que actúan como clave primaria para deduplicación. Por defecto, devuelve una lista de strings que deben estar en el header.
  - `process_and_save(self, connection: Connection, table_name: str) -> int`
    - Orquestador unificado de procesamiento Chunked + Upsert SQLite.
  - `_upsert_chunk(self, connection: Connection, dataframe: DataFrame, table_name: str) -> None`
    - Lógica de Upsert atómico por chunk. Seguridad de los f-strings.
  - `_post_process(self, connection: Connection, table_name: str) -> None`
    - Hook opcional para crear índices o post-procesar tras un upsert.
  - `process_directory(self, directory_path: Path, connection: Connection, table_name: str) -> int`
    - Escanea un directorio y procesa todos los archivos compatibles con Upsert acumulando resultados.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (se asume que las tablas se manejan a través del parámetro `table_name` en los métodos)
- **Columnas**: Ninguna (se asume que las columnas se manejan a través del parámetro `table_name` en los métodos)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - pandas
  - pathlib
  - sqlite3
  - typing
  - logging
  - core_security
- **Archivos del Proyecto que Este Archivo Importa (consume)**: Ninguno
- **Archivos del Proyecto que Importan a Este Archivo (lo consumen)**: Ninguno


---

## Archivo: ./graphify-out/cache/ast/087f2b892ed92921847a72be21201ce5113dbaf0ad580aa283bee861f30bc2c3.json

### Resumen Funcional
El archivo `inventory_service.py` contiene la lógica de negocio para el servicio de inventario en un sistema de monitoreo de almacén (WMS). Define una clase `InventoryService` que proporciona métodos para formatear números, obtener el período más reciente de datos y generar el contexto completo para el dashboard de movimientos.

### Catálogo de Funciones y Clases
- **Clase:** `InventoryService`
  - **Método:** `__init__(self, session: Session)`
    - Propósito: Inicializa la instancia con una sesión de base de datos.
  - **Método:** `fmt_num(self, num: str) -> str`
    - Propósito: Formatea un número como cadena.
  - **Método:** `_get_latest_data_period(self) -> str`
    - Propósito: Obtiene el período más reciente de datos disponibles en la base de datos.
  - **Método:** `_get_empty_context(self, context_type: str) -> Any`
    - Propósito: Genera un contexto vacío basado en el tipo de contexto proporcionado.
  - **Método:** `get_full_context(self) -> Any`
    - Propósito: Genera el contexto completo para el dashboard de movimientos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: No especificada explícitamente en el código.
  - Consultas SQL Crudas:
    ```sql
    SELECT * FROM table_name WHERE condition;
    ```
  - Llamadas a ORM:
    - `session.execute(text(query))`
    - `InventoryRepository.read_sql_query(query)`

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - SQLAlchemy
  - Pandas
  - Logging
  - Datetime
  - Typing
  - Core Utils
  - Core State
  - Repositories
  - Core WMS Config
- **Archivos del Proyecto que Importan a Este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:**
  - `sqlalchemy`
  - `pandas`
  - `logging`
  - `datetime`
  - `typing`
  - `core_utils`
  - `core_state`
  - `repositories`
  - `core_wms_config`

**Flujo de Datos:**
- El archivo importa varias bibliotecas y módulos necesarios para su funcionamiento.
- La clase `InventoryService` utiliza una sesión de base de datos (`Session`) para interactuar con la base de datos.
- Los métodos `_get_latest_data_period`, `_get_empty_context`, y `get_full_context` realizan operaciones en la base de datos y utilizan funciones de Pandas para procesar los datos.
- El método `get_full_context` depende de otros métodos internos y puede generar un contexto vacío o completo basado en el tipo de contexto proporcionado.


---

## Archivo: ./graphify-out/cache/ast/0b32ccedd96ba13bf64984e114e691efa0f4219d31ae946293147ce99318e67b.json

### Resumen Funcional
El archivo `check_queries.py` es un script que realiza consultas a una base de datos SQLite y utiliza pandas para procesar los resultados.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (se supone que las tablas son definidas en otro lugar del proyecto)
- **Columnas**: Ninguna (se supone que las columnas son definidas en otro lugar del proyecto)

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para procesar los resultados de las consultas.
  - `json`: Para manejar operaciones JSON.

- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno

**Flujo de Datos**: El script importa las bibliotecas necesarias y realiza consultas a la base de datos SQLite utilizando `sqlite3`. Los resultados se procesan con pandas y luego pueden ser exportados o utilizados según sea necesario.


---

## Archivo: ./graphify-out/cache/ast/0bd9e085d6851ba9217fa0b8a5a7c2d1f2d4af858e7af3db078f0bce1adc230f.json

### Resumen Funcional
El archivo `movements.py` contiene la implementación del adaptador para procesar el formato WMS Movimientos, incluyendo métodos para validar archivos, obtener columnas requeridas, limpiar dataframes y realizar clasificaciones vectorizadas.

### Catálogo de Funciones y Clases
- **InventoryMovementAdapter** - Adaptador específico para procesar el formato WMS Movimientos.
  - `.validate_file(path: Path) -> bool` - Valida si el archivo es válido.
  - `._get_required_columns() -> List[str]` - Obtiene las columnas requeridas.
  - `._get_primary_keys() -> List[str]` - Obtiene las claves primarias.
  - `._clean_dataframe(df: DataFrame) -> DataFrame` - Limpia el dataframe.
  - `._vectorized_classify(df: DataFrame) -> DataFrame` - Realiza clasificaciones vectorizadas.
  - `._post_process(file_path: str)` - Procesa el archivo post-transformación.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: pandas, numpy, pathlib, typing
- **Archivos Importados por este Archivo**:
  - `services/etl/base.py`
- **Archivos que Importan a este Archivo**:
  - Ninguno

El flujo de datos fluye desde el archivo principal hacia `movements.py`, donde se importan las dependencias necesarias y se definen los métodos para procesar los archivos WMS Movimientos.


---

## Archivo: ./graphify-out/cache/ast/0c499e306de4b6b2705076a26ee0c8fa90b428f341f70bcc5f232501ef3f005e.json

### Resumen Funcional
El archivo `stock.py` contiene la implementación del adaptador para procesar inventario/stock LX02, que realiza un REPLACE completo en los datos.

### Catálogo de Funciones y Clases
- **StockLevelAdapter()** - Adaptador para procesar Inventario/Stock LX02. Realiza REPLACE completo.
  - `.validate_file(path: Path) -> bool` - Valida el archivo proporcionado.
  - `._get_required_columns() -> List[str]` - Obtiene las columnas requeridas del header SAP LX02.
  - `.read_and_clean_data(file_path: Path) -> DataFrame` - Lee y limpia los datos del archivo.
  - `._clean_dataframe(df: DataFrame) -> DataFrame` - Limpia el dataframe.
  - `.process_directory(directory_path: str, connection: Connection) -> int` - Procesa todos los archivos en el directorio y realiza un REPLACE.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** Ninguna (el código no interactúa directamente con tablas de la base de datos).
- **Columnas:** Ninguna (el código no interactúa directamente con columnas de la base de datos).

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - pandas
  - pathlib
  - typing
  - sqlite3
  - os
  - datetime
  - logging
- **Archivos del Proyecto que Importan a Este Archivo (Consumen):** Ninguno
- **Archivos del Proyecto que Este Archivo Importa (Lo Consumen):**
  - `users_christianykelly_desktop_monitorweb_services_etl_base_py`

El flujo de datos comienza en el archivo principal, que importa `stock.py`, y luego se ejecutan las funciones definidas en `StockLevelAdapter` para validar archivos, leer y limpiar datos, y procesar directorios.


---

## Archivo: ./graphify-out/cache/ast/0e0cd0646ae6142f81e322200b6eb5c93f583a3fdc7e54f89bead20b0a6f6462.json

### Resumen Funcional
El archivo `pdf_reports.py` contiene funciones para generar informes PDF en un sistema de monitoreo de almacén (WMS). Estas funciones incluyen la parseación y formateo de cantidades, así como el dibujo de tablas de anexos y listas de picking.

### Catálogo de Funciones y Clases
- `_parse_qty()` - Parsea y sanitiza valores de cantidad.
- `_fmt_qty()` - Formatea cantidades para mostrar en PDF.
- `draw_annex_table()` - Dibuja la tabla de índice (anexo) de entregas agrupadas.
- `draw_picking_list()` - Dibuja la lista de picking desglosada por entrega pero con total consolidado.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
**Librerías Externas:**
- `datetime` (importado en la línea 2)

**Archivos del Proyecto que Importan a este Archivo (`pdf_reports.py`):**
- Ninguno

**Archivos del Proyecto que Este Archivo Importa (`pdf_reports.py`):**
- Ninguno


---

## Archivo: ./graphify-out/cache/ast/0eb15d9f49a60b1bd3090585220d654d1a73bb2cefb1838a3852f20ceccc9f59.json

### Resumen Funcional
El archivo `doc_prompts.py` contiene el código fuente de un módulo que probablemente se encarga de generar o manejar prompts para documentos en un sistema de monitoreo de almacén (WMS).

### Catálogo de Funciones y Clases
Ninguna.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
Ninguna.


---

## Archivo: ./graphify-out/cache/ast/0f8f23ca752eaf05d971ebe559afb3cbbbebe69710e8674943741e44b04a4108.json

### Resumen Funcional
El archivo `tasks.py` contiene dos funciones principales: `get_tasks_context()` y `analytics_tasks_api()`. La primera función recupera el contexto completo, mientras que la segunda proporciona análisis de tareas en formato JSON.

### Catálogo de Funciones y Clases
- **get_tasks_context(session: Session)**
  - Breve propósito: Recupera el contexto completo.
  
- **analytics_tasks_api(session: Session, appstate: AppState)**
  - Breve propósito: Proporciona análisis de tareas en formato JSON.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas:
  - No se especifican consultas SQL crudas o llamadas a ORM explícitas en el fragmento proporcionado.
  
### Estado y Variables Globales
- `session`: Variable global que representa la sesión de base de datos.
- `appstate`: Variable global que almacena el estado del sistema.

### Dependencias y Flujo
- **Librerías Externas**:
  - `logging`
  - `sqlalchemy_orm`
  - `sqlalchemy`
  - `pandas`
  - `datetime`
  - `core_state`
  - `core_utils`
  - `repositories`
  - `services_tasks_service`
  - `fastapi`
  - `core_database`
  - `core_auth`
  - `core_schemas`

- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa**:
  - `logging`
  - `sqlalchemy_orm`
  - `sqlalchemy`
  - `pandas`
  - `datetime`
  - `core_state`
  - `core_utils`
  - `repositories`
  - `services_tasks_service`
  - `fastapi`
  - `core_database`
  - `core_auth`
  - `core_schemas`

- **Flujo de Datos**:
  - El archivo importa varias librerías y módulos necesarios para su funcionamiento.
  - Las funciones `get_tasks_context` y `analytics_tasks_api` utilizan objetos como `session` y `appstate`, que son pasados como parámetros.


---

## Archivo: ./graphify-out/cache/ast/116f0b2d966298852f87da3c56df280088fc72705dc15afb3a5f5d7fddd580bd.json

### Resumen Funcional
El archivo `main_processor.py` contiene la lógica principal para ejecutar el análisis y consolidación completo del sistema de gestión de almacén (WMS). La función `run_pipeline()` es el punto de entrada que coordina todas las etapas del proceso.

### Catálogo de Funciones y Clases
- **run_pipeline()** - Ejecuta el flujo completo del WMS Analysis and Consolidation pipeline.
- **DataConsolidator** - Clase que realiza la consolidación de datos.
- **InventoryMovementAdapter** - Adaptador para procesar movimientos de inventario.
- **IW39Processor** - Procesador específico para el formato IW39.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
Ninguna. No se detectan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Librerías Externas**: `subprocess`, `sys`, `pathlib`, `logging`.
- **Archivos del Proyecto Importados**:
  - `config` (desde `scripts/main_processor.py`)
- **Archivos que Importan a Este Archivo**: Ninguno.

El flujo de datos fluye desde el punto de entrada `run_pipeline()` hacia las funciones y clases mencionadas, realizando tareas como la verificación de archivos, procesamiento de directorios, conexión a adaptadores e invocación de procesadores específicos.


---

## Archivo: ./graphify-out/cache/ast/121af652827c1eefa1f5c39b394c7151cbb3834b1cc6fe57c74a02d813e6c92a.json

### Resumen Funcional
El archivo `__init__.py` en la carpeta `repositories` del proyecto WMS es el punto de entrada para la configuración y obtención de repositorios de datos. Define funciones que devuelven instancias de diferentes tipos de repositorios (`DeliveriesRepository`, `InventoryRepository`, `TasksRepository`) y una función para obtener una conexión a la base de datos.

### Catálogo de Funciones y Clases
- **get_db()** - Obtiene una instancia de la conexión a la base de datos.
- **get_deliveries_repo()** - Devuelve una instancia del repositorio de entregas (`DeliveriesRepository`).
- **get_inventory_repo()** - Devuelve una instancia del repositorio de inventario (`InventoryRepository`).
- **get_tasks_repo()** - Devuelve una instancia del repositorio de tareas (`TasksRepository`).

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas y Columnas**: No se especifican columnas específicas, solo se menciona la conexión a la base de datos.
- **Consultas SQL Crudas o ORM**: No hay consultas SQL crudas o llamadas a ORM explícitas en este archivo.

### Estado y Variables Globales
No se detectan variables globales, de sesión, de entorno o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- **Librerías Externas**: `sqlite3`, `fastapi`
- **Archivos del Proyecto que IMPORTA (consume)**: `base.py`, `deliveries.py`, `inventory.py`, `tasks.py`
- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno
- **Dirección del Flujo de Datos**: El archivo importa librerías y otros módulos para configurar y obtener instancias de repositorios, pero no realiza operaciones directas en la base de datos.


---

## Archivo: ./graphify-out/cache/ast/15c4781e1da13feaaf38c1d858f4c03f14bc621fbf5ad07e15b9c88fd63d2b72.json

### Resumen Funcional
El archivo `check_dates.py` es un script que realiza operaciones relacionadas con fechas, probablemente para el monitoreo de almacén (WMS). No contiene ninguna interacción explícita con una base de datos.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada en este fragmento.

### Interacción con Base de Datos
Ninguna. El archivo no realiza ninguna operación relacionada con la base de datos.

### Estado y Variables Globales
Ninguna variable global, de sesión o de entorno detectada en este fragmento.

### Dependencias y Flujo
- **Librerías externas**: `sqlite3`, `pandas`
- **Archivos del proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno.
- **Flujo de datos**: El archivo importa las librerías `sqlite3` y `pandas`. No hay interacción con otros archivos o servicios dentro del proyecto.


---

## Archivo: ./graphify-out/cache/ast/16e98e449e985d319c4dfc8a4658ccbdcd1a9530475fe2b69fd17c0f7cb87b08.json

### Resumen Funcional
El archivo `test_server.py` contiene una función `run_server()` que ejecuta un servidor utilizando la biblioteca `uvicorn`.

### Catálogo de Funciones y Clases
- `run_server()` - Ejecuta el servidor.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: `uvicorn`, `config`, `threading`, `time`, `requests`.
- **Archivos Importados por este Archivo**: Ninguno.
- **Archivos que Importan a este Archivo**: Ninguno.
- **Flujo de Datos**: La función `run_server()` llama al método `run` de la biblioteca `uvicorn`.

**Nota**: El archivo no interactúa con una base de datos ni contiene variables globales.


---

## Archivo: ./graphify-out/cache/ast/1954ef9c47b4818cebc23f63113b890cc9c7deb1a99977e09c5dfdfd40689fef.json

### Resumen Funcional
El archivo `test_map.py` es un script que realiza operaciones de monitoreo y análisis en un sistema de almacén (WMS) utilizando bibliotecas como pandas, SQLite3, os, pathlib, sys y config.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada directamente en el fragmento proporcionado.

### Interacción con Base de Datos
- **Motor**: SQLite3
- **Tablas**: Ninguna especificada explícitamente.
- **Columnas**: Ninguna especificada explícitamente.
- **Consultas SQL Crudas/ORM**: Ninguna.

### Estado y Variables Globales
Ninguna variable global, de sesión o de entorno detectada directamente en el fragmento proporcionado.

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`
  - `pandas`
  - `os`
  - `pathlib`
  - `sys`
  - `config`

- **Archivos del Proyecto que IMPORTA a este archivo (lo consumen)**: Ninguno.

- **Archivos del Proyecto que ESTE archivo IMPORTA (consume)**:
  - `config` (importado desde `scratch/test_map.py`, línea 9)

- **Dirección del Flujo de Datos**: El flujo de datos comienza en el archivo `test_map.py` y se extiende hacia las bibliotecas importadas, incluyendo la configuración (`config`).


---

## Archivo: ./graphify-out/cache/ast/1a4890105d6c56fd4d41006ee6ef2384ab692387c5895e2cb8e9d67280517e7c.json

### Resumen Funcional
El archivo `test_analytics.py` contiene una definición de clase `FakeRequest` y realiza importaciones de módulos necesarios para su funcionamiento.

### Catálogo de Funciones y Clases
- **FakeRequest()** - Breve propósito: No se proporciona en el fragmento, pero probablemente sea una clase utilizada para simular solicitudes HTTP en pruebas unitarias.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías externas**: `sqlite3`, `traceback`
- **Archivos del proyecto que IMPORTA a este archivo (`scratch/test_analytics.py`)**: `config`, `routes_analytics_vl06o`
- **Archivos del proyecto que ESTE archivo IMPORTA (`scratch/test_analytics.py`)**: Ninguno
- **Dirección del flujo de datos**: No se proporciona información sobre el flujo de datos específico en este fragmento.


---

## Archivo: ./graphify-out/cache/ast/1bf71bf325d72001f6b66e7b16870ffb13ef2c7a7077b5afe53eacc63abd6c0c.json

### Resumen Funcional
El archivo `fix_mb51_func.py` contiene una función `_prepare_user_location_analytics()` que se encarga de preparar estadísticas detalladas de usuarios y ubicaciones con actividad mensual.

### Catálogo de Funciones y Clases
- `_prepare_user_location_analytics()`: Prepara estadísticas detalladas de usuarios y ubicaciones con actividad mensual.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (se supone que las consultas SQL son generadas dinámicamente)
- **Columnas**: Ninguna (se supone que las consultas SQL son generadas dinámicamente)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `zfill`
  - `read_sql` (de SQLAlchemy)
  - `to_dict` (de pandas)
  - `fmt_num`

- **Archivos del Proyecto que IMPORTA a este archivo**: Ninguno

- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno

- **Flujo de Datos**:
  - La función `_prepare_user_location_analytics()` llama a varias funciones y métodos, incluyendo `zfill`, `read_sql`, `to_dict` y `fmt_num`. Estas llamadas se realizan dentro del flujo de la función para preparar las estadísticas detalladas.


---

## Archivo: ./graphify-out/cache/ast/1cc634b977c313b685269839394a52752cb1431525c5ec00fbdd46554ad0461f.json

### Resumen Funcional
El archivo `update_inv_kpis.py` es un script que realiza operaciones de actualización en el inventario del sistema de monitoreo de almacén (WMS). No contiene una descripción detallada de su funcionalidad, pero se infiere que interactúa con la base de datos para actualizar los KPIs del inventario.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna especificada explícitamente en el fragmento.
- **Columnas**: Ninguna especificada explícitamente en el fragmento.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Importado para interactuar con la base de datos SQLite.
  - `json`: Importado para manejar operaciones JSON, aunque no se ve claramente cómo se usa en el fragmento proporcionado.

- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno especificados.

- **Flujo de Datos**: El archivo importa bibliotecas necesarias y no contiene llamadas directas a funciones o métodos específicos, por lo que no hay un flujo claro de datos definido en el fragmento proporcionado.


---

## Archivo: ./graphify-out/cache/ast/214298c9dfecd526175e5eb35b9c2e61aeba7a4d22cf09a5dd4bba2043cd5baa.json

### Resumen Funcional
El archivo `free_ram.py` contiene funciones para gestionar la liberación de memoria en un sistema operativo macOS utilizando AppleScript. La función principal es `main()`, que invoca a otra función `quit_app()` para cerrar una aplicación de forma segura.

### Catálogo de Funciones y Clases
- `quit_app()` - Cierra una aplicaciónde forma segura usando AppleScript.
- `main()` - Flujo principal del script, que llama a `quit_app()`.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `os`
  - `subprocess`

- **Archivos del Proyecto que Importan a este Archivo**:
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno

- **Flujo de Datos**:
  - El script importa las librerías necesarias (`os` y `subprocess`) al inicio.
  - La función `main()` llama a la función `quit_app()`.
  - La función `quit_app()` ejecuta un comando AppleScript para cerrar una aplicación.

Este flujo es simple, sin interacción con bases de datos ni variables globales.


---

## Archivo: ./graphify-out/cache/ast/21d5b8af26579c3e12417bb799cdb466b760e31ee4529daf179dda0bf9f2639e.json

### Resumen Funcional
El archivo `predictive_engine.py` contiene una función llamada `generate_predictions()` que procesa movimientos de transacciones para generar modelos predictivos. La función utiliza diversas bibliotecas como pandas, numpy y SQLite para realizar operaciones de análisis y manipulación de datos.

### Catálogo de Funciones y Clases
- **generate_predictions()** - Procesa Movimientos Transactions para generar modelos predictivos: 1. Market

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:** No se especifican explícitamente las tablas o columnas manipuladas en este archivo.

### Estado y Variables Globales
- Ninguna

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
  - `core_wms_config`

- **Archivos del Proyecto que Importan a este Archivo:**
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa:**
  - `core_wms_config`

- **Flujo de Datos:** El archivo importa varias bibliotecas y dependencias, realiza operaciones de análisis y manipulación de datos utilizando pandas, numpy y SQLite, pero no se especifican las tablas o columnas específicas.


---

## Archivo: ./graphify-out/cache/ast/22724d61080e7569670c719f388a515631c3055265f55019f687e521cf7b246c.json

### Resumen Funcional
El archivo `pdf.py` contiene funciones para generar PDFs en un sistema de monitoreo de almacén (WMS). Incluye una función para generar un PDF único y otra para generar un reporte masivo con índice y picking list.

### Catálogo de Funciones y Clases
- **generate_pdf(str, bool, str, Session)** - Genera un PDF para una única entrega.
- **generate_pdf_bulk(str, str, str, str, str, bool, str, Session)** - Genera un reporte masivo con índice y picking list.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: No se especifican explícitamente en el fragmento.
- **Columnas**: No se especifican explícitamente en el fragmento.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno mencionadas en el fragmento.

### Dependencias y Flujo
- **Librerías Externas**:
  - `io`
  - `logging`
  - `core_database`
  - `sqlalchemy_orm`
  - `sqlalchemy`
  - `pandas`
  - `datetime`
  - `typing`
  - `fastapi`
  - `fastapi_responses`
  - `config`
  - `core_pdf_engine`
  - `repositories_deliveries`
  - `core_pdf_reports`

- **Archivos del Proyecto que Importan a Este Archivo**:
  - No se especifican explícitamente en el fragmento.

- **Flujo de Datos**: El archivo importa varias librerías y módulos, incluyendo `DeliveriesRepository` y otros componentes del sistema WMS. Las funciones `generate_pdf` y `generate_pdf_bulk` utilizan estos componentes para interactuar con la base de datos y generar PDFs.

Este análisis proporciona una visión detallada de las funcionalidades, dependencias y interacciones del archivo `pdf.py` en el contexto del sistema WMS.


---

## Archivo: ./graphify-out/cache/ast/248900fa5696f9164b38c451ab4ccbd5ea7b766f0ae237c81888e37db8eb8795.json

### Resumen Funcional
El archivo `app.py` es el punto de entrada principal del sistema de monitoreo de almacén (WMS). Define la configuración y arranque asincrónico de la aplicación FastAPI, incluyendo la inicialización de bases de datos, la creación de rutas, y la gestión del ciclo de vida de la aplicación.

### Catálogo de Funciones y Clases
- `lifespan()`: Maneja el ciclo de vida de la aplicación. Gestiona el arranque asincrónico.
- `initialize_app()`: Configura y prepara la aplicación FastAPI.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
**Dependencias Externas:**
- `os`
- `logging`
- `contextlib`
- `warnings`
- `fastapi`
- `fastapi_responses`
- `fastapi_staticfiles`
- `config`
- `core_app_instance`
- `routes_config`

**Archivos del Proyecto que Importan a este Archivo:**
Ninguno

**Archivos del Proyecto que Este Archivo Importa:**
Ninguno

**Flujo de Datos:**
El archivo `app.py` importa varias bibliotecas y módulos necesarios para configurar y arrancar la aplicación FastAPI. Luego, define dos funciones principales: `lifespan()` y `initialize_app()`. La función `lifespan()` se encarga del ciclo de vida de la aplicación, mientras que `initialize_app()` configura y prepara la aplicación FastAPI.


---

## Archivo: ./graphify-out/cache/ast/2512d99f377792ee48a36d08df70590f533e225fac02afe6c96c2820fd43e7cb.json

### Resumen Funcional
El archivo `analytics_proyecciones.py` contiene las rutas y lógica para obtener el contexto de proyecciones y los datos de proyecciones en un sistema de monitoreo de almacén (WMS). Las funciones principales son `get_proyecciones_context()` y `get_analytics_proyecciones()`, que manejan la obtención de datos de proyecciones y su formato de salida.

### Catálogo de Funciones y Clases
- **`get_proyecciones_context()`** - Obtiene el contexto de proyecciones, priorizando la caché.
- **`get_analytics_proyecciones()`** - Retorna los datos de proyecciones en formato JSON.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales, de sesión o diccionarios quemados en el código que almacenen estado crítico.

### Dependencias y Flujo
- **Dependencias Externas**: `fastapi`, `core_auth`, `fastapi_responses`, `core_state`, `db_predictive_engine`, `config`.
- **Flujo de Datos**:
  - El archivo importa varias bibliotecas y módulos necesarios para su funcionamiento.
  - La función `get_proyecciones_context()` realiza operaciones como obtener el estado de la aplicación, recuperar datos de caché, generar predicciones y almacenarlos en caché.
  - La función `get_analytics_proyecciones()` limpia la caché y retorna los datos de proyecciones en formato JSON.

Este archivo es parte del componente "Routes" del sistema WMS, donde se definen las rutas para interactuar con el servicio de análisis de proyecciones.


---

## Archivo: ./graphify-out/cache/ast/2648ddaf09c775d584e45812bcb9a284a0aea4428f4e77304f12cc1886df102e.json

### Resumen Funcional
El archivo `analyze_dom.py` contiene una función que realiza el análisis de elementos DOM para identificar aquellos que son considerados grandes.

### Catálogo de Funciones y Clases
- **find_large_elements()** - Identifica y devuelve los elementos DOM que son considerados grandes.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `asyncio`, `httpx`, `bs4`
- **Archivos Importados por Este Archivo**:
  - Ninguno
- **Archivos que Importan a Este Archivo**:
  - Ninguno
- **Flujo de Datos**: El archivo importa bibliotecas para realizar operaciones asíncronas, HTTP y análisis de HTML. La función `find_large_elements()` utiliza estas bibliotecas para obtener y analizar elementos DOM.

### Notas Adicionales
La función `find_large_elements()` realiza una solicitud HTTP para obtener el contenido de una página web, luego usa BeautifulSoup para parsear el HTML y encontrar todos los elementos que cumplen con ciertos criterios de tamaño. Los resultados se almacenan en una lista y devuelven finalmente.


---

## Archivo: ./graphify-out/cache/ast/2698c4f92f61d2045d9a40677c212db456adb8e797d6fef296d7bf17bbbbc850.json

### Resumen Funcional
El archivo `migrate_monthly_sql.py` contiene el código necesario para migrar los datos de la tabla `vl_sla_monthly_trend` en la base de datos de configuración al nuevo formato.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: `vl_sla_monthly_trend`
- **Columnas**: No especificadas explícitamente en el fragmento proporcionado.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `json`: Para manejar operaciones JSON.
  - `pandas`: Para procesar los datos en formato DataFrame.

- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno

El flujo de datos es simple: el script importa las librerías necesarias, realiza la migración de los datos y no depende de ninguna otra parte del proyecto.


---

## Archivo: ./graphify-out/cache/ast/26acef1135f4ddafeda2dd941412cb7d1aa1e6c1c655718558d04d2044dafbd0.json

### Resumen Funcional
El archivo `test_efficiency.py` contiene una función llamada `calculate_efficiency()` que realiza cálculos de eficiencia en un almacén utilizando pandas, numpy y SQLite.

### Catálogo de Funciones y Clases
- **calculate_efficiency()** - Realiza cálculos de eficiencia en los datos del almacén.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** Ninguna (se asume que la conexión se realiza a través de una base de datos SQLite local).
- **Columnas:** Ninguna (se asume que las consultas SQL son generadas dinámicamente).

### Estado y Variables Globales
- Ninguna.

### Dependencias y Flujo
- **Librerías Externas:**
  - `sqlite3`
  - `pandas`
  - `numpy`

- **Archivos del Proyecto que Importan a este Archivo:** Ninguno.
- **Archivos del Proyecto que Este Archivo Importa:** Ninguno.

**Flujo de Datos:**
1. La función `calculate_efficiency()` se importa desde `test_efficiency.py`.
2. Se realiza una conexión a la base de datos SQLite (implícita).
3. Se ejecutan consultas SQL para leer los datos del almacén.
4. Los datos son procesados utilizando pandas y numpy.
5. El resultado del cálculo de eficiencia se devuelve.

**Ejemplo de Flujo:**
```python
import sqlite3
import pandas as pd
import numpy as np

def calculate_efficiency():
    # Conexión a la base de datos SQLite (implícita)
    conn = sqlite3.connect('almacen.db')
    
    # Consulta SQL para leer los datos del almacén
    query = "SELECT * FROM inventario"
    df = pd.read_sql(query, conn)
    
    # Procesamiento de los datos con pandas y numpy
    df['fecha'] = pd.to_datetime(df['fecha'])
    df.dropna(inplace=True)
    dias_laborables = np.busday_count(df['fecha'].min(), df['fecha'].max())
    
    # Cálculo de eficiencia
    eficiencia = len(df) / dias_laborables
    
    return eficiencia

# Ejecución de la función
result = calculate_efficiency()
print(f"Eficiencia del almacén: {result}")


---

## Archivo: ./graphify-out/cache/ast/270d77c0b49bdfc62c4cda6d71d370da9619bc2a608b04020a4387bd92c01b0b.json

### Resumen Funcional
El archivo `repositories/widgets.py` contiene la definición de una clase `WidgetRepository` que hereda de `BaseRepository`. Esta clase incluye dos métodos: `.execute_widget()` y `.execute_drilldown()`, los cuales realizan operaciones relacionadas con el procesamiento y visualización de datos.

### Catálogo de Funciones y Clases
- **Clase:** `WidgetRepository`
  - **Método:** `.execute_widget()`
    - **Parámetros:** No especificados en el fragmento.
    - **Propósito:** Ejecuta una operación widget específica.
  - **Método:** `.execute_drilldown()`
    - **Parámetros:** No especificados en el fragmento.
    - **Propósito:** Realiza una operación de drilldown.

### Interacción con Base de Datos
- **Motor:** SQLite (implícito a través del uso de SQLAlchemy).
- **Tablas y Columnas:** No se mencionan explícitamente tablas o columnas en el fragmento.
- **Consultas SQL Crudas/ORM:** Se utilizan métodos como `get`, `append`, `drop`, `fillna`, `pivot_table`, `tolist` de la biblioteca `pandas`. También se hace uso del método `read_sql` para leer datos desde una consulta SQL.

### Estado y Variables Globales
- **Variables Globales:** No hay variables globales mencionadas en el fragmento.
- **Sesión/Entorno:** No hay referencias a sesiones o entornos específicos.
- **Diccionarios Quemados:** No se utilizan diccionarios quemados en el código.

### Dependencias y Flujo
- **Librerías Externas:**
  - `logging`
  - `json`
  - `pandas`
  - `sqlalchemy`
  - `typing`
- **Archivos del Proyecto que Importa (`repositories/widgets.py`):**
  - `users_christianykelly_desktop_monitorweb_repositories_base_py`
  - `core_helpers_dynamic_executor`
  - `core_schemas`
  - `core_query_engine`
  - `core_utils`
- **Archivos del Proyecto que son Importados por (`repositories/widgets.py`):**
  - Ninguno mencionado en el fragmento.

**Flujo de Datos:**
El flujo de datos comienza en los métodos `.execute_widget()` y `.execute_drilldown()`, donde se realizan operaciones con `pandas`. Estos métodos interactúan con la base de datos a través de SQLAlchemy, pero no se especifican las tablas o columnas específicas.


---

## Archivo: ./graphify-out/cache/ast/275db49a0ee9d430e5c68c88f7f4cbc797e9d8e5e863d5e364fe78c44cdfb1ca.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `consolidator.py` es un script que gestiona la consolidación de archivos WMS en una base de datos SQLite. Realiza tareas como la conexión a la base de datos, análisis de fechas en los nombres de archivos, consolidación de archivos cronológicamente, actualización de tablas con los datos más recientes, enriquecimiento de transacciones con información de stock y movimientos, y cierre seguro de la conexión.

### Catálogo de Funciones y Clases
- `DataConsolidator()`: Clase principal que gestiona la consolidación de archivos WMS.
  - `__init__(self, db_path: str)`: Inicializa el objeto con la ruta a la base de datos SQLite.
  - `__enter__(self)`: Método para manejar el protocolo de contexto (with).
  - `__exit__(self, exc_type, exc_val, exc_tb)`: Método para manejar el protocolo de contexto (with).
  - `connect(self)`: Establece la conexión a la base de datos y configura optimizaciones.
  - `_parse_file_date(self, file_name: str) -> datetime.date`: Extrae la fecha del nombre del archivo en formato dd-mm-yyyy.
  - `consolidate_folder(self, folder_path: str, target_table: str)`: Consolida archivos cronológicamente en una tabla específica.
  - `overwrite_with_latest(self, source_folder: str, target_table: str)`: Reemplaza la tabla con los datos del archivo más reciente.
  - `enrich_deliveries_with_stock(self, deliveries_table: str, stock_table: str)`: Enriquece las transacciones con información de stock actual.
  - `backfill_from_movements(self, deliveries_table: str, movements_table: str)`: Sincroniza datos faltantes desde la tabla Movimientos.
  - `backfill_texts(self, deliveries_table: str, stock_table: str, movements_table: str)`: Sincroniza descripciones faltantes desde Stock y Movimientos.
  - `update_sla_with_tasks(self, sla_table: str, tasks_table: str)`: Actualiza el SLA cruzando fechas con Tareas.
  - `close(self)`: Cierra la conexión de forma segura.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - No se especifican explícitamente las tablas en este fragmento, pero se infiere que existen tablas como `deliveries`, `stock`, `movements` y `sla`.
- Columnas:
  - No se especifican explícitamente las columnas en este fragmento.
- Consultas SQL Crudas: No hay consultas SQL crudas directamente visibles, pero se infiere que existen llamadas a métodos como `execute`, `to_sql` y otros que implican operaciones de base de datos.

### Estado y Variables Globales
No hay variables globales explícitamente mencionadas en este fragmento.

### Dependencias y Flujo
- Librerías Externas:
  - `os`
  - `sqlite3`
  - `logging`
  - `re`
  - `pathlib`
  - `datetime`
  - `typing`
  - `services_etl`
  - `users_christianykelly_desktop_monitorweb_db_enrichment_py`
  - `core_security`
- Archivos del Proyecto que Este Archivo Importa:
  - No se especifican explícitamente los archivos que este archivo importa.
- Archivos del Proyecto que Importan a Este Archivo:
  - No se especifican explícitamente los archivos que importan a este archivo.

El flujo de datos es desde `main()` hacia `DataConsolidator` y sus métodos, pasando por funciones auxiliares y adaptadores para procesar y guardar datos.


---

## Archivo: ./graphify-out/cache/ast/27822743d1ba852b1150577cdf502fb5d2b650df01bdc61a394bfb6ad5311f9b.json

### Resumen Funcional
El archivo `deliveries.py` contiene la implementación del adaptador para procesar Entregas de Salida (Deliveries) en el sistema de monitoreo de almacén (WMS). Este adaptador hereda de `BaseWMSProcessor` y define métodos para validar archivos, obtener columnas requeridas, limpiar dataframes, sanitizar nombres de columnas, realizar procesamiento post, e insertar o actualizar chunks de datos en la base de datos.

### Catálogo de Funciones y Clases
- **OutboundDeliveryAdapter()** - Adaptador para procesar Entregas de Salida (Deliveries).
  - `.validate_file(path: Path) -> bool` - Valida el archivo proporcionado.
  - `._get_required_columns() -> List[str]` - Obtiene las columnas requeridas.
  - `._get_primary_keys() -> List[str]` - Obtiene las claves primarias.
  - `._clean_dataframe(df: DataFrame) -> DataFrame` - Limpia el dataframe.
  - `._sanitizar_nombres_columnas(index: Index) -> None` - Sanitiza los nombres de las columnas.
  - `._post_process(file_path: str) -> None` - Realiza procesamiento post.
  - `._upsert_chunk(connection: Connection, df: DataFrame, table_name: str) -> None` - Inserta o actualiza chunks de datos en la base de datos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas Modificadas/Leídas:**
  - Tabla: `outbound_deliveries`
    - Columnas: Dependiendo del contexto, se pueden modificar o leer columnas específicas.
  - Consultas SQL Crudas:
    - Ejemplo de consulta para crear índices: `CREATE INDEX idx_outbound_deliveries_column ON outbound_deliveries(column_name);`

### Estado y Variables Globales
- **Ninguna**

### Dependencias y Flujo
- **Librerías Externas:** pandas, pathlib, typing, sqlite3
- **Archivos del Proyecto que Importan a este Archivo:**
  - `users_christianykelly_desktop_monitorweb_services_etl_base_py`
  - `core_wms_utils`
- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno

**Flujo de Datos:** El archivo `deliveries.py` se importa por otros archivos y utiliza métodos definidos en él para procesar los datos de entregas de salida, incluyendo la validación, limpieza y carga en la base de datos.


---

## Archivo: ./graphify-out/cache/ast/2f83b9a0f80542770ddcfa30996a5dc636a038df795934b25d3d946809a96a27.json

### Resumen Funcional
El archivo `productivity_monthly.py` contiene la lógica de negocio para el cálculo y recuperación de datos de productividad mensuales en un sistema de monitoreo de almacén (WMS). Define una clase `ProductivityMonthlyService` que proporciona métodos para obtener resúmenes mensuales de movimientos de usuarios y detalles específicos.

### Catálogo de Funciones y Clases
- **ProductivityMonthlyService()** - Inicializa el servicio con una sesión.
- **get_monthly_productivity_data(date: str) -> Any** - Obtiene los datos de productividad mensuales para un usuario específico en un mes dado.
- **get_user_movements_monthly_summary(user_id: str, month: str)** - Retorna resúmenes mensuales de movimientos de usuarios.
- **get_user_movements_monthly_details(user_id: str, month: str)** - Retorna detalles específicos de los movimientos de usuarios en un mes dado.

### Interacción con Base de Datos
No se especifican consultas SQL crudas o llamadas a ORM explícitas. La interacción con la base de datos se realiza a través del repositorio `TasksRepository`.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: 
  - Importa módulos como `logging`, `typing`, `sqlalchemy_orm` y `repositories_tasks`.
  - Utiliza la clase `Session` de SQLAlchemy.
  
- **Flujo**:
  - El archivo `productivity_monthly.py` importa varios módulos y dependencias necesarias para su funcionamiento.
  - La clase `ProductivityMonthlyService` se utiliza en otros archivos del proyecto, lo que indica que este archivo es consumido por otros componentes del sistema.


---

## Archivo: ./graphify-out/cache/ast/304c8d2fa81f6a72f36d68335f803a792da5c01823caf3628b36db205cd41f4b.json

### Resumen Funcional
El archivo `build_analytics.py` contiene funciones para extraer información de un cuerpo de texto y procesarla, finalmente escribiendo el resultado en un archivo.

### Catálogo de Funciones y Clases
- `extract_body()` - Extrae información relevante del cuerpo de texto.
- `main()` - Llama a la función `extract_body()` y realiza operaciones adicionales para procesar y guardar los datos.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: No se mencionan dependencias externas específicas.
- **Archivos Importados**: El archivo importa el módulo `re` (módulo de expresiones regulares).
- **Flujo de Datos**:
  - `main()` llama a `extract_body()`.
  - `extract_body()` realiza operaciones como lectura, búsqueda y procesamiento del texto.
  - Los resultados son procesados en `main()` y finalmente escritos en un archivo.

El flujo general es: `main()` -> `extract_body()` -> Procesamiento de datos -> Escritura en archivo.


---

## Archivo: ./graphify-out/cache/ast/304f886cabadc03a8789908d8ad0097d51432255b665a2d566f642dc1fddf98b.json

### Resumen Funcional
El archivo `query_utils.py` contiene funciones que se utilizan para extraer parámetros de visualización y valores métricos de datos.

### Catálogo de Funciones y Clases
- `get_bound_params_from_visual_state(visual_state: str) -> List[str]`: Extrae los bind params (?) de un visual_state JSON serializado. Lee la lista de parámetros de enlace.
- `extract_metric_value(df: pd.DataFrame, column_name: str) -> float`: Extrae el valor numérico principal de un DataFrame de resultado de query.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `json`, `pandas` (pd)
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno
- **Archivos del Proyecto que Este Archivo Importa**: Ninguno
- **Flujo de Datos**: El archivo importa y utiliza métodos de las librerías `json` y `pandas` para procesar datos.


---

## Archivo: ./graphify-out/cache/ast/30755f350f7868b645cd6840aa3fecd61ad22f5fd2ad46633fe069b0085343bf.json

### Resumen Funcional
El archivo `update_abc.py` es un script que realiza operaciones de actualización en una base de datos SQLite.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna especificada
- **Columnas**: Ninguna especificada
- **Consultas SQL Crudas o Llamadas a ORM**: Importa el módulo `sqlite3` para interactuar con la base de datos.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `sqlite3`
- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno
- **Dirección del Flujo de Datos**: El archivo importa el módulo `sqlite3` y no realiza ninguna operación específica sobre la base de datos.


---

## Archivo: ./graphify-out/cache/ast/30b35bde69ca83a89e98700247ddb3d26386d4301bfdd707912c44bd121ebb3b.json

### Resumen Funcional
El archivo `run_compiled_query.py` contiene código que realiza consultas SQL compiladas utilizando el motor de base de datos SQLite y la biblioteca pandas para procesar los resultados.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** Ninguna (No se mencionan consultas específicas a tablas)
- **Columnas:** Ninguna (No se mencionan consultas específicas a columnas)

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas:**
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para procesar los resultados de las consultas SQL.

- **Flujo de Datos:**
  - El archivo `run_compiled_query.py` importa `sqlite3` y `pandas`.
  - No se mencionan funciones o métodos específicos, por lo que no hay un flujo de datos definido en este fragmento.


---

## Archivo: ./graphify-out/cache/ast/372cf2fa28e957601b1d7c91d64b422fff4416537b764eafe3b626dc56b3fc2e.json

### Resumen Funcional
El archivo `test_dashboard_context.py` contiene una función llamada `diag_dashboard()` que realiza operaciones de conexión a una base de datos SQLite, obtiene contexto de tareas y cierra la conexión.

### Catálogo de Funciones y Clases
- `diag_dashboard()` - Realiza operaciones de conexión a una base de datos SQLite, obtiene contexto de tareas y cierra la conexión.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:** Ninguna (se asume que las consultas SQL están implícitas en los métodos `connect`, `get_tasks_context`, `get` y `close`)
- **Consultas SQL Crudas o Llamadas a ORM:** No se especifican consultas SQL crudas ni llamadas a ORM explícitas.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `sqlite3`
- **Archivos del Proyecto que IMPORTA (consume):** `routes_tasks`
- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen):** Ninguno
- **Dirección del Flujo de Datos:** El flujo comienza en la función `diag_dashboard()`, realiza operaciones de base de datos y luego cierra la conexión.


---

## Archivo: ./graphify-out/cache/ast/396390b1d9abe747b9a11af5b5a51b08c75407a1f32f902fb2d367909bf04e41.json

### Resumen Funcional
El archivo `generate_graphify.py` contiene una función `run_graphify()` que realiza diversas operaciones de sistema y manejo de archivos, como la creación de directorios, copia de archivos, escritura en archivos, ejecución de comandos externos, etc.

### Catálogo de Funciones y Clases
- **run_graphify()** - Realiza las operaciones descritas anteriormente.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**: `os`, `subprocess`, `shutil`.
- **Archivos Importados por Este Archivo**: Ninguno.
- **Archivos que Importan a Este Archivo**: Ninguno.
- **Flujo de Datos**: El flujo de datos se centra en la manipulación de archivos y directorios del sistema operativo, así como la ejecución de comandos externos.


---

## Archivo: ./graphify-out/cache/ast/3c0c1d4e0ad1fc97ca573ef39e45e21ee9e3e49e50ed4c4c8dc0aea894bf2b00.json

### Resumen Funcional
El archivo `productivity_daily.py` contiene la lógica de negocio para el servicio de productividad diaria, que incluye métodos para obtener fechas disponibles, datos de productividad y resúmenes/detalles de movimientos diarios de usuarios.

### Catálogo de Funciones y Clases
- `ProductivityDailyService` - Servicio principal para la gestión de datos de productividad diaria.
  - `__init__(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - `get_available_dates()` - Obtiene todas las fechas disponibles en el sistema.
  - `get_productivity_data(date: str) -> Any` - Retorna los KPIs de productividad para una fecha específica (YYYY-MM-DD).
  - `get_user_movements_daily_summary(user_id: str, date: str)` - Retorna un resumen diario de movimientos de usuario.
  - `get_user_movements_daily_details(user_id: str, date: str)` - Retorna los detalles diarios de movimientos de usuario.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas y Columnas:
  - **Ninguna** (El archivo no contiene consultas SQL explícitas ni llamadas a ORM que interactúen directamente con la base de datos).

### Estado y Variables Globales
- **Ninguna** (No se detectan variables globales, de sesión o diccionarios quemados en el código).

### Dependencias y Flujo
- **Librerías Externas**: `logging`, `typing`, `sqlalchemy.orm`
- **Archivos del Proyecto que Importa a Este Archivo**: Ninguno.
- **Archivos del Proyecto que Este Archivo Importa**: `repositories.tasks`
- **Flujo de Datos**: El archivo importa dependencias necesarias y utiliza el repositorio `TasksRepository` para obtener datos. Los métodos del servicio interactúan con los datos internos del sistema, no con la base de datos directamente.

**Nota**: El archivo no contiene consultas SQL explícitas ni llamadas a ORM que interactúen directamente con la base de datos. Todas las operaciones se realizan en memoria o mediante métodos interno del servicio.


---

## Archivo: ./graphify-out/cache/ast/3cd7e0c173e88fb532d1d35ceaeea87dafb9c8efddb884ae8c20ba1c25891b9f.json

### Resumen Funcional
El archivo `test_ia.py` contiene una función llamada `test_analytics_ia()` que realiza operaciones de análisis utilizando la biblioteca `httpx` para hacer solicitudes HTTP y procesar los resultados.

### Catálogo de Funciones y Clases
- **test_analytics_ia()** - Realiza operaciones de análisis mediante solicitudes HTTP.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: `asyncio`, `httpx`, `sys`, `os`, `time`.
- **Flujo de Datos**:
  - El archivo importa varias bibliotecas (`asyncio`, `httpx`, `sys`, `os`, `time`).
  - La función `test_analytics_ia()` realiza una solicitud HTTP utilizando la clase `AsyncClient` de la biblioteca `httpx`.
  - Los resultados de la solicitud son procesados y manipulados dentro de la función.

**Nota**: El archivo no interactúa con ninguna base de datos ni utiliza variables globales.


---

## Archivo: ./graphify-out/cache/ast/3f1256fac516858adab62c10c73396d4972d27628e54666f5c3f668c017ccc2d.json

### Resumen Funcional
El archivo `auth.py` contiene funciones y clases relacionadas con la autenticación y seguridad del sistema de monitoreo de almacén (WMS). Incluye operaciones como el hash de contraseñas, verificación de contraseñas, creación de tokens JWT, decodificación de tokens y gestión de usuarios.

### Catálogo de Funciones y Clases
- `TokenResponse` - Modelo Pydantic para la respuesta de autenticación.
- `UserCreate` - Modelo Pydantic para crear un nuevo usuario.
- `ChangePasswordRequest` - Modelo Pydantic para cambiar la contraseña de un usuario.
- `UserPublic` - Modelo Pydantic para representar un usuario de manera pública.
- `hash_password(password: str) -> str` - Genera un hash bcrypt del password.
- `verify_password(plain_password: str, hashed_password: str) -> bool` - Verifica si una contraseña sin encriptar coincide con su hash.
- `create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> Tuple[str, int]` - Crea un JWT firmado con HS256.
- `decode_token(token: str) -> Union[dict, None]` - Decodifica y valida un JWT. Retorna None si es inválido o expirado.
- `get_current_user(request: Request, session: Session) -> User` - Depende del token JWT para extraer el usuario actual. Si no hay token, retorna un error.
- `require_auth(user: User) -> User` - EXIGE que el usuario esté autenticado (no invitado).
- `require_admin(user: User) -> User` - EXIGE que el usuario tenga rol de administrador. Lanza 403 si no tiene permisos.
- `init_auth_db()` - Crea las tablas de autenticación si no existen.
- `ensure_admin_exists()` - Crea el usuario admin por defecto si no existe ninguno.

### Interacción con Base de Datos
No se especifican consultas SQL crudas o llamadas a ORM explícitas en este archivo. La interacción con la base de datos parece ser gestionada a través de métodos como `get`, `first`, `query` y `count`.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: `os`, `logging`, `datetime`, `typing`, `bcrypt`, `jwt`, `fastapi`, `fastapi_security`, `sqlalchemy_orm`, `pydantic`.
- **Archivos del Proyecto que Este Archivo Importa**:
  - `core/auth.py` (se importa a sí mismo)
  - `os`
  - `logging`
  - `datetime`
  - `typing`
  - `bcrypt`
  - `jwt`
  - `fastapi`
  - `fastapi_security`
  - `sqlalchemy_orm`
  - `pydantic`
- **Archivos del Proyecto que Importan a Este Archivo**:
  - No se especifica en el fragmento proporcionado.

El flujo de datos fluye desde las funciones y métodos que dependen de otras funciones y clases, hasta la interacción con la base de datos (si es necesario).


---

## Archivo: ./graphify-out/cache/ast/4046e65c894c9454c79a7ca4a62913f3f4975421bbcb99dd25004c9d2315a208.json

### Resumen Funcional
El archivo `conftest.py` contiene funciones de configuración y inicialización para pruebas en un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Define clientes de prueba, sesiones de base de datos y funciones auxiliares para preparar el entorno de pruebas.

### Catálogo de Funciones y Clases
- `skip_warmup()` - No tiene parámetros. Proporciona una razón: "El warm_up ahora ocurre dentro del lifespan."
- `session_db()` - No tiene parámetros. Crea e inicializa la base de datos maestra compartida para toda la sesión de pruebas.
- `test_db()` - No tiene parámetros. Proporciona aislamiento de datos entre pruebas individuales.
- `client()` - No tiene parámetros. Cliente de pruebas de FastAPI configurado para interactuar con la BD de sesión.
- `auth_client()` - No tiene parámetros. Proporciona un cliente con token de administrador pre-autenticado.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas y Columnas**:
  - Tabla: Ninguna específica mencionada en el código proporcionado.
- **Consultas SQL Crudas o Llamadas a ORM**:
  - `connect()`
  - `executescript()`
  - `commit()`
  - `init_auth_db()`
  - `init_config_db()`
  - `seed_initial_config()`
  - `close()`
  - `execute()`

### Estado y Variables Globales
- Ninguna variable global, de sesión o de entorno quemada en el código.

### Dependencias y Flujo
- **Librerías Externas**:
  - `os`
  - `secrets`
  - `pathlib`
  - `sqlite3`
  - `unittest_mock`
  - `pytest`
  - `fastapi_testclient`
  - `config`
  - `app`
- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno mencionado.
- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno mencionado.

El flujo de datos es desde las funciones definidas en `conftest.py` hacia el resto del proyecto, proporcionando configuración y clientes de prueba necesarios para ejecutar pruebas.


---

## Archivo: ./graphify-out/cache/ast/418aaa07103f9a5817ee4bd7c1ea4ab84d1ad49d46b41118c661bd6e64189aa1.json

### Resumen Funcional
El archivo `test_cvalderrama.py` contiene una función de prueba llamada `test_query()` que realiza operaciones básicas en una base de datos SQLite.

### Catálogo de Funciones y Clases
- `test_query()` - Realiza consultas a la base de datos SQLite.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (operaciones directas sobre la conexión)
- **Columnas**: Ninguna (operaciones directas sobre la conexión)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: `sqlite3`
- **Archivos Importados por este Archivo**: Ninguno
- **Archivos que Importan a este Archivo**: Ninguno
- **Flujo de Datos**: El archivo importa el módulo `sqlite3` y realiza operaciones directas sobre la conexión a la base de datos SQLite.


---

## Archivo: ./graphify-out/cache/ast/41c6ecac133636d81ee103b15a4c36b1f085bba82765ec748007bd0682059258.json

### Resumen Funcional
El archivo `__init__.py` en la carpeta `scripts` es el punto de entrada para las funcionalidades relacionadas con el monitoreo del almacén. No contiene ninguna lógica específica, solo sirve como marcador de paquete.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna


---

## Archivo: ./graphify-out/cache/ast/4316fb8a7f251e010878cbae3e36cdce8ec23750ea17752236f4c23ea09e5b39.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `query_builder.py` contiene una función que compila un `VisualQueryBuilderPayload` validado en una tupla `(sql_text, bound_params)`. Esta función utiliza una sesión de SQLAlchemy para interactuar con la base de datos.

### Catálogo de Funciones y Clases
- **build_sql_from_payload(payload: VisualQueryBuilderPayload) -> Tuple[str, List[Any]]** - Compila un `VisualQueryBuilderPayload` validado en una tupla `(sql_text, bound_params)`.

### Interacción con Base de Datos
- **Motor:** SQLite
- **TABLAS:** Ninguna (el código no interactúa directamente con tablas de la base de datos).
- **COLUMNAS:** Ninguna (el código no interactúa directamente con columnas de la base de datos).

### Estado y Variables Globales
- **session:** Variable global que representa una sesión de SQLAlchemy.

### Dependencias y Flujo
- **Librerías Externas:**
  - `logging`
  - `typing`
  - `sqlalchemy.orm`
  - `sqlalchemy`
  - `fastapi`
  - `core_macros`
  - `core_query_validators`

- **Archivos del Proyecto que Importan a este Archivo (`query_builder.py`):** Ninguno.

- **Archivos del Proyecto que Este Archivo Importa:**
  - `core/macros`
  - `core/query_validators`

- **Flujo de Datos:** El archivo importa varias bibliotecas y módulos para su uso interno. La función `build_sql_from_payload` utiliza estos recursos para procesar el payload y generar la consulta SQL correspondiente.


---

## Archivo: ./graphify-out/cache/ast/4a08c549105832adb0358bb214615dadedbc01a9ad5d105e8ce6999f34f120a8.json

### Resumen Funcional
El archivo `models_transaccional.py` contiene definiciones de clases para diferentes entidades del sistema de monitoreo de almacén (WMS), utilizando SQLAlchemy como ORM.

### Catálogo de Funciones y Clases
- **WarehouseTask** - Representa una tarea en el almacén.
  - `__repr__()` - Devuelve una representación legible de la instancia.
- **InventoryMovement** - Representa un movimiento de inventario.
  - `__repr__()` - Devuelve una representación legible de la instancia.
- **OutboundDelivery** - Representa una entrega saliente.
  - `__repr__()` - Devuelve una representación legible de la instancia.
- **StockLevel** - Representa el nivel de stock.
  - `__repr__()` - Devuelve una representación legible de la instancia.
- **Lx02Pendiente** - Representa un pedido pendiente.
  - `__repr__()` - Devuelve una representación legible de la instancia.
- **SyncManifest** - Representa un manifiesto de sincronización.
  - No tiene métodos definidos en el fragmento.
- **AnalyticsSnapshot** - Representa una instantánea de análisis.
  - No tiene métodos definidos en el fragmento.
- **AutorAreaMapping** - Representa un mapeo de área autorizada.
  - No tiene métodos definidos en el fragmento.

### Interacción con Base de Datos
El archivo utiliza SQLAlchemy como ORM para interactuar con la base de datos. Las clases heredan de `Base`, lo que sugiere que están vinculadas a tablas en la base de datos SQLite. Sin embargo, no se proporciona información detallada sobre las columnas específicas o consultas SQL.

### Estado y Variables Globales
No hay variables globales, de sesión ni diccionarios quemados en el fragmento proporcionado.

### Dependencias y Flujo
- **Dependencias**: El archivo importa `typing`, `sqlalchemy`, `sqlalchemy_orm` y `core_database`.
- **Flujo**: 
  - `models_transaccional.py` depende de estos módulos.
  - No hay archivos que dependan directamente de este archivo.

Este fragmento muestra la definición de clases ORM para diferentes entidades del sistema WMS, utilizando SQLAlchemy como ORM y SQLite como motor de base de datos.


---

## Archivo: ./graphify-out/cache/ast/4d1f4a8e2b19730131b2fcce03e403741f4d454e7182dc23ff29de4aed1c34cb.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `routes/settings.py` contiene funciones y métodos relacionados con la gestión de configuraciones en un sistema de monitoreo de almacén (WMS). Incluye endpoints para obtener, actualizar y gestionar diferentes tipos de configuraciones como estados, costos centros, feriados y consultas.

### Catálogo de Funciones y Clases
- **invalidate_caches()** - Limpia el caché global en memoria y elimina todos los snapshots de base de datos.
- **SettingUpdate** - Modelo Pydantic para actualizar configuraciones.
- **StatusMappingUpdate** - Modelo Pydantic para actualizar mapeos de estados.
- **CostCenterMappingUpdate** - Modelo Pydantic para actualizar mapeos de costos centros.
- **HolidayAdd** - Modelo Pydantic para agregar feriados.
- **QueryUpdate** - Modelo Pydantic para actualizar consultas.
- **settings_view()** - Endpoint que renderiza el panel de control de configuraciones SaaS.
- **api_get_settings()** - Endpoint para obtener las configuraciones actuales.
- **api_update_setting()** - Endpoint para actualizar una configuración específica.
- **api_upsert_status()** - Endpoint para insertar o actualizar un estado.
- **api_delete_status()** - Endpoint para eliminar un estado.
- **api_upsert_cost_center()** - Endpoint para insertar o actualizar un mapeo de costos centros.
- **api_delete_cost_center()** - Endpoint para eliminar un mapeo de costos centros.
- **api_add_holiday()** - Endpoint para agregar un feriado.
- **api_sync_holidays()** - Endpoint para sincronizar automáticamente los feriados nacionales (Chile).
- **api_delete_holiday()** - Endpoint para eliminar un feriado.
- **api_get_query()** - Endpoint para obtener una consulta específica.
- **api_update_query()** - Endpoint para actualizar una consulta específica.
- **api_get_schema()** - Endpoint para obtener el esquema de datos para el editor.
- **api_preview_table()** - Endpoint para previsualizar una tabla.
- **api_query_preview()** - Endpoint para previsualizar los resultados de una consulta.
- **api_build_sql()** - Endpoint para compilar el estado visual del constructor en SQL parametrizado seguro.
- **api_export_missing_orders()** - Endpoint para exportar pedidos faltantes.

### Interacción con Base de Datos
El archivo interactúa con la base de datos SQLite a través de SQLAlchemy. Las tablas y columnas específicas no están detalladas, pero se pueden inferir desde los modelos Pydantic y las llamadas a ORM como `first()`, `query()`, `add()`, `delete()`.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno explícitas mencionadas en el código proporcionado.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `fastapi`
  - `pydantic`
  - `sqlalchemy_orm`
  - `core_auth`
  - `core_database`
  - `core_models`
  - `core_db_config_manager`
  - `core_app_instance`
  - `core_utils`
  - `core_state`
  - `core_query_engine`

- **Archivos Importados por este Archivo**:
  - No hay archivos importados directamente por este archivo.

- **Archivos que Importan a este Archivo**:
  - No hay archivos que importen directamente a este archivo.

- **Flujo de Datos**: 
  Los datos fluyen entre los endpoints y los modelos Pydantic, luego se procesan y persisten en la base de datos mediante SQLAlchemy.


---

## Archivo: ./graphify-out/cache/ast/4f9af946b1743e30eec64a351c630d05a8d09b09f18d70fea9fefd7957a923d5.json

### Resumen Funcional
El archivo `core/semantic_layer.py` contiene funciones y clases que definen la capa semántica del sistema de monitoreo de almacén (WMS). Esta capa se encarga de aislar el frontend del esquema físico, proporcionando una interfaz para obtener información sobre dimensiones, métricas y conjuntos de datos.

### Catálogo de Funciones y Clases
- `Dimension` - Representa una dimensión en el sistema.
- `Metric` - Representa una métrica en el sistema.
- `Dataset` - Representa un conjunto de datos en el sistema.
- `get_frontend_schema()` - Genera un diccionario semántico para exponer a la interfaz de usuario (UI).
- `resolve_dataset_physical_table(id)` - Devuelve la tabla física dado el ID del dataset.
- `resolve_physical_mapping(dim_area)` - Traduce un ID semántico a su columna física cualificada.
- `get_metric_formula(metric_id)` - Devuelve la fórmula compleja de una métrica si la tiene, inyectando la columna correspondiente.
- `get_formula_by_physical_table(table_name)` - Reverse-lookup: dado una tabla física y el nombre de una agregación compleja.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas SQL ni interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno quemadas en el código.

### Dependencias y Flujo
- **Dependencias**: Importa módulos `dataclasses` y `typing`.
- **Flujo de Datos**:
  - El archivo es importado por otros archivos (no se muestra aquí).
  - Se importa por `core/semantic_layer.py` desde los módulos `dataclasses` y `typing`.

Este archivo define la lógica semántica del sistema, proporcionando funciones para interactuar con dimensiones, métricas y conjuntos de datos, pero no realiza operaciones directas en una base de datos.


---

## Archivo: ./graphify-out/cache/ast/50bf0531bcf029b0fdca2f5044f64826d30fe1413fa37d63c7f98d186fb17959.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `deliveries.py` contiene la implementación de un repositorio para el dominio de Entregas (outbound_deliveries). Define métodos para obtener diferentes tipos de datos relacionados con las entregas, como umbrales SLA, auditorías SLA, entregas por lotes, áreas de entrega, elementos de recolección y gráficos de intensidad semanal.

### Catálogo de Funciones y Clases
- **DeliveriesRepository** - Repositorio para el dominio de Entregas.
  - `_sql()` - Obtiene SQL desde config_queries con fallback explícito.
  - `_get_sla_threshold()` - Obtiene el umbral SLA.
  - `get_sla_audit_records()` - Obtiene registros de auditoría SLA.
  - `get_deliveries_for_bulk()` - Obtiene entregas por lotes.
  - `get_area_lookup()` - Obtiene áreas de entrega.
  - `get_picking_items()` - Obtiene elementos de recolección.
  - `build_unified_where()` - Construye una cláusula WHERE unificada.
  - `get_filtered_transactions()` - Obtiene transacciones filtradas.
  - `get_filtered_kpis()` - Obtiene KPIs filtrados.
  - `get_delivery_by_id()` - Obtiene una entrega por su ID.
  - `get_weekly_intensity_chart()` - Obtiene el gráfico de intensidad semanal.
  - `get_dashboard_selectors()` - Obtiene selectores para el panel de control.

### Interacción con Base de Datos
- **Motor**: SQLite
- **TABLAS**:
  - No se especifican explícitamente las tablas, pero los métodos implican consultas a la base de datos.
- **COLUMNAS**:
  - No se especifican explícitamente las columnas, pero los métodos implican consultas a la base de datos.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno que almacenen estado crítico en este archivo.

### Dependencias y Flujo
- **Librerías Externas**:
  - `pandas`
  - `sqlalchemy`
  - `core_db_config_manager`
  - `users_christianykelly_desktop_monitorweb_repositories_base_py`
  - `core_macros`

- **Archivos del Proyecto que Importan a Este Archivo (lo consumen)**:
  - No se especifican explícitamente.

- **Flujo de Datos**:
  - El archivo importa varias librerías y dependencias necesarias para su funcionamiento.
  - Los métodos dentro de `DeliveriesRepository` realizan consultas a la base de datos utilizando SQLAlchemy, procesan los resultados con pandas y devuelven datos estructurados.


---

## Archivo: ./graphify-out/cache/ast/51c0d0497ae37e081bff0b6b5536227512cfebeffcd146d682d3558a59ec10c7.json

### Resumen Funcional
El archivo `tests/test_auth.py` contiene pruebas unitarias para el módulo de autenticación del sistema de monitoreo de almacén (WMS). Las pruebas cubren la funcionalidad de inicio de sesión, registro de usuarios y gestión de tokens JWT.

### Catálogo de Funciones y Clases
- `test_login_page_renders()` - Verifica que la página de login sea accesible.
- `test_login_success()` - Verifica login exitoso con credenciales del admin por defecto.
- `test_login_wrong_password()` - Verifica que credenciales incorrectas retornen 401.
- `test_me_endpoint_without_token()` - Verifica que `/me` sin token retorne 401.
- `test_me_endpoint_with_token()` - Verifica que `/me` con token válido retorne el perfil del usuario.
- `test_register_requires_admin()` - Verifica que registrar un usuario requiera token de admin.
- `test_register_and_login_new_user()` - Verifica el flujo completo: admin registra usuario → nuevo usuario hace login.
- `test_list_users_admin_only()` - Verifica que listar usuarios requiera rol admin.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: 
  - `pytest`
  - `fastapi_testclient`

- **Flujo de Datos**:
  - El archivo `tests/test_auth.py` importa `pytest` y `fastapi_testclient`.
  - Las funciones de prueba utilizan estos imports para realizar solicitudes HTTP a endpoints del sistema WMS.
  - No hay interacción directa con una base de datos en este archivo.


---

## Archivo: ./graphify-out/cache/ast/528131ed25a3e26cbf696584780a912857238297299edf194d464229f6254615.json

### Resumen Funcional
El archivo `main.py` es el punto de entrada oficial del sistema MonitorWeb Analyt. Configura e inicia los servicios de la plataforma.

### Catálogo de Funciones y Clases
- `start_application()` - Configura e inicia los servicios de la plataforma.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
**Librerías Externas:**
- `sys`
- `uvicorn`
- `logging`

**Archivos del Proyecto que Importan a este Archivo (`main.py`):**
- Ninguno

**Archivos del Proyecto que Este Archivo Importa (`main.py`):**
- `app`
- `config`
- `services_tunnel`

**Flujo de Datos:**
1. El archivo `main.py` importa las dependencias necesarias.
2. Llama a la función `start_application()`, que configura e inicia los servicios de la plataforma.
3. Utiliza métodos como `info`, `error`, `critical`, y `exit` para registrar información, errores y controlar el flujo del programa.

**Métodos Invocados:**
- `app.info(message)`
- `services_tunnel.start_tunnel()`
- `app.run()`
- `app.critical(message)`
- `app.exit()`
- `services_tunnel.stop_tunnel()`
- `app.error(message)`
- `app._exit()`


---

## Archivo: ./graphify-out/cache/ast/52d297b52b7fcb9c4fbf155602c2e074fd455e5d76ab62d4b336c6c656b28981.json

### Resumen Funcional
El archivo `inventory.py` contiene funciones relacionadas con el monitoreo de inventario en un sistema de gestión de almacenes (WMS). Define rutas y lógica para redirigir a las analíticas de inventario y obtener contexto de inventario.

### Catálogo de Funciones y Clases
- `analytics_inventory_redirect(request: Request, appstate: AppState)` - Redirige a las analíticas de inventario.
- `get_inventory_context(session: Session, item_id: str = None, context_type: Any = None)` - Obtiene el contexto del inventario para un ítem específico o todos los ítems.
- `analytics_inventory_api(session: Session, appstate: AppState)` - API JSON para analíticas de inventario.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
No se detectan variables globales o de sesión en el código proporcionado.

### Dependencias y Flujo
- **Librerías Externas**: `logging`, `sqlalchemy_orm`, `sqlalchemy`, `pandas`, `datetime`, `typing`, `fastapi`, `core_auth`, `fastapi_responses`, `core_database`, `core_schemas`, `core_state`, `core_wms_config`, `repositories`, `routes_analytics_proyecciones`, `core_utils`, `services_inventory_service`.
- **Archivos Importados**: El archivo importa varias clases y funciones de otros archivos dentro del proyecto.
- **Flujo de Datos**: El flujo de datos comienza en las rutas definidas, pasa por servicios y repositorios (si es necesario), y finalmente devuelve una respuesta al cliente.


---

## Archivo: ./graphify-out/cache/ast/54540c57687bae9117980cb18236f03ffd05937970c474132ebe2d03fe763092.json

### Resumen Funcional
El archivo `check_sla_queries.py` es un script que realiza consultas SLA (Service Level Agreement) en una base de datos SQLite.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna
- **Columnas**: Ninguna
- **Consultas SQL Crudas o Llamadas a ORM**: No hay consultas SQL crudas ni llamadas a ORM explícitas.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para procesar los resultados de las consultas en un formato tabular.
  - `json`: Para manejar el formato JSON.

- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno

**Flujo de Datos**: El script importa las bibliotecas necesarias y realiza consultas SLA en la base de datos SQLite, procesando los resultados con pandas y exportándolos en formato JSON.


---

## Archivo: ./graphify-out/cache/ast/54c706c5741a3b9d19d5418665fed07978bede460863afd005dbf2edd880b46b.json

### Resumen Funcional
El archivo `test_pdf.py` contiene pruebas unitarias para la generación de PDFs en un sistema de monitoreo de almacén (WMS). Las pruebas cubren la creación de instancias de PDF, la generación de códigos de barras y el dibujo de páginas de entrega.

### Catálogo de Funciones y Clases
- `pdf_instance()` - Crea una instancia de `WMS_Landscape_PDF`.
- `sample_header()` - Genera datos de cabecera de entrega ficticios.
- `sample_items()` - Genera un listado de materiales ficticios.
- `test_pdf_instantiation()` - Verifica que la clase PDF se instancie con la orientación Landscape y dimensiones correctas.
- `test_barcode_generation()` - Valida que la utilidad de códigos de barras produzca un stream binario válido.
- `test_get_ots_logic()` - Verifica la lógica de recuperación de OTs filtrando valores inválidos (0 o nulos).
- `test_draw_delivery_page_generates_content()` - Valida que el motor de dibujo escriba contenido binario en el buffer del PDF.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno quemadas en el código.

### Dependencias y Flujo
- **Dependencias Externas**: `pytest`, `pandas`, `io`, `sqlite3`, `typing`, `unittest_mock`, `core_pdf_engine`.
- **Archivos Importados por este Archivo**:
  - `tests/test_pdf.py` importa varios módulos y funciones.
- **Archivos que Importan a este Archivo**: No hay archivos que importen directamente a `test_pdf.py`.

El flujo de datos es principalmente entre las funciones de prueba y los métodos del objeto `WMS_Landscape_PDF`, así como la interacción con bibliotecas externas para generar PDFs y códigos de barras.


---

## Archivo: ./graphify-out/cache/ast/55169ca23a4786cca2c341a55744923258ccd63cada9f4477d1810e048705215.json

### Resumen Funcional
El archivo `check_areas.py` es un módulo que realiza operaciones relacionadas con el monitoreo de áreas en un sistema de almacén (WMS). Importa bibliotecas como `sqlite3` y `pandas` para interactuar con la base de datos y procesar los datos, respectivamente.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna (se supone que las operaciones se realizan a través de SQLAlchemy)
- Columnas: Ninguna (se supone que las operaciones se realizan a través de SQLAlchemy)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para procesar los datos.

- Archivos del proyecto que este archivo importa (consume): Ninguno
- Archivos del proyecto que importan a este archivo (lo consumen): Ninguno

El flujo de datos es directo, el módulo `check_areas.py` se encarga de realizar operaciones relacionadas con el monitoreo de áreas en el sistema de almacén.


---

## Archivo: ./graphify-out/cache/ast/56660310acc304b86472d8dd8bb0fbb599047df2c37ded7df1c612addb72d1f7.json

### Resumen Funcional
El archivo `test_lx02_pendientes.py` contiene una función de prueba que utiliza la biblioteca `pandas` para procesar un archivo Excel y extraer datos.

### Catálogo de Funciones y Clases
- `test_parse()` - Procesa un archivo Excel utilizando la clase `ExcelProcessor`.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: 
  - `sys`
  - `pandas`
  - `core_excel_processor` (importado como `ExcelProcessor`)
  
- **Flujo de Datos**:
  - El archivo importa las bibliotecas necesarias (`sys`, `pandas`, y `ExcelProcessor`).
  - La función `test_parse()` utiliza el método `process_file` de la clase `ExcelProcessor`.
  - Luego, se realizan operaciones como `tolist()`, `head()` en los datos procesados.


---

## Archivo: ./graphify-out/cache/ast/579446da8be16aaa260f86a2a3d843dc9368b5722f7414ce8393782e9ff62a44.json

### Resumen Funcional
El archivo `tunnel.py` contiene la implementación del servicio de túnel para el sistema de monitoreo de almacén (WMS). Este servicio permite iniciar y detener un túnel seguro y thread-safe.

### Catálogo de Funciones y Clases
- **NgrokService**
  - `__init__()`: Inicializa el servicio de túnel.
  - `_validate_bin()`: Valida la existencia y accesibilidad del binario del túnel.
  - `_save_url()`: Guarda la URL pública del túnel en un archivo.
  - `_get_public_url()`: Obtiene la URL pública del túnel desde una solicitud HTTP.
  - `start()`: Inicia el servicio de túnel de forma segura y thread-safe.
  - `stop()`: Detiene el servicio de túnel de forma segura y thread-safe.
  - `_run_loop()`: Ejecuta un bucle de ejecución para mantener el túnel activo.

- **start_tunnel()**: Función que inicia el servicio de túnel.
- **stop_tunnel()**: Función que detiene el servicio de túnel.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
**Librerías Externas:**
- `os`
- `subprocess`
- `threading`
- `time`
- `urllib.request`
- `json`
- `logging`

**Archivos del Proyecto que Importan a Este Archivo (lo consumen):**
Ninguno

**Este Archivo Importa a los siguientes Archivos del Proyecto:**
- `config`


---

## Archivo: ./graphify-out/cache/ast/5d34ccb8e2ec4e904045a3f6b9b0736b1497edf64f3e6550dc2de7016f75dd06.json

### Resumen Funcional
El archivo `check_schema.py` es un script que realiza operaciones relacionadas con la verificación del esquema de una base de datos SQLite.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna
- Columnas: Ninguna
- Consultas SQL Crudas o Llamadas a ORM: `import sqlite3`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías Externas: `sqlite3`
- Archivos del Proyecto que Importan a Este Archivo: Ninguno
- Archivos del Proyecto que Este Archivo Importa: Ninguno
- Dirección del Flujo de Datos: No aplica


---

## Archivo: ./graphify-out/cache/ast/5f2bf7aab62a6a6773f9e441fa2d333b037cc3c0941185a0ec3bed6ea28b7893.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `routes/filters.py` contiene funciones para filtrar transacciones y calcular KPIs en un sistema de monitoreo de almacén (WMS). Incluye endpoints para cargar datos asincrónicamente para el dashboard.

### Catálogo de Funciones y Clases
- `_build_unified_where()`
  - Propósito: Construye una cláusula WHERE unificada basada en múltiples criterios.
  
- `filter_transactions(request, session)`
  - Propósito: Filtra transacciones según los criterios proporcionados en la solicitud.

- `get_kpis(session)`
  - Propósito: Calcula KPIs dinámicos filtrados por área para el dashboard.

- `api_widget_data(request, session)`
  - Propósito: Endpoint de carga asincrónica para los componentes del Dashboard. Lee visual_s.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas y Columnas:
  - No se especifican columnas específicas en el fragmento proporcionado.
  
### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `logging`
  - `core_database`
  - `sqlalchemy_orm`
  - `sqlalchemy`
  - `datetime`
  - `typing`
  - `pandas`
  - `fastapi`
  - `config`
  - `core_models`
  - `core_query_engine`
  - `core_schemas`
  - `json`
  - `core_utils`
  - `repositories_deliveries`

- Archivos del proyecto que este archivo importa:
  - No se especifican archivos específicos en el fragmento proporcionado.

- Archivos del proyecto que importan a este archivo:
  - No se especifican archivos específicos en el fragmento proporcionado.


---

## Archivo: ./graphify-out/cache/ast/605433576c84cb4c894f851687548db973e1c020ee71f580177d67603ab99ceb.json

### Resumen Funcional
El archivo `inventory.py` contiene la implementación de un repositorio para el dominio de Movimientos de Inventario y Consumos. Define métodos para obtener consumos por centro de costo (`get_consumos_ceco`), materiales (`get_consumos_materiales`) y tendencias de material (`get_material_trend`). También incluye una verificación de la existencia de una tabla en la base de datos.

### Catálogo de Funciones y Clases
- `InventoryRepository()` - Repositorio para el dominio de Movimientos de Inventario y Consumos.
  - `.get_consumos_ceco(str centro_costo)` - Obtiene los consumos por centro de costo.
  - `.get_consumos_materiales(str material)` - Obtiene los consumos por material.
  - `.get_material_trend(str centro_costo, str material, str fecha_inicial, str fecha_final)` - Obtiene la tendencia de material.
  - `.check_table_exists()` - Verifica si una tabla existe en la base de datos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla `consumos`: Columnas (`id`, `centro_costo`, `material`, `fecha`, `cantidad`)
  - Tabla `materiales`: Columnas (`id`, `nombre`, `unidad_medida`, `stock_actual`)
  - Tabla `tendencias_material`: Columnas (`id`, `centro_costo`, `material`, `fecha`, `valor_trend`)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Dependencias Externas:**
  - `logging`
  - `pandas`
  - `sqlalchemy`
  - `datetime`

- **Archivos del Proyecto que Importan a Este Archivo (`inventory.py`):**
  - No hay dependencias directas.

- **Archivos del Proyecto que Este Archivo Importa:**
  - `base.py` (por lo menos, se importa en la definición de `InventoryRepository`)

- **Flujo de Datos:**
  - El archivo consume métodos y clases de SQLAlchemy para interactuar con la base de datos.
  - Utiliza pandas para procesar los resultados de las consultas SQL.
  - Los métodos devuelven datos procesados en formato de diccionario o lista.


---

## Archivo: ./graphify-out/cache/ast/606acc60977a4956c3b5059eac1d26eb0f46a1e367b4bef1a82a66dc1bab497c.json

### Resumen Funcional
El archivo `test_utils.py` contiene una función de prueba que verifica la seguridad e idempotencia del registro de manejadores de señales.

### Catálogo de Funciones y Clases
- `test_setup_signal_handlers_safety()` - Verifica que el registro de manejadores de señales sea seguro e idempotente.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: `pytest`, `core_utils`
- **Archivos Importados por este Archivo**: Ninguno
- **Archivos que Importan a este Archivo**: Ninguno
- **Flujo de Datos**: La función `test_setup_signal_handlers_safety()` llama al método `setup_signal_handlers` dos veces.

**Nota**: El archivo no interactúa con una base de datos ni utiliza variables globales.


---

## Archivo: ./graphify-out/cache/ast/6364b852f5601c620944dbdcb1a827fd2142e6c1d67b5808c8e721c459db32bb.json

### Resumen Funcional
El archivo `test_keys.py` es un módulo que importa bibliotecas necesarias para el sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite.

### Catálogo de Funciones y Clases
- Ninguna función o clase detectada directamente en este archivo.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna. El archivo no interactúa explícitamente con la base de datos a través de consultas SQL crudas o ORM.

### Estado y Variables Globales
- Ninguna variable global, de sesión, de entorno o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- **Librerías Externas**: `sqlite3`
- **Archivos del Proyecto que IMPORTA (consume)**: 
  - `routes_analytics_mb51`
  - `config`
- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno.
- **Dirección del Flujo de Datos**: El archivo `test_keys.py` importa bibliotecas y otros módulos, pero no realiza ninguna operación específica en la base de datos ni consume datos de otros archivos.


---

## Archivo: ./graphify-out/cache/ast/64976c195d2e4e4d9c04ae23fe4289d12f70e28e3e925bb3e8d719416d2fdac6.json

### Resumen Funcional
El archivo `compare_queries.py` contiene código que realiza comparaciones entre consultas SQL utilizando la biblioteca `sqlite3` para interactuar con una base de datos SQLite y la biblioteca `pandas` para manejar los resultados.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (se supone que las consultas son generadas dinámicamente)
- **Columnas**: Ninguna (se supone que las consultas son generadas dinámicamente)

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para manejar los resultados de las consultas SQL.

- **Archivos del Proyecto que Importan a Este Archivo**: Ninguno

- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno

- **Flujo de Datos**: El archivo importa `sqlite3` y `pandas`, realiza consultas SQL utilizando `sqlite3`, procesa los resultados con `pandas`, y no hay interacción directa con otros archivos del proyecto.


---

## Archivo: ./graphify-out/cache/ast/64d1f35fd94b79e06e1bbd905e2a0d47acc58f72b14287bd18394813e7d43721.json

### Resumen Funcional
El archivo `dynamic_executor.py` contiene una función que ejecuta consultas visuales a partir de un payload JSON crudo, valida y compila dicha consulta utilizando el motor SQLAlchemy.

### Catálogo de Funciones y Clases
- `execute_visual_query(session: Session) -> DataFrame` - Toma un payload JSON crudo desde el frontend, lo valida y compila usando el motor SQLAlchemy para ejecutar una consulta visual.

### Interacción con Base de Datos
- **Motor:** SQLite (implícito en la importación de SQLAlchemy).
- **Tablas y Columnas:** No se especifican explícitamente las tablas o columnas modificadas.
- **Consultas SQL Crudas:** La función `read_sql` es llamada, lo que implica que hay consultas SQL crudas.
- **ORM:** Se usa el ORM SQLAlchemy para la ejecución de consultas.

### Estado y Variables Globales
- Ninguna variable global o diccionario quemado en código que almacene estado crítico.

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `logging`
  - `typing`
  - `sqlalchemy.orm`
  - `core_query_engine`
  - `core_schemas`

- **Archivos del Proyecto que Importan a Este Archivo (lo consumen):** Ninguno.
- **Archivos del Proyecto que Este Archivo Importa (consume):**
  - `VisualQueryBuilderPayload` de `core_query_engine`
  - `build_sql_from_payload` de `core_query_engine`
  - `read_sql` y `connection` de `sqlalchemy.orm`

El flujo de datos es desde el frontend hacia este archivo, donde se recibe un payload JSON crudo, se valida y compila para ejecutar una consulta visual en la base de datos SQLite.


---

## Archivo: ./graphify-out/cache/ast/679e58595c2d5b0368fa9fcbe14b83d2400a592c09610b04a5d21a79fb43213a.json

### Resumen Funcional
El archivo `test_db_url.py` contiene una importación de la biblioteca `sqlalchemy`. No se proporciona ninguna otra información funcional.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: `sqlalchemy`
- **Flujo de datos**: El archivo importa la biblioteca `sqlalchemy` y no realiza ninguna otra operación relevante.


---

## Archivo: ./graphify-out/cache/ast/67c2b5bc142c856b40958f77b59dfb9d860d64db5c46a8c8aadf19f178bf8c18.json

### Resumen Funcional
El archivo `docs.py` contiene dos funciones principales: `get_docs_tree()` y `get_doc_content()`. La primera genera un árbol de archivos del proyecto indicando cuáles tienen documentación, mientras que la segunda obtiene el contenido de la documentación (.md) para un archivo específico.

### Catálogo de Funciones y Clases
- **`get_docs_tree(appstate: AppState)`** - Genera un árbol de archivos del proyecto indicando cuáles tienen documentación.
- **`get_doc_content(file_path: str, appstate: AppState)`** - Obtiene el contenido de la documentación (.md) para un archivo específico.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- **`appstate`** - Variable global que almacena el estado del sistema.

### Dependencias y Flujo
- **Dependencias Externas**: `os`, `fastapi`, `fastapi_responses`, `config`, `core_state`.
- **Archivos Importados por este Archivo**: Ninguno.
- **Archivos que Importan a este Archivo**: Ninguno.
- **Flujo de Datos**: El archivo importa varias bibliotecas y dependencias necesarias para su funcionamiento. La función `get_docs_tree` genera un árbol de archivos, mientras que la función `get_doc_content` lee el contenido de los archivos de documentación.

Este archivo es parte del módulo de rutas (`routes/docs.py`) en el sistema de monitoreo de almacén (WMS), y se utiliza para proporcionar endpoints para obtener información sobre la documentación del proyecto.


---

## Archivo: ./graphify-out/cache/ast/69d3b53515294f506e35991669de1dbbeb693294f1cff51d8694f65c2156c958.json

### Resumen Funcional
El archivo `check_all_columns.py` es un script que realiza operaciones relacionadas con la base de datos SQLite utilizando las bibliotecas `sqlite3` y `pandas`. Es probablemente parte del proceso de monitoreo de almacén (WMS) para verificar o manipular columnas en una tabla específica.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna especificada directamente
- **Columnas**: Ninguna especificada directamente
- **Consultas SQL Crudas o Llamadas a ORM**: No hay consultas SQL crudas ni llamadas a ORM explícitas en el fragmento proporcionado.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para manipular y analizar los datos obtenidos desde la base de datos.

- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno

- **Flujo de Datos**: El script importa las bibliotecas necesarias (`sqlite3` y `pandas`) y realiza operaciones relacionadas con la base de datos SQLite.


---

## Archivo: ./graphify-out/cache/ast/6d421f8f6df3e24a5c3ac5edc8b82c930b7691a09141da7d8b7970db44e636c0.json

### Resumen Funcional
El archivo `update_delivery_kpis.py` contiene código que realiza operaciones relacionadas con la actualización de indicadores clave del desempeño (KPIs) en el sistema de monitoreo de almacén.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite3
- **Tablas**: Ninguna
- **Columnas**: Ninguna
- **Consultas SQL Crudas o Llamadas a ORM**: No hay consultas SQL crudas ni llamadas a ORM explícitas.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Importada para interactuar con la base de datos SQLite.
  - `json`: Importada para manejar operaciones JSON.

- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno

- **Flujo de Datos**: El archivo importa las bibliotecas necesarias y no realiza ninguna interacción con la base de datos ni utiliza variables globales.


---

## Archivo: ./graphify-out/cache/ast/6dfcee190fc10c7da27c737a07a3f32ce1808c761b59957099ffb5047771d609.json (Procesado en 1 partes)


---

## Archivo: ./graphify-out/cache/ast/6e0e4b95bfba32918c0d480d8eeb265ad44cedcb8792ba390c8cfc9f828c87dd.json

### Resumen Funcional
El archivo `routes/productivity.py` contiene funciones que manejan diferentes aspectos del monitoreo de productividad en el sistema WMS. Estas funciones interactúan con servicios y repositorios para obtener datos y devolver respuestas al cliente.

### Catálogo de Funciones y Clases
- **get_available_dates()** - Retorna las fechas disponibles para el dashboard de productividad.
- **get_productivity_dashboard()** - Retorna los datos necesarios para el dashboard de productividad MB51.
- **get_monthly_productivity()** - Retorna los KPIs mensuales de productividad.
- **get_user_movements_summary()** - Retorna un resumen de movimientos del usuario.
- **get_user_movements_details()** - Retorna los detalles de los movimientos del usuario.
- **get_user_movements_monthly_summary()** - Retorna un resumen mensual de los movimientos del usuario.
- **get_user_movements_monthly_details()** - Retorna los detalles mensuales de los movimientos del usuario.

### Interacción con Base de Datos
No se especifican consultas SQL crudas o llamadas a ORM en este archivo. La interacción con la base de datos ocurre a través de servicios (`ProductivityDailyService` y `ProductivityMonthlyService`) que probablemente interactúen con los repositorios para acceder a los datos.

### Estado y Variables Globales
No se detectan variables globales, de sesión o de entorno en este archivo. Todas las referencias a estado crítico son parámetros de funciones.

### Dependencias y Flujo
- **Dependencias**: El archivo importa varias bibliotecas como `fastapi`, `sqlalchemy_orm`, `datetime`, entre otras, además de módulos internos del proyecto como `services_productivity_daily`, `services_productivity_monthly`, etc.
- **Flujo de Datos**: Los datos fluyen desde las funciones hacia los servicios y luego a través de estos hacia la base de datos. Las respuestas generadas por los servicios son devueltas al cliente a través de las funciones correspondientes.

Este archivo es una parte integral del sistema WMS, encargado de proporcionar endpoints para obtener diferentes tipos de datos relacionados con el monitoreo de productividad.


---

## Archivo: ./graphify-out/cache/ast/6f2a1f48352150b25fb5208ea7642620e72a91650ae759141dd1d53c645967ce.json

### Resumen Funcional
El archivo `tasks_service.py` contiene la lógica de negocio para el servicio de tareas en un sistema de monitoreo de almacén (WMS). Define una clase `TasksService` que proporciona métodos para obtener contexto analítico y resúmenes de tareas.

### Catálogo de Funciones y Clases
- **Clase:** `TasksService`
  - **Método:** `__init__(self, session: Session)`
    - **Propósito:** Inicializa una instancia de la clase con una sesión de base de datos.
  - **Método:** `get_full_context(self)`
    - **Propósito:** Genera y cachea el contexto analítico para la gestión de OTs.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - No se especifican columnas específicas, pero se hacen llamadas a métodos que implican consultas SQL (como `read_sql`, `execute`, `fetchone`).

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `sqlalchemy`
  - `pandas`
  - `logging`
  - `datetime`
  - `core_state`
  - `core_utils`
- **Archivos del Proyecto que Importan a Este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:**
  - `repositories`
  - `services_tasks_service_tasksservice`

El flujo de datos fluye desde la clase `TasksService` hacia los métodos y clases importadas, realizando operaciones como consultas a la base de datos, manipulación de datos con pandas, y registro de eventos con logging.


---

## Archivo: ./graphify-out/cache/ast/7c1b07c1b5126af3d9afe045d2ae833f779037728df9b890cd6f9b25e5f309d3.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `pdf_engine.py` contiene una clase base para reportes WMS en formato horizontal (`WMS_Landscape_PDF`) que genera PDFs utilizando la biblioteca FPDF. La clase incluye métodos para calcular posiciones de columnas, dibujar líneas punteadas, obtener OTs asociadas a entregas, generar códigos de barras y dibujar páginas de entrega con encabezados, bloques de información y tablas.

### Catálogo de Funciones y Clases
- **WMS_Landscape_PDF** - Clase base para reportes WMS en formato horizontal.
  - `__init__()`
  - `get_column_x(column: int) -> float` - Calcula la posición X de una columna específica.
  - `draw_dotted_line(x1: float, y1: float, x2: float, y2: float)`
  - `_generate_barcode_stream(barcode_data: str) -> bytesio.BytesIO`
  - `draw_delivery_page(delivery_info: pandas.Series, items_df: pandas.DataFrame, is_printed: bool, delivery_id: str)`
  - `_draw_page_header(delivery_info: pandas.Series, is_printed: bool)`
  - `_draw_info_block(delivery_info: pandas.Series)`
  - `_draw_table(items_df: pandas.DataFrame)`
  - `_draw_ot_barcodes(ots_list: list)`
  - `_draw_signature_block()`

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas y Columnas**:
  - `get_ots_for_delivery(delivery_id: str, connection: sqlite3.Connection) -> list[str]` - Consulta las OTs asociadas a una entrega y las devuelve como lista de strings.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `io`
  - `logging`
  - `sqlite3`
  - `datetime`
  - `typing`
  - `pathlib`
  - `numpy`
  - `pandas`
  - `fpdf`
  - `barcode`
  - `barcode_writer`
  - `config`

- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno


---

## Archivo: ./graphify-out/cache/ast/7c24e25851b398265dcba13704cc879b0317b685504e0376e17857c68897014b.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `db_enrichment.py` contiene funciones que realizan el enriquecimiento de datos en una base de datos SQLite. Estas funciones incluyen la rellena de columnas vacías en Entregas, el aprendizaje del mapeo de frecuencia Autor -> Área, la asignación de áreas de negocio a transacciones 'OTRO', y la enriquecimiento de transacciones con descripciones y ubicaciones físicas de Stock.

### Catálogo de Funciones y Clases
- `backfill_deliveries_from_movements(connection: str)`: Rellena columnas vacías en Entregas cruzando con Movi.
- `learn_author_areas(connection: str)`: Actualiza el mapeo de frecuencia Autor -> Área.
- `apply_author_learning(connection: str)`: Asigna áreas de negocio a transacciones 'OTRO' basadas en la memoria del autor.
- `enrich_deliveries_with_stock(connection: str)`: Enriquece transacciones con descripciones y ubicaciones físicas de Stock.
- `backfill_material_texts(connection: str)`: Rellena descripciones y UMBs faltantes en Entregas usando Stock y Movimientos coincidentes.
- `update_sla_with_tasks(connection: str)`: Actualiza la métrica de SLA en outbound_deliveries cruzando con la fecha de confirmación de tareas.
- `enrich_movements_with_iw39(connection: str)`: Enriquece la tabla inventory_movements con ceco_resp y autor provenientes de iw39.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQLite. Las tablas y columnas específicas no están detalladas en el fragmento proporcionado, pero se infiere que las funciones manipulan varias tablas relacionadas con entregas, movimientos, materiales y SLA.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno explícitamente mencionadas en el fragmento proporcionado.

### Dependencias y Flujo
- **Dependencias**: El archivo importa módulos como `logging`, `pandas`, `sqlite3` y `typing`.
- **Flujo de Datos**: El flujo de datos fluye desde las funciones hacia la base de datos, realizando operaciones de lectura (`read_sql`), escritura (`to_sql`) y actualización (`execute`). Las funciones también utilizan métodos de pandas para manipular los datos en memoria antes de escribirlos a la base de datos.


---

## Archivo: ./graphify-out/cache/ast/7d29a7d52d8c76e8bde35a684b01606b4d7d06822471efe988accc1694bc168a.json

### Resumen Funcional
Este archivo `database.py` contiene la configuración y funcionalidades relacionadas con la base de datos para el sistema de monitoreo de almacén (WMS). Define una clase base para los modelos ORM, funciones para obtener sesiones de base de datos y verificar su conectividad.

### Catálogo de Funciones y Clases
- `Base` - Clase base para todos los modelos ORM del sistema.
- `get_session()` - Context manager que entrega una sesión SQLAlchemy. Garantiza commit en éxito o rollback en fallo.
- `get_session_dep()` - Dependencia de FastAPI (Depends) para inyección de sesiones en endpoints.
- `health_check()` - Verifica la conectividad con la base de datos. Retorna True si OK.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: No especificadas explícitamente en el fragmento, pero se asume que interactúa con tablas definidas en los modelos ORM heredados de `Base`.
- Consultas SQL Crudas o Llamadas a ORM:
  - `SessionLocal`
  - `commit`, `rollback`, `close` (métodos de la sesión SQLAlchemy)
  - `connect`, `execute`, `text` (métodos del motor de base de datos)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Importa módulos como `os`, `logging`, `contextlib`, `typing`, `sqlalchemy`, `sqlalchemy_orm`, y `config`.
- Es importado por otros archivos del proyecto.
- Importa a otros archivos del proyecto (`core/database.py`).

Flujo de datos:
1. `database.py` se importa en otros archivos.
2. Se utilizan las funciones y clases definidas aquí para gestionar sesiones de base de datos y verificar conectividad.

Este archivo es fundamental para la capa de acceso a datos del sistema WMS, proporcionando una interfaz consistente para interactuar con la base de datos utilizando SQLAlchemy ORM.


---

## Archivo: ./graphify-out/cache/ast/80bfa4e4aa3f17049ec4ee2bcb50e1357fffb19d641addd30d60b5391501dc7e.json

### Resumen Funcional
El archivo `utils.py` contiene funciones utilitarias transversales y gestiòn de señales del sistema.

### Catálogo de Funciones y Clases
- `setup_signal_handlers()` - Configura los manejadores de señales (SIGINT, SIGTERM) para un cierre limpio.
- `log_startup_banner()` - Limpia datos para serialización JSON segura de forma recursiva y exhaustiva.
- `_get_bound_params_from_visual_state(state: str)` - Alias de compatibilidad → core/query_engine.get_bound_params_from_visual_state.
- `_extract_metric_value(metric_name: str)` - Alias de compatibilidad → core/query_engine.extract_metric_value.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: `signal`, `sys`, `logging`, `pandas`, `math`, `typing`
- **Archivos Importados por Este Archivo**:
  - No aplica.
- **Archivos que Importan a Este Archivo**:
  - No aplica.


---

## Archivo: ./graphify-out/cache/ast/82920e8133c919d6df598a58e34c44803ba5a97e6e3451d30140393c627f67cb.json

### Resumen Funcional
El archivo `check_months.py` es un script que realiza operaciones relacionadas con los meses, probablemente para el monitoreo de almacén (WMS). No contiene ninguna interacción explícita con la base de datos.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada en este fragmento.

### Interacción con Base de Datos
Ninguna. El archivo no realiza ninguna operación relacionada con la base de datos.

### Estado y Variables Globales
Ninguna variable global, de sesión o de entorno detectada en este fragmento.

### Dependencias y Flujo
- **Librerías externas**: `sqlite3`, `pandas`
- **Archivos del proyecto que IMPORTAN a este archivo**: Ninguno.
- **Archivos del proyecto que este archivo IMPORTA**: Ninguno.
- **Dirección del flujo de datos**: No aplica, ya que no hay funciones ni interacciones con la base de datos.


---

## Archivo: ./graphify-out/cache/ast/878b63f8b93c007822c5a2e02560fcef0eb1964373ab0ecef269bacc46a32916.json

### Resumen Funcional
El archivo `check_specific_deliveries.py` es un script que realiza operaciones relacionadas con el monitoreo de entregas en un sistema de almacén (WMS). Importa módulos para interactuar con una base de datos SQLite y pandas para manejar los datos.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna especificada
- **Columnas**: Ninguna especificada
- **Consultas SQL Crudas o Llamadas a ORM**: Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para manejar los datos.

- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno

- **Dirección del Flujo de Datos**:
  - El script importa las bibliotecas necesarias (`sqlite3` y `pandas`) para su ejecución.


---

## Archivo: ./graphify-out/cache/ast/8c8245b9595242aafc411b8d79cf57ce89c705230a7d38f0636a18ca562078d3.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `db_config_manager.py` es el administrador de configuraciones dinámicas SaaS. Crea las tablas de configuración SaaS via SQLAlchemy si no existen, inserta los valores por defecto si las tablas están vacías y proporciona métodos para recuperar configuraciones específicas.

### Catálogo de Funciones y Clases
- `init_config_db()` - Crea las tablas de configuración SaaS via SQLAlchemy si no existen.
- `seed_initial_config()` - Inserta los valores por defecto si las tablas están vacías.
- `load_config_to_memory()` - Carga la configuración a memoria.
- `_ensure_loaded()` - Método auxiliar para asegurar que la configuración esté cargada.
- `get_setting(setting_name: str) -> Any` - Recupera un valor de configuración específico.
- `get_status_mapping() -> Dict[str, str]` - Obtiene el mapeo de estados.
- `get_cost_center_mapping() -> Dict[str, str]` - Obtiene el mapeo de centros de costo.
- `get_holidays() -> List[Holiday]` - Obtiene los días festivos.
- `get_query_visual_state(query_id: str) -> str` - Recupera el visual_state JSON de una query.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `StatusMapping`
  - `CostCenterMapping`
  - `AppSetting`
  - `Holiday`
  - `ConfigQuery`
- Columnas (ejemplos):
  - `StatusMapping.id`, `StatusMapping.status_code`, `StatusMapping.description`
  - `CostCenterMapping.id`, `CostCenterMapping.cost_center_id`, `CostCenterMapping.description`
  - `AppSetting.id`, `AppSetting.setting_name`, `AppSetting.value`
  - `Holiday.id`, `Holiday.date`, `Holiday.description`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- Importa módulos como `logging`, `typing`, `sqlalchemy`, `sqlalchemy_orm`.
- Importa clases de otros archivos (`core/database.py`, `core/models.py`).
- Llama a métodos de ORM SQLAlchemy para interactuar con la base de datos.
- El flujo de datos fluye desde las funciones hacia el acceso a la base de datos y viceversa.


---

## Archivo: ./graphify-out/cache/ast/8e72c3a774307053c0b3e684d686c4ffa3e35ec2829bda3808d54e73f4ae237b.json

### Resumen Funcional
El archivo `analyze_html.py` contiene una función que analiza grandes archivos HTML utilizando la biblioteca `httpx` para hacer solicitudes HTTP y la biblioteca `re` para realizar búsquedas regulares.

### Catálogo de Funciones y Clases
- **analyze_large_html()** - Analiza grandes archivos HTML.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: `asyncio`, `httpx`, `sys`, `os`, `re`.
- **Archivos Importados por Este Archivo**:
  - Ninguno.
- **Archivos que Importan a Este Archivo**:
  - Ninguno.

El flujo de datos es simple: el archivo importa las bibliotecas necesarias y luego define la función `analyze_large_html()`, que realiza operaciones como hacer solicitudes HTTP, buscar patrones regulares en HTML y manipular listas.


---

## Archivo: ./graphify-out/cache/ast/8ee89e2bc21b701c250548368014f8ee524164b6d75123d28e1b343765391765.json

### Resumen Funcional
El archivo `test_preview_api.py` contiene pruebas unitarias para el sistema de monitoreo de almacén (WMS) utilizando FastAPI y SQLAlchemy.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `sys`, `json`
- **Archivos Importados por Este Archivo**:
  - `fastapi_testclient` (desde `main`)
- **Archivos que Importan a Este Archivo**: Ninguno

El archivo `test_preview_api.py` importa módulos necesarios para ejecutar pruebas unitarias en el sistema WMS, pero no realiza ninguna interacción con la base de datos ni utiliza variables globales.


---

## Archivo: ./graphify-out/cache/ast/9099043b37b2cb80a4ed1c0a1592141cf95c6ce604f6cb220061cf4ef93ec8db.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `routes/deliveries.py` contiene funciones relacionadas con el manejo de entregas en un sistema de monitoreo de almacén (WMS). Incluye rutas para guardar y cargar capturas de análisis, renderizar páginas de análisis, obtener detalles de auditoría SLA y proporcionar una API JSON para analíticas de entregas.

### Catálogo de Funciones y Clases
- `save_analytics_snapshot(session: Session, data: str) -> None`: Guarda una captura de las analíticas en la base de datos.
- `load_analytics_snapshot(session: Session, snapshot_id: str) -> Any`: Recupera la última captura de analíticas desde la base de datos.
- `analytics(request: Request, session: Session, appstate: AppState) -> TemplateResponse`: Renderiza la página principal de analíticas con caché multinivel (Memoria -> DB).
- `sla_details(request: Request, session: Session, year: str, month: str, day: str) -> TemplateResponse`: Vista detallada de auditoría SLA.
- `get_non_palletized_details(session: Session, warehouse_id: str) -> Any`: Obtiene el listado detallado (hasta 200) de movimientos no paletizados para un almacén específico.
- `analytics_deliveries_api(session: Session, appstate: AppState) -> AnalyticsDeliveriesResponse`: API JSON para analíticas de Entregas (Outbound Deliveries).

### Interacción con Base de Datos
- **Motor**: SQLite
- **TABLAS**:
  - No se especifican tablas explícitas en el código proporcionado.
- **COLUMNAS**:
  - No se especifican columnas explícitas en el código proporcionado.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `logging`, `sqlite3`, `pandas`, `json`, `datetime`, `typing`, `sqlalchemy`, `fastapi`, `fastapi_responses`
- **Archivos del Proyecto que Importan a este Archivo**:
  - No se especifican archivos que importen a este archivo.
- **Archivos del Proyecto que Este Archivo Importa**:
  - `core_database`
  - `sqlalchemy_orm`
  - `core_state`
  - `core_app_instance`
  - `core_schemas`
  - `repositories`
  - `routes_inventory`
  - `routes_tasks`
  - `routes_analytics_proyecciones`
  - `core_auth`
  - `core_utils`
  - `services_deliveries_service`
- **Flujo de Datos**: El archivo importa varias bibliotecas y módulos del proyecto, incluyendo servicios y repositorios para interactuar con la base de datos y lógica de negocio. Las funciones realizan operaciones como guardar y cargar capturas de análisis, renderizar páginas web y proporcionar APIs JSON.

Este archivo es crucial para el manejo de analíticas y detalles de entregas en el sistema WMS, utilizando una arquitectura basada en servicios y repositorios para mantener la separación de preocupaciones.


---

## Archivo: ./graphify-out/cache/ast/91f75411b1f3fc186d09119761d6cc0975acdde32a9ee05b709cb2b680b3f273.json

### Resumen Funcional
Clase base para todos los repositorios de datos en el sistema de monitoreo de almacén (WMS). Proporciona métodos para interactuar con la base de datos y verificar el estado visual de las consultas.

### Catálogo de Funciones y Clases
- `BaseRepository(session: Session)` - Constructor que recibe una sesión de SQLAlchemy.
- `._sql(sql_text: str) -> str` - Método privado que devuelve el texto SQL proporcionado como parámetro.
- `._has_visual_state(query: str) -> bool` - Método privado que verifica si la consulta tiene un estado visual JSON almacenado.

### Interacción con Base de Datos
- Motor de BD: SQLite (implícito en SQLAlchemy).
- Tablas y Columnas: No especificadas explícitamente.
- Consultas SQL Crudas: Sí, se utiliza el parámetro `sql_text` en el método `_sql`.
- ORM: Sí, se usa la sesión de SQLAlchemy (`Session`) para interactuar con la base de datos.

### Estado y Variables Globales
- No hay variables globales o de sesión definidas explícitamente.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `sqlalchemy_orm` (importado desde `repositories/base.py`)
  - `core_db_config_manager` (importado desde `repositories/base.py`)
- **Flujo de Datos**:
  - El archivo `base.py` importa dependencias necesarias y define la clase `BaseRepository`.
  - La clase `BaseRepository` contiene métodos para interactuar con la base de datos.
  - El método `_sql` recibe un texto SQL como parámetro y lo devuelve.
  - El método `_has_visual_state` verifica si una consulta tiene un estado visual JSON almacenado.

### Rationale
- Clase base para todos los repositorios de datos.
- Devuelve el fallback hardcodeado. (Fase 4 completada: sql_text ha sido eliminado).
- Retorna True si la query tiene un visual_state JSON almacenado.


---

## Archivo: ./graphify-out/cache/ast/9224144950785d5e538d3808d62b08a9f059284c033c2cfd955413c9ff65a564.json

### Resumen Funcional
El archivo `test_pipeline.py` contiene pruebas unitarias para el módulo de consolidación de datos en un sistema de monitoreo de almacén (WMS). Las pruebas cubren la funcionalidad de análisis de fechas, validación de seguridad de tablas y lógica de sobrescritura con los archivos más recientes.

### Catálogo de Funciones y Clases
- `consolidator()` - No se proporciona una descripción detallada.
- `test_parse_file_date()` - Verifica que el parsing de fechas sea correcto.
- `test_validate_table_security()` - Verifica la protección contra nombres de tabla no permitidos.
- `test_overwrite_with_latest_logic()` - Verifica que se tome el archivo más reciente para sobrescribir.

### Interacción con Base de Datos
No hay consultas SQL crudas o llamadas a ORM explícitas en este archivo. La interacción con la base de datos ocurre dentro del método `test_overwrite_with_latest_logic()`, donde se utiliza SQLAlchemy para ejecutar consultas y obtener resultados.

- **TABLAS**: Ninguna específica mencionada.
- **COLUMNAS**: Ninguna específica mencionada.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno que almacenen estado crítico en este archivo.

### Dependencias y Flujo
- **Librerías Externas**:
  - `pytest`
  - `pathlib`
  - `datetime`
  - `pandas`
  - `db_consolidator`

- **Archivos del Proyecto que IMPORTAN a Este Archivo**: Ninguno.
- **Archivos del Proyecto que ESTE ARCHIVO IMPORTA**: Ninguno.

**Flujo de Datos**: El archivo importa varias bibliotecas y módulos, incluyendo `pytest` para pruebas unitarias, `pathlib` para manejo de rutas de archivos, `datetime` para operaciones con fechas, `pandas` para manipulación de datos tabulares, y `db_consolidator` para la lógica de consolidación de datos. Las funciones de prueba utilizan estos módulos para realizar sus respectivas tareas de análisis, validación y sobrescritura de datos.


---

## Archivo: ./graphify-out/cache/ast/92831e8dc24ad42b677abae249e3eadd21d6a1a31e22e210b750e340c3314a08.json

### Resumen Funcional
El archivo `package.json` del proyecto de WMS contiene la configuración y dependencias necesarias para el desarrollo y ejecución del sistema.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: `puppeteer`
- **Flujo de datos**: El archivo `package.json` importa la dependencia `puppeteer`.


---

## Archivo: ./graphify-out/cache/ast/92b6fc5c26b266056ec4bb1504831d2d8ae4387779cca708b63e376bfbbfabc7.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `tasks.py` contiene la implementación de un repositorio para el dominio de Warehouse Tasks e interacciones de usuario. Define métodos para obtener resúmenes diarios, horarios, inactividades, mapas térmicos y movimientos de usuarios.

### Catálogo de Funciones y Clases
- **TasksRepository** - Repositorio que hereda de `BaseRepository` y contiene métodos para interactuar con la base de datos.
  - `.get_available_dates()`
  - `_get_daily_summary()`
  - `_get_hourly_trend()`
  - `_get_inactivity_gaps()`
  - `_get_activity_heatmap()`
  - `.get_user_movements_daily_summary()`
  - `.get_user_movements_daily_details()`
  - `_get_monthly_summary()`
  - `_get_monthly_shifts()`
  - `_get_monthly_heatmap()`
  - `.get_user_movements_monthly_summary()`
  - `.get_user_movements_monthly_details()`
  - `.get_tasks_summary()`
  - `.get_tasks_trend()`
  - `.get_tasks_by_user()`
  - `.get_tasks_by_type_dest()`
  - `.get_recent_tasks()`
  - `.get_non_palletized_movements()`
  - `.get_non_palletized_count()`
  - `.get_non_palletized_summary()`

### Interacción con Base de Datos
- **Motor**: SQLite
- **TABLAS**:
  - No se especifican explícitamente las tablas, pero los métodos interactúan con la base de datos para obtener y manipular datos.
- **COLUMNAS**:
  - No se especifican explícitamente las columnas, pero los métodos utilizan consultas SQL que implican varias columnas.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno mencionadas en el código proporcionado.

### Dependencias y Flujo
- **Librerías Externas**:
  - `logging`
  - `pandas`
  - `sqlalchemy`
- **Archivos del Proyecto que Importan a Este Archivo (lo consumen)**:
  - No se especifican archivos que importen directamente este archivo.
- **Flujo de Datos**: El flujo de datos fluye desde los métodos del repositorio hacia la base de datos para leer y escribir datos, y luego hacia el servicio o controlador que lo consume.


---

## Archivo: ./graphify-out/cache/ast/9742e8f505e0c6e7a22bee3c481e6f2e2b8bf062a4d24b2f148900af3ef72162.json

### Resumen Funcional
El archivo `check_query.py` es un script que realiza consultas a una base de datos SQLite y procesa los resultados utilizando la biblioteca pandas.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (se supone que las tablas se especifican en el código no proporcionado)
- **Columnas**: Ninguna (se supone que las columnas se especifican en el código no proporcionado)

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para procesar los resultados de las consultas.
  - `sys` y `os`: Para operaciones del sistema y manejo de archivos, respectivamente.
- **Archivos Importados por Este Archivo**:
  - Ninguno
- **Archivos que Importan a Este Archivo**:
  - Ninguno

El flujo de datos es simple: el script importa las bibliotecas necesarias, realiza consultas a la base de datos SQLite utilizando `sqlite3`, procesa los resultados con pandas, y no interactúa directamente con otros archivos o servicios dentro del proyecto.


---

## Archivo: ./graphify-out/cache/ast/9799d9fa4c3ad9179fe69a77d84f0f273a805fc4cec4422fecc5f41d59145002.json

### Resumen Funcional
El archivo `config.py` contiene funciones para validar la configuración del sistema y asegurar la estructura del proyecto.

### Catálogo de Funciones y Clases
- `validate_config()` - Realiza comprobaciones de salud en la configuración.
- `ensure_project_structure()` - Crea los directorios necesarios para el funcionamiento de la app si no existen.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `os`, `logging`, `typing`, `pathlib`
- **Archivos Importados por este Archivo**:
  - Ninguno
- **Archivos que Importan a este Archivo**:
  - Ninguno


---

## Archivo: ./graphify-out/cache/ast/97a6f6a5225f6f3647cb58765f640cbc92e9013f91f47cf90f44b0e4fa3db713.json

### Resumen Funcional
El archivo `test_mock.py` contiene una función de prueba que utiliza SQLite y el módulo `unittest.mock` para realizar pruebas unitarias.

### Catálogo de Funciones y Clases
- `test_mock()` - Breve propósito: Realiza pruebas unitarias utilizando SQLite y el módulo `unittest.mock`.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna
- Columnas: Ninguna
- Consultas SQL crudas o llamadas a ORM: 
  - `connect()` - Se llama tres veces en la función `test_mock()`.
  - `patch()` - Se llama una vez en la función `test_mock()`.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `sqlite3`
  - `unittest.mock`

- Archivos del proyecto que este archivo importa (consume):
  - Ninguno

- Archivos del proyecto que importan a este archivo (lo consumen):
  - Ninguno

- Dirección del flujo de datos: El archivo `test_mock.py` importa `sqlite3` y `unittest.mock`, luego realiza pruebas unitarias utilizando estos módulos.


---

## Archivo: ./graphify-out/cache/ast/99ebae81be068909bb52edbc099a6f0a7f09032c9131533d852998675cae5290.json

### Resumen Funcional
El archivo `print_query_details.py` contiene código que realiza una consulta a la base de datos SQLite y luego imprime los detalles de esa consulta.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna (La consulta SQL está directamente en el código)
- Columnas: Ninguna (La consulta SQL está directamente en el código)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas: `sqlite3`
- Archivos del proyecto que importan a este archivo: Ninguno
- Archivos del proyecto que este archivo importa: Ninguno
- Flujo de datos: El archivo importa la librería `sqlite3` para realizar una consulta SQL y luego imprime los detalles de esa consulta.


---

## Archivo: ./graphify-out/cache/ast/9b7ac37b72b0e2c41d7ee6a023049a35a1b760ad5d471a5f7953e86dc517d01a.json

### Resumen Funcional
El archivo `query_engine.py` es un módulo que actúa como una fachada para el motor de SQL, proporcionando una interfaz simplificada y segura para realizar consultas en la base de datos.

### Catálogo de Funciones y Clases
- **Ninguna**

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (El archivo no contiene consultas SQL directas ni llamadas a ORM)
- **Columnas**: Ninguna

### Estado y Variables Globales
- **Ninguna**

### Dependencias y Flujo
- **Librerías Externas**:
  - `core_query_validators`
  - `core_query_utils`
  - `core_query_builder`

- **Archivos del Proyecto que Importan a Este Archivo**: Ninguno

- **Archivos del Proyecto que Este Archivo Importa**: Ninguno

- **Flujo de Datos**: El archivo importa módulos auxiliares (`core_query_validators`, `core_query_utils`, `core_query_builder`) para proporcionar una interfaz simplificada y segura para realizar consultas en la base de datos.


---

## Archivo: ./graphify-out/cache/ast/9bf240441d5ca7bf44b13f9124b4aaed34347ec728b50eceb36090792cf5ab21.json

### Resumen Funcional
El archivo `run_tests.sh` es un script de Bash que se ejecuta para correr pruebas en el sistema de monitoreo de almacén (WMS). Este script está ubicado en la carpeta `setup`.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías externas**: No se mencionan librerías externas específicas.
- **Archivos del proyecto que IMPORTA a este archivo (lo consumen)**: Ninguno
- **Archivos del proyecto que ESTE archivo IMPORTA (consume)**: Ninguno

El flujo de datos es simple, ya que el script `run_tests.sh` no depende de ninguna otra función o clase dentro del proyecto.


---

## Archivo: ./graphify-out/cache/ast/9bf25396ed6731406f1f2edfa1a977d07569eeb7d272b8f85a87b9be65e8e09a.json

### Resumen Funcional
El archivo `test_sla_monthly_compiled.py` es un script que realiza operaciones de monitoreo y análisis en un sistema de almacén (WMS) utilizando FastAPI, SQLAlchemy y SQLite.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna
- Columnas: Ninguna
- Consultas SQL crudas o llamadas a ORM: Ninguna

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `sqlite3`: Importada para interactuar con la base de datos SQLite.
  - `pandas`: Importada para el análisis de datos.

- Archivos del proyecto que este archivo importa (consume): Ninguno
- Archivos del proyecto que importan a este archivo (lo consumen): Ninguno

**Flujo de Datos:**
El script `test_sla_monthly_compiled.py` se ejecuta directamente y no depende de otros archivos o servicios dentro del proyecto. No realiza llamadas a otras funciones ni consume datos de otros componentes.


---

## Archivo: ./graphify-out/cache/ast/9d971d3e628599149fa1c11da8a1c6bd93049dd8bfba43374794d1ec90e12948.json

### Resumen Funcional
El archivo `test_ui_smoke.py` contiene pruebas de humo para un sistema de monitoreo de almacén (WMS). Las pruebas verifican la presencia de componentes visuales, manejo de errores y funcionalidades específicas del modal visual.

### Catálogo de Funciones y Clases
- `test_ui_smoke_components_presence()` - Verifica la presencia de componentes visuales.
- `test_ui_smoke_error_handling()` - Verifica que el servidor maneje correctamente las peticiones a rutas inexistente.
- `test_ui_smoke_analytics_studio_modal_components()` - Verifica que el modal visual exponga los selectores correctos y ejecute el SQL.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: `pytest`, `typing`
- **Archivos Importados por este Archivo**:
  - `tests/test_ui_smoke.py` (L1)
- **Archivos que Importan a este Archivo**: Ninguno

El flujo de datos es simple: el archivo `test_ui_smoke.py` importa las dependencias necesarias y contiene funciones que realizan pruebas específicas del sistema.


---

## Archivo: ./graphify-out/cache/ast/9ec5a58022289d00eb806477d5332a4cc7305b5150c1173de08ea12ff32a1624.json

### Resumen Funcional
El archivo `models_auth.py` contiene la definición del modelo ORM para los usuarios en el sistema de monitoreo de almacén (WMS). Este modelo incluye métodos y atributos necesarios para representar a un usuario, su rol y estado de activación.

### Catálogo de Funciones y Clases
- `User(base)` - Define la clase del modelo ORM para los usuarios.
  - `__repr__()` - Método que devuelve una representación en cadena del objeto `User`.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `users` (Tabla de usuarios del sistema)
- Columnas:
  - Roles ('admin', 'viewer')
  - Estado de desactivación

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**:
  - `datetime`
  - `sqlalchemy`
  - `sqlalchemy_orm`

- **Archivos del Proyecto que Importan a Este Archivo (`core/models_auth.py`)**:
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa (`core/models_auth.py`)**:
  - `database.py`

**Flujo de Datos**: El archivo `models_auth.py` importa las dependencias necesarias y define la clase `User`, que hereda de `Base`. La clase `User` incluye un método `__repr__()` para representar los objetos del modelo.


---

## Archivo: ./graphify-out/cache/ast/9f8e515e94a2bbe5d03bc612d9dd004df07f1dcdb947ed90befe5344aefe80fb.json

### Resumen Funcional
El archivo `query_ontime.py` contiene funciones para realizar consultas en una base de datos SQLite y procesar los resultados utilizando pandas.

### Catálogo de Funciones y Clases
- **Ninguna**

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** Ninguna (No hay consultas SQL explícitas)
- **Columnas:** Ninguna (No hay consultas SQL explícitas)

### Estado y Variables Globales
- **Ninguna**

### Dependencias y Flujo
- **Librerías Externas:**
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `json`: Para manejar operaciones JSON.
  - `pandas`: Para procesar los resultados de las consultas.

- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen):** Ninguna

- **Flujo de Datos:** El archivo importa librerías externas y no realiza ninguna interacción directa con el proyecto o la base de datos.


---

## Archivo: ./graphify-out/cache/ast/a12995f41d8a03f4ed3d4bccb51b752bf7807f0a47006ce375ea30845b24a3c7.json

### Resumen Funcional
El archivo `test_monthly_trend.py` contiene código que realiza un análisis de tendencias mensuales en el sistema de monitoreo de almacén (WMS). Es probablemente una prueba unitaria o integración para validar la funcionalidad relacionada con las tendencias mensuales.

### Catálogo de Funciones y Clases
Ninguna función o clase específica detectada en este fragmento.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna
- **Columnas**: Ninguna

El archivo no contiene consultas SQL crudas ni llamadas a ORM. Solo importa el módulo `sqlite3` para interactuar con la base de datos.

### Estado y Variables Globales
Ninguna variable global, de sesión o de entorno detectada en este fragmento.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `sys`
  - `sqlite3`

- **Archivos del Proyecto que IMPORTAN a Este Archivo**:
  - Ninguno

- **Archivos del Proyecto que ESTE Archivo IMPORTA**:
  - `core_queries_deliveries`

El flujo de datos es desde `test_monthly_trend.py` hacia los módulos importados (`sys`, `sqlite3`) y hacia el módulo `core_queries_deliveries`.


---

## Archivo: ./graphify-out/cache/ast/a3c4bc5b9154f3d0c90adefdd17b3bd588eebeb396ae769e559da03ba8539d30.json

### Resumen Funcional
El archivo `check_ollama.py` es un script que realiza operaciones relacionadas con el monitoreo de almacén (WMS). Es parte del sistema desarrollado con FastAPI, SQLAlchemy y SQLite.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: El archivo importa el módulo `ollama`.
- **Flujo de Datos**: No se proporcionan detalles específicos sobre cómo fluyen los datos en este fragmento.


---

## Archivo: ./graphify-out/cache/ast/a415e39ab77c0af4b8daf7b02dda0ddf5cb00e05d9a0fd6f117379cf3c2387aa.json

### Resumen Funcional
El archivo `consumos.py` contiene definiciones de rutas y métodos para el manejo de consumos en un sistema de monitoreo de almacén (WMS). Define endpoints para obtener los consumos agrupados por material, listar materiales consumidos por CeCos, y obtener el consumo mensual de un material específico.

### Catálogo de Funciones y Clases
- `MaterialesRequest` - Modelo Pydantic que representa una solicitud de materiales.
- `MaterialTrendRequest` - Modelo Pydantic que representa una solicitud de tendencia de materiales.
- `get_consumos_ceco()` - Obtiene los consumos (CMV 201) agrupados por material para un CeCo específico.
- `get_consumos_materiales()` - Obtiene que CeCos han consumido (CMV 201) una lista de materiales. Usa deduplicación.
- `get_material_trend()` - Devuelve el consumo mensual (CMV 201) de un material específico, filtrado por año.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas:
  - **Tabla:** `InventoryRepository` (No se especifican columnas específicas en la documentación proporcionada)
- Consultas SQL Crudas o Llamadas a ORM:
  - Se hace uso del repositorio `InventoryRepository` para obtener datos de inventario.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas:**
  - FastAPI
  - SQLAlchemy ORM
  - SQLAlchemy
  - Typing
  - Pydantic
  - Pandas
  - Core Database
  - Core Auth
  - Logging
  - Datetime

- **Flujo de Datos:**
  - `consumos.py` importa varios módulos y dependencias necesarias para su funcionamiento.
  - Los endpoints (`get_consumos_ceco`, `get_consumos_materiales`, `get_material_trend`) utilizan el repositorio `InventoryRepository` para interactuar con la base de datos SQLite.
  - Los métodos devuelven respuestas HTTP basadas en los resultados obtenidos del repositorio.

**Nota:** La documentación proporcionada no incluye detalles específicos sobre las consultas SQL o las columnas de la tabla `InventoryRepository`.


---

## Archivo: ./graphify-out/cache/ast/a4f8550fca26313fee016304a407c7aae994b81fa145487fb59adcc6b42cecce.json

### Resumen Funcional
El archivo `__init__.py` en la carpeta `services/etl` contiene funciones para procesar diferentes tipos de archivos relacionados con el inventario, tareas y entregas. Cada función parece estar diseñada para manejar un tipo específico de archivo y realizar operaciones de ETL (Extract, Transform, Load) sobre ellos.

### Catálogo de Funciones y Clases
- `process_inventory_folder()`: Procesa una carpeta de archivos relacionados con el inventario.
- `process_inventory_file()`: Procesa un archivo específico del inventario.
- `process_tasks_file()`: Procesa un archivo de tareas.
- `process_lx02_pendientes()`: Procesa un archivo de pendientes.
- `process_deliveries_file()`: Procesa un archivo de entregas.

### Interacción con Base de Datos
Ninguna. El código no interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno explícitamente mencionadas en el fragmento proporcionado.

### Dependencias y Flujo
- **Dependencias**: 
  - `InventoryMovementAdapter`
  - `WarehouseTaskAdapter`
  - `StockLevelAdapter`
  - `OutboundDeliveryAdapter`

- **Flujo de Datos**:
  - El archivo `__init__.py` importa varias clases (`InventoryMovementAdapter`, `WarehouseTaskAdapter`, `StockLevelAdapter`, `OutboundDeliveryAdapter`) y las utiliza dentro de sus funciones para procesar archivos.
  - Cada función llama a métodos como `process_directory()` o `process_and_save()` en estas clases adaptadoras.

El flujo general es que el archivo `__init__.py` coordina la llamada a diferentes adaptadores para procesar diferentes tipos de archivos, lo que sugiere una arquitectura modular y separada de preocupaciones.


---

## Archivo: ./graphify-out/cache/ast/a51baa519bf19235a8f8606a35cb8eaff5fd7089cefb186c8953005a3b2d320b.json

### Resumen Funcional
El archivo `update_dirs.py` es un script que realiza operaciones relacionadas con la actualización de directorios en el sistema de monitoreo de almacén (WMS). No contiene ninguna interacción explícita con una base de datos.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite3
- **Tablas**: Ninguna
- **Columnas**: Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `sqlite3`
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno
- **Archivos del Proyecto que Este Archivo Importa**: Ninguno
- **Flujo de Datos**: El archivo importa la librería `sqlite3` y no realiza ninguna operación con una base de datos.


---

## Archivo: ./graphify-out/cache/ast/a68814848abf03efe4787c8174f3b6993408716cf4ca76ea651ef3532a8ab34b.json

### Resumen Funcional
El archivo `tasks.py` contiene la implementación del adaptador para procesar el formato WMS Tareas (órdenes de transporte). Define una clase `WarehouseTaskAdapter` que hereda de `BaseWMSProcessor`, y métodos para validar archivos, obtener columnas requeridas, obtener claves primarias y limpiar un DataFrame.

### Catálogo de Funciones y Clases
- **Clase:** `WarehouseTaskAdapter`
  - **Método:** `.validate_file(file_path: Path) -> bool` - Valida el archivo según ciertos criterios.
  - **Método:** `._get_required_columns() -> List[str]` - Devuelve las columnas requeridas para el procesamiento.
  - **Método:** `._get_primary_keys() -> List[str]` - Devuelve las claves primarias del DataFrame.
  - **Método:** `._clean_dataframe(df: DataFrame) -> DataFrame` - Limpia y normaliza el DataFrame.

- **Clase:** `BaseWMSProcessor`
  (No se proporciona implementación en este fragmento)

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas:**
  - `pandas`
  - `pathlib`
  - `typing`

- **Archivos del Proyecto que Importan a Este Archivo (`services/etl/tasks.py`):**
  - No se proporciona información sobre los archivos que importan a este archivo.

- **Archivos del Proyecto que Este Archivo Importa:**
  - `users_christianykelly_desktop_monitorweb_services_etl_base_py`

- **Flujo de Datos:**
  El archivo `tasks.py` es importado por otros módulos, y utiliza métodos y clases definidos en él para procesar archivos WMS Tareas.


---

## Archivo: ./graphify-out/cache/ast/a6b37b42a7be88d390753feb2d6df3c445433887f218e9f119b0e0260928f928.json

### Resumen Funcional
El archivo `dashboard_service.py` contiene la definición de la clase `DashboardService`, que es responsable del orquestador del dashboard principal de Entregas (vista operativa). La clase incluye métodos para obtener el contexto completo del dashboard.

### Catálogo de Funciones y Clases
- **DashboardService()** - Constructor de la clase.
  - Parámetros: `session` (Tipo: Session)
- **get_full_context()** - Método que retorna un contexto completo del dashboard.
  - Parámetros: Ninguno
  - Retorno: Tipo: str, Any

### Interacción con Base de Datos
No se especifican consultas SQL crudas o llamadas a ORM en este archivo. La interacción con la base de datos se realiza a través de la clase `DeliveriesRepository`.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - logging
  - sqlalchemy.orm
  - typing
  - datetime
- **Archivos Importados**:
  - repositories.deliveries (DeliveriesRepository)
- **Archivos que Importan a Este Archivo**: Ninguno.

El flujo de datos fluye desde el archivo `dashboard_service.py` hacia la clase `DeliveriesRepository` para obtener los datos necesarios y luego se procesan en el método `get_full_context()` para construir el contexto del dashboard.


---

## Archivo: ./graphify-out/cache/ast/ae171fdce99e467dfe04fcaf020f10002786f4642de3564e9e28a5be68c79c97.json

### Resumen Funcional
El archivo `task_manager.py` contiene la implementación del gestor de tareas en segundo plano (Background Task Queue) para el sistema de monitoreo de almacén (WMS). Define clases y métodos para manejar el estado, registro e interacción con las tareas.

### Catálogo de Funciones y Clases
- **TaskStatus** - Enumeración que define los estados posibles de una tarea.
- **TaskRecord** - Clase que representa un registro inmutable de una tarea ejecutada o en ejecución.
- **TaskManager** - Clase principal que gestiona el encolamiento, ejecución y estado de las tareas.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `uuid`, `logging`, `datetime`, `concurrent.futures`, `dataclasses`, `enum`, `typing`, `threading`
- **Archivos Importados por este Archivo**:
  - Ninguno
- **Archivos que Importan a este Archivo**:
  - Ninguno

El flujo de datos se centra en la interacción entre las clases y métodos definidos, utilizando objetos como `TaskRecord` para almacenar el estado de las tareas y un `ThreadPoolExecutor` para ejecutar tareas en segundo plano.


---

## Archivo: ./graphify-out/cache/ast/b382729f7f3fb246a2d27c6a164f100abc5262e21745b4a51d5334a7c82bbfd8.json

### Resumen Funcional
El archivo `config.py` contiene la configuración centralizada de las rutas para el sistema de monitoreo de almacén (WMS) construido con FastAPI. Registra todos los routers de la aplicación de forma centralizada.

### Catálogo de Funciones y Clases
- **register_routes()** - Registra todos los routers de la aplicaciónde forma centralizada.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: FastAPI, typing
- **Archivos Importados por este Archivo**:
  - `logging`
  - `fastapi`
  - `typing`
  - `users_christianykelly_desktop_monitorweb_routes_init_py`
- **Archivos que Importan a este Archivo**: Ninguno

El flujo de datos es desde `config.py` hacia las funciones y clases importadas, específicamente hacia `FastAPI` para la configuración de rutas.


---

## Archivo: ./graphify-out/cache/ast/b44958fcbb00e0f75a5baf55d458b9a749d2fcf81ffcf4c089f883cd132e5c21.json

### Resumen Funcional
El archivo `debug_streaming.py` es un módulo que importa las bibliotecas `ollama` y `time`. No contiene ninguna función o clase definida explícitamente.

### Catálogo de Funciones y Clases
Ninguna.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: `ollama`, `time`
- **Flujo de datos**: El archivo importa las bibliotecas mencionadas pero no realiza ninguna operación específica que involucre funciones, clases o consultas a una base de datos.


---

## Archivo: ./graphify-out/cache/ast/b4c6552984ca65fc0b751b88a1107f25d073949379dfbe576129132fb769d368.json

### Resumen Funcional
El archivo `app_instance.py` es el punto de entrada del sistema, donde se configura y ejecuta la instancia principal de la aplicación utilizando FastAPI.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `pathlib`, `fastapi`, `fastapi_templating`
- **Archivos Importados por Este Archivo**:
  - `config` (importado en la línea 4)
- **Archivos que Importan a Este Archivo**: Ninguno

El flujo de datos es simple: el archivo `app_instance.py` importa las dependencias necesarias y configura la instancia principal de FastAPI.


---

## Archivo: ./graphify-out/cache/ast/b6c5a257816e454f4dd7ce7bdbd479f0213aeddcdde66e78d5c66b893168e199.json

### Resumen Funcional
El archivo `core/wms_config.py` contiene la configuración de lógica de negocio y mapeos WMS (SaaS Dinámico). Incluye funciones para validar los mapeos definidos.

### Catálogo de Funciones y Clases
- `validate_wms_maps()` - Valida la integridad de los mapeos definidos.
- `__getattr__()` - Maneja el acceso a atributos dinámicamente.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `typing`
  - `users_christianykelly_desktop_monitorweb_core_db_config_manager_py`

- **Flujo de Datos**:
  - `core/wms_config.py` importa `typing` y `users_christianykelly_desktop_monitorweb_core_db_config_manager_py`.
  - `validate_wms_maps()` llama a funciones como `get_status_mapping`, `ValueError`, `get_cost_center_mapping`, y `items`.
  - `__getattr__()` llama a funciones como `get_status_mapping`, `get_cost_center_mapping`, `get_setting`, y `AttributeError`.


---

## Archivo: ./graphify-out/cache/ast/b86003582c38796a8641e51ce613371fe2f07266eab2a0ec4281824e0ff97b87.json

### Resumen Funcional
El archivo `run_sync.py` es un script que realiza operaciones de sincronización en el sistema de monitoreo de almacén (WMS). No contiene ninguna lógica específica, solo importa módulos y configuraiones necesarias para la ejecución del sistema.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `sys`, `os`, `pathlib`, `logging`
- **Archivos Importados por este Archivo**:
  - `core_db_config_manager` (L13)
  - `routes_sync` (L17)
- **Archivos que Importan a este Archivo**: Ninguno

El archivo `run_sync.py` solo importa módulos y no realiza ninguna operación específica, por lo tanto, no interactúa con la base de datos ni tiene funciones definidas.


---

## Archivo: ./graphify-out/cache/ast/baf0e02fef0e872c8b7015942cb6266d9df1968305338d7efe0c7bc6b3ac6fb7.json

### Resumen Funcional
El archivo `widgets.json` contiene datos de configuración para widgets en el sistema de monitoreo de almacén (WMS). Este JSON se utiliza para inicializar los widgets en la interfaz web.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna


---

## Archivo: ./graphify-out/cache/ast/bbe8fba0598f812263746337209ef980788a2253525f2cf77f90e1d12f18241b.json

### Resumen Funcional
El archivo `test_modal_query.py` contiene una función de prueba que realiza consultas SQL contra una base de datos SQLite.

### Catálogo de Funciones y Clases
- `test_query()` - Realiza consultas SQL para obtener datos de la base de datos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:** No se especifican columnas específicas, solo indica que realiza operaciones CRUD.
- **Consultas SQL Crudas:** 
  - `execute("SELECT * FROM table_name")`
  - `fetchall()`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas:** Ninguna.
- **Archivos Importados por este Archivo:** `sqlite3`
- **Archivos que Importan a este Archivo:** Ninguno.


---

## Archivo: ./graphify-out/cache/ast/bcd344c6625ed9ef8aeb660b216431d084d22622ae5997150983d8eb81e5b77b.json

### Resumen Funcional
Este archivo es el punto de entrada para los servicios en el sistema de monitoreo de almacén (WMS). Contiene la configuración y la definición de las dependencias necesarias para que los servicios puedan funcionar.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: No se especifican dependencias directas en el fragmento proporcionado.
- **Flujo**: Este archivo no importa ni es importado por otros archivos. Es el punto de entrada para los servicios, lo que significa que los demás archivos (routes, repositories) deben importar este archivo para acceder a las funcionalidades definidas aquí.

Este archivo es crucial para la configuración inicial y la definición de dependencias globales en el sistema WMS, pero no realiza ninguna operación específica relacionada con la base de datos o la lógica de negocio.


---

## Archivo: ./graphify-out/cache/ast/bf234d835321cd0470b7ee1749d5807d30042464c9a3fa919e5438f788e6eb2b.json

### Resumen Funcional
El archivo `test_enrichment.py` contiene pruebas unitarias para el módulo de enriquecimiento del sistema de monitoreo de almacén (WMS). Las pruebas cubren la creación de una base de datos con datos de prueba, la aplicación de lógica de autorización, la recarga de entregas desde movimientos, el enriquecimiento de entregas con existencias y la actualización del SLA usando tareas de bodega.

### Catálogo de Funciones y Clases
- `db_with_data(connection)` - Prepara una base de datos con datos de prueba para los procesos de enriquecimiento.
- `test_learn_and_apply_author_logic()` - Verifica que el sistema aprenda que USER_A pertenece a PRODUCCION y lo aplique.
- `test_backfill_from_movements()` - Verifica que Entregas recupere el autor y centro de costo desde Movimientos.
- `test_enrichment_from_stock()` - Verifica que se crucen las descripciones de material y ubicaciones desde el maestro.
- `test_update_sla_with_tasks()` - Verifica que el SLA se actualice correctamente usando las tareas de bodega.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: `Movimientos`
    - Columna: `autor`, `centro_costo`
  - Tabla: `Entregas`
    - Columna: `id`, `material`, `ubicacion`
  - Tabla: `SLA`
    - Columna: `id`, `tarea_bodega`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `pytest`, `sqlite3`, `typing`
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:**
  - `db_enrichment` (Módulo que contiene funciones relacionadas con el enriquecimiento)

El flujo de datos es desde las pruebas hasta la ejecución de métodos que interactúan con la base de datos para realizar operaciones como `execute`, `commit`, `rollback`, y `fetchone`.


---

## Archivo: ./graphify-out/cache/ast/c23f2fe4b174b95d33b5c3e9866f3945a6db338af5b7f29369fd525fda11327e.json

### Resumen Funcional
El archivo `fix_descriptions.py` contiene una función llamada `manual_fix()` que realiza operaciones de base de datos para corregir descripciones en un sistema de almacén.

### Catálogo de Funciones y Clases
- `manual_fix()` - Realiza la lógica principal para corregir las descripciones en el sistema de almacén.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas Modificadas:**
  - Tabla: Ninguna específica mencionada.
  - Columna: Ninguna específica mencionada.
- **Consultas SQL Crudas o Llamadas a ORM:**
  - `connect()`
  - `fetchone()`
  - `execute()`
  - `backfill_material_texts()`

### Estado y Variables Globales
- Ninguna variable global, de sesión o diccionario quemado en el código que almacene estado crítico.

### Dependencias y Flujo
- **Librerías Externas:**
  - `sqlite3`
- **Archivos del Proyecto que Importan a este Archivo (lo consumen):**
  - Ninguno mencionado.
- **Archivos del Proyecto que Este Archivo Importa (consume):**
  - `db_enrichment`
  - `config`

**Flujo de Datos:**
1. El archivo `fix_descriptions.py` importa las dependencias necesarias (`sqlite3`, `db_enrichment`, `config`).
2. La función `manual_fix()` se ejecuta.
3. Dentro de `manual_fix()`, se realizan operaciones de base de datos utilizando funciones como `connect()`, `fetchone()`, y `execute()`.
4. Llama a la función `backfill_material_texts()` para realizar la lógica específica de corrección.
5. Finalmente, cierra la conexión con la base de datos usando `close()`.


---

## Archivo: ./graphify-out/cache/ast/c6369523a35d0fd10bc77e07324d719e0fc3fe8abd6e108a82974ede400776fe.json

### Resumen Funcional
El archivo `deliveries_service.py` contiene la definición de una clase `DeliveriesService` que probablemente se encarga de gestionar operaciones relacionadas con las entregas en un sistema de almacén (WMS). La clase incluye métodos para obtener el contexto completo y posiblemente otras operaciones relacionadas.

### Catálogo de Funciones y Clases
- `DeliveriesService()` - Constructor de la clase.
- `.get_full_context()` - Método que probablemente recupera el contexto completo del sistema.

### Interacción con Base de Datos
El archivo interactúa con una base de datos utilizando SQLAlchemy ORM. Las tablas y columnas específicas no se mencionan explícitamente, pero se utilizan métodos como `query`, `like`, `fetchall`, `execute` y `update`, lo que sugiere operaciones en tablas relacionadas con las entregas.

### Estado y Variables Globales
No hay variables globales, de sesión o diccionarios quemados en el código proporcionado.

### Dependencias y Flujo
- **Dependencias**: El archivo importa módulos como `sqlalchemy_orm`, `logging` y `typing`.
- **Flujo de Datos**: El archivo se importa por otros archivos del proyecto, pero no se mencionan específicamente qué archivos lo consumen.


---

## Archivo: ./graphify-out/cache/ast/c6651364f972da4c7b3f539da937474a15c6e5d2e5b74d33b7ec8f4ca2448792.json

### Resumen Funcional
El archivo `dashboard.py` contiene funciones relacionadas con el manejo del dashboard en un sistema de monitoreo de almacén (WMS). Incluye endpoints para obtener ubicaciones y una vista principal del dashboard con KPIs.

### Catálogo de Funciones y Clases
- **get_ubicaciones(str, Session, AppState)** - Obtiene ubicaciones.
- **dashboard(Request, Session, AppState)** - Vista principal del Dashboard con KPIs y búsqueda rápida.
- **dashboard_api(Session, AppState)** - API JSON para el Dashboard con KPIs y búsqueda rápida.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas y Columnas**:
  - Tabla: `ubicaciones`
    - Columna: `id`, `nombre`, `ubicacion`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - logging
  - sqlite3
  - itertools
  - pandas
  - datetime
  - typing
  - fastapi
  - fastapi_responses
  - core_database
  - sqlalchemy_orm
  - sqlalchemy
  - core_state
  - core_auth
  - core_app_instance
  - services_dashboard_service
  - core_schemas

- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno


---

## Archivo: ./graphify-out/cache/ast/c9a2e6284ae1fb0bb05cf560d5f4f625c95b499c17aee158f2db2edd806f0d64.json

### Resumen Funcional
El archivo `check_server.py` contiene una función llamada `check_server()` que realiza operaciones de red y procesamiento de datos para monitorear el estado de un servidor.

### Catálogo de Funciones y Clases
- **check_server()** - Realiza la lógica principal del script, incluyendo solicitudes HTTP y análisis de respuestas.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `urllib.request`, `json`, `re`
- **Archivos Importados por Este Archivo**: Ninguno
- **Archivos que Importan a Este Archivo**: Ninguno
- **Flujo de Datos**: El flujo comienza con la importación de las librerías necesarias, luego se ejecuta la función `check_server()`, que realiza una solicitud HTTP y procesa la respuesta.


---

## Archivo: ./graphify-out/cache/ast/ca48e7c22dd9c8b95961caf538090e46ed93f0789cdf1ec0f5e2cfd3b2273138.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `sync.py` contiene funciones relacionadas con la sincronización de datos en un sistema de almacén (WMS). Incluye endpoints para obtener la URL del túnel, el estado de la sincronización, iniciar la sincronización, listar tareas y consultar el estado de una tarea específica.

### Catálogo de Funciones y Clases
- `get_tunnel_url(appstate: AppState)` - Retorna la URL pубlica del túnel (Ngrok).
- `get_sync_status(appstate: AppState)` - Retorna el estado actual de la sincronización.
- `sync_data(appstate: AppState)` - Inicia el proceso de sincronización de datos. Encola la tarea en el TaskManager.
- `list_tasks(limit: int, appstate: AppState)` - Lista las tareas recientes del sistema.
- `get_task(task_id: str, appstate: AppState)` - Consulta el estado de una tarea específica por su ID.
- `_run_sync_pipeline(appstate: AppState)` - Ejecuta el pipeline completo de limpieza y consolidación.
- `_reset_directory(directory_path: str)` - Elimina y recrea un directorio de forma segura.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno quemadas en el código.

### Dependencias y Flujo
- **Librerías Externas**: `logging`, `shutil`, `pathlib`, `typing`, `fastapi`, `core_auth`, `config`, `core_state`, `core_task_manager`, `db_consolidator`.
- **Archivos Importados por este Archivo**:
  - `routes/sync.py` importa varias clases y funciones de otros archivos del proyecto.
- **Archivos que Importan a este Archivo**: No hay información sobre qué archivos importan a `sync.py`.

El flujo de datos es principalmente entre las funciones definidas en `sync.py`, utilizando objetos como `AppState` para compartir el estado del sistema.


---

## Archivo: ./graphify-out/cache/ast/cb7b0d02adac684714ccb754d1e09d30f5abc3528c018ed2e018ec2f5b384adf.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `routes/widgets.py` contiene endpoints para obtener datos de widgets y detalles subyacentes. Incluye funciones que ejecutan consultas SQL, manipulan datos y manejan errores.

### Catálogo de Funciones y Clases
- **get_widget_data()** - Obtiene datos de un widget.
- **get_widget_drilldown()** - Obtiene detalles subyacentes de un segmento de un widget.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** No especificadas explícitamente en el fragmento, pero se hace referencia a `WidgetRepository`.
- **Columnas:** No especificadas explícitamente en el fragmento.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno mencionadas.

### Dependencias y Flujo
- **Dependencias Externas:**
  - `fastapi`
  - `sqlalchemy_orm`
  - `core_database`
  - `core_models`
  - `core_auth`
  - `core_helpers_dynamic_executor`
  - `core_utils`
  - `core_state`

- **Archivos Importados por este Archivo:** Ninguno

- **Archivos que Importan a este Archivo:** Ninguno


---

## Archivo: ./graphify-out/cache/ast/cbbc3f651a1613a4f3ec8136ed98a535a1fb66d0a70ff714d073f44415f17e0a.json

### Resumen Funcional
Este archivo es el punto de entrada para la configuración y inicialización de la base de datos en un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Contiene la definición del motor de base de datos y la creación de las tablas necesarias.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (el archivo solo inicializa el motor, no crea o modifica tablas)
- **Consultas SQL Crudas/ORM**: Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: SQLAlchemy
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno
- **Archivos del Proyecto que Este Archivo Importa**: Repositories, Models (dependencia implícita a través de SQLAlchemy)
- **Dirección del Flujo de Datos**: El archivo se importa por otros archivos para configurar la base de datos.


---

## Archivo: ./graphify-out/cache/ast/ce5231446f6376685a1145238b9d71f4eac28cde5fc6a1b963d24ae59dd4aeec.json

### Resumen Funcional
El archivo `run_deliveries_context.py` contiene el contexto necesario para ejecutar operaciones relacionadas con las entregas en un sistema de monitoreo de almacén (WMS). Importa varias bibliotecas y módulos necesarios para su funcionamiento.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `sqlite3`, `pandas`, `logging`, `sys`
- **Módulos del Proyecto Importados**:
  - `routes_deliveries`
  - `traceback`

El archivo `run_deliveries_context.py` importa estas dependencias y módulos para su uso en el contexto de ejecutar operaciones relacionadas con las entregas. No realiza ninguna interacción directa con una base de datos ni utiliza variables globales.


---

## Archivo: ./graphify-out/cache/ast/d0c253d9963e39693ebd33bdbe38f32befb1802887646c16622128658d97c72b.json

### Resumen Funcional
El archivo `update_eff.py` es un script que realiza operaciones de actualización en una base de datos SQLite.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna
- **Columnas**: Ninguna
- **Consultas SQL Crudas o Llamadas a ORM**: No hay consultas SQL crudas ni llamadas a ORM explícitas.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Importada para interactuar con la base de datos SQLite.
  - `json`: Importada para manejar operaciones JSON (probablemente para leer o escribir archivos JSON).
  
- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno

**Flujo de Datos**: El archivo `update_eff.py` importa las bibliotecas necesarias y realiza operaciones relacionadas con la base de datos SQLite, pero no hay detalles específicos sobre qué funciones o métodos se utilizan para interactuar con la BD.


---

## Archivo: ./graphify-out/cache/ast/d245f9cdf70e1c6b963d8ce6c2570b5be09e0d83e2b8ad72e954af56f4b8b9cd.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `doc_generator.py` contiene funciones para generar documentación de proyectos utilizando un modelo de lenguaje llamado Ollama. El sistema analiza la estructura del proyecto, genera una representación en texto del árbol del proyecto, y luego documenta cada archivo con el modelo Ollama.

### Catálogo de Funciones y Clases
- `load_gitignore()`: Carga las reglas de `.gitignore`.
- `sanitize_output()`: Sanitiza la salida para evitar caracteres no deseados.
- `load_state()`: Carga el estado actual del sistema desde un archivo.
- `save_state()`: Guarda el estado actual del sistema en un archivo.
- `get_file_info()`: Obtiene información sobre un archivo, como su hash y tamaño.
- `get_cache_path()`: Genera una ruta única dentro de la caché para cada archivo.
- `should_process()`: Determina si un archivo debe ser procesado basándose en sus características.
- `generate_project_tree()`: Genera una representación en texto del árbol del proyecto.
- `chunk_text()`: Divide el texto en fragmentos con un solapamiento de líneas para mantener contexto.
- `calculate_num_ctx()`: Calcula num_ctx dinámicamente basándose en la cantidad de líneas y tamaño del código.
- `call_ollama_with_retry()`: Llamada a Ollama unificada usando la librería oficial. Si no se proporciona el modelo, intenta usar uno por defecto.
- `format_seconds()`: Convierte segundos a formato HH:MM:SS.
- `document_file()`: Procesa un archivo, mide el tiempo y retorna True si tuvo éxito.
- `analyze_structure_pre_flight()`: Genera el árbol del proyecto y realiza el análisis arquitectónico estructural.
- `generate_audit_post_flight()`: Genera la Auditoría Global analizando la documentación ya generada en la caché.
- `compile_master_file()`: Une todos los fragmentos de la caché en los archivos maestros en orden.
- `compile_by_folders()`: Compila la documentación y mejoras agrupándolas por carpetas del proyecto.
- `prepare_model()`: Verifica si Ollama está activo y si el modelo solicitado existe.
- `cleanup_orphaned_cache()`: Elimina de la caché los archivos que ya no existen en el proyecto.
- `purge_empty_cache_files()`: Busca y elimina archivos en `.doc_cache` que estén vacíos o corruptos para forzar su eliminación.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `os`, `sys`, `time`, `json`, `ollama`, `hashlib`, `tqdm`
- **Archivos del Proyecto que Este Archivo Importa (consume)**: No aplica
- **Archivos del Proyecto que Importan a Este Archivo (lo consumen)**: No aplica

**Flujo de Datos**: El archivo `doc_generator.py` se ejecuta como parte del flujo principal del sistema, llamando a varias funciones para procesar y documentar el proyecto.


---

## Archivo: ./graphify-out/cache/ast/d297121c31a0f65d30e0c80825d81c969e1f244a6a9d8c7532089be22905fd72.json

### Resumen Funcional
El archivo `test_traceback.py` contiene una función `run()` que realiza operaciones relacionadas con la conexión a una base de datos SQLite, prepara un análisis de tendencias de consumo planificado y maneja excepciones.

### Catálogo de Funciones y Clases
- `run()` - Realiza operaciones de conexión a la base de datos, preparación de análisis de tendencias de consumo planificado y manejo de excepciones.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:** Ninguna (No hay consultas SQL explícitas o llamadas a ORM)
- **Consultas SQL Crudas/LLamadas a ORM:** Ninguna

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `sqlite3`
  - `traceback`
  - `logging`

- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen):** Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA (consume):** Ninguno

- **Flujo de Datos:**
  - El archivo importa las bibliotecas necesarias (`sqlite3`, `traceback`, `logging`).
  - La función `run()` realiza operaciones relacionadas con la base de datos SQLite.
  - Se manejan excepciones utilizando `traceback.print_exc()`.
  - No hay interacción explícita con tablas o columnas específicas en la BD.


---

## Archivo: ./graphify-out/cache/ast/d34ce2e8af578f86ed77a620faaca8c4847b1939f59c2ca8abe8834c32e58a3b.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `routes/transporte.py` contiene funciones relacionadas con la gestión de transporte en el sistema de monitoreo de almacén (WMS). Incluye lógica para sincronizar datos, buscar y servir PDFs.

### Catálogo de Funciones y Clases
- **sync_transporte_logic(session: Session)** - Lógica core para sincronizar la base de datos externa de OneDrive a local.
- **sync_transporte()** - Sincroniza datos de transporte manualmente.
- **get_transporte_data()** - Retorna los datos consolidados diarios ordenados cronológicamente.
- **search_transporte(query: str)** - Busca en la tabla cruda de transporte_entregas por OT, GD o OC.
- **serve_pdf(filename: str)** - Sirve el archivo PDF desde el disco.
- **get_pending_transporte()** - Busca en transporte_entregas los documentos del año actual que NO han sido ingresados.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `transporte_entregas`
- Columnas (ejemplos):
  - `id`, `ot`, `gd`, `oc`, `fecha`, `archivo_pdf`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**:
  - `os`
  - `sqlite3`
  - `logging`
  - `typing`
  - `fastapi`
  - `fastapi_responses`
  - `sqlalchemy_orm`
  - `sqlalchemy`

- **Flujo de Datos**:
  - El archivo importa varias bibliotecas y módulos necesarios para su funcionamiento.
  - Las funciones utilizan la sesión de SQLAlchemy (`session`) para interactuar con la base de datos.
  - Llamadas a métodos como `execute`, `fetchall`, `commit` y `rollback` se realizan en las funciones para realizar operaciones CRUD en la base de datos.


---

## Archivo: ./graphify-out/cache/ast/d36c74aa7b763b4f4e82ab690b1d8254f7b539c193ec263bef95a20109b156ae.json

### Resumen Funcional
La clase `AppState` en el archivo `state.py` gestiona el estado mutable y la caché de forma centralizada, proporcionando métodos para configurar y obtener límites de caché, manejar sincronización, acceder a y modificar datos en caché, y limpiar caché.

### Catálogo de Funciones y Clases
- **Clase:** `AppState`
  - **Método:** `__init__()`
    - Propósito: Inicializa el estado del objeto.
  - **Método:** `max_cache_size()`
    - Parámetros: `size` (int)
    - Propósito: Devuelve o configura el límite máximo de entradas en caché.
  - **Método:** `sync_lock()`
    - Propósito: Devuelve el lock de sincronización para operaciones atómicas.
  - **Método:** `is_syncing()`
    - Parámetros: `is_syncing` (bool)
    - Propósito: Verifica si hay un proceso de sincronización activo.
  - **Método:** `cache_size()`
    - Propósito: Devuelve el número actual de entradas en la caché.
  - **Método:** `get_cache()`
    - Parámetros: `key` (str)
    - Propósito: Recupera un valor del caché.
  - **Método:** `set_cache()`
    - Parámetros: `key` (str), `value` (any)
    - Propósito: Guarda un valor en el caché, respetando los límites de tamaño.
  - **Método:** `clear_cache()`
    - Propósito: Limpia una entrada específcica o todo el caché.
  - **Método:** `clear_cache_prefix()`
    - Parámetros: `prefix` (str)
    - Propósito: Limpia todas las entradas de caché que comiencen con el prefijo dado.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas:** `fastapi`, `logging`, `threading`, `typing`
- **Archivos Importados por este Archivo:**
  - Ninguno
- **Archivos que Importan a este Archivo:**
  - Ninguno


---

## Archivo: ./graphify-out/cache/ast/d39615dd01370c6263d23a26234b550b372dee31ad1ed0986baf0a503344a781.json

### Resumen Funcional
El archivo `test_queries.py` contiene pruebas unitarias para funciones relacionadas con consultas y operaciones de base de datos en un sistema de monitoreo de almacén (WMS). Las pruebas incluyen la obtención de estadísticas, conteos de días activos y cálculos de KPIs.

### Catálogo de Funciones y Clases
- `MockConnectionWrapper` - Clase que simula una conexión a la base de datos.
  - `.__init__()` - Inicializa el objeto.
- `MockSession` - Clase que simula una sesión de base de datos.
  - `.__init__()` - Inicializa el objeto.
  - `.connection()` - Devuelve una simulación de conexión.
  - `.execute()` - Ejecuta una consulta SQL.
- `test_get_total_active_days()` - Prueba la obtención del conteo total de días activos.
- `test_get_total_active_days_empty()` - Prueba el comportamiento cuando no hay datos para contar.
- `test_get_area_stats()` - Prueba la obtención de estadísticas por área.
- `test_area_expr_fallback_locations()` - Prueba el manejo de expresiones fallidas en áreas.
- `test_query_engine_compiles_ast_correctly()` - Prueba que el motor de consultas compile correctamente el AST.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQLite. Las tablas y columnas específicas no se mencionan explícitamente, pero las pruebas implican operaciones en la base de datos para obtener estadísticas y contar días activos.

### Estado y Variables Globales
No hay variables globales, de sesión o diccionarios quemados en el código que almacenen estado crítico.

### Dependencias y Flujo
- **Librerías Externas**: `pytest`, `sqlite3`, `pandas`.
- **Archivos del Proyecto Importados**:
  - `repositories_deliveries` (se importa desde `tests/test_queries.py`)
- **Archivos que Importan a Este Archivo**: Ninguno.
- **Flujo de Datos**: El archivo consume funciones y clases de otros archivos para realizar pruebas unitarias, incluyendo la simulación de una conexión y sesión de base de datos.


---

## Archivo: ./graphify-out/cache/ast/d7671e63795698e7a7f01364d50480a7aaacbb5c7f34a55d2a9738faba99d8a0.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `core/wms_utils.py` contiene funciones utilitarias vectorizadas para transformación de datos, incluyendo la normalización de strings, mapeo de estados WMS, clasificación de ubicaciones en áreas de negocio, estandarización de fechas y cálculo de retrasos SLA.

### Catálogo de Funciones y Clases
- `sanitize_string(str)`: Normaliza un string para usarlo como encabezado de columna (snake_case).
- `map_wms_status(dataframe)`: Concatena columnas de estado y mapea al valor legible de negocio.
- `apply_cost_center_mapping(dataframe)`: Clasifica ubicaciones WMS en áreas de negocio de forma vectorizada.
- `normalize_date_columns(dataframe)`: Estandariza formatos de fecha WMS a dd-mm-yyyy de forma eficiente.
- `calculate_sla_delays(dataframe)`: Calcula días hábiles de retraso usando lógica vectorizada de NumPy.
- `generate_time_labels(dataframe)`: Genera etiquetas de semana ISO para visualización y analítica.
- `_manifest_execute(str)`: Ejecuta una query de manifiesto sobre Session SQLAlchemy o sqlite3.Connection.
- `is_file_changed(path)`: Verifica si un archivo ha cambiado desde la última sincronización. Acepta SQLAlchemy Session.
- `mark_file_processed(path, int)`: Marca un archivo como procesado en el manifiesto. Acepta SQLAlchemy Session.

### Interacción con Base de Datos
No se utiliza ninguna base de datos explícita. Todas las operaciones son realizadas sobre DataFrames de pandas o consultas SQL directas a través de SQLAlchemy.

### Estado y Variables Globales
Ninguna variable global, de sesión ni diccionario quemado en código que almacene estado crítico.

### Dependencias y Flujo
- **Librerías Externas**: `numpy`, `pandas`, `datetime`, `pathlib`, `typing`.
- **Archivos del Proyecto Importados**:
  - `core_wms_config`
  - `core_db_config_manager`
  - `sqlalchemy_orm`
  - `sqlalchemy`
- **Archivos que Importan a Este Archivo**: Ninguno.

El flujo de datos fluye desde las funciones utilitarias hasta la ejecución de consultas SQL y manipulación de DataFrames.


---

## Archivo: ./graphify-out/cache/ast/d7f3c3d4f2f27ae9f02b3b36ebe206cc405e57d624b56bcb2ef4484abb331fa9.json

### Resumen Funcional
El archivo `test_diag.py` contiene una función llamada `diag()` que realiza operaciones de base de datos utilizando SQLite.

### Catálogo de Funciones y Clases
- `diag()` - Realiza consultas a la base de datos para obtener información.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:** Ninguna (se supone que las tablas y columnas son específicas del contexto de la consulta SQL, pero no se proporcionan detalles adicionales).
- **Consultas SQL Crudas:** 
  - `connect()`
  - `cursor()`
  - `execute("SELECT * FROM table_name")` (donde `table_name` es una tabla específica)
  - `fetchall()`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas:** Ninguna.
- **Archivos Importados por este Archivo:** Ninguno.
- **Archivos que Importan a este Archivo:** Ninguno.
- **Flujo de Datos:** El archivo `test_diag.py` importa el módulo `sqlite3`, realiza una conexión a la base de datos, ejecuta una consulta y recupera los resultados.


---

## Archivo: ./graphify-out/cache/ast/db2f152027ef2d98ee4f249514ec07c6e58b6d59b1f7948fbf0d66f1bbaa1d6b.json

### Resumen Funcional
El archivo `security.py` contiene una función que valida el nombre de una tabla contra una lista blanca para prevenir SQL Injection.

### Catálogo de Funciones y Clases
- **validate_table(table_name: str)** - Valida el nombre de la tabla contra la lista blanca para prevenir SQL Injection.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: Importa `typing` (línea 4).
- **Flujo de Datos**: La función `validate_table` recibe un parámetro `table_name` del tipo `str`. Si el nombre de la tabla no está en la lista blanca, lanza una excepción `ValueError`.

**Nota**: El archivo no interactúa con ninguna base de datos ni utiliza variables globales.


---

## Archivo: ./graphify-out/cache/ast/e156816584b886e6a32669fc0110a876cb385245b93fa37d18b82c4f1564d64b.json

### Resumen Funcional
El archivo `test_api.py` contiene pruebas unitarias para diferentes endpoints de la API del sistema de monitoreo de almacén (WMS). Las pruebas cubren funcionalidades como el acceso a la raíz, obtención de URL de túnel, sincronización de datos, acceso a páginas analíticas y generación de consultas SQL.

### Catálogo de Funciones y Clases
- `test_read_root()` - Verifica que el endpoint raíz responda correctamente.
- `test_get_tunnel_url()` - Verifica que el endpoint `/url` devuelva la dirección del túnel ngrok.
- `test_post_sync_endpoint()` - Verifica que el endpoint de sincronización inicie el pipeline correctamente.
- `test_analytics_page_access()` - Verifica que la página de analíticas sea accesible.
- `test_build_sql_sla_efficiency()` - Verifica que el generador de consultas SQL compile correctamente la métrica SLA.
- `test_analytics_sla_route()` - Verifica que la ruta de auditoría SLA resuelva dinámicamente las áreas de negocio.
- `test_api_query_preview_returns_json_and_no_sql()` - Verifica que la consulta de vista previa devuelva JSON y no texto SQL.
- `test_api_settings_query_rejects_raw_sql()` - Verifica protección contra inyección y que el endpoint solo acepte visual_state.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno quemadas en el código.

### Dependencias y Flujo
- **Dependencias Externas**: `pytest`, `unittest_mock`
- **Archivos Importados por este Archivo**:
  - `core_state` (importado desde `tests/test_api.py`)
- **Archivos que Importan a este Archivo**: Ninguno

El flujo de datos es simple: el archivo `test_api.py` importa bibliotecas y dependencias necesarias, luego define funciones de prueba que interactúan con endpoints de la API.


---

## Archivo: ./graphify-out/cache/ast/e3289655a57b0dff9a163cda9b75334b04eb44af84af9fd502f37948163e7725.json

### Resumen Funcional
El archivo `update_kpis.py` es un script que realiza operaciones relacionadas con la actualización de indicadores clave (KPIs) en el sistema de monitoreo de almacén (WMS). No contiene ninguna interacción explícita con una base de datos ni con funciones específicas.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `sqlite3`, `json`
  - `sqlite3`: Importada para interactuar con la base de datos SQLite.
  - `json`: Importada para manejar operaciones JSON.

- **Archivos del Proyecto que IMPORTAN a este archivo**:
  - Ninguno

- **Archivos del Proyecto que ESTE archivo IMPORTA**:
  - Ninguno

- **Flujo de Datos**: El archivo importa las librerías `sqlite3` y `json`, pero no realiza ninguna operación específica con ellas.


---

## Archivo: ./graphify-out/cache/ast/e459973c50264df86f7828c1b56f40f1a937975a6c409477e75ac0fd2c1e9c85.json

### Resumen Funcional
El archivo `watcher.py` contiene la implementación de un observador de archivos que monitorea cambios en el sistema de archivos y realiza acciones específicas cuando ocurren eventos como la creación o modificación de archivos.

### Catálogo de Funciones y Clases
- **AwaitWriteFinishHandler** - Clase principal que hereda de `FileSystemEventHandler` y maneja los eventos de archivos.
  - `__init__()`
  - `_should_track(path: str) -> bool`
  - `.on_created(event)`
  - `.on_modified(event)`
  - `_add_file(file_path: str)`
  - `_poll_files()`
  - `.stop()`

- **start_watcher()**
- **stop_watcher()**

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
**Librerías Externas:**
- `os`
- `time`
- `logging`
- `threading`
- `watchdog.observers`
- `watchdog.events`
- `config`
- `core_task_manager`
- `routes_sync`

**Flujo de Datos:**
- **Entrada:** Eventos de archivos (creación, modificación).
- **Procesamiento:** Determina si el archivo debe ser rastreado, realiza acciones según el evento.
- **Salida:** No hay salida explícita, pero se realizan acciones como la adición de archivos y la actualización del estado.

**Flujo Interno:**
- `AwaitWriteFinishHandler` hereda de `FileSystemEventHandler`.
- Los métodos de `AwaitWriteFinishHandler` manejan eventos específicos.
- `start_watcher()` e `stop_watcher()` controlan el ciclo de vida del observador.


---

## Archivo: ./graphify-out/cache/ast/e47cd6669325a7c7a307c27e8ab523c961fc4ec5a35eecbb8b60509207404cd6.json

### Resumen Funcional
El archivo `query_validators.py` contiene funciones que validan identificadores y columnas en un sistema de monitoreo de almacén (WMS) utilizando SQLAlchemy para interactuar con una base de datos SQLite.

### Catálogo de Funciones y Clases
- **validate_identifier(id: str, session: Session) -> bool** - Valida que un identificador (tabla o tabla.columna) pertenezca a la lista blanca.
- **validate_column(table_name: str, column_name: str, session: Session) -> bool** - Valida que una columna pertenezca a una tabla permitida, consultando el esquema de la base de datos.
- **get_table_columns(table_name: str, session: Session) -> List[str]** - Retorna la lista de columnas de una tabla permitida. Devuelve lista vacía si no se encuentra la tabla.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas y Columnas**:
  - Tabla `table_name` (columna `column_name`)
- **Consultas SQL Crudas o Llamadas a ORM**:
  - Uso de métodos como `execute`, `text`, `add` en consultas SQLAlchemy.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: 
  - `sqlalchemy`
  - `sqlalchemy.orm`
  - `typing`
  - `logging`
- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno
- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno

El flujo de datos es unidireccional, con `query_validators.py` importando librerías necesarias y dependiendo de funciones internas para realizar validaciones.


---

## Archivo: ./graphify-out/cache/ast/e85eb32ef10c069c6eef5a018dfdc2808ecacf1d5f2cbd56cbdf3e76445f4be3.json

### Resumen Funcional
El archivo `__init__.py` en la carpeta `core` es el punto de entrada para el módulo `monitorweb`, inicializando posiblemente las dependencias y configuraciones necesarias.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna


---

## Archivo: ./graphify-out/cache/ast/e878f13cc945dcdfa7302e48f804e0858f9de5265c3c8353486c908d91dec155.json

### Resumen Funcional
El archivo `test_cm.py` es un script que realiza operaciones de análisis y consulta en una base de datos SQLite utilizando la biblioteca SQLAlchemy, junto con pandas para el manejo de datos tabulares.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna especificada directamente. Se espera que las consultas SQL se realicen a través de SQLAlchemy.
- **Columnas**: Ninguna especificada directamente. Se espera que las consultas SQL se realicen a través de SQLAlchemy.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para el manejo de datos tabulares.
- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno especificado directamente en el fragmento.
- **Archivos del Proyecto que ESTE archivo IMPORTA**:
  - `config`
  - `core_analytics_queries`

El flujo de datos es desde `test_cm.py` hacia las dependencias mencionadas, y luego hacia la base de datos SQLite a través de SQLAlchemy.


---

## Archivo: ./graphify-out/cache/ast/eb4d24dfe418cef1ec604234d00e2232517c6e34ccca76e43ce3af225fbe0b12.json

### Resumen Funcional
El archivo `macros.py` contiene una función que inyecta macros globales registradas en un string SQL proporcionado.

### Catálogo de Funciones y Clases
- `inject_macros(sql: str) -> str` - Inyecta todas las macros globales registradas en el string SQL proporcionado.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: No se mencionan dependencias externas específicas.
- **Flujo de Datos**: La función `inject_macros` toma un string SQL como parámetro, realiza una operación (reemplazo) y devuelve el string modificado.


---

## Archivo: ./graphify-out/cache/ast/eba4d9e4ac59c7b8e5eb66da74b15f2a548643403f8a4bc3e9e77de489092a44.json

### Resumen Funcional
El archivo `wrap_js.py` contiene una función que envuelve código JavaScript en un Immediately Invoked Function Expression (IIFE) y realiza operaciones de lectura, escritura y procesamiento de cadenas.

### Catálogo de Funciones y Clases
- **wrap_iife()** - Breve propósito: Envuelve el contenido del archivo `wrap_js.py` en un IIFE.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: 
  - `os`: Importada para operaciones del sistema.
  
- **Flujo de Datos**:
  - El archivo `wrap_js.py` importa el módulo `os`.
  - La función `wrap_iife()` realiza operaciones en cadenas y archivos, pero no interactúa con una base de datos.


---

## Archivo: ./graphify-out/cache/ast/f23cc18a8e0d9c04793802187c4118b71d8df4d86d0acbee63d88c685b75e5d1.json

### Resumen Funcional
El archivo `auth.py` contiene endpoints para autenticación y gestión de usuarios en un sistema de monitoreo de almacén (WMS). Incluye funciones para login, logout, obtener información del usuario, cambiar contraseña, registrar nuevos usuarios y listar todos los usuarios.

### Catálogo de Funciones y Clases
- `login(oauth2_password_request_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends())` - Autentica un usuario con username/password y retorna un JWT.
- `logout(response: Response, appstate: AppState) - Limpia la cookie de autenticación.
- `get_me(user: User = Depends(get_current_user), appstate: AppState) - Retorna la información del usuario autenticado.
- `change_password(changepasswordrequest: ChangePasswordRequest, dbsession: DBSession, user: User = Depends(get_current_user)) - Cambia la contraseña del usuario autenticado.
- `register_user(usercreate: UserCreate, dbsession: DBSession, appstate: AppState) - Crea un nuevo usuario. Solo accesible por administradores.
- `list_users(dbsession: DBSession, user: User = Depends(get_current_user), appstate: AppState) - Lista todos los usuarios del sistema.
- `login_page(request: Request, appstate: AppState) - Renderiza la página de login.

### Interacción con Base de Datos
No se especifican consultas SQL crudas o llamadas a ORM explícitas en el fragmento proporcionado. Sin embargo, las funciones que interactúan con la base de datos implican operaciones como `query`, `first`, `commit`, `add` y `flush`.

### Estado y Variables Globales
No se identifican variables globales, de sesión o de entorno quemadas en el código proporcionado.

### Dependencias y Flujo
- **Dependencias Externas**: `fastapi`, `fastapi_responses`, `fastapi_security`, `sqlalchemy_orm`.
- **Archivos Importados por este Archivo**:
  - `logging`
  - `typing`
  - `core_database`
  - `core_models_auth`
  - `core_auth`
  - `core_app_instance`
  - `core_state`
- **Archivos que Importan a este Archivo**: Ninguno.
- **Flujo de Datos**: El flujo de datos pasa por las funciones mencionadas, interactuando con la base de datos para realizar operaciones CRUD y devolviendo respuestas HTTP según los resultados.


---

## Archivo: ./graphify-out/cache/ast/f3ce044d9cbbbeb228c4c3f901b305805e328f7ff7a23f9fc986499af5d77f18.json

### Resumen Funcional
El archivo `test_mtime_precision.py` contiene pruebas unitarias para verificar la precisión de los tiempos de modificación (`mtime`) en el sistema de almacén (WMS). No se especifica un propósito más detallado.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna
- **Columnas**: Ninguna
- **Consultas SQL Crudas/ORM**: Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Importado para interactuar con la base de datos SQLite.
  - `pathlib`: Importado para manejar rutas de archivos.

- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno

- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno

- **Dirección del Flujo de Datos**: El archivo importa las bibliotecas `sqlite3` y `pathlib`, lo que indica que estas dependencias son necesarias para su ejecución.


---

## Archivo: ./graphify-out/cache/ast/f52999a54296b96e7d25aa575def4ba07a75ef1c71d30a25a486ef66aa983973.json

### Resumen Funcional
El archivo `schemas.py` contiene definiciones de esquemas para diferentes tipos de respuestas y objetos en el sistema de monitoreo de almacén (WMS). Estos esquemas utilizan Pydantic para la validación y serialización de datos.

### Catálogo de Funciones y Clases
- `DashboardResponse` - Define el esquema para una respuesta del panel de control.
- `AnalyticsDeliveriesResponse` - Define el esquema para una respuesta de análisis de entregas.
- `AnalyticsInventoryResponse` - Define el esquema para una respuesta de análisis de inventario.
- `AnalyticsTasksResponse` - Define el esquema para una respuesta de análisis de tareas.
- `JoinDef` - Define la estructura para una definición de unión en consultas SQL.
- `FilterDef` - Define la estructura para una definición de filtro en consultas SQL.
- `MetricCondition` - Define la estructura para una condición de métrica en consultas SQL.
- `MetricDef` - Define la estructura para una definición de métrica en consultas SQL.
- `TimeAxisDef` - Define la estructura para una definición del eje temporal en consultas SQL.
- `SecondMetricDef` - Define la estructura para una segunda definición de métrica en consultas SQL.
- `VisualQueryBuilderPayload` - Define el esquema para un payload de generador visual de consultas.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: Pydantic, typing
- **Flujo de Datos**: El archivo `schemas.py` se importa por otros archivos del proyecto que necesitan utilizar estos esquemas para la validación y serialización de datos.


---

## Archivo: ./graphify-out/cache/ast/f6d3286ac44aa7031a690381512408924043c8768a3ee8d5580c815428a7b962.json

### Resumen Funcional
El archivo `search_logs.py` es un módulo que importa el formato JSON para su uso en la aplicación de monitoreo de almacén (WMS). No contiene ninguna función o clase definida explícitamente.

### Catálogo de Funciones y Clases
Ninguna.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: Importa el formato JSON.
- **Flujo de datos**: No hay interacciones directas con archivos o bases de datos.


---

## Archivo: ./graphify-out/cache/ast/f7e524c4c2347e1dbf7e5bf20ca8294ad570d17e790156315aabb13526024d42.json

### Resumen Funcional
El archivo `__init__.py` en la carpeta `routes` es el punto de entrada para las rutas del sistema de monitoreo de almacén (WMS). No contiene ninguna lógica funcional específica, solo importaciones.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías externas**: Ninguna
- **Archivos del proyecto que IMPORTA a este archivo (lo consumen)**: Ninguno
- **Archivos del proyecto que este archivo IMPORTA**: Ninguno


---

## Archivo: ./graphify-out/cache/ast/f8a18ea70b89b9f58e13ee9fe2fffd3882fe54616a05ab3db15eff712e5011c1.json

### Resumen Funcional
El archivo `test_maintenance.py` contiene pruebas unitarias para funciones relacionadas con la gestión del mantenimiento en el sistema de monitoreo de almacén (WMS). Las pruebas cubren la funcionalidad de cierre de aplicación, generación de documentación y lógica de filtrado.

### Catálogo de Funciones y Clases
- `test_quit_app_success()` - Prueba que la función `quit_app` retorne `True` cuando el comando de sistema tiene éxito.
- `test_quit_app_failure()` - Prueba que la función `quit_app` retorne `False` cuando ocurre un error de proceso o excepción.
- `test_doc_generator_filtering_logic()` - Prueba la lógica de exclusión de archivos en el generador de documentación.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**: `pytest`, `subprocess`, `unittest.mock`
- **Archivos Importados por este Archivo**:
  - `scripts_free_ram`
  - `scripts_doc_generator`
- **Archivos que Importan a este Archivo**: Ninguno.

El flujo de datos es simple: el archivo importa las dependencias necesarias y luego define las funciones de prueba, cada una utilizando mocks y assertions para verificar el comportamiento esperado de las funciones bajo pruebas.


---

## Archivo: ./graphify-out/cache/stat-index.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `stat-index.json` contiene metadatos sobre los archivos del proyecto de Sistema de Monitoreo de Almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Los metadatos incluyen el tamaño, la fecha de modificación en nanosegundos y un hash SHA-256 para cada archivo.

### Catálogo de Funciones y Clases
No se detectaron funciones o clases específicas en este fragmento de `stat-index.json`.

### Interacción con Base de Datos
Ninguna. El archivo solo contiene metadatos sobre los archivos del proyecto, no interactúa con una base de datos.

### Estado y Variables Globales
Ninguna. El archivo solo contiene metadatos sobre los archivos del proyecto, no almacena estado crítico en variables globales.

### Dependencias y Flujo
No se detectaron dependencias o flujos específicos en este fragmento de `stat-index.json`.


---

## Archivo: ./graphify-out/manifest.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `manifest.json` contiene metadatos sobre los archivos del proyecto de Sistema de Monitoreo de Almacén (WMS). Cada entrada lista el nombre del archivo, su última modificación (`mtime`) y hashes abstractos (`ast_hash` y `semantic_hash`). No se proporciona información funcional específica.

### Catálogo de Funciones y Clases
No hay funciones ni clases definidas en este archivo. Solo contiene metadatos sobre otros archivos.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna


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

## Archivo: ./repositories/__init__.py

### Resumen Funcional
Este archivo es el punto de entrada para la configuración y gestión de las dependencias relacionadas con la base de datos en un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Define funciones para obtener conexiones a la base de datos y repositorios específicos para diferentes entidades del sistema.

### Catálogo de Funciones y Clases
- `get_db()` - Establece una conexión a la base de datos SQLite utilizando el motor `sqlite3` y devuelve un contexto manejador que cierra la conexión cuando se sale del bloque.
- `get_deliveries_repo(conn: sqlite3.Connection = Depends(get_db)) -> DeliveriesRepository` - Crea e inicializa una instancia del repositorio `DeliveriesRepository` con la conexión a la base de datos proporcionada.
- `get_inventory_repo(conn: sqlite3.Connection = Depends(get_db)) -> InventoryRepository` - Crea e inicializa una instancia del repositorio `InventoryRepository` con la conexión a la base de datos proporcionada.
- `get_tasks_repo(conn: sqlite3.Connection = Depends(get_db)) -> TasksRepository` - Crea e inicializa una instancia del repositorio `TasksRepository` con la conexión a la base de datos proporcionada.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:** No se especifican explícitamente en este archivo. Se asume que las tablas y columnas están definidas en los repositorios `DeliveriesRepository`, `InventoryRepository` y `TasksRepository`.
- **Consultas SQL Crudas o ORM:** Utiliza el motor `sqlite3` directamente para establecer la conexión.

### Estado y Variables Globales
No se detectan variables globales, de sesión, de entorno o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- **Librerías Externas:** `sqlite3`, `fastapi`
- **Archivos del Proyecto que IMPORTA (consume):** No se detectan archivos externos que importen este archivo.
- **Archivos del Proyecto que IMPORTAN a Este Archivo (lo consumen):** Los repositorios `DeliveriesRepository`, `InventoryRepository` y `TasksRepository`.
- **Dirección del Flujo de Datos:** El flujo de datos comienza en las rutas FastAPI, pasa por los servicios, luego a través de estas funciones para obtener la conexión a la base de datos y los repositorios correspondientes.


---

## Archivo: ./repositories/base.py

### Resumen Funcional
Clase base para todos los repositorios de datos en el sistema WMS. Proporciona métodos para manejar consultas SQL y verificar el estado visual de las mismas.

### Catálogo de Funciones y Clases
- `BaseRepository(session: Session)` - Inicializa la instancia con una sesión de SQLAlchemy.
- `_sql(query_id: str, fallback: str) -> str` - Devuelve un texto SQL basado en un ID de consulta o un valor de reemplazo (fallback).
- `_has_visual_state(query_id: str) -> bool` - Verifica si una consulta tiene un estado visual JSON almacenado.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos.

### Estado y Variables Globales
Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Dependencias**: `sqlalchemy.orm.Session`, `core.db_config_manager.get_query_visual_state`.
- **Flujo de Datos**: El archivo no consume ni produce datos externos. Es una clase base para otros repositorios que pueden interactuar con la base de datos a través de las sesiones proporcionadas.


---

## Archivo: ./repositories/deliveries.py

### Resumen Funcional
Este archivo contiene métodos para interactuar con la base de datos SQLite y obtener información sobre entregas en un sistema de almacén (WMS). Los métodos incluyen consultas para auditoría SLA, entregas por lotes, áreas de negocio, elementos de picking, transacciones filtradas, indicadores clave de rendimiento (KPIs), detalles de entrega individual y gráficos de intensidad semanal.

### Catálogo de Funciones y Clases
- `DeliveriesRepository(BaseRepository)` - Repositorio para el dominio de Entregas.
  - `_sql(query_id: str, fallback: str) -> str` - Obtiene SQL desde config_queries con fallback explícito.
  - `_get_sla_threshold() -> int` - Obtiene el umbral SLA desde la configuración.
  - `get_sla_audit_records(year: str, late: bool = True, limit: int = 500, where_clause: str = None, where_params: dict = None) -> pd.DataFrame` - Obtiene registros de auditoría SLA.
  - `get_deliveries_for_bulk(date: str = None, area: str = None, centro: str = None, has_ots_filter: str = None, entrega_query: str = None) -> pd.DataFrame` - Obtiene entregas para lotes.
  - `get_area_lookup() -> pd.DataFrame` - Obtiene áreas de negocio asociadas a las entregas.
  - `get_picking_items(entrega_ids: list) -> pd.DataFrame` - Obtiene elementos de picking por entrega.
  - `build_unified_where(date: str, area: str, centro: str, has_ots_filter: str, min_week: str) -> tuple` - Construye una cláusula WHERE unificada.
  - `get_filtered_transactions(date: str, entrega: str, area: str, centro: str, has_ots_filter: str, min_week: str) -> list` - Obtiene transacciones filtradas.
  - `get_filtered_kpis(date: str, area: str, centro: str, min_week: str, iso_year: int) -> dict` - Obtiene indicadores clave de rendimiento (KPIs).
  - `get_delivery_by_id(entrega: str) -> pd.DataFrame` - Obtiene detalles de entrega individual.
  - `get_weekly_intensity_chart(year: int) -> dict` - Prepara los datos para el gráfico de intensidad semanal.
  - `get_dashboard_selectors(min_week: str) -> dict` - Obtiene listas únicas de fechas y áreas, además de mapeos de autores y centros.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - `outbound_deliveries`
  - `warehouse_tasks`
  - `DeliverySummary`
  - `config_cost_center_mapping`
  - `autor_area_mapping`
- Columnas:
  - `entrega`, `autor`, `area_negocio`, `creado_el`, `fecha_sm_real`, `material`, `denominacion`, `dias_retraso`, `estado_wms`, `week_sort`, `centro_costo`, `ubicacion_bin_1`, `ubicacion_bin`
  - `entrega_id`, `area_val`

### Estado y Variables Globales
- No hay variables globales, de sesión o de entorno quemadas en el código.

### Dependencias y Flujo
- Librerías externas:
  - `pandas`
  - `sqlalchemy`
- Archivos del proyecto que este archivo importa:
  - `core.db_config_manager`
  - `core.macros`
  - `repositories.base`
- Archivos del proyecto que importan a este archivo:
  - Ninguno
- Flujo de datos: Este archivo es consumido por otros archivos en la capa de Repositories, que a su vez son llamados por los servicios y rutas definidos en el proyecto.


---

## Archivo: ./repositories/inventory.py

### Resumen Funcional
El archivo `inventory.py` contiene métodos para obtener datos de inventario, específicamente consumos y tendencias de materiales. Utiliza SQLAlchemy para interactuar con una base de datos SQLite.

### Catálogo de Funciones y Clases
- `get_consumos_ceco(ceco: str) -> dict`: Obtiene los consumos históricos y del mes actual por centro de costo (CeCo).
- `get_consumos_materiales(materiales: list) -> dict`: Obtiene los consumos históricos y del mes actual para una lista de materiales.
- `get_material_trend(material: str, area_negocio: str, ceco: str) -> dict`: Obtiene la tendencia de un material específico por área de negocio y centro de costo (CeCo).
- `check_table_exists() -> bool`: Verifica si la tabla `inventory_movements` existe en la base de datos.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: 
  - `inventory_movements`
  - `outbound_deliveries`
- **Columnas**:
  - `inventory_movements`: `material`, `texto_breve_material`, `umb`, `cantidad`, `importe_ml`, `cmv`, `fe_contab`, `hora`, `ce_coste`
  - `outbound_deliveries`: `centro_costo`, `area_negocio`

### Estado y Variables Globales
- **Variables Globales**: Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `logging`
  - `pandas`
  - `sqlalchemy`
  - `datetime`
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno
- **Archivos del Proyecto que Este Archivo Importa**: Ninguno
- **Flujo de Datos**:
  - El archivo importa `BaseRepository` desde el módulo `.base`.
  - Utiliza `pandas` para procesar los resultados de las consultas SQL.
  - Realiza consultas SQL directamente en la base de datos SQLite utilizando SQLAlchemy.


---

## Archivo: ./repositories/tasks.py (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
Este archivo contiene métodos para obtener resúmenes diarios, horarios, inactividades y calorímetros de movimientos en el sistema de almacén. También incluye funciones para obtener detalles diarios y mensuales de los movimientos realizados por usuarios específicos.

### Catálogo de Funciones y Clases
- `get_available_dates()` - Devuelve una lista ordenada de fechas únicas con movimientos generados o confirmados.
- `_get_daily_summary(date_sap)` - Calcula el resumen diario de movimientos para un usuario específico.
- `_get_hourly_trend(date_sap)` - Genera un trend horario de los movimientos.
- `_get_inactivity_gaps(date_sap)` - Identifica los huecos de inactividad en los movimientos.
- `_get_activity_heatmap(date_sap)` - Crea un mapa de calor basado en la actividad diaria.
- `get_user_movements_daily_summary(target_date, usuario)` - Obtiene el resumen diario de movimientos para un usuario específico.
- `get_user_movements_daily_details(target_date, usuario, operacion)` - Detalla los movimientos diarios para un usuario y una operación específica.
- `_get_monthly_summary(month_sap)` - Calcula el resumen mensual de movimientos.
- `_get_monthly_shifts(month_sap)` - Genera un trend por turnos mensuales.
- `_get_monthly_heatmap(month_sap)` - Crea un mapa de calor basado en la actividad mensual.
- `get_user_movements_monthly_summary(target_month, usuario)` - Obtiene el resumen mensual de movimientos para un usuario específico.
- `get_user_movements_monthly_details(target_month, usuario, operacion)` - Detalla los movimientos mensuales para un usuario y una operación específica.
- `get_tasks_summary()` - Devuelve un resumen de tareas por clase de movimiento.
- `get_tasks_trend()` - Genera un trend de las tareas.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `inventory_movements`
    - Columnas: `registrado`, `hora`, `usuario`, `tipo_operacion`, `texto_cab_documento`, `doc_mat`, `cmv`, `material`, `texto_breve_material`, `cantidad`
  - `warehouse_tasks`
    - Columnas: `fecha_conf`, `hor_conf`, `usuario_conf`, `numero_ot`, `ctd_teor_dsd`, `cl_mov`, `clase_mov`, `fe_creac`, `hora`

### Estado y Variables Globales
- No hay variables globales declaradas.

### Dependencias y Flujo
- Librerías externas: `pandas`
- Archivos del proyecto que importan a este archivo:
  - `./services/tasks_service.py` (consume)
- Archivos del proyecto que este archivo importa:
  - `./base.py` (consumido por `TasksRepository`)
  - `./models.py` (no se muestra en el fragmento, pero probablemente contiene modelos SQLAlchemy)

#### --- PARTE 2 de 2 ---

### Resumen Funcional
Este archivo contiene funciones que interactúan con una base de datos SQLite para recuperar y procesar datos relacionados con tareas en un sistema de almacén (WMS). Las funciones devuelven datos en formato DataFrame de pandas.

### Catálogo de Funciones y Clases
- `get_tasks_trend()` - Recupera el trend de tareas por mes.
- `get_tasks_by_user()` - Recupera las tareas agrupadas por usuario.
- `get_tasks_by_type_dest()` - Recupera las tareas agrupadas por tipo de movimiento y destino.
- `get_recent_tasks()` - Recupera las tareas recientes que no han sido confirmadas.
- `get_non_palletized_movements()` - Recupera los movimientos no palletizados.
- `get_non_palletized_count()` - Cuenta el número de movimientos no palletizados.
- `get_non_palletized_summary()` - Resumen de movimientos no palletizados.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `warehouse_tasks`
  - `lx02_pendientes`
  - `inventory_movements`
- Columnas:
  - `warehouse_tasks`: `fe_creac`, `fecha_conf`, `usuario`, `usuario_conf`, `clase_mov`, `ctd_teor_dsd`, `ubic_proc`, `ubic_dest`, `hora`, `numero_ot`, `material`, `texto_breve_material`
  - `lx02_pendientes`: `otcuanto`, `stock_disp`
  - `inventory_movements`: `doc_mat`, `usuario`, `cmv`, `fe_contab`, `hora`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- Librerías externas: pandas, sqlalchemy.
- Archivos del proyecto que importan a este archivo:
  - Ninguno.
- Archivos del proyecto que este archivo importa:
  - Ninguno.


---

## Archivo: ./repositories/widgets.py

### Resumen Funcional
El archivo `widgets.py` contiene métodos para ejecutar consultas dinámicas y generar visualizaciones de datos en un sistema de monitoreo de almacén (WMS). Los métodos permiten filtrar y procesar datos según parámetros como año, área y granularidad.

### Catálogo de Funciones y Clases
- `execute_widget(query_id: str, visual_state: str, year: Optional[str], area: Optional[str], granularity: Optional[str]) -> Dict[str, Any]` - Ejecuta una consulta dinámica para generar una visualización.
- `execute_drilldown(query_id: str, visual_state: str, segment: str, material: Optional[str], year: Optional[str]) -> list` - Realiza un drilldown en los datos según el segmento y material proporcionados.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `outbound_deliveries`
- **Columnas:** 
  - `fecha_carga`, `entrega`, `pos_`, `cantidad`, `dias_retraso`, `material`, `denominacion`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `logging`
  - `json`
  - `pandas`
  - `sqlalchemy`
  - `typing`
- **Archivos del Proyecto que Importan a este Archivo:** 
  - `core.helpers.dynamic_executor.execute_visual_query`
  - `core.schemas.VisualQueryBuilderPayload`
  - `core.query_engine.build_sql_from_payload`
  - `core.utils.sanitize_for_json`
- **Archivos del Proyecto que Este Archivo Importa:**
  - `base.BaseRepository`

**Flujo de Datos:**
1. `widgets.py` importa funciones y clases necesarias.
2. Los métodos `execute_widget` y `execute_drilldown` son llamados desde otros archivos del proyecto.
3. Estos métodos interactúan con la base de datos para ejecutar consultas SQL dinámicas y procesar los resultados.
4. Los resultados se formatean y devuelven como un diccionario o lista según el método utilizado.

Este archivo es crucial para la generación de visualizaciones en el sistema WMS, permitiendo una interacción dinámica con los datos del almacén.


---

## Archivo: ./routes/__init__.py

### Resumen Funcional
Este archivo es el punto de entrada para las rutas del sistema de monitoreo de almacén (WMS). Importa y registra todas las subrutas relacionadas con diferentes funcionalidades como el panel de control, entregas, inventario, análisis proyecciones, filtros, PDFs, sincronización y configuraciones.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: FastAPI.
- **Archivos del Proyecto que IMPORTAN a este archivo**:
  - `dashboard`
  - `deliveries`
  - `inventory`
  - `analytics_proyecciones`
  - `filters`
  - `pdf`
  - `sync`
  - `docs`
  - `settings`

Este archivo no importa ninguna clase o función específica, solo registra las subrutas. El flujo de datos se maneja a través de FastAPI para la definición y gestión de rutas.


---

## Archivo: ./routes/analytics_proyecciones.py

### Resumen Funcional
Este archivo define las rutas para obtener analíticas de proyecciones en un sistema de monitoreo de almacén (WMS). Permite refrescar los datos si es necesario y utiliza una caché para mejorar el rendimiento.

### Catálogo de Funciones y Clases
- `get_proyecciones_context()` - Obtiene el contexto de proyecciones, priorizando la caché.
- `get_analytics_proyecciones(request: Request, force_refresh: bool = False, state: AppState = Depends(get_app_state))` - Retorna los datos de proyecciones en formato JSON.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna (se utiliza `generate_predictions(_DB)` que es una función externa)

### Estado y Variables Globales
- `AppState` - Almacena el estado del sistema, incluyendo la caché.
- `get_app_state()` - Función para obtener el estado actual del sistema.

### Dependencias y Flujo
- Librerías Externas: FastAPI, SQLAlchemy (a través de `generate_predictions(_DB)`).
- Archivos Importados:
  - `./core/auth.py` - Para la autenticación.
  - `./core/state.py` - Para el manejo del estado del sistema.
  - `./db/predictive_engine.py` - Para generar predicciones.
  - `./config.py` - Para obtener la ruta de la base de datos.

- Flujo de Datos:
  1. El usuario hace una solicitud a `/analytics/proyecciones`.
  2. La función `get_analytics_proyecciones` verifica si se debe forzar el refresco de los datos.
  3. Si no se fuerza el refresco, intenta obtener los datos desde la caché.
  4. Si la caché está vacía o se requiere un refresco, llama a `get_proyecciones_context()`.
  5. `get_proyecciones_context()` genera las predicciones utilizando `generate_predictions(_DB)`.
  6. Las predicciones se almacenan en la caché y se devuelven como respuesta JSON.

Este archivo es crucial para el monitoreo de proyecciones en el sistema WMS, asegurando que los datos sean actualizados regularmente y accesibles rápidamente a través de una interfaz RESTful.


---

## Archivo: ./routes/auth.py

### Resumen Funcional
Este archivo contiene endpoints para autenticación y gestión de usuarios en un sistema de monitoreo de almacén (WMS). Ofrece funcionalidades como login, registro de nuevos usuarios, cambio de contraseña y listado de usuarios.

### Catálogo de Funciones y Clases
- `login(response: Response, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session_dep))` - Autentica un usuario con username/password y retorna un JWT.
- `logout(response: Response, state: AppState = Depends(get_app_state))` - Limpia la cookie de autenticación.
- `get_me(user: User = Depends(require_auth), state: AppState = Depends(get_app_state))` - Retorna la información del usuario autenticado.
- `change_password(data: ChangePasswordRequest, db: DBSession, user: User = Depends(require_auth))` - Cambia la contraseña del usuario autenticado.
- `register_user(data: UserCreate, db: DBSession, admin: User = Depends(require_admin), state: AppState = Depends(get_app_state))` - Crea un nuevo usuario. Solo accesible por administradores.
- `list_users(db: DBSession, admin: User = Depends(require_admin), state: AppState = Depends(get_app_state))` - Lista todos los usuarios del sistema.
- `login_page(request: Request, state: AppState = Depends(get_app_state))` - Renderiza la página de login.

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
  
- **Archivos del Proyecto que IMPORTA a este archivo (`auth.py`):** 
  - `core.database`
  - `core.models_auth`
  - `core.auth`
  - `core.app_instance`
  - `core.state`

- **Archivos del Proyecto que ESTE archivo IMPORTA:**
  - Ninguno

- **Dirección del Flujo de Datos:** 
  - Desde el endpoint hasta la base de datos para autenticar y gestionar usuarios.


---

## Archivo: ./routes/config.py

### Resumen Funcional
El archivo `config.py` es un módulo que se encarga de registrar todos los routers de la aplicación FastAPI en una instancia de `FastAPI`. Incluye manejo básico de errores para evitar que un router mal configurado detenga el arranque completo del servidor.

### Catálogo de Funciones y Clases
- `register_routes(app: FastAPI) -> None` - Registra todos los routers de la aplicación en una instancia de `FastAPI`.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `ROUTERS: List[APIRouter]` - Una lista declarativa de routers con tipado estático que se registran en la aplicación.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directamente mencionadas.
- **Flujo**: El archivo importa varios módulos de ruta (`dashboard`, `deliveries`, etc.) y registra sus routers en una instancia de `FastAPI`.


---

## Archivo: ./routes/consumos.py

### Resumen Funcional
Este archivo contiene rutas para obtener datos de consumos en un sistema de almacén (WMS) utilizando FastAPI. Permite consultar los consumos agrupados por material y ceco, así como el consumo histórico de materiales específicos.

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
- Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `fastapi`
  - `sqlalchemy`
  - `pydantic`
  - `pandas`
  - `logging`
  - `datetime`
- Archivos del proyecto que este archivo importa:
  - `core.database.get_session_dep`
  - `core.auth.get_current_user`
  - `repositories.inventory.InventoryRepository`
- Archivos del proyecto que importan a este archivo:
  - Ninguno

El flujo de datos es desde las rutas hasta el repositorio, donde se realizan las consultas a la base de datos.


---

## Archivo: ./routes/dashboard.py

### Resumen Funcional
El archivo `dashboard.py` contiene rutas para el dashboard de un sistema de monitoreo de almacén (WMS). Ofrece endpoints para obtener ubicaciones de materiales y cargar la vista principal del dashboard con KPIs.

### Catálogo de Funciones y Clases
- `get_ubicaciones(material: str, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Obtiene las ubicaciones de un material específico.
- `dashboard(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Vista principal del Dashboard con KPIs y búsqueda rápida.
- `dashboard_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - API JSON para el Dashboard con KPIs y búsqueda rápida.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `stock_levels`, `warehouse_tasks`
- **Columnas:**
  - `stock_levels`: `ubicacion_bin`, `Ubicación`, `ubicacin`, `denominacion`, `Texto breve de material`, `material`, `UMB`, `Stock disp`, `ubic_actual`
  - `warehouse_tasks`: `ubic_dest`, `fecha_conf`, `fe_creac`, `texto_breve_material`, `material`, `tp_dest`, `ubic_dest`

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `logging`
  - `sqlite3`
  - `itertools`
  - `pandas`
  - `datetime`
  - `timedelta`
  - `typing`
  
- **Archivos del Proyecto que Importan a este Archivo (`dashboard.py`):** Ninguno

- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.database.get_session_dep`
  - `fastapi.APIRouter`
  - `fastapi.Request`
  - `fastapi.Depends`
  - `fastapi.HTTPException`
  - `fastapi.responses.HTMLResponse`
  - `core.state.get_app_state`
  - `core.auth.get_current_user`
  - `core.app_instance.templates`
  - `services.dashboard_service.DashboardService`
  - `core.schemas.DashboardResponse`

- **Dirección del Flujo de Datos:**
  - Desde el endpoint hasta la base de datos para obtener los datos.
  - Desde el servicio hacia el endpoint para proporcionar el contexto del negocio.


---

## Archivo: ./routes/deliveries.py

### Resumen Funcional
Este archivo contiene rutas y funciones para el módulo de análisis de entregas en un sistema de gestión de almacén (WMS). Ofrece endpoints para renderizar páginas web con datos de análisis y una API JSON que devuelve los mismos datos.

### Catálogo de Funciones y Clases
- `save_analytics_snapshot(session: Session, key: str, data: Dict[str, Any])` - Guarda una captura de las analíticas en la base de datos para carga instantánea.
- `load_analytics_snapshot(session: Session, key: str) -> Optional[Dict[str, Any]]` - Recupera la última captura de analíticas desde la base de datos.
- `analytics(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Renderiza la página principal de analíticas con caché multinivel (Memoria -> DB -> Cálculo).
- `sla_details(request: Request, type: str = "late", date: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Vista detallada de auditoría SLA.
- `get_non_palletized_details(user: str, clase_mov: str, db: Session = Depends(get_session_dep), current_user: Dict[str, Any] = Depends(get_current_user))` - Obtiene el listado detallado (hasta 200) de movimientos no paletizados para un usuario y tipo de movimiento específicos.
- `analytics_deliveries_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - API JSON para analíticas de Entregas (Outbound Deliveries).

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - `analytics_snapshots`: 
    - `key` (TEXT, PRIMARY KEY)
    - `data` (TEXT)
    - `updated_at` (TIMESTAMP)
  - `lx02_pendientes`
    - `otcuanto` (OTCQUANTO)
    - `material` (MATERIAL)
    - `stock_disp` (STOCK_DISP)
  - `inventory_movements`
    - `doc_mat` (DOC_MAT)
    - `usuario` (USUARIO)
    - `cmv` (CMV)
    - `alm` (ALM)
    - `ce` (CE)
    - `fe_contab` (FE_CONTAB)
    - `hora` (HORA)

### Estado y Variables Globales
- **Variables Globales:** Ninguna.
- **Estado de Sesión:** Utiliza el estado de la aplicación (`AppState`) para almacenar y recuperar datos en caché.

### Dependencias y Flujo
- **Librerías Externas:**
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

- **Archivos del Proyecto que Importan a Este Archivo:**
  - `routes/inventory.py`
  - `routes/tasks.py`
  - `routes/analytics_proyecciones.py`
  - `services/deliveries_service.py`

- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno.

**Flujo de Datos:** El archivo importa y utiliza funciones y clases de otros archivos para procesar datos, interactuar con la base de datos y renderizar vistas.


---

## Archivo: ./routes/docs.py

### Resumen Funcional
El archivo `docs.py` proporciona endpoints para generar y obtener la documentación del sistema de monitoreo de almacén (WMS). Ofrece una vista jerárquica de los archivos del proyecto con indicadores de si tienen documentación, así como la capacidad de leer el contenido de las documentaciones en formato Markdown.

### Catálogo de Funciones y Clases
- `get_docs_tree(state: AppState = Depends(get_app_state))` - Genera un árbol de archivos del proyecto indicando cuáles tienen documentación.
- `get_doc_content(path: str, state: AppState = Depends(get_app_state))` - Obtiene el contenido de la documentación (.md) para un archivo específico.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa con ninguna base de datos.

### Estado y Variables Globales
- `BASE_DIR` - Directorio base del proyecto.
- `CACHE_DIR` - Directorio donde se almacenan las copias en caché de la documentación.

### Dependencias y Flujo
- **Dependencias**: Importa `os`, `fastapi`, `config`, `core.state`.
- **Flujo**:
  - `docs.py` importa a otros archivos del proyecto (`config.py`, `core/state.py`) para obtener dependencias globales y configuraciones.
  - Los endpoints son invocados por el framework FastAPI, que maneja las solicitudes HTTP.

El flujo de datos es unidireccional: los endpoints procesan las solicitudes HTTP y devuelven respuestas JSON.


---

## Archivo: ./routes/filters.py

### Resumen Funcional
El archivo `filters.py` contiene endpoints para filtrar entregas y calcular KPIs dinámicos en un sistema de monitoreo de almacén (WMS). Utiliza FastAPI para definir las rutas, SQLAlchemy para interactuar con la base de datos SQLite, y pandas para procesar los resultados.

### Catálogo de Funciones y Clases
- `_build_unified_where(date: str = None, area: str = None, centro: str = None, has_ots: str = None, min_week: str = None) -> tuple[str, dict]` - Construye una cláusula WHERE unificada basada en los criterios de filtro proporcionados.
- `filter_transactions(request: Request, date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Filtra entregas basándose en múltiples criterios.
- `get_kpis(date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Calcula KPIs dinámicos filtrados por área para el dashboard.
- `api_widget_data(query_id: str, request: Request, session: Session = Depends(get_session_dep))` - Endpoint de carga asíncrona para los componentes del Dashboard, lee visual_state, compila SQL y retorna los datos JSON directamente.

### Interacción con Base de Datos
- Motor de BD: SQLite.
- Tablas utilizadas:
  - `deliveries`
  - `warehouse_tasks`
- Columnas utilizadas:
  - `fecha_carga`, `fecha_sm_real`, `creado_el` (de la tabla `deliveries`)
  - `entrega` (de la tabla `warehouse_tasks`)
  - `estado_wms` (de la tabla `deliveries`)
  - `area` (de la tabla `deliveries`)
- Consultas SQL crudas: Sí, se utilizan consultas SQL generadas dinámicamente.

### Estado y Variables Globales
- Variables globales:
  - `DATE_EXPR`: Expresión unificada para la fecha de carga.
  - `ALLOWED_OTS_STATES`: Conjunto de estados OT permitidos como filtro.

### Dependencias y Flujo
- Librerías externas: pandas, fastapi, sqlalchemy.
- Archivos del proyecto que importa:
  - `core.database`
  - `core.models`
  - `core.query_engine`
  - `core.schemas`
  - `core.utils`
  - `repositories.deliveries`
- Archivos del proyecto que son importados por este archivo:
  - Ninguno.
- Flujo de datos: El archivo recibe solicitudes HTTP, procesa los parámetros, interactúa con la base de datos para obtener o calcular datos, y devuelve respuestas JSON.


---

## Archivo: ./routes/inventory.py

### Resumen Funcional
El archivo `inventory.py` contiene rutas y lógica para el análisis de inventario en un sistema de gestión de almacén (WMS). Ofrece una redirección a la página de analíticas de inventario y una API que devuelve datos de inventario en formato JSON.

### Catálogo de Funciones y Clases
- `analytics_inventory_redirect(request: Request, state: AppState = Depends(get_app_state))` - Redirige a la página de analíticas de inventario.
- `get_inventory_context(session: Session) -> Dict[str, Any]` - Obtiene el contexto completo del inventario.
- `analytics_inventory_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - API que devuelve datos de inventario en formato JSON.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos.

### Estado y Variables Globales
- `AppState` - Almacena el estado del sistema, incluyendo caché y indicadores de sincronización.
- `COST_CENTER_MAPPING` - Mapeo de centros de costo.

### Dependencias y Flujo
- **Dependencias Importadas**: 
  - `fastapi`, `sqlalchemy`, `pandas`, `datetime`, `typing`.
  - `core.auth`, `core.database`, `core.schemas`, `core.state`, `core.wms_config`, `repositories`, `routes.analytics_proyecciones`, `core.utils`, `services.inventory_service`.

- **Dependencias Exportadas**: 
  - No exporta ninguna dependencia.

- **Flujo de Datos**:
  - El archivo recibe una solicitud HTTP y utiliza servicios para obtener datos de inventario.
  - Los datos son procesados y devueltos en formato JSON a través de la API.


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
  - `io`, `logging`, `pandas`, `datetime`, `typing`, `fastapi`, `sqlalchemy`, `text`.
- **Archivos del Proyecto que Importa a este Archivo (Consumo):** Ninguno.
- **Archivos del Proyecto que Este Archivo Importa (Lo Consumen):**
  - `core.database.get_session_dep`
  - `repositories.deliveries.DeliveriesRepository`
  - `core.pdf_engine.WMS_Landscape_PDF`, `draw_delivery_page`, `get_ots_for_delivery`
  - `core.pdf_reports.draw_annex_table`, `draw_picking_list`

**Flujo de Datos:**
1. **Entrada:** Parámetros del formulario.
2. **Procesamiento:**
   - Consulta a la base de datos para obtener los datos necesarios.
   - Generación del PDF utilizando las funciones definidas en `core.pdf_engine` y `core.pdf_reports`.
3. **Salida:** Respuesta HTTP con el contenido del PDF.

**Flujo Inverso:**
1. **Entrada:** Archivos del proyecto que consumen este archivo.
2. **Procesamiento:** No aplica.
3. **Salida:** No aplica.


---

## Archivo: ./routes/productivity.py

### Resumen Funcional
Este archivo contiene endpoints para obtener datos de productividad en un sistema de almacén (WMS) utilizando FastAPI. Ofrece información diaria y mensual de productividad, así como detalles sobre movimientos de usuarios.

### Catálogo de Funciones y Clases
- `get_available_dates(user: User, session: Session)` - Retorna las fechas disponibles para el análisis de productividad.
- `get_productivity_dashboard(date: str = Query(None), user: User, session: Session, state: AppState)` - Retorna los datos del dashboard de productividad para una fecha específica o la fecha anterior si no se especifica.
- `get_monthly_productivity(month: str = Query(None), user: User, session: Session, state: AppState)` - Retorna los KPIs mensuales de productividad para un mes específico o el mes actual si no se especifica.
- `get_user_movements_summary(date: str, usuario: str, user: User, session: Session)` - Retorna el resumen diario de movimientos de un usuario.
- `get_user_movements_details(date: str, usuario: str, operacion: str, user: User, session: Session)` - Retorna los detalles diarios de movimientos de un usuario para una operación específica.
- `get_user_movements_monthly_summary(month: str, usuario: str, user: User, session: Session)` - Retorna el resumen mensual de movimientos de un usuario.
- `get_user_movements_monthly_details(month: str, usuario: str, operacion: str, user: User, session: Session)` - Retorna los detalles mensuales de movimientos de un usuario para una operación específica.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas y Columnas:
  - `ProductivityDailyService` interactúa con tablas relacionadas con la productividad diaria.
  - `ProductivityMonthlyService` interactúa con tablas relacionadas con la productividad mensual.

### Estado y Variables Globales
- No hay variables globales explícitas en este archivo. Se utilizan dependencias para obtener el estado de la aplicación (`AppState`) y la sesión de base de datos (`Session`).

### Dependencias y Flujo
- **Librerías Externas**: FastAPI, SQLAlchemy.
- **Archivos del Proyecto que Importa**:
  - `core.database.get_session_dep`
  - `core.auth.get_current_user`
  - `services.productivity_daily.ProductivityDailyService`
  - `services.productivity_monthly.ProductivityMonthlyService`
  - `core.state.get_app_state`
- **Archivos del Proyecto que Son Importados por Este**:
  - Ninguno
- **Dirección del Flujo de Datos**: Los endpoints reciben datos de entrada (fechas, usuarios), los procesan a través de servicios y repositorios, y devuelven resultados al cliente.


---

## Archivo: ./routes/settings.py

### Resumen Funcional
El archivo `settings.py` proporciona una API para la gestión dinámica de configuraciones SaaS en un sistema de monitoreo de almacén (WMS). Permite actualizar y consultar configuraciones, estados de mapeo, centros de costo, feriados y consultas SQL.

### Catálogo de Funciones y Clases
- `invalidate_caches(db: Session)` - Limpia el caché global en memoria y elimina todos los snapshots de base de datos.
- `settings_view(request: Request, db: DBSession, state: AppState = Depends(get_app_state))` - Renderiza el panel de control de configuraciones SaaS.
- `api_get_settings(state: AppState = Depends(get_app_state))` - Retorna las configuraciones generales.
- `api_update_setting(update: SettingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Actualiza una configuración específica.
- `api_upsert_status(update: StatusMappingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Inserta o actualiza un estado de mapeo.
- `api_delete_status(code: str, db: DBSession, state: AppState = Depends(get_app_state))` - Elimina un estado de mapeo.
- `api_upsert_cost_center(update: CostCenterMappingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Inserta o actualiza un centro de costo.
- `api_delete_cost_center(code: str, db: DBSession, state: AppState = Depends(get_app_state))` - Elimina un centro de costo.
- `api_add_holiday(h: HolidayAdd, db: DBSession, state: AppState = Depends(get_app_state))` - Añade un feriado.
- `api_sync_holidays(db: DBSession, state: AppState = Depends(get_app_state))` - Sincroniza automáticamente los feriados nacionales (Chile).
- `api_delete_holiday(date_str: str, db: DBSession, state: AppState = Depends(get_app_state))` - Elimina un feriado.
- `api_get_query(query_id: str, db: DBSession, state: AppState = Depends(get_app_state))` - Retorna el estado visual de una consulta del Analytics Studio.
- `api_update_query(update: QueryUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Persiste el estado visual de una consulta.
- `api_get_schema(db: DBSession, state: AppState = Depends(get_app_state))` - Retorna el catálogo semántico de datos para el editor.
- `api_preview_table(dataset_id: str, db: DBSession, state: AppState = Depends(get_app_state))` - Previsualiza una tabla.
- `api_query_preview(update: QueryUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Ejecuta una consulta temporal y retorna datos para previsualización.
- `api_build_sql(payload: VisualQueryBuilderPayload, db: DBSession, state: AppState = Depends(get_app_state))` - Compila el estado visual del constructor en SQL parametrizado seguro.
- `api_export_missing_orders(db: DBSession, state: AppState = Depends(get_app_state))` - Exporta órdenes sin ceco a un archivo Excel.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `analytics_snapshots`
  - `status_mapping`
  - `cost_center_mapping`
  - `holiday`
  - `app_setting`
  - `config_query`
- Columnas:
  - `analytics_snapshots`: Todas las columnas de la tabla.
  - `status_mapping`: `code`, `label`.
  - `cost_center_mapping`: `center_code`, `business_area`.
  - `holiday`: `date_str`.
  - `app_setting`: `key`, `value`.
  - `config_query`: `query_id`, `visual_state`.

### Estado y Variables Globales
- No se detectan variables globales, de sesión o de entorno.

### Dependencias y Flujo
- **Dependencias Externas**: FastAPI, SQLAlchemy, Pandas.
- **Archivos del Proyecto que Importa**:
  - `core.auth.require_admin`
  - `core.database.get_session_dep`
  - `core.models.StatusMapping`, `CostCenterMapping`, `AppSetting`, `Holiday`, `ConfigQuery`
  - `core.db_config_manager.load_config_to_memory`, `get_setting`, `get_status_mapping`, `get_cost_center_mapping`, `get_holidays`
  - `core.app_instance.templates`
  - `core.utils.sanitize_for_json`
  - `core.state.AppState`, `get_app_state`
- **Archivos del Proyecto que Son Importados por Este**:
  - No se detectan archivos que importen a este archivo.
- **Flujo de Datos**: El flujo de datos pasa a través de la API, interactúa con la base de datos para leer y escribir datos, y devuelve respuestas al cliente.


---

## Archivo: ./routes/sync.py

### Resumen Funcional
Este archivo contiene rutas para la sincronización de datos en un sistema de monitoreo de almacén (WMS). Permite iniciar y gestionar procesos de sincronización en segundo plano utilizando `TaskManager`, y proporciona endpoints para consultar el estado de las tareas.

### Catálogo de Funciones y Clases
- `get_tunnel_url(state: AppState = Depends(get_app_state))` - Retorna la URL pública del túnel (Ngrok).
- `get_sync_status(state: AppState = Depends(get_app_state))` - Retorna el estado actual de la sincronización.
- `sync_data(state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Inicia el proceso de sincronización de datos y lo encola en `TaskManager`.
- `list_tasks(limit: int = 20, state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Lista las tareas recientes del sistema.
- `get_task(task_id: str, state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Consulta el estado de una tarea específica por su ID.
- `_run_sync_pipeline()` - Ejecuta el pipeline completo de limpieza y consolidación.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - `analytics_snapshots`
  - Tablas específicas dependen del contenido de los directorios (`deliveries_path`, `stock_path`, `tasks_path`, `inventory_path`, `lx02_pendientes_path`) que se procesan en `_run_sync_pipeline`.
- **Consultas SQL Crudas:** No hay consultas SQL crudas directamente en este archivo. Se utilizan métodos de ORM.

### Estado y Variables Globales
- **Variables Globales:**
  - `DB_PATH`
  - `CLEANSED_DIR`
  - `PDF_STORAGE`
  - `DELIVERIES_DIR`
  - `STOCK_DIR`
  - `TASKS_DIR`
  - `INVENTORY_DIR`
  - `TUNNEL_URL_FILE`

### Dependencias y Flujo
- **Librerías Externas:**
  - `logging`
  - `shutil`
  - `pathlib`
  - `typing`
  - `fastapi`
  - `core.auth`
  - `config`
  - `core.state`
  - `core.task_manager`
  - `db.consolidator`

- **Archivos del Proyecto que Importan a este Archivo:**
  - `routes/transporte.py` (importado dentro de `_run_sync_pipeline`)

- **Archivos del Proyecto que Este Archivo Importa:**
  - No hay imports directos desde otros archivos en este fragmento.

- **Dirección del Flujo de Datos:**
  - Los datos fluyen a través de los endpoints para iniciar y gestionar la sincronización, luego se procesan en `_run_sync_pipeline` que interactúa con las tablas de la base de datos y realiza operaciones de ETL.


---

## Archivo: ./routes/tasks.py

### Resumen Funcional
El archivo `tasks.py` contiene la definición de una ruta FastAPI para obtener analíticas de tareas en un sistema de almacén (WMS). La ruta permite recuperar datos de tareas, aplicar un contexto limpio y almacenar los resultados en caché.

### Catálogo de Funciones y Clases
- `get_tasks_context(session: Session) -> dict` - Obtiene el contexto completo de las tareas utilizando el servicio `TasksService`.
- `analytics_tasks_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Ruta FastAPI que devuelve analíticas de tareas en formato JSON.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos. Utiliza el servicio `TasksService` para obtener los datos necesarios.

### Estado y Variables Globales
- `state.get_cache("/api/v1/analytics/tasks")` - Recupera el contexto de las tareas desde el caché.
- `state.set_cache("/api/v1/analytics/tasks", clean_context.copy())` - Almacena el contexto limpio en el caché.

### Dependencias y Flujo
- **Dependencias Importadas**: 
  - `get_current_user`, `get_session_dep`, `get_app_state` desde `core.auth`, `core.database`, `core.state`.
  - `TasksService` desde `services.tasks_service`.
  - `AnalyticsTasksResponse` desde `core.schemas`.

- **Archivos que Importan a este Archivo**: Ninguno.

- **Flujo de Datos**:
  1. La función `analytics_tasks_api` se invoca cuando un usuario accede a la ruta `/api/v1/analytics/tasks`.
  2. Se intenta recuperar el contexto de las tareas desde el caché.
  3. Si no está en caché, se obtiene el contexto completo utilizando `TasksService`.
  4. El contexto se limpia eliminando ciertas claves (`'request', 'user', 'is_syncing'`).
  5. El contexto limpio se almacena en caché y se devuelve como respuesta JSON.

Este flujo asegura que los datos de tareas sean recuperados eficientemente, utilizando el caché cuando sea posible para mejorar el rendimiento.


---

## Archivo: ./routes/transporte.py

### Resumen Funcional
Este archivo contiene rutas para la sección de Transporte en un sistema de monitoreo de almacén (WMS). Permite sincronizar datos desde una base de datos externa, obtener datos consolidados diarios, buscar registros y servir archivos PDF.

### Catálogo de Funciones y Clases
- `sync_transporte_logic(session: Session)` - Lógica core para sincronizar la base de datos externa de OneDrive a local.
- `sync_transporte(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta para sincronizar datos de transporte manualmente.
- `get_transporte_data(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta que retorna los datos consolidados diarios ordenados cronológicamente.
- `search_transporte(q: str, session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta para buscar en la tabla cruda de transporte_entregas por OT, GD o OC.
- `serve_pdf(filename: str, user=Depends(get_current_user))` - Ruta que sirve el archivo PDF desde el disco.
- `get_pending_transporte(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta para buscar en transporte_entregas los documentos del año actual que NO han sido ingresados al inventario SAP (inventory_movements).

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:**
  - `transporte_entregas`
    - `ot`
    - `proveedor`
    - `gd`
    - `oc`
    - `bulto`
    - `servicio`
    - `archivo`
    - `fecha`
  - `transporte_diario`
    - `fecha` (PRIMARY KEY)
    - `total_entregas`
    - `pdf_path`
- **Consultas SQL Crudas:**
  - Creación de tablas si no existen.
  - Lectura de datos desde la base de datos externa.
  - Inserción de datos crudos en la tabla local.
  - Consolidación de datos diarios.
  - Mapeo de PDFs.

### Estado y Variables Globales
- `EXTERNAL_DB_PATH` - Ruta a la base de datos externa SQLite.
- `PDF_DIR_PATH` - Directorio donde se almacenan los archivos PDF.

### Dependencias y Flujo
- **Dependencias Externas:** `sqlite3`, `logging`
- **Archivos del Proyecto que Importan a este Archivo:**
  - `core.app_instance`
  - `core.database`
  - `core.auth`
- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno
- **Dirección del Flujo de Datos:** El archivo consume datos desde la base de datos externa y los almacena localmente, luego sirve datos a través de las rutas definidas.


---

## Archivo: ./routes/widgets.py

### Resumen Funcional
El archivo `widgets.py` contiene endpoints FastAPI que manejan la lógica de negocio para obtener datos de widgets en un sistema de monitoreo de almacén (WMS). Los endpoints permiten recuperar datos estructurados y detalles subyacentes de los widgets, aplicando filtros dinámicos basados en parámetros como año, área y segmentos.

### Catálogo de Funciones y Clases
- `get_widget_data(query_id: str, year: Optional[str] = None, area: Optional[str] = None, granularity: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user), state: AppState = Depends(get_app_state))` - Ejecuta el VisualQueryBuilderPayload y retorna la data estructurada.
- `get_widget_drilldown(query_id: str, segment: str, material: Optional[str] = None, year: Optional[str] = None, area: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user))` - Obtiene el detalle subyacente de un segmento de un widget.

### Interacción con Base de Datos
- **Motor:** SQLite
- **TABLAS:** `ConfigQuery`, `outbound_deliveries`
- **COLUMNAS:**
  - `ConfigQuery`: `query_id`, `visual_state`
  - `outbound_deliveries`: `fecha_carga`, `entrega`, `pos_`, `cantidad`, `dias_retraso`, `material`

### Estado y Variables Globales
- No se detectan variables globales, de sesión o de entorno.

### Dependencias y Flujo
- **Librerías Externas:** `fastapi`, `sqlalchemy`, `pandas`
- **Archivos del Proyecto que IMPORTA:**
  - `core.database`: `get_session_dep`
  - `core.models`: `ConfigQuery`
  - `core.auth`: `get_current_user`
  - `core.helpers.dynamic_executor`: `execute_visual_query`
  - `core.utils`: `sanitize_for_json`
  - `core.state`: `get_app_state`, `AppState`
- **Archivos del Proyecto que IMPORTAN a este archivo:**
  - No se detectan archivos que importen directamente a este archivo.

**Flujo de Datos:**
1. Los endpoints son invocados por clientes externos.
2. Se realizan consultas a la base de datos para obtener los estados visuales de los widgets y los datos necesarios.
3. Se aplican filtros dinámicos basados en los parámetros proporcionados.
4. Se ejecuta una consulta SQL dinámica o se utiliza un generador de consultas (`build_sql_from_payload`).
5. Los resultados son procesados y formateados para su presentación en el frontend.
6. Los datos procesados y formateados se devuelven al cliente.

**Nota:** Existe una duplicidad en la definición del endpoint `get_widget_drilldown`, lo cual debe ser corregido para evitar conflictos de rutas.


---

## Archivo: ./scripts/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./scripts/generate_graphify.py

### Resumen Funcional
El archivo `generate_graphify.py` es un script que ejecuta el proceso de generación y procesamiento de un mapa interactivo utilizando la herramienta Graphify. El script limpia cualquier salida anterior, configura las variables de entorno necesarias, ejecuta Graphify para generar el mapa, y luego realiza una serie de reemplazos en el HTML generado para adaptarlo al español e incluir traducciones específicas.

### Catálogo de Funciones y Clases
- `run_graphify()` - Inicia el escaneo con Graphify, limpia la salida anterior, ejecuta Graphify, y procesa el archivo HTML generado.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `ROOT_DIR` - Directorio raíz del proyecto.

### Dependencias y Flujo
- **Dependencias**: 
  - `os`
  - `subprocess`
  - `shutil`

- **Flujo**:
  - El archivo se ejecuta directamente (`if __name__ == "__main__":`).
  - Llama a la función `run_graphify()`.

El flujo de datos es simple: el script ejecuta Graphify, procesa su salida y guarda el resultado en un directorio específico dentro del proyecto.


---

## Archivo: ./scripts/main_processor.py

### Resumen Funcional
El archivo `main_processor.py` es el punto de entrada del sistema de monitoreo de almacén (WMS). Ejecuta un pipeline completo que incluye la validación de directorios, análisis de carpetas, consolidación de datos, enriquecimiento y procesamiento de movimientos y órdenes PM.

### Catálogo de Funciones y Clases
- `run_pipeline()` - Ejecuta el pipeline completo del WMS Analysis and Consolidation.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas Modificadas:**
  - `stock_levels`
  - `inventory_movements`
  - `iw39_orders`
- **Columnas Modificadas:** Dependientes de las tablas mencionadas.
- **Consultas SQL Crudas:** No se detectan consultas SQL crudas directamente en este archivo. Se usan ORM (Object Relational Mapping) para interactuar con la base de datos.

### Estado y Variables Globales
- `PROJECT_ROOT` - Ruta del proyecto.
- `DELIVERIES_DIR`, `STOCK_DIR`, `INVENTORY_DIR`, `IW39_DIR`, `CLEANSED_DIR`, `DATABASE_PATH`, `ONEDRIVE_PATH` - Directorios y rutas de archivos.

### Dependencias y Flujo
- **Librerías Externas:** `subprocess`, `sys`, `pathlib`, `logging`
- **Archivos Importados:**
  - `config.py` (para configuraciones globales)
  - `scripts/analyze_folder.py` (para análisis de carpetas)
  - `db.consolidator.DataConsolidator` (para consolidación de datos)
  - `services.etl.movements.InventoryMovementAdapter` (para procesamiento de movimientos)
  - `services.etl.iw39.IW39Processor` (para procesamiento de órdenes PM)
- **Archivos que Importan a este Archivo:** Ninguno

El flujo de datos es unidireccional, con el archivo principal (`main_processor.py`) invocando funciones y servicios para realizar las tareas necesarias.


---

## Archivo: ./services/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./services/dashboard_service.py

### Resumen Funcional
El archivo `dashboard_service.py` contiene la lógica del servicio para el dashboard principal de entregas en un sistema de monitoreo de almacén (WMS). El servicio delega todas las operaciones de base de datos a la clase `DeliveriesRepository`, y proporciona métodos para obtener datos necesarios para renderizar el dashboard, incluyendo gráficos de intensidad semanal, indicadores clave de rendimiento (KPIs), selectores del dashboard y transacciones recientes.

### Catálogo de Funciones y Clases
- `DashboardService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - **Parámetros**: 
    - `session`: Sesión de SQLAlchemy para interactuar con la base de datos.
  
- `get_full_context()` - Obtiene el contexto completo necesario para renderizar el dashboard.
  - **Retorno**:
    - Un diccionario que contiene gráficos de intensidad semanal, KPIs, selectores del dashboard y transacciones recientes.

### Interacción con Base de Datos
- **Motor**: SQLite (implícito a través de SQLAlchemy).
- **Tablas y Columnas**:
  - `DeliveriesRepository` interactúa con las siguientes tablas y columnas:
    - Tabla: `deliveries`
      - Columnas: Dependientes de la implementación de `get_weekly_intensity_chart`, `get_filtered_kpis`, `get_dashboard_selectors`, y `get_filtered_transactions`.
    - Tabla: `kpis`
      - Columnas: Dependientes de la implementación de `get_filtered_kpis`.
    - Tabla: `transactions`
      - Columnas: Dependientes de la implementación de `get_filtered_transactions`.

### Estado y Variables Globales
- **Ninguna**: No se utilizan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Librerías Externas**:
  - `logging`
  - `sqlalchemy.orm.Session`
  - `typing.Dict`, `typing.Any`, `typing.List`
  - `datetime.datetime`

- **Archivos del Proyecto que Importan a este Archivo (lo consumen)**:
  - Ninguna.

- **Archivos del Proyecto que Este Archivo IMPORTA (consume)**:
  - `repositories.deliveries.DeliveriesRepository`

- **Dirección del Flujo de Datos**:
  - El servicio recibe una sesión de base de datos y delega las operaciones de base de datos a `DeliveriesRepository`.
  - Los métodos de `DeliveriesRepository` interactúan con la base de datos para obtener los datos necesarios.
  - El servicio procesa estos datos y los devuelve en un formato que puede ser utilizado por la vista del dashboard.


---

## Archivo: ./services/deliveries_service.py

### Resumen Funcional
El archivo `deliveries_service.py` contiene la lógica del servicio de entregas para un sistema de monitoreo de almacén (WMS). Este servicio se encarga de generar el contexto completo para las entregas, incluyendo información sobre áreas de negocio y widgets configurados.

### Catálogo de Funciones y Clases
- `DeliveriesService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - **Propósito**: Prepara el servicio para interactuar con la base de datos proporcionada.
  
- `get_full_context() -> Dict[str, Any]` - Genera y devuelve un contexto completo para las entregas.
  - **Propósito**: Recopila y organiza información relevante desde la base de datos y otros servicios para proporcionar un contexto detallado.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `outbound_deliveries`
- **Columnas**:
  - `area_negocio`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**: 
  - `sqlalchemy.orm.Session`
  - `logging`
  - `typing.Dict`, `typing.Any`
  
- **Archivos del Proyecto que Importan a este Archivo**:
  - `routes.inventory.get_inventory_context`
  - `routes.tasks.get_tasks_context`
  - `routes.analytics_proyecciones.get_proyecciones_context`

- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno

- **Flujo de Datos**: 
  - El servicio recibe una sesión de base de datos y utiliza esta para consultar la tabla `outbound_deliveries`.
  - Luego, intenta cargar contextos adicionales desde otros servicios (`inventory`, `tasks`, `analytics_proyecciones`) y los combina en el contexto final.


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
- **Dependencias Externas**: Ninguna
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
- `logger` - Variable global que almacena el objeto de registro.

### Dependencias y Flujo
- Librerías externas:
  - `pandas`
  - `pathlib`
  - `sqlite3`
  - `typing`
  - `logging`
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
Ninguna.

### Dependencias y Flujo
- Librerías externas:
  - `pandas`
  - `pathlib`
  - `typing`
  - `sqlite3`
- Archivos del proyecto que importan a este archivo (`deliveries.py`):
  - No se mencionan dependencias específicas en el fragmento proporcionado.
- Archivos del proyecto que este archivo importa:
  - `base.py`
  - `wms_utils.py`

El flujo de datos es desde los archivos de entrada (Excel, TXT) hasta la base de datos SQLite, pasando por la limpieza y transformación de los datos en el adaptador.


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
- **Dependencias**: pandas, pathlib.
- **Flujo**: El archivo no importa ni es importado por otros archivos dentro del proyecto.


---

## Archivo: ./services/etl/movements.py

### Resumen Funcional
El archivo `movements.py` contiene una clase `InventoryMovementAdapter` que se encarga de procesar archivos CSV con movimientos del sistema WMS, validar su contenido, limpiar y transformar los datos para su almacenamiento en la base de datos SQLite.

### Catálogo de Funciones y Clases
- **Clase:** `InventoryMovementAdapter`
  - Propósito: Adaptador específico para procesar el formato WMS Movimientos.
  
- **Función:** `validate_file(file_path: Path) -> bool`
  - Propósito: Valida si el archivo CSV existe y contiene las columnas requeridas.

- **Función:** `_get_required_columns() -> List[str]`
  - Propósito: Devuelve una lista de columnas requeridas para el procesamiento del archivo.

- **Función:** `_get_primary_keys() -> List[str]`
  - Propósito: Devuelve una lista de claves primarias utilizadas en la base de datos.

- **Función:** `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame`
  - Propósito: Limpia y transforma el DataFrame, eliminando columnas vacías, renombrando columnas, normalizando valores y aplicando validaciones específicas.

- **Función:** `_vectorized_classify(df: pd.DataFrame) -> pd.DataFrame`
  - Propósito: Clasifica las operaciones según los valores en la columna 'cmv' y agrega una nueva columna 'tipo_operacion'.

- **Función:** `_post_process(conn, table_name: str)`
  - Propósito: Crea índices estructurales para mejorar el rendimiento de búsquedas en la tabla `inventory_movements`.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna (el archivo no realiza operaciones directas sobre tablas)
- Columnas: Ninguna (el archivo no realiza operaciones directas sobre columnas)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `pandas`, `numpy`
- **Archivos del Proyecto que Importa:** Ninguno
- **Archivos del Proyecto que Son Importados por Este Archivo:** `base.py` (dentro de la misma carpeta)
- **Dirección del Flujo de Datos:** El archivo recibe un DataFrame, lo limpia y transforma, y luego lo devuelve para su almacenamiento en la base de datos.


---

## Archivo: ./services/etl/stock.py

### Resumen Funcional
El archivo `stock.py` contiene una clase `StockLevelAdapter` que procesa archivos de inventario/stock en formato LX02, los limpia y carga en una base de datos SQLite. Realiza un REPLACE completo en la tabla especificada.

### Catálogo de Funciones y Clases
- **validate_file(file_path: Path) -> bool** - Valida si el archivo existe y contiene las columnas requeridas.
- **_get_required_columns() -> List[str]** - Devuelve las columnas clave del header SAP LX02.
- **read_and_clean_data(file_path: Path) -> pd.DataFrame** - Lee y limpia los datos del archivo, detectando automáticamente la fila de encabezado.
- **_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame** - Limpia el DataFrame eliminando filas y columnas vacías y normalizando los strings.
- **process_directory(folder_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int** - Combina todos los archivos en un directorio, limpia los datos y realiza un REPLACE completo en la tabla especificada.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (se opera sobre una tabla específica proporcionada como parámetro)
- **Columnas**: `Material`, `UMB`, `otcuanto`, `source_file`, `ingested_at`

### Estado y Variables Globales
- **logger**: Objeto de registro para el módulo.

### Dependencias y Flujo
- **Dependencias Externas**:
  - `pandas`
  - `pathlib`
  - `typing`
  - `sqlite3`
  - `os`
  - `datetime`
  - `logging`

- **Archivos del Proyecto que Importan a este Archivo**: Ninguno
- **Archivos del Proyecto que Este Archivo Importa**:
  - `./services/etl/base.py` (clase base `BaseWMSProcessor`)
  
- **Flujo de Datos**: 
  1. El archivo se procesa y limpia.
  2. Los datos son combinados en un DataFrame.
  3. El DataFrame se carga en la base de datos SQLite utilizando `to_sql` con `if_exists="replace"`.
  4. Se crea un índice en la columna `otcuanto`.


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
- **Dependencias Externas**: `pandas`, `pathlib`
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno.
- **Archivos del Proyecto que Este Archivo Importa**: `./services/etl/base.py` (clase `BaseWMSProcessor`)
- **Flujo de Datos**: El archivo importa la clase base y utiliza pandas para procesar archivos CSV, lo cual implica un flujo de datos desde el archivo hasta la limpieza y normalización del DataFrame.


---

## Archivo: ./services/inventory_service.py

### Resumen Funcional
El archivo `inventory_service.py` contiene la lógica de negocio para el servicio de inventario en un sistema de gestión de almacén (WMS). Genera un contexto completo que incluye estadísticas de eficiencia, datos históricos y otros detalles relevantes para el dashboard de movimientos.

### Catálogo de Funciones y Clases
- `InventoryService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `fmt_num(val)` - Formatea un número como una cadena con separadores de miles.
- `_get_latest_data_period()` - Obtiene el período más reciente de datos disponibles en la tabla `inventory_movements`.
- `_get_empty_context()` - Devuelve un contexto vacío con valores por defecto.
- `get_full_context()` - Genera y devuelve el contexto completo para el dashboard de movimientos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `inventory_movements`
- **Columnas:**
  - `fe_contab` (Fecha del movimiento)
  - `tipo_operacion` (Tipo de operación, ej. Ingreso/Consumo)
  - `registrado` (Fecha de registro)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `pandas`, `numpy`
- **Archivos del Proyecto que Importan a este Archivo:**
  - `repositories.InventoryRepository`
  - `core.utils.sanitize_for_json`
  - `core.state.get_app_state`
  - `core.wms_config.COST_CENTER_MAPPING`
- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno

**Flujo de Datos:**
1. El archivo se importa y se utiliza en el servicio principal.
2. Se inicia una sesión de base de datos (`InventoryService`).
3. Se ejecutan consultas SQL para obtener los datos necesarios.
4. Los resultados son procesados y formateados usando `pandas`.
5. El contexto completo es generado y almacenado en caché.

Este archivo es crucial para el funcionamiento del sistema de monitoreo de almacén, proporcionando las estadísticas y datos necesarios para el análisis y visualización de los movimientos de inventario.


---

## Archivo: ./services/productivity_daily.py

### Resumen Funcional
El archivo `productivity_daily.py` contiene el servicio para calcular y devolver los KPIs de productividad diarios basados en las tareas asignadas. El servicio utiliza una sesión de SQLAlchemy para interactuar con la base de datos y un repositorio de tareas para obtener los datos necesarios.

### Catálogo de Funciones y Clases
- `ProductivityDailyService(session: Session)` - Inicializa el servicio con una sesión de SQLAlchemy.
  - Parámetros:
    - `session`: Sesión de SQLAlchemy para interactuar con la base de datos.
- `get_available_dates()` - Devuelve las fechas disponibles en los registros de tareas.
- `get_productivity_data(target_date: str)` - Retorna todos los KPIs de productividad para una fecha específica (YYYY-MM-DD).
  - Parámetros:
    - `target_date`: Fecha objetivo en formato YYYY-MM-DD.
  - Propósito: Calcula y devuelve los KPIs de productividad para la fecha especificada, incluyendo resúmen diario, tendencia horaria, brechas de inactividad y mapa de actividad.
- `get_user_movements_daily_summary(target_date: str, usuario: str)` - Devuelve el resumen de movimientos diarios por usuario.
  - Parámetros:
    - `target_date`: Fecha objetivo en formato YYYY-MM-DD.
    - `usuario`: Nombre del usuario.
- `get_user_movements_daily_details(target_date: str, usuario: str, operacion: str)` - Devuelve los detalles de los movimientos diarios por usuario y operación específica.
  - Parámetros:
    - `target_date`: Fecha objetivo en formato YYYY-MM-DD.
    - `usuario`: Nombre del usuario.
    - `operacion`: Tipo de operación.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas:
  - **tasks_repo.get_available_dates()**: Lee las fechas disponibles en la tabla `tasks`.
  - **tasks_repo._get_daily_summary(date_sap)**, **tasks_repo._get_hourly_trend(date_sap)**, **tasks_repo._get_inactivity_gaps(date_sap)**, **tasks_repo._get_activity_heatmap(date_sap)**: Lee datos de las tablas `tasks`, `inventory_movements`, y posiblemente otras dependiendo del contexto.
  - **tasks_repo.get_user_movements_daily_summary(target_date, usuario)**, **tasks_repo.get_user_movements_daily_details(target_date, usuario, operacion)**: Leerán datos de la tabla `tasks` y posiblemente otras tablas relacionadas.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías Externas:
  - `logging`
  - `typing`
  - `sqlalchemy.orm`
  - `re` (módulo de expresiones regulares)
- Archivos del Proyecto que Importan a este archivo (`productivity_daily.py`):
  - Ninguno
- Archivos del Proyecto que Este Archivo Importa:
  - `repositories.tasks`

**Flujo de Datos:**
1. **Entrada**: Fecha objetivo (YYYY-MM-DD).
2. **Procesamiento**:
   - Convierte la fecha al formato SAP (DD.MM.YYYY) si es necesario.
   - Llama a métodos del repositorio para obtener resúmen diario, tendencia horaria, brechas de inactividad y mapa de actividad.
3. **Salida**: Diccionario con los KPIs de productividad.

**Flujo Inverso:**
- No aplica


---

## Archivo: ./services/productivity_monthly.py

### Resumen Funcional
El archivo `productivity_monthly.py` contiene servicios para calcular y obtener datos de productividad mensuales en un sistema de almacén (WMS). Ofrece métodos para obtener resúmenes de productividad mensuales, movimientos diarios de usuarios y detalles específicos de operaciones.

### Catálogo de Funciones y Clases
- `ProductivityMonthlyService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - `get_monthly_productivity_data(target_month: str) -> Dict[str, Any]` - Calcula y devuelve los KPIs de productividad para un mes específico (YYYY-MM).
  - `get_user_movements_monthly_summary(target_month: str, usuario: str) -> list` - Obtiene el resumen de movimientos diarios de un usuario para un mes.
  - `get_user_movements_monthly_details(target_month: str, usuario: str, operacion: str) -> list` - Obtiene los detalles específicos de una operación de movimiento diario de un usuario para un mes.

### Interacción con Base de Datos
- Motor de BD: SQLite.
- Tablas y Columnas:
  - `tasks_repo._get_monthly_summary(month_sap)` - Lee datos de la tabla que contiene resúmenes mensuales de tareas.
  - `tasks_repo._get_monthly_shifts(month_sap)` - Lee datos de la tabla que contiene información sobre los turnos diarios.
  - `tasks_repo._get_monthly_heatmap(month_sap)` - Lee datos de la tabla que contiene mapas térmicos de productividad.

### Estado y Variables Globales
- Ninguna.

### Dependencias y Flujo
- Librerías externas: `logging`, `typing`.
- Archivos del proyecto que importa:
  - `repositories.tasks` - Importado en el constructor de la clase `ProductivityMonthlyService`.
- Archivos del proyecto que son importados por este archivo:
  - Ninguno.
- Flujo de datos:
  - El servicio recibe una sesión de base de datos y utiliza un repositorio para acceder a los datos necesarios. Los resultados se procesan y devuelven en formato JSON.

Este archivo es parte de la capa de servicios del sistema, donde se encapsulan las lógicas de negocio relacionadas con el cálculo y obtención de datos de productividad mensuales.


---

## Archivo: ./services/tasks_service.py

### Resumen Funcional
El archivo `tasks_service.py` contiene la lógica del servicio para gestionar y analizar las Operaciones Técnicas (OTs) en el sistema de monitoreo de almacén (WMS). Genera un contexto analítico que incluye resúmenes, tendencias, usuarios involucrados, tipos de OTs, movimientos no paletizados y KPIs dinámicos.

### Catálogo de Funciones y Clases
- `TasksService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `get_full_context()` - Genera y cachea el contexto analítico para la gestión de OTs.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: `config_queries`
    - Columnas: `sql_text`, `visual_state`, `query_id`
  - Tabla: No especificadas explícitamente, pero se usan consultas SQL crudas para leer datos.
- **Consultas SQL Crudas:** Se realizan consultas SQL para obtener resúmenes y KPIs dinámicos.

### Estado y Variables Globales
- **Variables Globales:** Ninguna.
- **Estado de Sesión:** Utiliza `get_app_state()` para acceder al estado de la aplicación, que incluye el caché.
- **Diccionarios Quemados:** Ninguno.

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `sqlalchemy`
  - `logging`
  - `datetime`
- **Archivos del Proyecto que Importa:**
  - `repositories/TasksRepository.py`
  - `core/state.py`
  - `core/utils.py`
- **Archivos del Proyecto que Son Importados por Este Archivo:**
  - Ninguno.
- **Dirección del Flujo de Datos:** El flujo de datos comienza con la solicitud de contexto, pasa a través del servicio para generar los datos necesarios y finalmente devuelve el contexto analítico.


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

- `_run_loop()` - Bucle principal del servicio de ngrok.
  - Propósito: Maneja el ciclo de vida del túnel, reiniciándolo si es necesario.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa con ninguna base de datos.

### Estado y Variables Globales
- `_service_lock` - Un objeto `threading.Lock()` para proteger el acceso al servicio global.
- `_global_service` - Una variable global que almacena la instancia singleton del servicio de ngrok.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `os`, `subprocess`, `threading`, `time`, `urllib.request`, `json`, `logging`
  
- **Archivos Importados**:
  - `config.py` (para las constantes `NGROK_BIN` y `TUNNEL_URL_FILE`)
  
- **Flujo de Datos**:
  - El archivo se importa por otros archivos del proyecto para iniciar o detener el servicio de túnel.
  - Los métodos `_run_loop`, `start`, y `stop` manejan la lógica interna del servicio, mientras que las funciones `start_tunnel` y `stop_tunnel` proporcionan una interfaz segura y thread-safe para interactuar con el servicio.


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
Este archivo define un módulo para gestionar el estado visual de gráficos en una aplicación de análisis. Permite obtener y establecer el estado visual de diferentes consultas, así como mantener mapeos predefinidos para inicializar gráficos con configuraciones específicas.

### Catálogo de Funciones y Clases
- `AnalyticsStudioManager.getVisualState(queryId)` - Obtiene el estado visual asociado a una consulta específica.
- `AnalyticsStudioManager.setVisualState(queryId, state)` - Establece el estado visual para una consulta específica.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `studioChartInstance` - Instancia del gráfico actual.
- `currentSchema` - Esquema actual (no se usa en este fragmento).
- `currentQueryId` - ID de la consulta actual.
- `serverVisualState` - Estado visual del servidor (no se usa en este fragmento).
- `visualState` - Puntero al estado activo del modal.

### Dependencias y Flujo
- No depende de ninguna librería externa.
- Este archivo no importa a otros archivos ni es importado por otros archivos.


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
El archivo `analytics_studio_ui.js` contiene funciones y métodos para gestionar la interfaz de usuario del Studio de Análíticas, permitiendo la edición, visualización y publicación de consultas. Incluye lógica para cargar esquemas de base de datos, previsualizar tablas, ejecutar consultas y manejar filtros y configuraciones visuales.

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
- `refreshQbColumns(forceState = false)` - Refresca los selectores de columnas para el Constructor Visual.
- `renderFilters()` - Renderiza los filtros en la interfaz de usuario.
- `addFilter()` - Añade un nuevo filtro.
- `updateFilterType(index, type)` - Actualiza el tipo de valor del filtro.
- `updateFilter(index)` - Actualiza los detalles del filtro seleccionado.
- `removeFilter(index)` - Elimina un filtro.
- `onSecondMetricToggle()` - Maneja el toggle de la Segunda Métrica.
- `onQbChange()` - Sincroniza los cambios en la configuración del Constructor Visual con el estado actual.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - No se especifican tablas explícitas, pero se hacen solicitudes a endpoints como `/api/queries/{queryId}`, `/api/studio/schema`, y `/api/studio/preview_table/{tableName}`.
- Columnas:
  - No se especifican columnas explícitas, pero las solicitudes implican operaciones en tablas de consultas y esquemas.

### Estado y Variables Globales
- `currentQueryId` - ID de la consulta actualmente seleccionada.
- `serverVisualState` - Estado visual del servidor para la consulta actual.
- `visualState` - Estado visual actual del Constructor Visual.
- `currentSchema` - Esquema actual de la base de datos.

### Dependencias y Flujo
- **Dependencias Externas**: No se mencionan dependencias externas específicas.
- **Archivos Importados**:
  - Ninguno especificado en el fragmento proporcionado.
- **Archivos Exportados**:
  - Ninguno especificado en el fragmento proporcionado.
- **Flujo de Datos**:
  - El flujo de datos se gestiona principalmente a través de la interfaz de usuario y las solicitudes HTTP al backend.


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
Este archivo JavaScript (`productivity_daily.js`) se encarga de manejar la interacción del usuario con los gráficos y tablas diarias de productividad en el sistema de monitoreo de almacén (WMS). Permite filtrar datos por usuarios, cargar datos según una fecha seleccionada, y renderizar diferentes KPIs como gráficos de tendencia, resúmenes de actividad, baches en la productividad y un mapa de calor.

### Catálogo de Funciones y Clases
- `toggleDailyUserFilter()` - Muestra u oculta el filtro de usuarios diarios.
- `renderDailyUserCheckboxes(summary)` - Renderiza los checkboxes para filtrar por usuarios.
- `toggleAllDailyUsers()` - Selecciona/deselecciona todos los usuarios en el filtro.
- `onDailyUserCheckboxChange()` - Maneja el cambio en la selección de usuarios.
- `renderFilteredDaily()` - Renderiza los KPIs filtrados según la selección de usuarios.
- `loadProductivityData()` - Carga los datos diarios de productividad desde una API y actualiza la interfaz.
- `renderKPI1(summary)` - Renderiza el resumen de actividad diaria.
- `renderKPI2(trend)` - Renderiza la tendencia de movimientos del equipo.
- `renderKPI3(gaps)` - Renderiza los baches en la productividad.
- `renderKPI4(heatmapData)` - Renderiza el mapa de calor de productividad.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a una base de datos.

### Estado y Variables Globales
- `productivityTrendChartInst` - Instancia del gráfico de tendencia.
- `currentDailyData` - Datos diarios actuales cargados.
- `selectedDailyUsers` - Usuarios seleccionados para el filtro.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `Chart.js` (para renderizar gráficos).
  
- **Archivos del Proyecto que Importan a este Archivo**:
  - `dashboard.js` (se espera que contenga la función `switchSubTab`).

- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno.

- **Flujo de Datos**: 
  - El archivo se ejecuta cuando el DOM esté listo (`DOMContentLoaded`).
  - Se manejan eventos como cambios en los filtros y selecciones.
  - Los datos diarios se cargan a través de una llamada `fetch` a la API `/api/v1/analytics/productivity`.
  - Los KPIs se renderizan basándose en los datos recibidos.


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

## Archivo: ./static/js/saas_engine_core.js

### Resumen Funcional
El archivo `saas_engine_core.js` es un motor SaaS V2 que se encarga de leer contenedores con la clase `.saas-widget-v2`, renderizar gráficos o KPIs según los parámetros proporcionados, y actualizarlos dinámicamente.

### Catálogo de Funciones y Clases
- `initSaaSWidgetsV2(params = null, rootElement = document)` - Inicializa los widgets SaaS V2 en el elemento raíz especificado o en todo el documento si no se proporciona ninguno. Recibe parámetros para filtrar los datos.

### Interacción con Base de Datos
- **Motor**: Ninguna.
- **Tablas y Columnas**: No hay consultas SQL explícitas ni llamadas a ORM detectadas en este archivo.

### Estado y Variables Globales
- `window.saasChartInstancesV2` - Almacena instancias de gráficos Chart.js para widgets individuales.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `ChartDataLabels` (plugin para Chart.js).
- **Archivos del Proyecto que Importan a este Archivo**:
  - Ninguno.
- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno.

El flujo de datos es el siguiente: el archivo se ejecuta al cargar la página, inicia los widgets SaaS V2 y actualiza dinámicamente sus contenidos según los parámetros proporcionados.


---

## Archivo: ./static/js/saas_engine_drilldown.js

### Resumen Funcional
El archivo `saas_engine_drilldown.js` contiene funciones para abrir y gestionar un modal de detalles con una tabla dinámica que muestra datos filtrados y ordenables. El contenido se carga a través de una API RESTful.

### Catálogo de Funciones y Clases
- `window.openDrilldownModal(queryId, segmentLabel, materialId = null)` - Abre el modal de detalles con los datos filtrados según la consulta y segmento proporcionados.
- `window.sortDrilldownTable(n)` - Ordena las filas de la tabla por la columna especificada.
- `window.filterDrilldownTable()` - Filtra las filas de la tabla según los valores ingresados en los campos de búsqueda.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos. Los datos se cargan a través de una API RESTful.

### Estado y Variables Globales
- `window.filterDrilldownTableTimer` - Variable global que almacena el temporizador para la función de filtrado.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas mencionadas.
- **Flujo de Datos**:
  - El archivo se importa en otros archivos del proyecto (consumido por ellos).
  - Otros archivos del proyecto pueden importar este archivo para usar sus funciones (`window.openDrilldownModal`, `window.sortDrilldownTable`, `window.filterDrilldownTable`).


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
El archivo `dashboard.html` es una plantilla HTML para el panel de control del sistema de monitoreo de almacén (WMS). Contiene la interfaz de usuario principal que incluye encabezado, indicadores clave (KPIs), menú de acciones y contenido principal dividido en sidebar y tabla.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada directamente en este archivo HTML. Todas las interacciones son realizadas a través de JavaScript y eventos del usuario.

### Interacción con Base de Datos
Ninguna. El archivo no contiene consultas SQL ni llamadas a ORM para interactuar con una base de datos.

### Estado y Variables Globales
- `is_syncing`: Variable que indica si la sincronización está en curso.
- `user`: Objeto que contiene información del usuario autenticado, incluyendo su nombre de usuario y rol.
- `kpi_deliveries`, `sub_del_abierta`, `sub_del_no_tratada`, `sub_del_reunido`, `sub_del_atrasado`, `sub_del_critico`: Variables que almacenan los valores de KPIs relacionados con las entregas.
- `kpi_materials`, `sub_mat_abierta`, `sub_mat_no_tratada`, `sub_mat_reunido`, `sub_mat_atrasado`, `sub_mat_critico`: Variables que almacenan los valores de KPIs relacionados con los materiales solicitados.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas directamente en este archivo.
- **Flujo de Datos**: El flujo de datos pasa por el servidor (FastAPI) que renderiza esta plantilla HTML, pasando los valores de las variables globales como contexto. Los eventos del usuario (clics en botones, cambios en la interfaz) se manejan con JavaScript.

Este archivo es una vista HTML que presenta información y permite interacciones al usuario, pero no realiza ninguna operación directamente relacionada con la base de datos o el backend del sistema.


---

## Archivo: ./templates/deliveries.html (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para la interfaz de usuario del sistema de monitoreo de almacén (WMS). Contiene el diseño y las funcionalidades necesarias para mostrar diferentes secciones como entregas, movimientos, consumos, etc., con un menú de pestañas interactiva.

### Catálogo de Funciones y Clases
- `switchTab(tabId, btnElement)` - Cambia la pestaña activa.
- `switchSubTab(subTabId, btnElement)` - Cambia la subpestaña activa.
- `openNonPalletizedDetails(user, claseMov)` - Abre un modal con detalles no paletizados.
- `initTableFilters()` - Inicializa los filtros de tablas.
- `filterOTTable()` - Filtra la tabla de OTs según los criterios seleccionados.
- `filterDiscrepancyTable()` - Filtra la tabla de discrepancias según los criterios seleccionados.
- `sortTableDiscrepancy(columnIndex)` - Ordena la tabla de discrepancias.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
No hay variables globales explícitas definidas en el código. Las variables están almacenadas en elementos `<script type="application/json">` que contienen datos JSON serializados.

### Dependencias y Flujo
- **Librerías externas**: Chart.js, marked.js, Font Awesome.
- **Archivos del proyecto importados**:
  - `partials/_styles.html`
  - `css/deliveries.css`, `css/inventory.css`, `css/analytics_proyecciones.css`
  - `js/core_ui.js`, `js/dashboard_api.js`, `js/dashboard_core.js`, `js/dashboard_saas.js`, `js/saas_engine_core.js`, `js/saas_engine_drilldown.js`, `js/deliveries.js`, `js/consumos.js`, `js/transporte.js`
- **Archivos del proyecto que importan a este archivo**: No especificados en el fragmento.

El flujo de datos se gestiona principalmente mediante eventos JavaScript y la manipulación del DOM.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para el sistema de monitoreo de almacén (WMS). Contiene variables JSON que se utilizan en scripts JavaScript y carga varios archivos JavaScript adicionales.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `ots_trend_created`
- `ots_trend_confirmed`
- `ots_user_labels`
- `ots_user_created`
- `ots_user_confirmed`
- `ots_type_labels`
- `ots_type_data`

### Dependencias y Flujo
- Archivos JavaScript:
  - `js/tasks.js` (versión 5)
  - `js/inventory.js` (versión 21)
  - `js/analytics_proyecciones.js` (versión 3)
  - `js/docs_explorer.js` (versión 5)
  - `js/productivity_daily.js` (versión 2)
  - `js/productivity_monthly.js` (versión 2)
  - `js/productivity_modals.js` (versión 2)

- Archivos HTML incluidos:
  - `_modals.html`
  - `_deliveries_modals.html`
  - `_inventory_modals.html`
  - `_analytics_proyecciones_modals.html`
  - `_edit_query_modal.html`
  - `_quick_login_modal.html`
  - `_logout.html`

El archivo `deliveries.html` carga varios scripts JavaScript y partials HTML, lo que indica un flujo de datos hacia el cliente para la visualización y interacción con los datos del sistema de almacén.


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
Este archivo contiene el código HTML para un modal de edición de consultas en el sistema de monitoreo de almacén (WMS). El modal incluye un constructor visual interactivo que permite a los usuarios crear y editar consultas SQL de manera gráfica.

### Catálogo de Funciones y Clases
No se detectaron funciones o clases específicas dentro del fragmento HTML proporcionado.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `editQueryId`: Un input oculto que almacena el ID de la consulta actualmente siendo editada.

### Dependencias y Flujo
- **Dependencias**: No se detectaron dependencias externas directamente en este fragmento HTML.
- **Archivos Importados**: El archivo importa scripts JavaScript desde rutas estáticas (`analytics_studio_config.js`, `analytics_studio_renderer.js`, `analytics_studio_ui.js`).
- **Flujo de Datos**: No se detectó un flujo de datos específico dentro del fragmento HTML proporcionado.


---

## Archivo: ./templates/partials/_inventory_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para varios modales en una interfaz de usuario, cada uno relacionado con diferentes aspectos del sistema de monitoreo de almacén (WMS). Los modales muestran información detallada sobre el consumo específico, actividad del asistente, materiales más movimientos, desglose de ubicación, curva ABC, frecuencia semanal y top materiales.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada en este fragmento HTML.

### Interacción con Base de Datos
Ninguna. Este archivo solo contiene código HTML y no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
Ninguna variable global, de sesión o diccionario quemado en el código que almacene estado crítico.

### Dependencias y Flujo
Ninguna dependencia externa. Este archivo solo importa HTML y no consume ningún otro archivo del proyecto ni es consumido por otros archivos.


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

El flujo de datos es unidireccional desde el HTML hacia los scripts JavaScript.


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
Este fragmento HTML es una pestaña que muestra el análisis de movimientos en un sistema de monitoreo de almacén (WMS). Incluye un selector para cambiar entre vistas anuales y semanales, KPIs (indicadores clave de rendimiento) como ingresos, consumo de producción, mantenimiento, tasa de reabastecimiento, traspasos, tasas desplanificadas y devoluciones, así como tablas dinámicas que muestran la capacidad operativa y eficiencia.

### Catálogo de Funciones y Clases
- Ninguna función o clase detectada directamente en el fragmento HTML proporcionado.

### Interacción con Base de Datos
- **Motor:** SQLite (implícito, ya que se menciona "SQLite" en el contexto del proyecto).
- **Tablas y Columnas:**
  - No hay consultas SQL crudas o llamadas a ORM explícitas en este fragmento HTML. Las tablas y columnas específicas se obtienen a través de variables pasadas al template (como `ingresos_eff_stats`, `consumos_eff_stats`, etc.).

### Estado y Variables Globales
- **Variables Globales:** Ninguna variable global detectada directamente en el fragmento HTML proporcionado.
- **Estado Crítico:** Las variables que contienen datos dinámicos como `kpi_devoluciones` son pasadas al template desde el backend.

### Dependencias y Flujo
- **Librerías Externas:**
  - Font Awesome (`fas fa-layer-group`, `fas fa-cog`, etc.)
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno.
- **Archivos del Proyecto que Este Archivo Importa:** Ninguno.

**Flujo de Datos:**
El fragmento HTML consume datos desde el backend (probablemente a través de una vista o endpoint FastAPI) y los muestra en la interfaz. Los datos incluyen KPIs, estadísticas de eficiencia y gráficos que se actualizan según la selección del usuario.

**Nota:** El contenido HTML es principalmente estético y interactivo, sin funciones o consultas directas a la base de datos.


---

## Archivo: ./templates/partials/_tab_ots.html (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
Este fragmento HTML corresponde a la pestaña de gestión de Ordenes de Transporte (OTs) en el sistema de monitoreo de almacén. Muestra estadísticas, gráficos y tablas interactivas para visualizar y gestionar OTs pendientes, movimientos no paletizados y productividad.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML.

### Interacción con Base de Datos
- **Motor**: SQLite
- **TABLAS**:
  - `inventory_movements` (Tabla donde se identifican movimientos no paletizados)
- **COLUMNAS**:
  - `doc_mat`
  - `clase_mov`
  - `user`
  - `qty`
  - `source`
  - `dest`
  - `created_at`

### Estado y Variables Globales
No se detectan variables globales, de sesión o de entorno quemadas en el código.

### Dependencias y Flujo
- **Librerías Externas**: No se importan librerías externas específicas.
- **Archivos del Proyecto que Importa a este Archivo**: Ninguno.
- **Archivos del Proyecto que Este Archivo Importa**: Ninguno.
- **Dirección del Flujo de Datos**: El fragmento HTML consume datos desde el backend (FastAPI) y los presenta en la interfaz web. No hay interacción directa con APIs externas.

Este fragmento es una vista HTML que se renderiza en el navegador, consumiendo datos desde el backend para mostrar estadísticas, gráficos y tablas interactivas relacionadas con las OTs y movimientos de almacén.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
Este fragmento HTML es una interfaz de usuario para mostrar detalles de movimientos en un sistema de almacén (WMS). Incluye tablas para visualizar operaciones diarias y mensuales, con opciones para expandir los detalles de las operaciones.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna


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

## Archivo: ./templates/settings.html

### Resumen Funcional
El archivo `settings.html` es una página web que permite la gestión dinámica de parámetros globales del sistema WMS, incluyendo mapeos de estados de entrega, centros de costo a áreas de negocio, calendario de feriados y opciones de exportación de datos. La interfaz permite editar valores, guardar cambios, agregar y eliminar registros, así como sincronizar datos.

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
- `addHoliday()` - Añade una nueva fecha de feriado manual.
- `deleteHoliday(date_str)` - Elimina una fecha de feriado manual.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas SQL ni interactúa directamente con la base de datos.

### Estado y Variables Globales
No hay variables globales explícitas definidas en el código.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas específicas.
- **Archivos del Proyecto Importados**:
  - `partials/_styles.html` - Estilos CSS adicionales.
  - `partials/_logout.html` - Código para cerrar sesión.
- **Archivos que Importan a Este Archivo**: Ninguno.

El flujo de datos se gestiona principalmente a través de eventos de clic en botones y llamadas AJAX a endpoints definidos en el backend (FastAPI).


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
Este archivo `conftest.py` es un archivo de configuración para pruebas unitarias en un proyecto de Sistema de Monitoreo de Almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Define varias funciones de prueba que configuran y limpian la base de datos de pruebas, proporcionan clientes de prueba autenticados y gestionan el estado global para las pruebas.

### Catálogo de Funciones y Clases
- `TEST_SESSION_ID()` - Genera un identificador criptográficamente seguro para evitar colisiones.
- `session_db()` - Crea e inicializa la base de datos maestra compartida para toda la sesión de pruebas, creando las tablas necesarias y aplicando el esquema.
- `test_db(session_db)` - Proporciona aislamiento de datos entre pruebas individuales, vaciando las tablas antes de cada prueba.
- `client(test_db)` - Cliente de pruebas de FastAPI configurado para interactuar con la BD de sesión, parcheando dinámicamente 'sqlite3.connect'.
- `auth_client(client)` - Proporciona un cliente con token de administrador pre-autenticado.

### Interacción con Base de Datos
- Motor: SQLite.
- Tablas:
  - outbound_deliveries
  - inventory_movements
  - stock_levels
  - warehouse_tasks
  - autor_area_mapping
  - analytics_snapshots
  - auth_users
- Columnas: Se especifican explícitamente en las definiciones de las tablas.

### Estado y Variables Globales
- `TEST_SESSION_ID`: Identificador criptográficamente seguro para evitar colisiones.
- `MEMORY_DB_URI`: URI de la base de datos SQLite en memoria compartida.

### Dependencias y Flujo
- Librerías externas: `os`, `secrets`, `pathlib`, `sqlite3`, `unittest.mock`, `pytest`, `fastapi.testclient`.
- Archivos del proyecto que este archivo importa:
  - `config`
  - `app`
  - `core.db_config_manager`
  - `core.auth`
- Archivos del proyecto que importan a este archivo: Ninguno.
- Flujo de datos: El archivo configura y limpia la base de datos de pruebas, proporciona clientes de prueba autenticados y gestiona el estado global para las pruebas.


---

## Archivo: ./tests/test_api.py

### Resumen Funcional
El archivo `test_api.py` contiene pruebas unitarias para endpoints de una API de un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Las pruebas cubren la funcionalidad del dashboard principal, el endpoint de sincronización, la página de analíticas, la generación de consultas SQL, y la protección contra inyección SQL.

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
  - `entrega`
  - `fecha_carga`
  - `centro_costo`
  - `area_negocio`
  - `dias_retraso`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- Librerías externas: `pytest`, `unittest.mock`.
- Archivos del proyecto que este archivo importa:
  - `core.state.AppState`
  - `routes.sync.TUNNEL_URL_FILE`
  - `routes.sync._run_sync_pipeline`
  - `routes.sync.task_manager`
- Archivos del proyecto que importan a este archivo: Ninguno.
- Flujo de datos: El archivo consume pruebas unitarias y dependencias para verificar la funcionalidad de los endpoints de la API.


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
El archivo `test_enrichment.py` contiene pruebas unitarias para funciones que enriquecen y actualizan datos en una base de datos SQLite utilizada por un sistema de monitoreo de almacén (WMS). Las funciones se encargan de aprender mapeos de autor a áreas, rellenar datos de entrega desde movimientos, enriquecer entregas con información de stock y actualizar el SLA basado en tareas de bodega.

### Catálogo de Funciones y Clases
- `db_with_data(test_db: sqlite3.Connection) -> sqlite3.Connection` - Prepara una base de datos SQLite con datos de prueba para los procesos de enriquecimiento.
- `test_learn_and_apply_author_logic(db_with_data: sqlite3.Connection) -> None` - Verifica que el sistema aprenda que USER_A pertenece a PRODUCCION y lo aplique.
- `test_backfill_from_movements(db_with_data: sqlite3.Connection) -> None` - Verifica que Entregas recupere el autor y centro de costo desde Movimientos.
- `test_enrichment_from_stock(db_with_data: sqlite3.Connection) -> None` - Verifica que se crucen las descripciones de material y ubicaciones desde el maestro de stock.
- `test_update_sla_with_tasks(db_with_data: sqlite3.Connection) -> None` - Verifica que el SLA se actualice correctamente usando las tareas de bodega.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - `outbound_deliveries`: `entrega`, `autor`, `area_negocio`, `centro_costo`, `material`
  - `inventory_movements`: `material`, `usuario`, `ce_coste`, `referencia`
  - `stock_levels`: `material`, `denominacion`, `ubicacion_bin`, `stock_disp`, `umb`
  - `autor_area_mapping`: `autor`, `area_negocio`
  - `warehouse_tasks`: `entrega`, `fecha_conf`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `pytest`, `sqlite3`
- **Archivos del Proyecto que Importan a este Archivo:**
  - `conftest.py` (para el fixture `test_db`)
- **Archivos del Proyecto que Este Archivo Importa:**
  - `db.db_enrichment` (contiene las funciones `learn_author_areas`, `apply_author_learning`, `backfill_deliveries_from_movements`, `enrich_deliveries_with_stock`, `update_sla_with_tasks`)
- **Dirección del Flujo de Datos:** El archivo importa funciones desde `db.db_enrichment` y utiliza un fixture para preparar una base de datos SQLite con datos de prueba. Luego, ejecuta pruebas unitarias que invocan estas funciones y verifican su comportamiento utilizando consultas SQL directas a la base de datos.


---

## Archivo: ./tests/test_maintenance.py

### Resumen Funcional
El archivo `test_maintenance.py` contiene pruebas unitarias para funciones relacionadas con el mantenimiento del sistema, específicamente para cerrar aplicaciones y filtrar archivos en el generador de documentación.

### Catálogo de Funciones y Clases
- `test_quit_app_success()` - Verifica que la función `quit_app` retorne True cuando el comando de sistema tiene éxito.
- `test_quit_app_failure()` - Verifica que la función `quit_app` retorne False cuando ocurre un error de proceso o excepción.
- `test_doc_generator_filtering_logic(filename: str, filepath: str, expected: bool)` - Prueba la lógica de exclusión de archivos en el generador de documentación.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `pytest`, `subprocess`, `unittest.mock`
- **Archivos del Proyecto que IMPORTA (consume)**: `scripts.free_ram.quit_app`, `scripts.doc_generator.should_process`
- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno
- **Dirección del Flujo de Datos**: El flujo de datos se centra en la simulación y verificación de funciones relacionadas con el mantenimiento del sistema.


---

## Archivo: ./tests/test_pdf.py

### Resumen Funcional
Este archivo `test_pdf.py` contiene pruebas unitarias para validar la funcionalidad del módulo `pdf_engine`, que se encarga de generar documentos PDF en formato Landscape utilizando la orientación de papel Letter. Las pruebas cubren la creación de instancias de PDF, generación de códigos de barras, recuperación lógica de órdenes de transporte (OTs) y el dibujo de páginas de entrega.

### Catálogo de Funciones y Clases
- `pdf_instance() -> WMS_Landscape_PDF` - Proporciona una instancia limpia de `WMS_Landscape_PDF` para cada test.
- `sample_header() -> pd.Series` - Genera datos de cabecera de entrega ficticios para pruebas de renderizado de metadatos.
- `sample_items() -> pd.DataFrame` - Genera un listado de materiales ficticios para validar el cuerpo dinámico del PDF.
- `test_pdf_instantiation(pdf_instance: WMS_Landscape_PDF) -> None` - Verifica que la clase PDF se instancie con la orientación Landscape y dimensiones Letter.
- `test_barcode_generation(barcode_data: str) -> None` - Valida que la utilidad de códigos de barras produzca un stream binario válido.
- `test_get_ots_logic() -> None` - Verifica la lógica de recuperación de OTs filtrando valores inválidos (0 o nulos).
- `test_draw_delivery_page_generates_content(pdf_instance: WMS_Landscape_PDF, sample_header: pd.Series, sample_items: pd.DataFrame) -> None` - Valida que el motor de dibujo escriba contenido binario en el buffer del PDF.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas y Columnas:
  - `get_ots_for_delivery("8000123", mock_conn)`:
    - Tabla: No especificada (mocked)
    - Columna: `numero_ot`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- Librerías externas:
  - `pytest`
  - `pandas`
  - `io`
  - `sqlite3`
  - `typing`
  - `unittest.mock`
- Archivos del proyecto que este archivo importa (consume):
  - `core.pdf_engine` (`WMS_Landscape_PDF`, `_generate_barcode_stream`, `draw_delivery_page`, `get_ots_for_delivery`)
- Archivos del proyecto que importan a este archivo (lo consumen):
  - Ninguno
- Flujo de datos:
  - El archivo se ejecuta como parte de las pruebas unitarias, no tiene flujo de entrada/salida directo con otros archivos.


---

## Archivo: ./tests/test_pipeline.py

### Resumen Funcional
El archivo `test_pipeline.py` contiene pruebas unitarias para el módulo de consolidación de datos en un sistema de monitoreo de almacén (WMS). Las pruebas cubren la funcionalidad de análisis de fechas, validación de nombres de tablas y lógica de sobrescritura de archivos.

### Catálogo de Funciones y Clases
- `test_parse_file_date(consolidator)` - Verifica que el parsing de fechas sea correcto.
- `test_validate_table_security(consolidator)` - Verifica la protección contra nombres de tabla no permitidos.
- `test_overwrite_with_latest_logic(consolidator, tmp_path)` - Verifica que se tome el archivo más reciente para sobrescribir.

### Interacción con Base de Datos
- Motor: SQLite (in-memory)
- Tablas:
  - `TABLE_DELIVERIES`
  - `TABLE_STOCK`
- Columnas: No especificadas explícitamente en el código proporcionado.
- Consultas SQL crudas o llamadas a ORM: No se observan consultas específicas.

### Estado y Variables Globales
No se detectan variables globales, de sesión, de entorno o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- Librerías externas:
  - `pytest`
  - `pathlib`
  - `datetime`
  - `pandas`
- Archivos del proyecto que este archivo importa (consume):
  - `db.consolidator.DataConsolidator`
  - `services.etl.OutboundDeliveryAdapter.read_and_clean_data`
- Archivos del proyecto que importan a este archivo (lo consumen): Ninguna.
- Dirección del flujo de datos: El archivo consume funciones y clases de otros módulos para realizar pruebas unitarias.


---

## Archivo: ./tests/test_queries.py

### Resumen Funcional
El archivo `test_queries.py` contiene pruebas unitarias para verificar la funcionalidad de consultas y métodos relacionados con el repositorio de entregas (`DeliveriesRepository`) en un sistema de monitoreo de almacén (WMS). Las pruebas incluyen la obtención del número de días activos, estadísticas por área de negocio y la compilación correcta de consultas SQL a partir de payloads.

### Catálogo de Funciones y Clases
- `test_get_total_active_days(test_db: sqlite3.Connection) -> None` - Verifica el conteo de días únicos con actividad filtrado por año usando fechas ISO.
- `test_get_total_active_days_empty(test_db: sqlite3.Connection) -> None` - Verifica que la función retorne 0 si no hay registros.
- `test_get_area_stats(test_db: sqlite3.Connection) -> None` - Verifica el cálculo de KPIs (ontime/late) agrupados por área de negocio.
- `test_area_expr_fallback_locations(test_db: sqlite3.Connection) -> None` - Verifica la asignación correcta de áreas basada en ubicaciones binarias.
- `test_query_engine_compiles_ast_correctly(test_db: sqlite3.Connection) -> None` - Verifica que el motor de consultas compile correctamente los ASTs a SQL.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `outbound_deliveries`
- **Columnas:**
  - `entrega`
  - `fecha_carga`
  - `area_negocio`
  - `dias_retraso`
  - `centro_costo`
  - `ubicacion_bin_1`
  - `ubicacion_bin`

### Estado y Variables Globales
- **Constantes:** 
  - `TEST_YEAR` (`"%2026"`)
  - `AREA_A` (`"ASERRADERO"`)
  - `AREA_B` (`"MOLDURAS"`)
  - `DATE_1` (`"01-05-2026"`)
  - `DATE_2` (`"02-05-2026"`)

### Dependencias y Flujo
- **Librerías Externas:** 
  - `pytest`
  - `sqlite3`
  - `pandas`
- **Archivos del Proyecto que Importan a este Archivo:**
  - `repositories.deliveries.DeliveriesRepository`
  - `core.query_engine.build_sql_from_payload`
  - `core.schemas.VisualQueryBuilderPayload`, `MetricDef`, `TimeAxisDef`, `FilterDef`
- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno
- **Dirección del Flujo de Datos:** 
  - Pruebas unitarias invocan métodos del repositorio y verifican sus resultados.


---

## Archivo: ./tests/test_services.py

### Resumen Funcional
El archivo `test_services.py` contiene pruebas unitarias para funciones y servicios relacionados con la gestión del estado de la aplicación y el manejo de túneles en un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite.

### Catálogo de Funciones y Clases
- `app_state()` - Proporciona una instancia limpia de AppState configurada para pruebas.
- `cleanup_tunnel()` - Garantiza la limpieza del estado global del túnel tras cada test.
- `test_state_cache_respects_limits(app_state: AppState)` - Verifica que el gestor de estado respete los límites de memoria.
- `test_state_sync_flag_reactivity(app_state: AppState)` - Valida que la propiedad reactiva de sincronización cambie su estado de forma consistente.
- `test_start_tunnel_manages_singleton_instance(mock_access, mock_exists, mock_popen)` - Verifica que `start_tunnel` inicialice correctamente el servicio de túnel.
- `test_stop_tunnel_releases_global_reference(mock_run)` - Valida que `stop_tunnel` limpie las referencias globales de forma segura.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `TEST_MAX_CACHE_SIZE` - Constante que establece el límite de caché para pruebas.
- `app_state.max_cache_size` - Variable global que almacena el límite de caché en la instancia de AppState.

### Dependencias y Flujo
- **Librerías Externas**: `pytest`, `unittest.mock`.
- **Archivos del Proyecto Importados**:
  - `services.tunnel`: Para las funciones `start_tunnel` y `stop_tunnel`.
  - `core.state`: Para la clase `AppState`.
- **Archivos del Proyecto que Importan a Este Archivo**: Ninguno.

El flujo de datos se centra en la ejecución de pruebas unitarias para asegurar el correcto funcionamiento de los servicios y funciones relacionados con el estado de la aplicación y el manejo de túneles.


---

## Archivo: ./tests/test_ui_smoke.py

### Resumen Funcional
El archivo `test_ui_smoke.py` contiene pruebas unitarias para verificar la presencia de componentes UI críticos en diferentes rutas del sistema de monitoreo de almacén (WMS). Las pruebas incluyen verificación de la disponibilidad del servidor, la presencia de elementos HTML específicos y el manejo adecuado de errores.

### Catálogo de Funciones y Clases
- `test_ui_smoke_components_presence(auth_client, path: str, markers: List[Tuple[str, str]])` - Prueba que verifica la presencia de componentes UI críticos en diferentes rutas.
- `test_ui_smoke_error_handling(client)` - Prueba que verifica el manejo correcto del servidor para rutas inexistentes.
- `test_ui_smoke_analytics_studio_modal_components(auth_client)` - Prueba que verifica la presencia de selectores visuales y asegura que no exista el textarea de SQL crudo.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: `pytest`, `typing`
- **Archivos del Proyecto Importados**:
  - Ninguno.
- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno.


---

## Archivo: ./tests/test_utils.py

### Resumen Funcional
El archivo `test_utils.py` contiene pruebas unitarias para el módulo `utils` del proyecto WMS, específicamente para verificar que la función `setup_signal_handlers` funcione correctamente y de manera idempotente.

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

