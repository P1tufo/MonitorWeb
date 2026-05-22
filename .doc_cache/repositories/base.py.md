## Archivo: ./repositories/base.py

### Resumen Funcional
Clase base para todos los repositorios de datos que proporciona una sesión de SQLAlchemy y un método para obtener consultas SQL desde una configuración.

### Catálogo de Funciones y Clases
- `BaseRepository(session: Session)` - Inicializa la clase con una sesión de SQLAlchemy.
- `_sql(query_id: str, fallback: str) -> str` - Obtiene un SQL desde la BD de configuración, con fallback.

### Interacción con Base de Datos
- Motor: No aplica (no hay consultas SQL crudas o llamadas a ORM explícitas).
- Tablas y Columnas: No aplica (no interactúa directamente con tablas).

### Estado y Variables Globales
- No aplica (no define variables globales, de sesión, de entorno o diccionarios quemados en código que almacenan estado crítico).

### Dependencias y Flujo
- Librerías externas utilizadas: `sqlalchemy.orm.Session`, `core.wms_config.get_query`.
- Comunicación con otros archivos del proyecto: No aplica (no comunica con otros archivos).

