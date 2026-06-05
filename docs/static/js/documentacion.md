# Documentación Técnica - Directorio: static/js
Compilado el: 2026-06-04 23:43:39
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./static/js/analytics_proyecciones.js

### Resumen Funcional
El archivo `analytics_proyecciones.js` contiene la lógica para renderizar y controlar los modales de alertas, combinaciones y gráficos de dispersión en una interfaz web. Utiliza funciones para filtrar y mostrar datos basados en criterios de búsqueda y selección.

### Catálogo de Funciones y Clases
- `renderAlerts()` - Renderiza la tabla de alertas.
- `renderCombos(filterText = "")` - Renderiza los combos de materiales.
- `renderScatter()` - Renderiza el gráfico de dispersión.
- `openModalAlerts()` - Abre el modal de alertas y carga los datos.
- `openModalCombos()` - Abre el modal de combinaciones y carga los datos.
- `openModalScatter()` - Abre el modal de gráficos de dispersión y carga los datos.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas a una base de datos.

### Estado y Variables Globales
No hay variables globales explícitas definidas en este archivo. Las variables utilizadas son principalmente para almacenar referencias a elementos del DOM y datos obtenidos mediante `getData`.

### Dependencias y Flujo
- **Dependencias**: El archivo depende de `core_ui.js` que proporciona funciones como `CoreUI.openModal`, `CoreUI.closeModal`, `CoreUI.populateAreaSelect` y `CoreUI.getData`.
- **Flujo de Datos**: 
  - Los datos se obtienen mediante `getData('data_alerts')`, `getData('data_combos')`, y `getData('data_scatter')`.
  - Los datos son filtrados y renderizados en los modales correspondientes.
  - El gráfico de dispersión se inicializa con datos obtenidos de `getData('data_scatter')`.

Este archivo es parte del frontend de un sistema WMS, donde la lógica de interfaz interactúa con el backend a través de funciones que obtienen y manipulan datos para su visualización en los modales y gráficos.


---

## Archivo: ./static/js/analytics_studio_config.js

### Resumen Funcional
Este archivo define un módulo para gestionar el estado visual de gráficos en una aplicación de análisis. Permite obtener y establecer el estado visual de diferentes consultas, así como mantener mapeos predefinidos para inicializar gráficos con configuraciones específicas.

### Catálogo de Funciones y Clases
- `AnalyticsStudioManager.getVisualState(queryId)` - Obtiene el estado visual asociado a una consulta específica.
- `AnalyticsStudioManager.setVisualState(queryId, state)` - Establece el estado visual para una consulta específica.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `studioChartInstance` - Instancia del gráfico actual.
- `currentSchema` - Esquema actual (no se usa en este fragmento).
- `currentQueryId` - ID de la consulta actual.
- `serverVisualState` - Estado visual del servidor (no se usa en este fragmento).
- `visualState` - Puntero al estado activo del modal.

### Dependencias y Flujo
- No depende de ninguna librería externa.
- Este archivo no importa a otros archivos ni es importado por otros archivos.


---

## Archivo: ./static/js/analytics_studio_renderer.js

### Resumen Funcional
La función `renderPreviewChart` se encarga de renderizar un gráfico o tabla en el navegador basado en los datos proporcionados. El tipo de visualización (gráfico, tabla, KPI) y sus configuraciones son determinadas por parámetros del usuario.

### Catálogo de Funciones y Clases
- `renderPreviewChart(payload)` - Renderiza un gráfico o tabla según el tipo de dato proporcionado en `payload`.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `studioChartInstance` - Variable global que almacena la instancia actual del gráfico renderizado.

### Dependencias y Flujo
- **Dependencias**: 
  - `window.Chart` - Librería para crear gráficos.
  
- **Flujo de Datos**:
  - El archivo se importa en otros archivos JavaScript dentro del proyecto.
  - Otros archivos JavaScript pueden llamar a la función `renderPreviewChart(payload)` con los datos necesarios para renderizar el gráfico o tabla.


---

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


---

## Archivo: ./static/js/consumos.js

### Resumen Funcional
Este archivo JavaScript (`consumos.js`) es parte del sistema de monitoreo de almacén (WMS). Se encarga de manejar la interacción con el usuario, como buscar materiales por Centro de Costo (CeCo) o por lista de materiales ingresada en un textarea. También se encarga de renderizar tablas y mostrar tendencias mensuales de los materiales.

