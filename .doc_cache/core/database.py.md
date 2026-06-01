## Archivo: ./core/database.py

### Resumen Funcional
Este archivo es el punto de entrada para acceder a la capa ORM del sistema, utilizando SQLAlchemy. Soporta SQLite (desarrollo local) y PostgreSQL (producción SaaS) mediante la variable de entorno `DATABASE_URL`. Proporciona funciones para obtener sesiones de base de datos y realizar un chequeo de salud.

### Catálogo de Funciones y Clases
- `get_session() -> Generator[Session, None, None]`: Context manager que entrega una sesión SQLAlchemy. Garantiza commit en éxito y rollback automático en excepción.
- `get_session_dep() -> Generator[Session, None, None]`: Dependencia de FastAPI para inyección de sesiones en endpoints.
- `health_check() -> bool`: Verifica la conectividad con la base de datos. Retorna True si OK.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
- **Motor**: SQLite/Postgres (dependiendo de `DATABASE_URL`)
- **Operaciones**:
  - `SELECT` para verificar la salud de la base de datos (`health_check()`)

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
- **Variables globales y de módulo**: `engine`, `SessionLocal`
- **Caché en memoria**: No aplicable
- **Caché persistente**: No aplicable
- **Mecanismos de invalidación de caché**: No aplicable
- **Variables de entorno o sesión utilizadas**: `DATABASE_URL`

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- **Librerías externas**:
  - `sqlalchemy`
  - `logging`
  - `contextlib`
  - `typing`
  - `os`
- **Archivos del proyecto que ESTE archivo IMPORTA (consume)**: No aplicable
- **Archivos del proyecto que IMPORTAN a este archivo (lo consumen)**:
  - `config.py` (para `DB_PATH`)
  - Endpoints FastAPI que utilizan `get_session_dep()`

