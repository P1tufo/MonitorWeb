## Archivo: ./static/js/productivity_daily.js

### Resumen Funcional
Este archivo JavaScript (`productivity_daily.js`) se encarga de manejar la interacción del usuario con los gráficos y tablas diarias de productividad en el sistema de monitoreo de almacén (WMS). Permite filtrar datos por usuarios, cargar datos según una fecha seleccionada, y renderizar diferentes KPIs como gráficos de tendencia, resúmenes de actividad, baches en la productividad y un mapa de calor.

### Catálogo de Funciones y Clases
- `toggleDailyUserFilter()` - Muestra u oculta el filtro de usuarios diarios.
- `renderDailyUserCheckboxes(summary)` - Renderiza los checkboxes para filtrar por usuarios.
- `toggleAllDailyUsers()` - Selecciona/deselecciona todos los usuarios en el filtro.
- `onDailyUserCheckboxChange()` - Maneja el cambio en la selección de usuarios.
- `renderFilteredDaily()` - Renderiza los KPIs filtrados según la selección de usuarios.
- `loadProductivityData()` - Carga los datos diarios de productividad desde una API y actualiza la interfaz.
- `renderKPI1(summary)` - Renderiza el resumen de actividad diaria.
- `renderKPI2(trend)` - Renderiza la tendencia de movimientos del equipo.
- `renderKPI3(gaps)` - Renderiza los baches en la productividad.
- `renderKPI4(heatmapData)` - Renderiza el mapa de calor de productividad.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a una base de datos.

### Estado y Variables Globales
- `productivityTrendChartInst` - Instancia del gráfico de tendencia.
- `currentDailyData` - Datos diarios actuales cargados.
- `selectedDailyUsers` - Usuarios seleccionados para el filtro.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `Chart.js` (para renderizar gráficos).
  
- **Archivos del Proyecto que Importan a este Archivo**:
  - `dashboard.js` (se espera que contenga la función `switchSubTab`).

- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno.

- **Flujo de Datos**: 
  - El archivo se ejecuta cuando el DOM esté listo (`DOMContentLoaded`).
  - Se manejan eventos como cambios en los filtros y selecciones.
  - Los datos diarios se cargan a través de una llamada `fetch` a la API `/api/v1/analytics/productivity`.
  - Los KPIs se renderizan basándose en los datos recibidos.