### Catálogo de Funciones y Clases
- `handlePaste(e)` - Obsoleto: Manejaba el pegado de múltiples líneas, pero ahora es obsoleto.
- `limpiarGrilla()` - Limpia la grilla y oculta el contenedor de resultados.
- `formatearDinero(valor)` - Formatea un valor numérico como dinero.
- `formatearNumero(valor)` - Formatea un valor numérico como número.
- `filterTable(tableId)` - Filtra una tabla según los valores ingresados en las celdas de filtro.
- `renderVanillaTable(tbodyId, data, columns, onRowClick = null)` - Renderiza una tabla usando JavaScript puro.
- `buscarPorCeCo()` - Busca materiales por Centro de Costo y muestra los resultados.
- `buscarPorMateriales()` - Busca materiales ingresados en un textarea y muestra los resultados.
- `abrirTendenciaMaterial(material, areaNegocio, descripcion, ceco = '')` - Abre el modal con la tendencia mensual del material.
- `cerrarTendenciaMaterial()` - Cierra el modal de tendencia.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos. Todas las consultas y operaciones se realizan a través de llamadas a la API FastAPI.

### Estado y Variables Globales
- `_tendenciaChart` - Variable global que almacena el estado del gráfico de tendencias mensuales.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas mencionadas.
- **Flujo de Datos**:
  - `consumos.js` importa y es importado por otros archivos JavaScript dentro del proyecto, pero no se especifican los detalles específicos en este fragmento.


---

## Archivo: ./static/js/core_ui.js

### Resumen Funcional
El archivo `core_ui.js` es un módulo de utilidades de interfaz de usuario compartido por todas las vistas del sistema de monitoreo de almacén (WMS). Proporciona funciones para mostrar y ocultar modales, renderizar modales de lista de materiales, poblar selectores con áreas únicas y leer datos JSON embebidos en el DOM.

### Catálogo de Funciones y Clases
- `CoreUI.openModal(id)` - Muestra un modal por su ID de elemento.
- `CoreUI.closeModal(id)` - Oculta un modal por su ID de elemento.
- `CoreUI.renderMaterialModal(opts)` - Rellena y abre un modal de lista de materiales con los ítems proporcionados.
- `CoreUI.populateAreaSelect(selectId, data, key)` - Rellena un elemento `<select>` con áreas únicas encontradas en un array de datos.
- `CoreUI.getData(id)` - Lee y parsea JSON embebido en el textContent de un elemento del DOM.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas.
- **Flujo de datos**: El archivo no importa ni es importado por otros archivos. Se utiliza directamente en el HTML a través de `<script>` tags.


---

## Archivo: ./static/js/dashboard_api.js

### Resumen Funcional
El archivo `dashboard_api.js` contiene la lógica de la API para el módulo del panel de control en un sistema de monitoreo de almacén (WMS). Define funciones para interactuar con endpoints de la API, como obtener indicadores clave de rendimiento (KPIs), datos filtrados y sincronizar los datos.

### Catálogo de Funciones y Clases
- `_fetch(url, options = {})` - Realiza una solicitud HTTP a la URL especificada con las opciones proporcionadas.
- `fetchKPIs(params)` - Obtiene KPIs basándose en los parámetros proporcionados.
- `fetchFilteredData(params)` - Obtiene datos filtrados según los parámetros proporcionados.
- `sync()` - Sincroniza los datos del almacén con el servidor.
- `checkSyncStatus()` - Verifica el estado de la sincronización actual.
- `logout()` - Cierra sesión y limpia el almacenamiento local.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- Ninguna variable global explícita está declarada en este archivo.

### Dependencias y Flujo
- **Dependencias**: `fetch` (API web para hacer solicitudes HTTP).
- **Archivos que importan a este archivo**: Ninguno.
- **Archivos que este archivo importa**: Ninguno.
- **Flujo de datos**: El flujo de datos se gestiona principalmente a través de las funciones `_fetch`, `fetchKPIs`, `fetchFilteredData`, `sync`, `checkSyncStatus` y `logout`. Los datos son solicitados y procesados en el cliente, y la interacción con el servidor se realiza mediante solicitudes HTTP.

