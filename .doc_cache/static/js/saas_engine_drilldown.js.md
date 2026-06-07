## Archivo: ./static/js/saas_engine_drilldown.js

### Resumen Funcional
El archivo `saas_engine_drilldown.js` contiene funciones para abrir modales de detalles y cargar tablas dinámicas con datos desde una API. Los modales incluyen detalles de materiales, áreas de negocio y estadísticas relacionadas.

### Catálogo de Funciones y Clases
- `window.openDrilldownModal(queryId, segmentLabel, materialId = null)` - Abre el modal de detalles para un área o material específico.
- `window.sortDrilldownTable(n)` - Ordena la tabla de detalles por una columna específica.
- `window.filterDrilldownTable()` - Filtra los datos de la tabla según los valores ingresados en los campos de búsqueda.
- `window.openCmv201Modal()` - Abre el modal para mostrar resúmenes de CMV 201.
- `window.loadCmv201Data(planType)` - Carga los datos del resumen de CMV 201 según el tipo de planificación seleccionado.
- `window.openCmv201AreaDetails(area)` - Abre el modal para mostrar detalles específicos de una área en CMV 201.
- `window.backToCmv201Summary()` - Vuelve al resumen general de CMV 201.
- `window.onCmv201MonthChange()` - Maneja el cambio de mes seleccionado en los modales de CMV 201 y CMV 261.
- `window.loadCmv201AreaDetails()` - Carga los detalles específicos de una área en CMV 201 según el mes seleccionado.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos. Los datos se cargan a través de llamadas a la API FastAPI.

### Estado y Variables Globales
- `window.currentCmv201PlanType` - Almacena el tipo de planificación seleccionado para CMV 201.
- `window.currentCmv201Area` - Almacena el área de negocio seleccionada en los modales de CMV 201 y CMV 261.
- `window.cmv201MonthsAvailable` - Almacena los meses disponibles para la visualización en los modales de CMV 201 y CMV 261.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas específicas.
- **Flujo de Datos**:
  - `saas_engine_drilldown.js` importa y es importado por otros archivos JavaScript dentro del proyecto, pero no hay intercambio explícito de datos entre ellos.

