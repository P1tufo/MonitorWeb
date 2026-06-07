# Documentación Técnica - Directorio: routes
Compilado el: 2026-06-07 12:50:47
Modelo: qwen2.5-coder:7b | Separado por Carpetas

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
  - `core.state.CacheManager`, `core.state.SyncStateManager`, `get_cache_manager`, `get_sync_manager`
  - `services.dashboard_service.DashboardService`

**Flujo de Datos:**
1. **Entrada:** Requiere un usuario autenticado y una sesión de base de datos.
2. **Procesamiento:**
   - Para `get_ubicaciones`: Consulta la tabla `stock_levels` para obtener las ubicaciones del material especificado.
   - Para `dashboard` y `dashboard_api`: Utiliza el servicio `DashboardService` para obtener el contexto completo del negocio, que luego se almacena en caché.
3. **Salida:** Devuelve los datos en formato JSON o HTML según la solicitud.

**Nota:** El archivo no utiliza consultas SQL crudas directamente; en su lugar, usa SQLAlchemy ORM y pandas para manipular los datos.


---

## Archivo: ./routes/deliveries.py

### Resumen Funcional
Este archivo contiene rutas y funciones para el módulo de análisis de entregas en un sistema de gestión de almacén (WMS). Ofrece endpoints para renderizar páginas web con datos de análisis, así como una API JSON que devuelve los mismos datos.

