## Archivo: ./templates/deliveries.html (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para la interfaz de usuario del proyecto, que incluye elementos como encabezados, botones de pestañas y scripts JavaScript para manejar el comportamiento de las pestañas y cargar datos dinámicamente.

### Catálogo de Funciones y Clases
- `switchTab(tabId, btnElement)` - Cambia la pestaña activa.
- `openNonPalletizedDetails(user, claseMov)` - Abre un modal con detalles no paletizados.
- `initTableFilters()` - Inicializa los filtros de tablas.
- `filterOTTable()` - Filtra la tabla de OTs según los criterios seleccionados.
- `filterDiscrepancyTable()` - Filtra la tabla de Discrepancias según los criterios seleccionados.
- `sortTableDiscrepancy(columnIndex)` - Ordena la tabla de Discrepancias.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías externas**: 
  - Chart.js
  - Chartjs-plugin-datalabels
  - Font Awesome
  - marked
- **Archivos JavaScript**:
  - `core_ui.js`
  - `deliveries.js`
  - `inventory.js`
  - `analytics_proyecciones.js`
  - `docs_explorer.js`
- **Archivos CSS**:
  - Estilos definidos en el archivo y referencias a archivos externos
- **Datos JSON**: 
  - Datos inyectados desde variables de contexto del servidor (por ejemplo, `area_stats_json`, `weekdays`, etc.)

