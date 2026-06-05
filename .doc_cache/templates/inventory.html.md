## Archivo: ./templates/inventory.html

### Resumen Funcional
El archivo `inventory.html` es una plantilla HTML para la página de análisis del inventario en el sistema de monitoreo de almacén (WMS). Muestra gráficos y KPIs relacionados con las entradas, consumos, traspasos y otras métricas del inventario.

### Catálogo de Funciones y Clases
Ninguna.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `Chart.js`
  - `chartjs-plugin-datalabels`

- **Archivos del Proyecto Importados**:
  - `partials/_styles.html`
  - `css/inventory.css`
  - `partials/_inventory_modals.html`
  - `js/core_ui.js`
  - `js/saas_engine_core.js`
  - `js/saas_engine_drilldown.js`
  - `js/inventory.js`
  - `partials/_quick_login_modal.html`
  - `partials/_logout.html`

- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno.

El flujo de datos se realiza principalmente a través de la carga de scripts y estilos, así como el consumo de variables globales y funciones JavaScript definidas en los archivos importados.

