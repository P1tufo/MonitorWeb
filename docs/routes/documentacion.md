# Documentación Técnica - Directorio: routes
Compilado el: 2026-06-04 23:43:39
Modelo: qwen2.5-coder:7b | Separado por Carpetas

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
  - `docs.py` importado por otros archivos del proyecto.
  - Otros archivos del proyecto pueden importar `docs.py` para utilizar sus endpoints.

El flujo de datos es unidireccional, con `docs.py` proporcionando los endpoints y no consumiendo servicios o repositorios externos.


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

