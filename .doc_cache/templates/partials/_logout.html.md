## Archivo: ./templates/partials/_logout.html

### Resumen Funcional
El archivo `_logout.html` contiene un fragmento de código JavaScript que se ejecuta cuando el usuario intenta cerrar sesión. Realiza una solicitud asíncrona al backend para notificar la salida del usuario y luego limpia los datos almacenados localmente, finalmente recarga la página para reflejar el cambio.

### Catálogo de Funciones y Clases
- `logout()` - Llama a la API para cerrar sesión y limpia los datos locales antes de recargar la página.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- No hay variables globales explícitas mencionadas en el código.

### Dependencias y Flujo
- **Dependencias**: Ninguna.
- **Flujo**: 
  - Este fragmento se ejecuta cuando el usuario intenta cerrar sesión.
  - Llama a la API `/api/auth/logout` para notificar al backend.
  - Limpia los datos de almacenamiento local (`localStorage.removeItem`) y luego recarga la página con `window.location.reload()`.

Este fragmento es parte del proceso de cierre de sesión en el sistema WMS, asegurando que tanto el backend como el frontend estén actualizados y seguros al cerrar una sesión.

