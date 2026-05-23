## Archivo: ./templates/partials/_quick_login_modal.html

### Resumen Funcional
El archivo `_quick_login_modal.html` define un modal de inicio rápido para la sesión, que permite a los usuarios iniciar sesión sin perder sus filtros actuales. El formulario envía las credenciales al servidor y maneja la respuesta para actualizar el estado del usuario en el almacenamiento local o recargar la página según sea necesario.

### Catálogo de Funciones y Clases
- `handleQuickLogin(event)` - Maneja el evento de envío del formulario de inicio rápido, realiza una solicitud POST a la API de autenticación y actualiza el estado del usuario según la respuesta.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: No se utilizan librerías externas.
- **Flujo Interno**: El archivo interactúa con el servidor a través de una solicitud POST al endpoint `/api/auth/login`. La respuesta del servidor se utiliza para actualizar el estado del usuario en el almacenamiento local (`localStorage`) y para determinar si la página debe recargarse o no.

