# Documentación Técnica - Directorio: templates
Compilado el: 2026-05-22 16:53:13
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./templates/analytics_proyecciones.html

### Resumen Funcional
El archivo `analytics_proyecciones.html` es una plantilla HTML para la interfaz de usuario de un sistema de análisis predictivo, que muestra información sobre desplanificaciones y correlaciones entre materiales. Incluye gráficos interactivos y tablas para visualizar datos relevantes.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo HTML.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: 
  - `Chart.js` para gráficos.
  
- **Archivos del Proyecto**:
  - `_styles.html`: Incluye estilos CSS.
  - `_analytics_proyecciones_modals.html`: Contiene modales interactivos.
  - `_scripts.html`: Incluye scripts JavaScript adicionales.
  - `analytics_proyecciones.js`: Script personalizado para la funcionalidad específica de esta página.


---

## Archivo: ./templates/dashboard.html

### Resumen Funcional
El archivo `dashboard.html` es una plantilla HTML para el panel de control del proyecto Onedrive, que muestra indicadores clave (KPIs) y permite navegar entre diferentes secciones de análisis.

### Catálogo de Funciones y Clases
No aplica

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `is_syncing`: Un booleano que indica si la sincronización está en curso.
- `kpi_deliveries`: Cantidad total de entregas generadas.
- `sub_del_abierta`: Cantidad de entregas en curso.
- `sub_del_no_tratada`: Cantidad de entregas no tratadas.
- `sub_del_reunido`: Cantidad de entregas reunidas a tiempo.
- `sub_del_atrasado`: Cantidad de entregas reunidas atrasadas.
- `sub_del_critico`: Cantidad de entregas críticas (OT abierta atrasada).
- `kpi_materials`: Cantidad total de materiales solicitados.
- `sub_mat_abierta`: Cantidad de picking en curso.
- `sub_mat_no_tratada`: Cantidad de pendientes por generar OT.
- `sub_mat_reunido`: Cantidad de materiales reunidos a tiempo.
- `sub_mat_atrasado`: Cantidad de materiales reunidos atrasados.
- `sub_mat_critico`: Cantidad de materiales críticos (OT abierta atrasada).
- `user.username`: Nombre de usuario actual.
- `user.role`: Rol del usuario actual.

### Dependencias y Flujo
- Utiliza plantillas parciales (`_styles.html`, `_modals.html`, `_sidebar.html`, `_table.html`, `_scripts.html`).
- No depende de ninguna librería externa específica.


---

## Archivo: ./templates/deliveries.html (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `deliveries.html` es una plantilla HTML para la interfaz de usuario del proyecto, que incluye elementos como encabezado, pestañas para diferentes secciones (Entregas, Movimientos, Gestión de OTs, IA Insomnio y Ansiedad, Documentación, Historial de Ubicaciones), y scripts JavaScript para manejar el comportamiento de las pestañas, filtros y modales.

### Catálogo de Funciones y Clases
- `switchTab(tabId, btnElement)` - Cambia la pestaña activa.
- `switchSubTab(subTabId, btnElement)` - Cambia la subpestaña activa.
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
- **Librerías externas utilizadas:**
  - Chart.js
  - Chartjs-plugin-datalabels
  - Font Awesome
  - marked

- **Archivos JavaScript incluidos:**
  - `deliveries.js`
  - `tasks.js`
  - `inventory.js`
  - `analytics_proyecciones.js`
  - `docs_explorer.js`

- **Archivos HTML parciales incluidos:**
  - `_styles.html`
  - `_tab_docs.html`
  - `_tab_historial.html`
  - `_tab_ia.html`
  - `_tab_deliveries.html`
  - `_tab_inventory.html`
  - `_tab_ots.html`
  - `_deliveries_modals.html`
  - `_inventory_modals.html`
  - `_analytics_proyecciones_modals.html`
  - `_edit_query_modal.html`
  - `_logout.html`


---

## Archivo: ./templates/inventory.html

