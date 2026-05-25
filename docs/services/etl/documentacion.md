# Documentación Técnica - Directorio: services/etl
Compilado el: 2026-05-24 23:35:28
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


---

## Archivo: ./services/etl/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene una clase `OutboundDeliveryAdapter` que extiende `BaseWMSProcessor`. Esta clase se encarga de procesar archivos de entregas de salida (Deliveries) utilizando pandas y SQLite. El objetivo es validar el archivo, limpiar los datos, aplicar mapeos y cálculos necesarios, y finalmente insertar o actualizar los datos en una base de datos SQLite.

### Catálogo de Funciones y Clases
- `OutboundDeliveryAdapter(BaseWMSProcessor)` - Adaptador para procesar Entregas de Salida (Deliveries).
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo existe y tiene una extensión permitida.
  - `_get_required_columns() -> List[str]` - Devuelve las columnas requeridas en el DataFrame.
  - `_get_primary_keys() -> List[str]` - Devuelve las claves primarias utilizadas para la deduplicación.
  - `_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza el DataFrame.
  - `_sanitizar_nombres_columnas(columns: pd.Index) -> list` - Sanitiza los nombres de las columnas eliminando caracteres no válidos y evitando duplicados.
  - `_upsert_chunk(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str)` - Inserta o actualiza datos en una tabla SQLite.

### Interacción con Base de Datos
- Motor de base de datos: SQLite.
- Tablas modificadas: No se especifican explícitamente las tablas, pero el método `_upsert_chunk` indica que interactúa con una tabla SQLite.
- Columnas modificadas: Dependiendo del contenido del DataFrame `df`, se pueden agregar nuevas columnas a la tabla.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas` - Para el procesamiento de datos.
  - `pathlib` - Para manejar rutas de archivos.
  - `typing` - Para definir tipos de variables.
  - `sqlite3` - Para interactuar con la base de datos SQLite.
- Flujo interno:
  - El archivo se comunica con el módulo `base.py` a través de la herencia de la clase `BaseWMSProcessor`.
  - Utiliza funciones auxiliares definidas en `core.wms_utils`, como `sanitize_string`, `map_wms_status`, etc.
  - Interactúa con archivos de entrada (Excel, TXT) y una base de datos SQLite.


---

## Archivo: ./services/etl/movements.py

### Resumen Funcional
El archivo `movements.py` contiene una clase `InventoryMovementAdapter` que extiende de `BaseWMSProcessor`. Esta clase se encarga de procesar archivos CSV relacionados con movimientos en un sistema WMS (Warehouse Management System), validando su contenido, limpiándolo y clasificándolo según ciertas reglas.

### Catálogo de Funciones y Clases
- **InventoryMovementAdapter(BaseWMSProcessor)** - Adaptador específico para procesar el formato WMS Movimientos.
  - `validate_file(file_path: Path) -> bool` - Valida si el archivo CSV existe y cumple con los requisitos mínimos.
  - `_get_required_columns() -> List[str]` - Devuelve una lista de columnas requeridas en el archivo CSV.
  - `_get_primary_keys() -> List[str]` - Devuelve una lista de claves primarias utilizadas para identificar registros.
  - `_clean_dataframe(chunk: pd.DataFrame) -> pd.DataFrame` - Limpia y normaliza los datos del DataFrame, aplicando diversas transformaciones como la eliminación de columnas vacías, renombramiento de columnas, validación de valores y clasificación de operaciones según el tipo de movimiento.
  - `_vectorized_classify(df: pd.DataFrame) -> pd.DataFrame` - Clasifica las filas del DataFrame en función de los valores de ciertas columnas.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales, de sesión o de entorno en este archivo.

### Dependencias y Flujo
- **Librerías externas utilizadas**: `pandas`, `numpy`, `pathlib`.
- **Flujo interno**: El archivo interactúa con el objeto `BaseWMSProcessor` para procesar archivos CSV, utilizando métodos de limpieza y clasificación definidos en la clase `InventoryMovementAdapter`.


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

