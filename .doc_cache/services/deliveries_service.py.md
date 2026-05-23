## Archivo: ./services/deliveries_service.py

### Resumen Funcional
El archivo `deliveries_service.py` contiene una clase `DeliveriesService` que se encarga de generar un contexto completo para las entregas, incluyendo estadísticas, KPIs y datos relacionados con autores, ubicaciones y materiales. Utiliza SQLAlchemy para interactuar con la base de datos y pandas para procesar los datos.

### Catálogo de Funciones y Clases
- `DeliveriesService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `get_full_context()` - Genera el contexto completo para las entregas, incluyendo estadísticas, KPIs y datos relacionados.
- `_prepare_area_stats(year, month_str)` - Prepara el DataFrame de estadísticas por área.
- `_calculate_kpis(sla_df, area_stats_df, total_dias)` - Calcula el diccionario de KPIs globales de forma segura.
- `_prepare_authors(year, month_str)` - Obtiene ranking de autores con comparativa mensual.
- `_prepare_locations(year, month_str)` - Obtiene ranking de ubicaciones con comparativa mensual.
- `_prepare_materials_by_area(year, month_str)` - Estructura el ranking de materiales por cada área de negocio.

### Interacción con Base de Datos
El archivo interactúa con una base de datos utilizando SQLAlchemy. Las tablas y columnas específicas son:
- Tabla: `outbound_deliveries`
  - Columna: `fecha_carga`
- Tabla: `config_queries`
  - Columnas: `query_id`, `sql_text`, `visual_state`
- Tabla: `area_stats`
  - Columnas: `area`, `total_entregas`, `dias_activos`
- Tabla: `top_authors`
  - Columnas: `name`, `entregas`
- Tabla: `top_locations`
  - Columnas: `ubicacion`, `num_items`
- Tabla: `top_materials_by_area`
  - Columnas: `area`, `material`, `frequency`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
Dependencias:
- `sqlalchemy.orm.Session` - Para la sesión de base de datos.
- `pandas` - Para procesar los datos.
- `logging` - Para el registro de errores.
- `datetime` - Para manejar fechas.
- `typing` - Para tipos de datos.
- `core.utils.sanitize_for_json` - Para sanitizar datos para JSON.
- `core.state.get_app_state` - Para obtener el estado de la aplicación.
- `repositories.DeliveriesRepository` - Para interactuar con la base de datos.
- `core.query_engine.get_bound_params_from_visual_state` - Para obtener parámetros de consulta.
- `core.query_engine.extract_metric_value` - Para extraer métricas de los resultados de consulta.

Flujo:
El archivo se comunica con otros archivos del proyecto a través de las siguientes importaciones:
- `routes.inventory.get_inventory_context`
- `routes.tasks.get_tasks_context`
- `routes.analytics_proyecciones.get_proyecciones_context`

Estas funciones son llamadas para obtener contextos adicionales que se incluyen en el contexto final.

