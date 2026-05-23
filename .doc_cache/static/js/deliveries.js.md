## Archivo: ./static/js/deliveries.js (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `deliveries.js` contiene la lógica para el análisis de entregas, incluyendo la interacción con componentes UI, controladores de modales, inicialización de gráficos y actualizaciones dinámicas del estado.

### Catálogo de Funciones y Clases
- `openModal(id)` - Abre un modal utilizando CoreUI.
- `closeModal(id)` - Cierra un modal utilizando CoreUI.
- `renderMaterialModal(opts)` - Renderiza un modal con opciones específicas.
- `getData(id)` - Obtiene datos desde una fuente externa.
- `toggleModalFilter(type, isCurrentMonth)` - Alternativa entre mostrar modales de área y día según el contexto actual.
- `openModalWeekday(dayName, isCurrentMonth = false)` - Abre un modal para mostrar detalles del día.
- `openModalUbicacion(name)` - Abre un modal para mostrar detalles de ubicación.
- `openModalArea(name, isCurrentMonth = false)` - Abre un modal para mostrar detalles de área.
- `openModalUser(name)` - Abre un modal para mostrar detalles de usuario.
- `switchVLView(view)` - Cambia la vista entre operativa y histórica.
- `toggleMulti(id)` - Alterna la visibilidad de elementos según su ID.
- `updateDeliveriesAnalytics()` - Actualiza los KPIs y filtra listas y gráficos según las áreas seleccionadas.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `currentModalContext` - Almacena el contexto actual del modal (área y día).
- `window.slaTrendChart`, `window.monthlyTrendChart`, etc. - Referencias a gráficos inicializados.

### Dependencias y Flujo
Depende de `core_ui.js` para funciones UI como `openModal`, `closeModal`, y `renderMaterialModal`. Utiliza `getData` para obtener datos desde fuentes externas.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `deliveries.js` contiene funciones para actualizar gráficos de rendimiento diario, semanal y mensual basados en datos seleccionados. Actualiza los datos de las gráficas de SLA (Service Level Agreement) y entrega semanal.

### Catálogo de Funciones y Clases
- `updateDeliveriesAnalytics()` - Actualiza los datos de las gráficas de rendimiento.
- `window.toggleChartSelectAll(isChecked)` - Maneja la selección de todos los elementos en un grupo de checkboxes.
- `window.handleSmartCheckbox(cb)` - Maneja la selección inteligente de elementos individuales en un grupo de checkboxes.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- `getData('data_weekly_raw_json')`
- `getData('data_sla_area_trend_raw_json')`

Flujo:
1. La función `updateDeliveriesAnalytics()` se ejecuta cuando se necesitan actualizar los datos de las gráficas.
2. Se filtran los datos según la selección del usuario (`selected`).
3. Los datos filtrados se agrupan y procesan para calcular SLA y entregas.
4. Los resultados se actualizan en las gráficas correspondientes.

La función `window.toggleChartSelectAll(isChecked)` maneja la selección de todos los elementos en un grupo de checkboxes, asegurando que no haya una selección vacía.

La función `window.handleSmartCheckbox(cb)` maneja la selección inteligente de elementos individuales, asegurando que si "Todos" está seleccionado y se selecciona uno individualmente, "Todos" se deselecciona.

