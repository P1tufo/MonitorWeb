## Archivo: ./core/helpers/dynamic_executor.py

### Resumen Funcional
El archivo `dynamic_executor.py` es un módulo que permite la ejecución de consultas SQL dinámicas a partir de payloads JSON proporcionados por el frontend. Utiliza el motor de consulta `query_engine` para construir y ejecutar las consultas, devolviendo los resultados en forma de DataFrame de Pandas.

### Catálogo de Funciones y Clases
- `execute_visual_query(payload_dict: Dict, db: Session) -> pd.DataFrame` - Toma un payload JSON crudo desde el frontend, lo valida y compila usando el query_engine, y devuelve un DataFrame de Pandas directamente.

### Interacción con Base de Datos
- Motor de base de datos: SQLAlchemy.
- Tablas y Columnas: No aplica (no hay consultas SQL explícitas o llamadas a ORM).
- Consultas SQL Crudas: Sí, se genera una consulta SQL dinámica a través del `query_engine`.
- Llamadas a ORM: Sí, se utiliza el método `build_sql_from_payload` del módulo `core.query_engine`.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas`: Para manejar los DataFrames.
  - `logging`: Para registrar errores.
  - `typing.Dict`: Para tipar el parámetro de entrada.
  - `sqlalchemy.orm.Session`: Para la sesión de base de datos.
  
- Flujo hacia otros archivos del proyecto:
  - `core.query_engine.build_sql_from_payload`: Se utiliza para construir la consulta SQL dinámica.

