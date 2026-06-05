## Archivo: ./static/js/deliveries.js

### Resumen Funcional
El archivo `deliveries.js` contiene la lógica para el monitoreo de entregas en un sistema de almacén (WMS). Implementa funciones para abrir modales con detalles de áreas, días de la semana y ubicaciones, así como controladores para cambiar entre vistas operativas e históricas. También inicializa gráficos y actualiza los KPIs según las selecciones del usuario.

### Catálogo de Funciones y Clases
- `openModalWeekday(dayName, isCurrentMonth = false)` - Abre un modal con detalles del día seleccionado.
- `openModalUbicacion(name)` - Abre un modal con detalles de la ubicación seleccionada.
- `openModalArea(name, isCurrentMonth = false)` - Abre un modal con detalles de la área seleccionada.
- `openModalUser(name)` - Abre un modal con detalles del usuario seleccionado.
- `switchVLView(view)` - Cambia entre las vistas operativas e históricas.
- `updateDeliveriesAnalytics()` - Recalcula y actualiza los KPIs y filtra los gráficos según las selecciones del usuario.
- `toggleMulti(id)` - Alterna la visibilidad de un elemento con el ID especificado.
- `toggleChartSelectAll(isChecked)` - Maneja la selección de todos los elementos en una lista de verificación.
- `handleSmartCheckbox(cb)` - Maneja la lógica inteligente para las casillas de verificación, asegurando que no se pueda seleccionar vacío.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `currentModalContext` - Almacena el contexto actual del modal (área o día de la semana).
- `window.intensidadChart` - Referencia al gráfico de intensidad de entregas.
- `window.slaTrendChart`, `window.slaAreaTrendChart`, etc. - Referencias a otros gráficos históricos.

### Dependencias y Flujo
- **Dependencias**: `core_ui.js`
- **Archivos que importan este archivo**: Ninguno
- **Archivos que este archivo importa**: Ninguno

El flujo de datos se inicia con el evento `DOMContentLoaded`, donde se inicializan los gráficos y se configuran los controladores para los modales y las vistas. Los eventos de usuario, como la selección de áreas o días, desencadenan la actualización de KPIs y filtros en los gráficos.

