# Documentación Técnica - Directorio: db
Compilado el: 2026-05-24 00:59:57
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./db/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

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


---

## Archivo: ./db/db_enrichment.py

### Resumen Funcional
El archivo `db_enrichment.py` contiene funciones que realizan el enriquecimiento de datos en una base de datos SQLite, utilizando SQL directo y pandas para manipular los datos. Las principales operaciones incluyen rellenar columnas vacías en tablas como `outbound_deliveries`, actualizar mapeos de frecuencia Autor -> Área, aplicar aprendizaje basado en autores a transacciones, enriquecer transacciones con datos de stock y rellenar descripciones de materiales faltantes.

### Catálogo de Funciones y Clases
- `backfill_deliveries_from_movements(conn: sqlite3.Connection, trans_table: str = "outbound_deliveries", movements_table: str = "inventory_movements")` - Rellena columnas vacías en Entregas (autor, ubicacion, textos) cruzando con Movimientos.
- `learn_author_areas(conn: sqlite3.Connection)` - Actualiza el mapeo de frecuencia Autor -> Área.
- `apply_author_learning(conn: sqlite3.Connection, table_name: str = "outbound_deliveries")` - Asigna áreas de negocio a transacciones 'OTRO' basadas en la memoria del autor.
- `enrich_deliveries_with_stock(conn: sqlite3.Connection, trans_table: str = "outbound_deliveries", stock_table: str = "stock_levels")` - Enriquece transacciones con descripciones y ubicaciones físicas de Stock.
- `backfill_material_texts(conn: sqlite3.Connection)` - Rellena descripciones y UMBs faltantes en Entregas usando Stock y Movimientos como fuentes de verdad.
- `update_sla_with_tasks(conn: sqlite3.Connection)` - Actualiza la métrica de SLA en outbound_deliveries cruzando con la fecha de confirmación real en Tareas.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQLite. Las tablas y columnas específicas son:
- Tablas: `outbound_deliveries`, `inventory_movements`, `stock_levels`, `warehouse_tasks`.
- Columnas: `material`, `usuario`, `ce_coste`, `texto_breve_material`, `referencia`, `entrega`, `autor`, `centro_costo`, `denominacion`, `ubicacion_bin`, `umb`, `fecha_conf`, `creado_el`, `estado_wms`.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas: `logging`, `pandas`, `sqlite3`, `numpy`.
- Comunicación con otros archivos del proyecto:
  - `core.security.validate_table`
  - `core.db_config_manager.get_holidays`


---

## Archivo: ./db/predictive_engine.py

### Resumen Funcional
El archivo `predictive_engine.py` procesa datos de movimientos en una base de datos SQLite para generar modelos predictivos utilizando técnicas como el Análisis del Carrocería (Market Basket Analysis), la Relación Frecuencia-Volumen y la Estacionalidad Diaria Semana (DOW Bias). El objetivo es identificar patrones, anomalías y tendencias en los datos de inventario para mejorar la planificación y desplanificación.

### Catálogo de Funciones y Clases
- `generate_predictions(db_path: str)` - Procesa Movimientos Transactions para generar modelos predictivos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `inventory_movements`
- **Columnas:** 
  - `fe_contab`, `ce_coste`, `material`, `texto_breve_material`, `cantidad`, `cmv`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas:**
  - `sqlite3`
  - `pandas`
  - `numpy`
  - `datetime`
  - `logging`
  - `itertools`
  - `collections`
  - `sys`
  - `os`

- **Flujo Interno:** El archivo se comunica con el módulo `core.wms_config` para obtener una consulta específica y realiza operaciones de análisis y procesamiento en los datos leídos desde la base de datos SQLite.


---

