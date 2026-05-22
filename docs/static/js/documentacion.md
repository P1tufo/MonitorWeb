# Documentación Técnica - Directorio: static/js
Compilado el: 2026-05-22 16:53:13
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./static/js/analytics_proyecciones.js

### Resumen Funcional
El archivo `analytics_proyecciones.js` contiene lógica para manejar la interacción con una interfaz de usuario (UI) y renderizar datos en diferentes modales. Los datos se filtran y presentan según los criterios ingresados por el usuario.

### Catálogo de Funciones y Clases
- `UI.openModal(id)` - Abre un modal identificado por `id`.
- `UI.closeModal(id)` - Cierra un modal identificado por `id`.
- `UI.populateAreaSelect(selectId, data, key = 'area')` - Llena un selector de áreas con valores únicos del conjunto de datos proporcionado.
- `getData(id)` - Obtiene y parsea los datos almacenados en un elemento HTML con el ID especificado.
- `renderAlerts()` - Renderiza una tabla de alertas basada en los criterios de búsqueda y filtro.
- `renderCombos(filterText = "")` - Renderiza una lista de combinaciones de materiales basadas en la búsqueda del usuario.
- `renderScatter()` - Renderiza un gráfico de dispersión basado en los criterios de búsqueda y filtro.
- `openModalAlerts()` - Abre el modal de alertas, llena el selector de áreas y renderiza las alertas.
- `openModalCombos()` - Abre el modal de combinaciones, limpia la entrada de búsqueda y renderiza las combinaciones.
- `openModalScatter()` - Abre el modal de dispersión, llena los selectores de área y categoría, limpia las entradas de búsqueda y renderiza el gráfico.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: `Chart.js` (usado para crear el gráfico de dispersión).
- **Flujo Interno**: El archivo interactúa con elementos HTML para obtener datos, renderizar contenido en modales y actualizar gráficos.


---

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


---

## Archivo: ./static/js/dashboard.js

### Resumen Funcional
El archivo `dashboard.js` contiene la lógica principal del dashboard de MonitorWeb. Define funciones para interactuar con una API, manejar la interfaz de usuario (UI), renderizar tablas y aplicar filtros.

### Catálogo de Funciones y Clases
- **DashboardAPI**
  - `_fetch(url, options)` - Realiza solicitudes HTTP a la API.
  - `fetchKPIs(params)` - Obtiene los KPIs basados en los parámetros proporcionados.
  - `fetchFilteredData(params)` - Obtiene datos filtrados según los parámetros proporcionados.
  - `sync()` - Sincroniza los datos del cliente con el servidor.
  - `checkSyncStatus()` - Verifica el estado de la sincronización.
  - `logout()` - Cierra sesión y redirige al usuario a la página de inicio de sesión.

- **UI**
  - `openPdfModal()` - Abre el modal para ver PDFs.
  - `closePdfModal()` - Cierra el modal y limpia su contenido.
  - `toggleMulti(id)` - Alterna la visibilidad de un elemento con el ID especificado.
  - `setBtnLoading(btn, text, isLoading)` - Establece el estado de carga de un botón.

- **Funciones Globales**
  - `renderTableRow(t)` - Renderiza una fila de tabla para los datos proporcionados.
  - `executeFilters()` - Ejecuta los filtros y actualiza la tabla y KPIs.
  - `applyFilters()` - Aplica los filtros cuando se cambia un valor de entrada.
  - `getCheckboxValues(className)` - Obtiene los valores de las casillas de verificación con el nombre de clase especificado.
  - `toggleSelectAll(className, isChecked)` - Alterna la selección de todas las casillas de verificación con el nombre de clase especificado.
  - `handleSmartCheckbox(cb, className, selectAllId, context)` - Maneja la selección inteligente de casillas de verificación.
  - `filterTable()` - Filtra la tabla según los valores de entrada.
  - `sortTable(idx)` - Ordena la tabla según el índice de columna especificado.
  - `updateLogoVal(btn)` - Actualiza el valor del campo oculto para incluir o no el logotipo en el PDF.
  - `pdfSubmit(btn, frameTarget, preview)` - Envía un formulario para generar y visualizar/descargar PDFs.
  - `downloadBulk(action, btn)` - Descarga múltiples PDFs según los parámetros proporcionados.
  - `syncData(e, onlyPoll = false)` - Inicia la sincronización de datos y verifica su estado.
  - `startSyncPolling(btn)` - Comienza el sondeo para verificar el estado de la sincronización.
  - `toggleSidebar()` - Alterna la visibilidad del sidebar.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: `fetch`
