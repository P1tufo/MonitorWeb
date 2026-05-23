## Archivo: ./services/dashboard_service.py

### Resumen Funcional
Este archivo contiene el servicio `DashboardService` que se encarga de cargar la página principal del dashboard. Orquesta la carga de todos los datos necesarios para el dashboard, incluyendo gráficos, indicadores clave de rendimiento (KPIs) y listas únicas de fechas y áreas.

### Catálogo de Funciones y Clases
- `DashboardService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `get_full_context()` - Orquesta la carga de todos los datos necesarios para el dashboard.
- `_prepare_weekly_chart(year: int)` - Prepara los datos para el gráfico de intensidad semanal.
- `_calculate_dashboard_kpis(start_week: str, year_str: str)` - Calcula los indicadores clave de rendimiento (KPIs) desde una semana base.
- `_prepare_selectors(min_week: str)` - Obtiene listas únicas de fechas y áreas, además de mapeos de autores y centros.
- `_get_recent_transactions(week_str: str)` - Obtiene el listado de las últimas entregas para la tabla principal.

### Interacción con Base de Datos
- Motor: SQLite (inferred from `pd.read_sql`)
- Tablas:
  - `outbound_deliveries`
  - `config_cost_center_mapping`
  - `autor_area_mapping`
- Columnas:
  - `outbound_deliveries`: `week_sort`, `week_label`, `area_negocio`, `entrega`, `material`, `estado_wms`, `dias_retraso`, `fecha_carga`, `fecha_sm_real`, `creado_el`
  - `config_cost_center_mapping`: `center_code`, `business_area`
  - `autor_area_mapping`: `autor`, `area_negocio`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `logging`
  - `sqlalchemy.orm.Session`
  - `pandas as pd`
  - `itertools`
  - `typing`
  - `datetime`
- No comunica con otros archivos del proyecto directamente.

