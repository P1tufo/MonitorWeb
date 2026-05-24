## Archivo: ./static/js/dashboard.js (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `dashboard.js` contiene la lógica principal del dashboard de MonitorWeb, que incluye funciones para interactuar con una API, manejar la interfaz de usuario (UI), renderizar tablas y gráficos, aplicar filtros, y gestionar la sincronización de datos.

### Catálogo de Funciones y Clases
- `DashboardAPI._fetch(url, options = {})` - Realiza solicitudes HTTP a la API.
- `DashboardAPI.fetchKPIs(params)` - Obtiene los KPIs (Indicadores Clave de Desempeño) basados en los parámetros proporcionados.
- `DashboardAPI.fetchFilteredData(params)` - Obtiene datos filtrados según los parámetros proporcionados.
- `DashboardAPI.sync()` - Sincroniza los datos del cliente con el servidor.
- `DashboardAPI.checkSyncStatus()` - Verifica si la sincronización está en curso.
- `DashboardAPI.logout()` - Cierra sesión y limpia el almacenamiento local.
- `UI.openPdfModal()` - Abre un modal para ver PDFs.
- `UI.closePdfModal()` - Cierra el modal de PDF.
- `UI.toggleMulti(id)` - Alterna la visibilidad de elementos con una clase específica.
- `UI.setBtnLoading(btn, text, isLoading)` - Establece el estado de carga de un botón.
- `renderTableRow(t)` - Renderiza una fila de tabla HTML.
- `executeFilters()` - Ejecuta los filtros y actualiza la interfaz del usuario.
- `applyFilters()` - Aplica los filtros cuando se cambia algún valor.
- `getCheckboxValues(className)` - Obtiene los valores de las casillas de verificación seleccionadas.
- `toggleSelectAll(className, isChecked)` - Alterna el estado de todas las casillas de verificación en una clase específica.
- `handleSmartCheckbox(cb, className, selectAllId, context)` - Maneja la selección inteligente de casillas de verificación.
- `filterTable()` - Filtra la tabla según los valores de búsqueda.
- `sortTable(idx)` - Ordena la tabla por una columna específica.
- `updateLogoVal(btn)` - Actualiza el valor del logo en un formulario.
- `pdfSubmit(btn, frameTarget, preview)` - Envía un formulario para generar y visualizar PDFs.
- `downloadBulk(action, btn)` - Descarga o previsualiza múltiples PDFs según la acción seleccionada.
- `syncData(e, onlyPoll = false)` - Inicia la sincronización de datos y maneja el estado de carga del botón.
- `startSyncPolling(btn)` - Comienza a sondear el estado de la sincronización.
- `initSaaSWidgets(params = null)` - Inicializa los widgets SaaS en el dashboard.
- `renderSaaSChart(container, queryId, data)` - Renderiza un gráfico SaaS.
- `renderSaaSTrellis(container, queryId, data)` - Renderiza una trillera de gráficos SaaS.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción directa con bases de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales en este archivo.

### Dependencias y Flujo
- **Librerías Externas**: `fetch`, `Chart.js`, `ChartDataLabels`.
- **Flujo Interno**: El archivo interactúa con la API a través de las funciones del objeto `DashboardAPI` para obtener datos, ejecutar filtros, renderizar tablas y gráficos, manejar la sincronización, etc. La interfaz de usuario se actualiza en respuesta a los eventos del usuario y las respuestas de la API.

