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
  - `scripts/analyze_folder.py` (para análisis de carpetas)
  - `db.consolidator.DataConsolidator` (para consolidación de datos)
  - `services.etl.movements.InventoryMovementAdapter` (para procesamiento de Movimientos)
  - `services.etl.iw39.IW39Processor` (para procesamiento de IW39)
  - `services.etl.mb5b.MB5BProcessor` (para procesamiento de MB5B)
- **Archivos Importados por Otros:**
  - No se indica explícitamente quiénes importan a este archivo.

El flujo de datos fluye desde el punto de entrada hasta la ejecución de cada fase del pipeline, donde se realizan operaciones en archivos y actualizaciones en la base de datos.

