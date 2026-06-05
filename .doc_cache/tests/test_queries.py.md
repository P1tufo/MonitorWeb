## Archivo: ./tests/test_queries.py

### Resumen Funcional
El archivo `test_queries.py` contiene pruebas unitarias para verificar la funcionalidad de consultas y métodos relacionados con el repositorio de entregas (`DeliveriesRepository`) en un sistema de monitoreo de almacén (WMS). Las pruebas incluyen la obtención del número de días activos, estadísticas por área de negocio y la compilación correcta de consultas SQL a partir de payloads.

### Catálogo de Funciones y Clases
- `test_get_total_active_days(test_db: sqlite3.Connection) -> None` - Verifica el conteo de días únicos con actividad filtrado por año usando fechas ISO.
- `test_get_total_active_days_empty(test_db: sqlite3.Connection) -> None` - Verifica que la función retorne 0 si no hay registros.
- `test_get_area_stats(test_db: sqlite3.Connection) -> None` - Verifica el cálculo de KPIs (ontime/late) agrupados por área de negocio.
- `test_area_expr_fallback_locations(test_db: sqlite3.Connection) -> None` - Verifica la asignación correcta de áreas basada en ubicaciones binarias.
- `test_query_engine_compiles_ast_correctly(test_db: sqlite3.Connection) -> None` - Verifica que el motor de consultas compile correctamente los ASTs a SQL.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `outbound_deliveries`
- **Columnas:**
  - `entrega`
  - `fecha_carga`
  - `area_negocio`
  - `dias_retraso`
  - `centro_costo`
  - `ubicacion_bin_1`
  - `ubicacion_bin`

### Estado y Variables Globales
- **Constantes:** 
  - `TEST_YEAR` (`"%2026"`)
  - `AREA_A` (`"ASERRADERO"`)
  - `AREA_B` (`"MOLDURAS"`)
  - `DATE_1` (`"01-05-2026"`)
  - `DATE_2` (`"02-05-2026"`)

### Dependencias y Flujo
- **Librerías Externas:** 
  - `pytest`
  - `sqlite3`
  - `pandas`
- **Archivos del Proyecto que Importan a este Archivo:**
  - `repositories.deliveries.DeliveriesRepository`
  - `core.query_engine.build_sql_from_payload`
  - `core.schemas.VisualQueryBuilderPayload`, `MetricDef`, `TimeAxisDef`, `FilterDef`
- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno
- **Dirección del Flujo de Datos:** 
  - Pruebas unitarias invocan métodos del repositorio y verifican sus resultados.

