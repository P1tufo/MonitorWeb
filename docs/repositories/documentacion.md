# Documentación Técnica - Directorio: repositories
Compilado el: 2026-05-22 16:53:13
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./repositories/__init__.py

### Resumen Funcional
Este archivo es el punto de entrada para la configuración y la inyección de dependencias de los repositorios en una aplicación FastAPI que utiliza SQLite como base de datos.

### Catálogo de Funciones y Clases
- `get_db()` - Establece una conexión a la base de datos SQLite y la devuelve. La conexión se cierra automáticamente al finalizar el contexto.
- `get_deliveries_repo(conn: sqlite3.Connection = Depends(get_db))` - Crea e inicializa un repositorio para operaciones relacionadas con entregas.
- `get_inventory_repo(conn: sqlite3.Connection = Depends(get_db))` - Crea e inicializa un repositorio para operaciones relacionadas con el inventario.
- `get_tasks_repo(conn: sqlite3.Connection = Depends(get_db))` - Crea e inicializa un repositorio para operaciones relacionadas con tareas.

### Interacción con Base de Datos
- Motor de base de datos: SQLite
- Tablas y Columnas: No aplica (se asume que las tablas y columnas están definidas en los repositorios `DeliveriesRepository`, `InventoryRepository` y `TasksRepository`)
- Consultas SQL Crudas o ORM: Se utiliza el módulo `sqlite3` para interactuar con la base de datos.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `fastapi`: Para manejar las dependencias en FastAPI.
- Comunicación con otros archivos del proyecto:
  - Importa clases y funciones desde los módulos `base.py`, `deliveries.py`, `inventory.py` y `tasks.py`.


---

## Archivo: ./repositories/base.py

### Resumen Funcional
Clase base para todos los repositorios de datos que proporciona una sesión de SQLAlchemy y un método para obtener consultas SQL desde una configuración.

### Catálogo de Funciones y Clases
- `BaseRepository(session: Session)` - Inicializa la clase con una sesión de SQLAlchemy.
- `_sql(query_id: str, fallback: str) -> str` - Obtiene un SQL desde la BD de configuración, con fallback.

### Interacción con Base de Datos
- Motor: No aplica (no hay consultas SQL crudas o llamadas a ORM explícitas).
- Tablas y Columnas: No aplica (no interactúa directamente con tablas).

### Estado y Variables Globales
- No aplica (no define variables globales, de sesión, de entorno o diccionarios quemados en código que almacenan estado crítico).

### Dependencias y Flujo
- Librerías externas utilizadas: `sqlalchemy.orm.Session`, `core.wms_config.get_query`.
- Comunicación con otros archivos del proyecto: No aplica (no comunica con otros archivos).


---

## Archivo: ./repositories/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene una clase `DeliveriesRepository` que proporciona métodos para obtener estadísticas y datos relacionados con las entregas. Estos métodos interactúan con una base de datos para recuperar información sobre áreas, retrasos, autores, ubicaciones y materiales.

### Catálogo de Funciones y Clases
- `DeliveriesRepository(BaseRepository)` - Repositorio para el dominio de Entregas.
  - `_sql(query_id: str, fallback: str) -> str` - Reemplaza `{AREA_EXPR}` en la consulta SQL con una expresión CASE que determina el área basada en diferentes campos.
  - `_get_sla_threshold() -> int` - Obtiene el umbral de SLA (Service Level Agreement) desde las configuraciones del sistema.
  - `get_area_stats(year: str) -> pd.DataFrame` - Devuelve estadísticas por área, incluyendo el número total de entregas y días activos.
  - `get_total_active_days(year: str) -> int` - Calcula el número total de días activos en un año específico.
  - `get_sla_stats(year: str) -> pd.DataFrame` - Devuelve estadísticas sobre el cumplimiento del SLA por entrega.
  - `get_top_authors(year: str) -> pd.DataFrame` - Obtiene los autores con más entregas y su área asociada.
  - `get_dates_counts(year: str) -> pd.DataFrame` - Cuenta las entregas por fecha y área.
  - `get_top_locations(year: str) -> pd.DataFrame` - Devuelve las ubicaciones con más materiales y su área asociada.
  - `get_top_materials_by_area(year: str) -> pd.DataFrame` - Muestra los materiales más frecuentes por área.
  - `get_area_material_mapping(year: str) -> pd.DataFrame` - Mapea el material por área y cantidad.
  - `get_user_material_mapping(year: str) -> pd.DataFrame` - Mapea el material por usuario y cantidad.
  - `get_sla_audit_records(year: str, late: bool = True, limit: int = 500) -> pd.DataFrame` - Devuelve registros de auditoría del SLA basados en retrasos.
  - `get_monthly_evolution() -> pd.DataFrame` - Muestra la evolución mensual de entregas y días activos.
  - `get_weekly_evolution() -> pd.DataFrame` - Muestra la evolución semanal de entregas.
  - `get_wms_status_distribution(year: str) -> pd.DataFrame` - Distribución del estado WMS (Warehouse Management System).
  - `get_lead_time_by_area(year: str) -> pd.DataFrame` - Tiempo promedio de entrega por área.
  - `get_sla_trend() -> pd.DataFrame` - Tendencia del SLA a lo largo del tiempo.
  - `get_author_sla_correlation() -> pd.DataFrame` - Correlación entre el autor y el retraso en el SLA.
  - `get_volume_delay_trend() -> pd.DataFrame` - Tendencia de volumen y retardo.
  - `get_sla_trend_by_area() -> pd.DataFrame` - Tendencia del SLA por área a lo largo del tiempo.
  - `get_sla_monthly_trend() -> pd.DataFrame` - Tendencia mensual del SLA.
  - `get_sla_monthly_trend_by_area() -> pd.DataFrame` - Tendencia mensual del SLA por área.