- **Flujo Interno**: El archivo interactúa con el backend a través de la API definida en `DashboardAPI` para obtener datos, ejecutar filtros y sincronizar información. La UI se actualiza dinámicamente según los resultados obtenidos.


---

## Archivo: ./static/js/dashboard_charts.js

### Resumen Funcional
Este archivo JavaScript se encarga de inicializar y gestionar un gráfico de barras pilaado en el panel de control, calculando y mostrando la suma total de los datos para cada categoría. También proporciona funcionalidades para seleccionar/deseleccionar todos los elementos del gráfico.

### Catálogo de Funciones y Clases
- `stackedTotalPlugin` - Plugin que agrega una etiqueta con el total acumulado en cada barra del gráfico.
  - Parámetros: `chart` (el contexto del gráfico).
  - Propósito: Calcula la suma total de los datos para cada categoría y muestra esta suma en la parte superior de las barras.

- `initWeeklyChart(chartLabels, chartDatasets)` - Inicializa el gráfico de barras pilaado.
  - Parámetros: `chartLabels` (etiquetas del eje X), `chartDatasets` (conjuntos de datos para el gráfico).
  - Propósito: Configura y muestra el gráfico con los datos proporcionados.

- `toggleChartSelectAll(isChecked)` - Función que selecciona/deselecciona todos los elementos del gráfico.
  - Parámetros: `isChecked` (booleano, indica si se debe seleccionar o deseleccionar).
  - Propósito: Actualiza el estado de selección de todos los checkboxes relacionados con el gráfico.

- `updateChartVisibility()` - Función que actualiza la visibilidad de los conjuntos de datos del gráfico según las selecciones.
  - Parámetros: Ninguno.
  - Propósito: Oculta o muestra los conjuntos de datos del gráfico según qué checkboxes están seleccionados.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
- `window.weeklyChart` - Variable global que almacena el contexto del gráfico inicializado.

### Dependencias y Flujo
- **Librerías Externas**: `Chart.js` (usado para crear y gestionar el gráfico).
- **Flujo Interno**: El archivo se comunica con otros elementos del DOM para obtener referencias a checkboxes y elementos de entrada, y también interactúa con la función `applyFilters` si está definida.


---

## Archivo: ./static/js/deliveries.js (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `deliveries.js` contiene lógica para el análisis de entregas, incluyendo la interacción con componentes UI como modales y gráficos. Maneja datos de entrega, calcula indicadores clave (KPIs) y actualiza visualmente los gráficos en función de las selecciones del usuario.

### Catálogo de Funciones y Clases
- `UI.openModal(id)` - Abre un modal con el ID especificado.
- `UI.closeModal(id)` - Cierra un modal con el ID especificado.
- `UI.renderMaterialModal({ modalId, titleId, listId, title, items, colorVar, bgColor })` - Renderiza una lista de materiales en un modal.
- `getData(id)` - Obtiene datos JSON desde elementos del DOM.
- `openModalWeekday(dayName, isCurrentMonth = false)` - Abre el modal para mostrar detalles diarios.
- `openModalUbicacion(name)` - Abre el modal para mostrar detalles de ubicación.
- `openModalArea(name, isCurrentMonth = false)` - Abre el modal para mostrar detalles de área.
- `openModalUser(name)` - Abre el modal para mostrar detalles del usuario.
- `switchVLView(view)` - Cambia la vista entre operativa y histórica.
- `toggleMulti(id)` - Alterna la visibilidad de un elemento con el ID especificado.
- `updateDeliveriesAnalytics()` - Actualiza los KPIs y visualización en función de las selecciones del usuario.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `currentModalContext` - Almacena el contexto actual del modal (área o día).
- `window.openModal`, `window.closeModal`, `window.toggleModalFilter`, `window.openModalArea`, `window.openModalUser`, `window.openModalUbicacion` - Funciones globales para controlar modales y vistas.
- `window.slaTrendChart`, `window.slaAreaTrendChart`, `window.weeklyTrendChart`, `window.monthlyTrendChart`, `window.slaMonthlyTrendChart`, `window.slaMonthlyTrellisCharts` - Referencias a gráficos.

### Dependencias y Flujo
- Depende de la librería Chart.js para crear gráficos.
- Utiliza funciones globales definidas en el mismo archivo para controlar modales y vistas.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `deliveries.js` contiene funciones para actualizar gráficos y listas de áreas seleccionadas en una interfaz web, basándose en datos filtrados.

### Catálogo de Funciones y Clases
- `updateDeliveriesAnalytics()` - Actualiza los gráficos y la lista de áreas seleccionadas.
- `toggleChartSelectAll(isChecked)` - Maneja el estado del checkbox "Seleccionar todo" para los gráficos.
- `handleSmartCheckbox(cb)` - Maneja el comportamiento inteligente de los checkboxes individuales.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `window.areaMixChart` - Referencia al gráfico de mezcla de áreas.
- `window.weekHeatChart` - Referencia al gráfico de calor semanal.
- `selected` - Array que contiene las áreas seleccionadas.

