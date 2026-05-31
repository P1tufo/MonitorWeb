## Archivo: ./static/js/productivity.js (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `productivity.js` contiene funciones y lógica para cargar, renderizar y gestionar datos de productividad en una interfaz web. Permite cambiar la fecha y mes seleccionados, cargar datos de productividad diaria y mensual, y visualizar estos datos mediante gráficos y tablas.

### Catálogo de Funciones y Clases
- `loadProductivityData()` - Carga los datos de productividad para una fecha específica.
- `renderKPI1(summary)` - Renderiza el KPI 1 con resumen de actividad por usuario.
- `renderKPI2(trend)` - Renderiza el KPI 2 con tendencia diaria de movimientos.
- `renderKPI3(gaps)` - Renderiza el KPI 3 con baches de inactividad detectados.
- `renderKPI4(heatmapData)` - Renderiza el KPI 4 con mapa de calor de actividad.
- `loadMonthlyProductivityData()` - Carga los datos de productividad mensuales para un mes específico.
- `renderMonthlyKPI1(summary)` - Renderiza el KPI 1 mensual con resumen de actividad por usuario.
- `renderMonthlyKPI2(shifts)` - Renderiza el KPI 2 mensual con tendencia diaria de movimientos por turno.
- `renderMonthlyKPI3(heatmapData)` - Renderiza el KPI 3 mensual con mapa de calor de actividad.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `productivityTrendChartInst` - Instancia del gráfico de tendencia diaria.
- `productivityMonthlyTrendChartInst` - Instancia del gráfico de tendencia mensual.
- `COLORS` - Array con colores institucionales.

### Dependencias y Flujo
Dependencias:
- `fetch` - Para hacer solicitudes HTTP.
- `Chart.js` - Para renderizar gráficos.

Flujo:
- El archivo se comunica con el servidor a través de endpoints `/api/v1/analytics/productivity` y `/api/v1/analytics/productivity/monthly`.
- Los datos cargados se utilizan para actualizar las tablas y gráficos en la interfaz web.

