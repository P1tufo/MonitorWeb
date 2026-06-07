## Archivo: ./scripts/main_processor.py

### Resumen Funcional
El archivo `main_processor.py` es el punto de entrada del sistema de monitoreo de almacén (WMS). Ejecuta un pipeline completo que incluye la validación de directorios, análisis de carpetas, consolidación de datos, enriquecimiento y procesamiento de diferentes tipos de archivos (Entregas, Stock, Movimientos, IW39, MB5B) para actualizar una base de datos SQLite.

### Catálogo de Funciones y Clases
- `run_pipeline()` - Ejecuta el pipeline completo del WMS Analysis and Consolidation.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas Modificadas:**
  - `stock_levels`
  - `inventory_movements`
  - `iw39_orders`
  - `mb5b_initial_stock`
- **Columnas Modificadas:** Dependiendo del procesamiento, se insertan o actualizan filas en las tablas mencionadas.

### Estado y Variables Globales
- `PROJECT_ROOT` - Ruta al directorio raíz del proyecto.
- `DELIVERIES_DIR`, `STOCK_DIR`, `INVENTORY_DIR`, `IW39_DIR`, `MB5B_DIR`, `CLEANSED_DIR`, `DATABASE_PATH` - Rutas a los directorios y la base de datos.

### Dependencias y Flujo
- **Librerías Externas:** `logging`, `subprocess`, `sys`, `pathlib`
- **Archivos Importados:**
  - `config.py` (para configuraciones globales)
  - `db.consolidator.DataConsolidator` (para consolidación de datos)
  - `db.db_enrichment.enrich_deliveries_with_stock` y `db.db_enrichment.enrich_movements_with_iw39` (para enriquecimiento de datos)
  - `services.etl.movements.InventoryMovementAdapter` (para procesamiento de Movimientos)
  - `services.etl.iw39.IW39Processor` (para procesamiento de IW39)
  - `services.etl.mb5b.MB5BProcessor` (para procesamiento de MB5B)

**Flujo:**
1. `main_processor.py` importa configuraciones y dependencias.
2. Llama a `run_pipeline()`.
3. `run_pipeline()` ejecuta las fases del pipeline, que incluyen análisis de carpetas, consolidación de datos, enriquecimiento y procesamiento de diferentes tipos de archivos.
4. Los resultados se almacenan en la base de datos SQLite especificada.

Este archivo es el punto central para iniciar el proceso de análisis y consolidación en el sistema WMS, gestionando todas las fases del pipeline desde la validación de entrada hasta la actualización de la base de datos.

