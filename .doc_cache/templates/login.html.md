## Archivo: ./templates/login.html

### Resumen Funcional
El archivo `login.html` es una página de inicio de sesión para el sistema de monitoreo de almacén (WMS). Permite a los usuarios ingresar sus credenciales y autenticarse en la aplicación.

### Catálogo de Funciones y Clases
- **handleLogin(event)** - Maneja el evento de envío del formulario de inicio de sesión, realiza una solicitud POST a la API para autenticar al usuario y maneja la respuesta.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- **localStorage** - Se utilizan variables globales en el almacenamiento local del navegador para guardar el token de acceso, nombre de usuario y rol del usuario autenticado.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas mencionadas.
- **Flujo**: El archivo `login.html` se importa por la vista correspondiente en FastAPI. La función `handleLogin` es llamada cuando el formulario de inicio de sesión se envía, lo que desencadena una solicitud POST a `/api/auth/login`. La respuesta del servidor maneja la autenticación y redirige al usuario según sea necesario.

