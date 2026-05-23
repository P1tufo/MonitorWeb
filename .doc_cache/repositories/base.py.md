## Archivo: ./repositories/base.py

### Resumen Funcional
La clase `BaseRepository` proporciona una estructura base para interactuar con bases de datos mediante SQLAlchemy. Define métodos para obtener consultas SQL y verificar el estado visual de las mismas.

### Catálogo de Funciones y Clases
- `__init__(self, session: Session)` - Inicializa la instancia con una sesión de SQLAlchemy.
- `_sql(self, query_id: str, fallback: str) -> str` - Obtiene un SQL desde la base de datos de configuración o devuelve un fallback hardcodeado si no existe.
- `_has_visual_state(self, query_id: str) -> bool` - Verifica si una consulta tiene un estado visual JSON almacenado.

### Interacción con Base de Datos
- Motor: SQLAlchemy
- Tablas: `config_queries`
- Columnas: `query_id`, `sql_text`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sqlalchemy.orm.Session`
  - `core.wms_config.get_query`
  - `core.db_config_manager.get_query_visual_state`
- Comunicación con otros archivos del proyecto:
  - `core/query_engine.build_sql_from_payload()` (mencionado en la documentación, pero no implementado)

