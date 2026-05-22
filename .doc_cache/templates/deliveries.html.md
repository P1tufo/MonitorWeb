## Archivo: ./templates/deliveries.html (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para la interfaz de usuario del proyecto, que incluye elementos como encabezado, pestañas para diferentes secciones (Entregas, Movimientos, Gestión de OTs, IA Insomnio y Ansiedad, Documentación, Historial de Ubicaciones), y scripts JavaScript para manejar el comportamiento de las pestañas, filtros y modales.

### Catálogo de Funciones y Clases
- `switchTab(tabId, btnElement)` - Cambia la pestaña activa.
- `switchSubTab(subTabId, btnElement)` - Cambia la subpestaña activa.
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
- **Librerías externas utilizadas:**
  - Chart.js
  - Chartjs-plugin-datalabels
  - Font Awesome
  - marked

- **Archivos JavaScript incluidos:**
  - `deliveries.js`
  - `tasks.js`
  - `inventory.js`
  - `analytics_proyecciones.js`
  - `docs_explorer.js`

- **Archivos HTML parciales incluidos:**
  - `_styles.html`
  - `_tab_docs.html`
  - `_tab_historial.html`
  - `_tab_ia.html`
  - `_tab_deliveries.html`
  - `_tab_inventory.html`
  - `_tab_ots.html`
  - `_deliveries_modals.html`
  - `_inventory_modals.html`
  - `_analytics_proyecciones_modals.html`
  - `_edit_query_modal.html`
  - `_logout.html`

