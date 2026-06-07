## Archivo: ./templates/deliveries.html (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para la interfaz de usuario del sistema de monitoreo de almacén (WMS). Proporciona una vista consolidada con varias secciones, como entregas, movimientos, consumos y más. Incluye funcionalidades para filtrar y ordenar datos, así como modales para detalles adicionales.

### Catálogo de Funciones y Clases
- `switchTab(tabId, btnElement)` - Cambia la pestaña activa.
- `switchSubTab(subTabId, btnElement)` - Cambia la subpestaña activa.
- `openNonPalletizedDetails(user, claseMov)` - Abre un modal con detalles no paletizados.
- `initTableFilters()` - Inicializa los filtros de tablas.
- `filterOTTable()` - Filtra la tabla de OTs según criterios seleccionados.
- `filterDiscrepancyTable()` - Filtra la tabla de discrepancias según criterios seleccionados.
- `sortTableDiscrepancy(columnIndex)` - Ordena la tabla de discrepancias.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- Variables globales no detectadas directamente en el código proporcionado.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `Chart.js`
  - `chartjs-plugin-datalabels`
  - `marked`
  - `font-awesome`

- **Archivos del Proyecto Importados**:
  - `partials/_styles.html`
  - `css/deliveries.css`, `css/inventory.css`, `css/analytics_proyecciones.css`
  - `js/bundle.js`
  - `partials/_modals.html`, `_deliveries_modals.html`, `_inventory_modals.html`, `_analytics_proyecciones_modals.html`, `_edit_query_modal.html`, `_quick_login_modal.html`, `_logout.html`

- **Archivos del Proyecto que Importan a Este Archivo**:
  - No detectados directamente en el código proporcionado.

El flujo de datos se realiza principalmente mediante JavaScript para interactuar con la interfaz y cargar datos dinámicamente.

