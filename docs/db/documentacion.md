# Documentación Técnica - Directorio: db
Compilado el: 2026-06-05 14:46:00
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./db/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

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
  - `logging`
  - `pandas` (pd)
  - `sqlite3`
  - `numpy`
- **Archivos del Proyecto que IMPORTA**:
  - `core.security.validate_table`
  - `core.db_config_manager.get_holidays`
- **Archivos del Proyecto que IMPORTAN a Este Archivo**:
  - Ninguno
- **Dirección del Flujo de Datos**: El flujo de datos pasa por las funciones, realizando consultas SQL para leer y actualizar la base de datos SQLite.


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
  - `sqlite3`
  - `pandas`
  - `numpy`
  - `datetime`
  - `logging`
  - `itertools`
  - `collections`
  - `sys`
  - `os`

- **Archivos del Proyecto que Importan a este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.wms_config.COST_CENTER_MAPPING`

**Flujo de Datos:**
1. El archivo se ejecuta directamente (`if __name__ == "__main__"`).
2. Se importan las dependencias necesarias.
3. La función `generate_predictions` se invoca con la ruta a la base de datos SQLite.
4. Los movimientos de inventario son leídos desde la tabla `inventory_movements`.
5. El procesamiento y análisis de los datos ocurren dentro de la función.
6. Los resultados (combos, scatter data y alertas) se devuelven como un diccionario.

**Dirección del Flujo:**
- **Entrada:** Ruta a la base de datos SQLite.
- **Procesamiento:** Análisis de movimientos de inventario.
- **Salida:** Resultados en formato JSON.


---

