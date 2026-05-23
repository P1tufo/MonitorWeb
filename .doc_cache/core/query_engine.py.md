## Archivo: ./core/query_engine.py

### Resumen Funcional
Este archivo `query_engine.py` es el motor de construcción de consultas SQL seguras para el Analytics Studio. Centraliza la validación de identificadores (tablas y columnas) contra una lista blanca y construye consultas parametrizadas dinámicamente a partir de un `VisualQueryBuilderPayload`.

### Catálogo de Funciones y Clases
- `validate_identifier(name: str, db: Session)` - Valida que un identificador (tabla o tabla.columna) pertenezca a la lista blanca.
- `validate_column(table: str, column: str, db: Session)` - Valida que una columna pertenezca a una tabla permitida.
- `get_table_columns(table: str, db: Session)` - Retorna la lista de columnas de una tabla permitida.
- `get_bound_params_from_visual_state(visual_state_str: str)` - Extrae los bind params (?) de un visual_state JSON serializado.
- `extract_metric_value(df, active_year: str = None)` - Extrae el valor numérico principal de un DataFrame de resultado de query.
- `build_sql_from_payload(payload, db: Session)` - Compila un VisualQueryBuilderPayload validado en una tupla (sql_text, bound_params).

### Interacción con Base de Datos
- Motor de base de datos: SQLAlchemy
- Tablas permitidas:
  - `outbound_deliveries`
  - `stock_levels`
  - `warehouse_tasks`
  - `inventory_movements`
- Consultas SQL dinámicas que utilizan bind params para evitar inyección SQL.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas: `sqlalchemy`, `fastapi`
- Comunicación con otros archivos:
  - `routes/settings.py::api_build_sql` → llama a `build_sql_from_payload()`
  - `core/security.py::validate_table` → valida nombres de tabla en ETL (sin cambios)
  - `core/utils.py` → utilidades JSON y métricas (sin cambios)

