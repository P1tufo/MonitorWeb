# Documentación Técnica - Directorio: static/js
Compilado el: 2026-05-23 00:11:14
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./static/js/analytics_proyecciones.js

### Resumen Funcional
El archivo `analytics_proyecciones.js` contiene lógica para renderizar y controlar modales de alertas, combinaciones y gráficos de dispersión en una interfaz web. Utiliza funciones para filtrar y mostrar datos basados en criterios de búsqueda y selección.

### Catálogo de Funciones y Clases
- `renderAlerts()` - Renderiza los datos de alertas en un modal.
- `renderCombos(filterText = "")` - Renderiza los datos de combinaciones en un modal, filtrando por texto.
- `renderScatter()` - Renderiza los datos de dispersión en un modal, filtrando por texto y categoría.
- `openModalAlerts()` - Abre el modal de alertas y carga los datos iniciales.
- `openModalCombos()` - Abre el modal de combinaciones y carga los datos iniciales.
- `openModalScatter()` - Abre el modal de dispersión y carga los datos iniciales.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencia: `core_ui.js` (carga previa para proporcionar funciones como `CoreUI.openModal`, `CoreUI.closeModal`, `CoreUI.populateAreaSelect`, y `CoreUI.getData`).


---

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


---

## Archivo: ./static/js/core_ui.js

### Resumen Funcional
El archivo `core_ui.js` es un módulo de utilidades de interfaz de usuario compartido por todas las vistas del proyecto. Proporciona funciones para mostrar y ocultar modales, renderizar modales de lista de materiales, poblar selectores con áreas únicas y leer datos JSON embebidos en el DOM.

### Catálogo de Funciones y Clases
- `CoreUI.openModal(id)` - Muestra un modal por su ID de elemento.
- `CoreUI.closeModal(id)` - Oculta un modal por su ID de elemento.
- `CoreUI.renderMaterialModal(opts)` - Rellena y abre un modal de lista de materiales con los ítems proporcionados.
- `CoreUI.populateAreaSelect(selectId, data, key)` - Rellena un elemento `<select>` con áreas únicas encontradas en un array de datos.
- `CoreUI.getData(id)` - Lee y parsea JSON embebido en el textContent de un elemento del DOM.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- No se mencionan dependencias externas específicas en este archivo.

Flujo:
- El módulo expone funciones útiles para la interfaz de usuario.
- Las funciones pueden ser llamadas directamente desde el DOM o a través de alias globales (`window.openModal` y `window.closeModal`).


---

## Archivo: ./static/js/dashboard.js

### Resumen Funcional
El archivo `dashboard.js` contiene la lógica principal del dashboard de MonitorWeb. Define funciones para interactuar con una API, manejar la interfaz de usuario (UI), aplicar filtros y ordenar tablas, generar PDFs, y sincronizar datos.

### Catálogo de Funciones y Clases
- `DashboardAPI._fetch(url, options)` - Realiza solicitudes HTTP a la API.
- `DashboardAPI.fetchKPIs(params)` - Obtiene los KPIs (Indicadores Clave de Desempeño) basados en los parámetros proporcionados.
- `DashboardAPI.fetchFilteredData(params)` - Obtiene datos filtrados según los parámetros proporcionados.
- `DashboardAPI.sync()` - Sincroniza los datos del cliente con el servidor.
- `DashboardAPI.checkSyncStatus()` - Verifica el estado de la sincronización actual.
- `DashboardAPI.logout()` - Cierra sesión y redirige al usuario a la página de inicio de sesión.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- `fetch` (navegador)
- `localStorage`

Flujo:
- El archivo interactúa con la API para obtener datos, renderizar tablas, aplicar filtros, generar PDFs y sincronizar datos.
- Utiliza funciones globales como `closePdfModal`, `toggleMulti`, `sortTable`, etc., que se definen en el mismo archivo y son accesibles globalmente a través de `window`.


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
El archivo `deliveries.js` contiene la lógica para el análisis de entregas, incluyendo la interacción con componentes UI, controladores de modales, inicialización de gráficos y actualizaciones dinámicas del estado.

