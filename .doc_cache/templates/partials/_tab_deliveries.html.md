## Archivo: ./templates/partials/_tab_deliveries.html

### Resumen Funcional
Este fragmento HTML es una pestaña que muestra un análisis de entregas, incluyendo KPIs como volumen total y eficiencia de bodega. Permite cambiar la vista entre "Vista Anual" y "Vista Semanal", y filtra los datos por áreas seleccionadas.

### Catálogo de Funciones y Clases
- `switchVLView(value)` - Cambia la vista según el valor seleccionado en el selector.
- `openEditQueryModal(queryId, title)` - Abre un modal para editar una consulta SQL específica.
- `toggleMulti(id)` - Muestra u oculta los checkboxes de áreas.
- `toggleChartSelectAll(checked)` - Selecciona/deselecciona todos los checkboxes de áreas.
- `handleSmartCheckbox(element)` - Maneja el cambio en los checkboxes individuales.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `user.role` - Rol del usuario, utilizado para determinar si se muestran botones de edición.
- `areas_vl` - Lista de áreas disponibles para filtrar.

### Dependencias y Flujo
Dependencias:
- Font Awesome (para iconos)
- JavaScript (funciones definidas en el archivo)

Flujo:
Este fragmento interactúa con otros archivos a través de llamadas a funciones JavaScript (`switchVLView`, `openEditQueryModal`, etc.) que probablemente estén definidas en un archivo `.js` asociado.

