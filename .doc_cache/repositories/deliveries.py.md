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

