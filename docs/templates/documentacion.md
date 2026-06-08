# Documentación Técnica - Directorio: templates
Compilado el: 2026-06-07 18:34:58
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
El archivo `dashboard.html` es una plantilla HTML para el panel de control del sistema de monitoreo de almacén (WMS). Contiene la interfaz de usuario principal que incluye encabezado, indicadores clave (KPIs), menú lateral y tabla de datos.

### Catálogo de Funciones y Clases
Ninguna.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `INITIAL_USER_GROUPS`: Variable global que almacena los grupos de usuario en formato JSON.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas directamente en este archivo.
- **Archivos del Proyecto Importados**:
  - `partials/_styles.html`
  - `partials/_modals.html`
  - `partials/_sidebar.html`
  - `partials/_table.html`
  - `partials/_scripts.html`
- **Archivos que Importan a Este Archivo**: Ninguno.

El flujo de datos se realiza a través de la inclusión de parciales HTML, lo que permite modularizar el código y mantener una estructura organizada.


---

## Archivo: ./templates/deliveries.html (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para la interfaz de usuario del sistema de monitoreo de almacén (WMS). Proporciona una vista consolidada con varias secciones, como entregas, movimientos, consumos y más. Incluye funcionalidades para filtrar y ordenar datos, así como modales para detalles adicionales.

### Catálogo de Funciones y Clases
- `switchTab(tabId, btnElement)` - Cambia la pestaña activa.
- `switchSubTab(subTabId, btnElement)` - Cambia la subpestaña activa.
- `openNonPalletizedDetails(user, claseMov)` - Abre un modal con detalles no paletizados.
- `initTableFilters()` - Inicializa los filtros de tablas.
- `filterOTTable()` - Filtra la tabla de OTs según criterios seleccionados.
- `filterDiscrepancyTable()` - Filtra la tabla de discrepancias según criterios seleccionados.
- `sortTableDiscrepancy(columnIndex)` - Ordena la tabla de discrepancias.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- Variables globales no detectadas directamente en el código proporcionado.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `Chart.js`
  - `chartjs-plugin-datalabels`
  - `marked`
  - `font-awesome`

- **Archivos del Proyecto Importados**:
  - `partials/_styles.html`
  - `css/deliveries.css`, `css/inventory.css`, `css/analytics_proyecciones.css`
  - `js/bundle.js`
  - `partials/_modals.html`, `_deliveries_modals.html`, `_inventory_modals.html`, `_analytics_proyecciones_modals.html`, `_edit_query_modal.html`, `_quick_login_modal.html`, `_logout.html`

- **Archivos del Proyecto que Importan a Este Archivo**:
  - No detectados directamente en el código proporcionado.

El flujo de datos se realiza principalmente mediante JavaScript para interactuar con la interfaz y cargar datos dinámicamente.


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

## Archivo: ./templates/settings.html (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `settings.html` es una interfaz de usuario para la configuración dinámica del sistema WMS. Permite gestionar parámetros globales, mapeos de estados de entrega y centros de costo a áreas de negocio, así como grupos de usuarios y feriados.

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
- `addHoliday()` - Añade un nuevo feriado manual.
- `deleteHoliday(date_str)` - Elimina un feriado manual.
- `updateUserGroup(oldName, nameId, listId)` - Actualiza el nombre y usuarios de un grupo de usuarios.
- `addUserGroup()` - Añade un nuevo grupo de usuarios.
- `deleteUserGroup(name)` - Elimina un grupo de usuarios.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos. Todas las operaciones CRUD se realizan a través de llamadas a APIs.

### Estado y Variables Globales
No hay variables globales explícitas definidas en el código. Las variables utilizadas son principalmente para almacenar valores temporales como los valores de entrada del usuario o mensajes de toast.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas específicas.
- **Flujo de Datos**:
  - El archivo `settings.html` es consumido por el navegador del cliente.
  - Los scripts JavaScript realizan llamadas a APIs para interactuar con el backend (FastAPI).
  - Las respuestas de las API son utilizadas para actualizar la interfaz de usuario dinámicamente.

El flujo de datos va desde el frontend hacia el backend, donde se realizan operaciones CRUD y luego se reflejan los cambios en la interfaz de usuario.


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

