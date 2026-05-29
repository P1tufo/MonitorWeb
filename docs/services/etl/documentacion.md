# Documentación Técnica - Directorio: services/etl
Compilado el: 2026-05-29 00:41:03
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./services/etl/__init__.py

### Resumen Funcional
Este archivo contiene funciones para procesar diferentes tipos de archivos relacionados con inventario y entregas. Cada función utiliza un adaptador específico para interactuar con la base de datos y realizar operaciones como procesar directorios o archivos individuales.

### Catálogo de Funciones y Clases
- `OutboundDeliveryAdapter` - Adaptador para manejar operaciones relacionadas con las entregas.
- `InventoryMovementAdapter` - Adaptador para manejar movimientos de inventario.
- `WarehouseTaskAdapter` - Adaptador para manejar tareas del almacén.
- `StockLevelAdapter` - Adaptador para manejar niveles de stock.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: No se mencionan librerías externas específicas.
- **Flujo Interno**: Las funciones interactúan con adaptadores para procesar archivos o directorios, lo que implica una comunicación interna entre el archivo y los adaptadores definidos en otros módulos del proyecto.


---

## Archivo: ./services/etl/base.py

### Resumen Funcional
El archivo `base.py` define una clase abstracta `BaseWMSProcessor` que proporciona funcionalidades para procesar archivos WMS (TXT/CSV/XLSX) y cargarlos en una base de datos SQLite. Incluye métodos para validar archivos, leer y limpiar datos, realizar operaciones UPSERT atómicas, y procesar directorios de archivos.

### Catálogo de Funciones y Clases
- `BaseWMSProcessor(encodings=None, chunk_size=50000)` - Clase abstracta para procesar archivos WMS.
  - `validate_file(file_path: Path) -> bool` - Verifica si el archivo es válido para este procesador.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y transforma un chunk de datos crudos (Implementado por cada hijo).
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
- Tablas: No aplica (se espera que las tablas sean proporcionadas como parámetros).
- Columnas: No aplica (se espera que las columnas sean proporcionadas como parámetros).

### Estado y Variables Globales
- `logger` - Variable global para el registro de eventos.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `abc`: Para definir clases abstractas.
  - `pandas`: Para manipulación de datos.
  - `pathlib`: Para manejo de rutas de archivos.
  - `sqlite3`: Para interacción con la base de datos SQLite.
  - `typing`: Para tipos de datos anotados.
  - `logging`: Para registro de eventos.

- Flujo: El archivo interactúa con clases y funciones definidas en otros módulos (`core.security.validate_table`) y maneja archivos CSV, TXT, XLSX y XLS.


---

## Archivo: ./services/etl/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene una clase `OutboundDeliveryAdapter` que extiende `BaseWMSProcessor`. Esta clase se encarga de procesar archivos de entregas de salida (Deliveries) utilizando pandas y SQLite. El proceso incluye la validación del archivo, la limpieza y transformación de los datos, así como la inserción o actualización en una base de datos.

### Catálogo de Funciones y Clases
- `OutboundDeliveryAdapter(BaseWMSProcessor)` - Adaptador para procesar Entregas de Salida (Deliveries).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y tiene una extensión permitida.
  - `_get_required_columns() -> List[str]` - Devuelve las columnas requeridas en el DataFrame.
  - `_get_primary_keys() -> List[str]` - Devuelve las claves primarias utilizadas para la deduplicación.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y transforma el DataFrame.
  - `_sanitizar_nombres_columnas(columns: pd.Index) -> list` - Sanitiza los nombres de las columnas.
  - `_post_process(conn, table_name: str)` - Crea índices en la tabla `outbound_deliveries`.
  - `_upsert_chunk(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str)` - Inserta o actualiza datos en la base de datos.

