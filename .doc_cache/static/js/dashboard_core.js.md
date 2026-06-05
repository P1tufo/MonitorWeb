## Archivo: ./static/js/dashboard_core.js

### Resumen Funcional
El archivo `dashboard_core.js` contiene funciones y métodos para renderizar filas de una tabla, ejecutar filtros en un panel de control de almacén, manejar la interacción con el usuario (como seleccionar checkboxes y ordenar tablas), generar PDFs y sincronizar datos.

### Catálogo de Funciones y Clases
- `renderTableRow(t)` - Renderiza una fila de tabla con los detalles del pedido.
- `executeFilters()` - Ejecuta los filtros aplicados por el usuario en la interfaz.
- `applyFilters()` - Aplica los filtros cuando se selecciona un checkbox o se cambia el estado de "Seleccionar todo".
- `getCheckboxValues(className)` - Obtiene los valores de los checkboxes con una clase específica.
- `toggleSelectAll(className, isChecked)` - Maneja la selección de todos los checkboxes en una categoría.
- `handleSmartCheckbox(cb, className, selectAllId, context)` - Maneja el comportamiento inteligente de los checkboxes.
- `filterTable()` - Filtra las filas de la tabla según los criterios de búsqueda ingresados por el usuario.
- `sortTable(idx)` - Ordena las filas de la tabla según una columna específica.
- `updateLogoVal(btn)` - Actualiza el valor del checkbox que indica si se debe incluir el logo en el PDF.
- `pdfSubmit(btn, frameTarget, preview)` - Envía un formulario para generar y descargar PDFs.
- `downloadBulk(action, btn)` - Genera y descarga PDFs en lote según los criterios de filtro.
- `syncData(e, onlyPoll = false)` - Inicia la sincronización de datos con el servidor y maneja el estado de carga.
- `startSyncPolling(btn)` - Comienza a sondear el estado de la sincronización.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales explícitas definidas en este archivo. Las funciones utilizan elementos del DOM para almacenar y recuperar estado, como checkboxes seleccionados y valores de entrada de usuario.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas.
- **Flujo de Datos**:
  - `dashboard_core.js` es consumido por el archivo que contiene la interfaz del usuario (no especificado en el fragmento).
  - El archivo consume funciones de `DashboardAPI`, lo que sugiere que existe un módulo separado para interactuar con el backend.
  - Los datos se obtienen a través de llamadas asíncronas (`Promise.all`) a `DashboardAPI.fetchKPIs` y `DashboardAPI.fetchFilteredData`.
  - Los resultados son utilizados para actualizar la interfaz del usuario, incluyendo la tabla de pedidos, los KPIs y las notificaciones.

Este archivo es crucial para el funcionamiento del panel de control en el sistema de monitoreo de almacén, proporcionando funcionalidades avanzadas como filtros dinámicos, generación de PDFs y sincronización de datos.

