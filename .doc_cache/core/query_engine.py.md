## Archivo: ./core/query_engine.py (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
Este archivo `query_engine.py` es el motor de construcción de SQL seguro para el Analytics Studio. Centraliza la lista blanca de tablas permitidas, la validación dinámica de identificadores (tablas y columnas) contra el esquema real de la BD, y la construcción parametrizada de SQL con FROM, JOIN, WHERE, agregaciones, eje temporal y desglose por series.

### Catálogo de Funciones y Clases
- `validate_identifier(name: str, db: Session) -> bool`: Valida que un identificador (tabla o tabla.columna) pertenezca a la lista blanca.
- `validate_column(table: str, column: str, db: Session) -> bool`: Valida que una columna pertenezca a una tabla permitida.
- `get_table_columns(table: str, db: Session) -> List[str]`: Retorna la lista de columnas de una tabla permitida.
- `get_bound_params_from_visual_state(visual_state_str: str) -> list`: Extrae los bind params (?) de un visual_state JSON serializado.
- `extract_metric_value(df, active_year: str = None)`: Extrae el valor numérico principal de un DataFrame de resultado de query.
- `build_sql_from_payload(payload, db: Session, drilldown_segment: Optional[str] = None, drilldown_material: Optional[str] = None) -> Tuple[str, List]`: Compila un VisualQueryBuilderPayload validado en una tupla (sql_text, bound_params).

### Interacción con Base de Datos
- Motor de base de datos: SQLAlchemy.
- Tablas permitidas: `outbound_deliveries`, `stock_levels`, `warehouse_tasks`, `inventory_movements`.
- Consultas SQL crudas: Utiliza `PRAGMA table_info` para validar columnas.

### Estado y Variables Globales
- Variables globales: No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sqlalchemy`
  - `fastapi`
- Comunicación con otros archivos del proyecto:
  - `routes/settings.py::api_build_sql` → llama a `build_sql_from_payload()`.
  - `core/security.py::validate_table` → valida nombres de tabla en ETL (sin cambios).
  - `core/utils.py` → utilidades JSON y métricas (sin cambios).

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `query_engine.py` genera consultas SQL dinámicas basadas en los parámetros proporcionados en el objeto `payload`. La consulta puede incluir agrupaciones y ordenamientos según las necesidades del usuario.

### Catálogo de Funciones y Clases
- `generate_query(payload)` - Genera una consulta SQL dinámica basada en los parámetros del objeto `payload`.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `AREA_EXPR_MACRO` - Una macro global que puede ser inyectada en la consulta SQL.

### Dependencias y Flujo
- Depende de las variables globales `time_func`, `breakdown_select`, `metrics_select_str`, `from_clause`, `where_str`, `groupby_str`, `payload.baseTable`.
- No comunica con otros archivos del proyecto.

