## Archivo: ./static/js/productivity_monthly.js

### Resumen Funcional
Este archivo contiene la lógica para renderizar y gestionar los datos de productividad mensual en un sistema de almacén. Permite filtrar por usuarios, cargar datos desde una API, y visualizar KPIs como resúmenes de actividad, gráficos de tendencias y mapas de calor.

### Catálogo de Funciones y Clases
- `toggleMonthlyUserFilter()` - Alterna la visibilidad del filtro de usuarios.
- `renderMonthlyUserCheckboxes(summary)` - Renderiza los checkboxes para filtrar por usuarios.
- `toggleAllMonthlyUsers()` - Selecciona/deselecciona todos los usuarios en el filtro.
- `onMonthlyUserCheckboxChange()` - Maneja el cambio en el estado de los checkboxes de usuario.
- `renderFilteredMonthly()` - Filtra y renderiza los KPIs según los usuarios seleccionados.
- `loadMonthlyProductivityData()` - Carga los datos de productividad mensuales desde la API.
- `renderMonthlyKPI1(summary)` - Renderiza el primer KPI (resumen de actividad).
- `renderMonthlyKPI2(shifts)` - Renderiza el segundo KPI (tendencias por turno).
- `renderMonthlyKPI3(heatmapData)` - Renderiza el tercer KPI (mapa de calor).

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `productivityMonthlyTrendChartInst` - Instancia del gráfico de tendencias mensuales.
- `currentMonthlyData` - Datos actuales de productividad mensual.
- `selectedMonthlyUsers` - Usuarios seleccionados para el filtro.

### Dependencias y Flujo
- **Dependencias**: No se mencionan librerías externas específicas en este fragmento.
- **Flujo de Datos**:
  - El archivo es consumido por HTML (no se muestra aquí).
  - Importa funciones desde otros archivos JavaScript del proyecto, pero no se detalla cuáles son estos archivos.

