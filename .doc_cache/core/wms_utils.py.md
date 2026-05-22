## Archivo: ./core/wms_utils.py

### Resumen Funcional
Este archivo contiene funciones utilitarias vectorizadas para transformación de datos WMS, incluyendo limpieza de datos, mapeos de negocio, normalización y cálculos métricos.

### Catálogo de Funciones y Clases
- `sanitize_string(text: str) -> str` - Normaliza un string para usarlo como encabezado de columna.
- `map_wms_status(df: pd.DataFrame) -> pd.DataFrame` - Concatena columnas de estado y mapea al valor legible de negocio.
- `apply_cost_center_mapping(df: pd.DataFrame) -> pd.DataFrame` - Clasifica ubicaciones WMS en áreas de negocio de forma vectorizada.
- `normalize_date_columns(df: pd.DataFrame) -> pd.DataFrame` - Estandariza formatos de fecha WMS a dd-mm-yyyy de forma eficiente.
- `calculate_sla_delays(df: pd.DataFrame) -> pd.DataFrame` - Calcula días hábiles de retraso usando lógica vectorizada de NumPy.
- `generate_time_labels(df: pd.DataFrame) -> pd.DataFrame` - Genera etiquetas de semana ISO para visualización y analítica.
- `is_file_changed(session: Session, file_path: Path) -> bool` - Verifica si un archivo ha cambiado desde la última sincronización.
- `mark_file_processed(session: Session, file_path: Path, row_count: Optional[int] = None)` - Marca un archivo como procesado exitosamente en el manifiesto.

### Interacción con Base de Datos
- Motor: SQLAlchemy ORM
- Tablas:
  - `sync_manifest`
- Columnas:
  - `file_path`, `last_modified`, `file_size`, `processed_at`, `row_count`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: `re`, `logging`, `numpy`, `pandas`, `datetime`, `pathlib`, `typing`
- Comunicación con otros archivos del proyecto:
  - `core.wms_config`: Para mapeos de estado y centro de costo.
  - `core.db_config_manager`: Para obtener feriados.

