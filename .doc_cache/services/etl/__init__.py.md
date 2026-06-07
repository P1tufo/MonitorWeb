## Archivo: ./services/etl/__init__.py

### Resumen Funcional
Este archivo contiene funciones para procesar diferentes tipos de archivos y directorios relacionados con el inventario y las tareas del almacén. Utiliza adaptadores específicos para cada tipo de dato (inventario, tareas, entregas) y guarda los datos en una base de datos SQLite.

### Catálogo de Funciones y Clases
- `process_inventory_folder(folder_path: str, db_path: str, table_name: str = "inventory_movements", conn=None) -> int` - Procesa un directorio de archivos de inventario y guarda los datos en la base de datos.
- `process_inventory_file(file_path: str, db_path: str, table_name: str = "inventory_movements", conn=None) -> int` - Procesa un archivo de inventario y guarda los datos en la base de datos.
- `process_tasks_file(file_path: str, db_path: str, table_name: str = "warehouse_tasks", conn=None) -> int` - Procesa un archivo de tareas del almacén y guarda los datos en la base de datos.
- `process_lx02_pendientes(folder_path: str, db_path: str, table_name: str = "lx02_pendientes", conn=None) -> int` - Procesa un directorio de archivos pendientes relacionados con el LX02 y guarda los datos en la base de datos.
- `process_deliveries_file(file_path: str, db_path: str, table_name: str = "outbound_deliveries", conn=None) -> int` - Procesa un archivo de entregas y guarda los datos en la base de datos.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas modificadas:
  - `inventory_movements`
  - `warehouse_tasks`
  - `lx02_pendientes`
  - `outbound_deliveries`

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: No hay dependencias externas.
- **Archivos del Proyecto que Importan a este Archivo**:
  - `./services/etl/deliveries.py`
  - `./services/etl/movements.py`
  - `./services/etl/tasks.py`
  - `./services/etl/stock.py`
- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno

El flujo de datos es desde los archivos de entrada (directorios o archivos) hasta la base de datos SQLite, utilizando adaptadores específicos para cada tipo de dato.

