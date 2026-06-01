## Archivo: ./core/models_auth.py

### Resumen Funcional
Este archivo define el modelo ORM para los usuarios del sistema de autenticación, incluyendo sus atributos y relaciones con la base de datos.

### Catálogo de Funciones y Clases
- `User` (id: int, username: str, password_hash: str, role: str, is_active: bool, created_at: datetime) -> Mapped[User]
  - **Propósito**: Representa una tabla en la base de datos que almacena información sobre los usuarios del sistema.
  - **Métodos Principales**:
    - `__repr__`: Devuelve una representación legible del objeto.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Operaciones SQL/ORM Detectadas**:
  - **Tabla Afectada**: `auth_users`
  - **Tipo de Operación**: SELECT, INSERT, UPDATE
  - **Columnas Leídas o Escritas**:
    - id (Integer)
    - username (String(50))
    - password_hash (String(255))
    - role (String(20))
    - is_active (Boolean)
    - created_at (DateTime)

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
- **Variables Globales y de Módulo**: No aplica.
- **Caché en Memoria**: No aplica.
- **Caché Persistente**: No aplica.
- **Mecanismos de Invalidación de Caché**: No aplica.
- **Variables de Entorno o Sesión Utilizadas**: No aplica.

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlalchemy`
  - `datetime`
- **Archivos del Proyecto que IMPORTA a este archivo (lo consumen)**: No aplica.
- **Archivos del Proyecto que ESTE archivo IMPORTA**: 
  - `database.py` (importado como `from .database import Base`)
- **Dirección del Flujo de Datos**: Este archivo es un modelo ORM y no realiza operaciones directamente sobre la base de datos o el flujo de datos.

