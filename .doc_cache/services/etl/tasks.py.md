## Archivo: ./services/etl/tasks.py

### Resumen Funcional
El archivo `tasks.py` contiene una clase `WarehouseTaskAdapter` que hereda de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos en formato WMS Tareas (Órdenes de Transporte), validando su contenido, obteniendo columnas requeridas y limpiando los datos.

### Catálogo de Funciones y Clases
- **WarehouseTaskAdapter(BaseWMSProcessor)** - Adaptador específico para procesar el formato WMS Tareas (Órdenes de Transporte).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas para el procesamiento.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias utilizadas en el procesamiento.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza los datos del DataFrame.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Dependencias**: `pandas`, `pathlib`
- **Flujo**: El archivo interactúa con el módulo `base.py` a través de la herencia de la clase `BaseWMSProcessor`. No realiza interacciones directas con bases de datos o variables globales.

