## Archivo: ./static/js/dashboard.js

### Resumen Funcional
El archivo `dashboard.js` contiene la lógica principal del dashboard de MonitorWeb. Define funciones para interactuar con una API, manejar la interfaz de usuario (UI), aplicar filtros y ordenar tablas, generar PDFs, y sincronizar datos.

### Catálogo de Funciones y Clases
- `DashboardAPI._fetch(url, options)` - Realiza solicitudes HTTP a la API.
- `DashboardAPI.fetchKPIs(params)` - Obtiene los KPIs (Indicadores Clave de Desempeño) basados en los parámetros proporcionados.
- `DashboardAPI.fetchFilteredData(params)` - Obtiene datos filtrados según los parámetros proporcionados.
- `DashboardAPI.sync()` - Sincroniza los datos del cliente con el servidor.
- `DashboardAPI.checkSyncStatus()` - Verifica el estado de la sincronización actual.
- `DashboardAPI.logout()` - Cierra sesión y redirige al usuario a la página de inicio de sesión.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- `fetch` (navegador)
- `localStorage`

Flujo:
- El archivo interactúa con la API para obtener datos, renderizar tablas, aplicar filtros, generar PDFs y sincronizar datos.
- Utiliza funciones globales como `closePdfModal`, `toggleMulti`, `sortTable`, etc., que se definen en el mismo archivo y son accesibles globalmente a través de `window`.

