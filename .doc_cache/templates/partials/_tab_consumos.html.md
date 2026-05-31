## Archivo: ./templates/partials/_tab_consumos.html

### Resumen Funcional
Este fragmento HTML define una pestaña para el análisis de consumos y costos, que incluye dos paneles: uno para buscar por Centro de Costo (CeCo) y otro para buscar inversamente por materiales. Cada panel contiene tablas interactivas y un modal para mostrar tendencias mensuales.

### Catálogo de Funciones y Clases
- `buscarPorCeCo()` - Llama a la función que realiza el análisis de consumos por CeCo.
- `limpiarGrilla()` - Limpia las celdas de entrada en el panel de búsqueda inversa por materiales.
- `buscarPorMateriales()` - Realiza el análisis de los materiales ingresados.
- `filterTable(tableId)` - Filtra las tablas según el texto ingresado en los campos de búsqueda.
- `cerrarTendenciaMaterial()` - Cierra el modal de tendencias mensuales.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Depende de las siguientes funciones y variables globales definidas en otros archivos del proyecto:
- `filterTable(tableId)` - Función para filtrar tablas.
- `cerrarTendenciaMaterial()` - Función para cerrar el modal de tendencias mensuales.

