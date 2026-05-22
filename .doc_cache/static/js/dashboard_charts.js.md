## Archivo: ./static/js/dashboard_charts.js

### Resumen Funcional
Este archivo JavaScript se encarga de inicializar y gestionar un gráfico de barras pilaado en el panel de control, calculando y mostrando la suma total de los datos para cada categoría. También proporciona funcionalidades para seleccionar/deseleccionar todos los elementos del gráfico.

### Catálogo de Funciones y Clases
- `stackedTotalPlugin` - Plugin que agrega una etiqueta con el total acumulado en cada barra del gráfico.
  - Parámetros: `chart` (el contexto del gráfico).
  - Propósito: Calcula la suma total de los datos para cada categoría y muestra esta suma en la parte superior de las barras.

- `initWeeklyChart(chartLabels, chartDatasets)` - Inicializa el gráfico de barras pilaado.
  - Parámetros: `chartLabels` (etiquetas del eje X), `chartDatasets` (conjuntos de datos para el gráfico).
  - Propósito: Configura y muestra el gráfico con los datos proporcionados.

- `toggleChartSelectAll(isChecked)` - Función que selecciona/deselecciona todos los elementos del gráfico.
  - Parámetros: `isChecked` (booleano, indica si se debe seleccionar o deseleccionar).
  - Propósito: Actualiza el estado de selección de todos los checkboxes relacionados con el gráfico.

- `updateChartVisibility()` - Función que actualiza la visibilidad de los conjuntos de datos del gráfico según las selecciones.
  - Parámetros: Ninguno.
  - Propósito: Oculta o muestra los conjuntos de datos del gráfico según qué checkboxes están seleccionados.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
- `window.weeklyChart` - Variable global que almacena el contexto del gráfico inicializado.

### Dependencias y Flujo
- **Librerías Externas**: `Chart.js` (usado para crear y gestionar el gráfico).
- **Flujo Interno**: El archivo se comunica con otros elementos del DOM para obtener referencias a checkboxes y elementos de entrada, y también interactúa con la función `applyFilters` si está definida.

