## Archivo: ./core/database.py

### Resumen Funcional
Este archivo define la fábrica de sesiones SQLAlchemy para el sistema de monitoreo de almacén (WMS). Proporciona funciones para obtener una sesión de base de datos y realizar un chequeo de salud de la base de datos.

### Catálogo de Funciones y Clases
- `get_session()` - Context manager que entrega una sesión SQLAlchemy, garantizando commit en éxito y rollback automático en excepción.
- `get_session_dep()` - Dependencia de FastAPI para inyección de sesiones en endpoints.
- `health_check()` - Verifica la conectividad con la base de datos. Retorna True si OK.

### Interacción con Base de Datos
- Motor de BD: SQLite (desarrollo local) y PostgreSQL (producción SaaS).
- Tablas: Ninguna (no se especifican tablas directamente en este archivo).
- Columnas: Ninguna (no se especifican columnas directamente en este archivo).

### Estado y Variables Globales
- `DATABASE_URL` - Variable de entorno que define la URL de la base de datos. Valor por defecto es SQLite local.
- `_connect_args` - Argumentos de conexión para SQLAlchemy, incluyendo `check_same_thread=False` para SQLite.

### Dependencias y Flujo
- Librerías externas: `sqlalchemy`, `logging`.
- Archivos del proyecto que importan a este archivo:
  - `config.py` (para `DB_PATH`)
- Archivos del proyecto que este archivo importa:
  - Ninguno

El flujo de datos es desde el archivo `database.py` hacia los endpoints de FastAPI que utilizan las dependencias `get_session_dep()` para obtener sesiones de base de datos.