### Resumen Funcional
El archivo `inventory.html` es una plantilla HTML para la interfaz de usuario del módulo de inventario, que muestra estadísticas y gráficos relacionados con el análisis del inventario. Incluye información sobre ingresos, consumos, traspasos y otras métricas clave.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo HTML.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `kpi_ingresos`: Total de ingresos.
- `kpi_consumos_prod`: Consumo de producción.
- `kpi_consumos_mant`: Consumo de mantenimiento.
- `rate_reabast`: Tasa de reabastecimiento.
- `kpi_traspasos`: Número de traspasos.
- `rate_devolucion`: Tasa de devoluciones.
- `kpi_devoluciones`: Cantidad de devoluciones.
- `volumen_data`: Datos de volumen.
- `area_stats_json`: Estadísticas por área.
- `trend_labels`: Etiquetas para los gráficos de tendencia.
- `trend_entradas`: Datos de entradas para el gráfico de tendencia.
- `trend_salidas_prod`: Datos de salidas de producción para el gráfico de tendencia.
- `trend_salidas_mant`: Datos de salidas de mantenimiento para el gráfico de tendencia.
- `abc_counts`: Conteo de elementos ABC.
- `abc_mapping`: Mapeo de elementos ABC.
- `dow_distribution`: Distribución semanal de BMRI.
- `ubicaciones_mapping`: Mapeo de ubicaciones.
- `area_material_mapping`: Mapeo de materiales por área.
- `user_material_mapping`: Mapeo de materiales por usuario.
- `dow_material_mapping`: Mapeo de materiales por distribución semanal.
- `pm_material_mapping`: Mapeo de materiales por producción vs mantenimiento.

### Dependencias y Flujo
- **Librerías externas**: 
  - Chart.js
  - Chartjs-plugin-datalabels

- **Archivos CSS**:
  - `https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap`
  - Archivo local: `css/inventory.css`

- **Archivos JS**:
  - `https://cdn.jsdelivr.net/npm/chart.js`
  - `https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0`
  - Archivo local: `js/inventory.js`


---

## Archivo: ./templates/login.html

### Resumen Funcional
El archivo `login.html` es una página de inicio de sesión para la aplicación MonitorWeb. Permite a los usuarios ingresar sus credenciales y autenticarse en el sistema.

### Catálogo de Funciones y Clases
- `handleLogin(event)` - Maneja el evento de envío del formulario de inicio de sesión, realiza la autenticación y redirige al usuario si es exitosa.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: No se utilizan librerías externas.
- **Flujo Interno**: El archivo interactúa con el servidor a través del endpoint `/api/auth/login` para autenticar al usuario. Los datos de inicio de sesión se envían mediante una solicitud POST en formato `application/x-www-form-urlencoded`. Si la autenticación es exitosa, los tokens y detalles del usuario se almacenan en `localStorage`, y el usuario es redirigido a la página principal. En caso de error, se muestra un mensaje de error en la interfaz.


---

## Archivo: ./templates/settings.html

### Resumen Funcional
El archivo `settings.html` es una página web que permite la configuración dinámica de parámetros globales del sistema, mapeos de estados de entrega y centros de costo a áreas de negocio, así como el manejo de feriados. Permite visualizar, editar y guardar cambios en estos elementos.

### Catálogo de Funciones y Clases
- `updateSetting(key)` - Actualiza un parámetro global.
- `updateStatus(code)` - Actualiza una etiqueta de estado de entrega.
- `addStatus()` - Añade un nuevo mapeo de estado de entrega.
- `deleteStatus(code)` - Elimina un mapeo de estado de entrega.
- `updateCostCenter(code)` - Actualiza el área de negocio asociada a un centro de costo.
- `addCostCenter()` - Añade un nuevo mapeo de centro de costo a área de negocio.
- `deleteCostCenter(code)` - Elimina un mapeo de centro de costo a área de negocio.
- `syncHolidays()` - Sincroniza los feriados nacionales de Chile para el año actual y el próximo.
- `addHoliday()` - Añade una nueva fecha de feriado manual.
- `deleteHoliday(date_str)` - Elimina una fecha de feriado.
- `updateQuery(id)` - Actualiza un query almacenado.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- `fetch` (API para hacer solicitudes HTTP)
- `async/await` (para manejar operaciones asíncronas)

Flujo:
- La página interactúa con el backend a través de endpoints como `/api/settings/update`, `/api/settings/status`, etc., utilizando la función `apiCall`.
- Los cambios en los inputs son enviados al servidor para ser procesados y guardados.


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

