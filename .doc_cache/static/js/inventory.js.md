## Archivo: ./static/js/inventory.js

### Resumen Funcional
El archivo `inventory.js` contiene lógica para manejar movimientos en un sistema de monitoreo de almacén (WMS). Incluye funciones para abrir modales con información sobre ubicaciones y usuarios, así como una funcionalidad de búsqueda dinámica para mostrar el stock y historial de ubicaciones.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra mensajes en la consola.
- `parseFormattedInt(val)` - Convierte un valor a un entero formateado, eliminando caracteres no numéricos.
- `window.openModalUbicacion(name)` - Abre un modal con información sobre una ubicación específica.
- `window.openModalUserInv(name)` - Abre un modal con información sobre un usuario específico.
- `window.switchInventarioView(view)` - Cambia la vista del inventario según el tipo de visualización seleccionada.

### Interacción con Base de Datos
Ninguna. El archivo no realiza ninguna operación directa en una base de datos.

### Estado y Variables Globales
No hay variables globales explícitas definidas en este archivo.

### Dependencias y Flujo
- **Dependencias**: `core_ui.js` (provee funciones como `CoreUI.openModal`, `CoreUI.closeModal`, etc.)
- **Flujo de Datos**:
  - El archivo se carga cuando el DOM esté listo.
  - Llama a funciones de `core_ui.js` para abrir modales y renderizar contenido.
  - Realiza solicitudes AJAX al servidor para obtener datos de ubicaciones y stock, que luego se procesan y mostran en la interfaz.

Este archivo es parte del frontend de un sistema WMS, gestionando la interacción con el usuario a través de modales y búsqueda dinámica.

