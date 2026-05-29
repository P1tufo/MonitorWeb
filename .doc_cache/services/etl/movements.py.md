## Archivo: ./services/etl/movements.py

### Resumen Funcional
El archivo `movements.py` contiene una clase `InventoryMovementAdapter` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos CSV con movimientos WMS, validando su contenido, limpiándolo y clasificándolo según ciertas reglas. Además, realiza operaciones post-procesamiento en la base de datos para optimizar el rendimiento de las búsquedas.

### Catálogo de Funciones y Clases
- `InventoryMovementAdapter(BaseWMSProcessor)` - Adaptador específico para procesar el formato WMS Movimientos.
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene los columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas en el archivo.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias utilizadas en la clasificación.
  - `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza el DataFrame, aplicando diversas transformaciones y validaciones.
  - `_vectorized_classify(df: pd.DataFrame) -> pd.DataFrame` - Clasifica las filas del DataFrame según ciertas condiciones.
  - `_post_process(conn, table_name: str)` - Crea índices en la base de datos para mejorar el rendimiento de las búsquedas.

### Interacción con Base de Datos
- Motor: No especificado.
- Tablas: `inventory_movements`.
- Columnas:
  - `cmv`
  - `ce_coste`
  - `material`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas` (pd)
  - `numpy` (np)
  - `pathlib` (Path)
  - `typing` (List)

- No se comunica con otros archivos del proyecto.

