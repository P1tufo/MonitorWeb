## Archivo: ./core/wms_utils.py

### Resumen Funcional
Este archivo contiene funciones utilitarias vectorizadas para transformación de datos en un sistema de monitoreo de almacén (WMS). Las funciones se centran en la limpieza, mapeo y normalización de datos, así como en el cálculo de métricas y la gestión del estado de archivos.

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
- Motor: SQLite
- Tablas:
  - `sync_manifest`
- Columnas:
  - `file_path`, `last_modified`, `file_size`, `processed_at`, `row_count`

### Estado y Variables Globales
- `logger` - Objeto de logging para el módulo.

### Dependencias y Flujo
- Librerías externas: `re`, `logging`, `numpy`, `pandas`, `datetime`, `pathlib`, `typing`.
- Archivos del proyecto que importa:
  - `core.wms_config`
  - `core.db_config_manager`
- Archivos del proyecto que son importados por este archivo:
  - Ninguno
- Flujo de datos: El flujo principal es el procesamiento y transformación de DataFrames, con interacciones ocasionales con la base de datos para gestionar el estado de archivos.

