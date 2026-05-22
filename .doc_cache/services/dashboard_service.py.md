## Archivo: ./services/dashboard_service.py

### Resumen Funcional
El archivo `dashboard_service.py` contiene una clase `DashboardService` que se encarga de cargar y preparar los datos necesarios para un dashboard. Esta clase interactúa con una base de datos SQL utilizando SQLAlchemy y pandas para procesar los datos.

### Catálogo de Funciones y Clases
- **DashboardService(session: Session)** - Inicializa la instancia con una sesión de base de datos.
- **get_full_context()** - Orquesta la carga de todos los datos necesarios para el dashboard, incluyendo gráficos, KPIs, selectores y transacciones recientes.
- **_prepare_weekly_chart(year: int)** - Prepara los datos para el gráfico de intensidad semanal.
- **_calculate_dashboard_kpis(start_week: str, year_str: str)** - Calcula los indicadores clave de rendimiento (KPIs) desde una semana base.
- **_prepare_selectors(min_week: str)** - Obtiene listas únicas de fechas y áreas, además de mapeos de autores y centros.
- **_get_recent_transactions(week_str: str)** - Obtiene el listado de las últimas entregas para la tabla principal.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQL utilizando SQLAlchemy. Las tablas utilizadas son:
- `outbound_deliveries`
- `config_cost_center_mapping`
- `autor_area_mapping`

Las columnas específicas que se están leyendo o modificando incluyen:
- `week_sort`, `week_label`, `area_negocio` y otras columnas de `outbound_deliveries`.
- `business_area`, `center_code` y otras columnas de `config_cost_center_mapping`.
- `autor`, `area_negocio` y otras columnas de `autor_area_mapping`.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
Las dependencias externas utilizadas son:
- `sqlalchemy`
- `pandas`

El archivo se comunica con otros archivos del proyecto a través de la clase `DashboardService`, que es instanciada y utilizada para obtener los datos necesarios para el dashboard.

