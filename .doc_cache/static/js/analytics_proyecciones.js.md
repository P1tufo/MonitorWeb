## Archivo: ./static/js/analytics_proyecciones.js

### Resumen Funcional
El archivo `analytics_proyecciones.js` contiene la lógica para renderizar y controlar los modales de alertas, combinaciones y gráficos de dispersión en una interfaz web. Utiliza funciones para filtrar y mostrar datos basados en criterios de búsqueda y selección.

### Catálogo de Funciones y Clases
- `renderAlerts()` - Renderiza la tabla de alertas.
- `renderCombos(filterText = "")` - Renderiza los combos de materiales.
- `renderScatter()` - Renderiza el gráfico de dispersión.
- `openModalAlerts()` - Abre el modal de alertas y carga los datos.
- `openModalCombos()` - Abre el modal de combinaciones y carga los datos.
- `openModalScatter()` - Abre el modal de gráficos de dispersión y carga los datos.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas a una base de datos.

### Estado y Variables Globales
No hay variables globales explícitas definidas en este archivo. Las variables utilizadas son principalmente para almacenar referencias a elementos del DOM y datos obtenidos mediante `getData`.

### Dependencias y Flujo
- **Dependencias**: El archivo depende de `core_ui.js` que proporciona funciones como `CoreUI.openModal`, `CoreUI.closeModal`, `CoreUI.populateAreaSelect` y `CoreUI.getData`.
- **Flujo de Datos**: 
  - Los datos se obtienen mediante `getData('data_alerts')`, `getData('data_combos')`, y `getData('data_scatter')`.
  - Los datos son filtrados y renderizados en los modales correspondientes.
  - El gráfico de dispersión se inicializa con datos obtenidos de `getData('data_scatter')`.

Este archivo es parte del frontend de un sistema WMS, donde la lógica de interfaz interactúa con el backend a través de funciones que obtienen y manipulan datos para su visualización en los modales y gráficos.

