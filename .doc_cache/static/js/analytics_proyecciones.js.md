## Archivo: ./static/js/analytics_proyecciones.js

### Resumen Funcional
El archivo `analytics_proyecciones.js` contiene lógica para renderizar y controlar modales de alertas, combinaciones y gráficos de dispersión en una interfaz web. Utiliza funciones para filtrar y mostrar datos basados en criterios de búsqueda y selección.

### Catálogo de Funciones y Clases
- `renderAlerts()` - Renderiza los datos de alertas en un modal.
- `renderCombos(filterText = "")` - Renderiza los datos de combinaciones en un modal, filtrando por texto.
- `renderScatter()` - Renderiza los datos de dispersión en un modal, filtrando por texto y categoría.
- `openModalAlerts()` - Abre el modal de alertas y carga los datos iniciales.
- `openModalCombos()` - Abre el modal de combinaciones y carga los datos iniciales.
- `openModalScatter()` - Abre el modal de dispersión y carga los datos iniciales.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencia: `core_ui.js` (carga previa para proporcionar funciones como `CoreUI.openModal`, `CoreUI.closeModal`, `CoreUI.populateAreaSelect`, y `CoreUI.getData`).

