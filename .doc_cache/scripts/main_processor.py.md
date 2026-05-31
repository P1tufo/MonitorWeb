## Archivo: ./scripts/main_processor.py

### Resumen Funcional
El archivo `main_processor.py` es el punto de entrada para un proceso automatizado que realiza análisis y consolidación de datos en un sistema de gestión de almacenes (WMS). El script ejecuta una serie de fases, cada una responsable de procesar diferentes tipos de datos (entregas, stock, movimientos, IW39) y actualizar una base de datos SQLite.

### Catálogo de Funciones y Clases
- `run_pipeline()` - Ejecuta el proceso completo de análisis y consolidación de WMS.
  - **Propósito**: Orquesta todas las fases del pipeline, desde la validación de entrada hasta la finalización del procesamiento.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas Modificadas**:
  - `stock_levels`
  - `inventory_movements`
  - `iw39_orders`
- **Columnas Modificadas**: Dependiendo de las operaciones realizadas en cada fase, se pueden modificar varias columnas dentro de estas tablas.

### Estado y Variables Globales
- **Variables Globales**:
  - `PROJECT_ROOT`: Ruta al directorio raíz del proyecto.
  - `DELIVERIES_DIR`, `STOCK_DIR`, `INVENTORY_DIR`, `IW39_DIR`, `CLEANSED_DIR`, `DATABASE_PATH`, `ONEDRIVE_PATH` (si se importan correctamente).
- **Estado Crítico**: No aplica.

### Dependencias y Flujo
- **Librerías Externas**:
  - `subprocess`
  - `sys`
  - `pathlib`
  - `logging`
  - `sqlite3`
- **Flujo Interno**: El script interactúa con varios módulos y clases, incluyendo `analyze_folder.py`, `DataConsolidator` de `db.consolidator`, `InventoryMovementAdapter` y `IW39Processor` de `services.etl.movements` y `services.etl.iw39`, respectivamente.

