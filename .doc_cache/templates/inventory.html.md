## Archivo: ./templates/inventory.html

### Resumen Funcional
El archivo `inventory.html` es una plantilla HTML para la interfaz de usuario del módulo de inventario, que muestra estadísticas y gráficos relacionados con el análisis del inventario. Incluye información sobre ingresos, consumos, traspasos y otras métricas clave.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo HTML.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `kpi_ingresos`: Total de ingresos.
- `kpi_consumos_prod`: Consumo de producción.
- `kpi_consumos_mant`: Consumo de mantenimiento.
- `rate_reabast`: Tasa de reabastecimiento.
- `kpi_traspasos`: Número de traspasos.
- `rate_devolucion`: Tasa de devoluciones.
- `kpi_devoluciones`: Cantidad de devoluciones.
- `volumen_data`: Datos de volumen.
- `area_stats_json`: Estadísticas por área.
- `trend_labels`: Etiquetas para los gráficos de tendencia.
- `trend_entradas`: Datos de entradas para el gráfico de tendencia.
- `trend_salidas_prod`: Datos de salidas de producción para el gráfico de tendencia.
- `trend_salidas_mant`: Datos de salidas de mantenimiento para el gráfico de tendencia.
- `abc_counts`: Conteo de elementos ABC.
- `abc_mapping`: Mapeo de elementos ABC.
- `dow_distribution`: Distribución semanal de BMRI.
- `ubicaciones_mapping`: Mapeo de ubicaciones.
- `area_material_mapping`: Mapeo de materiales por área.
- `user_material_mapping`: Mapeo de materiales por usuario.
- `dow_material_mapping`: Mapeo de materiales por distribución semanal.
- `pm_material_mapping`: Mapeo de materiales por producción vs mantenimiento.

### Dependencias y Flujo
- **Librerías externas**: 
  - Chart.js
  - Chartjs-plugin-datalabels

- **Archivos CSS**:
  - `https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap`
  - Archivo local: `css/inventory.css`

- **Archivos JS**:
  - `https://cdn.jsdelivr.net/npm/chart.js`
  - `https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0`
  - Archivo local: `js/inventory.js`

