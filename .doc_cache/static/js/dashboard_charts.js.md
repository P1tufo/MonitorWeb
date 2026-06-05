## Archivo: ./static/js/dashboard_charts.js

### Resumen Funcional
Este archivo JavaScript (`dashboard_charts.js`) se encarga de inicializar y gestionar un gráfico de barras pilaado en el panel de control del sistema de monitoreo de almacén (WMS). El gráfico muestra datos agrupados por áreas y centros, con la capacidad de seleccionar/deseleccionar ciertas áreas o centros para mostrar u ocultar sus datos en el gráfico.

### Catálogo de Funciones y Clases
- `stackedTotalPlugin(id: string, afterDatasetsDraw: function)` - Plugin para calcular y mostrar el total acumulado en cada barra del gráfico.
  - Parámetros:
    - `id`: Identificador único del plugin.
    - `afterDatasetsDraw`: Función que se ejecuta después de dibujar los conjuntos de datos, calculando y mostrando el total acumulado.

- `initWeeklyChart(chartLabels: Array<string>, chartDatasets: Array<Object>)` - Inicializa el gráfico de barras pilaado.
  - Parámetros:
    - `chartLabels`: Etiquetas para los ejes X del gráfico.
    - `chartDatasets`: Conjuntos de datos que se mostrarán en el gráfico.

- `toggleChartSelectAll(isChecked: boolean)` - Función para seleccionar/deseleccionar todos los checkboxes relacionados con áreas y centros.
  - Parámetros:
    - `isChecked`: Valor booleano que indica si se debe seleccionar o deseleccionar todos los checkboxes.

- `updateChartVisibility()` - Actualiza la visibilidad de los conjuntos de datos del gráfico según las selecciones realizadas en los checkboxes.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `window.weeklyChart`: Variable global que almacena el objeto del gráfico inicializado.

### Dependencias y Flujo
- **Dependencias**: No se mencionan dependencias externas específicas.
- **Flujo de Datos**:
  - El archivo importa funciones y variables desde otros archivos del proyecto, pero no se muestra cómo estos archivos están estructurados o qué datos fluyen entre ellos.
  - Los eventos DOM (`DOMContentLoaded`, `change` en checkboxes) desencadenan la inicialización y actualización del gráfico.

