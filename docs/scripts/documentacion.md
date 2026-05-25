# Documentación Técnica - Directorio: scripts
Compilado el: 2026-05-24 23:35:28
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./scripts/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./scripts/main_processor.py

### Resumen Funcional
El archivo `main_processor.py` es el punto de entrada para un proceso automatizado que realiza análisis y consolidación de datos en un sistema de gestión de almacenes (WMS). El script ejecuta una serie de fases, incluyendo la validación de directorios, la ejecución de scripts secundarios, la actualización de una base de datos y el procesamiento de movimientos.

### Catálogo de Funciones y Clases
- `run_pipeline()` - Ejecuta el proceso completo de análisis y consolidación de WMS.
  - **Propósito**: Orquesta todas las fases del proceso, desde la validación de directorios hasta el procesamiento final.

### Interacción con Base de Datos
- **Motor**: SQLite (deducido a partir del nombre del archivo de base de datos `.db`).
- **Tablas y Columnas**:
  - Tabla: `stock_levels`
    - Columnas: No especificadas explícitamente en el código, pero se refiere a la tabla donde se actualizan los niveles de stock.
- **Consultas SQL Crudas o Llamadas a ORM**: 
  - Se utiliza un objeto `DataConsolidator` para interactuar con la base de datos y actualizar la tabla `stock_levels`.
  - Se llama a una función `enrich_deliveries_with_stock` que probablemente realiza consultas SQL internamente.

### Estado y Variables Globales
- **Variables Globales**:
  - `PROJECT_ROOT`: Ruta al directorio raíz del proyecto.
  - `DELIVERIES_DIR`, `STOCK_DIR`, `INVENTORY_DIR`, `CLEANSED_DIR`, `DATABASE_PATH`, `ONEDRIVE_PATH`: Rutas a diferentes directorios y archivos, incluyendo la base de datos.

### Dependencias y Flujo
- **Librerías Externas**:
  - `subprocess` para ejecutar comandos externos.
  - `pathlib` para manejar rutas de archivos.
  - `logging` para registro de eventos.
- **Flujo Interno**:
  - El script importa configuraciones globales desde un archivo `config.py`.
  - Configura el registro de eventos con nivel de logging a INFO.
  - Ejecuta una serie de fases, cada una realizando tareas específicas como la validación de directorios, ejecución de scripts secundarios y actualización de la base de datos.


---

