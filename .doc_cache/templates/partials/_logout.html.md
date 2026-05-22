## Archivo: ./templates/partials/_logout.html

### Resumen Funcional
Este fragmento de código HTML contiene un script que define una función `logout` para cerrar la sesión del usuario. La función intenta notificar al backend mediante una solicitud POST a la ruta `/api/auth/logout`, limpia el almacenamiento local (tokens y datos de usuario) y redirige al usuario al Dashboard.

### Catálogo de Funciones y Clases
- `logout()` - Limpia el estado del usuario y cierra sesión.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales en este fragmento de código.

### Dependencias y Flujo
- **Librerías Externas**: `fetch` (navegador).
- **Flujo Interno**: La función `logout` no depende de otros archivos del proyecto directamente, pero interactúa con el backend a través de una solicitud HTTP.

