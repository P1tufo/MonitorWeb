## Archivo: ./repositories/dashboard.py

### Resumen Funcional
El archivo `dashboard.py` contiene funciones para obtener datos filtrados y estadísticas necesarios para el dashboard principal del sistema de monitoreo de almacén (WMS). Estas funciones interactúan con la base de datos SQLite para recuperar información sobre entregas, KPIs, gráficos de intensidad y selectores para el dashboard.

### Catálogo de Funciones y Clases
- `build_unified_where(date: Optional[str], area: Optional[str], centro: Optional[str], has_ots_filter: Optional[str], min_week: Optional[str])` - Construye una cláusula WHERE unificada basada en los filtros proporcionados.
- `get_filtered_transactions(date: Optional[str], entrega: Optional[str], area: Optional[str], centro: Optional[str], has_ots_filter: Optional[str], min_week: Optional[str]) -> list` - Obtiene transacciones filtradas y las devuelve como una lista de diccionarios.
- `get_filtered_kpis(date: Optional[str], area: Optional[str], centro: Optional[str], min_week: Optional[str], iso_year: int) -> dict` - Calcula KPIs basados en los filtros proporcionados y el año especificado.
- `get_weekly_intensity_chart(year: int) -> dict` - Prepara datos para un gráfico de intensidad semanal.
- `get_dashboard_selectors(min_week: str) -> dict` - Obtiene listas únicas de fechas, áreas, mapeos de autores y centros.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `outbound_deliveries`, `config_cost_center_mapping`, `autor_area_mapping`
- **Columnas:**
  - `outbound_deliveries`: `fecha_carga`, `fecha_sm_real`, `creado_el`, `entrega`, `material`, `estado_wms`, `dias_retraso`, `week_sort`, `area_negocio`, `centro_costo`, `ubicacion_bin_1`, `ubicacion_bin`
  - `config_cost_center_mapping`: `center_code`, `business_area`
  - `autor_area_mapping`: `autor`, `area_negocio`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `pandas`, `sqlalchemy`
- **Archivos del Proyecto que Importan a este Archivo:**
  - Ninguno
- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.macros` (importado en `build_unified_where`)
- **Dirección del Flujo de Datos:** El archivo consume datos de la base de datos y los procesa para devolver resultados al servicio o controlador que lo invoque.

