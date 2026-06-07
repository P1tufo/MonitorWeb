## Archivo: ./core/models_auth.py

### Resumen Funcional
Este archivo define el modelo ORM para los usuarios del sistema de autenticación, incluyendo campos como nombre de usuario, contraseña hash, rol y estado de actividad.

### Catálogo de Funciones y Clases
- `User` - Define la tabla de usuarios con sus atributos y métodos.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: `auth_users`
  - Columnas:
    - `id`: Entero, clave primaria, autoincremental.
    - `username`: Cadena (50 caracteres), único, no nulo, índice.
    - `password_hash`: Cadena (255 caracteres), no nula.
    - `role`: Cadena (20 caracteres), no nula, valor por defecto "viewer".
    - `is_active`: Booleano, valor por defecto True.
    - `created_at`: Fecha y hora UTC, valor por defecto la fecha actual.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- Importa: `Base` desde `core.database`.
- No importa a otros archivos del proyecto.
- Es consumido por los servicios de autenticación.

