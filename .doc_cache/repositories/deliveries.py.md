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

