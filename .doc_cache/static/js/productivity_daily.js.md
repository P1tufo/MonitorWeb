## Archivo: ./static/js/productivity_daily.js

### Resumen Funcional
Este archivo JavaScript (`productivity_daily.js`) se encarga de manejar la interacción del usuario con los gráficos y tablas de productividad diaria en el sistema de monitoreo de almacén (WMS). Permite filtrar usuarios, cargar datos según la fecha seleccionada, y renderizar diferentes KPIs como resúmenes, tendencias, baches y mapas de calor.

### Catálogo de Funciones y Clases
- `toggleDailyUserFilter()` - Muestra u oculta el filtro de usuarios diarios.
- `filterDailyUserList()` - Filtra la lista de usuarios según el texto ingresado en el campo de búsqueda.
- `renderDailyUserCheckboxes(summary)` - Renderiza los checkboxes para seleccionar usuarios, agrupados por grupos y individuales.
- `selectUserGroup(groupUsers)` - Selecciona todos los usuarios de un grupo específico.
- `toggleAllDailyUsers()` - Selecciona o deselecciona todos los usuarios.
- `onDailyUserCheckboxChange()` - Maneja el cambio en la selección de checkboxes de usuarios.
- `renderFilteredDaily()` - Renderiza los KPIs filtrados según los usuarios seleccionados.
- `changeProductivityDate(offset)` - Cambia la fecha seleccionada para cargar nuevos datos.
- `changeProductivityMonth(offsetMonths)` - Cambia el mes seleccionado para cargar nuevos datos.
- `loadProductivityData()` - Carga los datos de productividad diaria desde una API y renderiza los KPIs correspondientes.
- `renderKPI1(summary)` - Renderiza el resumen de movimientos diarios.
- `renderKPI2(trend)` - Renderiza la tendencia de movimientos diarios en un gráfico de líneas.
- `renderKPI3(gaps)` - Renderiza los baches de productividad diaria.
- `renderKPI4(heatmapData)` - Renderiza el mapa de calor de productividad diaria.

### Interacción con Base de Datos
Ninguna. El archivo no realiza ninguna consulta a una base de datos.

### Estado y Variables Globales
- `productivityTrendChartInst` - Instancia del gráfico de tendencias.
- `currentDailyData` - Datos actuales de productividad diaria.
- `selectedDailyUsers` - Usuarios seleccionados para el filtrado.
- `userGroupsCache` - Grupos de usuarios almacenados en caché.

### Dependencias y Flujo
Dependencias:
- `Chart.js` - Usado para renderizar gráficos.

Flujo:
- El archivo se carga cuando se abre la página.
- Se inicializan variables globales y eventos.
- Al seleccionar una fecha o cambiar de pestaña, se llama a `loadProductivityData()` para cargar los datos correspondientes.
- Los KPIs se renderizan según los datos cargados y las selecciones del usuario.

