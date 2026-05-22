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

