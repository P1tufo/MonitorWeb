## Archivo: ./db/db_enrichment.py

### Resumen Funcional
El archivo `db_enrichment.py` contiene funciones para enriquecer datos de entrega y movimiento mediante consultas SQL directas a una base de datos SQLite. Las funciones realizan tareas como rellenar columnas vacías, aprender mapeos de autor a área, aplicar aprendizaje al mapeo de áreas, enriquecer transacciones con datos de stock, rellenar descripciones y UMBs faltantes, actualizar métrica SLA y enriquecer movimientos con información de órdenes PM.

### Catálogo de Funciones y Clases
- `backfill_deliveries_from_movements(conn: sqlite3.Connection, trans_table: str = "outbound_deliveries", movements_table: str = "inventory_movements")` - Rellena columnas vacías en Entregas cruzando con Movimientos.
- `learn_author_areas(conn: sqlite3.Connection)` - Actualiza el mapeo de frecuencia Autor -> Área.
- `apply_author_learning(conn: sqlite3.Connection, table_name: str = "outbound_deliveries")` - Asigna áreas de negocio a transacciones 'OTRO' basadas en la memoria del autor.
- `enrich_deliveries_with_stock(conn: sqlite3.Connection, trans_table: str = "outbound_deliveries", stock_table: str = "stock_levels")` - Enriquece transacciones con descripciones y ubicaciones físicas de Stock.
- `backfill_material_texts(conn: sqlite3.Connection)` - Rellena descripciones y UMBs faltantes en Entregas usando Stock y Movimientos como fuentes de verdad.
- `update_sla_with_tasks(conn: sqlite3.Connection)` - Actualiza la métrica de SLA en outbound_deliveries cruzando con la fecha de confirmación real en Tareas.
- `enrich_movements_with_iw39(conn: sqlite3.Connection)` - Enriquece la tabla inventory_movements con ceco_resp y autor provenientes de iw39_orders.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `outbound_deliveries`
  - `inventory_movements`
  - `stock_levels`
  - `warehouse_tasks`
  - `iw39_orders`
- Columnas:
  - `material`, `usuario`, `ce_coste`, `texto_breve_material`, `referencia` (de `inventory_movements`)
  - `entrega`, `autor`, `centro_costo`, `denominacion` (de `outbound_deliveries`)
  - `ubicacion_bin`, `umb`, `stock_disp` (de `stock_levels`)
  - `orden`, `ceco_resp` (de `inventory_movements` y `iw39_orders`)
  - `fecha_conf` (de `warehouse_tasks`)

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `logging`
  - `pandas`
  - `sqlite3`
  - `typing`
  - `numpy`
- Comunicación con otros archivos del proyecto:
  - `core.security.validate_table`
  - `core.db_config_manager.get_holidays`

