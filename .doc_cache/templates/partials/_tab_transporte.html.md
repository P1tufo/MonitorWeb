## Archivo: ./templates/partials/_tab_transporte.html

### Resumen Funcional
Este fragmento HTML es una interfaz de usuario para mostrar la evolución de entregas, permitiendo filtrar por mensual o semanal. Incluye un gráfico de líneas, un buscador rápido y una tabla con datos históricos y PDFs.

### Catálogo de Funciones y Clases
- `updateTransporteChartGroup(filter)` - Actualiza el gráfico de líneas según el filtro seleccionado (mensual o semanal).
- `searchTransporte()` - Realiza la búsqueda en la tabla de entregas.
- `closePdfViewer()` - Cierra el modal del visor PDF.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- JavaScript (funciones mencionadas)
- CSS para estilos

Flujo: Este fragmento interactúa con el backend a través de funciones JavaScript que se disparan en eventos del usuario, como cambios en los filtros o la entrada de texto en el buscador.

