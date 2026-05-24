## Archivo: ./services/deliveries_service.py

### Resumen Funcional
El archivo `deliveries_service.py` contiene una clase `DeliveriesService` que se encarga de generar un contexto completo para las entregas, incluyendo estadísticas, gráficos y métricas dinámicas. Utiliza SQLAlchemy para interactuar con la base de datos y pandas para procesar los datos.

### Catálogo de Funciones y Clases
- `DeliveriesService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `get_full_context()` - Genera el contexto completo para las entregas, incluyendo estadísticas, gráficos y métricas dinámicas.
- `_execute_dynamic_kpi(query_id: str, default_params: tuple, raw_year: str)` - Ejecuta una consulta dinámica para calcular KPIs basados en parámetros de visualización.
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
  - Columnas: `sql_text`, `visual_state`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
Dependencias externas:
- `sqlalchemy.orm.Session`
- `pandas`
- `logging`
- `datetime`
- `typing`
- `core.utils.sanitize_for_json`
- `core.state.get_app_state`
- `repositories.DeliveriesRepository`
- `core.query_engine.get_bound_params_from_visual_state`
- `core.query_engine.extract_metric_value`

Flujo:
El archivo se comunica con otros archivos del proyecto a través de funciones como `get_inventory_context`, `get_tasks_context` y `get_proyecciones_context`.

