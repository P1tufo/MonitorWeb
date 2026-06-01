## Archivo: ./core/query_engine.py

### Resumen Funcional
Este archivo actúa como una fachada para el motor de SQL, proporcionando una interfaz para construir y ejecutar consultas SQL seguras y validadas en un sistema de monitoreo de almacén (WMS) utilizando FastAPI, SQLAlchemy y SQLite.

### Catálogo de Funciones y Clases
- `validate_identifier(identifier)` - Valida si el identificador proporcionado es válido.
- `validate_column(column_name, table_name)` - Valida si la columna pertenece a la tabla especificada.
- `get_table_columns(table_name)` - Obtiene las columnas de una tabla específica.
- `ALLOWED_TABLES` - Lista de tablas permitidas para consultas.
- `ALLOWED_AGGREGATIONS` - Lista de agregaciones permitidas en consultas.
- `ALLOWED_GRANULARITIES` - Lista de granularidades permitidas en consultas.
- `get_bound_params_from_visual_state(visual_state)` - Extrae los parámetros limitados desde el estado visual.
- `extract_metric_value(metric_data)` - Extrae el valor de una métrica de los datos proporcionados.
- `build_sql_from_payload(payload, area_expr_macro=AREA_EXPR_MACRO)` - Construye una consulta SQL a partir del payload proporcionado.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con la base de datos.

### Estado y Variables Globales
Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en el código que almacenen estado crítico.

### Dependencias y Flujo
- **Dependencias Externas**: `core.query_validators`, `core.query_utils`, `core.query_builder`.
- **Archivos del Proyecto Importados por Este Archivo**:
  - No aplica.
- **Archivos del Proyecto que Importan a Este Archivo**:
  - No aplica.

El flujo de datos es unidireccional, con este archivo proporcionando funciones y utilidades para construir consultas SQL seguras en el sistema WMS.

