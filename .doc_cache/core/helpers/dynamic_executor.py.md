## Archivo: ./core/helpers/dynamic_executor.py

### Resumen Funcional
El archivo `dynamic_executor.py` contiene una función que toma un payload JSON crudo, lo valida y compila en una consulta SQL utilizando el módulo `query_engine`. Luego ejecuta la consulta en una base de datos SQLite y devuelve los resultados como un DataFrame de Pandas.

### Catálogo de Funciones y Clases
- `execute_visual_query(payload_dict: Dict, db: Session) -> pd.DataFrame` - Toma un payload JSON crudo, lo valida y compila usando el query_engine, y devuelve un DataFrame de Pandas directamente.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna (la consulta SQL se genera dinámicamente)
- Consultas SQL Crudas o Llamadas a ORM: Sí, utiliza `pd.read_sql` para ejecutar la consulta generada por `build_sql_from_payload`.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías Externas:
  - `pandas`
  - `logging`
  - `typing`
  - `sqlalchemy.orm.Session`
- Archivos del Proyecto que Importan a este archivo (lo consumen):
  - No aplica
- Archivos del Proyecto que Este Archivo Importa (consume):
  - `core.query_engine.build_sql_from_payload`
  - `core.schemas.VisualQueryBuilderPayload`

**Flujo de Datos:**
1. El frontend envía un payload JSON crudo.
2. `execute_visual_query` recibe el payload y lo valida contra el esquema `VisualQueryBuilderPayload`.
3. Utiliza `build_sql_from_payload` para generar una consulta SQL dinámica.
4. Ejecuta la consulta en la base de datos SQLite utilizando `pd.read_sql`.
5. Devuelve los resultados como un DataFrame de Pandas.

Este flujo permite que el sistema genere consultas SQL flexibles basadas en los criterios proporcionados por el usuario, lo que es crucial para un sistema de monitoreo de almacén dinámico y adaptable.

