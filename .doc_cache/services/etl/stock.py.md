## Archivo: ./services/etl/stock.py

### Resumen Funcional
El archivo `stock.py` contiene una clase `StockLevelAdapter` que procesa archivos de inventario/stock en formato LX02, los limpia y carga en una base de datos SQLite. Realiza un REPLACE completo en la tabla especificada.

### Catálogo de Funciones y Clases
- `validate_file(file_path: Path) -> bool`: Valida si el archivo existe y contiene las columnas requeridas.
- `_get_required_columns() -> List[str]`: Devuelve las columnas clave del header SAP LX02.
- `read_and_clean_data(file_path: Path) -> pd.DataFrame`: Lee y limpia los datos del archivo de inventario.
- `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame`: Limpia el DataFrame eliminando filas y columnas vacías y normalizando los strings.
- `process_directory(folder_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int`: Procesa todos los archivos en un directorio, combina sus datos y carga el resultado en la base de datos.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna (se espera una tabla especificada por `table_name`).
- Columnas: Ninguna (se espera que la tabla tenga las columnas necesarias).

### Estado y Variables Globales
- No hay variables globales, de sesión o de entorno definidas en este archivo.

### Dependencias y Flujo
- Librerías externas:
  - `logging`
  - `os`
  - `sqlite3`
  - `datetime`
  - `pathlib`
  - `typing`
  - `pandas`
- Archivos del proyecto que importan a este archivo: Ninguno.
- Archivos del proyecto que este archivo importa: `./services/etl/base.py` (clase base `BaseWMSProcessor`).
- Flujo de datos:
  - El archivo lee archivos de inventario, los limpia y carga en una tabla de la base de datos SQLite.

