## Archivo: ./templates/partials/_tab_deliveries.html

### Resumen Funcional
Este fragmento HTML muestra una pestaña de análisis de entregas con gráficos y KPIs, permitiendo a los usuarios cambiar entre vistas operativas y históricas. Incluye estadísticas como volumen total, eficiencia de bodega, entregadas a tiempo y atrasadas, así como gráficos interactivos para visualizar la evolución mensual y semanal del cumplimiento SLA.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML. Todas las interacciones son realizadas mediante JavaScript y eventos del DOM.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `kpi_total`: Volumen total de entregas (Año).
- `kpi_eff`: Eficiencia de bodega (%).
- `kpi_ontime`: Entregadas a tiempo.
- `kpi_late`: Entregadas atrasadas.
- `areas_vl`: Lista de áreas seleccionadas para el filtrado.
- `top_authors`: Top solicitadores con sus entregas y áreas.
- `top_materials`: Ranking de materiales repetitivos por área.

### Dependencias y Flujo
Dependencias:
- Font Awesome (para íconos).
- JavaScript (para interactividad).

Flujo:
Este fragmento interactúa con el backend a través de funciones JavaScript que pueden abrir modales para editar consultas SQL, cambiar vistas, filtrar datos, y actualizar gráficos. No realiza llamadas directas a una base de datos ni depende de variables globales definidas en otros archivos del proyecto.

