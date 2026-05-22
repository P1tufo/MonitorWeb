## Archivo: ./services/deliveries_service.py

### Resumen Funcional
El archivo `deliveries_service.py` contiene una clase `DeliveriesService` que se encarga de generar un contexto completo para las entregas, incluyendo estadísticas, KPIs y datos relacionados con áreas, autores, ubicaciones y materiales. Utiliza SQLAlchemy para interactuar con la base de datos y pandas para procesar los datos.

### Catálogo de Funciones y Clases
- `DeliveriesService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `_get_bound_params_from_visual_state(visual_state_str: str) -> list` - Extrae parámetros de un estado visual en formato JSON.
- `_extract_metric_value(df, active_year: str = None) -> Any` - Extrae el valor numérico de una métrica de un DataFrame de forma segura.
- `get_full_context() -> Dict[str, Any]` - Genera el contexto completo para Entregas.
- `_prepare_area_stats(year, month_str)` - Prepara el DataFrame de estadísticas por área.
- `_calculate_kpis(sla_df, area_stats_df, total_dias)` - Calcula el diccionario de KPIs globales de forma segura.
- `_prepare_authors(year, month_str)` - Obtiene ranking de autores con comparativa mensual.
- `_prepare_locations(year, month_str)` - Obtiene ranking de ubicaciones con comparativa mensual.
- `_prepare_materials_by_area(year, month_str)` - Estructura el ranking de materiales por cada área de negocio.

### Interacción con Base de Datos
El archivo interactúa con una base de datos utilizando SQLAlchemy. Las tablas y columnas específicas son:
- Tablas: `outbound_deliveries`, `config_queries`
- Columnas: `fecha_carga`, `sql_text`, `visual_state`, `area`, `mes`, `semana`, `autor`, `centro`, `fecha`, `valor`, `total_qty`, `efficiency`, `ontime_qty`, `late_qty`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas: `sqlalchemy`, `pandas`, `logging`, `datetime`, `typing`.
- Comunicación con otros archivos del proyecto:
  - `core.utils.sanitize_for_json`
  - `core.state.get_app_state`
  - `repositories.DeliveriesRepository`
  - `routes.inventory.get_inventory_context`
  - `routes.tasks.get_tasks_context`
  - `routes.analytics_proyecciones.get_proyecciones_context`

