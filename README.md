# Documentación Técnica Global - MonitorWeb
Compilado el: 2026-06-05 14:46:00
Modelo: qwen2.5-coder:7b | Hardware: M1 Pro Optimized

---

## Análisis de Arquitectura Global

### Arquitectura General Detectada

La estructura del proyecto sugiere una arquitectura **Modular**. Esto se debe a la organización de los módulos y carpetas que separan diferentes aspectos del sistema, como el código principal (`app.py`), las configuraciones (`config.py`), las rutas (`routes/`), los modelos (`core/models.py`), las bases de datos (`db/`), los servicios (`services/`), y las pruebas (`tests/`). Además, la presencia de carpetas como `core`, `repositories`, `scripts`, `templates`, `docs`, y `deploy` indica una organización modular.

### Propósito Probable de las Carpetas Principales

- **app.py**: Punto de entrada principal del aplicativo.
- **config.py**: Archivo de configuración global para el proyecto.
- **core/**: Contiene componentes fundamentales del sistema, como modelos, seguridad, base de datos, y utilidades generales.
- **bin/**: Almacena herramientas binarias necesarias para el desarrollo o despliegue.
- **deploy/**: Archivos relacionados con la configuración y despliegue del proyecto, incluyendo Dockerfiles y archivos de configuración de Docker.
- **setup/**: Contiene scripts y archivos necesarios para la instalación y gestión del proyecto, como `requirements.txt` y `package.json`.
- **tests/**: Directorio que almacena todos los tests unitarios y de integración del proyecto.
- **repositories/**: Define las interfaces de acceso a datos (DAOs) para diferentes entidades del sistema.
- **docs/**: Documentación del proyecto, incluyendo documentación técnica y mejoras propuestas.
- **DELIVERIES_cleansed/**: Archivos limpios generados por el proceso de limpieza de datos.
- **static/**: Recursos estáticos como CSS y JavaScript para la interfaz web.
- **scripts/**: Scripts Python que realizan tareas específicas, como generación de documentación o procesamiento de datos.
- **db/**: Archivos relacionados con la base de datos, incluyendo archivos de configuración y scripts de consolidación.
- **templates/**: Plantillas HTML para las vistas del sistema web.
- **routes/**: Definición de rutas y controladores para el manejo de solicitudes HTTP.
- **services/**: Servicios que encapsulan la lógica de negocio, como servicios de inventario, entregas, etc.

### Organización Lógica de las Dependencias

La organización del proyecto muestra una clara separación de responsabilidades y dependencias:

1. **Core**: Contiene componentes fundamentales que son utilizados por todo el sistema.
2. **Repositories**: Define interfaces para acceder a los datos, lo que facilita la inyección de dependencias y la prueba unitaria.
3. **Services**: Encapsula la lógica de negocio, lo que permite una separación clara entre la capa de presentación y la capa de negocio.
4. **Routes**: Define las rutas HTTP y los controladores correspondientes, utilizando los servicios definidos en `services/`.
5. **Tests**: Contiene pruebas unitarias y de integración para asegurar que cada componente funcione correctamente.

Esta organización modular facilita el mantenimiento, la escalabilidad y la colaboración entre equipos de desarrollo.


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

