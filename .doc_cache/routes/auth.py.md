## Archivo: ./routes/auth.py

### Resumen Funcional
Este archivo contiene endpoints para autenticación y gestión de usuarios, incluyendo login, registro, cambio de contraseña, obtención de información del usuario autenticado y listado de usuarios (solo accesible por administradores). También proporciona una vista HTML para el formulario de login.

### Catálogo de Funciones y Clases
- `login(response: Response, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session_dep))` - Autentica un usuario con username/password y retorna un JWT.
- `logout(response: Response, state: AppState = Depends(get_app_state))` - Limpia la cookie de autenticación.
- `get_me(user: User = Depends(require_auth), state: AppState = Depends(get_app_state))` - Retorna la información del usuario autenticado.
- `change_password(data: ChangePasswordRequest, db: DBSession, user: User = Depends(require_auth))` - Cambia la contraseña del usuario autenticado.
- `register_user(data: UserCreate, db: DBSession, admin: User = Depends(require_admin), state: AppState = Depends(get_app_state))` - Crea un nuevo usuario. Solo accesible por administradores.
- `list_users(db: DBSession, admin: User = Depends(require_admin), state: AppState = Depends(get_app_state))` - Lista todos los usuarios del sistema.
- `login_page(request: Request, state: AppState = Depends(get_app_state))` - Renderiza la página de login.

### Interacción con Base de Datos
- Motor: SQLAlchemy ORM
- Tablas:
  - `User`
- Columnas:
  - `id`, `username`, `password_hash`, `role`, `is_active`, `created_at`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: FastAPI, SQLAlchemy ORM.
- Comunicación con otros archivos del proyecto:
  - `core.database.get_session_dep` para obtener la sesión de base de datos.
  - `core.models_auth.User` para definir el modelo de usuario.
  - `core.auth` para funciones de autenticación y gestión de usuarios.
  - `core.app_instance.templates` para renderizar vistas HTML.

