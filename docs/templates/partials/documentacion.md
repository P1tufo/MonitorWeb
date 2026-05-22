# Documentación Técnica - Directorio: templates/partials
Compilado el: 2026-05-22 16:53:13
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./templates/partials/_analytics_proyecciones_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para tres modales: uno que muestra todas las alertas de desplanificación, otro que muestra correlaciones de materiales (combos), y otro que muestra un listado frecuencia vs volumen. Cada modal tiene filtros y una tabla que se llena dinámicamente a través de JavaScript.

### Catálogo de Funciones y Clases
- `closeModal(modalId)` - Cierra el modal especificado.
- `filterAlerts()` - Filtra las alertas según los criterios de búsqueda y selección.
- `filterCombos()` - Filtra los combos según los criterios de búsqueda.
- `filterScatter()` - Filtra el listado frecuencia vs volumen según los criterios de búsqueda y selección.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
No depende de ninguna librería externa ni comunica con otros archivos del proyecto.


---

## Archivo: ./templates/partials/_deliveries_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para varios modales que probablemente se utilizan en una interfaz web para mostrar detalles específicos sobre entregas, actividades de usuarios, desglose de ubicaciones y movimientos no paletizados.

### Catálogo de Funciones y Clases
- `toggleModalFilter(filterType, isMonth)` - Alterna el filtro del modal según el tipo (area o weekday) y si se selecciona el mes actual.
- `closeModal(modalId)` - Cierra el modal con el ID especificado.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- `jQuery` (usado para manipular el DOM)
- `FontAwesome` (usado para iconos)

Flujo: Este archivo no interactúa directamente con otros archivos del proyecto, solo proporciona estructura HTML y JavaScript básico para los modales.


---

## Archivo: ./templates/partials/_edit_query_modal.html

### Resumen Funcional
Este archivo contiene el código HTML para un modal de edición de consultas SQL en una interfaz de usuario, que incluye un constructor visual interactivo y un panel de vista previa del gráfico resultante.

### Catálogo de Funciones y Clases
No se detectaron funciones o clases definidas explícitamente en este fragmento de código HTML.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Dependencias**: No hay dependencias directas mencionadas. El archivo incluye un script externo `analytics_studio.js` que se carga desde la carpeta `static/js`.
- **Flujo**: Este fragmento de código HTML no interactúa con otros archivos del proyecto o realiza ninguna operación específica en términos de flujo de control.

Este modal es principalmente una interfaz de usuario para editar consultas SQL y visualizar el resultado, pero no contiene lógica de negocio ni interacción directa con la base de datos.


---

## Archivo: ./templates/partials/_inventory_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para varios modales de interfaz de usuario, cada uno con un título y una lista desordenada (`<ul>`) que se llena dinámicamente a través de JavaScript. Los modales son utilizados para mostrar información detallada sobre diferentes aspectos del inventario, como el consumo específico, actividad del asistente, materiales más movimientos, desglose de ubicación, curva ABC, días de la semana y producción vs mantenimiento.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo. Todas las interacciones son realizadas a través de HTML y JavaScript.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías externas utilizadas**: No se detectan librerías externas específicas.
- **Flujo hacia otros archivos del proyecto**: Este archivo no comunica directamente con otros archivos del proyecto. Las interacciones son internas a la interfaz de usuario y se realizan mediante JavaScript para cargar dinámicamente los datos en las listas desordenadas (`<ul>`).


---

## Archivo: ./templates/partials/_logout.html

### Resumen Funcional
Este fragmento de código HTML contiene un script que define una función `logout` para cerrar la sesión del usuario. La función intenta notificar al backend mediante una solicitud POST a la ruta `/api/auth/logout`, limpia el almacenamiento local (tokens y datos de usuario) y redirige al usuario al Dashboard.

### Catálogo de Funciones y Clases
- `logout()` - Limpia el estado del usuario y cierra sesión.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales en este fragmento de código.

### Dependencias y Flujo
- **Librerías Externas**: `fetch` (navegador).
- **Flujo Interno**: La función `logout` no depende de otros archivos del proyecto directamente, pero interactúa con el backend a través de una solicitud HTTP.


---

## Archivo: ./templates/partials/_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para dos modales: uno que muestra un visor de PDF y otro que presenta una tabla de usuarios y sus áreas asignadas.

