## Archivo: ./services/etl/movements.py

### Resumen Funcional
El archivo `movements.py` contiene una clase `InventoryMovementAdapter` que se encarga de procesar archivos CSV con movimientos del sistema WMS, validar su contenido, limpiar y transformar los datos para su almacenamiento en la base de datos SQLite.

### Catálogo de Funciones y Clases
- **Clase:** `InventoryMovementAdapter`
  - Propósito: Adaptador específico para procesar el formato WMS Movimientos.
  
- **Métodos:**
  - `validate_file(file_path: Path) -> bool`: Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]`: Devuelve una lista de columnas requeridas para el procesamiento.
  - `_get_primary_keys() -> List[str]`: Devuelve una lista de claves primarias utilizadas en la base de datos.
  - `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame`: Limpia y transforma el DataFrame, eliminando columnas innecesarias y normalizando los valores.
  - `_vectorized_classify(df: pd.DataFrame) -> pd.DataFrame`: Clasifica las operaciones según el valor de la columna `cmv`.
  - `_post_process(conn, table_name: str)`: Crea índices en la base de datos para mejorar el rendimiento de las consultas.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: `inventory_movements`
    - Columnas: `fe_contab`, `alm`, `ce`, `cmv`, `referencia`, `texto_cab_documento`, `texto_breve_material`, `material`, `cantidad`, `umb`, `doc_mat`, `ej_mat`, `registrado`, `hora`, `usuario`, `pedido`, `ce_coste`, `importe_ml`, `mon`, `proveedor`, `orden`, `pos`, `pos_extra`, `tipo_operacion`

### Estado y Variables Globales
- **Ninguna**

### Dependencias y Flujo
- **Librerías Externas:**
  - `numpy`
  - `pandas`
  
- **Archivos del Proyecto que Importan a este Archivo (lo consumen):**
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa (consume):**
  - `./services/etl/base.py`

- **Dirección del Flujo de Datos:**
  - El archivo recibe un archivo CSV, lo valida, limpia y transforma, luego lo almacena en la base de datos SQLite.

