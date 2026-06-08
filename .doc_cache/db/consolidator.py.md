## Archivo: ./db/consolidator.py

### Resumen Funcional
El archivo `consolidator.py` es un orquestador que gestiona la consolidación de datos en una base de datos SQLite para un sistema de monitoreo de almacén (WMS). Realiza tareas como la lectura, procesamiento y almacenamiento de archivos WMS, así como el enriquecimiento de los datos con información adicional.

### Catálogo de Funciones y Clases
- `DataConsolidator(db_path: str)` - Gestiona la consolidación de archivos WMS en SQLite.
  - `__init__(self, db_path: str)` - Inicializa el objeto con la ruta a la base de datos.
  - `__enter__(self)` - Establece la conexión a la base de datos y devuelve el objeto.
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
- Columnas (no detalladas por brevedad):
  - Todas las columnas relevantes para cada tabla mencionada.
- Consultas SQL crudas o llamadas a ORM: Sí, se utilizan funciones como `_enrich_with_stock`, `_backfill_movements`, etc., que probablemente implican consultas SQL.

### Estado y Variables Globales
- `logger` - Variable global de logging.
- `TABLE_DELIVERIES` - Constante con el nombre de la tabla de entregas.
- `TABLE_STOCK` - Constante con el nombre de la tabla de niveles de stock.

### Dependencias y Flujo
- Librerías externas: `logging`, `os`, `re`, `sqlite3`, `datetime`, `pathlib`, `typing`.
- Archivos del proyecto que este archivo importa:
  - `services.etl.OutboundDeliveryAdapter`
  - `services.etl.StockLevelAdapter`
  - `db_enrichment.apply_author_learning`
  - `db_enrichment.learn_author_areas`
  - `db_enrichment.backfill_deliveries_from_movements`
  - `db_enrichment.backfill_material_texts`
  - `db_enrichment.enrich_deliveries_with_stock`
  - `db_enrichment.update_sla_with_tasks`
- Archivos del proyecto que importan a este archivo:
  - Ninguno
- Flujo de datos: El flujo de datos pasa por el objeto `DataConsolidator`, que se encarga de la conexión a la base de datos, el procesamiento de archivos y el enriquecimiento de los datos.

