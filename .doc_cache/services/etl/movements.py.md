## Archivo: ./services/etl/movements.py

### Resumen Funcional
El archivo `movements.py` contiene una clase `InventoryMovementAdapter` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos CSV relacionados con movimientos en un sistema WMS (Warehouse Management System), validando su contenido, limpiándolo y clasificándolo según ciertas reglas.

### Catálogo de Funciones y Clases
- **InventoryMovementAdapter(BaseWMSProcessor)** - Adaptador específico para procesar el formato WMS Movimientos.
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo CSV existe y cumple con los requisitos mínimos.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas en el archivo CSV.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias utilizadas para identificar registros.
  - `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza los datos del DataFrame, aplicando diversas transformaciones como la eliminación de columnas vacías, renombramiento de columnas, validación de valores y clasificación de operaciones según el tipo de movimiento.
  - `_vectorized_classify(df: pd.DataFrame) -> pd.DataFrame` - Clasifica las filas del DataFrame en función de los valores de ciertas columnas.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales, de sesión o de entorno en este archivo.

### Dependencias y Flujo
- **Librerías externas utilizadas**: `pandas`, `numpy`, `pathlib`.
- **Flujo interno**: El archivo interactúa con el objeto `BaseWMSProcessor` para procesar archivos CSV, utilizando métodos de limpieza y clasificación definidos en la clase `InventoryMovementAdapter`.

