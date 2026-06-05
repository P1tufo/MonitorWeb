## Archivo: ./tests/test_enrichment.py

### Resumen Funcional
El archivo `test_enrichment.py` contiene pruebas unitarias para funciones que enriquecen y actualizan datos en una base de datos SQLite utilizada por un sistema de monitoreo de almacén (WMS). Las funciones se encargan de aprender mapeos de autor a áreas, rellenar datos de entrega desde movimientos, enriquecer entregas con información de stock y actualizar el SLA basado en tareas de bodega.

### Catálogo de Funciones y Clases
- `db_with_data(test_db: sqlite3.Connection) -> sqlite3.Connection` - Prepara una base de datos SQLite con datos de prueba para los procesos de enriquecimiento.
- `test_learn_and_apply_author_logic(db_with_data: sqlite3.Connection) -> None` - Verifica que el sistema aprenda que USER_A pertenece a PRODUCCION y lo aplique.
- `test_backfill_from_movements(db_with_data: sqlite3.Connection) -> None` - Verifica que Entregas recupere el autor y centro de costo desde Movimientos.
- `test_enrichment_from_stock(db_with_data: sqlite3.Connection) -> None` - Verifica que se crucen las descripciones de material y ubicaciones desde el maestro de stock.
- `test_update_sla_with_tasks(db_with_data: sqlite3.Connection) -> None` - Verifica que el SLA se actualice correctamente usando las tareas de bodega.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - `outbound_deliveries`: `entrega`, `autor`, `area_negocio`, `centro_costo`, `material`
  - `inventory_movements`: `material`, `usuario`, `ce_coste`, `referencia`
  - `stock_levels`: `material`, `denominacion`, `ubicacion_bin`, `stock_disp`, `umb`
  - `autor_area_mapping`: `autor`, `area_negocio`
  - `warehouse_tasks`: `entrega`, `fecha_conf`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `pytest`, `sqlite3`
- **Archivos del Proyecto que Importan a este Archivo:**
  - `conftest.py` (para el fixture `test_db`)
- **Archivos del Proyecto que Este Archivo Importa:**
  - `db.db_enrichment` (contiene las funciones `learn_author_areas`, `apply_author_learning`, `backfill_deliveries_from_movements`, `enrich_deliveries_with_stock`, `update_sla_with_tasks`)
- **Dirección del Flujo de Datos:** El archivo importa funciones desde `db.db_enrichment` y utiliza un fixture para preparar una base de datos SQLite con datos de prueba. Luego, ejecuta pruebas unitarias que invocan estas funciones y verifican su comportamiento utilizando consultas SQL directas a la base de datos.

