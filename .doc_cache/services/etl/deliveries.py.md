## Archivo: ./services/etl/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene una clase `OutboundDeliveryAdapter` que extiende `BaseWMSProcessor`. Esta clase se encarga de procesar archivos de entregas de salida (Deliveries) utilizando pandas y SQLite. El proceso incluye la validación del archivo, la limpieza y transformación de los datos, así como la inserción o actualización en una base de datos.

### Catálogo de Funciones y Clases
- `OutboundDeliveryAdapter(BaseWMSProcessor)` - Adaptador para procesar Entregas de Salida (Deliveries).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y tiene una extensión permitida.
  - `_get_required_columns() -> List[str]` - Devuelve las columnas requeridas en el DataFrame.
  - `_get_primary_keys() -> List[str]` - Devuelve las claves primarias utilizadas para la deduplicación.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y transforma el DataFrame.
  - `_sanitizar_nombres_columnas(columns: pd.Index) -> list` - Sanitiza los nombres de las columnas.
  - `_post_process(conn, table_name: str)` - Crea índices en la tabla `outbound_deliveries`.
  - `_upsert_chunk(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str)` - Inserta o actualiza datos en la base de datos.

### Interacción con Base de Datos
- Motor: SQLite.
- Tablas: `outbound_deliveries`.
- Columnas:
  - `entrega`
  - `pos_`
  - `centro_costo`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas` (para el procesamiento de datos)
  - `sqlite3` (para la interacción con SQLite)
  - `pathlib` (para manejar rutas de archivos)
  - `typing` (para definir tipos de variables)

- Flujo hacia otros archivos del proyecto:
  - Importa funciones desde `core.wms_utils`, lo que sugiere que interactúa con módulos de utilidades generales.
  - Extiende `BaseWMSProcessor`, lo que indica una arquitectura orientada a objetos donde `OutboundDeliveryAdapter` es un componente específico dentro del sistema.

