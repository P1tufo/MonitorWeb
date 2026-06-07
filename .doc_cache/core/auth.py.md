## Archivo: ./core/auth.py

### Resumen Funcional
El archivo `auth.py` proporciona funcionalidades de autenticación y seguridad utilizando JWT (JSON Web Tokens) y OAuth2 para un sistema de monitoreo de almacén (WMS). Incluye funciones para crear, verificar y gestionar tokens JWT, así como dependencias FastAPI para proteger endpoints según el rol del usuario.

### Catálogo de Funciones y Clases
- `hash_password(plain: str) -> str` - Genera un hash bcrypt del password.
- `verify_password(plain: str, hashed: str) -> bool` - Verifica un password contra su hash bcrypt.
- `create_access_token(username: str, role: str) -> tuple[str, int]` - Crea un JWT firmado con HS256 y retorna el token y la duración de expiración.
- `decode_token(token: str) -> Optional[dict]` - Decodifica y valida un JWT. Retorna None si es inválido o expirado.
- `get_current_user(token: Optional[str] = Depends(oauth2_scheme), request: Optional[Request] = None, db: Session = Depends(get_session_dep)) -> User` - Dependencia que extrae el usuario del token JWT y retorna un usuario 'invitado' si no hay token válido.
- `require_auth(user: User = Depends(get_current_user)) -> User` - Dependencia que EXIGE un usuario autenticado (no invitado).
- `require_admin(user: User = Depends(require_auth)) -> User` - Dependencia que EXIGE rol de administrador. Lanza 403 si no tiene permisos.
- `init_auth_db()` - Crea las tablas de autenticación si no existen.
- `ensure_admin_exists()` - Crea el usuario admin por defecto si no existe ningún usuario.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `User` (columnas: id, username, password_hash, role, is_active, created_at)
- Consultas SQL crudas o llamadas a ORM:
  - `db.query(User).filter(User.username == username, User.is_active).first()`
  - `session.query(User).count()`

### Estado y Variables Globales
- Variables globales:
  - `SECRET_KEY` (debe cambiarse en producción)
  - `ALGORITHM`
  - `ACCESS_TOKEN_EXPIRE_MINUTES`
- Variables de sesión: Ninguna
- Variables de entorno: Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `bcrypt`
  - `jwt`
  - `fastapi`
  - `pydantic`
  - `sqlalchemy`
- Archivos del proyecto que ESTE archivo IMPORTA (consume):
  - `core.database`
  - `core.models_auth`
- Archivos del proyecto que IMPORTAN a este archivo (lo consumen): Ninguno
- Flujo de datos:
  - Dependencias FastAPI (`get_current_user`, `require_auth`, `require_admin`) consumen funciones para autenticación y autorización.
  - Funciones para crear tokens JWT utilizan dependencias como `bcrypt` y `jwt`.
  - Inicializaciones (`init_auth_db`, `ensure_admin_exists`) interactúan con la base de datos.

