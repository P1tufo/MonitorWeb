## Archivo: ./templates/deliveries.html (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para la interfaz de usuario del proyecto, que incluye elementos como encabezado, botones de pestañas y scripts JavaScript para manejar el comportamiento de las pestañas y cargar datos dinámicamente.

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
- Librerías externas utilizadas:
  - Chart.js
  - marked.js
  - Font Awesome
- Archivos JavaScript incluidos:
  - `core_ui.js`
  - `dashboard.js`
  - `saas_engine.js`
  - `deliveries.js`
  - `consumos.js`
  - `transporte.js`
- Variables JSON inyectadas dinámicamente desde el backend.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML que contiene scripts para cargar datos JSON y referencias a archivos JavaScript. También incluye varios modales parciales.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento de código.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `ots_user_confirmed`: Almacena datos del usuario confirmado.
- `ots_type_labels`: Almacena etiquetas de tipo OTS.
- `ots_type_data`: Almacena datos de tipo OTS.

### Dependencias y Flujo
- **Librerías externas**: No se mencionan librerías externas específicas en este fragmento.
- **Archivos JavaScript incluidos**:
  - `js/tasks.js`
  - `js/inventory.js`
  - `js/analytics_proyecciones.js`
  - `js/docs_explorer.js`

- **Modales parciales incluidos**:
  - `_modals.html`
  - `_deliveries_modals.html`
  - `_inventory_modals.html`
  - `_analytics_proyecciones_modals.html`
  - `_edit_query_modal.html`
  - `_quick_login_modal.html`
  - `_logout.html`

Este archivo se utiliza para cargar datos y recursos necesarios en una página web, incluyendo modales que probablemente contienen funcionalidades adicionales.

