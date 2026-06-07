## Archivo: ./services/etl/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene una clase `OutboundDeliveryAdapter` que extiende `BaseWMSProcessor`. Esta clase se encarga de procesar archivos de entregas de salida (Deliveries) en un sistema de gestión de almacén (WMS). El proceso incluye la validación del archivo, la limpieza y transformación de los datos, así como la inserción o actualización de estos datos en una base de datos SQLite.

### Catálogo de Funciones y Clases
- `OutboundDeliveryAdapter(BaseWMSProcessor)` - Adaptador para procesar Entregas de Salida (Deliveries).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y tiene una extensión permitida.
  - `_get_required_columns() -> List[str]` - Devuelve las columnas requeridas en el DataFrame.
  - `_get_primary_keys() -> List[str]` - Devuelve las claves primarias utilizadas para la deduplicación.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y transforma el DataFrame de entrada.
  - `_sanitizar_nombres_columnas(columns: pd.Index) -> list` - Sanitiza los nombres de las columnas del DataFrame.
  - `_post_process(conn, table_name: str)` - Crea índices adicionales en la tabla especificada.
  - `_upsert_chunk(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str)` - Inserta o actualiza datos en la base de datos SQLite.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas modificadas:
  - `outbound_deliveries`
- Columnas modificadas:
  - Todas las columnas presentes en el DataFrame, incluyendo nuevas columnas dinámicas.
- Consultas SQL crudas:
  - `CREATE INDEX IF NOT EXISTS idx_out_ceco_upper ON outbound_deliveries(UPPER(TRIM(centro_costo)))`
  - `PRAGMA table_info({table_name})`

### Estado y Variables Globales
No se detectaron variables globales, de sesión o de entorno en este archivo.

### Dependencias y Flujo
- Librerías externas:
  - `sqlite3`
  - `pandas`
  - `pathlib`
  - `typing`
- Archivos del proyecto que importan a este archivo (`deliveries.py`):
  - No se detectaron archivos que importen directamente a `deliveries.py`.
- Archivos del proyecto que este archivo importa:
  - `core.wms_utils`: Contiene funciones utilitarias para el procesamiento de datos.
  - `.base.BaseWMSProcessor`: Clase base para procesadores de WMS.

**Flujo de Datos:**
1. **Entrada**: Archivo CSV, Excel o TXT con datos de entregas de salida.
2. **Procesamiento**:
   - Validación del archivo.
   - Extracción y limpieza de columnas requeridas.
   - Transformación de los datos utilizando funciones utilitarias (`map_wms_status`, `apply_cost_center_mapping`, etc.).
3. **Salida**: Inserción o actualización de los datos en la tabla `outbound_deliveries` de la base de datos SQLite.

Este flujo asegura que los datos de entregas de salida sean procesados y almacenados correctamente en el sistema de gestión de almacén.

