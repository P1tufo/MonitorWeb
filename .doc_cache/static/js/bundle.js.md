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

