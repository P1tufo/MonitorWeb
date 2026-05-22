## Archivo: ./static/js/dashboard.js

### Resumen Funcional
El archivo `dashboard.js` contiene la lógica principal del dashboard de MonitorWeb. Define funciones para interactuar con una API, manejar la interfaz de usuario (UI), renderizar tablas y aplicar filtros.

### Catálogo de Funciones y Clases
- **DashboardAPI**
  - `_fetch(url, options)` - Realiza solicitudes HTTP a la API.
  - `fetchKPIs(params)` - Obtiene los KPIs basados en los parámetros proporcionados.
  - `fetchFilteredData(params)` - Obtiene datos filtrados según los parámetros proporcionados.
  - `sync()` - Sincroniza los datos del cliente con el servidor.
  - `checkSyncStatus()` - Verifica el estado de la sincronización.
  - `logout()` - Cierra sesión y redirige al usuario a la página de inicio de sesión.

- **UI**
  - `openPdfModal()` - Abre el modal para ver PDFs.
  - `closePdfModal()` - Cierra el modal y limpia su contenido.
  - `toggleMulti(id)` - Alterna la visibilidad de un elemento con el ID especificado.
  - `setBtnLoading(btn, text, isLoading)` - Establece el estado de carga de un botón.

- **Funciones Globales**
  - `renderTableRow(t)` - Renderiza una fila de tabla para los datos proporcionados.
  - `executeFilters()` - Ejecuta los filtros y actualiza la tabla y KPIs.
  - `applyFilters()` - Aplica los filtros cuando se cambia un valor de entrada.
  - `getCheckboxValues(className)` - Obtiene los valores de las casillas de verificación con el nombre de clase especificado.
  - `toggleSelectAll(className, isChecked)` - Alterna la selección de todas las casillas de verificación con el nombre de clase especificado.
  - `handleSmartCheckbox(cb, className, selectAllId, context)` - Maneja la selección inteligente de casillas de verificación.
  - `filterTable()` - Filtra la tabla según los valores de entrada.
  - `sortTable(idx)` - Ordena la tabla según el índice de columna especificado.
  - `updateLogoVal(btn)` - Actualiza el valor del campo oculto para incluir o no el logotipo en el PDF.
  - `pdfSubmit(btn, frameTarget, preview)` - Envía un formulario para generar y visualizar/descargar PDFs.
  - `downloadBulk(action, btn)` - Descarga múltiples PDFs según los parámetros proporcionados.
  - `syncData(e, onlyPoll = false)` - Inicia la sincronización de datos y verifica su estado.
  - `startSyncPolling(btn)` - Comienza el sondeo para verificar el estado de la sincronización.
  - `toggleSidebar()` - Alterna la visibilidad del sidebar.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: `fetch`
- **Flujo Interno**: El archivo interactúa con el backend a través de la API definida en `DashboardAPI` para obtener datos, ejecutar filtros y sincronizar información. La UI se actualiza dinámicamente según los resultados obtenidos.

