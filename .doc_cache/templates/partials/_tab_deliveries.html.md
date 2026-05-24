## Archivo: ./templates/partials/_tab_deliveries.html

### Resumen Funcional
Este fragmento HTML muestra una pestaña de análisis de entregas con gráficos y KPIs, permitiendo a los usuarios cambiar entre vistas operativas y históricas. Incluye indicadores como volumen total, eficiencia de bodega, entregadas a tiempo y atrasadas, así como gráficos que muestran la evolución mensual del SLA y el ranking de solicitadores.

### Catálogo de Funciones y Clases
No se detectaron funciones o clases definidas en este fragmento HTML.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `kpi_total`: Volumen total de entregas (Año)
- `kpi_eff`: Eficiencia de bodega (%)
- `kpi_ontime`: Entregadas a tiempo
- `kpi_late`: Entregadas atrasadas
- `areas_vl`: Áreas seleccionadas para el filtrado
- `top_authors`: Top solicitadores
- `top_materials`: Ranking de materiales repetitivos por área

### Dependencias y Flujo
Dependencias:
- Font Awesome (para iconos)
- JavaScript (funciones como `switchVLView`, `openEditQueryModal`, etc.)

Flujo: Este fragmento HTML se comunica con el backend a través de funciones JavaScript que pueden realizar acciones como cambiar la vista, abrir modales para editar consultas SQL y filtrar datos.

