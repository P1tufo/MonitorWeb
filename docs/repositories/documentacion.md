# Documentación Técnica - Directorio: repositories
Compilado el: 2026-06-07 12:50:47
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./repositories/__init__.py

### Resumen Funcional
Este archivo es el punto de entrada para la configuración y la inyección de dependencias relacionadas con las operaciones de base de datos en un sistema de monitoreo de almacén (WMS). Define funciones para obtener conexiones a la base de datos SQLite y repositorios específicos para diferentes entidades del sistema.

### Catálogo de Funciones y Clases
- `get_db()` - Establece una conexión a la base de datos SQLite y la devuelve. La conexión se cierra automáticamente al finalizar el contexto.
- `get_deliveries_repo(conn: sqlite3.Connection = Depends(get_db))` - Devuelve una instancia del repositorio de entregas utilizando la conexión proporcionada.
- `get_inventory_repo(conn: sqlite3.Connection = Depends(get_db))` - Devuelve una instancia del repositorio de inventario utilizando la conexión proporcionada.
- `get_tasks_repo(conn: sqlite3.Connection = Depends(get_db))` - Devuelve una instancia del repositorio de tareas utilizando la conexión proporcionada.
- `get_productivity_repo(conn: sqlite3.Connection = Depends(get_db))` - Devuelve una instancia del repositorio de productividad utilizando la conexión proporcionada.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:** No se especifican explícitamente en este archivo. Se asume que los repositorios (`DeliveriesRepository`, `InventoryRepository`, `TasksRepository`, `ProductivityRepository`) interactúan con tablas correspondientes, pero no se detalla qué columnas son utilizadas.
- **Consultas SQL Crudas o ORM:** No hay consultas SQL crudas ni llamadas a ORM directamente en este archivo. Las operaciones de base de datos se realizan a través de los métodos de los repositorios.

### Estado y Variables Globales
No se detectan variables globales, de sesión, de entorno o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- **Librerías Externas:** `sqlite3`, `fastapi`
- **Archivos del Proyecto que IMPORTA (consume):** No se especifican archivos externos que importen este archivo.
- **Archivos del Proyecto que IMPORTAN a Este Archivo (lo consumen):** Los repositorios (`DeliveriesRepository`, `InventoryRepository`, `TasksRepository`, `ProductivityRepository`) y la configuración de base de datos (`config.py`).
- **Dirección del Flujo de Datos:** El flujo de datos comienza en las rutas (Routes), pasa por los servicios (Services) hasta llegar a este archivo para obtener una conexión a la base de datos y luego a los repositorios específicos.


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
El archivo `dashboard.py` contiene métodos para obtener datos filtrados y estadísticas necesarios para el dashboard principal del sistema de monitoreo de almacén (WMS). Estos métodos interactúan con la base de datos SQLite para recuperar información sobre entregas, KPIs, gráficos de intensidad y selectores.

### Catálogo de Funciones y Clases
- `build_unified_where(date: str, area: str, centro: str, has_ots_filter: str, min_week: str)` - Construye una cláusula WHERE unificada para las consultas SQL.
- `get_filtered_transactions(date: str, entrega: str, area: str, centro: str, has_ots_filter: str, min_week: str) -> list` - Obtiene transacciones filtradas según los criterios proporcionados y devuelve un DataFrame de pandas.
- `get_filtered_kpis(date: str, area: str, centro: str, min_week: str, iso_year: int) -> dict` - Calcula KPIs basados en las entregas filtradas y devuelve un diccionario con los resultados formateados.
- `get_weekly_intensity_chart(year: int) -> dict` - Prepara los datos para el gráfico de intensidad semanal.
- `get_dashboard_selectors(min_week: str) -> dict` - Obtiene listas únicas de fechas y áreas, además de mapeos de autores y centros.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `outbound_deliveries`, `config_cost_center_mapping`, `warehouse_tasks`, `autor_area_mapping`
- **Columnas:**
  - `outbound_deliveries`: `fecha_carga`, `fecha_sm_real`, `creado_el`, `entrega`, `material`, `estado_wms`, `dias_retraso`, `week_sort`, `area_negocio`, `centro_costo`, `ubicacion_bin_1`, `ubicacion_bin`
  - `config_cost_center_mapping`: `center_code`, `business_area`
  - `warehouse_tasks`: `entrega`
  - `autor_area_mapping`: `autor`, `area_negocio`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Dependencias Externas:** pandas, sqlalchemy
