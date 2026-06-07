## Archivo: ./routes/auth.py

### Resumen Funcional
El archivo `auth.py` contiene endpoints para autenticación y gestión de usuarios en un sistema de monitoreo de almacén (WMS) utilizando FastAPI, SQLAlchemy y SQLite. Los endpoints permiten login con username/password, registro de nuevos usuarios (solo por administradores), obtención de información del usuario autenticado, cambio de contraseña y listado de todos los usuarios (también solo para administradores). Además, proporciona una vista HTML para el formulario de login.

### Catálogo de Funciones y Clases
- `login(response: Response, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session_dep))` - Autentica un usuario con username/password y retorna un JWT.
- `logout(response: Response)` - Limpia la cookie de autenticación.
- `get_me(user: User = Depends(require_auth))` - Retorna la información del usuario autenticado.
- `change_password(data: ChangePasswordRequest, db: DBSession, user: User = Depends(require_auth))` - Cambia la contraseña del usuario autenticado.
- `register_user(data: UserCreate, db: DBSession, admin: User = Depends(require_admin))` - Crea un nuevo usuario. Solo accesible por administradores.
- `list_users(db: DBSession, admin: User = Depends(require_admin))` - Lista todos los usuarios del sistema.
- `login_page(request: Request)` - Renderiza la página de login.

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

- **Archivos del Proyecto que Importan a este Archivo (`auth.py`):** Ninguno

- **Archivos del Proyecto que Este Archivo Importa (`auth.py`):**
  - `core.app_instance`
  - `core.auth`
  - `core.database`
  - `core.models_auth`

- **Flujo de Datos:**
  - El archivo importa dependencias necesarias y define endpoints para autenticación y gestión de usuarios.
  - Los endpoints interactúan con la base de datos a través de funciones definidas en otros módulos (`core.auth`, `core.database`, etc.).
  - La interacción con la base de datos se realiza mediante consultas SQL generadas por SQLAlchemy.

Este archivo es crucial para el manejo de autenticación y gestión de usuarios en el sistema WMS, asegurando que solo los usuarios autorizados puedan realizar ciertas acciones y proporcionando mecanismos seguros para el login y cambio de contraseña.

