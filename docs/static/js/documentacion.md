# Documentación Técnica - Directorio: static/js
Compilado el: 2026-06-07 12:50:47
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

## Archivo: ./static/js/bundle.js (Procesado en 8 partes)

#### --- PARTE 1 de 8 ---

### Resumen Funcional
El archivo `bundle.js` contiene módulos de utilidades para la interfaz de usuario (UI) y lógica del backend para un sistema de monitoreo de almacén (WMS). Incluye funciones para manejar modales, renderizar materiales, llenar selectores con áreas, leer datos JSON embebidos en el DOM, así como funciones de API para interactuar con el backend.

### Catálogo de Funciones y Clases
- `CoreUI.openModal(id)` - Muestra un modal por su ID.
- `CoreUI.closeModal(id)` - Oculta un modal por su ID.
- `CoreUI.renderMaterialModal(opts)` - Rellena y abre un modal con una lista de materiales.
- `CoreUI.populateAreaSelect(selectId, data, key)` - Llena un `<select>` con áreas únicas de un array.
- `CoreUI.getData(id)` - Lee y parsea JSON embebido en el DOM.
- `DashboardAPI._fetch(url, options)` - Realiza una solicitud HTTP a la API.
- `DashboardAPI.fetchKPIs(params)` - Obtiene indicadores clave del negocio (KPIs).
- `DashboardAPI.fetchFilteredData(params)` - Obtiene datos filtrados.
- `DashboardAPI.sync()` - Sincroniza los datos con el backend.
- `DashboardAPI.checkSyncStatus()` - Verifica el estado de la sincronización.
- `DashboardAPI.logout()` - Cierra sesión y limpia el almacenamiento local.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `window.CoreUI` - Objeto que expone funciones comunes para la UI.
- `window.openModal`, `window.closeModal` - Aliases globales para compatibilidad con handlers inline.

### Dependencias y Flujo
- **Dependencias Externas**: `fetch`
- **Archivos Importados**: Ninguno
- **Archivos Exportados**: `bundle.js` es importado por otros archivos del proyecto, como `_logout.html`, `dashboard_core.js`, etc.

#### --- PARTE 2 de 8 ---

### Resumen Funcional
El archivo `bundle.js` contiene funciones para renderizar gráficos de líneas y trellis en un sistema de monitoreo de almacén. Utiliza Chart.js para crear visualizaciones dinámicas basadas en datos proporcionados.

### Catálogo de Funciones y Clases
- `renderSaaSChart(container, queryId, data)` - Renderiza un gráfico de líneas.
- `renderSaaSTrellis(container, queryId, data)` - Renderiza una grilla de gráficos trellis.
- `initSaaSWidgets(params = null, rootElement = document)` - Inicializa widgets SaaS en el DOM.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `window.saasChartInstances` - Almacena instancias de gráficos Chart.js.
- `window.saasChartInstancesV2` - Almacena instancias de gráficos Chart.js para la versión 2.

### Dependencias y Flujo
- **Dependencias Externas**: `Chart.js`, `ChartDataLabels`
- **Archivos Importados**: No se importan archivos adicionales.
- **Archivos Exportados**: No se exportan funciones adicionales.

**Flujo de Datos**:
1. `initSaaSWidgets` es llamado al cargar el DOM.
2. Busca elementos con la clase `.saas-widget-v2`.
3. Para cada widget, llama a `renderSaaSChart` o `renderSaaSTrellis` según los datos proporcionados.
4. Los gráficos se renderizan en los contenedores correspondientes.

**Flujo de Datos (Continuación)**:
- `renderSaaSChart` y `renderSaaSTrellis` procesan los datos y crean instancias de Chart.js para renderizar los gráficos.
- Los gráficos se actualizan dinámicamente según los parámetros proporcionados en `initSaaSWidgets`.

**Flujo de Datos (Continuación)**:
- Los widgets pueden interactuar con el usuario a través de eventos como clics, que pueden abrir modales o cargar datos adicionales.

#### --- PARTE 3 de 8 ---

### Resumen Funcional
El archivo `bundle.js` contiene funciones JavaScript que se utilizan para inicializar widgets de monitoreo en un sistema de almacén (WMS). Incluye la actualización de valores en el DOM, carga de sugerencias de reabastecimiento y manejo de modales con detalles específicos.

