# Documentación Técnica - Directorio: templates/partials
Compilado el: 2026-06-07 18:34:58
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./templates/partials/_analytics_proyecciones_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para tres modales en una interfaz de usuario, cada uno con filtros y tablas para mostrar diferentes tipos de alertas y correlaciones de materiales. Los modales son utilizados para visualizar datos relacionados con desplanificación, correlaciones de materiales (basket) y listado frecuencia vs volumen.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna


---

## Archivo: ./templates/partials/_deliveries_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML que definen varios modales para una interfaz de usuario en un sistema de monitoreo de almacén (WMS). Cada modal muestra diferentes tipos de información, como el consumo específico, actividad del solicitador, desglose de ubicación, movimientos no paletizados y reportes mensuales de productividad.

### Catálogo de Funciones y Clases
No se detectaron funciones o clases definidas en este fragmento HTML. Todas las interacciones son realizadas a través de JavaScript y eventos del DOM.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: No se detectaron dependencias externas directamente en este fragmento.
- **Flujo**: Este archivo no importa ni es importado por otros archivos. Las interacciones con JavaScript son locales al contexto del HTML donde se incluyen estos modales.


---

## Archivo: ./templates/partials/_edit_query_modal.html

### Resumen Funcional
Este archivo contiene el código HTML para un modal de edición de consultas en el sistema de monitoreo de almacén (WMS). El modal incluye un constructor visual interactivo que permite configurar gráficos y KPIs, así como una vista previa del resultado.

### Catálogo de Funciones y Clases
No se detectaron funciones o clases específicas en este fragmento HTML. Todo el contenido es estructura HTML y CSS.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `editQueryId`: Un input oculto que almacena el ID de la consulta actualmente editada.

### Dependencias y Flujo
- **Dependencias**: No se importan bibliotecas externas ni archivos del proyecto en este fragmento.
- **Flujo**: Este archivo es consumido por otros archivos HTML o JavaScript para renderizar el modal de edición de consultas.


---

## Archivo: ./templates/partials/_inventory_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para varios modales en una interfaz de usuario de sistema de monitoreo de almacén (WMS). Cada modal muestra diferentes tipos de información, como consumo específico, actividad del asistente, materiales más movimientos, desglose de ubicación, curva ABC, materiales frecuentes y detalles de producción vs mantenimiento.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada directamente en este fragmento HTML. Todas las interacciones son realizadas a través del DOM y JavaScript.

### Interacción con Base de Datos
Ninguna interacción con la base de datos detectada en este archivo. Todas las listas y detalles se muestran dinámicamente mediante JavaScript.

### Estado y Variables Globales
Ninguna variable global, de sesión o de entorno detectada directamente en este fragmento HTML. Todas las variables y estados son gestionados por el JavaScript que interactúa con el DOM.

### Dependencias y Flujo
- **Librerías externas**: Ninguna librería externa importada.
- **Archivos del proyecto que IMPORTA a este archivo**: Ninguno.
- **Archivos del proyecto que este archivo IMPORTA (lo consume)**: Ninguno.
- **Flujo de datos**: El flujo de datos se gestiona completamente por JavaScript, que interactúa con el DOM para mostrar y ocultar modales y cargar contenido dinámicamente.


---

## Archivo: ./templates/partials/_logout.html

### Resumen Funcional
El archivo `_logout.html` contiene un fragmento de código JavaScript que se ejecuta cuando el usuario intenta cerrar sesión. Realiza una solicitud asíncrona al backend para notificar la salida del usuario y luego limpia los datos almacenados localmente, finalmente recarga la página para reflejar el cambio.

### Catálogo de Funciones y Clases
- `logout()` - Llama a la API para cerrar sesión y limpia los datos locales antes de recargar la página.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- No hay variables globales explícitas mencionadas en el código.

### Dependencias y Flujo
- **Dependencias**: Ninguna.
- **Flujo**: 
  - Este fragmento se ejecuta cuando el usuario intenta cerrar sesión.
  - Llama a la API `/api/auth/logout` para notificar al backend.
  - Limpia los datos de almacenamiento local (`localStorage.removeItem`) y luego recarga la página con `window.location.reload()`.

Este fragmento es parte del proceso de cierre de sesión en el sistema WMS, asegurando que tanto el backend como el frontend estén actualizados y seguros al cerrar una sesión.


---

## Archivo: ./templates/partials/_modals.html

