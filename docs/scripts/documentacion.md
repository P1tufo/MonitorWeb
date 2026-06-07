# Documentación Técnica - Directorio: scripts
Compilado el: 2026-06-07 12:50:47
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./scripts/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./scripts/bundler.py

### Resumen Funcional
El archivo `bundler.py` es un script que concatena múltiples archivos JavaScript en un solo archivo llamado `bundle.js`, lo cual se utiliza para la producción del frontend de un sistema de monitoreo de almacén (WMS).

### Catálogo de Funciones y Clases
- `bundle_js()` - Concatena múltiples archivos JS en un solo bundle.js para producción.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `JS_FILES_ORDER` - Una lista ordenada de nombres de archivos JavaScript que se concatenarán.
- `logger` - Un objeto de registro utilizado para registrar mensajes de información, advertencia y error.

### Dependencias y Flujo
- **Dependencias Externas**: `logging`, `os`, `pathlib`.
- **Archivos del Proyecto Importados por Este Archivo**: Ninguno.
- **Archivos del Proyecto que Importan a Este Archivo**: Ninguno.
- **Flujo de Datos**: El script lee archivos JavaScript desde un directorio específico, los concatena en un solo archivo `bundle.js`, y registra el proceso.


---

## Archivo: ./scripts/generate_graphify.py

### Resumen Funcional
El archivo `generate_graphify.py` es un script que prepara y ejecuta el proceso de generación de un mapa interactivo utilizando la herramienta `graphify`. El script limpia el directorio de salida, ejecuta el CLI de `graphify`, procesa el HTML generado para aplicar traducciones y finalmente mueve el archivo HTML resultante a una ubicación específica dentro del proyecto.

### Catálogo de Funciones y Clases
- `prepare_environment()` - Limpia el directorio anterior y prepara la configuración.
- `execute_graphify()` - Ejecuta el CLI de graphify.
- `process_and_move_html()` - Lee el HTML generado, lo traduce y lo guarda en su destino.
- `run_graphify()` - Inicia el escaneo con Graphify.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `ROOT_DIR` - Directorio raíz del proyecto.
- `OUT_DIR` - Directorio donde se genera el HTML por `graphify`.
- `DEST_DIR` - Directorio de destino para el archivo HTML final.
- `TRANSLATIONS` - Diccionario con traducciones para elementos HTML.

### Dependencias y Flujo
- **Dependencias**: `shutil`, `subprocess`, `pathlib`.
- **Flujo**:
  - `generate_graphify.py` importa `shutil`, `subprocess` y `pathlib`.
  - No hay archivos del proyecto que importen a este archivo.
  - El flujo de datos es desde el script hasta la ejecución del CLI de `graphify`, procesamiento del HTML y finalmente su movimiento al directorio de destino.


---

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


---

## Archivo: ./scripts/run_consolidator.py

### Resumen Funcional
El archivo `run_consolidator.py` es un script que ejecuta la consolidación de datos en una carpeta especificada utilizando el motor de base de datos SQLite. El script recibe como argumento la ruta de la carpeta a procesar y utiliza una instancia de `DataConsolidator` para realizar la consolidación.

### Catálogo de Funciones y Clases
- `main()` - Función principal que verifica si se proporciona un argumento (ruta de la carpeta) y luego ejecuta el método `consolidate_folder` de la clase `DataConsolidator`.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna. El script no realiza consultas directas a la base de datos.

### Estado y Variables Globales
- Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- Librerías externas: `os`, `sys`
- Archivos del proyecto que importa:
  - `config.py` (para obtener la ruta de la base de datos)
  - `db.consolidator.DataConsolidator` (clase para la consolidación de datos)

- Archivos del proyecto que son importados por este archivo: Ninguno.

**Flujo de Datos:** El script recibe una ruta de carpeta como argumento, crea una instancia de `DataConsolidator`, y llama al método `consolidate_folder` con la ruta proporcionada.


---

