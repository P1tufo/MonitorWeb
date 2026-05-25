# Documentación Técnica - Directorio: static/js
Compilado el: 2026-05-24 23:35:28
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
El archivo `analytics_studio.js` contiene funciones y clases para gestionar el estado visual de consultas en un sistema de análisis. Permite abrir modales, cargar esquemas de base de datos, previsualizar tablas y ejecutar consultas para generar gráficos.

### Catálogo de Funciones y Clases
- `AnalyticsStudioManager.getVisualState(queryId)` - Obtiene el estado visual de una consulta.
- `AnalyticsStudioManager.setVisualState(queryId, state)` - Establece el estado visual de una consulta.
- `openEditQueryModal(queryId, chartTitle)` - Abre un modal para editar una consulta.
- `loadSchema()` - Carga el esquema de la base de datos.
- `previewTable(tableName, el)` - Previsualiza los datos de una tabla.
- `runPreview()` - Ejecuta una previsualización de la consulta y renderiza el gráfico.
- `renderPreviewChart(payload)` - Renderiza el gráfico basado en los datos de la consulta.
- `closeEditQueryModal()` - Cierra el modal para editar una consulta.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `AnalyticsStudioManager.instances` - Almacena instancias de estado visual por consulta.
- `studioChartInstance` - Instancia del gráfico actual.
- `currentSchema` - Esquema de la base de datos actual.
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
El archivo `analytics_studio.js` contiene funciones y lógica para gestionar la edición, publicación y configuración de consultas analíticas en un estudio de datos. Permite crear, modificar y ejecutar consultas SQL interactuando con una interfaz gráfica basada en JavaScript.

### Catálogo de Funciones y Clases
- `closeEditQueryModal()` - Cierra el modal para editar consultas.
- `showConfirmPublish()` - Muestra la ventana de confirmación para publicar una consulta.
- `hideConfirmPublish()` - Oculta la ventana de confirmación para publicar una consulta.
- `executePublishQuery()` - Ejecuta la publicación de una consulta y maneja la respuesta del servidor.
- `initVisualQuery(queryId)` - Inicializa el estado visual de la consulta y carga los datos necesarios.
- `onBaseTableChange()` - Maneja el cambio en la tabla base seleccionada.
- `getActiveTables()` - Devuelve las tablas activas en la consulta.
- `getActiveColumns()` - Devuelve las columnas activas en la consulta.
- `refreshQbColumns(forceState = false)` - Refresca los selectores de columnas para los ejes y desglose.
- `renderJoins()` - Renderiza los controles de joins en la interfaz.
- `addJoin()` - Añade un nuevo join a la consulta.
- `updateJoin(index)` - Actualiza un join existente.
- `removeJoin(index)` - Elimina un join.
- `renderFilters()` - Renderiza los controles de filtros en la interfaz.
- `addFilter()` - Añade un nuevo filtro a la consulta.
- `updateFilterType(index, type)` - Actualiza el tipo de valor para un filtro.
- `updateFilter(index)` - Actualiza los detalles de un filtro existente.
- `removeFilter(index)` - Elimina un filtro.
- `onSecondMetricToggle()` - Maneja el toggle de la segunda métrica.
- `onQbChange()` - Sincroniza los cambios en la interfaz con el estado visual de la consulta.

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
- `AnalyticsStudioManager` - Para gestionar el estado visual de la consulta.

Flujo: El archivo interactúa con la interfaz del usuario para permitir la edición, publicación y ejecución de consultas analíticas. No realiza interacciones directas con una base de datos.


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

## Archivo: ./static/js/dashboard.js (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `dashboard.js` contiene la lógica principal del dashboard de MonitorWeb, que incluye funciones para interactuar con una API, manejar la interfaz de usuario (UI), renderizar tablas y gráficos, aplicar filtros, y gestionar la sincronización de datos.

### Catálogo de Funciones y Clases
- `DashboardAPI._fetch(url, options = {})` - Realiza solicitudes HTTP a la API.
- `DashboardAPI.fetchKPIs(params)` - Obtiene los KPIs (Indicadores Clave de Desempeño) basados en los parámetros proporcionados.
- `DashboardAPI.fetchFilteredData(params)` - Obtiene datos filtrados según los parámetros proporcionados.
- `DashboardAPI.sync()` - Sincroniza los datos del cliente con el servidor.
- `DashboardAPI.checkSyncStatus()` - Verifica si la sincronización está en curso.
- `DashboardAPI.logout()` - Cierra sesión y limpia el almacenamiento local.
- `UI.openPdfModal()` - Abre un modal para ver PDFs.
- `UI.closePdfModal()` - Cierra el modal de PDF.
- `UI.toggleMulti(id)` - Alterna la visibilidad de elementos con una clase específica.
- `UI.setBtnLoading(btn, text, isLoading)` - Establece el estado de carga de un botón.
- `renderTableRow(t)` - Renderiza una fila de tabla HTML.
- `executeFilters()` - Ejecuta los filtros y actualiza la interfaz del usuario.
- `applyFilters()` - Aplica los filtros cuando se cambia algún valor.
- `getCheckboxValues(className)` - Obtiene los valores de las casillas de verificación seleccionadas.
- `toggleSelectAll(className, isChecked)` - Alterna el estado de todas las casillas de verificación en una clase específica.
- `handleSmartCheckbox(cb, className, selectAllId, context)` - Maneja la selección inteligente de casillas de verificación.
- `filterTable()` - Filtra la tabla según los valores de búsqueda.
- `sortTable(idx)` - Ordena la tabla por una columna específica.
- `updateLogoVal(btn)` - Actualiza el valor del logo en un formulario.
- `pdfSubmit(btn, frameTarget, preview)` - Envía un formulario para generar y visualizar PDFs.
- `downloadBulk(action, btn)` - Descarga o previsualiza múltiples PDFs según la acción seleccionada.
- `syncData(e, onlyPoll = false)` - Inicia la sincronización de datos y maneja el estado de carga del botón.
- `startSyncPolling(btn)` - Comienza a sondear el estado de la sincronización.
- `initSaaSWidgets(params = null)` - Inicializa los widgets SaaS en el dashboard.
- `renderSaaSChart(container, queryId, data)` - Renderiza un gráfico SaaS.
- `renderSaaSTrellis(container, queryId, data)` - Renderiza una trillera de gráficos SaaS.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción directa con bases de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales en este archivo.

