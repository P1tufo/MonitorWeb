## Archivo: ./core/auth.py

### Resumen Funcional
Este archivo `auth.py` contiene las funcionalidades de autenticación y seguridad JWT/OAuth2 para el sistema de monitoreo de almacén (WMS). Define modelos, esquemas, funciones de hashing de contraseñas, gestión de tokens JWT, dependencias FastAPI para proteger endpoints y lógica para crear y gestionar usuarios administradores.

### Catálogo de Funciones y Clases
- `hash_password(plain: str) -> str`: Genera un hash bcrypt del password.
- `verify_password(plain: str, hashed: str) -> bool`: Verifica un password contra su hash bcrypt.
- `create_access_token(username: str, role: str) -> tuple[str, int]`: Crea un JWT firmado con HS256 y retorna el token y la duración de expiración.
- `decode_token(token: str) -> Optional[dict]`: Decodifica y valida un JWT. Retorna None si es inválido o expirado.
- `get_current_user(token: Optional[str] = Depends(oauth2_scheme), request: Request = None, db: Session = Depends(get_session_dep)) -> User`: Dependencia que extrae el usuario del token JWT.
- `require_auth(user: User = Depends(get_current_user)) -> User`: Dependencia que EXIGE un usuario autenticado (no invitado).
- `require_admin(user: User = Depends(require_auth)) -> User`: Dependencia que EXIGE rol de administrador. Lanza 403 si no tiene permisos.
- `init_auth_db()`: Crea las tablas de autenticación si no existen.
- `ensure_admin_exists()`: Crea el usuario admin por defecto si no existe ningún usuario.

### Contratos de API / Endpoints
No aplica. Este archivo no define rutas HTTP.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Operaciones**:
  - **Tabla afectada**: `User`
  - **Tipo de operación**: SELECT/INSERT
  - **Columnas leídas o escritas**: `username`, `password_hash`, `role`, `is_active`, `created_at`

### Flujo de Datos y Pipeline
No aplica. Este archivo no procesa, transforma o mueve datos.

### Caché y Estado
- **Variables globales y de módulo**:
  - `SECRET_KEY`: Clave secreta para JWT.
  - `ALGORITHM`: Algoritmo de codificación JWT.
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Duración de expiración del token JWT.
- **Caché en memoria**: No aplica.
- **Caché persistente**: No aplica.
- **Mecanismos de invalidación de caché**: No aplica.
- **Variables de entorno o sesión utilizadas**:
  - `JWT_SECRET_KEY`: Clave secreta para JWT.
  - `JWT_EXPIRE_MINUTES`: Duración de expiración del token JWT.
  - `ADMIN_USERNAME`: Nombre de usuario administrador por defecto.
  - `ADMIN_PASSWORD`: Contraseña administrador por defecto.

### Lógica de Negocio y Reglas
- **Diccionarios o mapeos hardcoded**:
  - `roles`: Mapeo de roles disponibles (`admin`, `viewer`).
- **Constantes de negocio o umbrales**:
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Duración de expiración del token JWT.
- **Fórmulas de cálculo o reglas de validación**: No aplica.
- **Expresiones CASE/condicionales que implementan reglas de dominio**:
  - Verificación de rol en `require_admin`.
  - Creación de usuario invitado en `get_current_user`.

### Dependencias y Flujo
- **Librerías externas**:
  - `bcrypt`: Para hashing de contraseñas.
  - `jwt`: Para gestión de tokens JWT.
  - `fastapi.security.OAuth2PasswordBearer`: Para manejo de tokens OAuth2.
  - `sqlalchemy.orm.Session`: Para operaciones con la base de datos.
- **Archivos del proyecto que ESTE archivo IMPORTA (consume)**:
  - `core.database.get_session_dep`
  - `core.database.engine`
  - `core.database.Base`
  - `core.models_auth.User`
- **Archivos del proyecto que IMPORTAN a este archivo (lo consumen)**:
  - No aplica.

Este archivo es fundamental para la seguridad y autenticación en el sistema de monitoreo de almacén, proporcionando mecanismos robustos para gestionar usuarios y proteger endpoints sensibles.