### Catálogo de Funciones y Clases
- `initSaaSWidgetsV2(queryId)` - Inicializa widgets V2 basados en el ID de la consulta.
- `loadReplenishmentSuggestions(freq='all')` - Carga sugerencias de reabastecimiento en función de la frecuencia seleccionada.
- `openDrilldownModal(queryId, segmentLabel, materialId=null)` - Abre un modal con detalles de drill-down para una consulta específica.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `window.initSaaSWidgetsV2` - Función global que inicializa widgets V2.
- `window.loadReplenishmentSuggestions` - Función global que carga sugerencias de reabastecimiento.
- `window.openDrilldownModal` - Función global para abrir modales de drill-down.

### Dependencias y Flujo
- **Dependencias Externas**: No se mencionan dependencias externas específicas en el fragmento proporcionado.
- **Archivos Importados**: No hay importaciones de archivos dentro del fragmento proporcionado.
- **Archivos Exportados**: El archivo no exporta ninguna función o variable.

El flujo de datos es principalmente entre funciones y el DOM, con llamadas a APIs para cargar datos.

#### --- PARTE 4 de 8 ---

### Resumen Funcional
Este archivo JavaScript (`bundle.js`) contiene lógica para cargar y mostrar datos en una interfaz web, utilizando funciones como `fetch` para obtener datos de un servidor, manipular el DOM para actualizar la vista y renderizar tablas con información sobre materiales y entregas.

### Catálogo de Funciones y Clases
- **getData(id)** - Obtiene datos desde el almacenamiento local.
- **openModalArea(name, isCurrentMonth = false)** - Abre un modal con detalles de una área.
- **openModalWeekday(dayName, isCurrentMonth = false)** - Abre un modal con detalles de un día.
- **openModalUbicacion(name)** - Abre un modal con detalles de ubicaciones.
- **openModalUser(name)** - Abre un modal con detalles de usuarios.
- **switchVLView(view)** - Cambia la vista entre operativa y histórica.
- **toggleMulti(id)** - Alterna la visibilidad de elementos.
- **updateDeliveriesAnalytics()** - Actualiza los KPIs y filtra listas según selección.
- **toggleChartSelectAll(isChecked)** - Maneja el estado del checkbox "Seleccionar todo".
- **handleSmartCheckbox(cb)** - Maneja la lógica inteligente de los checkboxes.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- `currentModalContext` - Almacena el contexto actual del modal.
- `window.slaTrendChart`, `window.slaAreaTrendChart`, etc. - Referencias a gráficos que se redibujan en ciertas acciones.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas mencionadas directamente en el código proporcionado.
- **Flujo de Datos**: El flujo de datos comienza con una solicitud `fetch` para obtener datos, luego se procesan y renderizan en la interfaz web. Los eventos como clics en checkboxes o botones desencadenan funciones que actualizan el estado y la vista.

#### --- PARTE 5 de 8 ---

### Resumen Funcional
El archivo `bundle.js` contiene funciones y lógica para manejar la visualización de gráficos, tablas y modales en un sistema de monitoreo de almacén (WMS). Incluye funcionalidades para cargar datos desde una API, renderizar gráficos utilizando Chart.js, gestionar el estado del usuario y mostrar información detallada en modales.

### Catálogo de Funciones y Clases
- `cerrarTendenciaMaterial()` - Cierra un modal de tendencia de material.
- `loadData()` - Carga datos de transporte desde una API y los renderiza en gráficos y tablas.
- `getMonday(dateStr)` - Calcula la fecha del lunes correspondiente a una fecha dada.
- `updateTransporteChartGroup(group)` - Actualiza el grupo de datos para el gráfico de transporte.
- `loadPendingData()` - Carga y muestra los datos pendientes de entrega en una tabla con agrupación por mes y fecha.
- `renderChart()` - Renderiza un gráfico de líneas utilizando Chart.js.
- `renderTable(data)` - Renderiza una tabla con los últimos 25 registros de transporte.
- `openPdfViewer(url)` - Abre un modal para visualizar un PDF.
- `closePdfViewer()` - Cierra el modal del PDF.
- `searchTransporte()` - Realiza una búsqueda en tiempo real de datos de transporte y muestra los resultados.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `_tendenciaChart` - Variable global que almacena la instancia del gráfico de tendencia.
- `chartInstance` - Variable global que almacena la instancia del gráfico de transporte.
- `allTransporteData` - Array global que almacena los datos de transporte cargados desde la API.
- `currentChartGroup` - Variable global que almacena el grupo actual de datos para el gráfico de transporte.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `fetch` (API web para hacer solicitudes HTTP)
  - `Chart.js` (biblioteca para renderizar gráficos)

