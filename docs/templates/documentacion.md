# Documentación Técnica - Directorio: templates
Compilado el: 2026-05-29 00:41:03
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./templates/analytics_proyecciones.html

### Resumen Funcional
El archivo `analytics_proyecciones.html` es una plantilla HTML para la interfaz de usuario de un módulo de análisis predictivo, que muestra información sobre desplanificaciones y correlaciones entre materiales. Incluye gráficos interactivos y tablas para visualizar datos relevantes.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo HTML.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `user`: Objeto que contiene información del usuario autenticado.
- `error_msg`: Mensaje de error a mostrar en la interfaz.
- `alerts`: Lista de alertas de desplanificación.
- `scatter_data`: Datos para el gráfico de dispersión.
- `combos`: Lista de combinaciones frecuentes (Market Basket Analysis).

### Dependencias y Flujo
- **Librerías Externas**: 
  - `Chart.js` para gráficos interactivos.
- **Archivos Incluidos**:
  - `_styles.html`: Estilos CSS adicionales.
  - `_analytics_proyecciones_modals.html`: Modales adicionales.
  - `_scripts.html`: Scripts adicionales.
- **Scripts Internos**: 
  - `analytics_proyecciones.js`: Script específico para este módulo.


---

## Archivo: ./templates/dashboard.html

### Resumen Funcional
El archivo `dashboard.html` es una plantilla HTML para el panel de control del proyecto Onedrive, que muestra información sobre entregas y materiales solicitados. Incluye un encabezado con opciones de navegación, indicadores clave (KPIs) y un menú lateral.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo HTML.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `is_syncing`: Variable que indica si la sincronización está en curso.
- `user.username`: Nombre del usuario actual.
- `user.role`: Rol del usuario actual.
- `kpi_deliveries`: Número total de entregas generadas.
- `sub_del_abierta`, `sub_del_no_tratada`, `sub_del_reunido`, `sub_del_atrasado`, `sub_del_critico`: Contadores para diferentes estados de las entregas.
- `kpi_materials`: Número total de materiales solicitados.
- `sub_mat_abierta`, `sub_mat_no_tratada`, `sub_mat_reunido`, `sub_mat_atrasado`, `sub_mat_critico`: Contadores para diferentes estados de los materiales.

### Dependencias y Flujo
- **Librerías externas**: No se detectan librerías externas utilizadas.
- **Flujo hacia otros archivos**: El archivo incluye parciales HTML (`_styles.html`, `_modals.html`, `_sidebar.html`, `_table.html`, `_scripts.html`) que probablemente contienen el estilo, modales, menú lateral, tabla y scripts necesarios para la funcionalidad del panel de control.


---

## Archivo: ./templates/deliveries.html (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para la interfaz de usuario del proyecto, que incluye elementos como encabezado, botones de pestañas y scripts JavaScript para manejar el comportamiento de las pestañas y cargar datos dinámicamente.

### Catálogo de Funciones y Clases
- `switchTab(tabId, btnElement)` - Cambia la pestaña activa.
- `openNonPalletizedDetails(user, claseMov)` - Abre un modal con detalles no paletizados.
- `initTableFilters()` - Inicializa los filtros de tablas.
- `filterOTTable()` - Filtra la tabla de OTs según los criterios seleccionados.
- `filterDiscrepancyTable()` - Filtra la tabla de Discrepancias según los criterios seleccionados.
- `sortTableDiscrepancy(columnIndex)` - Ordena la tabla de Discrepancias.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - Chart.js
  - marked.js
  - Font Awesome
- Archivos JavaScript incluidos:
  - `core_ui.js`
  - `dashboard.js`
  - `saas_engine.js`
  - `deliveries.js`
  - `consumos.js`
  - `transporte.js`
- Variables JSON inyectadas dinámicamente desde el backend.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML que contiene scripts para cargar datos JSON y referencias a archivos JavaScript. También incluye varios modales parciales.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento de código.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `ots_user_confirmed`: Almacena datos del usuario confirmado.
- `ots_type_labels`: Almacena etiquetas de tipo OTS.
- `ots_type_data`: Almacena datos de tipo OTS.

### Dependencias y Flujo
- **Librerías externas**: No se mencionan librerías externas específicas en este fragmento.
- **Archivos JavaScript incluidos**:
  - `js/tasks.js`
  - `js/inventory.js`
  - `js/analytics_proyecciones.js`
  - `js/docs_explorer.js`

- **Modales parciales incluidos**:
  - `_modals.html`
  - `_deliveries_modals.html`
  - `_inventory_modals.html`
  - `_analytics_proyecciones_modals.html`
  - `_edit_query_modal.html`
  - `_quick_login_modal.html`
  - `_logout.html`

Este archivo se utiliza para cargar datos y recursos necesarios en una página web, incluyendo modales que probablemente contienen funcionalidades adicionales.


---

## Archivo: ./templates/inventory.html

