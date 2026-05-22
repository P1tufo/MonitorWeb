## Archivo: ./templates/partials/_sidebar.html

### Resumen Funcional
Este archivo contiene el código HTML para un panel lateral que incluye varios filtros y controles de búsqueda para una interfaz web. Permite filtrar por fecha, área, centro, estado OT (Estado WMS), buscar por número de OT o entrega, incluir un logo específico, y descargar reportes consolidados en formato PDF.

### Catálogo de Funciones y Clases
- `toggleSidebar()` - Cierra el panel lateral.
- `toggleMulti(id)` - Muestra u oculta los checkboxes dentro del multiselect.
- `toggleSelectAll(group, checked)` - Selecciona/deselecciona todos los checkboxes en un grupo.
- `handleSmartCheckbox(checkbox, group, allCheckboxId, table)` - Maneja el cambio de estado de los checkboxes inteligentes.
- `applyCentroFilter(value)` - Aplica el filtro por centro seleccionado.
- `applyFilters()` - Aplica los filtros según las selecciones del usuario.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- JavaScript (funciones como `toggleSidebar`, `toggleMulti`, etc.)
- Jinja2 templating (para iterar sobre variables como `dates` y `areas`)

Flujo: Este archivo se comunica con otros archivos JavaScript para manejar eventos de usuario, actualizar el estado del filtro y generar reportes.

