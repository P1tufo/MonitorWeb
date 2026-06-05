## Archivo: ./static/js/dashboard_api.js

### Resumen Funcional
El archivo `dashboard_api.js` contiene la lógica de la API para el módulo del panel de control en un sistema de monitoreo de almacén (WMS). Define funciones para interactuar con endpoints de la API, como obtener indicadores clave de rendimiento (KPIs), datos filtrados y sincronizar los datos.

### Catálogo de Funciones y Clases
- `_fetch(url, options = {})` - Realiza una solicitud HTTP a la URL especificada con las opciones proporcionadas.
- `fetchKPIs(params)` - Obtiene KPIs basándose en los parámetros proporcionados.
- `fetchFilteredData(params)` - Obtiene datos filtrados según los parámetros proporcionados.
- `sync()` - Sincroniza los datos del almacén con el servidor.
- `checkSyncStatus()` - Verifica el estado de la sincronización actual.
- `logout()` - Cierra sesión y limpia el almacenamiento local.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- Ninguna variable global explícita está declarada en este archivo.

### Dependencias y Flujo
- **Dependencias**: `fetch` (API web para hacer solicitudes HTTP).
- **Archivos que importan a este archivo**: Ninguno.
- **Archivos que este archivo importa**: Ninguno.
- **Flujo de datos**: El flujo de datos se gestiona principalmente a través de las funciones `_fetch`, `fetchKPIs`, `fetchFilteredData`, `sync`, `checkSyncStatus` y `logout`. Los datos son solicitados y procesados en el cliente, y la interacción con el servidor se realiza mediante solicitudes HTTP.

Este archivo es una parte integral del frontend que interactúa con el backend a través de endpoints definidos para obtener y gestionar los datos necesarios para el panel de control.

