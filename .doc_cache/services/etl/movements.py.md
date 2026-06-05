## Archivo: ./services/etl/movements.py

### Resumen Funcional
El archivo `movements.py` contiene una clase `InventoryMovementAdapter` que se encarga de procesar archivos CSV con movimientos del sistema WMS, validar su contenido, limpiar y transformar los datos para su almacenamiento en la base de datos SQLite.

### Catálogo de Funciones y Clases
- **Clase:** `InventoryMovementAdapter`
  - Propósito: Adaptador específico para procesar el formato WMS Movimientos.
  
- **Función:** `validate_file(file_path: Path) -> bool`
  - Propósito: Valida si el archivo CSV existe y contiene las columnas requeridas.

- **Función:** `_get_required_columns() -> List[str]`
  - Propósito: Devuelve una lista de columnas requeridas para el procesamiento del archivo.

- **Función:** `_get_primary_keys() -> List[str]`
  - Propósito: Devuelve una lista de claves primarias utilizadas en la base de datos.

- **Función:** `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame`
  - Propósito: Limpia y transforma el DataFrame, eliminando columnas vacías, renombrando columnas, normalizando valores y aplicando validaciones específicas.

- **Función:** `_vectorized_classify(df: pd.DataFrame) -> pd.DataFrame`
  - Propósito: Clasifica las operaciones según los valores en la columna 'cmv' y agrega una nueva columna 'tipo_operacion'.

- **Función:** `_post_process(conn, table_name: str)`
  - Propósito: Crea índices estructurales para mejorar el rendimiento de búsquedas en la tabla `inventory_movements`.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna (el archivo no realiza operaciones directas sobre tablas)
- Columnas: Ninguna (el archivo no realiza operaciones directas sobre columnas)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `pandas`, `numpy`
- **Archivos del Proyecto que Importa:** Ninguno
- **Archivos del Proyecto que Son Importados por Este Archivo:** `base.py` (dentro de la misma carpeta)
- **Dirección del Flujo de Datos:** El archivo recibe un DataFrame, lo limpia y transforma, y luego lo devuelve para su almacenamiento en la base de datos.

