## Archivo: ./routes/auth.py

### Resumen Funcional
Este archivo contiene endpoints para autenticación y gestión de usuarios en un sistema de monitoreo de almacén (WMS). Ofrece funcionalidades como login, registro de nuevos usuarios, cambio de contraseña y listado de usuarios.

### Catálogo de Funciones y Clases
- `login(response: Response, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session_dep))` - Autentica un usuario con username/password y retorna un JWT.
- `logout(response: Response, state: AppState = Depends(get_app_state))` - Limpia la cookie de autenticación.
- `get_me(user: User = Depends(require_auth), state: AppState = Depends(get_app_state))` - Retorna la información del usuario autenticado.
- `change_password(data: ChangePasswordRequest, db: DBSession, user: User = Depends(require_auth))` - Cambia la contraseña del usuario autenticado.
- `register_user(data: UserCreate, db: DBSession, admin: User = Depends(require_admin), state: AppState = Depends(get_app_state))` - Crea un nuevo usuario. Solo accesible por administradores.
- `list_users(db: DBSession, admin: User = Depends(require_admin), state: AppState = Depends(get_app_state))` - Lista todos los usuarios del sistema.
- `login_page(request: Request, state: AppState = Depends(get_app_state))` - Renderiza la página de login.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `User`
- **Columnas:** 
  - `id`
  - `username`
  - `password_hash`
  - `role`
  - `is_active`
  - `created_at`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - FastAPI
  - SQLAlchemy
  - Python Standard Library (logging, typing)
  
- **Archivos del Proyecto que IMPORTA a este archivo (`auth.py`):** 
  - `core.database`
  - `core.models_auth`
  - `core.auth`
  - `core.app_instance`
  - `core.state`

- **Archivos del Proyecto que ESTE archivo IMPORTA:**
  - Ninguno

- **Dirección del Flujo de Datos:** 
  - Desde el endpoint hasta la base de datos para autenticar y gestionar usuarios.