- **Archivos del Proyecto que Importan a este Archivo**:
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa**:
  - `transporte.js`
  - `tasks.js`
  - `inventory.js`

- **Flujo de Datos**: 
  - El archivo se carga en el navegador y ejecuta las funciones necesarias para cargar y mostrar datos.
  - Los datos son cargados desde una API utilizando `fetch`.
  - Los datos son procesados y renderizados en gráficos y tablas utilizando Chart.js y DOM manipulation.

#### --- PARTE 6 de 8 ---

### Resumen Funcional
El archivo `bundle.js` contiene funciones JavaScript que se utilizan en un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. El script realiza operaciones como la carga de datos desde una API, el procesamiento de estos datos y la actualización del contenido de las páginas web.

### Catálogo de Funciones y Clases
- `toggleDailyUserFilter()` - Alterna la visibilidad del filtro de usuarios diarios.
- `renderDailyUserCheckboxes(summary)` - Renderiza los checkboxes para seleccionar usuarios diarios.
- `toggleAllDailyUsers()` - Selecciona/deselecciona todos los usuarios diarios.
- `onDailyUserCheckboxChange()` - Maneja el cambio en la selección de usuarios diarios.
- `renderFilteredDaily()` - Renderiza los KPIs filtrados según los usuarios seleccionados.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `productivityTrendChartInst` - Instancia del gráfico de tendencias de productividad.
- `currentDailyData` - Datos actuales de productividad.
- `selectedDailyUsers` - Usuarios diarios seleccionados.

### Dependencias y Flujo
- Depende de librerías como `marked` para el procesamiento de markdown.
- Importa funciones desde otros archivos JavaScript (`analytics_proyecciones.js`, `docs_explorer.js`, `productivity_daily.js`).
- Exporta funciones globales para ser utilizadas en otros scripts.

#### --- PARTE 7 de 8 ---

### Resumen Funcional
El archivo `bundle.js` contiene funciones para cargar y renderizar datos de productividad diaria y mensual en un sistema de monitoreo de almacén (WMS). Utiliza una interfaz de usuario con elementos como tablas, gráficos y modales para mostrar estadísticas detalladas.

### Catálogo de Funciones y Clases
- `renderDailyUserCheckboxes(summary)` - Renderiza los checkboxes para filtrar usuarios diarios.
- `renderFilteredDaily()` - Filtra y renderiza datos diarios según el usuario seleccionado.
- `renderKPI1(summary)` - Renderiza la KPI 1 (Productividad Diaria) en una tabla con barras de progreso.
- `renderKPI2(trend)` - Renderiza la KPI 2 (Tendencia Productiva) en un gráfico de líneas.
- `renderKPI3(gaps)` - Renderiza la KPI 3 (Baches en Productividad) en una lista de tarjetas.
- `renderKPI4(heatmapData)` - Renderiza la KPI 4 (Mapa de Calor de Productividad) en una tabla.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `currentDailyData` - Almacena los datos diarios actuales.
- `productivityTrendChartInst` - Instancia del gráfico de tendencia productiva mensual.
- `selectedMonthlyUsers` - Lista de usuarios seleccionados para el filtrado mensual.

### Dependencias y Flujo
Dependencias:
- `fetch` - Para hacer solicitudes HTTP.
- `Chart.js` - Para renderizar gráficos.

Flujo:
- `bundle.js` importa funciones desde otros archivos (`productivity_monthly.js`, `productivity_modals.js`).
- Otros archivos importan `bundle.js`.

El flujo de datos es unidireccional, con `bundle.js` consumiendo datos y renderizando la interfaz de usuario.

#### --- PARTE 8 de 8 ---

### Resumen Funcional
El archivo `bundle.js` contiene funciones JavaScript que gestionan la interacción del usuario con el sistema de monitoreo de almacén, permitiendo ver resúmenes diarios y mensuales de movimientos de productos por usuarios.

### Catálogo de Funciones y Clases
- `cargarNivel2Diario(operacion)` - Carga los detalles de una operación diaria.
- `volverNivel1Diario()` - Vuelve al nivel 1 del detalle diario.
- `cerrarDetalleUsuario()` - Cierra el modal de movimientos diarios.
- `abrirDetalleMensualUsuario(usuario)` - Abre el modal de resumen mensual de movimientos por usuario.
- `cargarNivel2Mensual(operacion)` - Carga los detalles de una operación mensual.
- `volverNivel1Mensual()` - Vuelve al nivel 1 del detalle mensual.
- `cerrarDetalleMensualUsuario()` - Cierra el modal de movimientos mensuales.

