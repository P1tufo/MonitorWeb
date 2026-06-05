# Documentación Técnica - Directorio: repositories
Compilado el: 2026-06-05 03:03:51
Modelo: qwen2.5-coder:7b | Separado por Carpetas

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

