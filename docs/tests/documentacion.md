# Documentación Técnica - Directorio: tests
Compilado el: 2026-06-05 03:03:51
Modelo: qwen2.5-coder:7b | Separado por Carpetas

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

