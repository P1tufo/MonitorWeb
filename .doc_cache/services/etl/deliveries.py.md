## Archivo: ./services/etl/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene una clase `OutboundDeliveryAdapter` que extiende `BaseWMSProcessor`. Esta clase se encarga de procesar archivos de entregas de salida (Deliveries) en un sistema de gestión de almacén (WMS). El proceso incluye la validación del archivo, la limpieza y transformación de los datos, así como la inserción o actualización de estos datos en una base de datos SQLite.

### Catálogo de Funciones y Clases
- `OutboundDeliveryAdapter(BaseWMSProcessor)` - Adaptador para procesar Entregas de Salida (Deliveries).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y tiene una extensión permitida.
  - `_get_required_columns() -> List[str]` - Devuelve las columnas requeridas en el DataFrame.
  - `_get_primary_keys() -> List[str]` - Devuelve las claves primarias utilizadas para la deduplicación.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y transforma el DataFrame de entrada.
  - `_sanitizar_nombres_columnas(columns: pd.Index) -> list` - Sanitiza los nombres de las columnas del DataFrame.
  - `_post_process(conn, table_name: str)` - Crea índices adicionales en la tabla especificada.
  - `_upsert_chunk(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str)` - Inserta o actualiza datos en la base de datos SQLite.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas modificadas:
  - `outbound_deliveries`
- Columnas modificadas:
  - Todas las columnas presentes en el DataFrame, incluyendo nuevas columnas dinámicas.
- Consultas SQL crudas:
  - `CREATE INDEX IF NOT EXISTS idx_out_ceco_upper ON outbound_deliveries(UPPER(TRIM(centro_costo)))`
  - `PRAGMA table_info({table_name})`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- Librerías externas:
  - `pandas`
  - `pathlib`
  - `typing`
  - `sqlite3`
- Archivos del proyecto que importan a este archivo (`deliveries.py`):
  - No se mencionan dependencias específicas en el fragmento proporcionado.
- Archivos del proyecto que este archivo importa:
  - `base.py`
  - `wms_utils.py`

El flujo de datos es desde los archivos de entrada (Excel, TXT) hasta la base de datos SQLite, pasando por la limpieza y transformación de los datos en el adaptador.