### Catálogo de Funciones y Clases
- `openModal(id)` - Abre un modal utilizando CoreUI.
- `closeModal(id)` - Cierra un modal utilizando CoreUI.
- `renderMaterialModal(opts)` - Renderiza un modal con opciones específicas.
- `getData(id)` - Obtiene datos desde una fuente externa.
- `toggleModalFilter(type, isCurrentMonth)` - Alternativa entre mostrar modales de área y día según el contexto actual.
- `openModalWeekday(dayName, isCurrentMonth = false)` - Abre un modal para mostrar detalles del día.
- `openModalUbicacion(name)` - Abre un modal para mostrar detalles de ubicación.
- `openModalArea(name, isCurrentMonth = false)` - Abre un modal para mostrar detalles de área.
- `openModalUser(name)` - Abre un modal para mostrar detalles de usuario.
- `switchVLView(view)` - Cambia la vista entre operativa y histórica.
- `toggleMulti(id)` - Alterna la visibilidad de elementos según su ID.
- `updateDeliveriesAnalytics()` - Actualiza los KPIs y filtra listas y gráficos según las áreas seleccionadas.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `currentModalContext` - Almacena el contexto actual del modal (área y día).
- `window.slaTrendChart`, `window.monthlyTrendChart`, etc. - Referencias a gráficos inicializados.

### Dependencias y Flujo
Depende de `core_ui.js` para funciones UI como `openModal`, `closeModal`, y `renderMaterialModal`. Utiliza `getData` para obtener datos desde fuentes externas.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `deliveries.js` contiene funciones para actualizar gráficos de rendimiento diario, semanal y mensual basados en datos seleccionados. Actualiza los datos de las gráficas de SLA (Service Level Agreement) y entrega semanal.

### Catálogo de Funciones y Clases
- `updateDeliveriesAnalytics()` - Actualiza los datos de las gráficas de rendimiento.
- `window.toggleChartSelectAll(isChecked)` - Maneja la selección de todos los elementos en un grupo de checkboxes.
- `window.handleSmartCheckbox(cb)` - Maneja la selección inteligente de elementos individuales en un grupo de checkboxes.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- `getData('data_weekly_raw_json')`
- `getData('data_sla_area_trend_raw_json')`

Flujo:
1. La función `updateDeliveriesAnalytics()` se ejecuta cuando se necesitan actualizar los datos de las gráficas.
2. Se filtran los datos según la selección del usuario (`selected`).
3. Los datos filtrados se agrupan y procesan para calcular SLA y entregas.
4. Los resultados se actualizan en las gráficas correspondientes.

La función `window.toggleChartSelectAll(isChecked)` maneja la selección de todos los elementos en un grupo de checkboxes, asegurando que no haya una selección vacía.

La función `window.handleSmartCheckbox(cb)` maneja la selección inteligente de elementos individuales, asegurando que si "Todos" está seleccionado y se selecciona uno individualmente, "Todos" se deselecciona.


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
El archivo `inventory.js` contiene lógica para el análisis de inventario, incluyendo la visualización de gráficos y la interacción con modales. Se utilizan Chart.js para crear gráficos de doughnut y lineas, y se manejan eventos de entrada para buscar ubicaciones dinámicamente.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra mensajes en la consola.
- `UI.openModal(id)` - Abre un modal utilizando CoreUI.
- `UI.closeModal(id)` - Cierra un modal utilizando CoreUI.
- `UI.renderMaterialModal(opts)` - Renderiza un modal de material utilizando CoreUI.
- `getData(id)` - Obtiene datos desde el DOM utilizando CoreUI.
- `parseFormattedInt(val)` - Convierte una cadena a un número entero, eliminando caracteres no numéricos.
- `window.openModalUbicacion(name)` - Abre un modal con información de ubicación.
- `window.openModalUserInv(name)` - Abre un modal con información de usuario.
- `window.switchInventarioView(view)` - Cambia la vista del gráfico de tendencias según el parámetro `view`.
- `window.toggleMultiInv(id)` - Alterna la visibilidad de un elemento según su ID.
- `window.toggleAllInvAreas(checkbox)` - Alterna la selección de todas las áreas y actualiza los KPIs.
- `window.updateInventoryAnalytics()` - Actualiza los KPIs y filtra listas según las áreas seleccionadas.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: Chart.js, CoreUI.
- **Flujo Interno**: El archivo interactúa con el DOM para obtener datos y renderizar gráficos. Utiliza funciones de CoreUI para abrir y cerrar modales.


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

