## Archivo: ./repositories/base.py

### Resumen Funcional
Clase base para todos los repositorios de datos en el sistema WMS. Proporciona métodos para manejar consultas SQL y verificar el estado visual de las mismas.

### Catálogo de Funciones y Clases
- `BaseRepository(session: Session)` - Inicializa la instancia con una sesión de SQLAlchemy.
- `_sql(query_id: str, fallback: str) -> str` - Devuelve un texto SQL basado en un ID de consulta o un valor de reemplazo (fallback).
- `_has_visual_state(query_id: str) -> bool` - Verifica si una consulta tiene un estado visual JSON almacenado.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos.

### Estado y Variables Globales
Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Dependencias**: `sqlalchemy.orm.Session`, `core.db_config_manager.get_query_visual_state`.
- **Flujo de Datos**: El archivo no consume ni produce datos externos. Es una clase base para otros repositorios que pueden interactuar con la base de datos a través de las sesiones proporcionadas.

