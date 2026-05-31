# Documentación Técnica - Directorio: static/js
Compilado el: 2026-05-30 00:23:08
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


---

## Archivo: ./static/js/consumos.js

### Resumen Funcional
El archivo `consumos.js` contiene funciones y métodos para gestionar la interfaz de usuario y el procesamiento de datos relacionados con los consumos en materiales. Permite buscar y filtrar datos por Centro de Costo (CeCo) o por materiales, muestra resultados en una tabla y permite visualizar tendencias mensuales de consumo.

### Catálogo de Funciones y Clases
- `handlePaste(e)` - Maneja el evento de pegado para rellenar múltiples celdas.
- `limpiarGrilla()` - Limpia la grilla de entrada y oculta el contenedor de resultados.
- `formatearDinero(valor)` - Formatea un valor numérico como dinero.
- `formatearNumero(valor)` - Formatea un valor numérico como número.
- `filterTable(tableId)` - Filtra una tabla según los valores en las celdas de entrada de la cabecera.
- `renderVanillaTable(tbodyId, data, columns, onRowClick = null)` - Renderiza una tabla usando elementos HTML y JavaScript puro.
- `buscarPorCeCo()` - Busca datos por Centro de Costo y muestra los resultados en una tabla.
- `buscarPorMateriales()` - Busca datos por materiales ingresados en la grilla y muestra los resultados en una tabla.
- `abrirTendenciaMaterial(material, areaNegocio, descripcion, ceco = '')` - Abre un modal con la tendencia mensual de consumo para un material específico.
- `cerrarTendenciaMaterial()` - Cierra el modal de tendencia.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `_tendenciaChart` - Variable global que almacena una instancia del gráfico de tendencias mensuales.

### Dependencias y Flujo
- **Librerías Externas**: `Chart.js` (usado para renderizar el gráfico de tendencias).
- **Flujo Interno**: El archivo interactúa con elementos HTML para mostrar resultados, manejar eventos de usuario y realizar peticiones a una API para obtener datos.


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

## Archivo: ./static/js/dashboard.js (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `dashboard.js` contiene la lógica principal del dashboard de MonitorWeb, que incluye funciones para interactuar con una API, manejar la interfaz de usuario y actualizar los datos en tiempo real.

### Catálogo de Funciones y Clases
- **DashboardAPI**
  - `_fetch(url, options = {})`: Realiza solicitudes HTTP a la API.
  - `fetchKPIs(params)`: Obtiene indicadores clave (KPIs).
  - `fetchFilteredData(params)`: Obtiene datos filtrados.
  - `sync()`: Sincroniza los datos del cliente con el servidor.
  - `checkSyncStatus()`: Verifica el estado de la sincronización.
  - `logout()`: Cierra sesión y limpia el almacenamiento local.

- **UI**
  - `openPdfModal()`: Abre un modal para ver PDFs.
  - `closePdfModal()`: Cierra el modal de PDFs.
  - `toggleMulti(id)`: Muestra u oculta elementos según su ID.
  - `setBtnLoading(btn, text, isLoading)`: Cambia el estado del botón a cargando o normal.

- **renderTableRow(t)**: Renderiza una fila de la tabla con los datos proporcionados.
- **executeFilters()**: Ejecuta los filtros y actualiza los KPIs y la tabla.
- **applyFilters()**: Aplica los filtros cuando se cambia un checkbox.
- **getCheckboxValues(className)**: Obtiene los valores de los checkboxes seleccionados.
- **toggleSelectAll(className, isChecked)**: Selecciona/deselecciona todos los checkboxes según el estado del checkbox "Seleccionar todo".
- **handleSmartCheckbox(cb, className, selectAllId, context)**: Maneja la selección inteligente de checkboxes.
- **filterTable()**: Filtra las filas de la tabla según los valores de búsqueda.
- **sortTable(idx)**: Ordena la tabla por una columna específica.
- **updateLogoVal(btn)**: Actualiza el valor del checkbox "Incluir Logo".
- **pdfSubmit(btn, frameTarget, preview)**: Envía un formulario para generar y visualizar PDFs.
- **downloadBulk(action, btn)**: Descarga o previsualiza múltiples PDFs según la acción seleccionada.
- **syncData(e, onlyPoll = false)**: Inicia la sincronización de datos y verifica su estado.
- **startSyncPolling(btn)**: Comienza el sondeo para verificar el estado de la sincronización.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción directa con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales en este archivo.

### Dependencias y Flujo
- **Librerías Externas**: `fetch`, `Chart.js`, `ChartDataLabels`.
- **Flujo Interno**: El archivo interactúa con la API para obtener datos, actualiza el estado de los KPIs y la tabla, maneja eventos del usuario (como clics en botones y checkboxes), y renderiza elementos de la interfaz de usuario.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `dashboard.js` se encarga de inicializar y configurar los elementos del dashboard, incluyendo la sincronización de estado de radio buttons y la carga de widgets inmediatamente al iniciar.

### Catálogo de Funciones y Clases
- `initSaaSWidgets()` - Inicia el motor SaaS y carga los widgets inmediatamente al iniciar.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencia externa: `DashboardAPI` (se utiliza para verificar el estado de sincronización).


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

