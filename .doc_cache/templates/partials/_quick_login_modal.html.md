## Archivo: ./templates/partials/_quick_login_modal.html

### Resumen Funcional
El archivo `_quick_login_modal.html` es un fragmento de HTML que define una ventana modal para iniciar sesión rápidamente en el sistema de monitoreo de almacén (WMS). La ventana incluye campos para usuario y contraseña, y un botón para enviar los datos. Al enviar el formulario, se realiza una solicitud POST a la API de autenticación del sistema.

### Catálogo de Funciones y Clases
- `handleQuickLogin(event)` - Maneja el envío del formulario de inicio de sesión, realiza la autenticación y actualiza el estado del usuario en el almacenamiento local o recarga la página según sea necesario.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- `localStorage` - Se utilizan para almacenar el token de acceso, nombre de usuario y rol del usuario autenticado.
- `window.handleQuickLogin` - Variable global que expone la función `handleQuickLogin` al ámbito global.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directamente mencionadas en el código.
- **Flujo de Datos**:
  - El archivo se importa en otros archivos del proyecto (no especificados aquí).
  - Otros archivos pueden llamar a la función `handleQuickLogin` para iniciar sesión rápidamente.

El flujo de datos es unidireccional desde el HTML hasta el JavaScript, donde se maneja la autenticación y la actualización del estado del usuario.

