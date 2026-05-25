## Archivo: ./templates/partials/_tab_deliveries.html

### Resumen Funcional
Este fragmento HTML es una pestaña que muestra análisis de entregas, incluyendo KPIs como volumen total y eficiencia de bodega. Permite cambiar entre vistas operativas (anual) y históricas (semanales), y filtra los datos por áreas seleccionadas.

### Catálogo de Funciones y Clases
No se detectaron funciones o clases definidas en este fragmento HTML.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `user.role`: Rol del usuario, utilizado para determinar si se muestran botones de edición.
- `areas_vl`: Lista de áreas disponibles para filtrar.
- `top_authors`: Lista de los top solicitadores con sus entregas.
- `top_materials`: Diccionario con materiales repetitivos por área.

### Dependencias y Flujo
Dependencias:
- `FontAwesome` (usado para iconos)
- JavaScript (`openEditQueryModal`, `toggleMulti`, etc.)

Flujo:
Este fragmento interactúa con el backend a través de funciones JavaScript que pueden abrir modales, cambiar vistas y filtrar datos. No realiza ninguna interacción directa con la base de datos.

