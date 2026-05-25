## Archivo: ./static/js/inventory.js

### Resumen Funcional
El archivo `inventory.js` contiene lógica para manejar movimientos de inventario, incluyendo la interacción con una interfaz de usuario y la obtención de datos desde una base de datos a través de una API.

### Catálogo de Funciones y Clases
- `log(msg, data = null)` - Registra mensajes en la consola.
- `parseFormattedInt(val)` - Convierte un valor a un entero, eliminando caracteres no numéricos.
- `openModalUbicacion(name)` - Abre una ventana modal con información de ubicación.
- `openModalUserInv(name)` - Abre una ventana modal con información del inventario de usuarios.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción directa con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales en este archivo.

### Dependencias y Flujo
- Depende de `core_ui.js` para funciones como `CoreUI.openModal`, `CoreUI.closeModal`, `CoreUI.renderMaterialModal`, y `CoreUI.getData`.
- Comunica con el servidor a través de una API (`/api/ubicaciones/${encodeURIComponent(val)}`) para obtener datos de ubicación.

El archivo no utiliza ORM ni consultas SQL crudas.

