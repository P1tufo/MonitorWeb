## Archivo: ./services/etl/movements.py

### Resumen Funcional
El archivo `movements.py` contiene una clase `InventoryMovementAdapter` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos CSV en formato WMS Movimientos, validar su contenido, limpiar y transformar los datos, y cargarlos en una base de datos.

### Catálogo de Funciones y Clases
- **InventoryMovementAdapter(BaseWMSProcessor)** - Adaptador específico para procesar el formato WMS Movimientos.
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas en el archivo.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias utilizadas para la carga en la base de datos.
  - `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame` - Limpia y transforma el DataFrame, renombrando columnas, eliminando valores nulos, normalizando tipos de datos, etc.
  - `_vectorized_classify(df: pd.DataFrame) -> pd.DataFrame` - Clasifica las operaciones según los valores en la columna 'cmv'.
  - `_post_process(conn, table_name: str)` - Crea índices para mejorar el rendimiento de consultas en la tabla `inventory_movements`.

### Interacción con Base de Datos
- **Motor**: No especificado.
- **Tablas**: `inventory_movements`.
- **Columnas**:
  - `fe_contab`
  - `alm`
  - `ce`
  - `cmv`
  - `referencia`
  - `texto_cab_documento`
  - `texto_breve_material`
  - `material`
  - `cantidad`
  - `umb`
  - `doc_mat`
  - `ej_mat`
  - `registrado`
  - `hora`
  - `usuario`
  - `pedido`
  - `ce_coste`
  - `importe_ml`
  - `mon`
  - `proveedor`
  - `orden`

### Estado y Variables Globales
- No aplica.

### Dependencias y Flujo
- **Librerías Externas**: `pandas`, `numpy`.
- **Flujo Interno**: El archivo se comunica con la clase base `BaseWMSProcessor` para procesar archivos CSV, limpia los datos utilizando pandas, y luego carga los datos en una base de datos mediante consultas SQL.

