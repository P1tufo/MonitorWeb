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
- Librerías externas utilizadas:
  - Chart.js
  - marked.js
  - Font Awesome
- Archivos JavaScript incluidos:
  - `core_ui.js`
  - `dashboard.js`
  - `saas_engine.js`
  - `deliveries.js`
  - `tasks.js`
  - `inventory.js`
  - `analytics_proyecciones.js`
  - `docs_explorer.js`

- Archivos CSS incluidos:
  - Estilos generales
  - Estilos específicos para entregas, inventario, análisis de proyecciones

El archivo interactúa con varios componentes del proyecto, incluyendo scripts y estilos que manejan la interfaz de usuario y el comportamiento dinámico.

