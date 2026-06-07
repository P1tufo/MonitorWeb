## Archivo: ./core/auth.py

### Resumen Funcional
Este archivo `auth.py` contiene las funcionalidades de autenticación y seguridad para el sistema de monitoreo de almacén (WMS). Implementa la gestión de usuarios, tokens JWT, roles de usuario y dependencias FastAPI para proteger endpoints.

### Catálogo de Funciones y Clases
- `hash_password(plain: str) -> str` - Genera un hash bcrypt del password.
- `verify_password(plain: str, hashed: str) -> bool` - Verifica un password contra su hash bcrypt.
- `create_access_token(username: str, role: str) -> tuple[str, int]` - Crea un JWT firmado con HS256.
- `decode_token(token: str) -> Optional[dict]` - Decodifica y valida un JWT. Retorna None si es inválido o expirado.
- `get_current_user(token: Optional[str] = Depends(oauth2_scheme), request: Request = None, db: Session = Depends(get_session_dep)) -> User` - Dependencia que extrae el usuario del token JWT.
- `require_auth(user: User = Depends(get_current_user)) -> User` - Dependencia que EXIGE un usuario autenticado (no invitado).
- `require_admin(user: User = Depends(require_auth)) -> User` - Dependencia que EXIGE rol de administrador. Lanza 403 si no tiene permisos.
- `init_auth_db()` - Crea las tablas de autenticación si no existen.
- `ensure_admin_exists()` - Crea el usuario admin por defecto si no existe ningún usuario.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `User` (columnas: id, username, password_hash, role, is_active, created_at)
- Consultas SQL crudas o llamadas a ORM: Sí, se usan consultas ORM para leer y escribir en la tabla `User`.

### Estado y Variables Globales
- Variables globales:
  - `SECRET_KEY`: Clave secreta para JWT.
  - `ALGORITHM`: Algoritmo de codificación JWT.
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración del token JWT.

### Dependencias y Flujo
- Librerías externas: `bcrypt`, `jwt`, `fastapi`, `pydantic`.
- Archivos del proyecto que este archivo importa:
  - `core.database`
  - `core.models_auth`
- Archivos del proyecto que importan a este archivo:
  - Ninguno.
- Flujo de datos: El flujo de datos pasa por las funciones y dependencias definidas aquí, desde la autenticación hasta la creación de tokens JWT y la gestión de usuarios.

