## Archivo: ./static/js/saas_engine.js (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `saas_engine.js` es un motor SaaS que se encarga de leer contenedores con la clase `.saas-widget-v2`, renderizar gráficos o KPIs, y manejar interacciones como el drilldown.

### Catálogo de Funciones y Clases
- `initSaaSWidgetsV2(params = null, rootElement = document)` - Inicializa los widgets SaaS en el elemento raíz especificado.
- `openDrilldownModal(queryId, segmentLabel, materialId = null)` - Abre un modal con detalles del drilldown.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `window.saasChartInstancesV2` - Almacena instancias de gráficos Chart.js para widgets individuales.
- `window.openDrilldownModal` - Función global que maneja el drilldown.

### Dependencias y Flujo
- Depende de la librería `Chart.js` para renderizar gráficos.
- Comunica con un servidor a través de peticiones `fetch` a endpoints como `/api/widget/{queryId}` y `/api/widget/{queryId}/drilldown`.
- Utiliza funciones globales como `window.openDrilldownModal`, `window.sortDrilldownTable`, y `window.filterDrilldownTable`.

