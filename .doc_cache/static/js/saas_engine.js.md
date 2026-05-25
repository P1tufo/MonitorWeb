## Archivo: ./static/js/saas_engine.js

### Resumen Funcional
El archivo `saas_engine.js` es un motor SaaS V2 que se encarga de renderizar gráficos y KPIs en elementos HTML con la clase `.saas-widget-v2`. Utiliza una API para obtener los datos necesarios y actualiza el contenido del widget según estos datos.

### Catálogo de Funciones y Clases
- `initSaaSWidgetsV2(params = null)` - Inicializa los widgets SaaS V2, leyendo parámetros desde la interfaz o URL, y renderizando gráficos o KPIs en los elementos correspondientes.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
- `window.saasChartInstancesV2` - Almacena instancias de gráficos Chart.js para widgets que ya han sido renderizados.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `fetch` - Para hacer solicitudes HTTP.
  - `Chart.js` - Para renderizar gráficos.
  - `ChartDataLabels` - Plugin de Chart.js para etiquetar datos en gráficos.
  
- **Flujo Interno**:
  - El archivo se ejecuta al cargar el DOM (`DOMContentLoaded`).
  - Intercepta la función `updateDeliveriesAnalytics` si existe, y reemplaza su contenido con una versión que también llama a `initSaaSWidgetsV2`.
  - Llama a `initSaaSWidgetsV2` después de un pequeño delay para asegurar que el DOM esté listo.

El archivo interactúa con elementos HTML mediante la selección de clases y atributos, y utiliza funciones asíncronas para obtener datos desde una API y actualizar el contenido de los widgets.

