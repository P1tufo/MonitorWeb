## Archivo: ./tests/test_queries.py

### Resumen Funcional
El archivo `test_queries.py` contiene pruebas unitarias para funciones que interactúan con una base de datos SQLite, específicamente para contar días activos y calcular estadísticas por área de negocio.

### Catálogo de Funciones y Clases
- `test_get_total_active_days(test_db: sqlite3.Connection) -> None`: Verifica el conteo de días únicos con actividad filtrado por año usando fechas ISO.
- `test_get_total_active_days_empty(test_db: sqlite3.Connection) -> None`: Verifica que el conteo de días activos devuelva 0 cuando la tabla está vacía.
- `test_get_area_stats(test_db: sqlite3.Connection) -> None`: Verifica el cálculo de KPIs (ontime/late) agrupados por área de negocio.
- `test_area_expr_fallback_locations(test_db: sqlite3.Connection) -> None`: Verifica que el mapeo de área resuelva correctamente usando las columnas de fallback.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: `outbound_deliveries`
- **Columnas**:
  - `entrega`
  - `fecha_carga`
  - `area_negocio`
  - `dias_retraso`
  - `ubicacion_area`
  - `ubicacion_bin_1`
  - `ubicacion_bin`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- **Librerías Externas**: `pytest`, `sqlite3`, `pandas`
- **Flujo Interno**: El archivo interactúa con el módulo `core.queries_deliveries` para ejecutar consultas y validar resultados.

