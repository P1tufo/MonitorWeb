## Archivo: ./tests/test_enrichment.py

### Resumen Funcional
El archivo `test_enrichment.py` contiene pruebas unitarias para funciones que enriquecen datos en una base de datos SQLite utilizada por un sistema de monitoreo de almacén (WMS). Las funciones se encargan de aprender mapeos de autor a áreas, rellenar información de entregas desde movimientos, enriquecer entregas con detalles de stock y actualizar el SLA basado en tareas de bodega.

### Catálogo de Funciones y Clases
- `db_with_data(test_db: sqlite3.Connection) -> sqlite3.Connection` - Prepara una base de datos SQLite con datos de prueba para los procesos de enriquecimiento.
- `test_learn_and_apply_author_logic(db_with_data: sqlite3.Connection) -> None` - Verifica que el sistema aprenda que USER_A pertenece a PRODUCCION y lo aplique.
- `test_backfill_from_movements(db_with_data: sqlite3.Connection) -> None` - Verifica que Entregas recupere el autor y centro de costo desde Movimientos.
- `test_enrichment_from_stock(db_with_data: sqlite3.Connection) -> None` - Verifica que se crucen las descripciones de material y ubicaciones desde el maestro de stock.
- `test_update_sla_with_tasks(db_with_data: sqlite3.Connection) -> None` - Verifica que el SLA se actualice correctamente usando las tareas de bodega.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas Modificadas/Leídas:**
  - `outbound_deliveries`: Campos modificados (`area_negocio`, `autor`, `centro_costo`, `material`, `dias_retraso`).
  - `inventory_movements`: Campos leídos (`usuario`, `ce_coste`, `referencia`).
  - `stock_levels`: Campos leídos (`material`, `denominacion`, `ubicacion_bin`, `stock_disp`, `umb`).

### Estado y Variables Globales
- Ninguna.

### Dependencias y Flujo
- **Librerías Externas:** `pytest`, `sqlite3`.
- **Archivos del Proyecto Importados:**
  - `db.db_enrichment`: Contiene las funciones que se prueban (`apply_author_learning`, `backfill_deliveries_from_movements`, `enrich_deliveries_with_stock`, `learn_author_areas`, `update_sla_with_tasks`).
- **Archivos del Proyecto Importados por:** Ninguno.
- **Dirección del Flujo de Datos:**
  - El archivo importa funciones desde `db.db_enrichment`.
  - Las pruebas crean y manipulan datos en una base de datos SQLite para verificar el comportamiento de las funciones.

