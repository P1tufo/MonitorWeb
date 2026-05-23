## Archivo: ./static/js/analytics_studio.js (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `analytics_studio.js` contiene funciones y variables para gestionar el estado del Studio de Análíticas, incluyendo la carga de esquemas de base de datos, visualización de consultas SQL y generación de gráficos.

### Catálogo de Funciones y Clases
- `openEditQueryModal(queryId, chartTitle)` - Abre un modal para editar una consulta.
- `loadSchema()` - Carga el esquema de la base de datos.
- `previewTable(tableName, el)` - Muestra una vista previa de una tabla en la interfaz.
- `runPreview()` - Ejecuta una consulta SQL y muestra su resultado en un gráfico o tabla.
- `renderPreviewChart(data)` - Renderiza el resultado de una consulta como un gráfico.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `studioChartInstance` - Instancia del gráfico actual.
- `currentSchema` - Esquema de la base de datos actual.
- `currentQueryId` - ID de la consulta actualmente seleccionada.
- `studioBoundParams` - Parámetros de la consulta actual.
- `serverVisualState` - Estado visual guardado en el servidor.
- `visualState` - Estado del constructor visual actual.
- `defaultVisualStates` - Mapeo predefinido para inicializar gráficos.

### Dependencias y Flujo
Dependencias:
- `Chart.js` - Librería para renderizar gráficos.

Flujo:
1. El usuario selecciona una consulta en el Studio de Análíticas.
2. Se abre un modal con la opción de editar la consulta.
3. La consulta se carga y se muestra en un editor de texto.
4. El usuario puede modificar la consulta y ejecutarla para obtener resultados.
5. Los resultados se renderizan como gráficos o tablas según el tipo de consulta.

El archivo interactúa con una API que proporciona los datos necesarios para cargar esquemas, ejecutar consultas y obtener visualizaciones.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `analytics_studio.js` contiene funciones y métodos para gestionar la creación, edición y publicación de consultas analíticas. Permite configurar gráficos, filtros y condiciones de búsqueda, y sincroniza estos cambios con un backend que genera y ejecuta consultas SQL.

### Catálogo de Funciones y Clases
- `closeEditQueryModal()` - Cierra el modal para editar una consulta.
- `showConfirmPublish()` - Muestra la ventana de confirmación para publicar una consulta.
- `hideConfirmPublish()` - Oculta la ventana de confirmación para publicar una consulta.
- `executePublishQuery()` - Ejecuta la publicación de una consulta y maneja la respuesta del backend.
- `initVisualQuery(queryId)` - Inicializa el estado visual de la consulta y carga los datos necesarios.
- `onBaseTableChange()` - Maneja el cambio en la tabla base seleccionada.
- `getActiveTables()` - Devuelve las tablas activas en la consulta.
- `getActiveColumns()` - Devuelve las columnas activas en la consulta.
- `refreshQbColumns(forceState = false)` - Refresca los selectores de columnas para los ejes y desglose.
- `renderJoins()` - Renderiza los controles de join en el formulario.
- `addJoin()` - Añade un nuevo join al estado visual.
- `updateJoin(index)` - Actualiza un join existente en el estado visual.
- `removeJoin(index)` - Elimina un join del estado visual.
- `renderFilters()` - Renderiza los controles de filtro en el formulario.
- `addFilter()` - Añade un nuevo filtro al estado visual.
- `updateFilterType(index, type)` - Actualiza el tipo de valor para un filtro.
- `updateFilter(index)` - Actualiza la configuración de un filtro existente.
- `removeFilter(index)` - Elimina un filtro del estado visual.
- `onSecondMetricToggle()` - Maneja el toggle de la segunda métrica.
- `onQbChange()` - Sincroniza los cambios en el formulario con el estado visual y genera SQL.
- `syncVisualToSQL()` - Envía el estado visual al backend para generar y ejecutar una consulta SQL.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `studioChartInstance` - Instancia del gráfico generado por Chart.js.
- `visualState` - Estado visual actual de la consulta, incluyendo tablas, joins, filtros, métricas, etc.
- `serverVisualState` - Estado visual proporcionado por el servidor.
- `defaultVisualStates` - Estados visuales predeterminados para diferentes consultas.
- `currentSchema` - Esquema de las tablas disponibles en la base de datos.
- `studioBoundParams` - Parámetros vinculados a la consulta SQL generada.

### Dependencias y Flujo
Dependencias:
- `Chart.js` - Usado para generar gráficos.
- `fetch` - Para hacer solicitudes HTTP al backend.

Flujo interno:
1. El usuario interactúa con el formulario de configuración de consultas (tablas, joins, filtros, métricas).
2. Los cambios en el formulario se reflejan en el estado visual (`visualState`).
3. Al cambiar algo en el formulario, se llama a `onQbChange()`, que sincroniza los cambios con el backend y genera SQL.
4. El backend devuelve la consulta SQL generada, que se muestra en un editor de texto.
5. Cuando el usuario publica una consulta, se envía el estado visual al backend para ejecutar la consulta.

Flujo externo:
- La función `executePublishQuery()` se comunica con el backend a través de una solicitud POST a `/api/settings/query` para publicar la consulta.
- La función `syncVisualToSQL()` se comunica con el backend a través de una solicitud POST a `/api/studio/build_sql` para generar y ejecutar la consulta SQL.

