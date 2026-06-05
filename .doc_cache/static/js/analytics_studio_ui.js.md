## Archivo: ./static/js/analytics_studio_ui.js (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `analytics_studio_ui.js` contiene funciones y métodos para gestionar la interfaz de usuario del Studio de Análíticas, permitiendo la edición, visualización y publicación de consultas. Incluye lógica para cargar esquemas de base de datos, previsualizar tablas, ejecutar consultas y manejar filtros y configuraciones visuales.

### Catálogo de Funciones y Clases
- `openEditQueryModal(queryId, chartTitle)` - Abre el modal para editar una consulta.
- `loadSchema()` - Carga el esquema de la base de datos.
- `previewTable(tableName, el)` - Previsualiza los datos de una tabla.
- `runPreview()` - Ejecuta una previsualización de la consulta actual.
- `closeEditQueryModal()` - Cierra el modal para editar una consulta.
- `showConfirmPublish()` - Muestra el overlay de confirmación para publicar una consulta.
- `hideConfirmPublish()` - Oculta el overlay de confirmación para publicar una consulta.
- `executePublishQuery()` - Publica la consulta actual.
- `initVisualQuery(queryId)` - Inicializa el Constructor Visual con los datos de la consulta.
- `onBaseTableChange()` - Maneja el cambio en la tabla base seleccionada.
- `getActiveTables()` - Devuelve las tablas activas.
- `getActiveColumns()` - Devuelve las columnas activas.
- `refreshQbColumns(forceState = false)` - Refresca los selectores de columnas para el Constructor Visual.
- `renderFilters()` - Renderiza los filtros en la interfaz de usuario.
- `addFilter()` - Añade un nuevo filtro.
- `updateFilterType(index, type)` - Actualiza el tipo de valor del filtro.
- `updateFilter(index)` - Actualiza los detalles del filtro seleccionado.
- `removeFilter(index)` - Elimina un filtro.
- `onSecondMetricToggle()` - Maneja el toggle de la Segunda Métrica.
- `onQbChange()` - Sincroniza los cambios en la configuración del Constructor Visual con el estado actual.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - No se especifican tablas explícitas, pero se hacen solicitudes a endpoints como `/api/queries/{queryId}`, `/api/studio/schema`, y `/api/studio/preview_table/{tableName}`.
- Columnas:
  - No se especifican columnas explícitas, pero las solicitudes implican operaciones en tablas de consultas y esquemas.

### Estado y Variables Globales
- `currentQueryId` - ID de la consulta actualmente seleccionada.
- `serverVisualState` - Estado visual del servidor para la consulta actual.
- `visualState` - Estado visual actual del Constructor Visual.
- `currentSchema` - Esquema actual de la base de datos.

### Dependencias y Flujo
- **Dependencias Externas**: No se mencionan dependencias externas específicas.
- **Archivos Importados**:
  - Ninguno especificado en el fragmento proporcionado.
- **Archivos Exportados**:
  - Ninguno especificado en el fragmento proporcionado.
- **Flujo de Datos**:
  - El flujo de datos se gestiona principalmente a través de la interfaz de usuario y las solicitudes HTTP al backend.