### Dependencias y Flujo
- No depende de ninguna librería externa.
- Comunica con otros archivos del proyecto a través de funciones globales como `updateDeliveriesAnalytics()`.


---

## Archivo: ./static/js/docs_explorer.js

### Resumen Funcional
El archivo `docs_explorer.js` es un script que se encarga de cargar y renderizar una estructura de árbol de documentos en la interfaz web. Este árbol permite navegar por los archivos y carpetas, y al seleccionar un archivo, carga su contenido en el área de visualización.

### Catálogo de Funciones y Clases
- `initDocs()` - Inicializa la exploración de documentos, cargando la estructura del árbol desde una API y renderizando los nodos.
- `loadFile(path)` - Carga el contenido de un archivo específico en el área de visualización.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Dependencias**: El script utiliza la librería `fetch` para hacer solicitudes HTTP a una API. También depende de la librería `marked` si está disponible, para procesar el contenido del archivo como Markdown.
- **Flujo**: El flujo comienza con la carga del documento (`DOMContentLoaded`), luego se ejecuta `initDocs()`. Este método llama a `loadFile()` cuando se selecciona un archivo en el árbol.


---

## Archivo: ./static/js/inventory.js

### Resumen Funcional
El archivo `inventory.js` contiene lógica para el análisis de movimientos en un inventario, con funcionalidades como la visualización de gráficos y modales interactivos. Incluye manejo de datos desde elementos HTML, renderizado de gráficos usando Chart.js, y funciones para abrir y cerrar modales.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra mensajes en la consola con un formato específico.
- `UI.openModal(id)` - Abre un modal identificado por `id`.
- `UI.closeModal(id)` - Cierra un modal identificado por `id`.
- `UI.renderMaterialModal(options)` - Renderiza un modal con detalles de materiales, incluyendo una lista de elementos y estadísticas.
- `getData(id)` - Obtiene datos desde un elemento HTML con el ID especificado.
- `parseFormattedInt(val)` - Convierte una cadena formateada en un número entero.
- `window.openModalUbicacion(name)` - Abre un modal con la ubicación de un material específico.
- `window.openModalUserInv(name)` - Abre un modal con los detalles del inventario de un usuario específico.
- `window.switchInventarioView(view)` - Cambia la vista del gráfico de tendencias entre históricos y actuales.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales en este archivo.

### Dependencias y Flujo
- **Librerías Externas**: `Chart.js`, `ChartDataLabels`.
- **Flujo Interno**: El archivo interactúa con elementos HTML para obtener datos, renderizar modales y actualizar gráficos de Chart.js. No hay interacción directa con otros archivos del proyecto a menos que se invoquen las funciones globales definidas (`window.openModalUbicacion`, `window.openModalUserInv`, `window.switchInventarioView`).


---

## Archivo: ./static/js/sla_table.js

### Resumen Funcional
Este archivo contiene la lógica para manejar el comportamiento de una tabla de auditoría SLA en una aplicación web, incluyendo la interacción con un modal PDF y el envío de formularios.

### Catálogo de Funciones y Clases
- `openPdfModal()` - Abre el modal PDF.
- `closePdfModal()` - Cierra el modal PDF y limpia su contenido.
- `pdfSubmit(btn, frameTarget, preview)` - Envía un formulario y maneja la interacción con un iframe para mostrar una vista previa del PDF.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- No depende de ninguna librería externa.
- Se comunica con otros archivos a través de la ventana global (`window.pdfSubmit` y `window.closePdfModal`).


---

## Archivo: ./static/js/tasks.js

### Resumen Funcional
El archivo `tasks.js` contiene la lógica para inicializar y configurar dos gráficos de tendencia y usuarios utilizando la biblioteca Chart.js. Los datos necesarios se obtienen del DOM y se utilizan para renderizar los gráficos.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra un mensaje en la consola con opcionalmente datos adicionales.
- `getData(id)` - Obtiene y analiza el contenido JSON de un elemento del DOM identificado por su ID.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales en este archivo.

### Dependencias y Flujo
- **Librerías Externas**: `Chart.js`, `ChartDataLabels`.
- **Flujo Interno**: El archivo se ejecuta cuando el DOM esté completamente cargado (`DOMContentLoaded`). Luego, intenta obtener datos de elementos del DOM y usarlos para crear dos gráficos (uno de tipo línea y otro de tipo barras) utilizando Chart.js.


---