### Catálogo de Funciones y Clases
No se detectan funciones ni clases definidas en este archivo.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `autores_map`: Una variable global o diccionario que contiene la información de los autores y sus áreas asignadas. Se utiliza para llenar la tabla en el modal "Tabla de usuarios y sus areas".

### Dependencias y Flujo
No se detectan dependencias externas ni llamadas a otros archivos del proyecto.


---

## Archivo: ./templates/partials/_scripts.html

### Resumen Funcional
Este fragmento HTML incluye scripts para Chart.js y una lógica de negocio y ayuda de interfaz de usuario para el panel de control.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- **Librerías externas utilizadas**: Chart.js.
- **Flujo hacia otros archivos del proyecto**: Se incluye un fragmento HTML (`_logout.html`) y se carga un script JavaScript (`dashboard.js`).


---

## Archivo: ./templates/partials/_sidebar.html

### Resumen Funcional
Este archivo contiene el código HTML para un panel lateral que incluye varios filtros y controles de búsqueda para una interfaz web. Permite filtrar por fecha, área, centro, estado OT (Estado WMS), buscar por número de OT o entrega, incluir un logo específico, y descargar reportes consolidados en formato PDF.

### Catálogo de Funciones y Clases
- `toggleSidebar()` - Cierra el panel lateral.
- `toggleMulti(id)` - Muestra u oculta los checkboxes dentro del multiselect.
- `toggleSelectAll(group, checked)` - Selecciona/deselecciona todos los checkboxes en un grupo.
- `handleSmartCheckbox(checkbox, group, allCheckboxId, table)` - Maneja el cambio de estado de los checkboxes inteligentes.
- `applyCentroFilter(value)` - Aplica el filtro por centro seleccionado.
- `applyFilters()` - Aplica los filtros según las selecciones del usuario.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- JavaScript (funciones como `toggleSidebar`, `toggleMulti`, etc.)
- Jinja2 templating (para iterar sobre variables como `dates` y `areas`)

Flujo: Este archivo se comunica con otros archivos JavaScript para manejar eventos de usuario, actualizar el estado del filtro y generar reportes.


---

## Archivo: ./templates/partials/_styles.html

### Resumen Funcional
Este archivo contiene estilos CSS para una interfaz web, definiendo colores, layout y animaciones.

### Catálogo de Funciones y Clases
No aplica

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
No aplica


---

## Archivo: ./templates/partials/_tab_deliveries.html

### Resumen Funcional
Este fragmento HTML muestra una pestaña de análisis de entregas con gráficos y KPIs, permitiendo a los usuarios cambiar entre vistas operativas y históricas. Incluye estadísticas como volumen total, eficiencia de bodega, entregadas a tiempo y atrasadas, así como gráficos interactivos para visualizar la evolución mensual y semanal del cumplimiento SLA.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML. Todas las interacciones son realizadas mediante JavaScript y eventos del DOM.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `kpi_total`: Volumen total de entregas (Año).
- `kpi_eff`: Eficiencia de bodega (%).
- `kpi_ontime`: Entregadas a tiempo.
- `kpi_late`: Entregadas atrasadas.
- `areas_vl`: Lista de áreas seleccionadas para el filtrado.
- `top_authors`: Top solicitadores con sus entregas y áreas.
- `top_materials`: Ranking de materiales repetitivos por área.

### Dependencias y Flujo
Dependencias:
- Font Awesome (para íconos).
- JavaScript (para interactividad).

Flujo:
Este fragmento interactúa con el backend a través de funciones JavaScript que pueden abrir modales para editar consultas SQL, cambiar vistas, filtrar datos, y actualizar gráficos. No realiza llamadas directas a una base de datos ni depende de variables globales definidas en otros archivos del proyecto.


---

## Archivo: ./templates/partials/_tab_docs.html

### Resumen Funcional
Este fragmento HTML es una pestaña de interfaz de usuario que muestra la estructura del proyecto y permite explorar los archivos de documentación. Incluye un panel lateral para navegar por el árbol de documentos y una sección principal donde se visualiza el contenido seleccionado.

### Catálogo de Funciones y Clases
No aplica

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas mencionadas.
- **Flujo**: Este fragmento no interactúa con otros archivos del proyecto ni realiza llamadas a funciones. Es una vista estática que muestra la estructura del proyecto y permite seleccionar archivos para visualizar su contenido.


---