### Resumen Funcional
Este archivo contiene fragmentos HTML para modales que se utilizan en el sistema de monitoreo de almacén (WMS). Los modales incluyen un visor de PDF, una tabla de mapeo de autores y áreas, y un modal de análisis detallado.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: Ninguna
- **Archivos Importados por Este Archivo**: Ninguno
- **Archivos que Importan a Este Archivo**: Ninguno


---

## Archivo: ./templates/partials/_quick_login_modal.html

### Resumen Funcional
El archivo `_quick_login_modal.html` es un fragmento de HTML que define una ventana modal para iniciar sesión rápidamente en el sistema de monitoreo de almacén (WMS). La ventana incluye campos para usuario y contraseña, y un botón para enviar los datos. Al enviar el formulario, se realiza una solicitud POST a la API de autenticación del sistema.

### Catálogo de Funciones y Clases
- `handleQuickLogin(event)` - Maneja el envío del formulario de inicio de sesión, realiza la autenticación y actualiza el estado del usuario en el almacenamiento local o recarga la página según sea necesario.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- `localStorage` - Se utilizan para almacenar el token de acceso, nombre de usuario y rol del usuario autenticado.
- `window.handleQuickLogin` - Variable global que expone la función `handleQuickLogin` al ámbito global.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directamente mencionadas en el código.
- **Flujo de Datos**:
  - El archivo se importa en otros archivos del proyecto (no especificados aquí).
  - Otros archivos pueden llamar a la función `handleQuickLogin` para iniciar sesión rápidamente.

El flujo de datos es unidireccional desde el HTML hasta el JavaScript, donde se maneja la autenticación y la actualización del estado del usuario.


---

## Archivo: ./templates/partials/_scripts.html

### Resumen Funcional
Este archivo contiene fragmentos de HTML que incluyen scripts para Chart.js, modales de inicio rápido y cierre, lógica del negocio y UI helpers para el panel de control, así como scripts específicos para la productividad diaria y mensual.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías externas**: Chart.js, chartjs-plugin-datalabels.
- **Archivos del proyecto que IMPORTA (consume)**: Ninguno.
- **Archivos del proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno.

El flujo de datos es unidireccional desde el HTML hacia los scripts externos y locales.


---

## Archivo: ./templates/partials/_sidebar.html

### Resumen Funcional
El archivo `_sidebar.html` es un fragmento de interfaz de usuario que contiene filtros y controles para interactuar con el sistema de monitoreo de almacén (WMS). Permite seleccionar fechas, áreas, centros, estados OT, realizar búsquedas y generar reportes PDF.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `dates`: Lista de fechas disponibles para filtrar.
- `default_dates`: Lista de fechas seleccionadas por defecto.
- `areas`: Lista de áreas disponibles para filtrar.
- `area_centro_map`: Diccionario que mapea áreas a centros.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directamente mencionadas en el código.
- **Flujo de Datos**:
  - El archivo se importa por otros archivos HTML para renderizar la interfaz del sidebar.
  - Los eventos de los controles (checkboxes, radios, input) invocan funciones JavaScript (`toggleSidebar`, `toggleMulti`, `handleSmartCheckbox`, `applyCentroFilter`, `applyFilters`, `downloadBulk`) que pueden interactuar con el backend a través de llamadas AJAX o directamente manipular el DOM.

Este fragmento es una parte integral del frontend, proporcionando la interfaz para los usuarios interactivos y controladores para manejar las acciones del usuario.


---

## Archivo: ./templates/partials/_styles.html

### Resumen Funcional
Este archivo contiene estilos CSS para el sistema de monitoreo de almacén (WMS). Define la apariencia visual del sitio web, incluyendo colores, fuentes, diseños de componentes y animaciones.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna


---

## Archivo: ./templates/partials/_tab_consumos.html

### Resumen Funcional
Este fragmento HTML corresponde a una pestaña dentro de un sistema de monitoreo de almacén (WMS) que permite analizar los consumos y costos de materiales. Permite buscar por Centro de Costo o por materiales específicos, mostrando históricos mensuales y anuales.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla `movimientos` (Mov. 201): 
    - `id`
    - `material_id`
    - `centro_costo_id`
    - `cantidad`
    - `precio_unitario`
    - `fecha`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Dependencias Externas:** Ninguna
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:** Ninguno
- **Flujo de Datos:** El archivo se utiliza para renderizar la interfaz de usuario y no interactúa directamente con el backend o base de datos.


---

## Archivo: ./templates/partials/_tab_deliveries.html

