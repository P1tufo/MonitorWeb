## Archivo: ./templates/deliveries.html (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para la interfaz de usuario del sistema de monitoreo de almacén (WMS). Contiene el diseño y las funcionalidades necesarias para mostrar diferentes secciones como entregas, movimientos, consumos, etc., con un menú de pestañas interactiva.

### Catálogo de Funciones y Clases
- `switchTab(tabId, btnElement)` - Cambia la pestaña activa.
- `switchSubTab(subTabId, btnElement)` - Cambia la subpestaña activa.
- `openNonPalletizedDetails(user, claseMov)` - Abre un modal con detalles no paletizados.
- `initTableFilters()` - Inicializa los filtros de tablas.
- `filterOTTable()` - Filtra la tabla de OTs según los criterios seleccionados.
- `filterDiscrepancyTable()` - Filtra la tabla de discrepancias según los criterios seleccionados.
- `sortTableDiscrepancy(columnIndex)` - Ordena la tabla de discrepancias.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
No hay variables globales explícitas definidas en el código. Las variables están almacenadas en elementos `<script type="application/json">` que contienen datos JSON serializados.

### Dependencias y Flujo
- **Librerías externas**: Chart.js, marked.js, Font Awesome.
- **Archivos del proyecto importados**:
  - `partials/_styles.html`
  - `css/deliveries.css`, `css/inventory.css`, `css/analytics_proyecciones.css`
  - `js/core_ui.js`, `js/dashboard_api.js`, `js/dashboard_core.js`, `js/dashboard_saas.js`, `js/saas_engine_core.js`, `js/saas_engine_drilldown.js`, `js/deliveries.js`, `js/consumos.js`, `js/transporte.js`
- **Archivos del proyecto que importan a este archivo**: No especificados en el fragmento.

El flujo de datos se gestiona principalmente mediante eventos JavaScript y la manipulación del DOM.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para el sistema de monitoreo de almacén (WMS). Contiene variables JSON que se utilizan en scripts JavaScript y carga varios archivos JavaScript adicionales.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `ots_trend_created`
- `ots_trend_confirmed`
- `ots_user_labels`
- `ots_user_created`
- `ots_user_confirmed`
- `ots_type_labels`
- `ots_type_data`

### Dependencias y Flujo
- Archivos JavaScript:
  - `js/tasks.js` (versión 5)
  - `js/inventory.js` (versión 21)
  - `js/analytics_proyecciones.js` (versión 3)
  - `js/docs_explorer.js` (versión 5)
  - `js/productivity_daily.js` (versión 2)
  - `js/productivity_monthly.js` (versión 2)
  - `js/productivity_modals.js` (versión 2)

- Archivos HTML incluidos:
  - `_modals.html`
  - `_deliveries_modals.html`
  - `_inventory_modals.html`
  - `_analytics_proyecciones_modals.html`
  - `_edit_query_modal.html`
  - `_quick_login_modal.html`
  - `_logout.html`

El archivo `deliveries.html` carga varios scripts JavaScript y partials HTML, lo que indica un flujo de datos hacia el cliente para la visualización y interacción con los datos del sistema de almacén.