Este archivo es una parte integral del frontend que interactúa con el backend a través de endpoints definidos para obtener y gestionar los datos necesarios para el panel de control.


---

## Archivo: ./static/js/dashboard_charts.js

### Resumen Funcional
Este archivo JavaScript (`dashboard_charts.js`) se encarga de inicializar y gestionar un gráfico de barras pilaado en el panel de control del sistema de monitoreo de almacén (WMS). El gráfico muestra datos agrupados por áreas y centros, con la capacidad de seleccionar/deseleccionar ciertas áreas o centros para mostrar u ocultar sus datos en el gráfico.

### Catálogo de Funciones y Clases
- `stackedTotalPlugin(id: string, afterDatasetsDraw: function)` - Plugin para calcular y mostrar el total acumulado en cada barra del gráfico.
  - Parámetros:
    - `id`: Identificador único del plugin.
    - `afterDatasetsDraw`: Función que se ejecuta después de dibujar los conjuntos de datos, calculando y mostrando el total acumulado.

- `initWeeklyChart(chartLabels: Array<string>, chartDatasets: Array<Object>)` - Inicializa el gráfico de barras pilaado.
  - Parámetros:
    - `chartLabels`: Etiquetas para los ejes X del gráfico.
    - `chartDatasets`: Conjuntos de datos que se mostrarán en el gráfico.

- `toggleChartSelectAll(isChecked: boolean)` - Función para seleccionar/deseleccionar todos los checkboxes relacionados con áreas y centros.
  - Parámetros:
    - `isChecked`: Valor booleano que indica si se debe seleccionar o deseleccionar todos los checkboxes.

- `updateChartVisibility()` - Actualiza la visibilidad de los conjuntos de datos del gráfico según las selecciones realizadas en los checkboxes.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `window.weeklyChart`: Variable global que almacena el objeto del gráfico inicializado.

### Dependencias y Flujo
- **Dependencias**: No se mencionan dependencias externas específicas.
- **Flujo de Datos**:
  - El archivo importa funciones y variables desde otros archivos del proyecto, pero no se muestra cómo estos archivos están estructurados o qué datos fluyen entre ellos.
  - Los eventos DOM (`DOMContentLoaded`, `change` en checkboxes) desencadenan la inicialización y actualización del gráfico.


---

## Archivo: ./static/js/dashboard_core.js

### Resumen Funcional
El archivo `dashboard_core.js` contiene funciones y métodos para renderizar filas de una tabla, ejecutar filtros en un panel de control de almacén, manejar la interacción con el usuario (como seleccionar checkboxes y ordenar tablas), generar PDFs y sincronizar datos.

### Catálogo de Funciones y Clases
- `renderTableRow(t)` - Renderiza una fila de tabla con los detalles del pedido.
- `executeFilters()` - Ejecuta los filtros aplicados por el usuario en la interfaz.
- `applyFilters()` - Aplica los filtros cuando se selecciona un checkbox o se cambia el estado de "Seleccionar todo".
- `getCheckboxValues(className)` - Obtiene los valores de los checkboxes con una clase específica.
- `toggleSelectAll(className, isChecked)` - Maneja la selección de todos los checkboxes en una categoría.
- `handleSmartCheckbox(cb, className, selectAllId, context)` - Maneja el comportamiento inteligente de los checkboxes.
- `filterTable()` - Filtra las filas de la tabla según los criterios de búsqueda ingresados por el usuario.
- `sortTable(idx)` - Ordena las filas de la tabla según una columna específica.
- `updateLogoVal(btn)` - Actualiza el valor del checkbox que indica si se debe incluir el logo en el PDF.
- `pdfSubmit(btn, frameTarget, preview)` - Envía un formulario para generar y descargar PDFs.
- `downloadBulk(action, btn)` - Genera y descarga PDFs en lote según los criterios de filtro.
- `syncData(e, onlyPoll = false)` - Inicia la sincronización de datos con el servidor y maneja el estado de carga.
- `startSyncPolling(btn)` - Comienza a sondear el estado de la sincronización.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales explícitas definidas en este archivo. Las funciones utilizan elementos del DOM para almacenar y recuperar estado, como checkboxes seleccionados y valores de entrada de usuario.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas.
- **Flujo de Datos**:
  - `dashboard_core.js` es consumido por el archivo que contiene la interfaz del usuario (no especificado en el fragmento).
  - El archivo consume funciones de `DashboardAPI`, lo que sugiere que existe un módulo separado para interactuar con el backend.
  - Los datos se obtienen a través de llamadas asíncronas (`Promise.all`) a `DashboardAPI.fetchKPIs` y `DashboardAPI.fetchFilteredData`.
  - Los resultados son utilizados para actualizar la interfaz del usuario, incluyendo la tabla de pedidos, los KPIs y las notificaciones.