### Resumen Funcional
Este fragmento HTML es una pestaña dentro de un sistema de monitoreo de almacén (WMS) que muestra análisis y gráficos relacionados con las entregas. Permite seleccionar entre vistas anuales y semanales, mostrar estadísticas clave como volumen total de entregas y eficiencia de bodega, y filtrar los datos por áreas.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML. Todo el contenido es estructurado en elementos HTML y JavaScript.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `user.role`: Almacena el rol del usuario actual, utilizado para determinar si se muestran botones de edición de consultas SQL.
- `areas_vl`: Lista de áreas que pueden ser seleccionadas para filtrar los datos.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias directas en este fragmento HTML. Se utilizan elementos de JavaScript y CSS, pero no se importa ninguna biblioteca externa.
- **Flujo**: Este fragmento es consumido por la vista principal del sistema WMS. No importa a otros archivos ni es importado por otros archivos dentro del proyecto.


---

## Archivo: ./templates/partials/_tab_docs.html

### Resumen Funcional
Este archivo es un fragmento HTML que define una pestaña de interfaz de usuario en el sistema de monitoreo de almacén (WMS). Muestra un explorador de documentación con opciones para ver la estructura del proyecto y un mapa global generado por Graphify.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `fas fa-sitemap`, `fas fa-project-diagram`
- **Archivos del Proyecto que IMPORTA a este archivo (lo consumen)**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA (consume)**: Ninguno

**Flujo de Datos**: El fragmento HTML no consume ni produce datos. Es una vista estática que interactúa con el backend a través de eventos JavaScript para cargar contenido dinámicamente.


---

## Archivo: ./templates/partials/_tab_historial.html

### Resumen Funcional
Este fragmento HTML es una pestaña que muestra el historial de ubicaciones de un material en un sistema de monitoreo de almacén (WMS). Permite a los usuarios buscar un material y ver su stock actual y su historial de ubicaciones anteriores.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** Ninguna
- **Columnas:** Ninguna
- **Consultas SQL Crudas o Llamadas a ORM:** Ninguna

### Estado y Variables Globales
- `user.role`: Rol del usuario actual.

### Dependencias y Flujo
- **Librerías Externas:** Ninguna
- **Archivos Importados por este Archivo:** Ninguna
- **Archivos que Importan a este Archivo:** Ninguna

El flujo de datos es unidireccional, con el usuario interactuando con la interfaz y no habiendo intercambio de datos entre diferentes partes del sistema.


---

## Archivo: ./templates/partials/_tab_ia.html

### Resumen Funcional
Este fragmento HTML es una pestaña de la interfaz de usuario que muestra información sobre el análisis predictivo y los comportamientos de materiales en un sistema de monitoreo de almacén (WMS). Muestra semáforos de desplanificación, gráficos de frecuencia vs volumen y combos frecuentes.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **TABLAS:** Ninguna (El fragmento HTML no contiene consultas SQL ni llamadas a ORM directamente).
- **COLUMNAS:** Ninguna (No se accede a ninguna columna específica de la base de datos).

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas:** Ninguna
- **Archivos del Proyecto que IMPORTA:** Ninguno
- **Archivos del Proyecto que IMPORTAN a Este Archivo:** Ninguno
- **Flujo de Datos:** El fragmento HTML se renderiza en el cliente y no interactúa directamente con la base de datos o dependencias externas.


---

## Archivo: ./templates/partials/_tab_inventory.html

### Resumen Funcional
Este fragmento HTML es una pestaña de análisis de movimientos en el sistema de monitoreo de almacén (WMS). Muestra estadísticas clave como ingresos, consumos y traspasos, junto con gráficos que representan la eficiencia operativa y tendencias de consumo.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - No se especifican consultas SQL o llamadas a ORM en este fragmento HTML. Todas las estadísticas y datos son presentados directamente desde el contexto del backend.

### Estado y Variables Globales
- `user.role`: Rol del usuario actual.
- `ingresos_eff_stats`, `ingresos_eff_stats_weekly`: Datos de eficiencia operativa para ingresos (mensuales y semanales).
- `consumos_eff_stats`, `consumos_eff_stats_weekly`: Datos de eficiencia operativa para consumos (mensuales y semanales).
- `kpi_devoluciones`: Tasa de devoluciones.

### Dependencias y Flujo
- **Dependencias Externas:** Font Awesome (`fas fa-layer-group`, `fas fa-cog`, etc.)
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:** Ninguno

El flujo de datos es unidireccional, con el backend proporcionando los datos necesarios para renderizar la vista en el frontend.


---

## Archivo: ./templates/partials/_tab_ots.html (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
Este fragmento HTML corresponde a una pestaña dentro de un sistema de monitoreo de almacén (WMS) que muestra estadísticas y tablas interactivas relacionadas con las Ordenes de Transporte (OTs). Incluye gráficos, contadores y listados filtrables para visualizar el estado de las OTs pendientes, movimientos no paletizados y análisis de productividad.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML. Todo es contenido estático y dinámico generado por JavaScript.

