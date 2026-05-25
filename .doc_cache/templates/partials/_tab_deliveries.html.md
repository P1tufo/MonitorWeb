## Archivo: ./templates/partials/_tab_deliveries.html

### Resumen Funcional
Este fragmento HTML es una pestaña que muestra un análisis de entregas, incluyendo KPIs como volumen total y eficiencia de bodega. Permite cambiar entre vistas operativas (anual) y históricas (semanales), y filtra los datos por áreas seleccionadas.

### Catálogo de Funciones y Clases
- `switchVLView(value)` - Cambia la vista según el valor seleccionado en el selector.
- `openEditQueryModal(queryId, title)` - Abre un modal para editar una consulta SQL específica.
- `toggleMulti(id)` - Muestra u oculta los checkboxes de áreas.
- `toggleChartSelectAll(checked)` - Selecciona/deselecciona todos los checkboxes de áreas.
- `handleSmartCheckbox(element)` - Maneja el cambio en los checkboxes individuales.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- jQuery (para eventos como `onchange`, `onclick`, etc.)
- Font Awesome (para iconos)

Flujo: Este fragmento interactúa con el backend a través de JavaScript para cargar datos dinámicamente en los KPIs y gráficos. No realiza consultas directas a la base de datos, sino que espera que estos datos se le pasen desde el backend.

