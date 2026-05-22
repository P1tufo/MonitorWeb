## Archivo: ./services/etl/stock.py

### Resumen Funcional
El archivo `stock.py` contiene una clase `StockLevelAdapter` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos de inventario/stock en formato CSV, TXT, XLS o XLSX, y cargarlos en una base de datos SQLite. Realiza un proceso de limpieza de los datos y sobrescribe el método `process_directory` para combinar múltiples archivos en uno solo y luego realizar un `REPLACE` completo en la tabla especificada.

### Catálogo de Funciones y Clases
- **Clase:** `StockLevelAdapter(BaseWMSProcessor)`
  - Propósito: Adaptador para procesar Inventario/Stock LX02. Realiza REPLACE completo.
  
- **Función:** `validate_file(file_path: Path) -> bool`
  - Propósito: Valida si el archivo existe y cumple con los requisitos.

- **Función:** `_get_required_columns() -> List[str]`
  - Propósito: Devuelve una lista de columnas requeridas. Actualmente está vacía.

- **Función:** `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame`
  - Propósito: Limpia el DataFrame eliminando filas y columnas totalmente vacías y limpia los strings.

- **Función:** `process_directory(folder_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int`
  - Propósito: Combina todos los archivos en el directorio especificado, realiza una limpieza y carga los datos en la base de datos SQLite.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** No aplica (se espera que se proporcione una tabla al llamar a `process_directory`)
- **Columnas:** Se espera que la columna `otcuanto` esté presente en los archivos procesados. Se crea un índice en esta columna.

### Estado y Variables Globales
- **No aplica**

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`: Para el manejo de DataFrames.
  - `pathlib`: Para la manipulación de rutas de archivos.
  - `typing`: Para las anotaciones de tipos.
  - `sqlite3`: Para la interacción con la base de datos SQLite.
  - `os`: Para operaciones del sistema operativo.
  - `datetime`: Para obtener la fecha y hora actual.
  - `logging`: Para el registro de eventos.

- **Flujo Interno:**
  - El archivo se valida y se limpia.
  - Los archivos en el directorio se procesan y combinan en un solo DataFrame.
  - El DataFrame se carga en la base de datos SQLite utilizando `REPLACE`.
  - Se crea un índice en la columna `otcuanto` si no existe.

