# Documentación Técnica - Directorio: repositories
Compilado el: 2026-06-07 18:34:58
Modelo: qwen2.5-coder:7b | Separado por Carpetas

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