### Resumen Funcional
El archivo `inventory.html` es una plantilla HTML para la interfaz de usuario del módulo de inventario. Define la estructura y el diseño de la página, incluyendo encabezados, botones de acción, gráficos y enlaces a otros módulos del sistema.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas directamente en este archivo HTML.

### Interacción con Base de Datos
No aplica. El archivo no contiene consultas SQL ni interacciones con bases de datos.

### Estado y Variables Globales
No aplica. No hay variables globales, de sesión o diccionarios quemados en el código que almacenen estado crítico.

### Dependencias y Flujo
- **Librerías externas utilizadas:**
  - `Chart.js`
  - `chartjs-plugin-datalabels`

- **Archivos JavaScript incluidos:**
  - `core_ui.js` (versión 1)
  - `saas_engine.js` (versión 3)
  - `inventory.js` (versión 11)

- **Interacción con otros archivos del proyecto:**
  - `_styles.html`
  - `_inventory_modals.html`
  - `_quick_login_modal.html`
  - `_logout.html`

Este archivo HTML es principalmente una estructura de página que utiliza plantillas Jinja2 para incluir contenido dinámico y scripts JavaScript. No realiza operaciones directas con la base de datos ni maneja variables globales significativas.


---

## Archivo: ./templates/login.html

### Resumen Funcional
El archivo `login.html` es una página de inicio de sesión para la aplicación MonitorWeb. Permite a los usuarios ingresar sus credenciales y autenticarse en el sistema.

### Catálogo de Funciones y Clases
- `handleLogin(event)` - Maneja el evento de envío del formulario de inicio de sesión, realiza la autenticación y redirige al usuario según sea necesario.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: No se utilizan librerías externas.
- **Flujo Interno**: El archivo interactúa con el backend a través de una solicitud POST a la ruta `/api/auth/login`. La respuesta del servidor es manejada para determinar si la autenticación fue exitosa o no, y en consecuencia, se redirige al usuario.


---

## Archivo: ./templates/settings.html

### Resumen Funcional
El archivo `settings.html` es una página web que permite la gestión dinámica de parámetros globales del sistema, mapeos de estados de entrega y centros de costo a áreas de negocio, así como la sincronización de feriados. La interfaz presenta tablas interactivas para editar y guardar cambios en estos elementos.

### Catálogo de Funciones y Clases
- `openPasswordModal()` - Abre el modal para cambiar la contraseña.
- `closePasswordModal()` - Cierra el modal para cambiar la contraseña.
- `changePassword()` - Maneja el cambio de contraseña, validando los campos y haciendo una solicitud a la API.
- `updateSetting(key)` - Actualiza un parámetro global en la base de datos.
- `updateStatus(code)` - Actualiza un mapeo de estado de entrega en la base de datos.
- `addStatus()` - Añade un nuevo mapeo de estado de entrega a la base de datos.
- `deleteStatus(code)` - Elimina un mapeo de estado de entrega de la base de datos.
- `updateCostCenter(code)` - Actualiza un mapeo de centro de costo a área de negocio en la base de datos.
- `addCostCenter()` - Añade un nuevo mapeo de centro de costo a área de negocio a la base de datos.
- `deleteCostCenter(code)` - Elimina un mapeo de centro de costo a área de negocio de la base de datos.
- `syncHolidays()` - Sincroniza los feriados nacionales de Chile para el año actual y el próximo.
- `addHoliday()` - Añade una nueva fecha de feriado manualmente.
- `deleteHoliday(date_str)` - Elimina una fecha de feriado de la base de datos.
- `updateQuery(id)` - No se menciona en el código proporcionado.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- `fetch` para hacer solicitudes HTTP a la API.
- `apiCall(url, method, data = null)` - Función auxiliar para manejar las solicitudes HTTP.

Flujo:
- La página interactúa con el backend a través de endpoints como `/api/auth/change-password`, `/api/settings/update`, `/api/settings/status`, etc., para realizar operaciones CRUD en los parámetros globales, mapeos y feriados.


---

## Archivo: ./templates/sla_table.html

### Resumen Funcional
El archivo `sla_table.html` es una plantilla HTML para mostrar una tabla de transacciones que cumplen con ciertos criterios, incluyendo detalles como el número de entrega, autor/creador, área de negocio, días de retraso, fecha de creación y salida de mercancias. La página también proporciona opciones para generar y descargar PDFs relacionados con cada transacción.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo HTML.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías externas utilizadas**: No hay librerías externas directamente importadas.
- **Flujo hacia otros archivos del proyecto**:
  - `partials/_styles.html`: Incluye estilos CSS adicionales.
  - `static/css/sla_table.css`: Archivo de estilo específico para esta página.
  - `partials/_modals.html`: Incluye modales adicionales.
  - `js/sla_table.js`: Script JavaScript asociado a esta página.

El archivo HTML interactúa con el backend a través de formularios que envían solicitudes POST a rutas como `/generate-pdf`, lo que implica que el backend debe manejar estas solicitudes para generar y devolver PDFs.


---

