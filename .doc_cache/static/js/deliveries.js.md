## Archivo: ./static/js/deliveries.js (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `deliveries.js` contiene lógica para el análisis de entregas, incluyendo la interacción con componentes UI como modales y gráficos. Maneja datos de entrega, calcula indicadores clave (KPIs) y actualiza visualmente los gráficos en función de las selecciones del usuario.

### Catálogo de Funciones y Clases
- `UI.openModal(id)` - Abre un modal con el ID especificado.
- `UI.closeModal(id)` - Cierra un modal con el ID especificado.
- `UI.renderMaterialModal({ modalId, titleId, listId, title, items, colorVar, bgColor })` - Renderiza una lista de materiales en un modal.
- `getData(id)` - Obtiene datos JSON desde elementos del DOM.
- `openModalWeekday(dayName, isCurrentMonth = false)` - Abre el modal para mostrar detalles diarios.
- `openModalUbicacion(name)` - Abre el modal para mostrar detalles de ubicación.
- `openModalArea(name, isCurrentMonth = false)` - Abre el modal para mostrar detalles de área.
- `openModalUser(name)` - Abre el modal para mostrar detalles del usuario.
- `switchVLView(view)` - Cambia la vista entre operativa y histórica.
- `toggleMulti(id)` - Alterna la visibilidad de un elemento con el ID especificado.
- `updateDeliveriesAnalytics()` - Actualiza los KPIs y visualización en función de las selecciones del usuario.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `currentModalContext` - Almacena el contexto actual del modal (área o día).
- `window.openModal`, `window.closeModal`, `window.toggleModalFilter`, `window.openModalArea`, `window.openModalUser`, `window.openModalUbicacion` - Funciones globales para controlar modales y vistas.
- `window.slaTrendChart`, `window.slaAreaTrendChart`, `window.weeklyTrendChart`, `window.monthlyTrendChart`, `window.slaMonthlyTrendChart`, `window.slaMonthlyTrellisCharts` - Referencias a gráficos.

### Dependencias y Flujo
- Depende de la librería Chart.js para crear gráficos.
- Utiliza funciones globales definidas en el mismo archivo para controlar modales y vistas.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `deliveries.js` contiene funciones para actualizar gráficos y listas de áreas seleccionadas en una interfaz web, basándose en datos filtrados.

### Catálogo de Funciones y Clases
- `updateDeliveriesAnalytics()` - Actualiza los gráficos y la lista de áreas seleccionadas.
- `toggleChartSelectAll(isChecked)` - Maneja el estado del checkbox "Seleccionar todo" para los gráficos.
- `handleSmartCheckbox(cb)` - Maneja el comportamiento inteligente de los checkboxes individuales.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `window.areaMixChart` - Referencia al gráfico de mezcla de áreas.
- `window.weekHeatChart` - Referencia al gráfico de calor semanal.
- `selected` - Array que contiene las áreas seleccionadas.

### Dependencias y Flujo
- No depende de ninguna librería externa.
- Comunica con otros archivos del proyecto a través de funciones globales como `updateDeliveriesAnalytics()`.

