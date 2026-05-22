## Archivo: ./static/js/inventory.js

### Resumen Funcional
El archivo `inventory.js` contiene lógica para el análisis de movimientos en un inventario, con funcionalidades como la visualización de gráficos y modales interactivos. Incluye manejo de datos desde elementos HTML, renderizado de gráficos usando Chart.js, y funciones para abrir y cerrar modales.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra mensajes en la consola con un formato específico.
- `UI.openModal(id)` - Abre un modal identificado por `id`.
- `UI.closeModal(id)` - Cierra un modal identificado por `id`.
- `UI.renderMaterialModal(options)` - Renderiza un modal con detalles de materiales, incluyendo una lista de elementos y estadísticas.
- `getData(id)` - Obtiene datos desde un elemento HTML con el ID especificado.
- `parseFormattedInt(val)` - Convierte una cadena formateada en un número entero.
- `window.openModalUbicacion(name)` - Abre un modal con la ubicación de un material específico.
- `window.openModalUserInv(name)` - Abre un modal con los detalles del inventario de un usuario específico.
- `window.switchInventarioView(view)` - Cambia la vista del gráfico de tendencias entre históricos y actuales.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales en este archivo.

### Dependencias y Flujo
- **Librerías Externas**: `Chart.js`, `ChartDataLabels`.
- **Flujo Interno**: El archivo interactúa con elementos HTML para obtener datos, renderizar modales y actualizar gráficos de Chart.js. No hay interacción directa con otros archivos del proyecto a menos que se invoquen las funciones globales definidas (`window.openModalUbicacion`, `window.openModalUserInv`, `window.switchInventarioView`).

