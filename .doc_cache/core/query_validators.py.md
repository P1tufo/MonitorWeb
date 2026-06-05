## Archivo: ./core/query_validators.py

### Resumen Funcional
Este archivo contiene funciones para validar identificadores de tablas y columnas en un sistema de monitoreo de almacén (WMS) utilizando FastAPI, SQLAlchemy y SQLite. Las funciones garantizan que solo se acceda a tablas y columnas permitidas, evitando así inyecciones SQL.

### Catálogo de Funciones y Clases
- `validate_identifier(name: str, db: Session) -> bool` - Valida si un identificador (tabla o tabla.columna) pertenece a la lista blanca.
- `validate_column(table: str, column: str, db: Session) -> bool` - Valida si una columna pertenece a una tabla permitida.
- `get_table_columns(table: str, db: Session) -> List[str]` - Retorna la lista de columnas de una tabla permitida.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `outbound_deliveries`
  - `stock_levels`
  - `warehouse_tasks`
  - `inventory_movements`
- Columnas:
  - Consulta dinámica a través de `PRAGMA table_info(table_name)` para verificar la existencia de columnas.

### Estado y Variables Globales
- `ALLOWED_TABLES` (frozenset): Lista blanca de tablas permitidas.
- `ALLOWED_AGGREGATIONS` (frozenset): Conjunto de agregaciones permitidas.
- `ALLOWED_GRANULARITIES` (frozenset): Granularidades permitidas.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `sqlalchemy.orm.Session`
  - `sqlalchemy.text`
  - `typing.List`
  - `logging`

- **Archivos del Proyecto que Importan a este Archivo**:
  - No se mencionan archivos específicos.

- **Archivos del Proyecto que Este Archivo Importa**:
  - No se mencionan archivos específicos.

- **Flujo de Datos**: 
  - El archivo interactúa con la base de datos para validar identificadores y columnas, utilizando consultas SQL dinámicas.

