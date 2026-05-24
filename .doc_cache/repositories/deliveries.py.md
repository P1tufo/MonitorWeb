## Archivo: ./repositories/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene una clase `DeliveriesRepository` que proporciona métodos para obtener estadísticas y datos relacionados con las entregas (`outbound_deliveries`). Utiliza pandas para procesar los resultados de consultas SQL ejecutadas contra una base de datos.

### Catálogo de Funciones y Clases
- **Clase:** `DeliveriesRepository`
  - **Métodos:**
    - `_sql(query_id: str, fallback: str) -> str`: Obtiene SQL desde config_queries con fallback explícito.
    - `_get_sla_threshold() -> int`: Obtiene el umbral de SLA (Service Level Agreement).
    - `get_area_stats(year: str) -> pd.DataFrame`: Obtiene estadísticas por área para un año dado.
    - `get_total_active_days(year: str) -> int`: Obtiene el número total de días activos en un año dado.
    - `get_sla_stats(year: str) -> pd.DataFrame`: Obtiene estadísticas de SLA para un año dado.
    - `get_top_authors(year: str) -> pd.DataFrame`: Obtiene los autores con más entregas en un año dado.
    - `get_dates_counts(year: str) -> pd.DataFrame`: Obtiene el conteo de fechas por área para un año dado.
    - `get_top_locations(year: str) -> pd.DataFrame`: Obtiene las ubicaciones con más items en un año dado.
    - `get_top_materials_by_area(year: str) -> pd.DataFrame`: Obtiene los materiales con más frecuencia por área en un año dado.
    - `get_area_material_mapping(year: str) -> pd.DataFrame`: Obtiene el mapeo de áreas a materiales en un año dado.
    - `get_user_material_mapping(year: str) -> pd.DataFrame`: Obtiene el mapeo de usuarios a materiales en un año dado.
    - `get_sla_audit_records(year: str, late: bool = True, limit: int = 500, where_clause: str = None, where_params: dict = None) -> pd.DataFrame`: Obtiene registros de auditoría de SLA para un año dado.
    - `get_monthly_evolution() -> pd.DataFrame`: Obtiene la evolución mensual de entregas y días activos.
    - `get_weekly_evolution() -> pd.DataFrame`: Obtiene la evolución semanal de entregas.
    - `get_wms_status_distribution(year: str) -> pd.DataFrame`: Obtiene la distribución del estado WMS para un año dado.
    - `get_lead_time_by_area(year: str) -> pd.DataFrame`: Obtiene el tiempo promedio de entrega por área en un año dado.
    - `get_sla_trend() -> pd.DataFrame`: Obtiene la tendencia de SLA a lo largo del tiempo.
    - `get_author_sla_correlation() -> pd.DataFrame`: Obtiene la correlación entre autores y SLA.
    - `get_volume_delay_trend() -> pd.DataFrame`: Obtiene la tendencia de volumen y retraso en el tiempo.
    - `get_sla_trend_by_area() -> pd.DataFrame`: Obtiene la tendencia de SLA por área a lo largo del tiempo.
    - `get_sla_monthly_trend() -> pd.DataFrame`: Obtiene la tendencia mensual de SLA.
    - `get_sla_monthly_trend_by_area() -> pd.DataFrame`: Obtiene la tendencia mensual de SLA por área.

### Interacción con Base de Datos
- **Motor:** SQLAlchemy (ORM)
- **Tablas y Columnas:**
  - Tabla: `outbound_deliveries`
    - Columnas: `entrega`, `autor`, `creado_el`, `fecha_sm_real`, `material`, `denominacion`, `dias_retraso`, `fecha_carga`, `ubicacion_bin`, `business_area`
  - Tabla: `warehouse_tasks`
    - Columna: `entrega`

### Estado y Variables Globales
- **No aplica**

### Dependencias y Flujo
- **Librerías Externas:** pandas, sqlalchemy
- **Flujo Interno:** El archivo interactúa con otros módulos como `core.db_config_manager`, `core.helpers.visual_query_adapter`, y `core.query_engine` para construir y ejecutar consultas SQL.

