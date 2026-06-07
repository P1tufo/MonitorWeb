## Archivo: ./repositories/base.py

### Resumen Funcional
Clase base para todos los repositorios de datos en el sistema WMS. Proporciona métodos para interactuar con la sesión de SQLAlchemy y verificar el estado visual de consultas.

### Catálogo de Funciones y Clases
- `BaseRepository(session: Session)` - Inicializa una instancia del repositorio con una sesión de SQLAlchemy.
- `_sql(query_id: str, fallback: str) -> str` - Devuelve un texto SQL basado en el ID de la consulta o un valor de reemplazo (fallback).
- `_has_visual_state(query_id: str) -> bool` - Verifica si una consulta tiene un estado visual JSON almacenado.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos.

### Estado y Variables Globales
Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Dependencias**: `sqlalchemy.orm.Session`, `core.db_config_manager.get_query_visual_state`.
- **Flujo de Datos**: El archivo no consume ni produce datos externos. Se utiliza para proporcionar métodos comunes a los repositorios de datos en el sistema WMS.

