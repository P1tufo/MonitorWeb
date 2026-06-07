# Documentación Técnica - Directorio: services/etl
Compilado el: 2026-06-07 12:50:47
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
- **Dependencias Externas**: No hay dependencias externas.
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
- `logger` - Variable global para el registro de eventos.

### Dependencias y Flujo
- Librerías externas:
  - `logging`
  - `sqlite3`
  - `abc`
  - `pathlib`
  - `typing`
  - `pandas`
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
No se detectaron variables globales, de sesión o de entorno en este archivo.

### Dependencias y Flujo
- Librerías externas:
  - `sqlite3`
  - `pandas`
  - `pathlib`
  - `typing`
- Archivos del proyecto que importan a este archivo (`deliveries.py`):
  - No se detectaron archivos que importen directamente a `deliveries.py`.
- Archivos del proyecto que este archivo importa:
  - `core.wms_utils`: Contiene funciones utilitarias para el procesamiento de datos.
  - `.base.BaseWMSProcessor`: Clase base para procesadores de WMS.

**Flujo de Datos:**
1. **Entrada**: Archivo CSV, Excel o TXT con datos de entregas de salida.
2. **Procesamiento**:
   - Validación del archivo.
   - Extracción y limpieza de columnas requeridas.
   - Transformación de los datos utilizando funciones utilitarias (`map_wms_status`, `apply_cost_center_mapping`, etc.).
3. **Salida**: Inserción o actualización de los datos en la tabla `outbound_deliveries` de la base de datos SQLite.

Este flujo asegura que los datos de entregas de salida sean procesados y almacenados correctamente en el sistema de gestión de almacén.


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
- **Dependencias**: pandas.
- **Flujo**: El archivo no importa ni es importado por otros archivos dentro del proyecto.


---

## Archivo: ./services/etl/mb5b.py

### Resumen Funcional
El archivo `mb5b.py` contiene una clase `MB5BProcessor` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos en formato MB5B, que representan el stock inicial en un sistema de monitoreo de almacén (WMS). El proceso incluye la validación del archivo, la detección de columnas requeridas y la limpieza y transformación del DataFrame.

### Catálogo de Funciones y Clases
- `MB5BProcessor(BaseWMSProcessor)` - Adaptador específico para procesar el formato MB5B (Stock Inicial).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas para el formato MB5B.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias para el formato MB5B.
  - `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame` - Limpia y transforma el DataFrame del archivo.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**: `pandas`
- **Archivos Importados por Este Archivo**: Ninguno.
- **Archivos que Importan a Este Archivo**: Ninguno.
- **Flujo de Datos**: El archivo importa `BaseWMSProcessor` desde el módulo local y utiliza `pandas` para procesar los datos.


---

## Archivo: ./services/etl/movements.py

### Resumen Funcional
El archivo `movements.py` contiene una clase `InventoryMovementAdapter` que se encarga de procesar archivos CSV con movimientos del sistema WMS, validar su contenido, limpiar y transformar los datos para su almacenamiento en la base de datos SQLite.

### Catálogo de Funciones y Clases
- **Clase:** `InventoryMovementAdapter`
  - Propósito: Adaptador específico para procesar el formato WMS Movimientos.
  
- **Métodos:**
  - `validate_file(file_path: Path) -> bool`: Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]`: Devuelve una lista de columnas requeridas para el procesamiento.
  - `_get_primary_keys() -> List[str]`: Devuelve una lista de claves primarias utilizadas en la base de datos.
  - `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame`: Limpia y transforma el DataFrame, eliminando columnas innecesarias y normalizando los valores.
  - `_vectorized_classify(df: pd.DataFrame) -> pd.DataFrame`: Clasifica las operaciones según el valor de la columna `cmv`.
  - `_post_process(conn, table_name: str)`: Crea índices en la base de datos para mejorar el rendimiento de las consultas.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: `inventory_movements`
    - Columnas: `fe_contab`, `alm`, `ce`, `cmv`, `referencia`, `texto_cab_documento`, `texto_breve_material`, `material`, `cantidad`, `umb`, `doc_mat`, `ej_mat`, `registrado`, `hora`, `usuario`, `pedido`, `ce_coste`, `importe_ml`, `mon`, `proveedor`, `orden`, `pos`, `pos_extra`, `tipo_operacion`

### Estado y Variables Globales
- **Ninguna**

### Dependencias y Flujo
- **Librerías Externas:**
  - `numpy`
  - `pandas`
  
- **Archivos del Proyecto que Importan a este Archivo (lo consumen):**
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa (consume):**
  - `./services/etl/base.py`

- **Dirección del Flujo de Datos:**
  - El archivo recibe un archivo CSV, lo valida, limpia y transforma, luego lo almacena en la base de datos SQLite.


---

## Archivo: ./services/etl/stock.py

### Resumen Funcional
El archivo `stock.py` contiene una clase `StockLevelAdapter` que procesa archivos de inventario/stock en formato LX02, los limpia y carga en una base de datos SQLite. Realiza un REPLACE completo en la tabla especificada.

### Catálogo de Funciones y Clases
- `validate_file(file_path: Path) -> bool`: Valida si el archivo existe y contiene las columnas requeridas.
- `_get_required_columns() -> List[str]`: Devuelve las columnas clave del header SAP LX02.
- `read_and_clean_data(file_path: Path) -> pd.DataFrame`: Lee y limpia los datos del archivo de inventario.
- `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame`: Limpia el DataFrame eliminando filas y columnas vacías y normalizando los strings.
- `process_directory(folder_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int`: Procesa todos los archivos en un directorio, combina sus datos y carga el resultado en la base de datos.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna (se espera una tabla especificada por `table_name`).
- Columnas: Ninguna (se espera que la tabla tenga las columnas necesarias).

### Estado y Variables Globales
- No hay variables globales, de sesión o de entorno definidas en este archivo.

### Dependencias y Flujo
- Librerías externas:
  - `logging`
  - `os`
  - `sqlite3`
  - `datetime`
  - `pathlib`
  - `typing`
  - `pandas`
- Archivos del proyecto que importan a este archivo: Ninguno.
- Archivos del proyecto que este archivo importa: `./services/etl/base.py` (clase base `BaseWMSProcessor`).
- Flujo de datos:
  - El archivo lee archivos de inventario, los limpia y carga en una tabla de la base de datos SQLite.


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
- **Dependencias Externas**: `pandas`
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno.
- **Archivos del Proyecto que Este Archivo Importa**: `./services/etl/base.py` (clase `BaseWMSProcessor`)
- **Flujo de Datos**: El archivo importa la clase base y utiliza pandas para procesar archivos CSV, lo cual implica un flujo de datos desde el archivo hasta la limpieza y preparación del DataFrame.


---

