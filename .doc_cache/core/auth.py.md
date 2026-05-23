## Archivo: ./core/auth.py

### Resumen Funcional
El archivo `auth.py` proporciona funcionalidades de autenticación y seguridad utilizando JSON Web Tokens (JWT) y OAuth2, con soporte para roles de usuario ('admin' y 'viewer'). Incluye funciones para crear tokens, verificar contraseñas, manejar sesiones de usuarios y proteger endpoints en una aplicación FastAPI.

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
- Motor: SQLAlchemy
- Tablas: `User`
- Columnas:
  - `id` (int)
  - `username` (str)
  - `password_hash` (str)
  - `role` (str)
  - `is_active` (bool)
  - `created_at` (datetime)

### Estado y Variables Globales
- `SECRET_KEY`: Clave secreta para firmar JWT.
- `ALGORITHM`: Algoritmo de firma para JWT.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración del token JWT.

### Dependencias y Flujo
- Librerías externas: `bcrypt`, `jwt`, `fastapi`
- Comunicaciones internas:
  - Conecta con el archivo `database.py` para obtener sesiones de base de datos.
  - Utiliza el modelo `User` definido en `models_auth.py`.

