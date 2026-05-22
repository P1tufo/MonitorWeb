## Archivo: ./templates/partials/_table.html

### Resumen Funcional
Este fragmento HTML define una tabla para mostrar transacciones, con columnas para entrega/OT, fecha, items, área y estado. Incluye funcionalidades de ordenación y búsqueda.

### Catálogo de Funciones y Clases
- `sortTable(column)` - Ordena la tabla según la columna especificada.
- `filterTable()` - Filtra las filas de la tabla según los valores de entrada en los campos de búsqueda.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- JavaScript (`sortTable`, `filterTable`)
- CSS (estilos para la tabla y elementos)

Flujo: Este fragmento se comunica con el backend a través de formularios que envían solicitudes POST al endpoint `/generate-pdf` para generar y previsualizar/descargar PDFs.

