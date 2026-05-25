## Archivo: ./static/js/saas_engine.js

### Resumen Funcional
El archivo `saas_engine.js` es un motor SaaS que se encarga de leer contenedores con la clase `.saas-widget-v2`, obtener datos a través de una API y renderizar gráficos o KPIs en estos contenedores. El motor maneja diferentes tipos de widgets, como KPI numéricos y trellis (múltiples minigráficos), y permite el filtrado por área y año.

### Catálogo de Funciones y Clases
- `initSaaSWidgetsV2(params = null, rootElement = document)` - Inicializa los widgets SaaS en el elemento raíz especificado.
- `openDrilldownModal(queryId, segmentLabel, materialId = null)` - Abre un modal con detalles adicionales para un segmento específico.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción directa con una base de datos.

### Estado y Variables Globales
- `window.saasChartInstancesV2` - Almacena instancias de gráficos Chart.js renderizados en los widgets.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `fetch` - Para hacer solicitudes HTTP.
  - `Chart.js` - Para crear y gestionar gráficos.
  - `ChartDataLabels` - Plugin para Chart.js que permite mostrar etiquetas de datos en los gráficos.

- **Flujo Interno**:
  - El archivo se ejecuta al cargar el DOM (`DOMContentLoaded`).
  - Llama a `initSaaSWidgetsV2()` con un pequeño retraso para asegurar que el DOM esté listo.
  - `initSaaSWidgetsV2()` busca todos los elementos con la clase `.saas-widget-v2`, recopila parámetros de filtro, realiza solicitudes a una API y renderiza gráficos o KPIs en estos elementos.

El archivo no depende de otros archivos del proyecto directamente.

