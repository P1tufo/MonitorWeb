## Archivo: ./services/etl/base.py

### Resumen Funcional
El archivo `base.py` define una clase abstracta `BaseWMSProcessor` que proporciona funcionalidades para procesar archivos WMS (TXT/CSV/XLSX) y cargarlos en una base de datos SQLite. Incluye métodos para validar archivos, leer y limpiar datos, realizar operaciones UPSERT atómicas, y procesar directorios de archivos.

### Catálogo de Funciones y Clases
- `BaseWMSProcessor(encodings=None, chunk_size=50000)` - Clase abstracta para procesar archivos WMS.
  - `validate_file(file_path: Path) -> bool` - Verifica si el archivo es válido para este procesador.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y transforma un chunk de datos crudos (Implementado por cada hijo).
  - `_detect_file_params(file_path: Path, required_columns: List[str]) -> Tuple[int, str]` - Detecta la fila de encabezado y codificación buscando columnas clave.
  - `read_and_clean_data(file_path: Path) -> pd.DataFrame` - Lee el archivo completo (para testing o archivos pequeños).
  - `_get_required_columns() -> List[str]` - Lista de strings que deben estar en el header para detectar el inicio. Por defecto vacía.
  - `_get_primary_keys() -> List[str]` - Devuelve las columnas que actúan como clave primaria para deduplicación. Por defecto vacía.
  - `process_and_save(file_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int` - Orquestador unificado de procesamiento Chunked + Upsert SQLite.
  - `_upsert_chunk(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str)` - Lógica de Upsert atómico.
  - `process_directory(folder_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int` - Escanea un directorio y procesa todos los archivos compatibles con Upsert acumulativo.

### Interacción con Base de Datos
- Motor: SQLite.
- Tablas: No aplica (se espera que las tablas sean proporcionadas como parámetros).
- Columnas: No aplica (se espera que las columnas sean proporcionadas como parámetros).

### Estado y Variables Globales
- `logger` - Variable global para el registro de eventos.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `abc`: Para definir clases abstractas.
  - `pandas`: Para manipulación de datos.
  - `pathlib`: Para manejo de rutas de archivos.
  - `sqlite3`: Para interacción con la base de datos SQLite.
  - `typing`: Para tipos de datos anotados.
  - `logging`: Para registro de eventos.

- Flujo: El archivo interactúa con clases y funciones definidas en otros módulos, como `core.security.validate_table`, para validar tablas antes de procesar archivos.

