## Archivo: ./services/etl/mb5b.py

### Resumen Funcional
El archivo `mb5b.py` contiene una clase `MB5BProcessor` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos en formato MB5B, que representan el stock inicial en un sistema de monitoreo de almacén (WMS). El proceso incluye la validación del archivo, la detección de columnas requeridas y la limpieza y transformación del DataFrame.

### Catálogo de Funciones y Clases
- `MB5BProcessor(BaseWMSProcessor)` - Adaptador específico para procesar el formato MB5B (Stock Inicial).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas para el formato MB5B.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias para el formato MB5B.
  - `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame` - Limpia y transforma el DataFrame del archivo.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**: `pandas`
- **Archivos Importados por Este Archivo**: Ninguno.
- **Archivos que Importan a Este Archivo**: Ninguno.
- **Flujo de Datos**: El archivo importa `BaseWMSProcessor` desde el módulo local y utiliza `pandas` para procesar los datos.

