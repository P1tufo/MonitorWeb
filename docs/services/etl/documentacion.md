# Documentación Técnica - Directorio: services/etl
Compilado el: 2026-06-04 23:43:39
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

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
- **Dependencias Externas**: Ninguna
- **Archivos del Proyecto que Importan a este Archivo**:
  - `./services/etl/deliveries.py`
  - `./services/etl/movements.py`
  - `./services/etl/tasks.py`
  - `./services/etl/stock.py`
- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno

El flujo de datos es desde los archivos de entrada (directorios o archivos) hasta la base de datos SQLite, utilizando adaptadores específicos para cada tipo de dato.


---

## Archivo: ./services/etl/base.py

### Resumen Funcional
El archivo `base.py` define una clase abstracta `BaseWMSProcessor` que proporciona funcionalidades para procesar archivos WMS (TXT/CSV/XLSX) y cargarlos en una base de datos SQLite. Incluye métodos para validar archivos, leer y limpiar datos, realizar operaciones UPSERT atómicas, y procesar directorios de archivos.

### Catálogo de Funciones y Clases
- `BaseWMSProcessor(encodings=None, chunk_size=50000)` - Clase abstracta que define métodos para procesar archivos WMS.
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo es válido para este procesador.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y transforma un chunk de datos crudos (implementado por cada hijo).
  - `_detect_file_params(file_path: Path, required_columns: List[str]) -> Tuple[int, str]` - Detecta la fila de encabezado y codificación buscando columnas clave.
  - `read_and_clean_data(file_path: Path) -> pd.DataFrame` - Lee el archivo completo (para testing o archivos pequeños).
  - `_get_required_columns() -> List[str]` - Lista de strings que deben estar en el header para detectar el inicio. Por defecto vacía.
  - `_get_primary_keys() -> List[str]` - Devuelve las columnas que actúan como clave primaria para deduplicación. Por defecto vacía.
  - `process_and_save(file_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int` - Orquestador unificado de procesamiento Chunked + Upsert SQLite.
  - `_upsert_chunk(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str)` - Lógica de Upsert atómico por chunk.
  - `_post_process(conn: sqlite3.Connection, table_name: str)` - Hook opcional para crear índices o post-procesar tras un upsert.
  - `process_directory(folder_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int` - Escanea un directorio y procesa todos los archivos compatibles con Upsert acumulativo.

### Interacción con Base de Datos
- Motor: SQLite.
- Tablas: Ninguna (operaciones directas en la base de datos).
- Columnas: Ninguna (operaciones directas en la base de datos).

### Estado y Variables Globales
- `logger` - Variable global que almacena el objeto de registro.

### Dependencias y Flujo
- Librerías externas:
  - `pandas`
  - `pathlib`
  - `sqlite3`
  - `typing`
  - `logging`
- Archivos del proyecto que este archivo importa: Ninguno.
- Archivos del proyecto que importan a este archivo: Ninguno.
- Flujo de datos: El archivo procesa archivos WMS y carga los datos en una base de datos SQLite.


---

## Archivo: ./services/etl/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene una clase `OutboundDeliveryAdapter` que extiende `BaseWMSProcessor`. Esta clase se encarga de procesar archivos de entregas de salida (Deliveries) en un sistema de gestión de almacén (WMS). El proceso incluye la validación del archivo, la limpieza y transformación de los datos, así como la inserción o actualización de estos datos en una base de datos SQLite.

### Catálogo de Funciones y Clases
- `OutboundDeliveryAdapter(BaseWMSProcessor)` - Adaptador para procesar Entregas de Salida (Deliveries).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y tiene una extensión permitida.
  - `_get_required_columns() -> List[str]` - Devuelve las columnas requeridas en el DataFrame.
  - `_get_primary_keys() -> List[str]` - Devuelve las claves primarias utilizadas para la deduplicación.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y transforma el DataFrame de entrada.
  - `_sanitizar_nombres_columnas(columns: pd.Index) -> list` - Sanitiza los nombres de las columnas del DataFrame.
  - `_post_process(conn, table_name: str)` - Crea índices adicionales en la tabla especificada.
  - `_upsert_chunk(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str)` - Inserta o actualiza datos en la base de datos SQLite.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas modificadas:
  - `outbound_deliveries`
- Columnas modificadas:
  - Todas las columnas presentes en el DataFrame, incluyendo nuevas columnas dinámicas.
- Consultas SQL crudas:
  - `CREATE INDEX IF NOT EXISTS idx_out_ceco_upper ON outbound_deliveries(UPPER(TRIM(centro_costo)))`
  - `PRAGMA table_info({table_name})`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- Librerías externas:
  - `pandas`
  - `pathlib`
  - `typing`
  - `sqlite3`
- Archivos del proyecto que importan a este archivo (`deliveries.py`):
  - No se mencionan dependencias específicas en el fragmento proporcionado.
- Archivos del proyecto que este archivo importa:
  - `base.py`
  - `wms_utils.py`

El flujo de datos es desde los archivos de entrada (Excel, TXT) hasta la base de datos SQLite, pasando por la limpieza y transformación de los datos en el adaptador.


---

## Archivo: ./services/etl/iw39.py

### Resumen Funcional
El archivo `iw39.py` contiene una clase `IW39Processor` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos en formato IW39, validando su contenido y limpiándolo para su uso en el sistema de monitoreo de almacén (WMS).

