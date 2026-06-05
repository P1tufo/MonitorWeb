## Archivo: ./static/js/tasks.js

### Resumen Funcional
El archivo `tasks.js` contiene la lógica para inicializar y configurar gráficos de tendencias y usuarios en una interfaz web utilizando la biblioteca Chart.js. Los datos necesarios se obtienen del DOM y se utilizan para crear gráficos de líneas y barras con opciones personalizadas.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra mensajes en la consola.
- `getData(id)` - Obtiene datos JSON desde elementos del DOM.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: 
  - `Chart.js` (incluye `ChartDataLabels`)
  
- **Flujo**:
  - El archivo se ejecuta cuando el DOM esté completamente cargado (`DOMContentLoaded`).
  - Llama a `getData()` para obtener datos de los elementos del DOM.
  - Utiliza estos datos para crear gráficos con Chart.js.

### Notas Adicionales
- El código utiliza la biblioteca Chart.js para crear gráficos interactivos en el navegador.
- Los gráficos se inicializan con opciones personalizadas, incluyendo colores, fuentes y estilos específicos.