Este archivo es crucial para el funcionamiento del panel de control en el sistema de monitoreo de almacén, proporcionando funcionalidades avanzadas como filtros dinámicos, generación de PDFs y sincronización de datos.


---

## Archivo: ./static/js/dashboard_saas.js

### Resumen Funcional
El archivo `dashboard_saas.js` es un componente del sistema de monitoreo de almacén (WMS) que inicializa y gestiona widgets interactivos en la interfaz de usuario. Estos widgets pueden mostrar gráficos y tablas dinámicas basadas en datos obtenidos a través de una API.

### Catálogo de Funciones y Clases
- `initSaaSWidgets(params = null)` - Inicializa los widgets SaaS, leyendo parámetros del DOM o proporcionados explícitamente.
- `renderSaaSChart(container, queryId, data)` - Renderiza un gráfico de líneas para el widget SaaS.
- `renderSaaSTrellis(container, queryId, data)` - Renderiza una trellis de gráficos para el widget SaaS.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos. Todas las operaciones de obtención de datos se realizan a través de una API (`DashboardAPI`).

### Estado y Variables Globales
- `window.saasChartInstances` - Almacena instancias de gráficos Chart.js renderizados.

### Dependencias y Flujo
- **Dependencias**: 
  - `ChartDataLabels` (plugin para Chart.js).
  - `DashboardAPI` (API personalizada para obtener datos del servidor).

- **Flujo**:
  - El archivo se carga en el DOM.
  - Al cargar, inicializa los widgets SaaS llamando a `initSaaSWidgets()`.
  - `initSaaSWidgets()` lee parámetros de filtros y solicita datos a través de la API.
  - Los datos recibidos se utilizan para renderizar gráficos o tablas en el DOM.

El flujo es unidireccional, con el archivo consumiendo datos de la API y generando contenido visual en el navegador.


---

## Archivo: ./static/js/deliveries.js

### Resumen Funcional
El archivo `deliveries.js` contiene la lógica para el monitoreo de entregas en un sistema de almacén (WMS). Implementa funciones para abrir modales con detalles de áreas, días de la semana y ubicaciones, así como controladores para cambiar entre vistas operativas e históricas. También inicializa gráficos y actualiza los KPIs según las selecciones del usuario.

### Catálogo de Funciones y Clases
- `openModalWeekday(dayName, isCurrentMonth = false)` - Abre un modal con detalles del día seleccionado.
- `openModalUbicacion(name)` - Abre un modal con detalles de la ubicación seleccionada.
- `openModalArea(name, isCurrentMonth = false)` - Abre un modal con detalles de la área seleccionada.
- `openModalUser(name)` - Abre un modal con detalles del usuario seleccionado.
- `switchVLView(view)` - Cambia entre las vistas operativas e históricas.
- `updateDeliveriesAnalytics()` - Recalcula y actualiza los KPIs y filtra los gráficos según las selecciones del usuario.
- `toggleMulti(id)` - Alterna la visibilidad de un elemento con el ID especificado.
- `toggleChartSelectAll(isChecked)` - Maneja la selección de todos los elementos en una lista de verificación.
- `handleSmartCheckbox(cb)` - Maneja la lógica inteligente para las casillas de verificación, asegurando que no se pueda seleccionar vacío.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `currentModalContext` - Almacena el contexto actual del modal (área o día de la semana).
- `window.intensidadChart` - Referencia al gráfico de intensidad de entregas.
- `window.slaTrendChart`, `window.slaAreaTrendChart`, etc. - Referencias a otros gráficos históricos.

### Dependencias y Flujo
- **Dependencias**: `core_ui.js`
- **Archivos que importan este archivo**: Ninguno
- **Archivos que este archivo importa**: Ninguno

