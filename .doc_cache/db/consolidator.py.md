## Archivo: ./db/consolidator.py

### Resumen Funcional
El archivo `consolidator.py` es un orquestador de consolidación de datos que opera sobre una base de datos SQLite. Se encarga de procesar archivos WMS, realizar operaciones UPSERT y sincronizar información entre diferentes tablas.

### Catálogo de Funciones y Clases
- **DataConsolidator(db_path: str)** - Gestiona la conexión a la base de datos y el proceso de consolidación.
  - `__init__(self, db_path: str)` - Inicializa el objeto con la ruta de la base de datos.
  - `__enter__(self)` - Establece la conexión a la base de datos.
  - `__exit__(self, exc_type, exc_val, exc_tb)` - Cierra la conexión a la base de datos.
  - `connect(self)` - Establece y configura la conexión a SQLite.
  - `_parse_file_date(self, file_path: Path) -> datetime` - Extrae la fecha del nombre del archivo.
  - `consolidate_folder(self, folder_path: str, table_name: str = TABLE_DELIVERIES)` - Consolida archivos cronológicamente mediante lógica UPSERT.
  - `overwrite_with_latest(self, folder_path: str, table_name: str = TABLE_STOCK)` - Reemplaza la tabla con los datos del archivo más reciente.
  - `enrich_deliveries_with_stock(self)` - Enriquece las transacciones con información de stock actual.
  - `backfill_from_movements(self)` - Sincroniza datos faltantes desde la tabla Movimientos.
  - `backfill_texts(self)` - Sincroniza descripciones faltantes desde Stock y Movimientos.
  - `update_sla_with_tasks(self)` - Actualiza el SLA cruzando fechas con Tareas.
  - `close(self)` - Cierra la conexión de forma segura.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `outbound_deliveries`
  - `stock_levels`
- **Columnas**: No especificadas explícitamente, pero se asume que las tablas tienen columnas necesarias para los procesos descritos.

### Estado y Variables Globales
- **Variables Globales**: No aplica

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`
  - `logging`
  - `re`
  - `pathlib`
  - `datetime`
  - `typing`
  - `services.etl.OutboundDeliveryAdapter`
  - `db_enrichment` (varias funciones)
- **Flujo**: El archivo interactúa con el resto del proyecto a través de llamadas a funciones y clases definidas en otros archivos, como `etl.py`, `db_enrichment.py`, y `wms_utils.py`.

