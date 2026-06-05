# Documentación Técnica - Directorio: templates
Compilado el: 2026-06-05 03:03:51
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./templates/analytics_proyecciones.html

### Resumen Funcional
El archivo `analytics_proyecciones.html` es una plantilla HTML para la interfaz de usuario del módulo de análisis predictivo en el Sistema de Monitoreo de Almacén (WMS). Muestra información sobre alertas de desplanificación, un gráfico de dispersión y analisis de market basket.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada directamente en este archivo HTML. Todas las interacciones son a través de JavaScript y llamadas a funciones definidas en otros archivos.

### Interacción con Base de Datos
Ninguna. El archivo no contiene consultas SQL ni interacciones con una base de datos.

### Estado y Variables Globales
- `user`: Objeto que contiene información del usuario actual.
- `error_msg`: Mensaje de error a mostrar en la interfaz.
- `alerts`: Lista de alertas de desplanificación.
- `scatter_data`: Datos para el gráfico de dispersión.
- `combos`: Datos para el análisis de market basket.

### Dependencias y Flujo
- **Dependencias**: 
  - Chart.js: Para renderizar gráficos.
  
- **Archivos Importados**:
  - `_styles.html`: Archivo que contiene estilos CSS.
  - `analytics_proyecciones.css`: Hoja de estilo específica para esta página.
  - `_scripts.html`: Archivo que contiene scripts JavaScript generales.
  - `analytics_proyecciones.js`: Script específico para esta página.

- **Archivos Exporados**:
  - No se exportan funciones o clases desde este archivo HTML. Todas las interacciones son a través de eventos y llamadas a funciones en otros archivos JavaScript.

El flujo de datos es principalmente hacia la interfaz del usuario, donde los datos JSON (`data_scatter`, `data_alerts`, `data_combos`) son utilizados para alimentar gráficos y tablas.


---

## Archivo: ./templates/dashboard.html

### Resumen Funcional
El archivo `dashboard.html` es una plantilla HTML para el panel de control del sistema de monitoreo de almacén (WMS). Contiene la interfaz de usuario principal que incluye encabezado, indicadores clave (KPIs), menú de acciones y contenido principal dividido en sidebar y tabla.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada directamente en este archivo HTML. Todas las interacciones son realizadas a través de JavaScript y eventos del usuario.

### Interacción con Base de Datos
Ninguna. El archivo no contiene consultas SQL ni llamadas a ORM para interactuar con una base de datos.

### Estado y Variables Globales
- `is_syncing`: Variable que indica si la sincronización está en curso.
- `user`: Objeto que contiene información del usuario autenticado, incluyendo su nombre de usuario y rol.
- `kpi_deliveries`, `sub_del_abierta`, `sub_del_no_tratada`, `sub_del_reunido`, `sub_del_atrasado`, `sub_del_critico`: Variables que almacenan los valores de KPIs relacionados con las entregas.
- `kpi_materials`, `sub_mat_abierta`, `sub_mat_no_tratada`, `sub_mat_reunido`, `sub_mat_atrasado`, `sub_mat_critico`: Variables que almacenan los valores de KPIs relacionados con los materiales solicitados.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas directamente en este archivo.
- **Flujo de Datos**: El flujo de datos pasa por el servidor (FastAPI) que renderiza esta plantilla HTML, pasando los valores de las variables globales como contexto. Los eventos del usuario (clics en botones, cambios en la interfaz) se manejan con JavaScript.

Este archivo es una vista HTML que presenta información y permite interacciones al usuario, pero no realiza ninguna operación directamente relacionada con la base de datos o el backend del sistema.


---

## Archivo: ./templates/deliveries.html (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para la interfaz de usuario del sistema de monitoreo de almacén (WMS). Contiene el diseño y las funcionalidades necesarias para mostrar diferentes secciones como entregas, movimientos, consumos, etc., con un menú de pestañas interactiva.

### Catálogo de Funciones y Clases
- `switchTab(tabId, btnElement)` - Cambia la pestaña activa.
- `switchSubTab(subTabId, btnElement)` - Cambia la subpestaña activa.
- `openNonPalletizedDetails(user, claseMov)` - Abre un modal con detalles no paletizados.
- `initTableFilters()` - Inicializa los filtros de tablas.
- `filterOTTable()` - Filtra la tabla de OTs según los criterios seleccionados.
- `filterDiscrepancyTable()` - Filtra la tabla de discrepancias según los criterios seleccionados.
- `sortTableDiscrepancy(columnIndex)` - Ordena la tabla de discrepancias.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
No hay variables globales explícitas definidas en el código. Las variables están almacenadas en elementos `<script type="application/json">` que contienen datos JSON serializados.

### Dependencias y Flujo
- **Librerías externas**: Chart.js, marked.js, Font Awesome.
- **Archivos del proyecto importados**:
  - `partials/_styles.html`
  - `css/deliveries.css`, `css/inventory.css`, `css/analytics_proyecciones.css`
  - `js/core_ui.js`, `js/dashboard_api.js`, `js/dashboard_core.js`, `js/dashboard_saas.js`, `js/saas_engine_core.js`, `js/saas_engine_drilldown.js`, `js/deliveries.js`, `js/consumos.js`, `js/transporte.js`
- **Archivos del proyecto que importan a este archivo**: No especificados en el fragmento.

El flujo de datos se gestiona principalmente mediante eventos JavaScript y la manipulación del DOM.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para el sistema de monitoreo de almacén (WMS). Contiene variables JSON que se utilizan en scripts JavaScript y carga varios archivos JavaScript adicionales.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `ots_trend_created`
- `ots_trend_confirmed`
- `ots_user_labels`
- `ots_user_created`
- `ots_user_confirmed`
- `ots_type_labels`
- `ots_type_data`

