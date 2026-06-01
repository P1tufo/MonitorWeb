## Archivo: ./core/wms_utils.py

### Resumen Funcional
Este archivo `wms_utils.py` contiene funciones utilitarias vectorizadas para transformación de datos en un sistema de monitoreo de almacén (WMS). Estas funciones se utilizan para limpiar, mapear y normalizar datos, así como calcular métricas y marcar archivos procesados.

### Catálogo de Funciones y Clases
- `sanitize_string(text: str) -> str`: Normaliza un string para usarlo como encabezado de columna.
- `map_wms_status(df: pd.DataFrame) -> pd.DataFrame`: Concatena columnas de estado y mapea al valor legible de negocio.
- `apply_cost_center_mapping(df: pd.DataFrame) -> pd.DataFrame`: Clasifica ubicaciones WMS en áreas de negocio de forma vectorizada.
- `normalize_date_columns(df: pd.DataFrame) -> pd.DataFrame`: Estandariza formatos de fecha WMS a dd-mm-yyyy de forma eficiente.
- `calculate_sla_delays(df: pd.DataFrame) -> pd.DataFrame`: Calcula días hábiles de retraso usando lógica vectorizada de NumPy.
- `generate_time_labels(df: pd.DataFrame) -> pd.DataFrame`: Genera etiquetas de semana ISO para visualización y analítica.
- `_manifest_execute(session_or_conn, sql: str, params: dict)`: Ejecuta una query de manifiesto sobre Session SQLAlchemy o sqlite3.Connection.
- `is_file_changed(session_or_conn, file_path: Path) -> bool`: Verifica si un archivo ha cambiado desde la última sincronización.
- `mark_file_processed(session_or_conn, file_path: Path, row_count: Optional[int] = None)`: Marca un archivo como procesado en el manifiesto.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Operaciones SQL**:
  - `SELECT last_modified, file_size FROM sync_manifest WHERE file_path = :path`
  - `INSERT INTO sync_manifest (file_path, last_modified, file_size, processed_at, row_count) ... ON CONFLICT(file_path) DO UPDATE SET ...`

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
- **Variables globales y de módulo**: `RE_CLEAN`, `RE_UNSAFE`, `RE_DATE_DOT`
- **Caché en memoria**: No aplica.
- **Caché persistente**: No aplica.
- **Mecanismos de invalidación de caché**: No aplica.
- **Variables de entorno o sesión utilizadas**: No aplica.

### Lógica de Negocio y Reglas
- **Diccionarios o mapeos hardcoded**:
  - `STATUS_MAPPING`: Mapeo de estados WMS a valores legibles de negocio.
  - `COST_CENTER_MAPPING`: Mapeo de centros de costo a áreas de negocio.
- **Constantes de negocio o umbrales**: No aplica.
- **Fórmulas de cálculo o reglas de validación**: No aplica.
- **Expresiones CASE/condicionales que implementan reglas de dominio**: No aplica.

### Dependencias y Flujo
- **Librerías externas**:
  - `re`, `logging`, `numpy`, `pandas`, `datetime`, `pathlib`, `typing`
- **Archivos del proyecto que ESTE archivo IMPORTA (consume)**: `core.wms_config`, `core.db_config_manager`
- **Archivos del proyecto que IMPORTAN a este archivo (lo consumen)**: No aplica
- **Dirección del flujo de datos**: No aplica.

