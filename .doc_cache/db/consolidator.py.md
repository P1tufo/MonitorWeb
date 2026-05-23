## Archivo: ./db/consolidator.py

### Resumen Funcional
El archivo `consolidator.py` es un orquestador de consolidación de datos que opera sobre una base de datos SQLite. Se encarga de procesar archivos WMS, actualizar tablas con los datos más recientes y realizar diversas operaciones de enriquecimiento y sincronización.

### Catálogo de Funciones y Clases
- `DataConsolidator(db_path: str)` - Gestiona la consolidación de archivos WMS en SQLite.
  - `__init__(self, db_path: str)` - Inicializa el objeto con la ruta a la base de datos.
  - `__enter__(self)` - Establece la conexión a la base de datos.
  - `__exit__(self, exc_type, exc_val, exc_tb)` - Cierra la conexión a la base de datos.
  - `connect(self)` - Establece la conexión y configura optimizaciones de SQLite.
  - `_parse_file_date(self, file_path: Path) -> datetime` - Extrae la fecha del nombre del archivo (dd-mm-yyyy).
  - `consolidate_folder(self, folder_path: str, table_name: str = TABLE_DELIVERIES)` - Consolida archivos cronológicamente mediante lógica UPSERT.
  - `overwrite_with_latest(self, folder_path: str, table_name: str = TABLE_STOCK)` - Reemplaza la tabla con los datos del archivo más reciente.
  - `enrich_deliveries_with_stock(self)` - Enriquece las transacciones con información de stock actual.
  - `backfill_from_movements(self)` - Sincroniza datos faltantes desde la tabla Movimientos.
  - `backfill_texts(self)` - Sincroniza descripciones faltantes desde Stock y Movimientos.
  - `update_sla_with_tasks(self)` - Actualiza el SLA cruzando fechas con Tareas.
  - `close(self)` - Cierra la conexión de forma segura.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `outbound_deliveries`
  - `stock_levels`
- Columnas y Operaciones:
  - Lectura y escritura en las tablas mencionadas.
  - Uso de consultas SQL para procesar y actualizar datos.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías Externas: `sqlite3`, `logging`, `re`, `pathlib`, `datetime`, `typing`
- Comunicación con otros archivos:
  - `services.etl.OutboundDeliveryAdapter` y `services.etl.StockLevelAdapter` para procesar y guardar datos.
  - `db_enrichment` para funciones de enriquecimiento y sincronización.
  - `core.security.validate_table` para validar tablas.
  - `core.wms_utils.is_file_changed` y `core.wms_utils.mark_file_processed` para gestionar archivos procesados.

