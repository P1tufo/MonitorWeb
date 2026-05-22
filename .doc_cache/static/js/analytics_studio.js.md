## Archivo: ./static/js/analytics_studio.js (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `analytics_studio.js` contiene funciones y variables para gestionar el estado del Studio de Análíticas, incluyendo la carga de esquemas de base de datos, visualización de consultas SQL, generación de gráficos y tarjetas métricas KPI.

### Catálogo de Funciones y Clases
- `openEditQueryModal(queryId, chartTitle)` - Abre el modal para editar una consulta.
- `loadSchema()` - Carga el esquema de la base de datos.
- `previewTable(tableName, el)` - Muestra una vista previa de los datos de una tabla.
- `runPreview()` - Ejecuta una consulta SQL y muestra su resultado en un gráfico o tabla.
- `renderPreviewChart(data)` - Renderiza el gráfico o tabla basado en los datos de la consulta.
- `closeEditQueryModal()` - Cierra el modal para editar una consulta.
- `showConfirmPublish()` - Muestra la ventana de confirmación para publicar.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `studioChartInstance` - Instancia del gráfico actual.
- `currentSchema` - Esquema de la base de datos actual.
- `currentQueryId` - ID de la consulta actualmente seleccionada.
- `studioBoundParams` - Parámetros de la consulta actual.
- `serverVisualState` - Estado visual del servidor.
- `visualState` - Estado del constructor visual.
- `defaultVisualStates` - Mapeos predefinidos para inicialización visual intuitiva.

### Dependencias y Flujo
Dependencias:
- `Chart.js` - Librería para renderizar gráficos.

Flujo:
- El archivo interactúa con el backend a través de endpoints como `/api/queries/{queryId}`, `/api/studio/schema`, y `/api/studio/preview`.
- Utiliza funciones asíncronas (`async/await`) para cargar datos y ejecutar consultas.
- Renderiza gráficos utilizando la librería `Chart.js`.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
Este archivo contiene funciones y métodos para gestionar la edición de consultas, publicación de consultas, y construcción de consultas SQL dinámicamente en un entorno de análisis. Permite crear, modificar y ejecutar consultas SQL basadas en una interfaz gráfica de usuario (GUI) interactiva.

### Catálogo de Funciones y Clases
- `closeEditQueryModal()` - Cierra el modal de edición de consulta.
- `showConfirmPublish()` - Muestra la ventana de confirmación para publicar una consulta.
- `hideConfirmPublish()` - Oculta la ventana de confirmación para publicar una consulta.
- `executePublishQuery()` - Ejecuta la publicación de una consulta a través de una API y actualiza la interfaz según el resultado.
- `initVisualQuery(queryId)` - Inicializa la interfaz visual del editor de consultas con los parámetros proporcionados.
- `onBaseTableChange()` - Maneja el cambio en la tabla base seleccionada.
- `getActiveTables()` - Devuelve una lista de tablas activas basadas en el estado actual.
- `getActiveColumns()` - Devuelve una lista de columnas activas basadas en las tablas activas.
- `refreshQbColumns(forceState = false)` - Refresca los selectores de columnas para los ejes Y, X y desglose.
- `renderJoins()` - Renderiza la interfaz gráfica para gestionar los joins entre tablas.
- `addJoin()` - Añade un nuevo join a la configuración actual.
- `updateJoin(index)` - Actualiza el estado de un join específico.
- `removeJoin(index)` - Elimina un join específico del estado.
- `renderFilters()` - Renderiza la interfaz gráfica para gestionar los filtros (WHERE).
- `addFilter()` - Añade un nuevo filtro a la configuración actual.
- `updateFilterType(index, type)` - Actualiza el tipo de valor para un filtro específico.
- `updateFilter(index)` - Actualiza el estado de un filtro específico.
- `removeFilter(index)` - Elimina un filtro específico del estado.
- `onSecondMetricToggle()` - Maneja el toggle de la segunda métrica.
- `onQbChange()` - Sincroniza los cambios en la interfaz visual con el estado actual y genera una consulta SQL correspondiente.
- `syncVisualToSQL()` - Envía el estado actual a través de una API para generar y sincronizar la consulta SQL.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `visualState` - Almacena el estado actual del editor visual, incluyendo tablas, joins, filtros, métricas, etc.
- `serverVisualState` - Estado visual proporcionado por el servidor.
- `defaultVisualStates` - Estados visuales predeterminados para diferentes consultas.
- `currentSchema` - Esquema de la base de datos actual.
- `studioBoundParams` - Parámetros vinculados al estudio.

### Dependencias y Flujo
Dependencias:
- `fetch` - Para hacer solicitudes HTTP a la API del servidor.

Flujo:
Este archivo interactúa con el backend a través de llamadas a `/api/settings/query` para publicar consultas y `/api/studio/build_sql` para generar consultas SQL. No depende de ninguna base de datos específica, solo utiliza `fetch` para comunicarse con el backend.

