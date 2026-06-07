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