- **Archivos Importados por Este Archivo:**
  - `./base.py`
  - `core.macros`
- **Archivos que Importan a Este Archivo:**
  - Ninguno

**Flujo de Datos:**
1. `dashboard.py` importa y utiliza métodos desde `base.py` y `core.macros`.
2. Los métodos en `dashboard.py` realizan consultas SQL utilizando SQLAlchemy para interactuar con la base de datos SQLite.
3. Los resultados de las consultas se procesan y formatean en pandas DataFrames o diccionarios según sea necesario.
4. Los métodos devuelven los resultados al servicio que los consume, generalmente a través de endpoints FastAPI definidos en otro archivo del proyecto.


---

## Archivo: ./repositories/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene métodos para interactuar con la base de datos SQLite y obtener registros relacionados con entregas en un sistema de almacén (WMS). Los métodos permiten consultar registros de entrega, realizar auditorías SLA, obtener detalles de entregas por lotes y recuperar información sobre áreas de negocio.

### Catálogo de Funciones y Clases
- `DeliveriesRepository(BaseRepository)` - Repositorio para el dominio de Entregas (outbound_deliveries).
  - `_sql(query_id: str, fallback: str) -> str` - Obtiene SQL desde config_queries con fallback explícito.
  - `_get_sla_threshold() -> int` - Retorna el umbral SLA configurado en la base de datos.
  - `get_sla_audit_records(year: str, late: bool = True, limit: int = 500, where_clause: str = None, where_params: dict = None) -> pd.DataFrame` - Obtiene registros de auditoría SLA para entregas.
  - `get_deliveries_for_bulk(date: str = None, area: str = None, centro: str = None, has_ots_filter: str = None, entrega_query: str = None) -> pd.DataFrame` - Obtiene detalles de entregas por lotes.
  - `get_area_lookup() -> pd.DataFrame` - Obtiene una lista de áreas de negocio asociadas a las entregas.
  - `get_picking_items(entrega_ids: list) -> pd.DataFrame` - Obtiene los elementos de picking para un conjunto de entregas.
  - `get_delivery_by_id(entrega: str) -> pd.DataFrame` - Obtiene detalles de una entrega específica por su ID.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - `outbound_deliveries`
  - `warehouse_tasks`
  - `DeliverySummary`
- Columnas:
  - `entrega`, `autor`, `area_negocio`, `creado_el`, `fecha_sm_real`, `material`, `denominacion`, `dias_retraso`, `sla_limit`, `has_ots` en `outbound_deliveries`
  - `entrega_id`, `entrega`, `autor`, `ubicacion_bin`, `material`, `descripcion`, `cantidad`, `umb`, `area`, `entrega` en `warehouse_tasks`
  - `entrega_id`, `entrega`, `area_negocio` en `DeliverySummary`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `pandas`
  - `sqlalchemy`
- Archivos del proyecto que IMPORTA a este archivo (`deliveries.py`):
  - `core.db_config_manager`
  - `core.macros`
  - `repositories.base`
- Archivos del proyecto que este archivo IMPORTA (`deliveries.py`):
  - Ninguno
- Flujo de datos:
  - El archivo importa y utiliza métodos de otras clases para interactuar con la base de datos y procesar los resultados en formato DataFrame.


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
El archivo `productivity.py` contiene métodos para obtener resúmenes diarios, mensuales y detalles de movimientos de usuarios en un sistema de almacén (WMS). Utiliza SQLAlchemy para interactuar con una base de datos SQLite y pandas para procesar los resultados.

