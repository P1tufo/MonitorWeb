## Archivo: ./static/js/inventory.js

### Resumen Funcional
El archivo `inventory.js` contiene lógica para el análisis de inventario, incluyendo la visualización de gráficos y la interacción con modales. Se utilizan Chart.js para crear gráficos de doughnut y lineas, y se manejan eventos de entrada para buscar ubicaciones dinámicamente.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra mensajes en la consola.
- `UI.openModal(id)` - Abre un modal utilizando CoreUI.
- `UI.closeModal(id)` - Cierra un modal utilizando CoreUI.
- `UI.renderMaterialModal(opts)` - Renderiza un modal de material utilizando CoreUI.
- `getData(id)` - Obtiene datos desde el DOM utilizando CoreUI.
- `parseFormattedInt(val)` - Convierte una cadena a un número entero, eliminando caracteres no numéricos.
- `window.openModalUbicacion(name)` - Abre un modal con información de ubicación.
- `window.openModalUserInv(name)` - Abre un modal con información de usuario.
- `window.switchInventarioView(view)` - Cambia la vista del gráfico de tendencias según el parámetro `view`.
- `window.toggleMultiInv(id)` - Alterna la visibilidad de un elemento según su ID.
- `window.toggleAllInvAreas(checkbox)` - Alterna la selección de todas las áreas y actualiza los KPIs.
- `window.updateInventoryAnalytics()` - Actualiza los KPIs y filtra listas según las áreas seleccionadas.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: Chart.js, CoreUI.
- **Flujo Interno**: El archivo interactúa con el DOM para obtener datos y renderizar gráficos. Utiliza funciones de CoreUI para abrir y cerrar modales.

