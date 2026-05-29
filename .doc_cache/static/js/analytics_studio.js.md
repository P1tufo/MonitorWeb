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
- `runPreview()` - Ejecuta una previsualización de la consulta y renderiza el gráfico.
- `renderPreviewChart(payload)` - Renderiza el gráfico basado en los datos de la consulta.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `AnalyticsStudioManager.instances` - Almacena instancias de estado visual por consulta.
- `studioChartInstance` - Instancia del gráfico actual.
- `currentSchema` - Esquema actual de la base de datos.
- `currentQueryId` - ID de la consulta actualmente seleccionada.
- `serverVisualState` - Estado visual de la consulta desde el servidor.
- `visualState` - Puntero al estado activo del modal.

### Dependencias y Flujo
Depende de las siguientes librerías:
- `Chart.js` para renderizar gráficos.

Se comunica con los siguientes archivos del proyecto:
- `/api/queries/{queryId}` - Para cargar el estado visual de una consulta.
- `/api/studio/schema` - Para cargar el esquema de la base de datos.
- `/api/studio/preview_table/{tableName}` - Para previsualizar los datos de una tabla.
- `/api/studio/preview` - Para ejecutar una previsualización de la consulta.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `analytics_studio.js` contiene funciones y métodos para gestionar la interfaz de usuario y el estado del editor de consultas analíticas. Permite crear, editar y publicar consultas SQL interactuando con un backend a través de una API.

### Catálogo de Funciones y Clases
- `closeEditQueryModal()` - Cierra el modal para edición de consultas.
- `showConfirmPublish()` - Muestra la ventana de confirmación para publicar una consulta.
- `hideConfirmPublish()` - Oculta la ventana de confirmación para publicar una consulta.
- `executePublishQuery()` - Ejecuta la publicación de una consulta a través de una API y maneja el estado del botón de confirmación.
- `initVisualQuery(queryId)` - Inicializa el estado visual del editor de consultas con los datos proporcionados o por defecto.
- `onBaseTableChange()` - Maneja el cambio en la tabla base seleccionada.
- `getActiveTables()` - Devuelve las tablas activas basadas en el estado actual.
- `getActiveColumns()` - Devuelve las columnas activas basadas en las tablas activas.
- `refreshQbColumns(forceState = false)` - Refresca los selectores de columnas para los ejes y desglose.
- `renderJoins()` - Renderiza los controles de join en la interfaz de usuario.
- `addJoin()` - Añade un nuevo join al estado visual.
- `updateJoin(index)` - Actualiza el estado del join seleccionado.
- `removeJoin(index)` - Elimina el join seleccionado.
- `renderFilters()` - Renderiza los controles de filtro en la interfaz de usuario.
- `addFilter()` - Añade un nuevo filtro al estado visual.
- `updateFilterType(index, type)` - Actualiza el tipo de valor del filtro seleccionado.
- `updateFilter(index)` - Actualiza el estado del filtro seleccionado.
- `removeFilter(index)` - Elimina el filtro seleccionado.
- `onSecondMetricToggle()` - Maneja el toggle para la segunda métrica.
- `onQbChange()` - Sincroniza los cambios en la interfaz de usuario con el estado visual.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `visualState` - Almacena el estado actual del editor de consultas.
- `serverVisualState` - Almacena el estado visual desde el servidor.
- `defaultVisualStates` - Almacena los estados visuales por defecto para diferentes consultas.
- `currentSchema` - Almacena la estructura de las tablas y columnas disponibles.

### Dependencias y Flujo
Dependencias:
- `fetch` - Para hacer solicitudes HTTP al backend.
- `AnalyticsStudioManager` - Para gestionar el estado visual del editor de consultas.

