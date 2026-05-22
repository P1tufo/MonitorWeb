## Archivo: ./templates/login.html

### Resumen Funcional
El archivo `login.html` es una página de inicio de sesión para la aplicación MonitorWeb. Permite a los usuarios ingresar sus credenciales y autenticarse en el sistema.

### Catálogo de Funciones y Clases
- `handleLogin(event)` - Maneja el evento de envío del formulario de inicio de sesión, realiza la autenticación y redirige al usuario si es exitosa.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: No se utilizan librerías externas.
- **Flujo Interno**: El archivo interactúa con el servidor a través del endpoint `/api/auth/login` para autenticar al usuario. Los datos de inicio de sesión se envían mediante una solicitud POST en formato `application/x-www-form-urlencoded`. Si la autenticación es exitosa, los tokens y detalles del usuario se almacenan en `localStorage`, y el usuario es redirigido a la página principal. En caso de error, se muestra un mensaje de error en la interfaz.

