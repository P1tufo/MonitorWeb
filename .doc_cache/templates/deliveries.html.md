## Archivo: ./templates/deliveries.html (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para la interfaz de usuario del proyecto, que incluye elementos como encabezado, botones de pestañas y scripts JavaScript para manejar el comportamiento de las pestañas y cargar datos dinámicamente.

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
  - marked.js

- **Archivos JavaScript que se comunican con este archivo:**
  - `core_ui.js`
  - `dashboard.js`
  - `saas_engine.js`
  - `deliveries.js`
  - `consumos.js`
  - `transporte.js`

Estos archivos JavaScript probablemente contienen la lógica de negocio y los controladores que interactúan con el backend para cargar datos y manejar eventos.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML que contiene scripts para cargar datos JSON y referencias a archivos JavaScript. También incluye varios modales parciales.

### Catálogo de Funciones y Clases
No se detectan funciones ni clases definidas en este fragmento de código.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No se detectan variables globales, de sesión o de entorno quemadas en el código.

### Dependencias y Flujo
- **Librerías externas utilizadas**: No se mencionan librerías específicas.
- **Archivos JavaScript incluidos**:
  - `js/tasks.js` (versión 5)
  - `js/inventory.js` (versión 11)
  - `js/analytics_proyecciones.js` (versión 3)
  - `js/docs_explorer.js` (versión 5)
  - `js/productivity.js` (versión 21)

- **Modales incluidos**:
  - `_modals.html`
  - `_deliveries_modals.html`
  - `_inventory_modals.html`
  - `_analytics_proyecciones_modals.html`
  - `_edit_query_modal.html`
  - `_quick_login_modal.html`
  - `_logout.html`

Este archivo se utiliza para cargar datos JSON y referencias a scripts JavaScript, además de incluir varios modales parciales que probablemente contienen funcionalidades específicas del sistema.