El flujo de datos se inicia con el evento `DOMContentLoaded`, donde se inicializan los gráficos y se configuran los controladores para los modales y las vistas. Los eventos de usuario, como la selección de áreas o días, desencadenan la actualización de KPIs y filtros en los gráficos.


---

## Archivo: ./static/js/docs_explorer.js

### Resumen Funcional
El archivo `docs_explorer.js` es un componente del sistema de monitoreo de almacén (WMS) que se encarga de cargar y renderizar la estructura de documentos en un árbol visual, permitiendo expandir/colapsar carpetas y cargar el contenido de los archivos seleccionados.

### Catálogo de Funciones y Clases
- `initDocs()` - Inicializa el explorador de documentos, llamando a la API para obtener la estructura del árbol de documentos y renderizarla.
- `loadFile(path)` - Carga el contenido de un archivo específico en la vista principal.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- **Dependencias**: `fetch`, `marked` (si está disponible).
- **Flujo**:
  - El archivo se carga inicialmente (`DOMContentLoaded`).
  - Al hacer clic en la pestaña de "Docs", se ejecuta `initDocs()`.
  - `initDocs()` realiza una solicitud a `/api/docs/tree` para obtener la estructura del árbol y luego llama a `renderNodes(data, treeRoot)` para renderizarla.
  - Al seleccionar un archivo en el árbol, se ejecuta `loadFile(node.path)`, que carga el contenido del archivo en `#docs-content-view`.

El flujo de datos es unidireccional desde la API hasta el cliente y luego hacia la vista.


---

## Archivo: ./static/js/inventory.js

### Resumen Funcional
El archivo `inventory.js` contiene lógica para manejar movimientos en un sistema de monitoreo de almacén (WMS). Incluye funciones para abrir modales con información sobre ubicaciones y usuarios, así como una funcionalidad de búsqueda dinámica para mostrar el stock y historial de ubicaciones.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra mensajes en la consola.
- `parseFormattedInt(val)` - Convierte un valor a un entero formateado, eliminando caracteres no numéricos.
- `window.openModalUbicacion(name)` - Abre un modal con información sobre una ubicación específica.
- `window.openModalUserInv(name)` - Abre un modal con información sobre un usuario específico.
- `window.switchInventarioView(view)` - Cambia la vista del inventario según el tipo de visualización seleccionada.

### Interacción con Base de Datos
Ninguna. El archivo no realiza ninguna operación directa en una base de datos.

### Estado y Variables Globales
No hay variables globales explícitas definidas en este archivo.

### Dependencias y Flujo
- **Dependencias**: `core_ui.js` (provee funciones como `CoreUI.openModal`, `CoreUI.closeModal`, etc.)
- **Flujo de Datos**:
  - El archivo se carga cuando el DOM esté listo.
  - Llama a funciones de `core_ui.js` para abrir modales y renderizar contenido.
  - Realiza solicitudes AJAX al servidor para obtener datos de ubicaciones y stock, que luego se procesan y mostran en la interfaz.

Este archivo es parte del frontend de un sistema WMS, gestionando la interacción con el usuario a través de modales y búsqueda dinámica.


---

## Archivo: ./static/js/productivity_daily.js

### Resumen Funcional
Este archivo JavaScript (`productivity_daily.js`) se encarga de manejar la interacción del usuario con los gráficos y tablas diarias de productividad en el sistema de monitoreo de almacén (WMS). Permite filtrar datos por usuarios, cargar datos según una fecha seleccionada, y renderizar diferentes KPIs como gráficos de tendencia, resúmenes de actividad, baches en la productividad y un mapa de calor.

### Catálogo de Funciones y Clases
- `toggleDailyUserFilter()` - Muestra u oculta el filtro de usuarios diarios.
- `renderDailyUserCheckboxes(summary)` - Renderiza los checkboxes para filtrar por usuarios.
- `toggleAllDailyUsers()` - Selecciona/deselecciona todos los usuarios en el filtro.
- `onDailyUserCheckboxChange()` - Maneja el cambio en la selección de usuarios.
- `renderFilteredDaily()` - Renderiza los KPIs filtrados según la selección de usuarios.
- `loadProductivityData()` - Carga los datos diarios de productividad desde una API y actualiza la interfaz.
- `renderKPI1(summary)` - Renderiza el resumen de actividad diaria.
- `renderKPI2(trend)` - Renderiza la tendencia de movimientos del equipo.
- `renderKPI3(gaps)` - Renderiza los baches en la productividad.
- `renderKPI4(heatmapData)` - Renderiza el mapa de calor de productividad.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a una base de datos.

