# Documentación Técnica - Directorio: routes
Compilado el: 2026-05-28 23:22:17
Modelo: qwen2.5-coder:7b | Separado por Carpetas

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
El archivo `config.py` es un módulo que se encarga de registrar todos los routers de una aplicación FastAPI. Estos routers corresponden a diferentes funcionalidades del sistema, como autenticación, dashboards, entregas, inventario, análisis proyecciones, filtros, PDFs, sincronización, documentos, configuraciones, tareas, widgets, consumos y transporte.

### Catálogo de Funciones y Clases
- `register_routes(app: FastAPI) -> None` - Registra todos los routers de la aplicación de forma centralizada. Maneja errores para evitar que un router mal configurado detenga el arranque completo del servidor.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `ROUTERS: List[APIRouter]` - Una lista declarativa de routers con tipado estático. Almacena todos los routers que se van a registrar en la aplicación FastAPI.

### Dependencias y Flujo
- **Dependencias**: 
  - `fastapi`: Se utiliza para crear y gestionar la aplicación FastAPI.
  - `logging`: Para el registro de errores y mensajes de depuración.
  
- **Flujo**:
  - El archivo importa varios módulos que contienen routers específicos (`dashboard`, `deliveries`, etc.).
  - La función `register_routes` itera sobre la lista de routers, intentando registrar cada uno en la aplicación FastAPI.
  - Si ocurre un error al registrar un router, se registra el error y continúa con el siguiente router.

Este archivo es crucial para mantener una estructura organizada y modular de los endpoints de la API, facilitando su mantenimiento y escalabilidad.


---

## Archivo: ./routes/consumos.py

### Resumen Funcional
El archivo `consumos.py` define dos endpoints para obtener información de los consumos (CMV 201) en función del CeCo y una lista de materiales. Utiliza FastAPI para crear las rutas, SQLAlchemy para interactuar con la base de datos y pandas para procesar los resultados.

