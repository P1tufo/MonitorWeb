## Archivo: ./templates/inventory.html

### Resumen Funcional
El archivo `inventory.html` es una plantilla HTML para la interfaz de usuario del módulo de inventario, que muestra análisis y gráficos relacionados con las entradas, consumos y traspasos de materiales.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo. Todo el contenido es estructura HTML y JavaScript.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `user.username`: Nombre del usuario actual.
- `kpi_ingresos`: Total de ingresos.
- `kpi_consumos_prod`: Consumo de producción.
- `kpi_consumos_mant`: Consumo de mantenimiento.
- `rate_reabast`: Tasa de reabastecimiento.
- `kpi_traspasos`: Número de traspasos.
- `rate_devolucion`: Tasa de devoluciones.
- `kpi_devoluciones`: Cantidad de devoluciones.
- `volumen_data`: Datos de volumen.
- `area_stats_json`: Estadísticas por área.
- `trend_labels`: Etiquetas para gráficos de tendencia.
- `trend_entradas`: Datos de entradas para gráficos de tendencia.
- `trend_salidas_prod`: Datos de salidas de producción para gráficos de tendencia.
- `trend_salidas_mant`: Datos de salidas de mantenimiento para gráficos de tendencia.
- `abc_counts`: Conteo de elementos ABC.
- `abc_mapping`: Mapeo de elementos ABC.
- `kpi_consumos_prod`: Consumo de producción (repetido).
- `kpi_consumos_mant`: Consumo de mantenimiento (repetido).
- `dow_distribution`: Distribución diaria.
- `ubicaciones_mapping`: Mapeo de ubicaciones.
- `area_material_mapping`: Mapeo de materiales por área.
- `user_material_mapping`: Mapeo de materiales por usuario.
- `dow_material_mapping`: Mapeo de materiales por distribución diaria.
- `pm_material_mapping`: Mapeo de materiales para producción vs mantenimiento.

### Dependencias y Flujo
- **Librerías externas**: 
  - Chart.js
  - Chartjs-plugin-datalabels

- **Archivos JavaScript**:
  - `core_ui.js`
  - `inventory.js`

- **Modales y parciales HTML incluidos**:
  - `_styles.html`
  - `_inventory_modals.html`
  - `_quick_login_modal.html`
  - `_logout.html`

