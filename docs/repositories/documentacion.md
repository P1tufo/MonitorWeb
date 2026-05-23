# Documentación Técnica - Directorio: repositories
Compilado el: 2026-05-23 00:11:14
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
La clase `BaseRepository` proporciona una estructura base para interactuar con bases de datos mediante SQLAlchemy. Define métodos para obtener consultas SQL y verificar el estado visual de las mismas.

### Catálogo de Funciones y Clases
- `__init__(self, session: Session)` - Inicializa la instancia con una sesión de SQLAlchemy.
- `_sql(self, query_id: str, fallback: str) -> str` - Obtiene un SQL desde la base de datos de configuración o devuelve un fallback hardcodeado si no existe.
- `_has_visual_state(self, query_id: str) -> bool` - Verifica si una consulta tiene un estado visual JSON almacenado.

### Interacción con Base de Datos
- Motor: SQLAlchemy
- Tablas: `config_queries`
- Columnas: `query_id`, `sql_text`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sqlalchemy.orm.Session`
  - `core.wms_config.get_query`
  - `core.db_config_manager.get_query_visual_state`
- Comunicación con otros archivos del proyecto:
  - `core/query_engine.build_sql_from_payload()` (mencionado en la documentación, pero no implementado)


---

## Archivo: ./repositories/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene una clase `DeliveriesRepository` que proporciona métodos para obtener estadísticas y datos relacionados con las entregas (`outbound_deliveries`). Estos métodos realizan consultas SQL en una base de datos utilizando SQLAlchemy y pandas para procesar los resultados.

### Catálogo de Funciones y Clases
- `DeliveriesRepository(BaseRepository)` - Repositorio para el dominio de Entregas (outbound_deliveries).
  - `_sql(query_id: str, fallback: str) -> str` - Obtiene SQL desde config_queries con fallback explícito.
  - `_get_sla_threshold() -> int` - Retorna el umbral SLA configurado en las variables de entorno.
  - `get_area_stats(year: str) -> pd.DataFrame` - Obtiene estadísticas por área para un año dado.
  - `get_total_active_days(year: str) -> int` - Cuenta los días activos de entrega para un año dado.
  - `get_sla_stats(year: str) -> pd.DataFrame` - Obtiene estadísticas de SLA para un año dado.
  - `get_top_authors(year: str) -> pd.DataFrame` - Obtiene los autores con más entregas en un año dado.
  - `get_dates_counts(year: str) -> pd.DataFrame` - Obtiene el conteo de entregas por fecha y área para un año dado.
  - `get_top_locations(year: str) -> pd.DataFrame` - Obtiene las ubicaciones con más entregas en un año dado.
  - `get_top_materials_by_area(year: str) -> pd.DataFrame` - Obtiene los materiales con mayor frecuencia por área para un año dado.
  - `get_area_material_mapping(year: str) -> pd.DataFrame` - Mapea el material por área y cantidad para un año dado.
  - `get_user_material_mapping(year: str) -> pd.DataFrame` - Mapea el material por usuario y cantidad para un año dado.
  - `get_sla_audit_records(year: str, late: bool = True, limit: int = 500) -> pd.DataFrame` - Obtiene registros de auditoría de SLA para un año dado.
  - `get_monthly_evolution() -> pd.DataFrame` - Obtiene la evolución mensual de entregas y días activos.
  - `get_weekly_evolution() -> pd.DataFrame` - Obtiene la evolución semanal de entregas.
  - `get_wms_status_distribution(year: str) -> pd.DataFrame` - Distribución del estado WMS para un año dado.
  - `get_lead_time_by_area(year: str) -> pd.DataFrame` - Tiempo promedio de entrega por área para un año dado.
  - `get_sla_trend() -> pd.DataFrame` - Tendencia de SLA semanal.
  - `get_author_sla_correlation() -> pd.DataFrame` - Correlación entre el autor y el SLA.
  - `get_volume_delay_trend() -> pd.DataFrame` - Tendencia del volumen y retraso por semana.
  - `get_sla_trend_by_area() -> pd.DataFrame` - Tendencia de SLA semanal por área.
  - `get_sla_monthly_trend() -> pd.DataFrame` - Tendencia mensual de SLA.
  - `get_sla_monthly_trend_by_area() -> pd.DataFrame` - Tendencia mensual de SLA por área.

### Interacción con Base de Datos
- Motor: SQLAlchemy (no especificado el motor exacto).
- Tablas:
  - `outbound_deliveries`
  - `warehouse_tasks`
- Columnas:
  - `entrega`, `fecha_carga`, `dias_retraso`, `autor`, `material`, `denominacion`, `estado_wms`, `creado_el`, `fecha_sm_real`, `ubicacion_bin`, `business_area`, `week_sort`, `week_label`
- Consultas SQL crudas:
  - Todas las consultas SQL utilizan parámetros de enlace (`?`) para evitar inyecciones SQL.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas: pandas, sqlalchemy.
- Comunicación con otros archivos del proyecto:
  - `core.db_config_manager` (para obtener configuraciones de variables de entorno).


---

## Archivo: ./repositories/inventory.py

### Resumen Funcional
El archivo `inventory.py` contiene una clase `InventoryRepository` que se encarga de interactuar con la base de datos para obtener estadísticas y datos relacionados con el inventario, utilizando SQL queries y pandas DataFrames.

### Catálogo de Funciones y Clases
- **Clase:** `InventoryRepository`
  - **Métodos:**
    - `get_cmv_prod()`: Devuelve el valor configurado para CMV_PROD.
    - `get_cmv_mant()`: Devuelve el valor configurado para CMV_MANT.
    - `get_cmv_consumos()`: Devuelve una tupla con los valores de CMV_PROD y CMV_MANT.
    - `get_cmv_reversas()`: Devuelve una tupla con los valores configurados para CMV_REVERSAS.
    - `check_table_exists()`: Verifica si la tabla 'inventory_movements' existe en la base de datos.
    - `get_volumen_stats()`: Obtiene estadísticas de volumen del inventario.
    - `get_area_stats_prod()`: Obtiene estadísticas por área para el producto.
    - `get_material_consumos_abc()`: Obtiene estadísticas de materiales consumidos en ABC.
    - `get_top_users(start_year='2026')`: Obtiene los usuarios con más movimientos.
    - `get_trend_stats(start_year='2025')`: Obtiene tendencias de movimientos por período.
    - `get_dow_stats()`: Obtiene estadísticas diarias de movimiento.
    - `get_pm_type_material_records()`: Obtiene registros de tipo PM y material.
    - `get_area_material_mapping_201()`: Obtiene mapeo de área para el producto 201.
    - `get_user_material_mapping(users: Tuple[str, ...])`: Obtiene mapeo de usuario y material.
    - `get_location_material_summary()`: Obtiene resumen de materiales por ubicación.
    - `get_total_active_days()`: Obtiene el número total de días activos en los movimientos.

### Interacción con Base de Datos
- **Motor:** SQLite (inferred from the use of `sqlite_master`).
- **Tablas:** `inventory_movements`.
- **Columnas:**
  - `tipo_operacion`
  - `material`
  - `num_tx`
  - `business_area`
  - `ce_coste`
  - `cmv`
  - `fe_contab`
  - `alm`
  - `usuario`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- **Librerías Externas:** pandas, sqlalchemy.
- **Flujo Interno:** Utiliza métodos de la clase base `BaseRepository` para interactuar con la base de datos.


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

