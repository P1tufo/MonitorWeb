## Archivo: ./tests/test_queries.py

### Resumen Funcional
El archivo `test_queries.py` contiene pruebas unitarias para verificar la funcionalidad de un repositorio que interactúa con una base de datos SQLite. Las pruebas cubren el conteo de días activos, cálculo de KPIs agrupados por área de negocio y la compilación correcta de consultas SQL a partir de payloads.

### Catálogo de Funciones y Clases
- `test_get_total_active_days(test_db: sqlite3.Connection) -> None` - Verifica el conteo de días únicos con actividad filtrado por año usando fechas ISO.
- `test_get_total_active_days_empty(test_db: sqlite3.Connection) -> None` - Verifica que la función retorne 0 si no hay registros.
- `test_get_area_stats(test_db: sqlite3.Connection) -> None` - Verifica el cálculo de KPIs (ontime/late) agrupados por área de negocio.
- `test_area_expr_fallback_locations(test_db: sqlite3.Connection) -> None` - Verifica la asignación correcta de áreas basada en ubicaciones.
- `test_query_engine_compiles_ast_correctly(test_db: sqlite3.Connection) -> None` - Verifica que el motor de consultas compile correctamente los ASTs a SQL.

### Interacción con Base de Datos
- Motor de base de datos: SQLite
- Tablas:
  - `outbound_deliveries`
- Columnas:
  - `entrega`, `fecha_carga`, `area_negocio`, `dias_retraso`, `ubicacion_area`, `ubicacion_bin_1`, `ubicacion_bin`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pytest`
  - `sqlite3`
  - `pandas`
- Comunicación con otros archivos del proyecto:
  - `repositories.deliveries.DeliveriesRepository`
  - `core.query_engine.build_sql_from_payload`

