## Archivo: ./services/etl/stock.py

### Resumen Funcional
El archivo `stock.py` contiene una clase `StockLevelAdapter` que procesa archivos de inventario/stock en formato LX02, los limpia y carga en una base de datos SQLite. Realiza un REPLACE completo en la tabla especificada.

### Catálogo de Funciones y Clases
- **validate_file(file_path: Path) -> bool** - Valida si el archivo existe y contiene las columnas requeridas.
- **_get_required_columns() -> List[str]** - Devuelve las columnas clave del header SAP LX02.
- **read_and_clean_data(file_path: Path) -> pd.DataFrame** - Lee y limpia los datos del archivo, detectando automáticamente la fila de encabezado.
- **_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame** - Limpia el DataFrame eliminando filas y columnas vacías y normalizando los strings.
- **process_directory(folder_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int** - Combina todos los archivos en un directorio, limpia los datos y realiza un REPLACE completo en la tabla especificada.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (se opera sobre una tabla específica proporcionada como parámetro)
- **Columnas**: `Material`, `UMB`, `otcuanto`, `source_file`, `ingested_at`

### Estado y Variables Globales
- **logger**: Objeto de registro para el módulo.

### Dependencias y Flujo
- **Dependencias Externas**:
  - `pandas`
  - `pathlib`
  - `typing`
  - `sqlite3`
  - `os`
  - `datetime`
  - `logging`

- **Archivos del Proyecto que Importan a este Archivo**: Ninguno
- **Archivos del Proyecto que Este Archivo Importa**:
  - `./services/etl/base.py` (clase base `BaseWMSProcessor`)
  
- **Flujo de Datos**: 
  1. El archivo se procesa y limpia.
  2. Los datos son combinados en un DataFrame.
  3. El DataFrame se carga en la base de datos SQLite utilizando `to_sql` con `if_exists="replace"`.
  4. Se crea un índice en la columna `otcuanto`.

