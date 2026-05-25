## Archivo: ./static/js/inventory.js

### Resumen Funcional
El archivo `inventory.js` contiene lógica para manejar movimientos analíticos en una interfaz web, utilizando funciones y métodos para abrir modales, procesar datos, y gestionar la interacción con un buscador de ubicaciones dinámico.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra mensajes en la consola.
- `parseFormattedInt(val)` - Convierte una cadena a un número entero, eliminando caracteres no numéricos.
- `openModalUbicacion(name)` - Abre un modal con información de ubicación.
- `openModalUserInv(name)` - Abre un modal con información de usuario.
- `switchInventarioView(view)` - Cambia la vista del inventario según el parámetro proporcionado.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales en este archivo.

### Dependencias y Flujo
- Depende de `core_ui.js` para funciones como `openModal`, `closeModal`, `renderMaterialModal`, y `getData`.
- Comunica con el servidor a través de una solicitud `fetch` a la ruta `/api/ubicaciones/{valor}` para obtener datos de ubicaciones.

