## Archivo: ./static/js/analytics_studio.js (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `analytics_studio.js` contiene funciones y variables para gestionar la visualización de gráficos en un entorno de análisis. Permite abrir modales, cargar esquemas de base de datos, previsualizar tablas y ejecutar consultas para generar gráficos.

### Catálogo de Funciones y Clases
- `openEditQueryModal(queryId, chartTitle)` - Abre un modal para editar una consulta.
- `loadSchema()` - Carga el esquema de la base de datos.
- `previewTable(tableName, el)` - Previsualiza los datos de una tabla.
- `runPreview()` - Ejecuta una previsualización de la consulta y renderiza el gráfico.
- `renderPreviewChart(data)` - Renderiza el gráfico basado en los datos obtenidos.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `studioChartInstance` - Instancia del gráfico actual.
- `currentSchema` - Esquema actual de la base de datos.
- `currentQueryId` - ID de la consulta actual.
- `studioBoundParams` - Parámetros vinculados al estudio.
- `serverVisualState` - Estado visual del servidor.
- `legacySqlText` - Texto SQL heredado.
- `visualState` - Estado del constructor visual.
- `defaultVisualStates` - Mapeos predefinidos para inicialización visual intuitiva de gráficos.

### Dependencias y Flujo
Depende de la librería Chart.js para renderizar los gráficos. Comunica con el servidor a través de endpoints como `/api/queries/{queryId}`, `/api/studio/schema`, y `/api/studio/preview`.

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
- `refreshQbColumns(forceState = false)` - Refresca los selectores de columnas para los ejes y desglose según el estado actual.
- `renderJoins()` - Renderiza los controles de join en la interfaz de usuario.
- `addJoin()` - Añade un nuevo join al estado visual.
- `updateJoin(index)` - Actualiza un join existente en el estado visual.
- `removeJoin(index)` - Elimina un join del estado visual.
- `renderFilters()` - Renderiza los controles de filtro en la interfaz de usuario.
- `addFilter()` - Añade un nuevo filtro al estado visual.
- `updateFilterType(index, type)` - Actualiza el tipo de valor para un filtro específico.
- `updateFilter(index)` - Actualiza los detalles de un filtro específico.
- `removeFilter(index)` - Elimina un filtro del estado visual.
- `onSecondMetricToggle()` - Maneja el toggle de la segunda métrica.
- `onQbChange()` - Sincroniza los cambios en la interfaz de usuario con el estado visual.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `visualState` - Almacena el estado actual del editor de consultas, incluyendo tablas, joins, filtros, métricas, etc.
- `serverVisualState` - Estado visual proporcionado por el servidor.
- `defaultVisualStates` - Estados visuales predeterminados para diferentes consultas.
- `currentSchema` - Esquema actual de la base de datos.

### Dependencias y Flujo
Dependencias:
- `fetch` - Para hacer solicitudes HTTP al backend.
- `document.getElementById`, `querySelector`, etc. - Para interactuar con el DOM.

Flujo:
Este archivo se comunica con el backend a través de una API para publicar consultas. No realiza interacciones directas con bases de datos ni utiliza ORM.