### Interacción con Base de Datos
- Motor: SQLite.
- Tablas: `outbound_deliveries`.
- Columnas:
  - `entrega`
  - `pos_`
  - `centro_costo`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas` (para el procesamiento de datos)
  - `sqlite3` (para la interacción con SQLite)
  - `pathlib` (para manejar rutas de archivos)
  - `typing` (para definir tipos de variables)

- Flujo hacia otros archivos del proyecto:
  - Importa funciones desde `core.wms_utils`, lo que sugiere que interactúa con módulos de utilidades generales.
  - Extiende `BaseWMSProcessor`, lo que indica una arquitectura orientada a objetos donde `OutboundDeliveryAdapter` es un componente específico dentro del sistema.


---

## Archivo: ./services/etl/movements.py

### Resumen Funcional
El archivo `movements.py` contiene una clase `InventoryMovementAdapter` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos CSV con movimientos WMS, validando su contenido, limpiándolo y clasificándolo según ciertas reglas. Además, realiza operaciones post-procesamiento en la base de datos para optimizar el rendimiento de las búsquedas.

### Catálogo de Funciones y Clases
- `InventoryMovementAdapter(BaseWMSProcessor)` - Adaptador específico para procesar el formato WMS Movimientos.
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene los columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas en el archivo.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias utilizadas en la clasificación.
  - `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza el DataFrame, aplicando diversas transformaciones y validaciones.
  - `_vectorized_classify(df: pd.DataFrame) -> pd.DataFrame` - Clasifica las filas del DataFrame según ciertas condiciones.
  - `_post_process(conn, table_name: str)` - Crea índices en la base de datos para mejorar el rendimiento de las búsquedas.

### Interacción con Base de Datos
- Motor: No especificado.
- Tablas: `inventory_movements`.
- Columnas:
  - `cmv`
  - `ce_coste`
  - `material`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas` (pd)
  - `numpy` (np)
  - `pathlib` (Path)
  - `typing` (List)

- No se comunica con otros archivos del proyecto.


---

## Archivo: ./services/etl/stock.py

### Resumen Funcional
El archivo `stock.py` contiene una clase `StockLevelAdapter` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos de inventario/stock en formato LX02, validar su contenido, leer y limpiar los datos, y luego guardarlos en una base de datos SQLite.

### Catálogo de Funciones y Clases
- **StockLevelAdapter(BaseWMSProcessor)** - Adaptador para procesar Inventario/Stock LX02. Realiza REPLACE completo.
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve las columnas clave del header SAP LX02.
  - `read_and_clean_data(file_path: Path) -> pd.DataFrame` - Lee el archivo LX02/Stock, detectando la fila header automáticamente y limpia los datos.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia las filas y columnas vacías y limpia los strings de las columnas de tipo objeto.
  - `process_directory(folder_path: str, db_path: str, table_name: str, conn: Optional[sqlite3.Connection] = None) -> int` - Combina todos los archivos en el directorio especificado, realiza la limpieza y guarda los datos en una base de datos SQLite.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: No aplica (No se mencionan tablas específicas).
- **Columnas**: No aplica (No se mencionan columnas específicas).

### Estado y Variables Globales
- **Variables Globales**: No aplica.

### Dependencias y Flujo
- **Librerías Externas**:
  - `pandas` - Para el procesamiento de datos.
  - `pathlib` - Para manejar rutas de archivos.
  - `typing` - Para definir tipos de variables.
  - `sqlite3` - Para interactuar con la base de datos SQLite.
  - `os` - Para operaciones del sistema.
  - `datetime` - Para obtener la fecha y hora actual.
  - `logging` - Para el registro de errores.

- **Flujo**: El archivo se comunica con otros archivos dentro del proyecto a través de importaciones relativas (`from .base import BaseWMSProcessor`).


---

## Archivo: ./services/etl/tasks.py

### Resumen Funcional
El archivo `tasks.py` contiene una clase `WarehouseTaskAdapter` que hereda de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos en formato WMS Tareas (Órdenes de Transporte), validando su contenido, obteniendo columnas requeridas y limpiando los datos.

### Catálogo de Funciones y Clases
- **WarehouseTaskAdapter(BaseWMSProcessor)** - Adaptador específico para procesar el formato WMS Tareas (Órdenes de Transporte).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y contiene las columnas requeridas.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas para el procesamiento.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias utilizadas en el procesamiento.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza los datos del DataFrame.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Dependencias**: `pandas`, `pathlib`
- **Flujo**: El archivo interactúa con el módulo `base.py` a través de la herencia de la clase `BaseWMSProcessor`. No realiza interacciones directas con bases de datos o variables globales.


---

