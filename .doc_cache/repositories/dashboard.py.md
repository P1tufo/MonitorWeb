## Archivo: ./repositories/dashboard.py

### Resumen Funcional
El archivo `dashboard.py` contiene métodos para obtener datos filtrados y estadísticas necesarios para el dashboard principal del sistema de monitoreo de almacén (WMS). Estos métodos interactúan con la base de datos SQLite para recuperar información sobre entregas, KPIs, gráficos de intensidad y selectores.

### Catálogo de Funciones y Clases
- `build_unified_where(date: str, area: str, centro: str, has_ots_filter: str, min_week: str)` - Construye una cláusula WHERE unificada para las consultas SQL.
- `get_filtered_transactions(date: str, entrega: str, area: str, centro: str, has_ots_filter: str, min_week: str) -> list` - Obtiene transacciones filtradas según los criterios proporcionados y devuelve un DataFrame de pandas.
- `get_filtered_kpis(date: str, area: str, centro: str, min_week: str, iso_year: int) -> dict` - Calcula KPIs basados en las entregas filtradas y devuelve un diccionario con los resultados formateados.
- `get_weekly_intensity_chart(year: int) -> dict` - Prepara los datos para el gráfico de intensidad semanal.
- `get_dashboard_selectors(min_week: str) -> dict` - Obtiene listas únicas de fechas y áreas, además de mapeos de autores y centros.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `outbound_deliveries`, `config_cost_center_mapping`, `warehouse_tasks`, `autor_area_mapping`
- **Columnas:**
  - `outbound_deliveries`: `fecha_carga`, `fecha_sm_real`, `creado_el`, `entrega`, `material`, `estado_wms`, `dias_retraso`, `week_sort`, `area_negocio`, `centro_costo`, `ubicacion_bin_1`, `ubicacion_bin`
  - `config_cost_center_mapping`: `center_code`, `business_area`
  - `warehouse_tasks`: `entrega`
  - `autor_area_mapping`: `autor`, `area_negocio`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Dependencias Externas:** pandas, sqlalchemy
- **Archivos Importados por Este Archivo:**
  - `./base.py`
  - `core.macros`
- **Archivos que Importan a Este Archivo:**
  - Ninguno

**Flujo de Datos:**
1. `dashboard.py` importa y utiliza métodos desde `base.py` y `core.macros`.
2. Los métodos en `dashboard.py` realizan consultas SQL utilizando SQLAlchemy para interactuar con la base de datos SQLite.
3. Los resultados de las consultas se procesan y formatean en pandas DataFrames o diccionarios según sea necesario.
4. Los métodos devuelven los resultados al servicio que los consume, generalmente a través de endpoints FastAPI definidos en otro archivo del proyecto.