## Archivo: ./templates/partials/_tab_historial.html

### Resumen Funcional
Este fragmento HTML es una pestaña que muestra el historial de ubicaciones de un material. Permite a los usuarios buscar un material y ver su stock actual y su historial de ubicaciones anteriores.

### Catálogo de Funciones y Clases
No se detectan funciones ni clases definidas en este fragmento HTML.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías externas utilizadas**: `FontAwesome` (referenciado por `<i class="fas fa-cog"></i>`).
- **Flujo hacia otros archivos del proyecto**: No se detecta interacción con otros archivos específicos dentro del proyecto.


---

## Archivo: ./templates/partials/_tab_ia.html

### Resumen Funcional
Este fragmento HTML es una pestaña que muestra información sobre el análisis de IA, incluyendo semáforos de desplanificación y cuadrantes de frecuencia vs volumen. Muestra alertas de materiales con alta probabilidad de solicitud inminente y combos frecuentes.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `error_msg`: Variable global que almacena un mensaje de error si ocurre algún problema.
- `alerts`: Lista de alertas que se muestran en el semáforo de desplanificación.
- `combos`: Lista de combos frecuentes que se muestran en la sección de Market Basket.

### Dependencias y Flujo
- **Librerías externas**: No se detectan librerías externas utilizadas específicamente en este fragmento HTML.
- **Flujo hacia otros archivos**: Este fragmento interactúa con JavaScript a través de funciones como `openEditQueryModal`, `openModalAlerts`, y `openModalScatter`.


---

## Archivo: ./templates/partials/_tab_inventory.html

### Resumen Funcional
Este fragmento HTML es una pestaña que muestra un análisis de movimientos en una interfaz web, incluyendo estadísticas clave y gráficos interactivos.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML. Todas las interacciones son realizadas a través de JavaScript y eventos del usuario.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `user.role`: Rol del usuario actual.
- `kpi_ingresos`, `kpi_consumos_prod`, `kpi_consumos_mant`, `rate_reabast`, `kpi_traspasos`, `rate_devolucion`, `rate_eficiencia`: Valores de KPIs que se muestran en la interfaz.
- `top_materials_quick`: Lista de materiales más consumidos (Top Consumidos).
- `top_users`: Lista de usuarios con mayor frecuencia de despachos.

### Dependencias y Flujo
Dependencias:
- JavaScript: Se utilizan funciones como `switchInventarioView`, `openEditQueryModal`, `openModal`, `openModalUserInventario`.

Flujo:
Este fragmento HTML se comunica con otros archivos a través de llamadas a funciones JavaScript que pueden estar definidas en otros archivos del proyecto. No hay interacción directa con bases de datos ni dependencias externas adicionales mencionadas.


---

## Archivo: ./templates/partials/_tab_ots.html

### Resumen Funcional
Este fragmento HTML muestra una pestaña de gestión de Ordenes de Transporte (OTs) con estadísticas, gráficos y tablas interactivas. Permite filtrar y visualizar OTs pendientes, movimientos no paletizados y detalles específicos.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML.

### Interacción con Base de Datos
- **Motor:** No aplica (el código no contiene consultas SQL ni interacciones directas con una base de datos).
- **Tablas:** No aplica.
- **Columnas:** No aplica.

### Estado y Variables Globales
No se detectan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Librerías Externas:** `FontAwesome` para iconos.
- **Flujo Interno:** El fragmento interactúa con JavaScript a través de eventos como `onclick`, que llaman funciones como `openEditQueryModal`, `filterOTTable`, `switchSubTab`, etc. No se indica interacción directa con otros archivos del proyecto en este fragmento.


---

## Archivo: ./templates/partials/_table.html

### Resumen Funcional
Este fragmento HTML define una tabla para mostrar transacciones, con columnas para entrega/OT, fecha, items, área y estado. Incluye funcionalidades de ordenación y búsqueda.

### Catálogo de Funciones y Clases
- `sortTable(column)` - Ordena la tabla según la columna especificada.
- `filterTable()` - Filtra las filas de la tabla según los valores de entrada en los campos de búsqueda.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- JavaScript (`sortTable`, `filterTable`)
- CSS (estilos para la tabla y elementos)

Flujo: Este fragmento se comunica con el backend a través de formularios que envían solicitudes POST al endpoint `/generate-pdf` para generar y previsualizar/descargar PDFs.


---