### Dependencias y Flujo
- **Librerías Externas**: `fetch`, `Chart.js`, `ChartDataLabels`.
- **Flujo Interno**: El archivo interactúa con la API a través de las funciones del objeto `DashboardAPI` para obtener datos, ejecutar filtros, renderizar tablas y gráficos, manejar la sincronización, etc. La interfaz de usuario se actualiza en respuesta a los eventos del usuario y las respuestas de la API.


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

## Archivo: ./static/js/deliveries.js

### Resumen Funcional
El archivo `deliveries.js` contiene la lógica para el análisis de entregas, incluyendo la interacción con modales y gráficos. Permite filtrar datos por área, día de la semana y usuario, y actualiza los KPIs y listas en función de estos filtros.

### Catálogo de Funciones y Clases
- `toggleModalFilter(type, isCurrentMonth)` - Abre un modal basado en el tipo de filtro (área o día de la semana).
- `openModalWeekday(dayName, isCurrentMonth = false)` - Abre el modal para mostrar datos del día.
- `openModalUbicacion(name)` - Abre el modal para mostrar materiales retirados desde una ubicación específica.
- `openModalArea(name, isCurrentMonth = false)` - Abre el modal para mostrar datos de una área específica.
- `openModalUser(name)` - Abre el modal para mostrar los materiales solicitados por un usuario específico.
- `switchVLView(view)` - Cambia la vista entre operativa y histórica.
- `updateDeliveriesAnalytics()` - Recalcula y actualiza los KPIs y listas de entregas según los filtros seleccionados.
- `toggleMulti(id)` - Alterna la visibilidad de un elemento con el ID especificado.
- `toggleChartSelectAll(isChecked)` - Maneja el estado del checkbox "Seleccionar todo".
- `handleSmartCheckbox(cb)` - Maneja el comportamiento inteligente de los checkboxes individuales.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `currentModalContext` - Almacena el contexto actual del modal (área o día de la semana).

### Dependencias y Flujo
- Depende de `core_ui.js`, que proporciona funciones como `CoreUI.openModal`, `CoreUI.closeModal`, `CoreUI.renderMaterialModal`, y `CoreUI.getData`.
- Comunica con otros archivos a través de las siguientes variables globales:
  - `window.toggleModalFilter`
  - `window.openModalArea`
  - `window.openModalUser`
  - `window.openModalUbicacion`
  - `window.switchVLView`
  - `window.updateDeliveriesAnalytics`
  - `window.toggleChartSelectAll`
  - `window.handleSmartCheckbox`


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
El archivo `inventory.js` contiene lógica para manejar movimientos analíticos en una interfaz web, utilizando funciones y métodos para abrir modales, procesar datos, y gestionar la interacción con un buscador de ubicaciones dinámico.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra mensajes en la consola.
- `parseFormattedInt(val)` - Convierte una cadena a un número entero, eliminando caracteres no numéricos.
- `openModalUbicacion(name)` - Abre un modal con información de ubicación.
- `openModalUserInv(name)` - Abre un modal con información de usuario.
- `switchInventarioView(view)` - Cambia la vista del inventario según el parámetro proporcionado.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales en este archivo.

### Dependencias y Flujo
- Depende de `core_ui.js` para funciones como `openModal`, `closeModal`, `renderMaterialModal`, y `getData`.
- Comunica con el servidor a través de una solicitud `fetch` a la ruta `/api/ubicaciones/{valor}` para obtener datos de ubicaciones.


---

## Archivo: ./static/js/saas_engine.js

### Resumen Funcional
El archivo `saas_engine.js` es un motor SaaS que se encarga de leer contenedores con la clase `.saas-widget-v2`, obtener datos a través de una API y renderizar gráficos o KPIs en estos contenedores. El motor maneja diferentes tipos de widgets, como KPI numéricos y trellis (múltiples minigráficos), y permite el filtrado por área y año.

### Catálogo de Funciones y Clases
- `initSaaSWidgetsV2(params = null, rootElement = document)` - Inicializa los widgets SaaS en el elemento raíz especificado.
- `openDrilldownModal(queryId, segmentLabel, materialId = null)` - Abre un modal con detalles adicionales para un segmento específico.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción directa con una base de datos.

### Estado y Variables Globales
- `window.saasChartInstancesV2` - Almacena instancias de gráficos Chart.js renderizados en los widgets.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `fetch` - Para hacer solicitudes HTTP.
  - `Chart.js` - Para crear y gestionar gráficos.
  - `ChartDataLabels` - Plugin para Chart.js que permite mostrar etiquetas de datos en los gráficos.

- **Flujo Interno**:
  - El archivo se ejecuta al cargar el DOM (`DOMContentLoaded`).
  - Llama a `initSaaSWidgetsV2()` con un pequeño retraso para asegurar que el DOM esté listo.
  - `initSaaSWidgetsV2()` busca todos los elementos con la clase `.saas-widget-v2`, recopila parámetros de filtro, realiza solicitudes a una API y renderiza gráficos o KPIs en estos elementos.

El archivo no depende de otros archivos del proyecto directamente.


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