### Estado y Variables Globales
- `productivityTrendChartInst` - Instancia del gráfico de tendencia.
- `currentDailyData` - Datos diarios actuales cargados.
- `selectedDailyUsers` - Usuarios seleccionados para el filtro.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `Chart.js` (para renderizar gráficos).
  
- **Archivos del Proyecto que Importan a este Archivo**:
  - `dashboard.js` (se espera que contenga la función `switchSubTab`).

- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno.

- **Flujo de Datos**: 
  - El archivo se ejecuta cuando el DOM esté listo (`DOMContentLoaded`).
  - Se manejan eventos como cambios en los filtros y selecciones.
  - Los datos diarios se cargan a través de una llamada `fetch` a la API `/api/v1/analytics/productivity`.
  - Los KPIs se renderizan basándose en los datos recibidos.


---

## Archivo: ./static/js/productivity_modals.js

### Resumen Funcional
Este archivo contiene funciones JavaScript para abrir y cargar detalles de movimientos diarios y mensuales de usuarios en un sistema de monitoreo de almacén. Utiliza una interfaz modal para mostrar los datos y realiza solicitudes a una API para obtener los datos necesarios.

### Catálogo de Funciones y Clases
- `abrirDetalleUsuario(usuario)` - Abre el modal de movimientos diarios del usuario especificado.
- `cargarNivel2Diario(operacion)` - Carga el nivel 2 de detalles para una operación específica en el nivel 1 de los movimientos diarios.
- `volverNivel1Diario()` - Vuelve al nivel 1 de los movimientos diarios.
- `cerrarDetalleUsuario()` - Cierra el modal de movimientos diarios.
- `abrirDetalleMensualUsuario(usuario)` - Abre el modal de resumen mensual del usuario especificado.
- `cargarNivel2Mensual(operacion)` - Carga el nivel 2 de detalles para una operación específica en el nivel 1 de los movimientos mensuales.
- `volverNivel1Mensual()` - Vuelve al nivel 1 de los movimientos mensuales.
- `cerrarDetalleMensualUsuario()` - Cierra el modal de resumen mensual del usuario.

### Interacción con Base de Datos
No se utiliza ninguna base de datos directamente en este archivo. Todas las operaciones de carga de datos se realizan a través de solicitudes HTTP a una API (`/api/v1/analytics/productivity/user-movements-summary`, `/api/v1/analytics/productivity/user-movements-details`, `/api/v1/analytics/productivity/user-movements-monthly-summary`, `/api/v1/analytics/productivity/user-movements-monthly-details`).

### Estado y Variables Globales
- `currentDailyUsuario` - Almacena el usuario seleccionado para los movimientos diarios.
- `currentDailyDate` - Almacena la fecha seleccionada para los movimientos diarios.
- `currentMonthlyUsuario` - Almacena el usuario seleccionado para el resumen mensual.
- `currentMonthlyDate` - Almacena la fecha seleccionada para el resumen mensual.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas en este archivo.
- **Flujo de Datos**:
  - El archivo es consumido por HTML que contiene los elementos DOM necesarios (modales, tablas, etc.).
  - Los datos se cargan a través de solicitudes HTTP a la API FastAPI definida en el proyecto.

Este archivo no interactúa con una base de datos directamente, sino que consume datos desde una API para mostrar detalles de movimientos diarios y mensuales de usuarios en un sistema de monitoreo de almacén.


---

## Archivo: ./static/js/productivity_monthly.js

### Resumen Funcional
Este archivo contiene la lógica para renderizar y gestionar los datos de productividad mensual en un sistema de almacén. Permite filtrar por usuarios, cargar datos desde una API, y visualizar KPIs como resúmenes de actividad, gráficos de tendencias y mapas de calor.

