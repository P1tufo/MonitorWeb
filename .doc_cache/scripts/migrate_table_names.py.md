## Archivo: ./scripts/migrate_table_names.py

### Resumen Funcional
El archivo `migrate_table_names.py` es un script que renombra las tablas de una base de datos SQLite de producción, reemplazando nombres específicos del sistema WMS por nombres genéricos. El objetivo es hacer la base de datos agnóstica al sistema WMS original.

### Catálogo de Funciones y Clases
- `migrate_tables(db_path: str, dry_run: bool = False)` - Ejecuta la migración de nombres de tablas.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas modificadas:
  - `vl06o_transactions` → `outbound_deliveries`
  - `mb51_transactions` → `inventory_movements`
  - `lx02_stock` → `stock_levels`
  - `lt22_transactions` → `warehouse_tasks`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías utilizadas:
  - `sys`, `os`, `sqlite3`, `logging`, `shutil`, `pathlib`
- Comunicación con otros archivos del proyecto: Utiliza `config.DB_PATH` para obtener la ruta de la base de datos.

