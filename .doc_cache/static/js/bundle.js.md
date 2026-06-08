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
El archivo `bundle.js` contiene funciones JavaScript que se utilizan para actualizar y renderizar información en una interfaz de usuario web. Específicamente, maneja la carga de datos desde un servidor a través de peticiones AJAX, actualiza el contenido de tablas y elementos HTML basándose en los datos recibidos, y controla la interacción con modales y gráficos.

### Catálogo de Funciones y Clases
- `renderAlerts()` - Renderiza una tabla de alertas.
- `renderCombos(filterText)` - Renderiza una lista de combinaciones de materiales.
- `renderScatter()` - Renderiza un gráfico de dispersión.
- `openModalAlerts()` - Abre el modal de alertas y carga los datos.
- `openModalCombos()` - Abre el modal de combinaciones y carga los datos.
- `openModalScatter()` - Abre el modal de scatter y carga los datos.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `ubicTimer` - Variable global que almacena un temporizador para la actualización de datos.

### Dependencias y Flujo
Dependencias:
- `CoreUI` (vía `window.CoreUI`)
- `Chart.js`

Flujo:
1. **analytics_proyecciones.js**:
   - Carga los datos necesarios desde el almacenamiento local (`getData`) y los filtra según los criterios de búsqueda.
   - Renderiza las tablas y gráficos en función de los datos filtrados.

2. **docs_explorer.js**:
   - Llama a la API para cargar el árbol de documentos y renderiza el contenido del documento seleccionado.

3. **productivity_daily.js**:
   - No se muestra ninguna interacción con base de datos ni dependencias externas específicas en este fragmento.

El flujo general es que los componentes de la interfaz web interactúan con funciones JavaScript para cargar y mostrar datos, utilizando `fetch` para obtener información del servidor.

#### --- PARTE 7 de 8 ---

### Resumen Funcional
El archivo `bundle.js` contiene funciones y lógica relacionada con la interacción del usuario en una interfaz web de sistema de monitoreo de almacén (WMS). Permite cambiar entre diferentes pestañas, cargar datos de productividad diaria y mensual, y renderizar gráficos y tablas basados en esos datos.

### Catálogo de Funciones y Clases
- `changeProductivityDate(offset)` - Cambia la fecha seleccionada para el análisis de productividad.
- `changeProductivityMonth(offsetMonths)` - Cambia el mes seleccionado para el análisis de productividad mensual.
- `loadProductivityData()` - Carga los datos de productividad diaria y actualiza la interfaz web.
- `renderKPI1(summary)` - Renderiza el KPI 1 (resumen de movimientos diarios).
- `renderKPI2(trend)` - Renderiza el KPI 2 (tendencia de movimientos diarios).
- `renderKPI3(gaps)` - Renderiza el KPI 3 (baches en la productividad).
- `renderKPI4(heatmapData)` - Renderiza el KPI 4 (mapa de calor de productividad).

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `currentDailyData` - Almacena los datos de productividad diarios actuales.
- `selectedDailyUsers` - Lista de usuarios seleccionados para el análisis diario.
- `productivityTrendChartInst` - Instancia del gráfico de tendencia de movimientos diarios.
- `currentMonthlyData` - Almacena los datos de productividad mensuales actuales.
- `selectedMonthlyUsers` - Lista de usuarios seleccionados para el análisis mensual.
- `productivityMonthlyTrendChartInst` - Instancia del gráfico de tendencia de movimientos mensuales.

### Dependencias y Flujo
- **Dependencias Externas**: `fetch`, `Chart.js`
- **Archivos Importados**: Ninguno
- **Archivos Exportados**: Ninguno

El flujo de datos es el siguiente:
1. El usuario selecciona una pestaña (diaria o mensual).
2. Se llama a las funciones correspondientes (`changeProductivityDate`, `changeProductivityMonth`).
3. Estas funciones cargan los datos necesarios y llaman a las funciones de renderizado (`renderKPI1`, `renderKPI2`, etc.) para actualizar la interfaz web con los nuevos datos.

#### --- PARTE 8 de 8 ---

### Resumen Funcional
Este archivo JavaScript (`bundle.js`) contiene funciones para crear y actualizar tablas HTML dinámicamente basadas en datos de usuarios y sus movimientos. También incluye funciones para abrir y cerrar modales que muestran detalles diarios y mensuales de los movimientos de usuario.

### Catálogo de Funciones y Clases
- `getColor(val, max)` - Calcula un color RGB con opacidad basada en el valor proporcionado.
- `abrirDetalleUsuario(usuario)` - Abre el modal para mostrar los detalles diarios de un usuario.
- `cargarNivel2Diario(operacion)` - Carga los detalles del nivel 2 (detalles específicos) para una operación diaria.
- `volverNivel1Diario()` - Cierra el nivel 2 y vuelve al nivel 1 en el modal de movimientos diarios.
- `cerrarDetalleUsuario()` - Cierra el modal de movimientos diarios.
- `abrirDetalleMensualUsuario(usuario)` - Abre el modal para mostrar los detalles mensuales de un usuario.
- `cargarNivel2Mensual(operacion)` - Carga los detalles del nivel 2 (detalles específicos) para una operación mensual.
- `volverNivel1Mensual()` - Cierra el nivel 2 y vuelve al nivel 1 en el modal de movimientos mensuales.
- `cerrarDetalleMensualUsuario()` - Cierra el modal de movimientos mensuales.

### Interacción con Base de Datos
Ninguna. Este archivo no interactúa directamente con una base de datos. Los datos se obtienen a través de llamadas AJAX a endpoints de API (`/api/v1/analytics/productivity/user-movements-summary`, `/api/v1/analytics/productivity/user-movements-details`, etc.).

### Estado y Variables Globales
- `currentDailyUsuario` - Almacena el usuario seleccionado para los detalles diarios.
- `currentDailyDate` - Almacena la fecha seleccionada para los detalles diarios.
- `currentMonthlyUsuario` - Almacena el usuario seleccionado para los detalles mensuales.
- `currentMonthlyDate` - Almacena la fecha seleccionada para los detalles mensuales.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas específicas en este fragmento de código.
- **Flujo de Datos**:
  - El archivo `bundle.js` es consumido por otros archivos JavaScript que no se muestran aquí.
  - Los datos para las tablas y modales se obtienen a través de llamadas AJAX al backend FastAPI.

Este archivo es crucial para la interfaz de usuario del sistema, proporcionando una forma visual de interactuar con los datos de movimientos de usuarios en el sistema de monitoreo de almacén.

