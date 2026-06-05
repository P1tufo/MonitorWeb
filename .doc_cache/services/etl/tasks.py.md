## Archivo: ./services/etl/tasks.py

### Resumen Funcional
El archivo `tasks.py` contiene una clase `WarehouseTaskAdapter` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos en formato WMS Tareas (Órdenes de Transporte), validando su contenido, limpiándolo y preparándolo para ser utilizado en el sistema de monitoreo de almacén.

### Catálogo de Funciones y Clases
- `WarehouseTaskAdapter(BaseWMSProcessor)` - Adaptador específico para procesar el formato WMS Tareas (Órdenes de Transporte).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas para el procesamiento.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias utilizadas en el procesamiento.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza el DataFrame, eliminando duplicados y corrigiendo tipos de datos.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**: `pandas`, `pathlib`
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno.
- **Archivos del Proyecto que Este Archivo Importa**: `./services/etl/base.py` (clase `BaseWMSProcessor`)
- **Flujo de Datos**: El archivo importa la clase base y utiliza pandas para procesar archivos CSV, lo cual implica un flujo de datos desde el archivo hasta la limpieza y normalización del DataFrame.