## Archivo: ./static/js/productivity.js (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `productivity.js` contiene funciones y lógica para cargar, renderizar y gestionar datos de productividad en una interfaz web. Permite cambiar la fecha y mes seleccionados, cargar datos de productividad diaria y mensual, y visualizar estos datos mediante gráficos y tablas.

### Catálogo de Funciones y Clases
- `loadProductivityData()` - Carga los datos de productividad para una fecha específica.
- `renderKPI1(summary)` - Renderiza el KPI 1 con resumen de actividad por usuario.
- `renderKPI2(trend)` - Renderiza el KPI 2 con tendencia diaria de movimientos.
- `renderKPI3(gaps)` - Renderiza el KPI 3 con baches de inactividad detectados.
- `renderKPI4(heatmapData)` - Renderiza el KPI 4 con mapa de calor de actividad.
- `loadMonthlyProductivityData()` - Carga los datos de productividad mensuales para un mes específico.
- `renderMonthlyKPI1(summary)` - Renderiza el KPI 1 mensual con resumen de actividad por usuario.
- `renderMonthlyKPI2(shifts)` - Renderiza el KPI 2 mensual con tendencia diaria de movimientos por turno.
- `renderMonthlyKPI3(heatmapData)` - Renderiza el KPI 3 mensual con mapa de calor de actividad.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `productivityTrendChartInst` - Instancia del gráfico de tendencia diaria.
- `productivityMonthlyTrendChartInst` - Instancia del gráfico de tendencia mensual.
- `COLORS` - Array con colores institucionales.

### Dependencias y Flujo
Dependencias:
- `fetch` - Para hacer solicitudes HTTP.
- `Chart.js` - Para renderizar gráficos.

Flujo:
- El archivo se comunica con el servidor a través de endpoints `/api/v1/analytics/productivity` y `/api/v1/analytics/productivity/monthly`.
- Los datos cargados se utilizan para actualizar las tablas y gráficos en la interfaz web.


---

## Archivo: ./static/js/saas_engine.js (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `saas_engine.js` es un motor SaaS que se encarga de leer contenedores con la clase `.saas-widget-v2`, renderizar gráficos o KPIs, y manejar interacciones como el drilldown.

### Catálogo de Funciones y Clases
- `initSaaSWidgetsV2(params = null, rootElement = document)` - Inicializa los widgets SaaS en el elemento raíz especificado.
- `openDrilldownModal(queryId, segmentLabel, materialId = null)` - Abre un modal con detalles del drilldown.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `window.saasChartInstancesV2` - Almacena instancias de gráficos Chart.js para widgets individuales.
- `window.openDrilldownModal` - Función global que maneja el drilldown.

### Dependencias y Flujo
- Depende de la librería `Chart.js` para renderizar gráficos.
- Comunica con un servidor a través de peticiones `fetch` a endpoints como `/api/widget/{queryId}` y `/api/widget/{queryId}/drilldown`.
- Utiliza funciones globales como `window.openDrilldownModal`, `window.sortDrilldownTable`, y `window.filterDrilldownTable`.


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

## Archivo: ./static/js/transporte.js

### Resumen Funcional
El archivo `transporte.js` es un script que se encarga de cargar y mostrar datos de transporte en un gráfico y una tabla. Los datos son obtenidos a través de una API, filtrados y agrupados según el grupo seleccionado (mensual o semanal), y luego renderizados en un gráfico de líneas y una tabla.

### Catálogo de Funciones y Clases
- `loadData()` - Carga los datos de transporte desde la API y los renderiza.
- `getMonday(dateStr)` - Calcula la fecha del lunes correspondiente a una fecha dada.
- `updateTransporteChartGroup(group)` - Actualiza el grupo de datos para el gráfico y vuelve a renderizarlo.
- `renderChart()` - Renderiza el gráfico de transporte basado en los datos cargados.
- `renderTable(data)` - Renderiza la tabla de transporte con los últimos 25 registros.
- `openPdfViewer(url)` - Abre un modal para ver un PDF.
- `closePdfViewer()` - Cierra el modal y detiene la carga del PDF.
- `searchTransporte()` - Realiza una búsqueda en tiempo real en los datos de transporte.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con bases de datos.

### Estado y Variables Globales
- `chartInstance` - Almacena la instancia actual del gráfico.
- `allTransporteData` - Almacena todos los datos de transporte cargados desde la API.
- `currentChartGroup` - Almacena el grupo actual seleccionado para el gráfico (mensual o semanal).
- `transporteSearchTimeout` - Almacena el timeout para el debouncer del buscador.

### Dependencias y Flujo
- **Librerías Externas**: `fetch`, `Chart.js`, `ChartDataLabels`.
- **Flujo Interno**: El archivo se carga al DOMContentLoaded, luego llama a `loadData()`. `loadData()` realiza una solicitud fetch a la API para obtener los datos de transporte, que luego son renderizados en el gráfico y la tabla. Los eventos como el cambio de grupo del gráfico o la búsqueda activan funciones específicas para actualizar el contenido visual.


---

