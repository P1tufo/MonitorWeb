# Documentación Técnica - Directorio: templates
Compilado el: 2026-05-23 00:11:14
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./templates/analytics_proyecciones.html

### Resumen Funcional
El archivo `analytics_proyecciones.html` es una plantilla HTML para la interfaz de usuario de un módulo de análisis predictivo, que muestra información sobre desplanificaciones y predicciones de demanda. Incluye gráficos interactivos y tablas para visualizar datos relevantes.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo HTML.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `user.username`: Almacena el nombre de usuario actual.
- `error_msg`: Almacena un mensaje de error si ocurre algún problema.
- `alerts`: Lista de alertas de desplanificación.
- `scatter_data`: Datos para el gráfico de dispersión "Frecuencia vs Volumen".
- `combos`: Datos para la visualización de combinaciones frecuentes (Market Basket Analysis).

### Dependencias y Flujo
- **Librerías Externas**: 
  - `Chart.js` para crear gráficos interactivos.
- **Archivos del Proyecto**:
  - `_styles.html`: Incluye estilos CSS adicionales.
  - `_analytics_proyecciones_modals.html`: Contiene modales adicionales.
  - `_scripts.html`: Incluye scripts adicionales.
  - `analytics_proyecciones.js`: Script personalizado para el módulo de análisis predictivo.


---

## Archivo: ./templates/dashboard.html

### Resumen Funcional
El archivo `dashboard.html` es una plantilla HTML para el panel de control del proyecto Onedrive, que muestra indicadores clave (KPIs) y proporciona acceso a diferentes módulos y funciones.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo. Todo el contenido es estructura HTML y Jinja2 templating.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `is_syncing`: Variable que indica si la sincronización está en curso.
- `user.username`: Nombre del usuario actual.
- `user.role`: Rol del usuario actual.
- `kpi_deliveries`: Número total de entregas generadas.
- `sub_del_abierta`, `sub_del_no_tratada`, `sub_del_reunido`, `sub_del_atrasado`, `sub_del_critico`: Contadores para diferentes estados de entregas.
- `kpi_materials`: Número total de materiales solicitados.
- `sub_mat_abierta`, `sub_mat_no_tratada`, `sub_mat_reunido`, `sub_mat_atrasado`, `sub_mat_critico`: Contadores para diferentes estados de materiales.

### Dependencias y Flujo
- **Librerías externas**: No se detectan librerías externas específicas.
- **Flujo interno**: El archivo incluye varios parciales HTML (`_styles.html`, `_modals.html`, `_sidebar.html`, `_table.html`, `_scripts.html`) que probablemente contienen el contenido específico para estos elementos.


---

## Archivo: ./templates/deliveries.html (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para la interfaz de usuario del proyecto, que incluye elementos como encabezados, botones de pestañas y scripts JavaScript para manejar el comportamiento de las pestañas y cargar datos dinámicamente.

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
- **Librerías externas**: 
  - Chart.js
  - Chartjs-plugin-datalabels
  - Font Awesome
  - marked
- **Archivos JavaScript**:
  - `core_ui.js`
  - `deliveries.js`
  - `inventory.js`
  - `analytics_proyecciones.js`
  - `docs_explorer.js`
- **Archivos CSS**:
  - Estilos definidos en el archivo y referencias a archivos externos
- **Datos JSON**: 
  - Datos inyectados desde variables de contexto del servidor (por ejemplo, `area_stats_json`, `weekdays`, etc.)


---

## Archivo: ./templates/inventory.html

### Resumen Funcional
El archivo `inventory.html` es una plantilla HTML para la interfaz de usuario del módulo de inventario, que muestra análisis y gráficos relacionados con las entradas, consumos y traspasos de materiales.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo. Todo el contenido es estructura HTML y JavaScript.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `user.username`: Nombre del usuario actual.
- `kpi_ingresos`: Total de ingresos.
- `kpi_consumos_prod`: Consumo de producción.
- `kpi_consumos_mant`: Consumo de mantenimiento.
- `rate_reabast`: Tasa de reabastecimiento.
- `kpi_traspasos`: Número de traspasos.
- `rate_devolucion`: Tasa de devoluciones.
- `kpi_devoluciones`: Cantidad de devoluciones.
- `volumen_data`: Datos de volumen.
- `area_stats_json`: Estadísticas por área.
- `trend_labels`: Etiquetas para gráficos de tendencia.
- `trend_entradas`: Datos de entradas para gráficos de tendencia.
- `trend_salidas_prod`: Datos de salidas de producción para gráficos de tendencia.
- `trend_salidas_mant`: Datos de salidas de mantenimiento para gráficos de tendencia.
- `abc_counts`: Conteo de elementos ABC.
- `abc_mapping`: Mapeo de elementos ABC.
- `kpi_consumos_prod`: Consumo de producción (repetido).
- `kpi_consumos_mant`: Consumo de mantenimiento (repetido).
- `dow_distribution`: Distribución diaria.
- `ubicaciones_mapping`: Mapeo de ubicaciones.
- `area_material_mapping`: Mapeo de materiales por área.
- `user_material_mapping`: Mapeo de materiales por usuario.
- `dow_material_mapping`: Mapeo de materiales por distribución diaria.
- `pm_material_mapping`: Mapeo de materiales para producción vs mantenimiento.

### Dependencias y Flujo
- **Librerías externas**: 
  - Chart.js
  - Chartjs-plugin-datalabels

- **Archivos JavaScript**:
  - `core_ui.js`
  - `inventory.js`

- **Modales y parciales HTML incluidos**:
  - `_styles.html`
  - `_inventory_modals.html`
  - `_quick_login_modal.html`
  - `_logout.html`


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

