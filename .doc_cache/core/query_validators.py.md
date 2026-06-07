## Archivo: ./core/query_validators.py

### Resumen Funcional
El archivo `query_validators.py` contiene funciones para validar identificadores (tablas y columnas) en el contexto de un sistema de monitoreo de almacén (WMS). Las funciones verifican si los nombres proporcionados están dentro de listas blancas predefinidas y, en caso de ser columnas, consultan la base de datos para asegurarse de su existencia.

### Catálogo de Funciones y Clases
- `validate_identifier(name: str, db: Session) -> bool` - Valida que un identificador (tabla o tabla.columna) pertenezca a la lista blanca. Si es una columna, consulta la base de datos para verificar su existencia.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna
- Columnas: Ninguna

### Estado y Variables Globales
- `ALLOWED_TABLES` - Conjunto inmutable de tablas permitidas.
- `ALLOWED_AGGREGATIONS` - Conjunto inmutable de agregaciones permitidas.
- `ALLOWED_GRANULARITIES` - Conjunto inmutable de granularidades permitidas.

### Dependencias y Flujo
- Librerías externas: `logging`, `typing`
- Archivos del proyecto que IMPORTA a este archivo:
  - `routes/settings.py`
  - `core/security.py`

Este archivo no importa archivos del proyecto, pero es consumido por otros archivos dentro del proyecto.

