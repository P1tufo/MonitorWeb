## Archivo: ./static/js/analytics_studio.js (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `analytics_studio.js` contiene funciones y métodos para gestionar el estado visual de consultas en un sistema de análisis. Permite abrir, editar y publicar consultas, cargar esquemas de base de datos, previsualizar tablas y ejecutar consultas para generar gráficos.

### Catálogo de Funciones y Clases
- `AnalyticsStudioManager.getVisualState(queryId)` - Obtiene el estado visual de una consulta.
- `AnalyticsStudioManager.setVisualState(queryId, state)` - Establece el estado visual de una consulta.
- `openEditQueryModal(queryId, chartTitle)` - Abre un modal para editar una consulta.
- `loadSchema()` - Carga el esquema de la base de datos.
- `previewTable(tableName, el)` - Previsualiza los datos de una tabla.
- `runPreview()` - Ejecuta una previsualización de la consulta actual.
- `renderPreviewChart(payload)` - Renderiza un gráfico basado en los resultados de la consulta.
- `closeEditQueryModal()` - Cierra el modal de edición de consultas.
- `showConfirmPublish()` - Muestra el overlay para confirmar la publicación de una consulta.
- `hideConfirmPublish()` - Oculta el overlay de confirmación de publicación.
- `executePublishQuery()` - Publica una consulta.

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
Dependencias:
- `Chart.js` - Librería para renderizar gráficos.

Flujo:
1. El usuario abre un modal para editar una consulta utilizando `openEditQueryModal`.
2. Se carga el esquema de la base de datos con `loadSchema`.
3. Los datos de la tabla seleccionada se previsualizan con `previewTable`.
4. La consulta actual se ejecuta y los resultados se renderizan con `runPreview` y `renderPreviewChart`.
5. El usuario puede publicar una consulta utilizando `executePublishQuery`.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
Este archivo contiene la lógica para el editor de consultas analíticas, que permite crear y editar consultas SQL interactivamente. Permite seleccionar tablas, columnas, filtros, métricas y configuraciones de gráficos.

### Catálogo de Funciones y Clases
- `initVisualQuery(queryId)` - Inicializa el estado visual del editor de consultas.
- `onBaseTableChange()` - Maneja el cambio en la tabla base seleccionada.
- `getActiveTables()` - Devuelve las tablas activas en el estado actual.
- `getActiveColumns()` - Devuelve las columnas activas disponibles para la consulta.
- `refreshQbColumns(forceState = false)` - Refresca los selectores de columnas (Eje Y, Eje X, Desglose) basándose en el estado actual.
- `renderFilters()` - Renderiza los controles de filtro dinámicamente según el estado del usuario.
- `addFilter()` - Añade un nuevo filtro al estado y lo renderiza.
- `updateFilterType(index, type)` - Actualiza el tipo de valor para un filtro específico.
- `updateFilter(index)` - Actualiza los valores de un filtro específico basándose en la interfaz del usuario.
- `removeFilter(index)` - Elimina un filtro específico del estado y lo actualiza en la interfaz.
- `onSecondMetricToggle()` - Maneja el toggle de la segunda métrica.
- `onQbChange()` - Sincroniza los cambios en la interfaz con el estado interno.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `visualState` - Almacena el estado actual del editor de consultas, incluyendo tablas, columnas, filtros, métricas y configuraciones de gráficos.
- `currentSchema` - Esquema de la base de datos que contiene información sobre las tablas y columnas disponibles.

### Dependencias y Flujo
Dependencias:
- `AnalyticsStudioManager` - Un módulo que gestiona el estado visual del editor de consultas.

