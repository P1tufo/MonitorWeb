## Archivo: ./core/helpers/dynamic_executor.py

### Resumen Funcional
El archivo `dynamic_executor.py` contiene una función que toma un payload JSON crudo, lo valida y compila en una consulta SQL utilizando el módulo `query_engine`. Luego ejecuta la consulta en una base de datos SQLite y devuelve los resultados como un DataFrame de Pandas.

### Catálogo de Funciones y Clases
- `execute_visual_query(payload_dict: Dict, db: Session) -> pd.DataFrame` - Toma un payload JSON crudo, lo valida y compila usando el query_engine, y devuelve un DataFrame de Pandas directamente.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna (se espera que la consulta SQL genere los resultados necesarios).
- Consultas SQL Crudas o Llamadas a ORM: Sí, utiliza `pd.read_sql` para ejecutar la consulta SQL generada.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías Externas:
  - `pandas`
  - `sqlalchemy.orm.Session`
- Archivos del Proyecto que Importan a este Archivo: Ninguno
- Archivos del Proyecto que Este Archivo Importa:
  - `core.query_engine.build_sql_from_payload`
  - `core.schemas.VisualQueryBuilderPayload`

**Flujo de Datos:**
1. El archivo se importa en algún lugar dentro del proyecto.
2. Se llama a la función `execute_visual_query` con un payload JSON y una sesión de base de datos.
3. La función valida el payload, compila una consulta SQL usando `build_sql_from_payload`, ejecuta la consulta en la base de datos y devuelve los resultados como un DataFrame de Pandas.

