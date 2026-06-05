## Archivo: ./db/consolidator.py

### Resumen Funcional
El archivo `consolidator.py` es un orquestador de consolidación de datos para un sistema de monitoreo de almacén (WMS) utilizando FastAPI, SQLAlchemy y SQLite. Gestiona la importación y procesamiento de archivos WMS en una base de datos SQLite, aplicando diversas operaciones como UPSERT, actualización de tablas, enriquecimiento de datos y sincronización.

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
- Columnas (no detalladas por brevedad):
  - Todas las columnas relevantes para cada tabla mencionada.
- Consultas SQL crudas o llamadas a ORM: Sí, se utilizan métodos de ORM y consultas SQL dentro de los métodos.

### Estado y Variables Globales
- `logger` - Variable global que almacena el objeto de registro.
- `TABLE_DELIVERIES` - Constante con el nombre de la tabla `outbound_deliveries`.
- `TABLE_STOCK` - Constante con el nombre de la tabla `stock_levels`.

### Dependencias y Flujo
- Librerías externas: `sqlite3`, `logging`, `re`, `pathlib`, `datetime`, `typing`.
- Archivos del proyecto que este archivo importa:
  - `services.etl.OutboundDeliveryAdapter`
  - `services.etl.StockLevelAdapter`
  - `db_enrichment` (varias funciones)
- Archivos del proyecto que importan a este archivo: Ninguno.
- Flujo de datos: El archivo se ejecuta como un script principal (`main`) que toma una carpeta como argumento y procesa los archivos dentro de ella utilizando la clase `DataConsolidator`.

