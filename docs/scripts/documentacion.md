# Documentación Técnica - Directorio: scripts
Compilado el: 2026-06-05 03:03:51
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./scripts/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./scripts/generate_graphify.py

### Resumen Funcional
El archivo `generate_graphify.py` es un script que ejecuta el proceso de generación y procesamiento de un mapa interactivo utilizando la herramienta Graphify. El script limpia cualquier salida anterior, configura las variables de entorno necesarias, ejecuta Graphify para generar el mapa, y luego realiza una serie de reemplazos en el HTML generado para adaptarlo al español e incluir traducciones específicas.

### Catálogo de Funciones y Clases
- `run_graphify()` - Inicia el escaneo con Graphify, limpia la salida anterior, ejecuta Graphify, y procesa el archivo HTML generado.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `ROOT_DIR` - Directorio raíz del proyecto.

### Dependencias y Flujo
- **Dependencias**: 
  - `os`
  - `subprocess`
  - `shutil`

- **Flujo**:
  - El archivo se ejecuta directamente (`if __name__ == "__main__":`).
  - Llama a la función `run_graphify()`.

El flujo de datos es simple: el script ejecuta Graphify, procesa su salida y guarda el resultado en un directorio específico dentro del proyecto.


---

## Archivo: ./scripts/main_processor.py

### Resumen Funcional
El archivo `main_processor.py` es el punto de entrada del sistema de monitoreo de almacén (WMS). Ejecuta un pipeline completo que incluye la validación de directorios, análisis de carpetas, consolidación de datos, enriquecimiento y procesamiento de movimientos y órdenes PM.

### Catálogo de Funciones y Clases
- `run_pipeline()` - Ejecuta el pipeline completo del WMS Analysis and Consolidation.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas Modificadas:**
  - `stock_levels`
  - `inventory_movements`
  - `iw39_orders`
- **Columnas Modificadas:** Dependientes de las tablas mencionadas.
- **Consultas SQL Crudas:** No se detectan consultas SQL crudas directamente en este archivo. Se usan ORM (Object Relational Mapping) para interactuar con la base de datos.

### Estado y Variables Globales
- `PROJECT_ROOT` - Ruta del proyecto.
- `DELIVERIES_DIR`, `STOCK_DIR`, `INVENTORY_DIR`, `IW39_DIR`, `CLEANSED_DIR`, `DATABASE_PATH`, `ONEDRIVE_PATH` - Directorios y rutas de archivos.

### Dependencias y Flujo
- **Librerías Externas:** `subprocess`, `sys`, `pathlib`, `logging`
- **Archivos Importados:**
  - `config.py` (para configuraciones globales)
  - `scripts/analyze_folder.py` (para análisis de carpetas)
  - `db.consolidator.DataConsolidator` (para consolidación de datos)
  - `services.etl.movements.InventoryMovementAdapter` (para procesamiento de movimientos)
  - `services.etl.iw39.IW39Processor` (para procesamiento de órdenes PM)
- **Archivos que Importan a este Archivo:** Ninguno

El flujo de datos es unidireccional, con el archivo principal (`main_processor.py`) invocando funciones y servicios para realizar las tareas necesarias.


---

