## Archivo: ./static/js/analytics_studio.js (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `analytics_studio.js` contiene funciones y clases para gestionar el estado visual de consultas en un sistema de análisis. Permite abrir modales, cargar esquemas de base de datos, previsualizar tablas y ejecutar consultas para generar gráficos.

### Catálogo de Funciones y Clases
- `AnalyticsStudioManager.getVisualState(queryId)` - Obtiene el estado visual de una consulta.
- `AnalyticsStudioManager.setVisualState(queryId, state)` - Establece el estado visual de una consulta.
- `openEditQueryModal(queryId, chartTitle)` - Abre un modal para editar una consulta.
- `loadSchema()` - Carga el esquema de la base de datos.
- `previewTable(tableName, el)` - Previsualiza los datos de una tabla.
- `runPreview()` - Ejecuta una previsualización de la consulta actual.
- `renderPreviewChart(data)` - Renderiza un gráfico basado en los datos de la previsualización.
- `closeEditQueryModal()` - Cierra el modal para editar una consulta.
- `showConfirmPublish()` - Muestra una overlay para confirmar la publicación.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `AnalyticsStudioManager.instances` - Almacena los estados visuales de las consultas.
- `studioChartInstance` - Instancia del gráfico actual.
- `currentSchema` - Esquema actual de la base de datos.
- `currentQueryId` - ID de la consulta actualmente seleccionada.
- `serverVisualState` - Estado visual de la consulta desde el servidor.
- `visualState` - Puntero al estado activo del modal.

### Dependencias y Flujo
Depende de las siguientes librerías externas:
- `Chart.js` para renderizar gráficos.

Se comunica con los siguientes archivos del proyecto:
- `/api/queries/{queryId}` - Para cargar el estado visual de una consulta.
- `/api/studio/schema` - Para cargar el esquema de la base de datos.
- `/api/studio/preview_table/{tableName}` - Para previsualizar los datos de una tabla.
- `/api/studio/preview` - Para ejecutar una previsualización de la consulta actual.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `analytics_studio.js` contiene funciones y lógica para gestionar la edición, publicación y configuración de consultas analíticas en un estudio de datos. Permite crear, modificar y ejecutar consultas SQL interactuando con una interfaz gráfica basada en JavaScript.

### Catálogo de Funciones y Clases
- `closeEditQueryModal()` - Cierra el modal de edición de consulta.
- `showConfirmPublish()` - Muestra la ventana de confirmación para publicar una consulta.
- `hideConfirmPublish()` - Oculta la ventana de confirmación para publicar una consulta.
- `executePublishQuery()` - Ejecuta la publicación de una consulta y maneja la respuesta del servidor.
- `initVisualQuery(queryId)` - Inicializa el estado visual de la consulta.
- `onBaseTableChange()` - Maneja el cambio en la tabla base seleccionada.
- `getActiveTables()` - Obtiene las tablas activas en la consulta.
- `getActiveColumns()` - Obtiene las columnas activas en la consulta.
- `refreshQbColumns(forceState)` - Refresca los selectores de columnas para el eje Y, X y desglose.
- `renderJoins()` - Renderiza los joins en la interfaz gráfica.
- `addJoin()` - Añade un nuevo join a la consulta.
- `updateJoin(index)` - Actualiza un join existente.
- `removeJoin(index)` - Elimina un join de la consulta.
- `renderFilters()` - Renderiza los filtros en la interfaz gráfica.
- `addFilter()` - Añade un nuevo filtro a la consulta.
- `updateFilterType(index, type)` - Actualiza el tipo de valor para un filtro.
- `updateFilter(index)` - Actualiza los detalles de un filtro existente.
- `removeFilter(index)` - Elimina un filtro de la consulta.
- `onSecondMetricToggle()` - Maneja el toggle de la segunda métrica.
- `onQbChange()` - Sincroniza los cambios en la interfaz gráfica con el estado visual.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `visualState` - Almacena el estado actual de la consulta visual.
- `serverVisualState` - Almacena el estado visual del servidor.
- `defaultVisualStates` - Almacena los estados visuales por defecto para diferentes consultas.
- `currentSchema` - Almacena el esquema de la base de datos actual.

### Dependencias y Flujo
Dependencias:
- `fetch` - Para hacer solicitudes HTTP al servidor.
- `AnalyticsStudioManager` - Para gestionar el estado visual del estudio de datos.

