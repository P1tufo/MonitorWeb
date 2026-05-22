## Archivo: ./static/js/analytics_proyecciones.js

### Resumen Funcional
El archivo `analytics_proyecciones.js` contiene lógica para manejar la interacción con una interfaz de usuario (UI) y renderizar datos en diferentes modales. Los datos se filtran y presentan según los criterios ingresados por el usuario.

### Catálogo de Funciones y Clases
- `UI.openModal(id)` - Abre un modal identificado por `id`.
- `UI.closeModal(id)` - Cierra un modal identificado por `id`.
- `UI.populateAreaSelect(selectId, data, key = 'area')` - Llena un selector de áreas con valores únicos del conjunto de datos proporcionado.
- `getData(id)` - Obtiene y parsea los datos almacenados en un elemento HTML con el ID especificado.
- `renderAlerts()` - Renderiza una tabla de alertas basada en los criterios de búsqueda y filtro.
- `renderCombos(filterText = "")` - Renderiza una lista de combinaciones de materiales basadas en la búsqueda del usuario.
- `renderScatter()` - Renderiza un gráfico de dispersión basado en los criterios de búsqueda y filtro.
- `openModalAlerts()` - Abre el modal de alertas, llena el selector de áreas y renderiza las alertas.
- `openModalCombos()` - Abre el modal de combinaciones, limpia la entrada de búsqueda y renderiza las combinaciones.
- `openModalScatter()` - Abre el modal de dispersión, llena los selectores de área y categoría, limpia las entradas de búsqueda y renderiza el gráfico.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: `Chart.js` (usado para crear el gráfico de dispersión).
- **Flujo Interno**: El archivo interactúa con elementos HTML para obtener datos, renderizar contenido en modales y actualizar gráficos.

