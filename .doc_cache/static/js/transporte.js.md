## Archivo: ./static/js/transporte.js

### Resumen Funcional
El archivo `transporte.js` es un script JavaScript que se encarga de cargar y mostrar datos de transporte en una interfaz web. Realiza solicitudes a una API para obtener información sobre entregas, renderiza gráficos y tablas con estos datos, y permite la búsqueda y visualización de PDFs.

### Catálogo de Funciones y Clases
- `loadData()` - Carga los datos de transporte desde la API y actualiza la interfaz.
- `getMonday(dateStr)` - Calcula la fecha del lunes correspondiente a una fecha dada.
- `updateTransporteChartGroup(group)` - Actualiza el grupo de datos para el gráfico de transporte.
- `loadPendingData()` - Carga los datos pendientes de entrega y los muestra en una tabla con detalles agrupados por mes y fecha.
- `renderChart()` - Renderiza un gráfico de líneas mostrando las entregas y bultos según el grupo seleccionado (mensual o semanal).
- `renderTable(data)` - Renderiza una tabla con los últimos 25 registros de transporte.
- `openPdfViewer(url)` - Abre un modal para visualizar un PDF.
- `closePdfViewer()` - Cierra el modal y detiene la carga del PDF.
- `searchTransporte()` - Realiza una búsqueda en tiempo real de datos de transporte según un término ingresado.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos. Todas las operaciones de lectura y escritura se realizan a través de solicitudes HTTP a la API FastAPI.

### Estado y Variables Globales
- `chartInstance` - Almacena la instancia del gráfico actual.
- `allTransporteData` - Almacena todos los datos de transporte cargados desde la API.
- `currentChartGroup` - Almacena el grupo actual seleccionado para el gráfico (mensual o semanal).
- `transporteSearchTimeout` - Almacena un temporizador para el debouncing en la búsqueda.

### Dependencias y Flujo
- **Dependencias**: 
  - `fetch` - Para hacer solicitudes HTTP.
  - `Chart.js` y `ChartDataLabels` - Para renderizar gráficos.
  
- **Flujo de Datos**:
  - El archivo se carga en el DOM (`DOMContentLoaded`).
  - Llama a `loadData()` al cargar la página.
  - `loadData()` hace una solicitud a `/api/transporte/data` para obtener los datos de transporte y luego llama a `renderChart()`, `renderTable()`, y `loadPendingData()`.
  - `loadPendingData()` hace una solicitud a `/api/transporte/pending` para obtener los datos pendientes.
  - Los eventos de clic en los elementos del DOM (como botones, encabezados de tabla) invocan funciones como `updateTransporteChartGroup()`, `openPdfViewer()`, y `closePdfViewer()`.
  - La función `searchTransporte()` se ejecuta cuando el usuario ingresa texto en un campo de búsqueda.

