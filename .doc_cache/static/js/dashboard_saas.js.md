## Archivo: ./static/js/dashboard_saas.js

### Resumen Funcional
El archivo `dashboard_saas.js` es un componente del sistema de monitoreo de almacén (WMS) que inicializa y gestiona widgets interactivos en la interfaz de usuario. Estos widgets pueden mostrar gráficos y tablas dinámicas basadas en datos obtenidos a través de una API.

### Catálogo de Funciones y Clases
- `initSaaSWidgets(params = null)` - Inicializa los widgets SaaS, leyendo parámetros del DOM o proporcionados explícitamente.
- `renderSaaSChart(container, queryId, data)` - Renderiza un gráfico de líneas para el widget SaaS.
- `renderSaaSTrellis(container, queryId, data)` - Renderiza una trellis de gráficos para el widget SaaS.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos. Todas las operaciones de obtención de datos se realizan a través de una API (`DashboardAPI`).

### Estado y Variables Globales
- `window.saasChartInstances` - Almacena instancias de gráficos Chart.js renderizados.

### Dependencias y Flujo
- **Dependencias**: 
  - `ChartDataLabels` (plugin para Chart.js).
  - `DashboardAPI` (API personalizada para obtener datos del servidor).

- **Flujo**:
  - El archivo se carga en el DOM.
  - Al cargar, inicializa los widgets SaaS llamando a `initSaaSWidgets()`.
  - `initSaaSWidgets()` lee parámetros de filtros y solicita datos a través de la API.
  - Los datos recibidos se utilizan para renderizar gráficos o tablas en el DOM.

El flujo es unidireccional, con el archivo consumiendo datos de la API y generando contenido visual en el navegador.

