## Archivo: ./core/wms_utils.py

### Resumen Funcional
Este archivo contiene funciones utilitarias vectorizadas para transformación de datos en un sistema WMS (Warehouse Management System). Incluye operaciones como limpieza de cadenas, mapeos de estados y centros de costo, normalización de fechas y cálculos de retraso.

### Catálogo de Funciones y Clases
- `sanitize_string(text: str) -> str` - Normaliza un string para usarlo como encabezado de columna.
- `map_wms_status(df: pd.DataFrame) -> pd.DataFrame` - Concatena columnas de estado y mapea al valor legible de negocio.
- `apply_cost_center_mapping(df: pd.DataFrame) -> pd.DataFrame` - Clasifica ubicaciones WMS en áreas de negocio de forma vectorizada.
- `normalize_date_columns(df: pd.DataFrame) -> pd.DataFrame` - Estandariza formatos de fecha WMS a dd-mm-yyyy de forma eficiente.
- `calculate_sla_delays(df: pd.DataFrame) -> pd.DataFrame` - Calcula días hábiles de retraso usando lógica vectorizada de NumPy.
- `generate_time_labels(df: pd.DataFrame) -> pd.DataFrame` - Genera etiquetas de semana ISO para visualización y analítica.
- `_manifest_execute(session_or_conn, sql: str, params: dict)` - Ejecuta una query de manifiesto sobre Session SQLAlchemy o sqlite3.Connection.
- `is_file_changed(session_or_conn, file_path: Path) -> bool` - Verifica si un archivo ha cambiado desde la última sincronización.
- `mark_file_processed(session_or_conn, file_path: Path, row_count: Optional[int] = None)` - Marca un archivo como procesado en el manifiesto.

### Interacción con Base de Datos
- Motor: SQLAlchemy (puede interactuar con SQLite o otras bases de datos compatibles).
- Tablas:
  - `sync_manifest` (Tabla utilizada para almacenar información sobre archivos procesados, incluyendo su ruta, tamaño, última modificación y número de filas procesadas).

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas: `re`, `logging`, `numpy`, `pandas`, `datetime`, `pathlib`, `typing`.
- Comunicación con otros archivos:
  - `core.wms_config`: Para mapeos de estados y centros de costo.
  - `core.db_config_manager`: Para obtener información sobre feriados.