### Catálogo de Funciones y Clases
- `_get_raw_activities_cte(is_monthly=False)`: Genera una Common Table Expression (CTE) que une todos los eventos de actividad desde diferentes tablas.
- `get_available_dates()`: Devuelve una lista ordenada de fechas únicas en formato YYYY-MM-DD con movimientos generados o confirmados.
- `_get_daily_summary(date_sap: str)`: Obtiene un resumen diario de movimientos y actividades por usuario.
- `_get_hourly_trend(date_sap: str)`: Genera una tendencia horaria de las actividades por usuario.
- `_get_inactivity_gaps(date_sap: str)`: Identifica los huecos de inactividad en el movimiento de usuarios.
- `_get_activity_heatmap(date_sap: str)`: Crea un mapa de calor de las actividades diarias por usuario y franja horaria.
- `get_user_movements_daily_summary(target_date: str, usuario: str)`: Obtiene un resumen diario de movimientos por operación para un usuario específico.
- `get_user_movements_daily_details(target_date: str, usuario: str, operacion: str)`: Detalla los movimientos diarios de un usuario para una operación específica.
- `_get_monthly_summary(month_sap: str)`: Obtiene un resumen mensual de movimientos y actividades por usuario.
- `_get_monthly_shifts(month_sap: str)`: Genera un resumen mensual de las actividades por usuario y turno.
- `_get_monthly_heatmap(month_sap: str)`: Crea un mapa de calor de las actividades mensuales por usuario y día de la semana.
- `get_user_movements_monthly_summary(target_month: str, usuario: str)`: Obtiene un resumen mensual de movimientos por operación para un usuario específico.
- `get_user_movements_monthly_details(target_month: str, usuario: str, operacion: str)`: Detalla los movimientos mensuales de un usuario para una operación específica.
- `_format_date_sap(target_date: str)`: Formatea una fecha en formato SAP (DD.MM.YYYY).
- `_format_month_sap(target_month: str)`: Formatea un mes en formato SAP (MM.YYYY).

### Interacción con Base de Datos
- Motor de BD: SQLite.
- Tablas:
  - `inventory_movements`
  - `warehouse_tasks`
- Columnas:
  - `inventory_movements`: `usuario`, `registrado`, `hora`, `doc_mat`, `tipo_operacion`, `texto_cab_documento`, `cmv`, `material`, `texto_breve_material`, `cantidad`.
  - `warehouse_tasks`: `usuario_conf`, `fecha_conf`, `hor_conf`, `numero_ot`, `ctd_teor_dsd`.

### Estado y Variables Globales
- No hay variables globales, de sesión o de entorno definidas en este archivo.

### Dependencias y Flujo
- Librerías externas: `logging`, `re`, `pandas`.
- Archivos del proyecto que importan a este archivo:
  - `core.macros`
  - `repositories.base.BaseRepository`
- Archivos del proyecto que este archivo importa:
  - Ninguno.
- Flujo de datos: El archivo consume datos desde la base de datos SQLite y los procesa con pandas, luego devuelve resultados en formato JSON.


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
El archivo `widgets.py` contiene métodos para ejecutar consultas dinámicas y generar visualizaciones de datos en un sistema de monitoreo de almacén (WMS). Utiliza FastAPI, SQLAlchemy y SQLite para interactuar con la base de datos.

### Catálogo de Funciones y Clases
- `execute_widget(query_id: str, visual_state: str, year: Optional[str], area: Optional[str], granularity: Optional[str]) -> Dict[str, Any]` - Ejecuta una consulta dinámica para generar una visualización de datos.
- `execute_drilldown(query_id: str, visual_state: str, segment: str, material: Optional[str], year: Optional[str]) -> list` - Realiza un drilldown en los datos para obtener detalles adicionales.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: `outbound_deliveries`
    - Columnas: `fecha_carga`, `entrega`, `pos_`, `cantidad`, `dias_retraso`, `material`, `denominacion`

### Estado y Variables Globales
- No hay variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `sqlalchemy`
  - `json`
  - `logging`
  - `typing`

- **Archivos del Proyecto que Importan a este Archivo (lo consumen):**
  - No se mencionan archivos específicos.

- **Flujo de Datos:**
  - El archivo importa funciones y clases desde otros módulos (`core.helpers.dynamic_executor`, `core.query_engine`, `core.schemas`, `core.utils`) para ejecutar consultas dinámicas y generar visualizaciones.
  - Los métodos `execute_widget` y `execute_drilldown` interactúan con la base de datos mediante SQLAlchemy y pandas, procesando los resultados para generar visualizaciones.


---

