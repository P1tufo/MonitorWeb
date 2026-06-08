# Documentación Técnica - Directorio: scripts
Compilado el: 2026-06-07 18:34:58
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
El archivo `generate_graphify.py` es un script que prepara y ejecuta el proceso de generación de un mapa interactivo utilizando la herramienta `graphify`. El script limpia cualquier salida previa, ejecuta el CLI de `graphify`, traduce el HTML generado y lo mueve al directorio estático para su visualización en la aplicación web.

### Catálogo de Funciones y Clases
- `prepare_environment()` - Limpia el directorio anterior y prepara la configuración.
- `execute_graphify()` - Ejecuta el CLI de graphify.
- `process_and_move_html()` - Lee el HTML generado, lo traduce y lo guarda en su destino.
- `run_graphify()` - Inicia el escaneo con Graphify.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `ROOT_DIR` - Directorio raíz del proyecto.
- `OUT_DIR` - Directorio donde se genera la salida de `graphify`.
- `DEST_DIR` - Directorio donde se mueve el archivo HTML final.
- `TRANSLATIONS` - Diccionario con traducciones para elementos HTML.

### Dependencias y Flujo
- **Dependencias**: `shutil`, `subprocess`, `pathlib`.
- **Flujo de Datos**:
  - `generate_graphify.py` importa `shutil`, `subprocess` y `pathlib`.
  - `graphify-out` es el directorio donde se genera la salida de `graphify`.
  - El archivo HTML generado se mueve a `static/docs`.

El flujo comienza con la ejecución del script, que llama a `run_graphify()`, que en su turno llama a `prepare_environment()`, `execute_graphify()` y finalmente `process_and_move_html()`.


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


---

## Archivo: ./scripts/run_consolidator.py

### Resumen Funcional
El archivo `run_consolidator.py` es un script que ejecuta la consolidación de transacciones del almacén. Recibe como parámetro el camino a una carpeta y utiliza la clase `DataConsolidator` para procesar y consolidar los datos de las transacciones almacenados en una base de datos SQLite.

### Catálogo de Funciones y Clases
- `main()` - Función principal que verifica si se proporciona un argumento (camino a la carpeta) y luego llama al método `consolidate_folder` de la clase `DataConsolidator`.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna. La base de datos se especifica en el parámetro del constructor de `DataConsolidator`.
- Consultas SQL Crudas o ORM: Ninguna.

### Estado y Variables Globales
- Ninguna.

### Dependencias y Flujo
- Librerías Externas:
  - `pathlib`: Para manejar rutas de archivos.
  - `os`: Para manipular el sistema operativo.
- Archivos del Proyecto que Importan a este Archivo: Ninguno.
- Archivos del Proyecto que Este Archivo Importa:
  - `config.DB_PATH`: Ruta de la base de datos.
  - `db.consolidator.DataConsolidator`: Clase para la consolidación de datos.

**Flujo de Datos:**
1. El script se ejecuta desde la línea de comandos con un argumento que es el camino a una carpeta.
2. La función `main()` verifica si se proporciona el argumento necesario.
3. Se crea una instancia de `DataConsolidator` con la ruta a la base de datos SQLite.
4. El método `consolidate_folder` de `DataConsolidator` es llamado para procesar y consolidar los datos en la carpeta especificada.

Este flujo asegura que el script se comporte correctamente cuando se ejecuta desde la línea de comandos con el argumento adecuado.


---

