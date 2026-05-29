## Archivo: ./static/js/dashboard.js (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `dashboard.js` contiene la lógica principal del dashboard de MonitorWeb, que incluye funciones para interactuar con una API, manejar la interfaz de usuario y actualizar los datos en tiempo real.

### Catálogo de Funciones y Clases
- **DashboardAPI**
  - `_fetch(url, options = {})`: Realiza solicitudes HTTP a la API.
  - `fetchKPIs(params)`: Obtiene indicadores clave (KPIs).
  - `fetchFilteredData(params)`: Obtiene datos filtrados.
  - `sync()`: Sincroniza los datos del cliente con el servidor.
  - `checkSyncStatus()`: Verifica el estado de la sincronización.
  - `logout()`: Cierra sesión y limpia el almacenamiento local.

- **UI**
  - `openPdfModal()`: Abre un modal para ver PDFs.
  - `closePdfModal()`: Cierra el modal de PDFs.
  - `toggleMulti(id)`: Muestra u oculta elementos según su ID.
  - `setBtnLoading(btn, text, isLoading)`: Cambia el estado del botón a cargando o normal.

- **renderTableRow(t)**: Renderiza una fila de la tabla con los datos proporcionados.
- **executeFilters()**: Ejecuta los filtros y actualiza los KPIs y la tabla.
- **applyFilters()**: Aplica los filtros cuando se cambia un checkbox.
- **getCheckboxValues(className)**: Obtiene los valores de los checkboxes seleccionados.
- **toggleSelectAll(className, isChecked)**: Selecciona/deselecciona todos los checkboxes según el estado del checkbox "Seleccionar todo".
- **handleSmartCheckbox(cb, className, selectAllId, context)**: Maneja la selección inteligente de checkboxes.
- **filterTable()**: Filtra las filas de la tabla según los valores de búsqueda.
- **sortTable(idx)**: Ordena la tabla por una columna específica.
- **updateLogoVal(btn)**: Actualiza el valor del checkbox "Incluir Logo".
- **pdfSubmit(btn, frameTarget, preview)**: Envía un formulario para generar y visualizar PDFs.
- **downloadBulk(action, btn)**: Descarga o previsualiza múltiples PDFs según la acción seleccionada.
- **syncData(e, onlyPoll = false)**: Inicia la sincronización de datos y verifica su estado.
- **startSyncPolling(btn)**: Comienza el sondeo para verificar el estado de la sincronización.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción directa con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales en este archivo.

### Dependencias y Flujo
- **Librerías Externas**: `fetch`, `Chart.js`, `ChartDataLabels`.
- **Flujo Interno**: El archivo interactúa con la API para obtener datos, actualiza el estado de los KPIs y la tabla, maneja eventos del usuario (como clics en botones y checkboxes), y renderiza elementos de la interfaz de usuario.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `dashboard.js` se encarga de inicializar y configurar los elementos del dashboard, incluyendo la sincronización de estado de radio buttons y la carga de widgets inmediatamente al iniciar.

### Catálogo de Funciones y Clases
- `initSaaSWidgets()` - Inicia el motor SaaS y carga los widgets inmediatamente al iniciar.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencia externa: `DashboardAPI` (se utiliza para verificar el estado de sincronización).