### Catálogo de Funciones y Clases
- `save_analytics_snapshot(session: Session, key: str, data: Dict[str, Any])` - Guarda una captura de las analíticas en la base de datos para carga instantánea.
- `load_analytics_snapshot(session: Session, key: str) -> Optional[Dict[str, Any]]` - Recupera la última captura de analíticas desde la base de datos.
- `analytics(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager))` - Renderiza la página principal de analíticas con caché multinivel (Memoria -> DB -> Cálculo).
- `sla_details(request: Request, type: str = "late", date: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Vista detallada de auditoría SLA.
- `get_non_palletized_details(user: str, clase_mov: str, db: Session = Depends(get_session_dep), current_user: Dict[str, Any] = Depends(get_current_user))` - Obtiene el listado detallado (hasta 200) de movimientos no paletizados para un usuario y tipo de movimiento específicos.
- `analytics_deliveries_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager), sync: SyncStateManager = Depends(get_sync_manager))` - API JSON para analíticas de Entregas (Outbound Deliveries).

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - `analytics_snapshots`: 
    - `key` (TEXT, PRIMARY KEY)
    - `data` (TEXT)
    - `updated_at` (TIMESTAMP)
  - `inventory_movements`: 
    - `doc_mat`
    - `usuario`
    - `cmv`
    - `alm`
    - `ce`
    - `fe_contab`
    - `hora`

### Estado y Variables Globales
- **Variables Globales:** Ninguna.
- **Estado de Sesión:** Ninguna.
- **Estado de Entorno:** Ninguna.
- **Diccionarios Quemados en Código:** Ninguno.

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `fastapi`
  - `sqlalchemy`
  - `logging`
  - `json`
  - `datetime`
  - `typing`

- **Archivos del Proyecto que Este Archivo IMPORTA (consume):**
  - `core.app_instance`
  - `core.auth`
  - `core.database`
  - `core.schemas`
  - `core.state`
  - `core.utils`
  - `repositories.DeliveriesRepository`
  - `routes.analytics_proyecciones`
  - `routes.inventory`
  - `routes.tasks`
  - `services.deliveries_service`

- **Archivos del Proyecto que IMPORTAN a Este Archivo (lo consumen):**
  - Ninguno.

**Flujo de Datos:**
1. **Entrada:** Solicitudes HTTP a las rutas definidas.
2. **Procesamiento:** Llamadas a funciones y servicios para obtener datos, aplicar caché y guardar capturas en la base de datos.
3. **Salida:** Renderizado de plantillas HTML o respuesta JSON con los datos procesados.

Este archivo es crucial para el rendimiento y la eficiencia del sistema de análisis de entregas, ya que implementa un mecanismo de caché multinivel y persistente en la base de datos.


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
- **Dependencias Externas**: No hay dependencias externas directamente importadas.
- **Archivos Importados**:
  - `config.py`: Para obtener los directorios base (`BASE_DIR`, `CACHE_DIR`).
- **Archivos que Importan a este Archivo**: Ninguno.

El flujo de datos es el siguiente:
1. El usuario accede al endpoint `/api/docs/tree` para obtener la estructura del proyecto con indicadores de documentación.
2. El usuario accede al endpoint `/api/docs/content/{path:path}` para leer el contenido específico de una documentación (.md).


---

## Archivo: ./routes/filters.py

### Resumen Funcional
El archivo `filters.py` contiene endpoints para filtrar entregas y calcular KPIs dinámicos en un sistema de monitoreo de almacén (WMS). Utiliza FastAPI, SQLAlchemy y SQLite para interactuar con la base de datos.

### Catálogo de Funciones y Clases
- `_build_unified_where(date: str = None, area: str = None, centro: str = None, has_ots: str = None, min_week: str = None) -> tuple[str, dict]` - Construye una cláusula WHERE unificada basada en los criterios de filtro proporcionados.
- `filter_transactions(request: Request, date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Filtra entregas basándose en múltiples criterios.
- `get_kpis(date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Calcula KPIs dinámicos filtrados por área para el dashboard.
- `api_widget_data(query_id: str, request: Request, session: Session = Depends(get_session_dep))` - Endpoint de carga asíncrona para los componentes del Dashboard.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - `warehouse_tasks`
  - `deliveries`
  - `dashboard`
  - `config_query`
- Columnas:
  - `v.fecha_carga`, `v.fecha_sm_real`, `v.creado_el` (de la tabla `deliveries`)
  - `l.entrega` (de la tabla `warehouse_tasks`)
  - `v.week_sort` (de la tabla `dashboard`)
  - `v.visual_state`, `v.sql_text` (de la tabla `config_query`)
- Consultas SQL crudas: Sí, se utilizan consultas SQL generadas dinámicamente.

### Estado y Variables Globales
- `DATE_EXPR`: Expresión para obtener la fecha de carga.
- `ALLOWED_OTS_STATES`: Conjunto de estados OT permitidos como filtro.

### Dependencias y Flujo
- Librerías externas: `pandas`, `fastapi`, `sqlalchemy`
- Archivos del proyecto que importan a este archivo:
  - `core.database`
  - `core.models`
  - `core.query_engine`
  - `core.schemas`
  - `core.utils`
  - `repositories.deliveries`
  - `repositories.dashboard`
- Archivos del proyecto que este archivo importa:
  - `config`
  - `core.macros`

**Flujo de datos:**
1. **Entrada**: Parámetros de filtro desde el cliente.
2. **Procesamiento**:
   - Construcción dinámica de consultas SQL basadas en los criterios de filtro.
   - Ejecución de consultas SQL contra la base de datos SQLite.
3. **Salida**: Datos filtrados o KPIs calculados en formato JSON.

Este archivo es crucial para el funcionamiento del sistema de monitoreo de almacén, proporcionando endpoints para obtener datos filtrados y calcular indicadores clave de rendimiento (KPIs) dinámicamente.


---

## Archivo: ./routes/inventory.py

### Resumen Funcional
Este archivo contiene rutas y lógica para el análisis de inventario en un sistema de gestión de almacén (WMS). Ofrece una redirección a la página de analíticas de inventario y una API que devuelve datos de inventario optimizados.

### Catálogo de Funciones y Clases
- `analytics_inventory_redirect(request: Request)` - Redirige a la página de analíticas de inventario.
- `get_inventory_context(session: Session) -> Dict[str, Any]` - Obtiene el contexto completo del inventario.
- `analytics_inventory_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager), sync: SyncStateManager = Depends(get_sync_manager))` - API que devuelve datos de inventario optimizados.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas a la base de datos directamente.

### Estado y Variables Globales
- `logger` - Manejador de registros.
- `router` - Ruta FastAPI para el módulo de analíticas de inventario.

### Dependencias y Flujo
- **Dependencias Importadas**: 
  - `get_current_user`, `get_session_dep`, `get_cache_manager`, `get_sync_manager` (desde `core.auth`, `core.database`, `core.state`).
  - `InventoryService` (desde `services.inventory_service`).
  - `AnalyticsInventoryResponse` (desde `core.schemas`).

- **Dependencias Exportadas**: 
  - No se exportan dependencias.

- **Flujo de Datos**:
  - El archivo recibe una solicitud HTTP y utiliza dependencias para obtener el contexto del inventario.
  - Luego, intenta recuperar los datos desde la caché. Si no están en caché, obtiene los datos del servicio de inventario, limpia el contexto y lo almacena en caché antes de devolverlo.

Este archivo es parte del módulo de analíticas de inventario y se encarga de manejar las solicitudes para obtener datos optimizados del inventario.


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
- **Variables de Sesión:** Ninguna.
- **Diccionarios Quemados:** Ninguno.

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `fastapi`
  - `sqlalchemy`
  - `logging`
  - `io`
  - `datetime`
  - `typing`
- **Archivos del Proyecto que Importa a este Archivo:** Ninguno.
- **Archivos del Proyecto que Este Archivo Importa:**
  - `config.DB_PATH`
  - `config.PDF_STORAGE`
  - `core.database.get_session_dep`
  - `core.pdf_engine.WMS_Landscape_PDF`
  - `core.pdf_engine.draw_delivery_page`
  - `core.pdf_engine.get_ots_for_delivery`
  - `core.pdf_reports.draw_annex_table`
  - `core.pdf_reports.draw_picking_list`
  - `repositories.deliveries.DeliveriesRepository`

**Flujo de Datos:**
1. **Entrada:** Parámetros del formulario.
2. **Procesamiento:**
   - Consulta a la base de datos para obtener los datos necesarios.
   - Generación del PDF utilizando las funciones definidas en `core.pdf_engine` y `core.pdf_reports`.
3. **Salida:** Respuesta HTTP con el contenido del PDF.

Este flujo asegura que los datos se procesen correctamente y se generen los PDFs según los parámetros proporcionados.


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
El archivo `settings.py` contiene endpoints para la gestión dinámica de configuraciones SaaS en un sistema de monitoreo de almacén (WMS). Utiliza SQLAlchemy ORM para todas las operaciones de escritura y FastAPI para crear una API RESTful.

### Catálogo de Funciones y Clases
- `invalidate_caches(db: Session)` - Limpia el caché global en memoria y elimina todos los snapshots de base de datos.
- `settings_view(request: Request, db: DBSession)` - Renderiza el panel de control de configuraciones SaaS.
- `api_get_settings()` - Retorna las configuraciones generales.
- `api_update_setting(update: SettingUpdate, db: DBSession)` - Actualiza una configuración específica.
- `api_upsert_status(update: StatusMappingUpdate, db: DBSession)` - Inserta o actualiza un mapeo de estado.
- `api_delete_status(code: str, db: DBSession)` - Elimina un mapeo de estado.
- `api_upsert_cost_center(update: CostCenterMappingUpdate, db: DBSession)` - Inserta o actualiza un centro de costo.
- `api_delete_cost_center(code: str, db: DBSession)` - Elimina un centro de costo.
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
- Motor: SQLite
- Tablas:
  - `analytics_snapshots`
- Columnas:
  - `id` (de `analytics_snapshots`)
- Consultas SQL crudas o llamadas a ORM:
  - `DELETE FROM analytics_snapshots`

### Estado y Variables Globales
- No hay variables globales, de sesión, de entorno o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- Librerías externas: `fastapi`, `sqlalchemy`, `pydantic`, `pandas`, `holidays`, `openpyxl`
- Archivos del proyecto que este archivo importa:
  - `core.app_instance`
  - `core.auth`
  - `core.database`
  - `core.db_config_manager`
  - `core.models`
  - `core.state`
  - `core.utils`
  - `core.schemas`
  - `core.semantic_layer`
  - `core.query_engine`
- Archivos del proyecto que importan a este archivo:
  - Ninguno
- Flujo de datos: El archivo es un endpoint de FastAPI que consume y produce datos para la gestión de configuraciones SaaS.


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
El archivo `tasks.py` proporciona una interfaz RESTful para obtener analíticas de tareas en un sistema de almacén (WMS) utilizando FastAPI. La API permite recuperar datos de tareas, almacenándolos en caché para mejorar el rendimiento y gestionando el estado de sincronización.

### Catálogo de Funciones y Clases
- `get_tasks_context(session: Session) -> dict` - Obtiene el contexto completo de las tareas utilizando un servicio.
- `analytics_tasks_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager), sync: SyncStateManager = Depends(get_sync_manager))` - Endpoint FastAPI para obtener analíticas de tareas, recuperando datos del caché si es posible.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos. Utiliza un servicio (`TasksService`) que probablemente interactúa con el repositorio de tareas para obtener los datos necesarios.

### Estado y Variables Globales
- `logger` - Objeto de registro utilizado para registrar errores.
- `router` - Instancia de `APIRouter` de FastAPI para definir las rutas del API.

### Dependencias y Flujo
- **Dependencias Importadas**: 
  - `get_current_user`, `get_session_dep`, `get_cache_manager`, `get_sync_manager` - Funciones que proporcionan dependencias como la sesión de base de datos, el manejador de caché y el estado de sincronización.
  
- **Archivos Importados**:
  - `core.auth`: Para autenticación del usuario.
  - `core.database`: Para obtener la sesión de base de datos.
  - `core.schemas`: Para definir los modelos de respuesta.
  - `core.state`: Para gestionar el estado de caché y sincronización.
  - `core.utils`: Para utilidades como la limpieza de datos para JSON.
  - `repositories`: Para interactuar con las tablas de la base de datos.
  - `services.tasks_service`: Para obtener el contexto completo de las tareas.

- **Flujo de Datos**:
  1. El endpoint `analytics_tasks_api` se invoca a través de una solicitud HTTP GET a `/api/v1/analytics/tasks`.
  2. Se intenta recuperar los datos del caché.
  3. Si el dato no está en caché, se obtiene utilizando el servicio `TasksService`.
  4. El contexto obtenido se limpia para eliminar información sensible y se almacena en caché.
  5. Finalmente, se devuelve la respuesta con los datos limpios y el estado de sincronización.

Este archivo es crucial para proporcionar una interfaz eficiente y segura para obtener analíticas de tareas en un sistema de almacén, utilizando técnicas de caché y gestión de estado para mejorar el rendimiento.


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