### Interacción con Base de Datos
- **Motor**: SQLite
- **TABLAS**:
  - `inventory_movements` (Mencionada en la alerta operativa)
- **COLUMNAS**:
  - No se especifican columnas explícitas, pero el fragmento hace referencia a campos como `doc_mat`, `creator`, `clase_mov`, etc.

### Estado y Variables Globales
No se detectan variables globales o de sesión definidas en este fragmento HTML. Todo es contenido dinámico generado por JavaScript.

### Dependencias y Flujo
- **Librerías Externas**: No se mencionan librerías externas específicas.
- **Archivos del Proyecto que IMPORTA a este archivo**: Ninguno.
- **Archivos del Proyecto que ESTE archivo IMPORTA (consume)**: Ninguno.

El flujo de datos es principalmente entre el cliente y el servidor, con la generación dinámica de contenido HTML y JavaScript basado en los datos recuperados desde la base de datos.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
Este archivo contiene el código HTML para una interfaz de usuario que muestra detalles diarios y mensuales de movimientos en un sistema de almacén (WMS). Incluye tablas interactivas para visualizar los datos y botones para navegar entre diferentes niveles de detalle.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: No se mencionan dependencias específicas en el código proporcionado.
- **Flujo**: El archivo no importa ni es importado por otros archivos. Es un fragmento de HTML que se utiliza para renderizar la interfaz de usuario en una página web.

Este archivo solo contiene estructura HTML y CSS, sin interacción con base de datos o lógica de negocio.


---

## Archivo: ./templates/partials/_tab_replenishment.html

### Resumen Funcional
Este fragmento HTML es una interfaz de usuario para mostrar sugerencias de pedido en un sistema de monitoreo de almacén (WMS). Muestra una tabla con detalles sobre el material, su descripción, UMB, stock inicial y actual, consumo mensual, frecuencia de retiros, autonomía en meses y clasificación ABC. Incluye filtros para la frecuencia de pedido y un botón para exportar los datos a Excel.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** Ninguna (El fragmento HTML no interactúa directamente con una base de datos. Los datos se cargan desde un endpoint API).
- **Columnas:** Ninguna (No hay consultas SQL o ORM explícitas en el fragmento HTML).

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `fas fa-exclamation-triangle`, `fas fa-file-excel`
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno (Este archivo no importa otros archivos).
- **Archivos del Proyecto que Este Archivo Importa:** Ninguno (No hay imports en el fragmento HTML).

**Flujo de Datos:**
El fragmento HTML se carga en la interfaz del usuario. Los datos para llenar la tabla se obtienen a través de una solicitud GET al endpoint `/api/inventory/replenishment-suggestions/export`.


---

## Archivo: ./templates/partials/_tab_transporte.html

### Resumen Funcional
Este fragmento HTML es una sección de la interfaz de usuario para el sistema de monitoreo de almacén (WMS), que muestra gráficos y tablas relacionados con las entregas. Incluye un filtro por tiempo, un gráfico de líneas, alertas de OTs pendientes de ingreso en SAP, un buscador rápido de entregas y una tabla con los últimos 25 registros y reportes PDF.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:**
  - `transporte` (Tabla que almacena información sobre las entregas)
- **Columnas:**
  - `id`
  - `fecha`
  - `ot`
  - `gd`
  - `oc`
  - `bultos`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** Ninguna
- **Archivos del Proyecto que Importan a este Archivo:**
  - `routes.py` (Consumen el fragmento para mostrarlo en la interfaz de usuario)
- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno

El flujo de datos es unidireccional, con el archivo HTML consumido por otros componentes del sistema para renderizar la interfaz de usuario.


---

## Archivo: ./templates/partials/_table.html

### Resumen Funcional
Este fragmento HTML es una tabla que muestra transacciones en un sistema de monitoreo de almacén (WMS). La tabla incluye columnas para la entrega/OT, fecha, items, área y estado. Ofrece funcionalidades como ordenar las columnas, buscar registros y generar PDFs.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directamente mencionadas en este fragmento.
- **Flujo**: Este archivo es un fragmento HTML que se renderiza en una página web. No realiza ninguna operación de base de datos ni interactúa con variables globales. Se consume por vistas o componentes que lo incluyen en su plantilla.

Este fragmento es parte de la interfaz de usuario y no contiene lógica de negocio o acceso a bases de datos.


---