### Catálogo de Funciones y Clases
- **IW39Processor(BaseWMSProcessor)** - Adaptador específico para procesar el formato IW39 (Órdenes PM).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas para el procesamiento del IW39.
  - `_get_primary_keys() -> List[str]` - Devuelve la clave primaria utilizada en el procesamiento del IW39.
  - `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza un DataFrame de pandas, eliminando columnas vacías, renombrando columnas según un mapeo específico, filtrando filas sin clave primaria, y normalizando datos como fechas y cadenas.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: pandas, pathlib.
- **Flujo**: El archivo no importa ni es importado por otros archivos dentro del proyecto.


---

## Archivo: ./services/etl/movements.py

### Resumen Funcional
El archivo `movements.py` contiene una clase `InventoryMovementAdapter` que se encarga de procesar archivos CSV con movimientos del sistema WMS, validar su contenido, limpiar y transformar los datos para su almacenamiento en la base de datos SQLite.

### Catálogo de Funciones y Clases
- **Clase:** `InventoryMovementAdapter`
  - Propósito: Adaptador específico para procesar el formato WMS Movimientos.
  
- **Función:** `validate_file(file_path: Path) -> bool`
  - Propósito: Valida si el archivo CSV existe y contiene las columnas requeridas.

- **Función:** `_get_required_columns() -> List[str]`
  - Propósito: Devuelve una lista de columnas requeridas para el procesamiento del archivo.

- **Función:** `_get_primary_keys() -> List[str]`
  - Propósito: Devuelve una lista de claves primarias utilizadas en la base de datos.

- **Función:** `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame`
  - Propósito: Limpia y transforma el DataFrame, eliminando columnas vacías, renombrando columnas, normalizando valores y aplicando validaciones específicas.

- **Función:** `_vectorized_classify(df: pd.DataFrame) -> pd.DataFrame`
  - Propósito: Clasifica las operaciones según los valores en la columna 'cmv' y agrega una nueva columna 'tipo_operacion'.

- **Función:** `_post_process(conn, table_name: str)`
  - Propósito: Crea índices estructurales para mejorar el rendimiento de búsquedas en la tabla `inventory_movements`.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna (el archivo no realiza operaciones directas sobre tablas)
- Columnas: Ninguna (el archivo no realiza operaciones directas sobre columnas)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `pandas`, `numpy`
- **Archivos del Proyecto que Importa:** Ninguno
- **Archivos del Proyecto que Son Importados por Este Archivo:** `base.py` (dentro de la misma carpeta)
- **Dirección del Flujo de Datos:** El archivo recibe un DataFrame, lo limpia y transforma, y luego lo devuelve para su almacenamiento en la base de datos.


---

## Archivo: ./services/etl/stock.py

### Resumen Funcional
El archivo `stock.py` contiene una clase `StockLevelAdapter` que procesa archivos de inventario/stock en formato LX02, los limpia y carga en una base de datos SQLite. Realiza un REPLACE completo en la tabla especificada.

### Catálogo de Funciones y Clases
- **validate_file(file_path: Path) -> bool** - Valida si el archivo existe y contiene las columnas requeridas.
- **_get_required_columns() -> List[str]** - Devuelve las columnas clave del header SAP LX02.
- **read_and_clean_data(file_path: Path) -> pd.DataFrame** - Lee y limpia los datos del archivo, detectando automáticamente la fila de encabezado.
- **_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame** - Limpia el DataFrame eliminando filas y columnas vacías y normalizando los strings.
- **process_directory(folder_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int** - Combina todos los archivos en un directorio, limpia los datos y realiza un REPLACE completo en la tabla especificada.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (se opera sobre una tabla específica proporcionada como parámetro)
- **Columnas**: `Material`, `UMB`, `otcuanto`, `source_file`, `ingested_at`

### Estado y Variables Globales
- **logger**: Objeto de registro para el módulo.

### Dependencias y Flujo
- **Dependencias Externas**:
  - `pandas`
  - `pathlib`
  - `typing`
  - `sqlite3`
  - `os`
  - `datetime`
  - `logging`

- **Archivos del Proyecto que Importan a este Archivo**: Ninguno
- **Archivos del Proyecto que Este Archivo Importa**:
  - `./services/etl/base.py` (clase base `BaseWMSProcessor`)
  
- **Flujo de Datos**: 
  1. El archivo se procesa y limpia.
  2. Los datos son combinados en un DataFrame.
  3. El DataFrame se carga en la base de datos SQLite utilizando `to_sql` con `if_exists="replace"`.
  4. Se crea un índice en la columna `otcuanto`.


---

## Archivo: ./services/etl/tasks.py

### Resumen Funcional
El archivo `tasks.py` contiene una clase `WarehouseTaskAdapter` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos en formato WMS Tareas (Órdenes de Transporte), validando su contenido, limpiándolo y preparándolo para ser utilizado en el sistema de monitoreo de almacén.

### Catálogo de Funciones y Clases
- `WarehouseTaskAdapter(BaseWMSProcessor)` - Adaptador específico para procesar el formato WMS Tareas (Órdenes de Transporte).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas para el procesamiento.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias utilizadas en el procesamiento.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza el DataFrame, eliminando duplicados y corrigiendo tipos de datos.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**: `pandas`, `pathlib`
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno.
- **Archivos del Proyecto que Este Archivo Importa**: `./services/etl/base.py` (clase `BaseWMSProcessor`)
- **Flujo de Datos**: El archivo importa la clase base y utiliza pandas para procesar archivos CSV, lo cual implica un flujo de datos desde el archivo hasta la limpieza y normalización del DataFrame.


---