### Catálogo de Funciones y Clases
- `get_consumos_ceco(ceco: str, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Obtiene los consumos agrupados por material para un CeCo específico.
- `get_consumos_materiales(req: MaterialesRequest, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Obtiene qué CeCos han consumido una lista de materiales.

### Interacción con Base de Datos
- Motor: SQLite (inferred from the use of `session.connection()`).
- Tablas:
  - `inventory_movements`
  - `outbound_deliveries`
- Columnas:
  - `inventory_movements`: `material`, `texto_breve_material`, `cantidad`, `importe_ml`, `cmv`, `ce_coste`, `fe_contab`.
  - `outbound_deliveries`: `centro_costo`, `area_negocio`.

### Estado y Variables Globales
- No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `fastapi`
  - `sqlalchemy`
  - `pandas`
  - `pydantic`
  - `logging`
  - `datetime`

- Flujo de comunicación:
  - El archivo se comunica con el resto del proyecto a través de dependencias como `get_current_user` y `get_session_dep`.


---

## Archivo: ./routes/dashboard.py

### Resumen Funcional
El archivo `dashboard.py` define rutas para un dashboard que incluye endpoints para obtener ubicaciones de materiales y la vista principal del dashboard con KPIs. Utiliza FastAPI para definir las rutas, SQLAlchemy para interactuar con una base de datos SQLite, y pandas para procesar los resultados.

### Catálogo de Funciones y Clases
- `get_ubicaciones(material: str, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Obtiene las ubicaciones de un material específico.
- `dashboard(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Vista principal del dashboard con KPIs y búsqueda rápida.
- `dashboard_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - API JSON para el dashboard con KPIs y búsqueda rápida.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `stock_levels`
- Columnas:
  - `ubicacion_bin`, `Ubicación`, `ubicacin`, `denominacion`, `Texto breve de material`, `material`, `UMB`, `Stock disp`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: `logging`, `sqlite3`, `itertools`, `pandas`, `datetime`, `timedelta`, `typing`, `fastapi`, `sqlalchemy`, `core.database`, `core.state`, `core.auth`, `core.app_instance`, `services.dashboard_service`, `core.wms_config`, `core.schemas`
- Flujo: El archivo interactúa con el servicio `DashboardService` para obtener datos de negocio y los presenta a través de endpoints FastAPI. Utiliza una sesión de base de datos SQLAlchemy para ejecutar consultas SQL y pandas para procesar los resultados.


---

## Archivo: ./routes/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene rutas y funciones para manejar las analíticas de entregas en una aplicación web. Incluye endpoints para renderizar páginas HTML con datos de análisis, guardar y cargar capturas de estado en la base de datos, y proporcionar datos de análisis a través de una API JSON.

### Catálogo de Funciones y Clases
- `save_analytics_snapshot(session: Session, key: str, data: Dict[str, Any])` - Guarda una captura de las analíticas en la base de datos.
- `load_analytics_snapshot(session: Session, key: str) -> Optional[Dict[str, Any]]` - Recupera la última captura de analíticas desde la base de datos.
- `analytics(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Renderiza la página principal de analíticas con caché multinivel.
- `sla_details(request: Request, type: str = "late", date: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Vista detallada de auditoría SLA.
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

- Flujo de comunicación:
  - El archivo interactúa con otros archivos del proyecto a través de importaciones, como `core.database`, `repositories`, `routes.inventory`, etc.
  - Utiliza dependencias inyectadas para obtener sesiones de base de datos y estados de aplicación.


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
El archivo `filters.py` contiene funciones y rutas para filtrar entregas y calcular KPIs dinámicos en un sistema de gestión de materiales. Ofrece endpoints para obtener datos filtrados por múltiples criterios y calcular indicadores clave de rendimiento (KPIs) basados en estos filtros.

### Catálogo de Funciones y Clases
- `_build_unified_where(date: str, area: str, centro: str, has_ots_filter: str, min_week: Optional[str])` - Construye la cláusula WHERE a nivel de MATERIAL con seguridad contra SQL Injection.
- `filter_transactions(request: Request, date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Filtra entregas basándose en múltiples criterios.
- `get_kpis(date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Calcula KPIs dinámicos filtrados por área para el dashboard.
- `api_widget_data(query_id: str, request: Request, session: Session = Depends(get_session_dep))` - Endpoint de carga asíncrona para los componentes del Dashboard.

### Interacción con Base de Datos
- Motor de BD: SQLAlchemy
- Tablas:
  - `outbound_deliveries`
  - `config_cost_center_mapping`
  - `warehouse_tasks`
- Columnas:
  - `v.entrega`
  - `v.week_sort`
  - `v.area_negocio`
  - `v.ubicacion_area`
  - `v.ubicacion_bin_1`
  - `v.ubicacion_bin`
  - `v.estado_wms`
  - `v.dias_retraso`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas`
  - `fastapi`
  - `sqlalchemy`
  - `logging`
- Comunicación con otros archivos del proyecto:
  - `core.database.get_session_dep`
  - `core.models.ConfigQuery`
  - `core.query_engine.build_sql_from_payload`
  - `core.schemas.VisualQueryBuilderPayload`
  - `repositories.deliveries.DeliveriesRepository`


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
Este archivo contiene rutas para generar reportes PDF en un sistema WMS (Warehouse Management System). Ofrece dos endpoints: uno para generar un PDF individual y otro para generar un reporte masivo con múltiples entregas.

### Catálogo de Funciones y Clases
- `generate_pdf(entrega, include_logo, action, session)` - Genera un PDF para una única entrega.
- `generate_pdf_bulk(date, entrega_query, area, centro, has_ots_filter, include_logo, action, session)` - Genera un reporte masivo con índice y picking list.

### Interacción con Base de Datos
- Motor: SQLite (inferred from the use of SQLAlchemy)
- Tablas:
  - `outbound_deliveries`
  - Consultas SQL crudas para leer datos de estas tablas.
- Columnas:
  - Todas las columnas de la tabla `outbound_deliveries` se leen en los métodos.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: `pandas`, `fastapi`, `sqlalchemy`, `logging`.
- Comunicación con otros archivos del proyecto:
  - `core.database.get_session_dep` para obtener la sesión de base de datos.
  - `core.pdf_engine.WMS_Landscape_PDF` y sus métodos (`draw_delivery_page`, `get_ots_for_delivery`) para generar el PDF.
  - `core.pdf_queries` para consultas SQL relacionadas con las entregas.
  - `core.pdf_reports` para dibujar tablas y listas en el PDF.


---

## Archivo: ./routes/settings.py

### Resumen Funcional
El archivo `settings.py` define una API para la gestión dinámica de configuraciones SaaS utilizando SQLAlchemy ORM. Permite crear, actualizar y eliminar configuraciones como mapeos de estado, centros de costo y feriados, así como consultar y modificar consultas SQL.

### Catálogo de Funciones y Clases
- `invalidate_caches(db: Session)` - Limpia el caché global en memoria y elimina todos los snapshots de base de datos.
- `settings_view(request: Request, db: DBSession, state: AppState = Depends(get_app_state))` - Renderiza el panel de control de configuraciones SaaS.
- `api_get_settings(state: AppState = Depends(get_app_state))` - Retorna las configuraciones generales.
- `api_update_setting(update: SettingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Actualiza una configuración específica.
- `api_upsert_status(update: StatusMappingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Inserta o actualiza un mapeo de estado.
- `api_delete_status(code: str, db: DBSession, state: AppState = Depends(get_app_state))` - Elimina un mapeo de estado.
- `api_upsert_cost_center(update: CostCenterMappingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Inserta o actualiza un centro de costo.
- `api_delete_cost_center(code: str, db: DBSession, state: AppState = Depends(get_app_state))` - Elimina un centro de costo.
- `api_add_holiday(h: HolidayAdd, db: DBSession, state: AppState = Depends(get_app_state))` - Añade un feriado.
- `api_sync_holidays(db: DBSession, state: AppState = Depends(get_app_state))` - Sincroniza automáticamente los feriados nacionales (Chile).
- `api_delete_holiday(date_str: str, db: DBSession, state: AppState = Depends(get_app_state))` - Elimina un feriado.
- `api_get_query(query_id: str, db: DBSession, state: AppState = Depends(get_app_state))` - Retorna el estado visual de una consulta del Analytics Studio.
- `api_update_query(update: QueryUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Persiste el estado visual de una consulta.
- `api_get_schema(db: DBSession, state: AppState = Depends(get_app_state))` - Retorna el listado de tablas y sus columnas para el editor.
- `api_preview_table(table_name: str, db: DBSession, state: AppState = Depends(get_app_state))` - Previsualiza una tabla.
- `api_query_preview(update: QueryUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Ejecuta una consulta temporal y retorna datos para previsualización.
- `api_build_sql(payload: VisualQueryBuilderPayload, db: DBSession, state: AppState = Depends(get_app_state))` - Compila el estado visual del constructor en SQL parametrizado seguro.

### Interacción con Base de Datos
- Motor: SQLAlchemy ORM (Pilar 3)
- Tablas:
  - `analytics_snapshots`
- Columnas:
  - No se especifican columnas explícitas, solo consultas generales sobre la tabla `analytics_snapshots`.

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: `fastapi`, `pydantic`, `sqlalchemy`, `holidays`, `pandas`.
- Comunicación con otros archivos del proyecto:
  - `core.auth.require_admin`
  - `core.database.get_session_dep`
  - `core.models.StatusMapping`, `CostCenterMapping`, `AppSetting`, `Holiday`, `ConfigQuery`
  - `core.db_config_manager.load_config_to_memory`, `get_setting`, `get_status_mapping`, `get_cost_center_mapping`, `get_holidays`
  - `core.app_instance.templates`
  - `core.utils.sanitize_for_json`
  - `core.state.AppState`, `get_app_state`
  - `core.query_engine.build_sql_from_payload`


---

## Archivo: ./routes/sync.py

### Resumen Funcional
Este archivo contiene rutas para la sincronización de datos con gestión de concurrencia. Utiliza `TaskManager` para ejecutar tareas en segundo plano y proporciona endpoints para iniciar, monitorear y obtener el estado de las sincronizaciones.

### Catálogo de Funciones y Clases
- `get_tunnel_url(state: AppState = Depends(get_app_state))` - Retorna la URL pública del túnel (Ngrok).
- `get_sync_status(state: AppState = Depends(get_app_state))` - Retorna el estado actual de la sincronización.
- `sync_data(state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Inicia el proceso de sincronización de datos y lo encola en `TaskManager`.
- `list_tasks(limit: int = 20, state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Lista las tareas recientes del sistema.
- `get_task(task_id: str, state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Consulta el estado de una tarea específica por su ID.
- `_run_sync_pipeline()` - Ejecuta el pipeline completo de limpieza y consolidación.

### Interacción con Base de Datos
- Motor: No aplica (No hay consultas SQL crudas o llamadas a ORM).
- Tablas: `analytics_snapshots` (se intenta eliminar en la sincronización finalizada).

### Estado y Variables Globales
- `state.is_syncing`: Indica si una sincronización está en curso.
- `state.sync_lock`: Bloqueo para evitar ejecuciones duplicadas de la sincronización.

### Dependencias y Flujo
- Librerías externas: `logging`, `shutil`, `pathlib`, `typing`.
- Comunicación con otros archivos:
  - `core.auth.require_auth` (para autenticación).
  - `config.DB_PATH`, etc. (para configuraciones globales).
  - `core.state.AppState` y `get_app_state()` (para el estado de la aplicación).
  - `core.task_manager.task_manager` (para gestionar tareas en segundo plano).
  - `db.consolidator.DataConsolidator` (para consolidación de datos).
  - `core.database.get_session` (para obtener sesiones de base de datos).
  - `core.wms_utils.is_file_changed`, `mark_file_processed` (para manejo de archivos).
  - `services.etl.OutboundDeliveryAdapter`, etc. (para procesamiento de datos ETL).
  - `routes.transporte.sync_transporte_logic` (para sincronización de transporte).


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

## Archivo: ./routes/transporte.py

### Resumen Funcional
Este archivo contiene rutas para la sección de Transporte (Avanti), que incluyen funciones para sincronizar datos desde una base de datos externa SQLite, obtener datos consolidados diarios, buscar en los datos de transporte y servir archivos PDF.

### Catálogo de Funciones y Clases
- `sync_transporte_logic(session: Session)` - Lógica core para sincronizar la base de datos externa de OneDrive a local.
- `sync_transporte(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta POST para sincronizar datos de transporte manualmente.
- `get_transporte_data(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta GET para obtener los datos consolidados diarios ordenados cronológicamente.
- `search_transporte(q: str, session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta GET para buscar en la tabla cruda de transporte_entregas por OT, GD o OC.
- `serve_pdf(filename: str, user=Depends(get_current_user))` - Ruta GET para servir el archivo PDF desde el disco.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `transporte_entregas`
    - Columnas: `ot`, `proveedor`, `gd`, `oc`, `bulto`, `servicio`, `archivo`, `fecha`
  - `transporte_diario`
    - Columnas: `fecha`, `total_entregas`, `pdf_path`
- Consultas SQL crudas:
  - Creación de tablas si no existen
  - Lectura de datos desde la base de datos externa
  - Inserción de datos en las tablas locales
  - Consolidación de datos
  - Mapeo de PDFs

### Estado y Variables Globales
- `EXTERNAL_DB_PATH` - Ruta a la base de datos externa SQLite.
- `PDF_DIR_PATH` - Directorio donde se almacenan los archivos PDF.

### Dependencias y Flujo
- Librerías utilizadas: `os`, `sqlite3`, `logging`, `typing`, `fastapi`, `sqlalchemy`.
- Comunicación con otros archivos del proyecto:
  - `core.app_instance.templates` (no se muestra el contenido, pero probablemente para renderizar plantillas HTML).
  - `core.database.get_session_dep` y `core.auth.get_current_user` (para manejar la sesión y autenticación).


---

## Archivo: ./routes/widgets.py

### Resumen Funcional
El archivo `widgets.py` contiene endpoints FastAPI que manejan la lógica de negocio para obtener datos de widgets y realizar drilldowns. Los endpoints interactúan con una base de datos SQL para recuperar y procesar los datos, y utilizan un estado global para almacenar en caché resultados recientes.

### Catálogo de Funciones y Clases
- `get_widget_data(query_id: str, year: Optional[str] = None, area: Optional[str] = None, granularity: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user), state: AppState = Depends(get_app_state))` - Ejecuta el VisualQueryBuilderPayload y retorna la data estructurada.
- `get_widget_drilldown(query_id: str, segment: str, material: Optional[str] = None, year: Optional[str] = None, area: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user))` - Obtiene el detalle subyacente de un segmento de un widget.

### Interacción con Base de Datos
- **Motor:** SQLAlchemy ORM.
- **Tablas:** `ConfigQuery`, `outbound_deliveries`.
- **Columnas:**
  - `ConfigQuery`: `query_id`, `visual_state`, `sql_text`.
  - `outbound_deliveries`: `fecha_carga`, `entrega`, `pos_`, `cantidad`, `dias_retraso`, `material`.

### Estado y Variables Globales
- **Variables Globales:** No aplica.

### Dependencias y Flujo
- **Librerías Externas:** FastAPI, SQLAlchemy, Pandas.
- **Flujo Interno:**
  - Los endpoints dependen de funciones como `get_session_dep`, `get_current_user`, `execute_visual_query`, `sanitize_for_json`, y `build_sql_from_payload`.
  - Utilizan el estado global `AppState` para almacenar en caché resultados.


---

