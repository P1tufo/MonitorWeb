## Archivo: ./static/js/transporte.js

### Resumen Funcional
El archivo `transporte.js` es un script que se encarga de cargar y mostrar datos de transporte en un gráfico y una tabla. Los datos son obtenidos a través de una API, filtrados y agrupados según el grupo seleccionado (mensual o semanal), y luego renderizados en un gráfico de líneas y una tabla.

### Catálogo de Funciones y Clases
- `loadData()` - Carga los datos de transporte desde la API y los renderiza.
- `getMonday(dateStr)` - Calcula la fecha del lunes correspondiente a una fecha dada.
- `updateTransporteChartGroup(group)` - Actualiza el grupo de datos para el gráfico y vuelve a renderizarlo.
- `renderChart()` - Renderiza el gráfico de transporte basado en los datos cargados.
- `renderTable(data)` - Renderiza la tabla de transporte con los últimos 25 registros.
- `openPdfViewer(url)` - Abre un modal para ver un PDF.
- `closePdfViewer()` - Cierra el modal y detiene la carga del PDF.
- `searchTransporte()` - Realiza una búsqueda en tiempo real en los datos de transporte.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con bases de datos.

### Estado y Variables Globales
- `chartInstance` - Almacena la instancia actual del gráfico.
- `allTransporteData` - Almacena todos los datos de transporte cargados desde la API.
- `currentChartGroup` - Almacena el grupo actual seleccionado para el gráfico (mensual o semanal).
- `transporteSearchTimeout` - Almacena el timeout para el debouncer del buscador.

### Dependencias y Flujo
- **Librerías Externas**: `fetch`, `Chart.js`, `ChartDataLabels`.
- **Flujo Interno**: El archivo se carga al DOMContentLoaded, luego llama a `loadData()`. `loadData()` realiza una solicitud fetch a la API para obtener los datos de transporte, que luego son renderizados en el gráfico y la tabla. Los eventos como el cambio de grupo del gráfico o la búsqueda activan funciones específicas para actualizar el contenido visual.