### Catálogo de Funciones y Clases
- `toggleMonthlyUserFilter()` - Alterna la visibilidad del filtro de usuarios.
- `renderMonthlyUserCheckboxes(summary)` - Renderiza los checkboxes para filtrar por usuarios.
- `toggleAllMonthlyUsers()` - Selecciona/deselecciona todos los usuarios en el filtro.
- `onMonthlyUserCheckboxChange()` - Maneja el cambio en el estado de los checkboxes de usuario.
- `renderFilteredMonthly()` - Filtra y renderiza los KPIs según los usuarios seleccionados.
- `loadMonthlyProductivityData()` - Carga los datos de productividad mensuales desde la API.
- `renderMonthlyKPI1(summary)` - Renderiza el primer KPI (resumen de actividad).
- `renderMonthlyKPI2(shifts)` - Renderiza el segundo KPI (tendencias por turno).
- `renderMonthlyKPI3(heatmapData)` - Renderiza el tercer KPI (mapa de calor).

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `productivityMonthlyTrendChartInst` - Instancia del gráfico de tendencias mensuales.
- `currentMonthlyData` - Datos actuales de productividad mensual.
- `selectedMonthlyUsers` - Usuarios seleccionados para el filtro.

### Dependencias y Flujo
- **Dependencias**: No se mencionan librerías externas específicas en este fragmento.
- **Flujo de Datos**:
  - El archivo es consumido por HTML (no se muestra aquí).
  - Importa funciones desde otros archivos JavaScript del proyecto, pero no se detalla cuáles son estos archivos.


---

## Archivo: ./static/js/saas_engine_core.js

### Resumen Funcional
El archivo `saas_engine_core.js` es un motor SaaS V2 que se encarga de leer contenedores con la clase `.saas-widget-v2`, renderizar gráficos o KPIs según los parámetros proporcionados, y actualizarlos dinámicamente.

### Catálogo de Funciones y Clases
- `initSaaSWidgetsV2(params = null, rootElement = document)` - Inicializa los widgets SaaS V2 en el elemento raíz especificado o en todo el documento si no se proporciona ninguno. Recibe parámetros para filtrar los datos.

### Interacción con Base de Datos
- **Motor**: Ninguna.
- **Tablas y Columnas**: No hay consultas SQL explícitas ni llamadas a ORM detectadas en este archivo.

### Estado y Variables Globales
- `window.saasChartInstancesV2` - Almacena instancias de gráficos Chart.js para widgets individuales.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `ChartDataLabels` (plugin para Chart.js).
- **Archivos del Proyecto que Importan a este Archivo**:
  - Ninguno.
- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno.

El flujo de datos es el siguiente: el archivo se ejecuta al cargar la página, inicia los widgets SaaS V2 y actualiza dinámicamente sus contenidos según los parámetros proporcionados.


---

## Archivo: ./static/js/saas_engine_drilldown.js

### Resumen Funcional
El archivo `saas_engine_drilldown.js` contiene funciones para abrir y gestionar un modal de detalles con una tabla dinámica que muestra datos filtrados y ordenables. El contenido se carga a través de una API RESTful.

### Catálogo de Funciones y Clases
- `window.openDrilldownModal(queryId, segmentLabel, materialId = null)` - Abre el modal de detalles con los datos filtrados según la consulta y segmento proporcionados.
- `window.sortDrilldownTable(n)` - Ordena las filas de la tabla por la columna especificada.
- `window.filterDrilldownTable()` - Filtra las filas de la tabla según los valores ingresados en los campos de búsqueda.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos. Los datos se cargan a través de una API RESTful.

### Estado y Variables Globales
- `window.filterDrilldownTableTimer` - Variable global que almacena el temporizador para la función de filtrado.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas mencionadas.
- **Flujo de Datos**:
  - El archivo se importa en otros archivos del proyecto (consumido por ellos).
  - Otros archivos del proyecto pueden importar este archivo para usar sus funciones (`window.openDrilldownModal`, `window.sortDrilldownTable`, `window.filterDrilldownTable`).


---

## Archivo: ./static/js/sla_table.js

### Resumen Funcional
El archivo `sla_table.js` contiene funciones relacionadas con la interacción de un usuario con una tabla de auditoría de SLA (Service Level Agreement) en un sistema de monitoreo de almacén. Las funciones permiten abrir y cerrar modales para visualizar PDFs, enviar formularios y manejar estados de botones.

