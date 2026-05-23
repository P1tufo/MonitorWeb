## Archivo: ./services/etl/base.py

### Resumen Funcional
El archivo `base.py` define una clase abstracta `BaseWMSProcessor` que proporciona funcionalidades para procesar archivos WMS (TXT/CSV/XLSX) y cargarlos en una base de datos SQLite. Incluye métodos para validar archivos, leer y limpiar datos, realizar operaciones UPSERT atómicas, y procesar directorios de archivos.

### Catálogo de Funciones y Clases
- `BaseWMSProcessor(encodings=None, chunk_size=50000)` - Constructor que inicializa los parámetros de codificación y tamaño de chunk.
  - Propósito: Configura las opciones iniciales para el procesamiento del archivo.

- `validate_file(file_path)` - Método abstracto que verifica si el archivo es válido para este procesador.
  - Propósito: Implementado por cada hijo para validar archivos específicos.

- `_clean_dataframe(df)` - Método abstracto que limpia y transforma un chunk de datos crudos.
  - Propósito: Implementado por cada hijo para realizar la limpieza específica del archivo.

- `_detect_file_params(file_path, required_columns)` - Detecta la fila de encabezado y codificación buscando columnas clave.
  - Propósito: Identifica los parámetros necesarios para leer el archivo correctamente.

- `read_and_clean_data(file_path)` - Lee el archivo completo (para testing o archivos pequeños).
  - Propósito: Carga y limpia un archivo en su totalidad.

- `_get_required_columns()` - Devuelve una lista de columnas requeridas en el encabezado.
  - Propósito: Implementado por cada hijo para especificar las columnas necesarias.

- `_get_primary_keys()` - Devuelve las columnas que actúan como clave primaria para deduplicación.
  - Propósito: Implementado por cada hijo para especificar las claves primarias.

- `process_and_save(file_path, db_path, table_name, conn=None)` - Orquestador unificado de procesamiento Chunked + Upsert SQLite.
  - Propósito: Procesa archivos en chunks y realiza operaciones UPSERT atómicas en la base de datos.

- `_upsert_chunk(conn, df, table_name)` - Lógica de Upsert atómico por chunk.
  - Propósito: Realiza una operación UPSERT atómica para un chunk de datos.

- `process_directory(folder_path, db_path, table_name, conn=None)` - Escanea un directorio y procesa todos los archivos compatibles con Upsert acumulativo.
  - Propósito: Procesa múltiples archivos en un directorio y realiza operaciones UPSERT atómicas.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: No aplica (se espera que las tablas sean proporcionadas como parámetros)
- Columnas: No aplica (se espera que las columnas sean proporcionadas como parámetros)

### Estado y Variables Globales
- `logger` - Variable global para el registro de eventos.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas`
  - `pathlib`
  - `sqlite3`
  - `typing`
  - `logging`

- Flujo: El archivo interactúa con clases y funciones definidas en otros archivos del proyecto, como `core.security.validate_table`.