### Interacción con Base de Datos
- Motor: SQLite (inferred from the use of SQLAlchemy's `text` function).
- Tablas:
  - `outbound_deliveries`
- Columnas:
  - `area`, `entrega`, `fecha_carga`, `dias_retraso`, `autor`, `creado_el`, `fecha_sm_real`, `material`, `denominacion`, `estado_wms`, `week_sort`, `week_label`

### Estado y Variables Globales
- No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas`
  - `sqlalchemy`
- Comunicación con otros archivos del proyecto:
  - `core.db_config_manager` (para obtener configuraciones)


---

## Archivo: ./repositories/inventory.py

### Resumen Funcional
El archivo `inventory.py` contiene una clase `InventoryRepository` que proporciona métodos para obtener estadísticas y datos de inventario desde una base de datos SQLite. Los métodos incluyen consultas para volumen, área, materiales consumidos, usuarios activos, tendencias temporales, días hábiles y tipos de material.

### Catálogo de Funciones y Clases
- `InventoryRepository(BaseRepository)` - Repositorio para el dominio de Inventario (ex-Movimientos).
  - `get_cmv_prod()` - Devuelve el valor de la configuración "CMV_PROD".
  - `get_cmv_mant()` - Devuelve el valor de la configuración "CMV_MANT".
  - `get_cmv_consumos()` - Devuelve una tupla con los valores de "CMV_PROD" y "CMV_MANT".
  - `get_cmv_reversas()` - Devuelve una tupla con los valores de "CMV_REVERSAS".
  - `check_table_exists()` - Verifica si la tabla 'inventory_movements' existe en la base de datos.
  - `_FALLBACK_QUERIES` - Diccionario con consultas SQL para diferentes estadísticas.
  - `_sql(query_id: str, fallback: str = "") -> str` - Obtiene una consulta SQL a partir del diccionario o devuelve una consulta de respaldo si no se encuentra.
  - `get_volumen_stats()` - Devuelve un DataFrame con las estadísticas de volumen de movimientos.
  - `get_area_stats_prod()` - Devuelve un DataFrame con las estadísticas de área para materiales de producción.
  - `get_material_consumos_abc()` - Devuelve un DataFrame con las estadísticas de consumo ABC.
  - `get_top_users(start_year: str = '2026') -> pd.DataFrame` - Devuelve un DataFrame con los usuarios más activos.
  - `get_trend_stats(start_year: str = '2025') -> pd.DataFrame` - Devuelve un DataFrame con las tendencias temporales de movimientos.
  - `get_dow_stats()` - Devuelve un DataFrame con las estadísticas de días hábiles.
  - `get_pm_type_material_records()` - Devuelve un DataFrame con los tipos de material según el tipo de mantenimiento.
  - `get_area_material_mapping_201()` - Devuelve un DataFrame con la asignación de materiales por área para CMV 201.
  - `get_user_material_mapping(users: Tuple[str, ...]) -> pd.DataFrame` - Devuelve un DataFrame con la asignación de materiales por usuario y tipo de movimiento.
  - `get_location_material_summary()` - Devuelve un DataFrame con las estadísticas de resumen de ubicaciones de materiales.
  - `get_total_active_days()` - Devuelve el número total de días activos en los movimientos.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `inventory_movements`
- Columnas:
  - `tipo_operacion`, `material`, `cantidad`, `fe_contab`, `usuario`, `alm`, `cmv`, `ce_coste`, `texto_breve_material`, `texto_cab_documento`, `referencia`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas:
  - `pandas`
  - `sqlalchemy`
- Flujo interno: La clase interactúa con una instancia de `BaseRepository` para obtener la sesión de base de datos y ejecutar consultas SQL.


---

## Archivo: ./repositories/tasks.py

### Resumen Funcional
Este archivo contiene un repositorio de datos para el dominio de tareas de almacén, que proporciona métodos para obtener resúmenes y tendencias de las tareas, así como detalles específicos sobre las tareas.

### Catálogo de Funciones y Clases
- `get_tasks_summary()` - Obtiene un resumen de las tareas agrupadas por código y nombre.
- `get_tasks_trend()` - Obtiene una tendencia diaria de creación y confirmación de tareas.
- `get_tasks_by_user()` - Obtiene el número de tareas creadas y confirmadas por usuario.
- `get_tasks_by_type_dest()` - Obtiene un resumen de las tareas agrupadas por tipo de destino.
- `get_recent_tasks()` - Obtiene las tareas recientes que no han sido confirmadas.
- `get_non_palletized_movements()` - Obtiene los movimientos no paletizados más recientes.
- `get_non_palletized_count()` - Cuenta el número de movimientos no paletizados.
- `get_non_palletized_summary()` - Obtiene un resumen de los movimientos no paletizados, incluyendo detalles sobre la fecha más antigua y más reciente.

### Interacción con Base de Datos
- Motor: PostgreSQL (deducido del uso de SQLAlchemy).
- Tablas:
  - `warehouse_tasks`
  - `lx02_pendientes`
  - `inventory_movements`
- Columnas:
  - `cl_mov`, `clase_mov`, `COUNT(*)`, `SUM(ctd_teor_dsd)`, `fe_creac`, `fecha_conf`, `usuario`, `material`, `texto_breve_material`, `ubic_proc`, `ubic_dest`, `hora`, `otcuanto`, `pos`, `denominacion`, `stock_disp`, `alm`, `ce`, `doc_mat`, `cmv`, `usuario_conf`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas: `pandas`, `sqlalchemy`.
- No se comunica con otros archivos del proyecto.


---