### Dependencias y Flujo
- Archivos JavaScript:
  - `js/tasks.js` (versión 5)
  - `js/inventory.js` (versión 21)
  - `js/analytics_proyecciones.js` (versión 3)
  - `js/docs_explorer.js` (versión 5)
  - `js/productivity_daily.js` (versión 2)
  - `js/productivity_monthly.js` (versión 2)
  - `js/productivity_modals.js` (versión 2)

- Archivos HTML incluidos:
  - `_modals.html`
  - `_deliveries_modals.html`
  - `_inventory_modals.html`
  - `_analytics_proyecciones_modals.html`
  - `_edit_query_modal.html`
  - `_quick_login_modal.html`
  - `_logout.html`

El archivo `deliveries.html` carga varios scripts JavaScript y partials HTML, lo que indica un flujo de datos hacia el cliente para la visualización y interacción con los datos del sistema de almacén.


---

## Archivo: ./templates/inventory.html

### Resumen Funcional
El archivo `inventory.html` es una plantilla HTML para la página de análisis del inventario en el sistema de monitoreo de almacén (WMS). Muestra gráficos y KPIs relacionados con las entradas, consumos, traspasos y otras métricas del inventario.

### Catálogo de Funciones y Clases
Ninguna.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `Chart.js`
  - `chartjs-plugin-datalabels`

- **Archivos del Proyecto Importados**:
  - `partials/_styles.html`
  - `css/inventory.css`
  - `partials/_inventory_modals.html`
  - `js/core_ui.js`
  - `js/saas_engine_core.js`
  - `js/saas_engine_drilldown.js`
  - `js/inventory.js`
  - `partials/_quick_login_modal.html`
  - `partials/_logout.html`

- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno.

El flujo de datos se realiza principalmente a través de la carga de scripts y estilos, así como el consumo de variables globales y funciones JavaScript definidas en los archivos importados.


---

## Archivo: ./templates/login.html

### Resumen Funcional
El archivo `login.html` es una página de inicio de sesión para el sistema de monitoreo de almacén (WMS). Permite a los usuarios ingresar sus credenciales y autenticarse en la aplicación.

### Catálogo de Funciones y Clases
- **handleLogin(event)** - Maneja el evento de envío del formulario de inicio de sesión, realiza una solicitud POST a la API para autenticar al usuario y maneja la respuesta.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- **localStorage** - Se utilizan variables globales en el almacenamiento local del navegador para guardar el token de acceso, nombre de usuario y rol del usuario autenticado.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas mencionadas.
- **Flujo**: El archivo `login.html` se importa por la vista correspondiente en FastAPI. La función `handleLogin` es llamada cuando el formulario de inicio de sesión se envía, lo que desencadena una solicitud POST a `/api/auth/login`. La respuesta del servidor maneja la autenticación y redirige al usuario según sea necesario.


---

## Archivo: ./templates/settings.html

### Resumen Funcional
El archivo `settings.html` es una página web que permite la gestión dinámica de parámetros globales del sistema WMS, incluyendo mapeos de estados de entrega, centros de costo a áreas de negocio, calendario de feriados y opciones de exportación de datos. La interfaz permite editar valores, guardar cambios, agregar y eliminar registros, así como sincronizar datos.

### Catálogo de Funciones y Clases
- `openPasswordModal()` - Abre el modal para cambiar la contraseña.
- `closePasswordModal()` - Cierra el modal para cambiar la contraseña.
- `changePassword()` - Maneja el cambio de contraseña a través de una API.
- `updateSetting(key)` - Actualiza un parámetro global.
- `updateStatus(code)` - Actualiza un mapeo de estado de entrega.
- `addStatus()` - Añade un nuevo mapeo de estado de entrega.
- `deleteStatus(code)` - Elimina un mapeo de estado de entrega.
- `updateCostCenter(code)` - Actualiza un mapeo de centro de costo a área de negocio.
- `addCostCenter()` - Añade un nuevo mapeo de centro de costo a área de negocio.
- `deleteCostCenter(code)` - Elimina un mapeo de centro de costo a área de negocio.
- `syncHolidays()` - Sincroniza los feriados nacionales de Chile.
- `addHoliday()` - Añade una nueva fecha de feriado manual.
- `deleteHoliday(date_str)` - Elimina una fecha de feriado manual.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas SQL ni interactúa directamente con la base de datos.

### Estado y Variables Globales
No hay variables globales explícitas definidas en el código.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas específicas.
- **Archivos del Proyecto Importados**:
  - `partials/_styles.html` - Estilos CSS adicionales.
  - `partials/_logout.html` - Código para cerrar sesión.
- **Archivos que Importan a Este Archivo**: Ninguno.

El flujo de datos se gestiona principalmente a través de eventos de clic en botones y llamadas AJAX a endpoints definidos en el backend (FastAPI).


---

## Archivo: ./templates/sla_table.html

### Resumen Funcional
El archivo `sla_table.html` es una plantilla HTML para mostrar una tabla de transacciones que cumplen con ciertos criterios en un sistema de monitoreo de almacén (WMS). La tabla incluye detalles como el número de entrega, autor/creador, área de negocio, días de retraso, fecha de creación y salida, y material involucrado. Además, proporciona opciones para generar y descargar PDFs relacionados con cada transacción.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías externas**: No se mencionan librerías externas específicas.
- **Archivos del proyecto que IMPORTA (consume)**: `partials/_styles.html`, `sla_table.css`, `_modals.html`, `sla_table.js`.
- **Archivos del proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno
- **Dirección del flujo de datos**: El archivo se renderiza en el navegador y no interactúa directamente con la base de datos o servicios externos.


---

