# Documentación Técnica - Directorio: db
Compilado el: 2026-06-07 12:50:47
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./db/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

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
- Consultas SQL crudas o llamadas a ORM: Sí, se utilizan funciones que interactúan con la base de datos.

### Estado y Variables Globales
- `logger` - Variable global para el registro de eventos.
- `TABLE_DELIVERIES` - Constante con el nombre de la tabla de entregas.
- `TABLE_STOCK` - Constante con el nombre de la tabla de niveles de stock.

### Dependencias y Flujo
- Librerías externas: `sqlite3`, `datetime`, `re`, `os`, `pathlib`, `typing`.
- Archivos del proyecto que este archivo importa:
  - `services.etl`
  - `db_enrichment` (varias funciones)
- Archivos del proyecto que importan a este archivo:
  - Ninguno
- Flujo de datos: El archivo se utiliza para procesar y consolidar archivos WMS, interactuar con la base de datos SQLite y llamar a funciones de enriquecimiento y actualización.


---

## Archivo: ./db/db_enrichment.py

### Resumen Funcional
El archivo `db_enrichment.py` contiene funciones para enriquecer los datos de la base de datos SQLite del sistema de monitoreo de almacén (WMS) mediante consultas SQL directas y manipulación de DataFrames con Pandas. Las funciones realizan tareas como rellenar columnas vacías, actualizar mapeos de frecuencia, aplicar aprendizaje basado en autores, enriquecer transacciones con datos de stock y movimientos, y sincronizar métricas de SLA.

### Catálogo de Funciones y Clases
- `backfill_deliveries_from_movements(conn: sqlite3.Connection, trans_table: str = "outbound_deliveries", movements_table: str = "inventory_movements")` - Rellena columnas vacías en Entregas (autor, ubicacion, textos) cruzando con Movimientos.
- `learn_author_areas(conn: sqlite3.Connection)` - Actualiza el mapeo de frecuencia Autor -> Área.
- `apply_author_learning(conn: sqlite3.Connection, table_name: str = "outbound_deliveries")` - Asigna áreas de negocio a transacciones 'OTRO' basadas en la memoria del autor.
- `enrich_deliveries_with_stock(conn: sqlite3.Connection, trans_table: str = "outbound_deliveries", stock_table: str = "stock_levels")` - Enriquece transacciones con descripciones y ubicaciones físicas de Stock.
- `backfill_material_texts(conn: sqlite3.Connection)` - Rellena descripciones y UMBs faltantes en Entregas usando Stock y Movimientos como fuentes de verdad.
- `update_sla_with_tasks(conn: sqlite3.Connection)` - Actualiza la métrica de SLA en outbound_deliveries cruzando con la fecha de confirmación real en Tareas.
- `enrich_movements_with_iw39(conn: sqlite3.Connection)` - Enriquece la tabla inventory_movements con ceco_resp y autor provenientes de iw39_orders.

### Interacción con Base de Datos
- **Motor:** SQLite
- **TABLAS**: 
  - `outbound_deliveries`
  - `inventory_movements`
  - `stock_levels`
  - `warehouse_tasks`
  - `iw39_orders`
- **COLUMNAS**:
  - `outbound_deliveries`: entrega, autor, centro_costo, denominacion
  - `inventory_movements`: orden, ceco_resp, autor
  - `stock_levels`: material, texto_breve_de_material, ubicacion_bin, stock_disp, umb
  - `warehouse_tasks`: entrega, fecha_conf
  - `iw39_orders`: orden, ceco_resp, autor

### Estado y Variables Globales
- **Variables Globales**: Ninguna
- **Sesión**: Ninguna
- **Entorno**: Ninguna
- **Diccionarios Quemados**: Ninguno

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`
  - `pandas`
  - `logging`
  - `numpy`
- **Archivos del Proyecto que IMPORTA (consume)**: Ninguno
- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno
- **Dirección del Flujo de Datos**: El flujo de datos pasa por la lectura y escritura directa en la base de datos SQLite, con el procesamiento intermedio realizado mediante Pandas.


---

## Archivo: ./db/predictive_engine.py

### Resumen Funcional
El archivo `predictive_engine.py` procesa los movimientos de inventario para generar modelos predictivos utilizando técnicas como el Análisis del Carrocería (Market Basket Analysis), la Relación Frecuencia-Volumen y el Índice MTBV con Semáforo de Desplanificación. El objetivo es identificar patrones, anomalías y tendencias en los datos de inventario para mejorar la gestión del almacén.

### Catálogo de Funciones y Clases
- `generate_predictions(db_path: str)` - Procesa movimientos de inventario para generar modelos predictivos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `inventory_movements`
- **Columnas:** 
  - `fe_contab` (Fecha)
  - `ce_coste` (Centro de Costo)
  - `material` (Material)
  - `texto_breve_material` (Texto breve del material)
  - `cantidad` (Cantidad)
  - `cmv` (Código Movimiento)

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `logging`
  - `os`
  - `sqlite3`
  - `sys`
  - `collections.Counter`
  - `datetime`
  - `itertools.combinations`
  - `numpy`
  - `pandas`

- **Archivos del Proyecto que Importan a este Archivo:**
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.wms_config.COST_CENTER_MAPPING`

- **Flujo de Datos:**
  - El archivo importa configuraciones y dependencias necesarias.
  - Llama a la función `generate_predictions` con el camino a la base de datos.
  - La función procesa los datos, realiza análisis predictivos y devuelve resultados.

### Notas Adicionales
- La función `generate_predictions` maneja excepciones y registra errores utilizando `logging`.
- El archivo incluye un bloque de prueba al final para ejecutar la función y mostrar el número de combos, puntos de dispersión y alertas generados.


---