### Catálogo de Funciones y Clases
- `openPdfModal()` - Abre el modal para mostrar un PDF.
- `closePdfModal()` - Cierra el modal y limpia el contenido del iframe.
- `pdfSubmit(btn, frameTarget, preview)` - Envía un formulario y maneja la interacción con un botón.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas.
- **Flujo**: El archivo no importa ni es importado por otros archivos. Las funciones están disponibles globalmente a través de `window.pdfSubmit` y `window.closePdfModal`.

El flujo de datos se realiza a través del formulario HTML, donde el usuario interactúa con un botón que invoca la función `pdfSubmit`. Esta función envía el formulario al servidor y maneja la interacción del usuario mientras el formulario se procesa.


---

## Archivo: ./static/js/tasks.js

### Resumen Funcional
El archivo `tasks.js` contiene la lógica para inicializar y configurar gráficos de tendencias y usuarios en una interfaz web utilizando la biblioteca Chart.js. Los datos necesarios se obtienen del DOM y se utilizan para crear gráficos de líneas y barras con opciones personalizadas.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra mensajes en la consola.
- `getData(id)` - Obtiene datos JSON desde elementos del DOM.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: 
  - `Chart.js` (incluye `ChartDataLabels`)
  
- **Flujo**:
  - El archivo se ejecuta cuando el DOM esté completamente cargado (`DOMContentLoaded`).
  - Llama a `getData()` para obtener datos de los elementos del DOM.
  - Utiliza estos datos para crear gráficos con Chart.js.

### Notas Adicionales
- El código utiliza la biblioteca Chart.js para crear gráficos interactivos en el navegador.
- Los gráficos se inicializan con opciones personalizadas, incluyendo colores, fuentes y estilos específicos.


---

## Archivo: ./static/js/transporte.js

### Resumen Funcional
El archivo `transporte.js` es un script JavaScript que se encarga de cargar y mostrar datos de transporte en una interfaz web. Realiza solicitudes a una API para obtener información sobre entregas, renderiza gráficos y tablas con estos datos, y permite la búsqueda y visualización de PDFs.

### Catálogo de Funciones y Clases
- `loadData()` - Carga los datos de transporte desde la API y actualiza la interfaz.
- `getMonday(dateStr)` - Calcula la fecha del lunes correspondiente a una fecha dada.
- `updateTransporteChartGroup(group)` - Actualiza el grupo de datos para el gráfico de transporte.
- `loadPendingData()` - Carga los datos pendientes de entrega y los muestra en una tabla con detalles agrupados por mes y fecha.
- `renderChart()` - Renderiza un gráfico de líneas mostrando las entregas y bultos según el grupo seleccionado (mensual o semanal).
- `renderTable(data)` - Renderiza una tabla con los últimos 25 registros de transporte.
- `openPdfViewer(url)` - Abre un modal para visualizar un PDF.
- `closePdfViewer()` - Cierra el modal y detiene la carga del PDF.
- `searchTransporte()` - Realiza una búsqueda en tiempo real de datos de transporte según un término ingresado.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos. Todas las operaciones de lectura y escritura se realizan a través de solicitudes HTTP a la API FastAPI.

### Estado y Variables Globales
- `chartInstance` - Almacena la instancia del gráfico actual.
- `allTransporteData` - Almacena todos los datos de transporte cargados desde la API.
- `currentChartGroup` - Almacena el grupo actual seleccionado para el gráfico (mensual o semanal).
- `transporteSearchTimeout` - Almacena un temporizador para el debouncing en la búsqueda.

### Dependencias y Flujo
- **Dependencias**: 
  - `fetch` - Para hacer solicitudes HTTP.
  - `Chart.js` y `ChartDataLabels` - Para renderizar gráficos.
  
- **Flujo de Datos**:
  - El archivo se carga en el DOM (`DOMContentLoaded`).
  - Llama a `loadData()` al cargar la página.
  - `loadData()` hace una solicitud a `/api/transporte/data` para obtener los datos de transporte y luego llama a `renderChart()`, `renderTable()`, y `loadPendingData()`.
  - `loadPendingData()` hace una solicitud a `/api/transporte/pending` para obtener los datos pendientes.
  - Los eventos de clic en los elementos del DOM (como botones, encabezados de tabla) invocan funciones como `updateTransporteChartGroup()`, `openPdfViewer()`, y `closePdfViewer()`.
  - La función `searchTransporte()` se ejecuta cuando el usuario ingresa texto en un campo de búsqueda.


---