### Interacción con Base de Datos
Ninguna. El archivo no realiza ninguna interacción directa con una base de datos.

### Estado y Variables Globales
- `currentDailyDate` - Almacena la fecha actual para los detalles diarios.
- `currentDailyUsuario` - Almacena el usuario actual para los detalles diarios.
- `currentMonthlyDate` - Almacena la fecha actual para los detalles mensuales.
- `currentMonthlyUsuario` - Almacena el usuario actual para los detalles mensuales.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas.
- **Flujo de Datos**:
  - El archivo es consumido por HTML que muestra modales y tablas interactivas.
  - Los datos son solicitados a través de llamadas `fetch` a endpoints definidos en el backend (FastAPI).
  - Los datos recibidos se procesan y mostrados en la interfaz del usuario.


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

## Archivo: ./static/js/saas_engine_core.js (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `saas_engine_core.js` es un script que inicializa widgets de gráficos y KPIs en una interfaz web, utilizando datos obtenidos a través de una API. Los widgets pueden mostrar diferentes tipos de gráficos (lineales, trellis, etc.) basándose en los parámetros proporcionados.

### Catálogo de Funciones y Clases
- `initSaaSWidgetsV2(params = null, rootElement = document)` - Inicializa los widgets SaaS V2.
- `loadReplenishmentSuggestions(freq = 'all')` - Carga sugerencias de abastecimiento en una tabla.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- `window.saasChartInstancesV2` - Almacena instancias de gráficos Chart.js para widgets trellis.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `fetch` (API web para hacer solicitudes HTTP).
  - `ChartDataLabels` (plugin para Chart.js que permite mostrar etiquetas en los gráficos).

- **Archivos del Proyecto Importados**:
  - Ninguno.

- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno.

- **Flujo de Datos**: 
  - El archivo se ejecuta al cargar el DOM (`DOMContentLoaded`).
  - Llama a `initSaaSWidgetsV2()` y `loadReplenishmentSuggestions()` con un pequeño retraso.
  - Los widgets son inicializados y actualizados según los parámetros proporcionados.

El flujo de datos es unidireccional, desde el archivo hasta la interfaz web y viceversa para las interacciones del usuario.


---

## Archivo: ./static/js/saas_engine_drilldown.js

### Resumen Funcional
El archivo `saas_engine_drilldown.js` contiene funciones para abrir modales de detalles y cargar tablas dinámicas con datos desde una API. Los modales incluyen detalles de materiales, áreas de negocio y estadísticas relacionadas.

### Catálogo de Funciones y Clases
- `window.openDrilldownModal(queryId, segmentLabel, materialId = null)` - Abre el modal de detalles para un área o material específico.
- `window.sortDrilldownTable(n)` - Ordena la tabla de detalles por una columna específica.
- `window.filterDrilldownTable()` - Filtra los datos de la tabla según los valores ingresados en los campos de búsqueda.
- `window.openCmv201Modal()` - Abre el modal para mostrar resúmenes de CMV 201.
- `window.loadCmv201Data(planType)` - Carga los datos del resumen de CMV 201 según el tipo de planificación seleccionado.
- `window.openCmv201AreaDetails(area)` - Abre el modal para mostrar detalles específicos de una área en CMV 201.
- `window.backToCmv201Summary()` - Vuelve al resumen general de CMV 201.
- `window.onCmv201MonthChange()` - Maneja el cambio de mes seleccionado en los modales de CMV 201 y CMV 261.
- `window.loadCmv201AreaDetails()` - Carga los detalles específicos de una área en CMV 201 según el mes seleccionado.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos. Los datos se cargan a través de llamadas a la API FastAPI.

### Estado y Variables Globales
- `window.currentCmv201PlanType` - Almacena el tipo de planificación seleccionado para CMV 201.
- `window.currentCmv201Area` - Almacena el área de negocio seleccionada en los modales de CMV 201 y CMV 261.
- `window.cmv201MonthsAvailable` - Almacena los meses disponibles para la visualización en los modales de CMV 201 y CMV 261.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas específicas.
- **Flujo de Datos**:
  - `saas_engine_drilldown.js` importa y es importado por otros archivos JavaScript dentro del proyecto, pero no hay intercambio explícito de datos entre ellos.


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

