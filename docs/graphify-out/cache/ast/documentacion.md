# Documentación Técnica - Directorio: graphify-out/cache/ast
Compilado el: 2026-06-05 03:03:51
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./graphify-out/cache/ast/00452bedb8e75d649f71f64e31759c0daf0372d27f59e7ca1d6b0298623dfa51.json

### Resumen Funcional
El archivo `iw39.py` contiene la implementación del procesador específico para el formato IW39, utilizado en el sistema de monitoreo de almacén (WMS). Este procesador hereda de una clase base y realiza operaciones como validación de archivos, obtención de columnas requeridas y limpieza de datos.

### Catálogo de Funciones y Clases
- **IW39Processor()** - Adaptador específico para procesar el formato IW39 (órdenes PM).
  - `.validate_file(path: Path) -> bool` - Valida si un archivo es válido según las reglas del formato IW39.
  - `._get_required_columns(required_columns: List[str]) -> None` - Obtiene las columnas requeridas para el procesamiento.
  - `._get_primary_keys(primary_keys: List[str]) -> None` - Obtiene las claves primarias necesarias.
  - `._clean_dataframe(dataframe: DataFrame) -> DataFrame` - Limpia y normaliza un DataFrame.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: pandas, pathlib, typing.
- **Archivos Importados por este Archivo**:
  - `users_christianykelly_desktop_monitorweb_services_etl_base_py` (BaseWMSProcessor)
- **Archivos que Importan a este Archivo**: Ninguno

El flujo de datos fluye desde el archivo principal hacia `IW39Processor`, donde se realizan las operaciones de validación, obtención de columnas y limpieza de datos.


---

## Archivo: ./graphify-out/cache/ast/022fcdc989a48317aa114587cfe71d8bc2562272154383999c6d2663a74c6320.json

### Resumen Funcional
El archivo `models.py` contiene definiciones de modelos ORM SQLAlchemy para el esquema de configuración SaaS del sistema de monitoreo de almacén (WMS). Estos modelos incluyen mapeos de códigos internos a etiquetas legibles, asociaciones de centros de costo con áreas de negocio, parámetros de comportamiento del sistema y días no hábiles para el cálculo de SLA.

### Catálogo de Funciones y Clases
- `StatusMapping` - Mapea códigos internos del WMS a etiquetas legibles por humanos.
- `CostCenterMapping` - Asocia un código de centro de costo del WMS con una área de Negocio.
- `AppSetting` - Parámetros de comportamiento del sistema. El campo `type` puede ser float, int, bool o str.
- `Holiday` - Días no hábiles para el cálculo de SLA (días de retraso).
- `ConfigQuery` - Almacena el estado visual (JSON) de las consultas del Analytics Studio.

### Interacción con Base de Datos
El archivo utiliza SQLAlchemy como ORM y SQLite como motor de base de datos. No hay consultas SQL crudas explícitas mencionadas en este fragmento, pero se asume que los modelos interactúan con la base de datos a través de las capas de Repositories y Services.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno quemadas en el código.

### Dependencias y Flujo
- **Dependencias**: 
  - `sqlalchemy`
  - `sqlalchemy_orm`
  - `users_christianykelly_desktop_monitorweb_core_database_py`

- **Flujo de Datos**:
  - El archivo `models.py` importa dependencias necesarias y define clases que representan los modelos ORM.
  - Estas clases son utilizadas por las capas superiores del sistema (Services, Repositories) para interactuar con la base de datos.

Este análisis proporciona una visión detallada de la estructura y funcionalidad del archivo `models.py` en el contexto del proyecto WMS.


---

## Archivo: ./graphify-out/cache/ast/06ebe39d7fb10fcd5acb5d80ec20f5fff5d8a35bf9258e9777a900ac3be93b71.json

### Resumen Funcional
El archivo `test_services.py` contiene pruebas unitarias para el módulo de servicios del sistema de monitoreo de almacén (WMS). Las pruebas cubren la creación y gestión de un estado global (`AppState`), la limpieza del estado después de cada prueba, y las funciones relacionadas con el manejo de túneles.

### Catálogo de Funciones y Clases
- `app_state()` - Devuelve una instancia limpia de `AppState`.
- `cleanup_tunnel()` - Limpia el estado global del túnel tras cada test.
- `test_state_cache_respects_limits(appstate)` - Verifica que el gestor de estado respete los límites de memoria.
- `test_state_sync_flag_reactivity(appstate)` - Valida que la propiedad reactiva de sincronización cambie su estado de forma correcta.
- `test_start_tunnel_manages_singleton_instance()` - Asegura que `start_tunnel` inicialice correctamente el servicio de túnel.
- `test_stop_tunnel_releases_global_reference()` - Valida que `stop_tunnel` limpie las referencias globales de forma segura.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `appstate` - Variable global que almacena el estado del sistema.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `pytest`
  - `unittest.mock`
  - `services_tunnel`
  - `core_state`

- **Flujo de Datos**:
  - El archivo `test_services.py` importa varios módulos y utiliza funciones para probar el comportamiento del sistema.
  - Las pruebas utilizan mocks y patches para simular comportamientos específicos durante las pruebas.
  - La función `app_state()` devuelve una instancia limpia de `AppState`, que es utilizada en algunas de las pruebas.

Este archivo se encuentra en la carpeta `tests/test_services.py` y es parte del proceso de prueba unitaria del sistema WMS.


---

## Archivo: ./graphify-out/cache/ast/0833fe33af9c0adc841e3fc694eddf131177b50ee7375fdfbc4a1dd23bb78d82.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
Clase abstracta unificada para procesar archivos WMS (TXT/CSV/XLSX). Implementa métodos para validar archivos, limpiar y transformar datos, detectar parámetros de archivo, leer y limpiar datos, obtener columnas requeridas y primarias, procesar y guardar datos, realizar upserts en SQLite, y procesar directorios.

### Catálogo de Funciones y Clases
- **BaseWMSProcessor**
  - `__init__(self, file_path: str, chunk_size: int = 1000)`
    - Inicializa el procesador con la ruta del archivo y el tamaño del chunk.
  - `validate_file(self) -> bool`
    - Verifica si el archivo es válido para este procesador.
  - `_clean_dataframe(self, dataframe: DataFrame) -> DataFrame`
    - Limpia y transforma un chunk de datos crudos (Implementado por cada hijo).
  - `_detect_file_params(self, file_path: Path) -> Tuple[str, str]`
    - Detecta la fila de encabezado y codificación buscando columnas clave.
  - `read_and_clean_data(self) -> DataFrame`
    - Lee el archivo completo (para testing o archivos pequeños).
  - `_get_required_columns(self, file_path: Path) -> List[str]`
    - Devuelve las columnas que actúan como clave primaria para deduplicación. Por defecto, devuelve una lista de strings que deben estar en el header.
  - `_get_primary_keys(self, file_path: Path) -> List[str]`
    - Devuelve las columnas que actúan como clave primaria para deduplicación. Por defecto, devuelve una lista de strings que deben estar en el header.
  - `process_and_save(self, connection: Connection, table_name: str) -> int`
    - Orquestador unificado de procesamiento Chunked + Upsert SQLite.
  - `_upsert_chunk(self, connection: Connection, dataframe: DataFrame, table_name: str) -> None`
    - Lógica de Upsert atómico por chunk. Seguridad de los f-strings.
  - `_post_process(self, connection: Connection, table_name: str) -> None`
    - Hook opcional para crear índices o post-procesar tras un upsert.
  - `process_directory(self, directory_path: Path, connection: Connection, table_name: str) -> int`
    - Escanea un directorio y procesa todos los archivos compatibles con Upsert acumulando resultados.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (se asume que las tablas se manejan a través del parámetro `table_name` en los métodos)
- **Columnas**: Ninguna (se asume que las columnas se manejan a través del parámetro `table_name` en los métodos)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - pandas
  - pathlib
  - sqlite3
  - typing
  - logging
  - core_security
- **Archivos del Proyecto que Este Archivo Importa (consume)**: Ninguno
- **Archivos del Proyecto que Importan a Este Archivo (lo consumen)**: Ninguno


---

## Archivo: ./graphify-out/cache/ast/087f2b892ed92921847a72be21201ce5113dbaf0ad580aa283bee861f30bc2c3.json

### Resumen Funcional
El archivo `inventory_service.py` contiene la lógica de negocio para el servicio de inventario en un sistema de monitoreo de almacén (WMS). Define una clase `InventoryService` que proporciona métodos para formatear números, obtener el período más reciente de datos y generar el contexto completo para el dashboard de movimientos.

### Catálogo de Funciones y Clases
- **Clase:** `InventoryService`
  - **Método:** `__init__(self, session: Session)`
    - Propósito: Inicializa la instancia con una sesión de base de datos.
  - **Método:** `fmt_num(self, num: str) -> str`
    - Propósito: Formatea un número como cadena.
  - **Método:** `_get_latest_data_period(self) -> str`
    - Propósito: Obtiene el período más reciente de datos disponibles en la base de datos.
  - **Método:** `_get_empty_context(self, context_type: str) -> Any`
    - Propósito: Genera un contexto vacío basado en el tipo de contexto proporcionado.
  - **Método:** `get_full_context(self) -> Any`
    - Propósito: Genera el contexto completo para el dashboard de movimientos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: No especificada explícitamente en el código.
  - Consultas SQL Crudas:
    ```sql
    SELECT * FROM table_name WHERE condition;
    ```
  - Llamadas a ORM:
    - `session.execute(text(query))`
    - `InventoryRepository.read_sql_query(query)`

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - SQLAlchemy
  - Pandas
  - Logging
  - Datetime
  - Typing
  - Core Utils
  - Core State
  - Repositories
  - Core WMS Config
- **Archivos del Proyecto que Importan a Este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:**
  - `sqlalchemy`
  - `pandas`
  - `logging`
  - `datetime`
  - `typing`
  - `core_utils`
  - `core_state`
  - `repositories`
  - `core_wms_config`

**Flujo de Datos:**
- El archivo importa varias bibliotecas y módulos necesarios para su funcionamiento.
- La clase `InventoryService` utiliza una sesión de base de datos (`Session`) para interactuar con la base de datos.
- Los métodos `_get_latest_data_period`, `_get_empty_context`, y `get_full_context` realizan operaciones en la base de datos y utilizan funciones de Pandas para procesar los datos.
- El método `get_full_context` depende de otros métodos internos y puede generar un contexto vacío o completo basado en el tipo de contexto proporcionado.


---

## Archivo: ./graphify-out/cache/ast/0b32ccedd96ba13bf64984e114e691efa0f4219d31ae946293147ce99318e67b.json

### Resumen Funcional
El archivo `check_queries.py` es un script que realiza consultas a una base de datos SQLite y utiliza pandas para procesar los resultados.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (se supone que las tablas son definidas en otro lugar del proyecto)
- **Columnas**: Ninguna (se supone que las columnas son definidas en otro lugar del proyecto)

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para procesar los resultados de las consultas.
  - `json`: Para manejar operaciones JSON.

- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno

**Flujo de Datos**: El script importa las bibliotecas necesarias y realiza consultas a la base de datos SQLite utilizando `sqlite3`. Los resultados se procesan con pandas y luego pueden ser exportados o utilizados según sea necesario.


---

## Archivo: ./graphify-out/cache/ast/0bd9e085d6851ba9217fa0b8a5a7c2d1f2d4af858e7af3db078f0bce1adc230f.json

### Resumen Funcional
El archivo `movements.py` contiene la implementación del adaptador para procesar el formato WMS Movimientos, incluyendo métodos para validar archivos, obtener columnas requeridas, limpiar dataframes y realizar clasificaciones vectorizadas.

### Catálogo de Funciones y Clases
- **InventoryMovementAdapter** - Adaptador específico para procesar el formato WMS Movimientos.
  - `.validate_file(path: Path) -> bool` - Valida si el archivo es válido.
  - `._get_required_columns() -> List[str]` - Obtiene las columnas requeridas.
  - `._get_primary_keys() -> List[str]` - Obtiene las claves primarias.
  - `._clean_dataframe(df: DataFrame) -> DataFrame` - Limpia el dataframe.
  - `._vectorized_classify(df: DataFrame) -> DataFrame` - Realiza clasificaciones vectorizadas.
  - `._post_process(file_path: str)` - Procesa el archivo post-transformación.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: pandas, numpy, pathlib, typing
- **Archivos Importados por este Archivo**:
  - `services/etl/base.py`
- **Archivos que Importan a este Archivo**:
  - Ninguno

El flujo de datos fluye desde el archivo principal hacia `movements.py`, donde se importan las dependencias necesarias y se definen los métodos para procesar los archivos WMS Movimientos.


---

## Archivo: ./graphify-out/cache/ast/0c499e306de4b6b2705076a26ee0c8fa90b428f341f70bcc5f232501ef3f005e.json

### Resumen Funcional
El archivo `stock.py` contiene la implementación del adaptador para procesar inventario/stock LX02, que realiza un REPLACE completo en los datos.

### Catálogo de Funciones y Clases
- **StockLevelAdapter()** - Adaptador para procesar Inventario/Stock LX02. Realiza REPLACE completo.
  - `.validate_file(path: Path) -> bool` - Valida el archivo proporcionado.
  - `._get_required_columns() -> List[str]` - Obtiene las columnas requeridas del header SAP LX02.
  - `.read_and_clean_data(file_path: Path) -> DataFrame` - Lee y limpia los datos del archivo.
  - `._clean_dataframe(df: DataFrame) -> DataFrame` - Limpia el dataframe.
  - `.process_directory(directory_path: str, connection: Connection) -> int` - Procesa todos los archivos en el directorio y realiza un REPLACE.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** Ninguna (el código no interactúa directamente con tablas de la base de datos).
- **Columnas:** Ninguna (el código no interactúa directamente con columnas de la base de datos).

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - pandas
  - pathlib
  - typing
  - sqlite3
  - os
  - datetime
  - logging
- **Archivos del Proyecto que Importan a Este Archivo (Consumen):** Ninguno
- **Archivos del Proyecto que Este Archivo Importa (Lo Consumen):**
  - `users_christianykelly_desktop_monitorweb_services_etl_base_py`

El flujo de datos comienza en el archivo principal, que importa `stock.py`, y luego se ejecutan las funciones definidas en `StockLevelAdapter` para validar archivos, leer y limpiar datos, y procesar directorios.


---

## Archivo: ./graphify-out/cache/ast/0e0cd0646ae6142f81e322200b6eb5c93f583a3fdc7e54f89bead20b0a6f6462.json

### Resumen Funcional
El archivo `pdf_reports.py` contiene funciones para generar informes PDF en un sistema de monitoreo de almacén (WMS). Estas funciones incluyen la parseación y formateo de cantidades, así como el dibujo de tablas de anexos y listas de picking.

### Catálogo de Funciones y Clases
- `_parse_qty()` - Parsea y sanitiza valores de cantidad.
- `_fmt_qty()` - Formatea cantidades para mostrar en PDF.
- `draw_annex_table()` - Dibuja la tabla de índice (anexo) de entregas agrupadas.
- `draw_picking_list()` - Dibuja la lista de picking desglosada por entrega pero con total consolidado.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
**Librerías Externas:**
- `datetime` (importado en la línea 2)

**Archivos del Proyecto que Importan a este Archivo (`pdf_reports.py`):**
- Ninguno

**Archivos del Proyecto que Este Archivo Importa (`pdf_reports.py`):**
- Ninguno


---

## Archivo: ./graphify-out/cache/ast/0eb15d9f49a60b1bd3090585220d654d1a73bb2cefb1838a3852f20ceccc9f59.json

### Resumen Funcional
El archivo `doc_prompts.py` contiene el código fuente de un módulo que probablemente se encarga de generar o manejar prompts para documentos en un sistema de monitoreo de almacén (WMS).

### Catálogo de Funciones y Clases
Ninguna.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
Ninguna.


---

## Archivo: ./graphify-out/cache/ast/0f8f23ca752eaf05d971ebe559afb3cbbbebe69710e8674943741e44b04a4108.json

### Resumen Funcional
El archivo `tasks.py` contiene dos funciones principales: `get_tasks_context()` y `analytics_tasks_api()`. La primera función recupera el contexto completo, mientras que la segunda proporciona análisis de tareas en formato JSON.

### Catálogo de Funciones y Clases
- **get_tasks_context(session: Session)**
  - Breve propósito: Recupera el contexto completo.
  
- **analytics_tasks_api(session: Session, appstate: AppState)**
  - Breve propósito: Proporciona análisis de tareas en formato JSON.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas:
  - No se especifican consultas SQL crudas o llamadas a ORM explícitas en el fragmento proporcionado.
  
### Estado y Variables Globales
- `session`: Variable global que representa la sesión de base de datos.
- `appstate`: Variable global que almacena el estado del sistema.

### Dependencias y Flujo
- **Librerías Externas**:
  - `logging`
  - `sqlalchemy_orm`
  - `sqlalchemy`
  - `pandas`
  - `datetime`
  - `core_state`
  - `core_utils`
  - `repositories`
  - `services_tasks_service`
  - `fastapi`
  - `core_database`
  - `core_auth`
  - `core_schemas`

- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa**:
  - `logging`
  - `sqlalchemy_orm`
  - `sqlalchemy`
  - `pandas`
  - `datetime`
  - `core_state`
  - `core_utils`
  - `repositories`
  - `services_tasks_service`
  - `fastapi`
  - `core_database`
  - `core_auth`
  - `core_schemas`

- **Flujo de Datos**:
  - El archivo importa varias librerías y módulos necesarios para su funcionamiento.
  - Las funciones `get_tasks_context` y `analytics_tasks_api` utilizan objetos como `session` y `appstate`, que son pasados como parámetros.


---

## Archivo: ./graphify-out/cache/ast/116f0b2d966298852f87da3c56df280088fc72705dc15afb3a5f5d7fddd580bd.json

### Resumen Funcional
El archivo `main_processor.py` contiene la lógica principal para ejecutar el análisis y consolidación completo del sistema de gestión de almacén (WMS). La función `run_pipeline()` es el punto de entrada que coordina todas las etapas del proceso.

### Catálogo de Funciones y Clases
- **run_pipeline()** - Ejecuta el flujo completo del WMS Analysis and Consolidation pipeline.
- **DataConsolidator** - Clase que realiza la consolidación de datos.
- **InventoryMovementAdapter** - Adaptador para procesar movimientos de inventario.
- **IW39Processor** - Procesador específico para el formato IW39.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
Ninguna. No se detectan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Librerías Externas**: `subprocess`, `sys`, `pathlib`, `logging`.
- **Archivos del Proyecto Importados**:
  - `config` (desde `scripts/main_processor.py`)
- **Archivos que Importan a Este Archivo**: Ninguno.

El flujo de datos fluye desde el punto de entrada `run_pipeline()` hacia las funciones y clases mencionadas, realizando tareas como la verificación de archivos, procesamiento de directorios, conexión a adaptadores e invocación de procesadores específicos.


---

## Archivo: ./graphify-out/cache/ast/121af652827c1eefa1f5c39b394c7151cbb3834b1cc6fe57c74a02d813e6c92a.json

### Resumen Funcional
El archivo `__init__.py` en la carpeta `repositories` del proyecto WMS es el punto de entrada para la configuración y obtención de repositorios de datos. Define funciones que devuelven instancias de diferentes tipos de repositorios (`DeliveriesRepository`, `InventoryRepository`, `TasksRepository`) y una función para obtener una conexión a la base de datos.

### Catálogo de Funciones y Clases
- **get_db()** - Obtiene una instancia de la conexión a la base de datos.
- **get_deliveries_repo()** - Devuelve una instancia del repositorio de entregas (`DeliveriesRepository`).
- **get_inventory_repo()** - Devuelve una instancia del repositorio de inventario (`InventoryRepository`).
- **get_tasks_repo()** - Devuelve una instancia del repositorio de tareas (`TasksRepository`).

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas y Columnas**: No se especifican columnas específicas, solo se menciona la conexión a la base de datos.
- **Consultas SQL Crudas o ORM**: No hay consultas SQL crudas o llamadas a ORM explícitas en este archivo.

### Estado y Variables Globales
No se detectan variables globales, de sesión, de entorno o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- **Librerías Externas**: `sqlite3`, `fastapi`
- **Archivos del Proyecto que IMPORTA (consume)**: `base.py`, `deliveries.py`, `inventory.py`, `tasks.py`
- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno
- **Dirección del Flujo de Datos**: El archivo importa librerías y otros módulos para configurar y obtener instancias de repositorios, pero no realiza operaciones directas en la base de datos.


---

## Archivo: ./graphify-out/cache/ast/15c4781e1da13feaaf38c1d858f4c03f14bc621fbf5ad07e15b9c88fd63d2b72.json

### Resumen Funcional
El archivo `check_dates.py` es un script que realiza operaciones relacionadas con fechas, probablemente para el monitoreo de almacén (WMS). No contiene ninguna interacción explícita con una base de datos.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada en este fragmento.

### Interacción con Base de Datos
Ninguna. El archivo no realiza ninguna operación relacionada con la base de datos.

### Estado y Variables Globales
Ninguna variable global, de sesión o de entorno detectada en este fragmento.

### Dependencias y Flujo
- **Librerías externas**: `sqlite3`, `pandas`
- **Archivos del proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno.
- **Flujo de datos**: El archivo importa las librerías `sqlite3` y `pandas`. No hay interacción con otros archivos o servicios dentro del proyecto.


---

## Archivo: ./graphify-out/cache/ast/16e98e449e985d319c4dfc8a4658ccbdcd1a9530475fe2b69fd17c0f7cb87b08.json

### Resumen Funcional
El archivo `test_server.py` contiene una función `run_server()` que ejecuta un servidor utilizando la biblioteca `uvicorn`.

### Catálogo de Funciones y Clases
- `run_server()` - Ejecuta el servidor.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: `uvicorn`, `config`, `threading`, `time`, `requests`.
- **Archivos Importados por este Archivo**: Ninguno.
- **Archivos que Importan a este Archivo**: Ninguno.
- **Flujo de Datos**: La función `run_server()` llama al método `run` de la biblioteca `uvicorn`.

**Nota**: El archivo no interactúa con una base de datos ni contiene variables globales.


---

## Archivo: ./graphify-out/cache/ast/1954ef9c47b4818cebc23f63113b890cc9c7deb1a99977e09c5dfdfd40689fef.json

### Resumen Funcional
El archivo `test_map.py` es un script que realiza operaciones de monitoreo y análisis en un sistema de almacén (WMS) utilizando bibliotecas como pandas, SQLite3, os, pathlib, sys y config.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada directamente en el fragmento proporcionado.

### Interacción con Base de Datos
- **Motor**: SQLite3
- **Tablas**: Ninguna especificada explícitamente.
- **Columnas**: Ninguna especificada explícitamente.
- **Consultas SQL Crudas/ORM**: Ninguna.

### Estado y Variables Globales
Ninguna variable global, de sesión o de entorno detectada directamente en el fragmento proporcionado.

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`
  - `pandas`
  - `os`
  - `pathlib`
  - `sys`
  - `config`

- **Archivos del Proyecto que IMPORTA a este archivo (lo consumen)**: Ninguno.

- **Archivos del Proyecto que ESTE archivo IMPORTA (consume)**:
  - `config` (importado desde `scratch/test_map.py`, línea 9)

- **Dirección del Flujo de Datos**: El flujo de datos comienza en el archivo `test_map.py` y se extiende hacia las bibliotecas importadas, incluyendo la configuración (`config`).


---

## Archivo: ./graphify-out/cache/ast/1a4890105d6c56fd4d41006ee6ef2384ab692387c5895e2cb8e9d67280517e7c.json

### Resumen Funcional
El archivo `test_analytics.py` contiene una definición de clase `FakeRequest` y realiza importaciones de módulos necesarios para su funcionamiento.

### Catálogo de Funciones y Clases
- **FakeRequest()** - Breve propósito: No se proporciona en el fragmento, pero probablemente sea una clase utilizada para simular solicitudes HTTP en pruebas unitarias.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías externas**: `sqlite3`, `traceback`
- **Archivos del proyecto que IMPORTA a este archivo (`scratch/test_analytics.py`)**: `config`, `routes_analytics_vl06o`
- **Archivos del proyecto que ESTE archivo IMPORTA (`scratch/test_analytics.py`)**: Ninguno
- **Dirección del flujo de datos**: No se proporciona información sobre el flujo de datos específico en este fragmento.


---

## Archivo: ./graphify-out/cache/ast/1bf71bf325d72001f6b66e7b16870ffb13ef2c7a7077b5afe53eacc63abd6c0c.json

### Resumen Funcional
El archivo `fix_mb51_func.py` contiene una función `_prepare_user_location_analytics()` que se encarga de preparar estadísticas detalladas de usuarios y ubicaciones con actividad mensual.

### Catálogo de Funciones y Clases
- `_prepare_user_location_analytics()`: Prepara estadísticas detalladas de usuarios y ubicaciones con actividad mensual.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (se supone que las consultas SQL son generadas dinámicamente)
- **Columnas**: Ninguna (se supone que las consultas SQL son generadas dinámicamente)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `zfill`
  - `read_sql` (de SQLAlchemy)
  - `to_dict` (de pandas)
  - `fmt_num`

- **Archivos del Proyecto que IMPORTA a este archivo**: Ninguno

- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno

- **Flujo de Datos**:
  - La función `_prepare_user_location_analytics()` llama a varias funciones y métodos, incluyendo `zfill`, `read_sql`, `to_dict` y `fmt_num`. Estas llamadas se realizan dentro del flujo de la función para preparar las estadísticas detalladas.


---

## Archivo: ./graphify-out/cache/ast/1cc634b977c313b685269839394a52752cb1431525c5ec00fbdd46554ad0461f.json

### Resumen Funcional
El archivo `update_inv_kpis.py` es un script que realiza operaciones de actualización en el inventario del sistema de monitoreo de almacén (WMS). No contiene una descripción detallada de su funcionalidad, pero se infiere que interactúa con la base de datos para actualizar los KPIs del inventario.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna especificada explícitamente en el fragmento.
- **Columnas**: Ninguna especificada explícitamente en el fragmento.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Importado para interactuar con la base de datos SQLite.
  - `json`: Importado para manejar operaciones JSON, aunque no se ve claramente cómo se usa en el fragmento proporcionado.

- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno especificados.

- **Flujo de Datos**: El archivo importa bibliotecas necesarias y no contiene llamadas directas a funciones o métodos específicos, por lo que no hay un flujo claro de datos definido en el fragmento proporcionado.


---

## Archivo: ./graphify-out/cache/ast/214298c9dfecd526175e5eb35b9c2e61aeba7a4d22cf09a5dd4bba2043cd5baa.json

### Resumen Funcional
El archivo `free_ram.py` contiene funciones para gestionar la liberación de memoria en un sistema operativo macOS utilizando AppleScript. La función principal es `main()`, que invoca a otra función `quit_app()` para cerrar una aplicación de forma segura.

### Catálogo de Funciones y Clases
- `quit_app()` - Cierra una aplicaciónde forma segura usando AppleScript.
- `main()` - Flujo principal del script, que llama a `quit_app()`.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `os`
  - `subprocess`

- **Archivos del Proyecto que Importan a este Archivo**:
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno

- **Flujo de Datos**:
  - El script importa las librerías necesarias (`os` y `subprocess`) al inicio.
  - La función `main()` llama a la función `quit_app()`.
  - La función `quit_app()` ejecuta un comando AppleScript para cerrar una aplicación.

Este flujo es simple, sin interacción con bases de datos ni variables globales.


---

## Archivo: ./graphify-out/cache/ast/21d5b8af26579c3e12417bb799cdb466b760e31ee4529daf179dda0bf9f2639e.json

### Resumen Funcional
El archivo `predictive_engine.py` contiene una función llamada `generate_predictions()` que procesa movimientos de transacciones para generar modelos predictivos. La función utiliza diversas bibliotecas como pandas, numpy y SQLite para realizar operaciones de análisis y manipulación de datos.

### Catálogo de Funciones y Clases
- **generate_predictions()** - Procesa Movimientos Transactions para generar modelos predictivos: 1. Market

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:** No se especifican explícitamente las tablas o columnas manipuladas en este archivo.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `sqlite3`
  - `pandas`
  - `numpy`
  - `datetime`
  - `logging`
  - `itertools`
  - `collections`
  - `sys`
  - `os`
  - `core_wms_config`

- **Archivos del Proyecto que Importan a este Archivo:**
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa:**
  - `core_wms_config`

- **Flujo de Datos:** El archivo importa varias bibliotecas y dependencias, realiza operaciones de análisis y manipulación de datos utilizando pandas, numpy y SQLite, pero no se especifican las tablas o columnas específicas.


---

## Archivo: ./graphify-out/cache/ast/22724d61080e7569670c719f388a515631c3055265f55019f687e521cf7b246c.json

### Resumen Funcional
El archivo `pdf.py` contiene funciones para generar PDFs en un sistema de monitoreo de almacén (WMS). Incluye una función para generar un PDF único y otra para generar un reporte masivo con índice y picking list.

### Catálogo de Funciones y Clases
- **generate_pdf(str, bool, str, Session)** - Genera un PDF para una única entrega.
- **generate_pdf_bulk(str, str, str, str, str, bool, str, Session)** - Genera un reporte masivo con índice y picking list.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: No se especifican explícitamente en el fragmento.
- **Columnas**: No se especifican explícitamente en el fragmento.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno mencionadas en el fragmento.

### Dependencias y Flujo
- **Librerías Externas**:
  - `io`
  - `logging`
  - `core_database`
  - `sqlalchemy_orm`
  - `sqlalchemy`
  - `pandas`
  - `datetime`
  - `typing`
  - `fastapi`
  - `fastapi_responses`
  - `config`
  - `core_pdf_engine`
  - `repositories_deliveries`
  - `core_pdf_reports`

- **Archivos del Proyecto que Importan a Este Archivo**:
  - No se especifican explícitamente en el fragmento.

- **Flujo de Datos**: El archivo importa varias librerías y módulos, incluyendo `DeliveriesRepository` y otros componentes del sistema WMS. Las funciones `generate_pdf` y `generate_pdf_bulk` utilizan estos componentes para interactuar con la base de datos y generar PDFs.

Este análisis proporciona una visión detallada de las funcionalidades, dependencias y interacciones del archivo `pdf.py` en el contexto del sistema WMS.


---

## Archivo: ./graphify-out/cache/ast/248900fa5696f9164b38c451ab4ccbd5ea7b766f0ae237c81888e37db8eb8795.json

### Resumen Funcional
El archivo `app.py` es el punto de entrada principal del sistema de monitoreo de almacén (WMS). Define la configuración y arranque asincrónico de la aplicación FastAPI, incluyendo la inicialización de bases de datos, la creación de rutas, y la gestión del ciclo de vida de la aplicación.

### Catálogo de Funciones y Clases
- `lifespan()`: Maneja el ciclo de vida de la aplicación. Gestiona el arranque asincrónico.
- `initialize_app()`: Configura y prepara la aplicación FastAPI.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
**Dependencias Externas:**
- `os`
- `logging`
- `contextlib`
- `warnings`
- `fastapi`
- `fastapi_responses`
- `fastapi_staticfiles`
- `config`
- `core_app_instance`
- `routes_config`

**Archivos del Proyecto que Importan a este Archivo:**
Ninguno

**Archivos del Proyecto que Este Archivo Importa:**
Ninguno

**Flujo de Datos:**
El archivo `app.py` importa varias bibliotecas y módulos necesarios para configurar y arrancar la aplicación FastAPI. Luego, define dos funciones principales: `lifespan()` y `initialize_app()`. La función `lifespan()` se encarga del ciclo de vida de la aplicación, mientras que `initialize_app()` configura y prepara la aplicación FastAPI.


---

## Archivo: ./graphify-out/cache/ast/2512d99f377792ee48a36d08df70590f533e225fac02afe6c96c2820fd43e7cb.json

### Resumen Funcional
El archivo `analytics_proyecciones.py` contiene las rutas y lógica para obtener el contexto de proyecciones y los datos de proyecciones en un sistema de monitoreo de almacén (WMS). Las funciones principales son `get_proyecciones_context()` y `get_analytics_proyecciones()`, que manejan la obtención de datos de proyecciones y su formato de salida.

### Catálogo de Funciones y Clases
- **`get_proyecciones_context()`** - Obtiene el contexto de proyecciones, priorizando la caché.
- **`get_analytics_proyecciones()`** - Retorna los datos de proyecciones en formato JSON.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales, de sesión o diccionarios quemados en el código que almacenen estado crítico.

### Dependencias y Flujo
- **Dependencias Externas**: `fastapi`, `core_auth`, `fastapi_responses`, `core_state`, `db_predictive_engine`, `config`.
- **Flujo de Datos**:
  - El archivo importa varias bibliotecas y módulos necesarios para su funcionamiento.
  - La función `get_proyecciones_context()` realiza operaciones como obtener el estado de la aplicación, recuperar datos de caché, generar predicciones y almacenarlos en caché.
  - La función `get_analytics_proyecciones()` limpia la caché y retorna los datos de proyecciones en formato JSON.

Este archivo es parte del componente "Routes" del sistema WMS, donde se definen las rutas para interactuar con el servicio de análisis de proyecciones.


---

## Archivo: ./graphify-out/cache/ast/2648ddaf09c775d584e45812bcb9a284a0aea4428f4e77304f12cc1886df102e.json

### Resumen Funcional
El archivo `analyze_dom.py` contiene una función que realiza el análisis de elementos DOM para identificar aquellos que son considerados grandes.

### Catálogo de Funciones y Clases
- **find_large_elements()** - Identifica y devuelve los elementos DOM que son considerados grandes.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `asyncio`, `httpx`, `bs4`
- **Archivos Importados por Este Archivo**:
  - Ninguno
- **Archivos que Importan a Este Archivo**:
  - Ninguno
- **Flujo de Datos**: El archivo importa bibliotecas para realizar operaciones asíncronas, HTTP y análisis de HTML. La función `find_large_elements()` utiliza estas bibliotecas para obtener y analizar elementos DOM.

### Notas Adicionales
La función `find_large_elements()` realiza una solicitud HTTP para obtener el contenido de una página web, luego usa BeautifulSoup para parsear el HTML y encontrar todos los elementos que cumplen con ciertos criterios de tamaño. Los resultados se almacenan en una lista y devuelven finalmente.


---

## Archivo: ./graphify-out/cache/ast/2698c4f92f61d2045d9a40677c212db456adb8e797d6fef296d7bf17bbbbc850.json

### Resumen Funcional
El archivo `migrate_monthly_sql.py` contiene el código necesario para migrar los datos de la tabla `vl_sla_monthly_trend` en la base de datos de configuración al nuevo formato.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: `vl_sla_monthly_trend`
- **Columnas**: No especificadas explícitamente en el fragmento proporcionado.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `json`: Para manejar operaciones JSON.
  - `pandas`: Para procesar los datos en formato DataFrame.

- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno

El flujo de datos es simple: el script importa las librerías necesarias, realiza la migración de los datos y no depende de ninguna otra parte del proyecto.


---

## Archivo: ./graphify-out/cache/ast/26acef1135f4ddafeda2dd941412cb7d1aa1e6c1c655718558d04d2044dafbd0.json

### Resumen Funcional
El archivo `test_efficiency.py` contiene una función llamada `calculate_efficiency()` que realiza cálculos de eficiencia en un almacén utilizando pandas, numpy y SQLite.

### Catálogo de Funciones y Clases
- **calculate_efficiency()** - Realiza cálculos de eficiencia en los datos del almacén.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** Ninguna (se asume que la conexión se realiza a través de una base de datos SQLite local).
- **Columnas:** Ninguna (se asume que las consultas SQL son generadas dinámicamente).

### Estado y Variables Globales
- Ninguna.

### Dependencias y Flujo
- **Librerías Externas:**
  - `sqlite3`
  - `pandas`
  - `numpy`

- **Archivos del Proyecto que Importan a este Archivo:** Ninguno.
- **Archivos del Proyecto que Este Archivo Importa:** Ninguno.

**Flujo de Datos:**
1. La función `calculate_efficiency()` se importa desde `test_efficiency.py`.
2. Se realiza una conexión a la base de datos SQLite (implícita).
3. Se ejecutan consultas SQL para leer los datos del almacén.
4. Los datos son procesados utilizando pandas y numpy.
5. El resultado del cálculo de eficiencia se devuelve.

**Ejemplo de Flujo:**
```python
import sqlite3
import pandas as pd
import numpy as np

def calculate_efficiency():
    # Conexión a la base de datos SQLite (implícita)
    conn = sqlite3.connect('almacen.db')
    
    # Consulta SQL para leer los datos del almacén
    query = "SELECT * FROM inventario"
    df = pd.read_sql(query, conn)
    
    # Procesamiento de los datos con pandas y numpy
    df['fecha'] = pd.to_datetime(df['fecha'])
    df.dropna(inplace=True)
    dias_laborables = np.busday_count(df['fecha'].min(), df['fecha'].max())
    
    # Cálculo de eficiencia
    eficiencia = len(df) / dias_laborables
    
    return eficiencia

# Ejecución de la función
result = calculate_efficiency()
print(f"Eficiencia del almacén: {result}")


---

## Archivo: ./graphify-out/cache/ast/270d77c0b49bdfc62c4cda6d71d370da9619bc2a608b04020a4387bd92c01b0b.json

### Resumen Funcional
El archivo `repositories/widgets.py` contiene la definición de una clase `WidgetRepository` que hereda de `BaseRepository`. Esta clase incluye dos métodos: `.execute_widget()` y `.execute_drilldown()`, los cuales realizan operaciones relacionadas con el procesamiento y visualización de datos.

### Catálogo de Funciones y Clases
- **Clase:** `WidgetRepository`
  - **Método:** `.execute_widget()`
    - **Parámetros:** No especificados en el fragmento.
    - **Propósito:** Ejecuta una operación widget específica.
  - **Método:** `.execute_drilldown()`
    - **Parámetros:** No especificados en el fragmento.
    - **Propósito:** Realiza una operación de drilldown.

### Interacción con Base de Datos
- **Motor:** SQLite (implícito a través del uso de SQLAlchemy).
- **Tablas y Columnas:** No se mencionan explícitamente tablas o columnas en el fragmento.
- **Consultas SQL Crudas/ORM:** Se utilizan métodos como `get`, `append`, `drop`, `fillna`, `pivot_table`, `tolist` de la biblioteca `pandas`. También se hace uso del método `read_sql` para leer datos desde una consulta SQL.

### Estado y Variables Globales
- **Variables Globales:** No hay variables globales mencionadas en el fragmento.
- **Sesión/Entorno:** No hay referencias a sesiones o entornos específicos.
- **Diccionarios Quemados:** No se utilizan diccionarios quemados en el código.

### Dependencias y Flujo
- **Librerías Externas:**
  - `logging`
  - `json`
  - `pandas`
  - `sqlalchemy`
  - `typing`
- **Archivos del Proyecto que Importa (`repositories/widgets.py`):**
  - `users_christianykelly_desktop_monitorweb_repositories_base_py`
  - `core_helpers_dynamic_executor`
  - `core_schemas`
  - `core_query_engine`
  - `core_utils`
- **Archivos del Proyecto que son Importados por (`repositories/widgets.py`):**
  - Ninguno mencionado en el fragmento.

**Flujo de Datos:**
El flujo de datos comienza en los métodos `.execute_widget()` y `.execute_drilldown()`, donde se realizan operaciones con `pandas`. Estos métodos interactúan con la base de datos a través de SQLAlchemy, pero no se especifican las tablas o columnas específicas.


---

## Archivo: ./graphify-out/cache/ast/275db49a0ee9d430e5c68c88f7f4cbc797e9d8e5e863d5e364fe78c44cdfb1ca.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `consolidator.py` es un script que gestiona la consolidación de archivos WMS en una base de datos SQLite. Realiza tareas como la conexión a la base de datos, análisis de fechas en los nombres de archivos, consolidación de archivos cronológicamente, actualización de tablas con los datos más recientes, enriquecimiento de transacciones con información de stock y movimientos, y cierre seguro de la conexión.

### Catálogo de Funciones y Clases
- `DataConsolidator()`: Clase principal que gestiona la consolidación de archivos WMS.
  - `__init__(self, db_path: str)`: Inicializa el objeto con la ruta a la base de datos SQLite.
  - `__enter__(self)`: Método para manejar el protocolo de contexto (with).
  - `__exit__(self, exc_type, exc_val, exc_tb)`: Método para manejar el protocolo de contexto (with).
  - `connect(self)`: Establece la conexión a la base de datos y configura optimizaciones.
  - `_parse_file_date(self, file_name: str) -> datetime.date`: Extrae la fecha del nombre del archivo en formato dd-mm-yyyy.
  - `consolidate_folder(self, folder_path: str, target_table: str)`: Consolida archivos cronológicamente en una tabla específica.
  - `overwrite_with_latest(self, source_folder: str, target_table: str)`: Reemplaza la tabla con los datos del archivo más reciente.
  - `enrich_deliveries_with_stock(self, deliveries_table: str, stock_table: str)`: Enriquece las transacciones con información de stock actual.
  - `backfill_from_movements(self, deliveries_table: str, movements_table: str)`: Sincroniza datos faltantes desde la tabla Movimientos.
  - `backfill_texts(self, deliveries_table: str, stock_table: str, movements_table: str)`: Sincroniza descripciones faltantes desde Stock y Movimientos.
  - `update_sla_with_tasks(self, sla_table: str, tasks_table: str)`: Actualiza el SLA cruzando fechas con Tareas.
  - `close(self)`: Cierra la conexión de forma segura.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - No se especifican explícitamente las tablas en este fragmento, pero se infiere que existen tablas como `deliveries`, `stock`, `movements` y `sla`.
- Columnas:
  - No se especifican explícitamente las columnas en este fragmento.
- Consultas SQL Crudas: No hay consultas SQL crudas directamente visibles, pero se infiere que existen llamadas a métodos como `execute`, `to_sql` y otros que implican operaciones de base de datos.

### Estado y Variables Globales
No hay variables globales explícitamente mencionadas en este fragmento.

### Dependencias y Flujo
- Librerías Externas:
  - `os`
  - `sqlite3`
  - `logging`
  - `re`
  - `pathlib`
  - `datetime`
  - `typing`
  - `services_etl`
  - `users_christianykelly_desktop_monitorweb_db_enrichment_py`
  - `core_security`
- Archivos del Proyecto que Este Archivo Importa:
  - No se especifican explícitamente los archivos que este archivo importa.
- Archivos del Proyecto que Importan a Este Archivo:
  - No se especifican explícitamente los archivos que importan a este archivo.

El flujo de datos es desde `main()` hacia `DataConsolidator` y sus métodos, pasando por funciones auxiliares y adaptadores para procesar y guardar datos.


---

## Archivo: ./graphify-out/cache/ast/27822743d1ba852b1150577cdf502fb5d2b650df01bdc61a394bfb6ad5311f9b.json

### Resumen Funcional
El archivo `deliveries.py` contiene la implementación del adaptador para procesar Entregas de Salida (Deliveries) en el sistema de monitoreo de almacén (WMS). Este adaptador hereda de `BaseWMSProcessor` y define métodos para validar archivos, obtener columnas requeridas, limpiar dataframes, sanitizar nombres de columnas, realizar procesamiento post, e insertar o actualizar chunks de datos en la base de datos.

### Catálogo de Funciones y Clases
- **OutboundDeliveryAdapter()** - Adaptador para procesar Entregas de Salida (Deliveries).
  - `.validate_file(path: Path) -> bool` - Valida el archivo proporcionado.
  - `._get_required_columns() -> List[str]` - Obtiene las columnas requeridas.
  - `._get_primary_keys() -> List[str]` - Obtiene las claves primarias.
  - `._clean_dataframe(df: DataFrame) -> DataFrame` - Limpia el dataframe.
  - `._sanitizar_nombres_columnas(index: Index) -> None` - Sanitiza los nombres de las columnas.
  - `._post_process(file_path: str) -> None` - Realiza procesamiento post.
  - `._upsert_chunk(connection: Connection, df: DataFrame, table_name: str) -> None` - Inserta o actualiza chunks de datos en la base de datos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas Modificadas/Leídas:**
  - Tabla: `outbound_deliveries`
    - Columnas: Dependiendo del contexto, se pueden modificar o leer columnas específicas.
  - Consultas SQL Crudas:
    - Ejemplo de consulta para crear índices: `CREATE INDEX idx_outbound_deliveries_column ON outbound_deliveries(column_name);`

### Estado y Variables Globales
- **Ninguna**

### Dependencias y Flujo
- **Librerías Externas:** pandas, pathlib, typing, sqlite3
- **Archivos del Proyecto que Importan a este Archivo:**
  - `users_christianykelly_desktop_monitorweb_services_etl_base_py`
  - `core_wms_utils`
- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno

**Flujo de Datos:** El archivo `deliveries.py` se importa por otros archivos y utiliza métodos definidos en él para procesar los datos de entregas de salida, incluyendo la validación, limpieza y carga en la base de datos.


---

## Archivo: ./graphify-out/cache/ast/2f83b9a0f80542770ddcfa30996a5dc636a038df795934b25d3d946809a96a27.json

### Resumen Funcional
El archivo `productivity_monthly.py` contiene la lógica de negocio para el cálculo y recuperación de datos de productividad mensuales en un sistema de monitoreo de almacén (WMS). Define una clase `ProductivityMonthlyService` que proporciona métodos para obtener resúmenes mensuales de movimientos de usuarios y detalles específicos.

### Catálogo de Funciones y Clases
- **ProductivityMonthlyService()** - Inicializa el servicio con una sesión.
- **get_monthly_productivity_data(date: str) -> Any** - Obtiene los datos de productividad mensuales para un usuario específico en un mes dado.
- **get_user_movements_monthly_summary(user_id: str, month: str)** - Retorna resúmenes mensuales de movimientos de usuarios.
- **get_user_movements_monthly_details(user_id: str, month: str)** - Retorna detalles específicos de los movimientos de usuarios en un mes dado.

### Interacción con Base de Datos
No se especifican consultas SQL crudas o llamadas a ORM explícitas. La interacción con la base de datos se realiza a través del repositorio `TasksRepository`.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: 
  - Importa módulos como `logging`, `typing`, `sqlalchemy_orm` y `repositories_tasks`.
  - Utiliza la clase `Session` de SQLAlchemy.
  
- **Flujo**:
  - El archivo `productivity_monthly.py` importa varios módulos y dependencias necesarias para su funcionamiento.
  - La clase `ProductivityMonthlyService` se utiliza en otros archivos del proyecto, lo que indica que este archivo es consumido por otros componentes del sistema.


---

## Archivo: ./graphify-out/cache/ast/304c8d2fa81f6a72f36d68335f803a792da5c01823caf3628b36db205cd41f4b.json

### Resumen Funcional
El archivo `build_analytics.py` contiene funciones para extraer información de un cuerpo de texto y procesarla, finalmente escribiendo el resultado en un archivo.

### Catálogo de Funciones y Clases
- `extract_body()` - Extrae información relevante del cuerpo de texto.
- `main()` - Llama a la función `extract_body()` y realiza operaciones adicionales para procesar y guardar los datos.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: No se mencionan dependencias externas específicas.
- **Archivos Importados**: El archivo importa el módulo `re` (módulo de expresiones regulares).
- **Flujo de Datos**:
  - `main()` llama a `extract_body()`.
  - `extract_body()` realiza operaciones como lectura, búsqueda y procesamiento del texto.
  - Los resultados son procesados en `main()` y finalmente escritos en un archivo.

El flujo general es: `main()` -> `extract_body()` -> Procesamiento de datos -> Escritura en archivo.


---

## Archivo: ./graphify-out/cache/ast/304f886cabadc03a8789908d8ad0097d51432255b665a2d566f642dc1fddf98b.json

### Resumen Funcional
El archivo `query_utils.py` contiene funciones que se utilizan para extraer parámetros de visualización y valores métricos de datos.

### Catálogo de Funciones y Clases
- `get_bound_params_from_visual_state(visual_state: str) -> List[str]`: Extrae los bind params (?) de un visual_state JSON serializado. Lee la lista de parámetros de enlace.
- `extract_metric_value(df: pd.DataFrame, column_name: str) -> float`: Extrae el valor numérico principal de un DataFrame de resultado de query.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `json`, `pandas` (pd)
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno
- **Archivos del Proyecto que Este Archivo Importa**: Ninguno
- **Flujo de Datos**: El archivo importa y utiliza métodos de las librerías `json` y `pandas` para procesar datos.


---

## Archivo: ./graphify-out/cache/ast/30755f350f7868b645cd6840aa3fecd61ad22f5fd2ad46633fe069b0085343bf.json

### Resumen Funcional
El archivo `update_abc.py` es un script que realiza operaciones de actualización en una base de datos SQLite.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna especificada
- **Columnas**: Ninguna especificada
- **Consultas SQL Crudas o Llamadas a ORM**: Importa el módulo `sqlite3` para interactuar con la base de datos.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `sqlite3`
- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno
- **Dirección del Flujo de Datos**: El archivo importa el módulo `sqlite3` y no realiza ninguna operación específica sobre la base de datos.


---

## Archivo: ./graphify-out/cache/ast/30b35bde69ca83a89e98700247ddb3d26386d4301bfdd707912c44bd121ebb3b.json

### Resumen Funcional
El archivo `run_compiled_query.py` contiene código que realiza consultas SQL compiladas utilizando el motor de base de datos SQLite y la biblioteca pandas para procesar los resultados.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** Ninguna (No se mencionan consultas específicas a tablas)
- **Columnas:** Ninguna (No se mencionan consultas específicas a columnas)

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas:**
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para procesar los resultados de las consultas SQL.

- **Flujo de Datos:**
  - El archivo `run_compiled_query.py` importa `sqlite3` y `pandas`.
  - No se mencionan funciones o métodos específicos, por lo que no hay un flujo de datos definido en este fragmento.


---

## Archivo: ./graphify-out/cache/ast/372cf2fa28e957601b1d7c91d64b422fff4416537b764eafe3b626dc56b3fc2e.json

### Resumen Funcional
El archivo `test_dashboard_context.py` contiene una función llamada `diag_dashboard()` que realiza operaciones de conexión a una base de datos SQLite, obtiene contexto de tareas y cierra la conexión.

### Catálogo de Funciones y Clases
- `diag_dashboard()` - Realiza operaciones de conexión a una base de datos SQLite, obtiene contexto de tareas y cierra la conexión.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:** Ninguna (se asume que las consultas SQL están implícitas en los métodos `connect`, `get_tasks_context`, `get` y `close`)
- **Consultas SQL Crudas o Llamadas a ORM:** No se especifican consultas SQL crudas ni llamadas a ORM explícitas.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `sqlite3`
- **Archivos del Proyecto que IMPORTA (consume):** `routes_tasks`
- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen):** Ninguno
- **Dirección del Flujo de Datos:** El flujo comienza en la función `diag_dashboard()`, realiza operaciones de base de datos y luego cierra la conexión.


---

## Archivo: ./graphify-out/cache/ast/396390b1d9abe747b9a11af5b5a51b08c75407a1f32f902fb2d367909bf04e41.json

### Resumen Funcional
El archivo `generate_graphify.py` contiene una función `run_graphify()` que realiza diversas operaciones de sistema y manejo de archivos, como la creación de directorios, copia de archivos, escritura en archivos, ejecución de comandos externos, etc.

### Catálogo de Funciones y Clases
- **run_graphify()** - Realiza las operaciones descritas anteriormente.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**: `os`, `subprocess`, `shutil`.
- **Archivos Importados por Este Archivo**: Ninguno.
- **Archivos que Importan a Este Archivo**: Ninguno.
- **Flujo de Datos**: El flujo de datos se centra en la manipulación de archivos y directorios del sistema operativo, así como la ejecución de comandos externos.


---

## Archivo: ./graphify-out/cache/ast/3c0c1d4e0ad1fc97ca573ef39e45e21ee9e3e49e50ed4c4c8dc0aea894bf2b00.json

### Resumen Funcional
El archivo `productivity_daily.py` contiene la lógica de negocio para el servicio de productividad diaria, que incluye métodos para obtener fechas disponibles, datos de productividad y resúmenes/detalles de movimientos diarios de usuarios.

### Catálogo de Funciones y Clases
- `ProductivityDailyService` - Servicio principal para la gestión de datos de productividad diaria.
  - `__init__(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - `get_available_dates()` - Obtiene todas las fechas disponibles en el sistema.
  - `get_productivity_data(date: str) -> Any` - Retorna los KPIs de productividad para una fecha específica (YYYY-MM-DD).
  - `get_user_movements_daily_summary(user_id: str, date: str)` - Retorna un resumen diario de movimientos de usuario.
  - `get_user_movements_daily_details(user_id: str, date: str)` - Retorna los detalles diarios de movimientos de usuario.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas y Columnas:
  - **Ninguna** (El archivo no contiene consultas SQL explícitas ni llamadas a ORM que interactúen directamente con la base de datos).

### Estado y Variables Globales
- **Ninguna** (No se detectan variables globales, de sesión o diccionarios quemados en el código).

### Dependencias y Flujo
- **Librerías Externas**: `logging`, `typing`, `sqlalchemy.orm`
- **Archivos del Proyecto que Importa a Este Archivo**: Ninguno.
- **Archivos del Proyecto que Este Archivo Importa**: `repositories.tasks`
- **Flujo de Datos**: El archivo importa dependencias necesarias y utiliza el repositorio `TasksRepository` para obtener datos. Los métodos del servicio interactúan con los datos internos del sistema, no con la base de datos directamente.

**Nota**: El archivo no contiene consultas SQL explícitas ni llamadas a ORM que interactúen directamente con la base de datos. Todas las operaciones se realizan en memoria o mediante métodos interno del servicio.


---

## Archivo: ./graphify-out/cache/ast/3cd7e0c173e88fb532d1d35ceaeea87dafb9c8efddb884ae8c20ba1c25891b9f.json

### Resumen Funcional
El archivo `test_ia.py` contiene una función llamada `test_analytics_ia()` que realiza operaciones de análisis utilizando la biblioteca `httpx` para hacer solicitudes HTTP y procesar los resultados.

### Catálogo de Funciones y Clases
- **test_analytics_ia()** - Realiza operaciones de análisis mediante solicitudes HTTP.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: `asyncio`, `httpx`, `sys`, `os`, `time`.
- **Flujo de Datos**:
  - El archivo importa varias bibliotecas (`asyncio`, `httpx`, `sys`, `os`, `time`).
  - La función `test_analytics_ia()` realiza una solicitud HTTP utilizando la clase `AsyncClient` de la biblioteca `httpx`.
  - Los resultados de la solicitud son procesados y manipulados dentro de la función.

**Nota**: El archivo no interactúa con ninguna base de datos ni utiliza variables globales.


---

## Archivo: ./graphify-out/cache/ast/3f1256fac516858adab62c10c73396d4972d27628e54666f5c3f668c017ccc2d.json

### Resumen Funcional
El archivo `auth.py` contiene funciones y clases relacionadas con la autenticación y seguridad del sistema de monitoreo de almacén (WMS). Incluye operaciones como el hash de contraseñas, verificación de contraseñas, creación de tokens JWT, decodificación de tokens y gestión de usuarios.

### Catálogo de Funciones y Clases
- `TokenResponse` - Modelo Pydantic para la respuesta de autenticación.
- `UserCreate` - Modelo Pydantic para crear un nuevo usuario.
- `ChangePasswordRequest` - Modelo Pydantic para cambiar la contraseña de un usuario.
- `UserPublic` - Modelo Pydantic para representar un usuario de manera pública.
- `hash_password(password: str) -> str` - Genera un hash bcrypt del password.
- `verify_password(plain_password: str, hashed_password: str) -> bool` - Verifica si una contraseña sin encriptar coincide con su hash.
- `create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> Tuple[str, int]` - Crea un JWT firmado con HS256.
- `decode_token(token: str) -> Union[dict, None]` - Decodifica y valida un JWT. Retorna None si es inválido o expirado.
- `get_current_user(request: Request, session: Session) -> User` - Depende del token JWT para extraer el usuario actual. Si no hay token, retorna un error.
- `require_auth(user: User) -> User` - EXIGE que el usuario esté autenticado (no invitado).
- `require_admin(user: User) -> User` - EXIGE que el usuario tenga rol de administrador. Lanza 403 si no tiene permisos.
- `init_auth_db()` - Crea las tablas de autenticación si no existen.
- `ensure_admin_exists()` - Crea el usuario admin por defecto si no existe ninguno.

### Interacción con Base de Datos
No se especifican consultas SQL crudas o llamadas a ORM explícitas en este archivo. La interacción con la base de datos parece ser gestionada a través de métodos como `get`, `first`, `query` y `count`.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: `os`, `logging`, `datetime`, `typing`, `bcrypt`, `jwt`, `fastapi`, `fastapi_security`, `sqlalchemy_orm`, `pydantic`.
- **Archivos del Proyecto que Este Archivo Importa**:
  - `core/auth.py` (se importa a sí mismo)
  - `os`
  - `logging`
  - `datetime`
  - `typing`
  - `bcrypt`
  - `jwt`
  - `fastapi`
  - `fastapi_security`
  - `sqlalchemy_orm`
  - `pydantic`
- **Archivos del Proyecto que Importan a Este Archivo**:
  - No se especifica en el fragmento proporcionado.

El flujo de datos fluye desde las funciones y métodos que dependen de otras funciones y clases, hasta la interacción con la base de datos (si es necesario).


---

## Archivo: ./graphify-out/cache/ast/4046e65c894c9454c79a7ca4a62913f3f4975421bbcb99dd25004c9d2315a208.json

### Resumen Funcional
El archivo `conftest.py` contiene funciones de configuración y inicialización para pruebas en un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Define clientes de prueba, sesiones de base de datos y funciones auxiliares para preparar el entorno de pruebas.

### Catálogo de Funciones y Clases
- `skip_warmup()` - No tiene parámetros. Proporciona una razón: "El warm_up ahora ocurre dentro del lifespan."
- `session_db()` - No tiene parámetros. Crea e inicializa la base de datos maestra compartida para toda la sesión de pruebas.
- `test_db()` - No tiene parámetros. Proporciona aislamiento de datos entre pruebas individuales.
- `client()` - No tiene parámetros. Cliente de pruebas de FastAPI configurado para interactuar con la BD de sesión.
- `auth_client()` - No tiene parámetros. Proporciona un cliente con token de administrador pre-autenticado.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas y Columnas**:
  - Tabla: Ninguna específica mencionada en el código proporcionado.
- **Consultas SQL Crudas o Llamadas a ORM**:
  - `connect()`
  - `executescript()`
  - `commit()`
  - `init_auth_db()`
  - `init_config_db()`
  - `seed_initial_config()`
  - `close()`
  - `execute()`

### Estado y Variables Globales
- Ninguna variable global, de sesión o de entorno quemada en el código.

### Dependencias y Flujo
- **Librerías Externas**:
  - `os`
  - `secrets`
  - `pathlib`
  - `sqlite3`
  - `unittest_mock`
  - `pytest`
  - `fastapi_testclient`
  - `config`
  - `app`
- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno mencionado.
- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno mencionado.

El flujo de datos es desde las funciones definidas en `conftest.py` hacia el resto del proyecto, proporcionando configuración y clientes de prueba necesarios para ejecutar pruebas.


---

## Archivo: ./graphify-out/cache/ast/418aaa07103f9a5817ee4bd7c1ea4ab84d1ad49d46b41118c661bd6e64189aa1.json

### Resumen Funcional
El archivo `test_cvalderrama.py` contiene una función de prueba llamada `test_query()` que realiza operaciones básicas en una base de datos SQLite.

### Catálogo de Funciones y Clases
- `test_query()` - Realiza consultas a la base de datos SQLite.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (operaciones directas sobre la conexión)
- **Columnas**: Ninguna (operaciones directas sobre la conexión)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: `sqlite3`
- **Archivos Importados por este Archivo**: Ninguno
- **Archivos que Importan a este Archivo**: Ninguno
- **Flujo de Datos**: El archivo importa el módulo `sqlite3` y realiza operaciones directas sobre la conexión a la base de datos SQLite.


---

## Archivo: ./graphify-out/cache/ast/41c6ecac133636d81ee103b15a4c36b1f085bba82765ec748007bd0682059258.json

### Resumen Funcional
El archivo `__init__.py` en la carpeta `scripts` es el punto de entrada para las funcionalidades relacionadas con el monitoreo del almacén. No contiene ninguna lógica específica, solo sirve como marcador de paquete.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna


---

## Archivo: ./graphify-out/cache/ast/4316fb8a7f251e010878cbae3e36cdce8ec23750ea17752236f4c23ea09e5b39.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `query_builder.py` contiene una función que compila un `VisualQueryBuilderPayload` validado en una tupla `(sql_text, bound_params)`. Esta función utiliza una sesión de SQLAlchemy para interactuar con la base de datos.

### Catálogo de Funciones y Clases
- **build_sql_from_payload(payload: VisualQueryBuilderPayload) -> Tuple[str, List[Any]]** - Compila un `VisualQueryBuilderPayload` validado en una tupla `(sql_text, bound_params)`.

### Interacción con Base de Datos
- **Motor:** SQLite
- **TABLAS:** Ninguna (el código no interactúa directamente con tablas de la base de datos).
- **COLUMNAS:** Ninguna (el código no interactúa directamente con columnas de la base de datos).

### Estado y Variables Globales
- **session:** Variable global que representa una sesión de SQLAlchemy.

### Dependencias y Flujo
- **Librerías Externas:**
  - `logging`
  - `typing`
  - `sqlalchemy.orm`
  - `sqlalchemy`
  - `fastapi`
  - `core_macros`
  - `core_query_validators`

- **Archivos del Proyecto que Importan a este Archivo (`query_builder.py`):** Ninguno.

- **Archivos del Proyecto que Este Archivo Importa:**
  - `core/macros`
  - `core/query_validators`

- **Flujo de Datos:** El archivo importa varias bibliotecas y módulos para su uso interno. La función `build_sql_from_payload` utiliza estos recursos para procesar el payload y generar la consulta SQL correspondiente.


---

## Archivo: ./graphify-out/cache/ast/4a08c549105832adb0358bb214615dadedbc01a9ad5d105e8ce6999f34f120a8.json

### Resumen Funcional
El archivo `models_transaccional.py` contiene definiciones de clases para diferentes entidades del sistema de monitoreo de almacén (WMS), utilizando SQLAlchemy como ORM.

### Catálogo de Funciones y Clases
- **WarehouseTask** - Representa una tarea en el almacén.
  - `__repr__()` - Devuelve una representación legible de la instancia.
- **InventoryMovement** - Representa un movimiento de inventario.
  - `__repr__()` - Devuelve una representación legible de la instancia.
- **OutboundDelivery** - Representa una entrega saliente.
  - `__repr__()` - Devuelve una representación legible de la instancia.
- **StockLevel** - Representa el nivel de stock.
  - `__repr__()` - Devuelve una representación legible de la instancia.
- **Lx02Pendiente** - Representa un pedido pendiente.
  - `__repr__()` - Devuelve una representación legible de la instancia.
- **SyncManifest** - Representa un manifiesto de sincronización.
  - No tiene métodos definidos en el fragmento.
- **AnalyticsSnapshot** - Representa una instantánea de análisis.
  - No tiene métodos definidos en el fragmento.
- **AutorAreaMapping** - Representa un mapeo de área autorizada.
  - No tiene métodos definidos en el fragmento.

### Interacción con Base de Datos
El archivo utiliza SQLAlchemy como ORM para interactuar con la base de datos. Las clases heredan de `Base`, lo que sugiere que están vinculadas a tablas en la base de datos SQLite. Sin embargo, no se proporciona información detallada sobre las columnas específicas o consultas SQL.

### Estado y Variables Globales
No hay variables globales, de sesión ni diccionarios quemados en el fragmento proporcionado.

### Dependencias y Flujo
- **Dependencias**: El archivo importa `typing`, `sqlalchemy`, `sqlalchemy_orm` y `core_database`.
- **Flujo**: 
  - `models_transaccional.py` depende de estos módulos.
  - No hay archivos que dependan directamente de este archivo.

Este fragmento muestra la definición de clases ORM para diferentes entidades del sistema WMS, utilizando SQLAlchemy como ORM y SQLite como motor de base de datos.


---

## Archivo: ./graphify-out/cache/ast/4d1f4a8e2b19730131b2fcce03e403741f4d454e7182dc23ff29de4aed1c34cb.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `routes/settings.py` contiene funciones y métodos relacionados con la gestión de configuraciones en un sistema de monitoreo de almacén (WMS). Incluye endpoints para obtener, actualizar y gestionar diferentes tipos de configuraciones como estados, costos centros, feriados y consultas.

### Catálogo de Funciones y Clases
- **invalidate_caches()** - Limpia el caché global en memoria y elimina todos los snapshots de base de datos.
- **SettingUpdate** - Modelo Pydantic para actualizar configuraciones.
- **StatusMappingUpdate** - Modelo Pydantic para actualizar mapeos de estados.
- **CostCenterMappingUpdate** - Modelo Pydantic para actualizar mapeos de costos centros.
- **HolidayAdd** - Modelo Pydantic para agregar feriados.
- **QueryUpdate** - Modelo Pydantic para actualizar consultas.
- **settings_view()** - Endpoint que renderiza el panel de control de configuraciones SaaS.
- **api_get_settings()** - Endpoint para obtener las configuraciones actuales.
- **api_update_setting()** - Endpoint para actualizar una configuración específica.
- **api_upsert_status()** - Endpoint para insertar o actualizar un estado.
- **api_delete_status()** - Endpoint para eliminar un estado.
- **api_upsert_cost_center()** - Endpoint para insertar o actualizar un mapeo de costos centros.
- **api_delete_cost_center()** - Endpoint para eliminar un mapeo de costos centros.
- **api_add_holiday()** - Endpoint para agregar un feriado.
- **api_sync_holidays()** - Endpoint para sincronizar automáticamente los feriados nacionales (Chile).
- **api_delete_holiday()** - Endpoint para eliminar un feriado.
- **api_get_query()** - Endpoint para obtener una consulta específica.
- **api_update_query()** - Endpoint para actualizar una consulta específica.
- **api_get_schema()** - Endpoint para obtener el esquema de datos para el editor.
- **api_preview_table()** - Endpoint para previsualizar una tabla.
- **api_query_preview()** - Endpoint para previsualizar los resultados de una consulta.
- **api_build_sql()** - Endpoint para compilar el estado visual del constructor en SQL parametrizado seguro.
- **api_export_missing_orders()** - Endpoint para exportar pedidos faltantes.

### Interacción con Base de Datos
El archivo interactúa con la base de datos SQLite a través de SQLAlchemy. Las tablas y columnas específicas no están detalladas, pero se pueden inferir desde los modelos Pydantic y las llamadas a ORM como `first()`, `query()`, `add()`, `delete()`.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno explícitas mencionadas en el código proporcionado.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `fastapi`
  - `pydantic`
  - `sqlalchemy_orm`
  - `core_auth`
  - `core_database`
  - `core_models`
  - `core_db_config_manager`
  - `core_app_instance`
  - `core_utils`
  - `core_state`
  - `core_query_engine`

- **Archivos Importados por este Archivo**:
  - No hay archivos importados directamente por este archivo.

- **Archivos que Importan a este Archivo**:
  - No hay archivos que importen directamente a este archivo.

- **Flujo de Datos**: 
  Los datos fluyen entre los endpoints y los modelos Pydantic, luego se procesan y persisten en la base de datos mediante SQLAlchemy.


---

## Archivo: ./graphify-out/cache/ast/4f9af946b1743e30eec64a351c630d05a8d09b09f18d70fea9fefd7957a923d5.json

### Resumen Funcional
El archivo `core/semantic_layer.py` contiene funciones y clases que definen la capa semántica del sistema de monitoreo de almacén (WMS). Esta capa se encarga de aislar el frontend del esquema físico, proporcionando una interfaz para obtener información sobre dimensiones, métricas y conjuntos de datos.

### Catálogo de Funciones y Clases
- `Dimension` - Representa una dimensión en el sistema.
- `Metric` - Representa una métrica en el sistema.
- `Dataset` - Representa un conjunto de datos en el sistema.
- `get_frontend_schema()` - Genera un diccionario semántico para exponer a la interfaz de usuario (UI).
- `resolve_dataset_physical_table(id)` - Devuelve la tabla física dado el ID del dataset.
- `resolve_physical_mapping(dim_area)` - Traduce un ID semántico a su columna física cualificada.
- `get_metric_formula(metric_id)` - Devuelve la fórmula compleja de una métrica si la tiene, inyectando la columna correspondiente.
- `get_formula_by_physical_table(table_name)` - Reverse-lookup: dado una tabla física y el nombre de una agregación compleja.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas SQL ni interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno quemadas en el código.

### Dependencias y Flujo
- **Dependencias**: Importa módulos `dataclasses` y `typing`.
- **Flujo de Datos**:
  - El archivo es importado por otros archivos (no se muestra aquí).
  - Se importa por `core/semantic_layer.py` desde los módulos `dataclasses` y `typing`.

Este archivo define la lógica semántica del sistema, proporcionando funciones para interactuar con dimensiones, métricas y conjuntos de datos, pero no realiza operaciones directas en una base de datos.


---

## Archivo: ./graphify-out/cache/ast/50bf0531bcf029b0fdca2f5044f64826d30fe1413fa37d63c7f98d186fb17959.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `deliveries.py` contiene la implementación de un repositorio para el dominio de Entregas (outbound_deliveries). Define métodos para obtener diferentes tipos de datos relacionados con las entregas, como umbrales SLA, auditorías SLA, entregas por lotes, áreas de entrega, elementos de recolección y gráficos de intensidad semanal.

### Catálogo de Funciones y Clases
- **DeliveriesRepository** - Repositorio para el dominio de Entregas.
  - `_sql()` - Obtiene SQL desde config_queries con fallback explícito.
  - `_get_sla_threshold()` - Obtiene el umbral SLA.
  - `get_sla_audit_records()` - Obtiene registros de auditoría SLA.
  - `get_deliveries_for_bulk()` - Obtiene entregas por lotes.
  - `get_area_lookup()` - Obtiene áreas de entrega.
  - `get_picking_items()` - Obtiene elementos de recolección.
  - `build_unified_where()` - Construye una cláusula WHERE unificada.
  - `get_filtered_transactions()` - Obtiene transacciones filtradas.
  - `get_filtered_kpis()` - Obtiene KPIs filtrados.
  - `get_delivery_by_id()` - Obtiene una entrega por su ID.
  - `get_weekly_intensity_chart()` - Obtiene el gráfico de intensidad semanal.
  - `get_dashboard_selectors()` - Obtiene selectores para el panel de control.

### Interacción con Base de Datos
- **Motor**: SQLite
- **TABLAS**:
  - No se especifican explícitamente las tablas, pero los métodos implican consultas a la base de datos.
- **COLUMNAS**:
  - No se especifican explícitamente las columnas, pero los métodos implican consultas a la base de datos.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno que almacenen estado crítico en este archivo.

### Dependencias y Flujo
- **Librerías Externas**:
  - `pandas`
  - `sqlalchemy`
  - `core_db_config_manager`
  - `users_christianykelly_desktop_monitorweb_repositories_base_py`
  - `core_macros`

- **Archivos del Proyecto que Importan a Este Archivo (lo consumen)**:
  - No se especifican explícitamente.

- **Flujo de Datos**:
  - El archivo importa varias librerías y dependencias necesarias para su funcionamiento.
  - Los métodos dentro de `DeliveriesRepository` realizan consultas a la base de datos utilizando SQLAlchemy, procesan los resultados con pandas y devuelven datos estructurados.


---

## Archivo: ./graphify-out/cache/ast/51c0d0497ae37e081bff0b6b5536227512cfebeffcd146d682d3558a59ec10c7.json

### Resumen Funcional
El archivo `tests/test_auth.py` contiene pruebas unitarias para el módulo de autenticación del sistema de monitoreo de almacén (WMS). Las pruebas cubren la funcionalidad de inicio de sesión, registro de usuarios y gestión de tokens JWT.

### Catálogo de Funciones y Clases
- `test_login_page_renders()` - Verifica que la página de login sea accesible.
- `test_login_success()` - Verifica login exitoso con credenciales del admin por defecto.
- `test_login_wrong_password()` - Verifica que credenciales incorrectas retornen 401.
- `test_me_endpoint_without_token()` - Verifica que `/me` sin token retorne 401.
- `test_me_endpoint_with_token()` - Verifica que `/me` con token válido retorne el perfil del usuario.
- `test_register_requires_admin()` - Verifica que registrar un usuario requiera token de admin.
- `test_register_and_login_new_user()` - Verifica el flujo completo: admin registra usuario → nuevo usuario hace login.
- `test_list_users_admin_only()` - Verifica que listar usuarios requiera rol admin.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: 
  - `pytest`
  - `fastapi_testclient`

- **Flujo de Datos**:
  - El archivo `tests/test_auth.py` importa `pytest` y `fastapi_testclient`.
  - Las funciones de prueba utilizan estos imports para realizar solicitudes HTTP a endpoints del sistema WMS.
  - No hay interacción directa con una base de datos en este archivo.


---

## Archivo: ./graphify-out/cache/ast/528131ed25a3e26cbf696584780a912857238297299edf194d464229f6254615.json

### Resumen Funcional
El archivo `main.py` es el punto de entrada oficial del sistema MonitorWeb Analyt. Configura e inicia los servicios de la plataforma.

### Catálogo de Funciones y Clases
- `start_application()` - Configura e inicia los servicios de la plataforma.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
**Librerías Externas:**
- `sys`
- `uvicorn`
- `logging`

**Archivos del Proyecto que Importan a este Archivo (`main.py`):**
- Ninguno

**Archivos del Proyecto que Este Archivo Importa (`main.py`):**
- `app`
- `config`
- `services_tunnel`

**Flujo de Datos:**
1. El archivo `main.py` importa las dependencias necesarias.
2. Llama a la función `start_application()`, que configura e inicia los servicios de la plataforma.
3. Utiliza métodos como `info`, `error`, `critical`, y `exit` para registrar información, errores y controlar el flujo del programa.

**Métodos Invocados:**
- `app.info(message)`
- `services_tunnel.start_tunnel()`
- `app.run()`
- `app.critical(message)`
- `app.exit()`
- `services_tunnel.stop_tunnel()`
- `app.error(message)`
- `app._exit()`


---

## Archivo: ./graphify-out/cache/ast/52d297b52b7fcb9c4fbf155602c2e074fd455e5d76ab62d4b336c6c656b28981.json

### Resumen Funcional
El archivo `inventory.py` contiene funciones relacionadas con el monitoreo de inventario en un sistema de gestión de almacenes (WMS). Define rutas y lógica para redirigir a las analíticas de inventario y obtener contexto de inventario.

### Catálogo de Funciones y Clases
- `analytics_inventory_redirect(request: Request, appstate: AppState)` - Redirige a las analíticas de inventario.
- `get_inventory_context(session: Session, item_id: str = None, context_type: Any = None)` - Obtiene el contexto del inventario para un ítem específico o todos los ítems.
- `analytics_inventory_api(session: Session, appstate: AppState)` - API JSON para analíticas de inventario.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
No se detectan variables globales o de sesión en el código proporcionado.

### Dependencias y Flujo
- **Librerías Externas**: `logging`, `sqlalchemy_orm`, `sqlalchemy`, `pandas`, `datetime`, `typing`, `fastapi`, `core_auth`, `fastapi_responses`, `core_database`, `core_schemas`, `core_state`, `core_wms_config`, `repositories`, `routes_analytics_proyecciones`, `core_utils`, `services_inventory_service`.
- **Archivos Importados**: El archivo importa varias clases y funciones de otros archivos dentro del proyecto.
- **Flujo de Datos**: El flujo de datos comienza en las rutas definidas, pasa por servicios y repositorios (si es necesario), y finalmente devuelve una respuesta al cliente.


---

## Archivo: ./graphify-out/cache/ast/54540c57687bae9117980cb18236f03ffd05937970c474132ebe2d03fe763092.json

### Resumen Funcional
El archivo `check_sla_queries.py` es un script que realiza consultas SLA (Service Level Agreement) en una base de datos SQLite.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna
- **Columnas**: Ninguna
- **Consultas SQL Crudas o Llamadas a ORM**: No hay consultas SQL crudas ni llamadas a ORM explícitas.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para procesar los resultados de las consultas en un formato tabular.
  - `json`: Para manejar el formato JSON.

- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno

**Flujo de Datos**: El script importa las bibliotecas necesarias y realiza consultas SLA en la base de datos SQLite, procesando los resultados con pandas y exportándolos en formato JSON.


---

## Archivo: ./graphify-out/cache/ast/54c706c5741a3b9d19d5418665fed07978bede460863afd005dbf2edd880b46b.json

### Resumen Funcional
El archivo `test_pdf.py` contiene pruebas unitarias para la generación de PDFs en un sistema de monitoreo de almacén (WMS). Las pruebas cubren la creación de instancias de PDF, la generación de códigos de barras y el dibujo de páginas de entrega.

### Catálogo de Funciones y Clases
- `pdf_instance()` - Crea una instancia de `WMS_Landscape_PDF`.
- `sample_header()` - Genera datos de cabecera de entrega ficticios.
- `sample_items()` - Genera un listado de materiales ficticios.
- `test_pdf_instantiation()` - Verifica que la clase PDF se instancie con la orientación Landscape y dimensiones correctas.
- `test_barcode_generation()` - Valida que la utilidad de códigos de barras produzca un stream binario válido.
- `test_get_ots_logic()` - Verifica la lógica de recuperación de OTs filtrando valores inválidos (0 o nulos).
- `test_draw_delivery_page_generates_content()` - Valida que el motor de dibujo escriba contenido binario en el buffer del PDF.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno quemadas en el código.

### Dependencias y Flujo
- **Dependencias Externas**: `pytest`, `pandas`, `io`, `sqlite3`, `typing`, `unittest_mock`, `core_pdf_engine`.
- **Archivos Importados por este Archivo**:
  - `tests/test_pdf.py` importa varios módulos y funciones.
- **Archivos que Importan a este Archivo**: No hay archivos que importen directamente a `test_pdf.py`.

El flujo de datos es principalmente entre las funciones de prueba y los métodos del objeto `WMS_Landscape_PDF`, así como la interacción con bibliotecas externas para generar PDFs y códigos de barras.


---

## Archivo: ./graphify-out/cache/ast/55169ca23a4786cca2c341a55744923258ccd63cada9f4477d1810e048705215.json

### Resumen Funcional
El archivo `check_areas.py` es un módulo que realiza operaciones relacionadas con el monitoreo de áreas en un sistema de almacén (WMS). Importa bibliotecas como `sqlite3` y `pandas` para interactuar con la base de datos y procesar los datos, respectivamente.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna (se supone que las operaciones se realizan a través de SQLAlchemy)
- Columnas: Ninguna (se supone que las operaciones se realizan a través de SQLAlchemy)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para procesar los datos.

- Archivos del proyecto que este archivo importa (consume): Ninguno
- Archivos del proyecto que importan a este archivo (lo consumen): Ninguno

El flujo de datos es directo, el módulo `check_areas.py` se encarga de realizar operaciones relacionadas con el monitoreo de áreas en el sistema de almacén.


---

## Archivo: ./graphify-out/cache/ast/56660310acc304b86472d8dd8bb0fbb599047df2c37ded7df1c612addb72d1f7.json

### Resumen Funcional
El archivo `test_lx02_pendientes.py` contiene una función de prueba que utiliza la biblioteca `pandas` para procesar un archivo Excel y extraer datos.

### Catálogo de Funciones y Clases
- `test_parse()` - Procesa un archivo Excel utilizando la clase `ExcelProcessor`.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: 
  - `sys`
  - `pandas`
  - `core_excel_processor` (importado como `ExcelProcessor`)
  
- **Flujo de Datos**:
  - El archivo importa las bibliotecas necesarias (`sys`, `pandas`, y `ExcelProcessor`).
  - La función `test_parse()` utiliza el método `process_file` de la clase `ExcelProcessor`.
  - Luego, se realizan operaciones como `tolist()`, `head()` en los datos procesados.


---

## Archivo: ./graphify-out/cache/ast/579446da8be16aaa260f86a2a3d843dc9368b5722f7414ce8393782e9ff62a44.json

### Resumen Funcional
El archivo `tunnel.py` contiene la implementación del servicio de túnel para el sistema de monitoreo de almacén (WMS). Este servicio permite iniciar y detener un túnel seguro y thread-safe.

### Catálogo de Funciones y Clases
- **NgrokService**
  - `__init__()`: Inicializa el servicio de túnel.
  - `_validate_bin()`: Valida la existencia y accesibilidad del binario del túnel.
  - `_save_url()`: Guarda la URL pública del túnel en un archivo.
  - `_get_public_url()`: Obtiene la URL pública del túnel desde una solicitud HTTP.
  - `start()`: Inicia el servicio de túnel de forma segura y thread-safe.
  - `stop()`: Detiene el servicio de túnel de forma segura y thread-safe.
  - `_run_loop()`: Ejecuta un bucle de ejecución para mantener el túnel activo.

- **start_tunnel()**: Función que inicia el servicio de túnel.
- **stop_tunnel()**: Función que detiene el servicio de túnel.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
**Librerías Externas:**
- `os`
- `subprocess`
- `threading`
- `time`
- `urllib.request`
- `json`
- `logging`

**Archivos del Proyecto que Importan a Este Archivo (lo consumen):**
Ninguno

**Este Archivo Importa a los siguientes Archivos del Proyecto:**
- `config`


---

## Archivo: ./graphify-out/cache/ast/5d34ccb8e2ec4e904045a3f6b9b0736b1497edf64f3e6550dc2de7016f75dd06.json

### Resumen Funcional
El archivo `check_schema.py` es un script que realiza operaciones relacionadas con la verificación del esquema de una base de datos SQLite.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna
- Columnas: Ninguna
- Consultas SQL Crudas o Llamadas a ORM: `import sqlite3`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías Externas: `sqlite3`
- Archivos del Proyecto que Importan a Este Archivo: Ninguno
- Archivos del Proyecto que Este Archivo Importa: Ninguno
- Dirección del Flujo de Datos: No aplica


---

## Archivo: ./graphify-out/cache/ast/5f2bf7aab62a6a6773f9e441fa2d333b037cc3c0941185a0ec3bed6ea28b7893.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `routes/filters.py` contiene funciones para filtrar transacciones y calcular KPIs en un sistema de monitoreo de almacén (WMS). Incluye endpoints para cargar datos asincrónicamente para el dashboard.

### Catálogo de Funciones y Clases
- `_build_unified_where()`
  - Propósito: Construye una cláusula WHERE unificada basada en múltiples criterios.
  
- `filter_transactions(request, session)`
  - Propósito: Filtra transacciones según los criterios proporcionados en la solicitud.

- `get_kpis(session)`
  - Propósito: Calcula KPIs dinámicos filtrados por área para el dashboard.

- `api_widget_data(request, session)`
  - Propósito: Endpoint de carga asincrónica para los componentes del Dashboard. Lee visual_s.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas y Columnas:
  - No se especifican columnas específicas en el fragmento proporcionado.
  
### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `logging`
  - `core_database`
  - `sqlalchemy_orm`
  - `sqlalchemy`
  - `datetime`
  - `typing`
  - `pandas`
  - `fastapi`
  - `config`
  - `core_models`
  - `core_query_engine`
  - `core_schemas`
  - `json`
  - `core_utils`
  - `repositories_deliveries`

- Archivos del proyecto que este archivo importa:
  - No se especifican archivos específicos en el fragmento proporcionado.

- Archivos del proyecto que importan a este archivo:
  - No se especifican archivos específicos en el fragmento proporcionado.


---

## Archivo: ./graphify-out/cache/ast/605433576c84cb4c894f851687548db973e1c020ee71f580177d67603ab99ceb.json

### Resumen Funcional
El archivo `inventory.py` contiene la implementación de un repositorio para el dominio de Movimientos de Inventario y Consumos. Define métodos para obtener consumos por centro de costo (`get_consumos_ceco`), materiales (`get_consumos_materiales`) y tendencias de material (`get_material_trend`). También incluye una verificación de la existencia de una tabla en la base de datos.

### Catálogo de Funciones y Clases
- `InventoryRepository()` - Repositorio para el dominio de Movimientos de Inventario y Consumos.
  - `.get_consumos_ceco(str centro_costo)` - Obtiene los consumos por centro de costo.
  - `.get_consumos_materiales(str material)` - Obtiene los consumos por material.
  - `.get_material_trend(str centro_costo, str material, str fecha_inicial, str fecha_final)` - Obtiene la tendencia de material.
  - `.check_table_exists()` - Verifica si una tabla existe en la base de datos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla `consumos`: Columnas (`id`, `centro_costo`, `material`, `fecha`, `cantidad`)
  - Tabla `materiales`: Columnas (`id`, `nombre`, `unidad_medida`, `stock_actual`)
  - Tabla `tendencias_material`: Columnas (`id`, `centro_costo`, `material`, `fecha`, `valor_trend`)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Dependencias Externas:**
  - `logging`
  - `pandas`
  - `sqlalchemy`
  - `datetime`

- **Archivos del Proyecto que Importan a Este Archivo (`inventory.py`):**
  - No hay dependencias directas.

- **Archivos del Proyecto que Este Archivo Importa:**
  - `base.py` (por lo menos, se importa en la definición de `InventoryRepository`)

- **Flujo de Datos:**
  - El archivo consume métodos y clases de SQLAlchemy para interactuar con la base de datos.
  - Utiliza pandas para procesar los resultados de las consultas SQL.
  - Los métodos devuelven datos procesados en formato de diccionario o lista.


---

## Archivo: ./graphify-out/cache/ast/606acc60977a4956c3b5059eac1d26eb0f46a1e367b4bef1a82a66dc1bab497c.json

### Resumen Funcional
El archivo `test_utils.py` contiene una función de prueba que verifica la seguridad e idempotencia del registro de manejadores de señales.

### Catálogo de Funciones y Clases
- `test_setup_signal_handlers_safety()` - Verifica que el registro de manejadores de señales sea seguro e idempotente.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: `pytest`, `core_utils`
- **Archivos Importados por este Archivo**: Ninguno
- **Archivos que Importan a este Archivo**: Ninguno
- **Flujo de Datos**: La función `test_setup_signal_handlers_safety()` llama al método `setup_signal_handlers` dos veces.

**Nota**: El archivo no interactúa con una base de datos ni utiliza variables globales.


---

## Archivo: ./graphify-out/cache/ast/6364b852f5601c620944dbdcb1a827fd2142e6c1d67b5808c8e721c459db32bb.json

### Resumen Funcional
El archivo `test_keys.py` es un módulo que importa bibliotecas necesarias para el sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite.

### Catálogo de Funciones y Clases
- Ninguna función o clase detectada directamente en este archivo.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna. El archivo no interactúa explícitamente con la base de datos a través de consultas SQL crudas o ORM.

### Estado y Variables Globales
- Ninguna variable global, de sesión, de entorno o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- **Librerías Externas**: `sqlite3`
- **Archivos del Proyecto que IMPORTA (consume)**: 
  - `routes_analytics_mb51`
  - `config`
- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno.
- **Dirección del Flujo de Datos**: El archivo `test_keys.py` importa bibliotecas y otros módulos, pero no realiza ninguna operación específica en la base de datos ni consume datos de otros archivos.


---

## Archivo: ./graphify-out/cache/ast/64976c195d2e4e4d9c04ae23fe4289d12f70e28e3e925bb3e8d719416d2fdac6.json

### Resumen Funcional
El archivo `compare_queries.py` contiene código que realiza comparaciones entre consultas SQL utilizando la biblioteca `sqlite3` para interactuar con una base de datos SQLite y la biblioteca `pandas` para manejar los resultados.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (se supone que las consultas son generadas dinámicamente)
- **Columnas**: Ninguna (se supone que las consultas son generadas dinámicamente)

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para manejar los resultados de las consultas SQL.

- **Archivos del Proyecto que Importan a Este Archivo**: Ninguno

- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno

- **Flujo de Datos**: El archivo importa `sqlite3` y `pandas`, realiza consultas SQL utilizando `sqlite3`, procesa los resultados con `pandas`, y no hay interacción directa con otros archivos del proyecto.


---

## Archivo: ./graphify-out/cache/ast/64d1f35fd94b79e06e1bbd905e2a0d47acc58f72b14287bd18394813e7d43721.json

### Resumen Funcional
El archivo `dynamic_executor.py` contiene una función que ejecuta consultas visuales a partir de un payload JSON crudo, valida y compila dicha consulta utilizando el motor SQLAlchemy.

### Catálogo de Funciones y Clases
- `execute_visual_query(session: Session) -> DataFrame` - Toma un payload JSON crudo desde el frontend, lo valida y compila usando el motor SQLAlchemy para ejecutar una consulta visual.

### Interacción con Base de Datos
- **Motor:** SQLite (implícito en la importación de SQLAlchemy).
- **Tablas y Columnas:** No se especifican explícitamente las tablas o columnas modificadas.
- **Consultas SQL Crudas:** La función `read_sql` es llamada, lo que implica que hay consultas SQL crudas.
- **ORM:** Se usa el ORM SQLAlchemy para la ejecución de consultas.

### Estado y Variables Globales
- Ninguna variable global o diccionario quemado en código que almacene estado crítico.

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `logging`
  - `typing`
  - `sqlalchemy.orm`
  - `core_query_engine`
  - `core_schemas`

- **Archivos del Proyecto que Importan a Este Archivo (lo consumen):** Ninguno.
- **Archivos del Proyecto que Este Archivo Importa (consume):**
  - `VisualQueryBuilderPayload` de `core_query_engine`
  - `build_sql_from_payload` de `core_query_engine`
  - `read_sql` y `connection` de `sqlalchemy.orm`

El flujo de datos es desde el frontend hacia este archivo, donde se recibe un payload JSON crudo, se valida y compila para ejecutar una consulta visual en la base de datos SQLite.


---

## Archivo: ./graphify-out/cache/ast/679e58595c2d5b0368fa9fcbe14b83d2400a592c09610b04a5d21a79fb43213a.json

### Resumen Funcional
El archivo `test_db_url.py` contiene una importación de la biblioteca `sqlalchemy`. No se proporciona ninguna otra información funcional.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: `sqlalchemy`
- **Flujo de datos**: El archivo importa la biblioteca `sqlalchemy` y no realiza ninguna otra operación relevante.


---

## Archivo: ./graphify-out/cache/ast/67c2b5bc142c856b40958f77b59dfb9d860d64db5c46a8c8aadf19f178bf8c18.json

### Resumen Funcional
El archivo `docs.py` contiene dos funciones principales: `get_docs_tree()` y `get_doc_content()`. La primera genera un árbol de archivos del proyecto indicando cuáles tienen documentación, mientras que la segunda obtiene el contenido de la documentación (.md) para un archivo específico.

### Catálogo de Funciones y Clases
- **`get_docs_tree(appstate: AppState)`** - Genera un árbol de archivos del proyecto indicando cuáles tienen documentación.
- **`get_doc_content(file_path: str, appstate: AppState)`** - Obtiene el contenido de la documentación (.md) para un archivo específico.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- **`appstate`** - Variable global que almacena el estado del sistema.

### Dependencias y Flujo
- **Dependencias Externas**: `os`, `fastapi`, `fastapi_responses`, `config`, `core_state`.
- **Archivos Importados por este Archivo**: Ninguno.
- **Archivos que Importan a este Archivo**: Ninguno.
- **Flujo de Datos**: El archivo importa varias bibliotecas y dependencias necesarias para su funcionamiento. La función `get_docs_tree` genera un árbol de archivos, mientras que la función `get_doc_content` lee el contenido de los archivos de documentación.

Este archivo es parte del módulo de rutas (`routes/docs.py`) en el sistema de monitoreo de almacén (WMS), y se utiliza para proporcionar endpoints para obtener información sobre la documentación del proyecto.


---

## Archivo: ./graphify-out/cache/ast/69d3b53515294f506e35991669de1dbbeb693294f1cff51d8694f65c2156c958.json

### Resumen Funcional
El archivo `check_all_columns.py` es un script que realiza operaciones relacionadas con la base de datos SQLite utilizando las bibliotecas `sqlite3` y `pandas`. Es probablemente parte del proceso de monitoreo de almacén (WMS) para verificar o manipular columnas en una tabla específica.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna especificada directamente
- **Columnas**: Ninguna especificada directamente
- **Consultas SQL Crudas o Llamadas a ORM**: No hay consultas SQL crudas ni llamadas a ORM explícitas en el fragmento proporcionado.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para manipular y analizar los datos obtenidos desde la base de datos.

- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno

- **Flujo de Datos**: El script importa las bibliotecas necesarias (`sqlite3` y `pandas`) y realiza operaciones relacionadas con la base de datos SQLite.


---

## Archivo: ./graphify-out/cache/ast/6d421f8f6df3e24a5c3ac5edc8b82c930b7691a09141da7d8b7970db44e636c0.json

### Resumen Funcional
El archivo `update_delivery_kpis.py` contiene código que realiza operaciones relacionadas con la actualización de indicadores clave del desempeño (KPIs) en el sistema de monitoreo de almacén.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite3
- **Tablas**: Ninguna
- **Columnas**: Ninguna
- **Consultas SQL Crudas o Llamadas a ORM**: No hay consultas SQL crudas ni llamadas a ORM explícitas.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Importada para interactuar con la base de datos SQLite.
  - `json`: Importada para manejar operaciones JSON.

- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno

- **Flujo de Datos**: El archivo importa las bibliotecas necesarias y no realiza ninguna interacción con la base de datos ni utiliza variables globales.


---

## Archivo: ./graphify-out/cache/ast/6dfcee190fc10c7da27c737a07a3f32ce1808c761b59957099ffb5047771d609.json (Procesado en 1 partes)


---

## Archivo: ./graphify-out/cache/ast/6e0e4b95bfba32918c0d480d8eeb265ad44cedcb8792ba390c8cfc9f828c87dd.json

### Resumen Funcional
El archivo `routes/productivity.py` contiene funciones que manejan diferentes aspectos del monitoreo de productividad en el sistema WMS. Estas funciones interactúan con servicios y repositorios para obtener datos y devolver respuestas al cliente.

### Catálogo de Funciones y Clases
- **get_available_dates()** - Retorna las fechas disponibles para el dashboard de productividad.
- **get_productivity_dashboard()** - Retorna los datos necesarios para el dashboard de productividad MB51.
- **get_monthly_productivity()** - Retorna los KPIs mensuales de productividad.
- **get_user_movements_summary()** - Retorna un resumen de movimientos del usuario.
- **get_user_movements_details()** - Retorna los detalles de los movimientos del usuario.
- **get_user_movements_monthly_summary()** - Retorna un resumen mensual de los movimientos del usuario.
- **get_user_movements_monthly_details()** - Retorna los detalles mensuales de los movimientos del usuario.

### Interacción con Base de Datos
No se especifican consultas SQL crudas o llamadas a ORM en este archivo. La interacción con la base de datos ocurre a través de servicios (`ProductivityDailyService` y `ProductivityMonthlyService`) que probablemente interactúen con los repositorios para acceder a los datos.

### Estado y Variables Globales
No se detectan variables globales, de sesión o de entorno en este archivo. Todas las referencias a estado crítico son parámetros de funciones.

### Dependencias y Flujo
- **Dependencias**: El archivo importa varias bibliotecas como `fastapi`, `sqlalchemy_orm`, `datetime`, entre otras, además de módulos internos del proyecto como `services_productivity_daily`, `services_productivity_monthly`, etc.
- **Flujo de Datos**: Los datos fluyen desde las funciones hacia los servicios y luego a través de estos hacia la base de datos. Las respuestas generadas por los servicios son devueltas al cliente a través de las funciones correspondientes.

Este archivo es una parte integral del sistema WMS, encargado de proporcionar endpoints para obtener diferentes tipos de datos relacionados con el monitoreo de productividad.


---

## Archivo: ./graphify-out/cache/ast/6f2a1f48352150b25fb5208ea7642620e72a91650ae759141dd1d53c645967ce.json

### Resumen Funcional
El archivo `tasks_service.py` contiene la lógica de negocio para el servicio de tareas en un sistema de monitoreo de almacén (WMS). Define una clase `TasksService` que proporciona métodos para obtener contexto analítico y resúmenes de tareas.

### Catálogo de Funciones y Clases
- **Clase:** `TasksService`
  - **Método:** `__init__(self, session: Session)`
    - **Propósito:** Inicializa una instancia de la clase con una sesión de base de datos.
  - **Método:** `get_full_context(self)`
    - **Propósito:** Genera y cachea el contexto analítico para la gestión de OTs.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - No se especifican columnas específicas, pero se hacen llamadas a métodos que implican consultas SQL (como `read_sql`, `execute`, `fetchone`).

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `sqlalchemy`
  - `pandas`
  - `logging`
  - `datetime`
  - `core_state`
  - `core_utils`
- **Archivos del Proyecto que Importan a Este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:**
  - `repositories`
  - `services_tasks_service_tasksservice`

El flujo de datos fluye desde la clase `TasksService` hacia los métodos y clases importadas, realizando operaciones como consultas a la base de datos, manipulación de datos con pandas, y registro de eventos con logging.


---

## Archivo: ./graphify-out/cache/ast/7c1b07c1b5126af3d9afe045d2ae833f779037728df9b890cd6f9b25e5f309d3.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `pdf_engine.py` contiene una clase base para reportes WMS en formato horizontal (`WMS_Landscape_PDF`) que genera PDFs utilizando la biblioteca FPDF. La clase incluye métodos para calcular posiciones de columnas, dibujar líneas punteadas, obtener OTs asociadas a entregas, generar códigos de barras y dibujar páginas de entrega con encabezados, bloques de información y tablas.

### Catálogo de Funciones y Clases
- **WMS_Landscape_PDF** - Clase base para reportes WMS en formato horizontal.
  - `__init__()`
  - `get_column_x(column: int) -> float` - Calcula la posición X de una columna específica.
  - `draw_dotted_line(x1: float, y1: float, x2: float, y2: float)`
  - `_generate_barcode_stream(barcode_data: str) -> bytesio.BytesIO`
  - `draw_delivery_page(delivery_info: pandas.Series, items_df: pandas.DataFrame, is_printed: bool, delivery_id: str)`
  - `_draw_page_header(delivery_info: pandas.Series, is_printed: bool)`
  - `_draw_info_block(delivery_info: pandas.Series)`
  - `_draw_table(items_df: pandas.DataFrame)`
  - `_draw_ot_barcodes(ots_list: list)`
  - `_draw_signature_block()`

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas y Columnas**:
  - `get_ots_for_delivery(delivery_id: str, connection: sqlite3.Connection) -> list[str]` - Consulta las OTs asociadas a una entrega y las devuelve como lista de strings.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `io`
  - `logging`
  - `sqlite3`
  - `datetime`
  - `typing`
  - `pathlib`
  - `numpy`
  - `pandas`
  - `fpdf`
  - `barcode`
  - `barcode_writer`
  - `config`

- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno


---

## Archivo: ./graphify-out/cache/ast/7c24e25851b398265dcba13704cc879b0317b685504e0376e17857c68897014b.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `db_enrichment.py` contiene funciones que realizan el enriquecimiento de datos en una base de datos SQLite. Estas funciones incluyen la rellena de columnas vacías en Entregas, el aprendizaje del mapeo de frecuencia Autor -> Área, la asignación de áreas de negocio a transacciones 'OTRO', y la enriquecimiento de transacciones con descripciones y ubicaciones físicas de Stock.

### Catálogo de Funciones y Clases
- `backfill_deliveries_from_movements(connection: str)`: Rellena columnas vacías en Entregas cruzando con Movi.
- `learn_author_areas(connection: str)`: Actualiza el mapeo de frecuencia Autor -> Área.
- `apply_author_learning(connection: str)`: Asigna áreas de negocio a transacciones 'OTRO' basadas en la memoria del autor.
- `enrich_deliveries_with_stock(connection: str)`: Enriquece transacciones con descripciones y ubicaciones físicas de Stock.
- `backfill_material_texts(connection: str)`: Rellena descripciones y UMBs faltantes en Entregas usando Stock y Movimientos coincidentes.
- `update_sla_with_tasks(connection: str)`: Actualiza la métrica de SLA en outbound_deliveries cruzando con la fecha de confirmación de tareas.
- `enrich_movements_with_iw39(connection: str)`: Enriquece la tabla inventory_movements con ceco_resp y autor provenientes de iw39.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQLite. Las tablas y columnas específicas no están detalladas en el fragmento proporcionado, pero se infiere que las funciones manipulan varias tablas relacionadas con entregas, movimientos, materiales y SLA.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno explícitamente mencionadas en el fragmento proporcionado.

### Dependencias y Flujo
- **Dependencias**: El archivo importa módulos como `logging`, `pandas`, `sqlite3` y `typing`.
- **Flujo de Datos**: El flujo de datos fluye desde las funciones hacia la base de datos, realizando operaciones de lectura (`read_sql`), escritura (`to_sql`) y actualización (`execute`). Las funciones también utilizan métodos de pandas para manipular los datos en memoria antes de escribirlos a la base de datos.


---

## Archivo: ./graphify-out/cache/ast/7d29a7d52d8c76e8bde35a684b01606b4d7d06822471efe988accc1694bc168a.json

### Resumen Funcional
Este archivo `database.py` contiene la configuración y funcionalidades relacionadas con la base de datos para el sistema de monitoreo de almacén (WMS). Define una clase base para los modelos ORM, funciones para obtener sesiones de base de datos y verificar su conectividad.

### Catálogo de Funciones y Clases
- `Base` - Clase base para todos los modelos ORM del sistema.
- `get_session()` - Context manager que entrega una sesión SQLAlchemy. Garantiza commit en éxito o rollback en fallo.
- `get_session_dep()` - Dependencia de FastAPI (Depends) para inyección de sesiones en endpoints.
- `health_check()` - Verifica la conectividad con la base de datos. Retorna True si OK.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: No especificadas explícitamente en el fragmento, pero se asume que interactúa con tablas definidas en los modelos ORM heredados de `Base`.
- Consultas SQL Crudas o Llamadas a ORM:
  - `SessionLocal`
  - `commit`, `rollback`, `close` (métodos de la sesión SQLAlchemy)
  - `connect`, `execute`, `text` (métodos del motor de base de datos)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Importa módulos como `os`, `logging`, `contextlib`, `typing`, `sqlalchemy`, `sqlalchemy_orm`, y `config`.
- Es importado por otros archivos del proyecto.
- Importa a otros archivos del proyecto (`core/database.py`).

Flujo de datos:
1. `database.py` se importa en otros archivos.
2. Se utilizan las funciones y clases definidas aquí para gestionar sesiones de base de datos y verificar conectividad.

Este archivo es fundamental para la capa de acceso a datos del sistema WMS, proporcionando una interfaz consistente para interactuar con la base de datos utilizando SQLAlchemy ORM.


---

## Archivo: ./graphify-out/cache/ast/80bfa4e4aa3f17049ec4ee2bcb50e1357fffb19d641addd30d60b5391501dc7e.json

### Resumen Funcional
El archivo `utils.py` contiene funciones utilitarias transversales y gestiòn de señales del sistema.

### Catálogo de Funciones y Clases
- `setup_signal_handlers()` - Configura los manejadores de señales (SIGINT, SIGTERM) para un cierre limpio.
- `log_startup_banner()` - Limpia datos para serialización JSON segura de forma recursiva y exhaustiva.
- `_get_bound_params_from_visual_state(state: str)` - Alias de compatibilidad → core/query_engine.get_bound_params_from_visual_state.
- `_extract_metric_value(metric_name: str)` - Alias de compatibilidad → core/query_engine.extract_metric_value.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: `signal`, `sys`, `logging`, `pandas`, `math`, `typing`
- **Archivos Importados por Este Archivo**:
  - No aplica.
- **Archivos que Importan a Este Archivo**:
  - No aplica.


---

## Archivo: ./graphify-out/cache/ast/82920e8133c919d6df598a58e34c44803ba5a97e6e3451d30140393c627f67cb.json

### Resumen Funcional
El archivo `check_months.py` es un script que realiza operaciones relacionadas con los meses, probablemente para el monitoreo de almacén (WMS). No contiene ninguna interacción explícita con la base de datos.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada en este fragmento.

### Interacción con Base de Datos
Ninguna. El archivo no realiza ninguna operación relacionada con la base de datos.

### Estado y Variables Globales
Ninguna variable global, de sesión o de entorno detectada en este fragmento.

### Dependencias y Flujo
- **Librerías externas**: `sqlite3`, `pandas`
- **Archivos del proyecto que IMPORTAN a este archivo**: Ninguno.
- **Archivos del proyecto que este archivo IMPORTA**: Ninguno.
- **Dirección del flujo de datos**: No aplica, ya que no hay funciones ni interacciones con la base de datos.


---

## Archivo: ./graphify-out/cache/ast/878b63f8b93c007822c5a2e02560fcef0eb1964373ab0ecef269bacc46a32916.json

### Resumen Funcional
El archivo `check_specific_deliveries.py` es un script que realiza operaciones relacionadas con el monitoreo de entregas en un sistema de almacén (WMS). Importa módulos para interactuar con una base de datos SQLite y pandas para manejar los datos.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna especificada
- **Columnas**: Ninguna especificada
- **Consultas SQL Crudas o Llamadas a ORM**: Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para manejar los datos.

- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno

- **Dirección del Flujo de Datos**:
  - El script importa las bibliotecas necesarias (`sqlite3` y `pandas`) para su ejecución.


---

## Archivo: ./graphify-out/cache/ast/8c8245b9595242aafc411b8d79cf57ce89c705230a7d38f0636a18ca562078d3.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `db_config_manager.py` es el administrador de configuraciones dinámicas SaaS. Crea las tablas de configuración SaaS via SQLAlchemy si no existen, inserta los valores por defecto si las tablas están vacías y proporciona métodos para recuperar configuraciones específicas.

### Catálogo de Funciones y Clases
- `init_config_db()` - Crea las tablas de configuración SaaS via SQLAlchemy si no existen.
- `seed_initial_config()` - Inserta los valores por defecto si las tablas están vacías.
- `load_config_to_memory()` - Carga la configuración a memoria.
- `_ensure_loaded()` - Método auxiliar para asegurar que la configuración esté cargada.
- `get_setting(setting_name: str) -> Any` - Recupera un valor de configuración específico.
- `get_status_mapping() -> Dict[str, str]` - Obtiene el mapeo de estados.
- `get_cost_center_mapping() -> Dict[str, str]` - Obtiene el mapeo de centros de costo.
- `get_holidays() -> List[Holiday]` - Obtiene los días festivos.
- `get_query_visual_state(query_id: str) -> str` - Recupera el visual_state JSON de una query.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `StatusMapping`
  - `CostCenterMapping`
  - `AppSetting`
  - `Holiday`
  - `ConfigQuery`
- Columnas (ejemplos):
  - `StatusMapping.id`, `StatusMapping.status_code`, `StatusMapping.description`
  - `CostCenterMapping.id`, `CostCenterMapping.cost_center_id`, `CostCenterMapping.description`
  - `AppSetting.id`, `AppSetting.setting_name`, `AppSetting.value`
  - `Holiday.id`, `Holiday.date`, `Holiday.description`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- Importa módulos como `logging`, `typing`, `sqlalchemy`, `sqlalchemy_orm`.
- Importa clases de otros archivos (`core/database.py`, `core/models.py`).
- Llama a métodos de ORM SQLAlchemy para interactuar con la base de datos.
- El flujo de datos fluye desde las funciones hacia el acceso a la base de datos y viceversa.


---

## Archivo: ./graphify-out/cache/ast/8e72c3a774307053c0b3e684d686c4ffa3e35ec2829bda3808d54e73f4ae237b.json

### Resumen Funcional
El archivo `analyze_html.py` contiene una función que analiza grandes archivos HTML utilizando la biblioteca `httpx` para hacer solicitudes HTTP y la biblioteca `re` para realizar búsquedas regulares.

### Catálogo de Funciones y Clases
- **analyze_large_html()** - Analiza grandes archivos HTML.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: `asyncio`, `httpx`, `sys`, `os`, `re`.
- **Archivos Importados por Este Archivo**:
  - Ninguno.
- **Archivos que Importan a Este Archivo**:
  - Ninguno.

El flujo de datos es simple: el archivo importa las bibliotecas necesarias y luego define la función `analyze_large_html()`, que realiza operaciones como hacer solicitudes HTTP, buscar patrones regulares en HTML y manipular listas.


---

## Archivo: ./graphify-out/cache/ast/8ee89e2bc21b701c250548368014f8ee524164b6d75123d28e1b343765391765.json

### Resumen Funcional
El archivo `test_preview_api.py` contiene pruebas unitarias para el sistema de monitoreo de almacén (WMS) utilizando FastAPI y SQLAlchemy.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `sys`, `json`
- **Archivos Importados por Este Archivo**:
  - `fastapi_testclient` (desde `main`)
- **Archivos que Importan a Este Archivo**: Ninguno

El archivo `test_preview_api.py` importa módulos necesarios para ejecutar pruebas unitarias en el sistema WMS, pero no realiza ninguna interacción con la base de datos ni utiliza variables globales.


---

## Archivo: ./graphify-out/cache/ast/9099043b37b2cb80a4ed1c0a1592141cf95c6ce604f6cb220061cf4ef93ec8db.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `routes/deliveries.py` contiene funciones relacionadas con el manejo de entregas en un sistema de monitoreo de almacén (WMS). Incluye rutas para guardar y cargar capturas de análisis, renderizar páginas de análisis, obtener detalles de auditoría SLA y proporcionar una API JSON para analíticas de entregas.

### Catálogo de Funciones y Clases
- `save_analytics_snapshot(session: Session, data: str) -> None`: Guarda una captura de las analíticas en la base de datos.
- `load_analytics_snapshot(session: Session, snapshot_id: str) -> Any`: Recupera la última captura de analíticas desde la base de datos.
- `analytics(request: Request, session: Session, appstate: AppState) -> TemplateResponse`: Renderiza la página principal de analíticas con caché multinivel (Memoria -> DB).
- `sla_details(request: Request, session: Session, year: str, month: str, day: str) -> TemplateResponse`: Vista detallada de auditoría SLA.
- `get_non_palletized_details(session: Session, warehouse_id: str) -> Any`: Obtiene el listado detallado (hasta 200) de movimientos no paletizados para un almacén específico.
- `analytics_deliveries_api(session: Session, appstate: AppState) -> AnalyticsDeliveriesResponse`: API JSON para analíticas de Entregas (Outbound Deliveries).

### Interacción con Base de Datos
- **Motor**: SQLite
- **TABLAS**:
  - No se especifican tablas explícitas en el código proporcionado.
- **COLUMNAS**:
  - No se especifican columnas explícitas en el código proporcionado.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `logging`, `sqlite3`, `pandas`, `json`, `datetime`, `typing`, `sqlalchemy`, `fastapi`, `fastapi_responses`
- **Archivos del Proyecto que Importan a este Archivo**:
  - No se especifican archivos que importen a este archivo.
- **Archivos del Proyecto que Este Archivo Importa**:
  - `core_database`
  - `sqlalchemy_orm`
  - `core_state`
  - `core_app_instance`
  - `core_schemas`
  - `repositories`
  - `routes_inventory`
  - `routes_tasks`
  - `routes_analytics_proyecciones`
  - `core_auth`
  - `core_utils`
  - `services_deliveries_service`
- **Flujo de Datos**: El archivo importa varias bibliotecas y módulos del proyecto, incluyendo servicios y repositorios para interactuar con la base de datos y lógica de negocio. Las funciones realizan operaciones como guardar y cargar capturas de análisis, renderizar páginas web y proporcionar APIs JSON.

Este archivo es crucial para el manejo de analíticas y detalles de entregas en el sistema WMS, utilizando una arquitectura basada en servicios y repositorios para mantener la separación de preocupaciones.


---

## Archivo: ./graphify-out/cache/ast/91f75411b1f3fc186d09119761d6cc0975acdde32a9ee05b709cb2b680b3f273.json

### Resumen Funcional
Clase base para todos los repositorios de datos en el sistema de monitoreo de almacén (WMS). Proporciona métodos para interactuar con la base de datos y verificar el estado visual de las consultas.

### Catálogo de Funciones y Clases
- `BaseRepository(session: Session)` - Constructor que recibe una sesión de SQLAlchemy.
- `._sql(sql_text: str) -> str` - Método privado que devuelve el texto SQL proporcionado como parámetro.
- `._has_visual_state(query: str) -> bool` - Método privado que verifica si la consulta tiene un estado visual JSON almacenado.

### Interacción con Base de Datos
- Motor de BD: SQLite (implícito en SQLAlchemy).
- Tablas y Columnas: No especificadas explícitamente.
- Consultas SQL Crudas: Sí, se utiliza el parámetro `sql_text` en el método `_sql`.
- ORM: Sí, se usa la sesión de SQLAlchemy (`Session`) para interactuar con la base de datos.

### Estado y Variables Globales
- No hay variables globales o de sesión definidas explícitamente.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `sqlalchemy_orm` (importado desde `repositories/base.py`)
  - `core_db_config_manager` (importado desde `repositories/base.py`)
- **Flujo de Datos**:
  - El archivo `base.py` importa dependencias necesarias y define la clase `BaseRepository`.
  - La clase `BaseRepository` contiene métodos para interactuar con la base de datos.
  - El método `_sql` recibe un texto SQL como parámetro y lo devuelve.
  - El método `_has_visual_state` verifica si una consulta tiene un estado visual JSON almacenado.

### Rationale
- Clase base para todos los repositorios de datos.
- Devuelve el fallback hardcodeado. (Fase 4 completada: sql_text ha sido eliminado).
- Retorna True si la query tiene un visual_state JSON almacenado.


---

## Archivo: ./graphify-out/cache/ast/9224144950785d5e538d3808d62b08a9f059284c033c2cfd955413c9ff65a564.json

### Resumen Funcional
El archivo `test_pipeline.py` contiene pruebas unitarias para el módulo de consolidación de datos en un sistema de monitoreo de almacén (WMS). Las pruebas cubren la funcionalidad de análisis de fechas, validación de seguridad de tablas y lógica de sobrescritura con los archivos más recientes.

### Catálogo de Funciones y Clases
- `consolidator()` - No se proporciona una descripción detallada.
- `test_parse_file_date()` - Verifica que el parsing de fechas sea correcto.
- `test_validate_table_security()` - Verifica la protección contra nombres de tabla no permitidos.
- `test_overwrite_with_latest_logic()` - Verifica que se tome el archivo más reciente para sobrescribir.

### Interacción con Base de Datos
No hay consultas SQL crudas o llamadas a ORM explícitas en este archivo. La interacción con la base de datos ocurre dentro del método `test_overwrite_with_latest_logic()`, donde se utiliza SQLAlchemy para ejecutar consultas y obtener resultados.

- **TABLAS**: Ninguna específica mencionada.
- **COLUMNAS**: Ninguna específica mencionada.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno que almacenen estado crítico en este archivo.

### Dependencias y Flujo
- **Librerías Externas**:
  - `pytest`
  - `pathlib`
  - `datetime`
  - `pandas`
  - `db_consolidator`

- **Archivos del Proyecto que IMPORTAN a Este Archivo**: Ninguno.
- **Archivos del Proyecto que ESTE ARCHIVO IMPORTA**: Ninguno.

**Flujo de Datos**: El archivo importa varias bibliotecas y módulos, incluyendo `pytest` para pruebas unitarias, `pathlib` para manejo de rutas de archivos, `datetime` para operaciones con fechas, `pandas` para manipulación de datos tabulares, y `db_consolidator` para la lógica de consolidación de datos. Las funciones de prueba utilizan estos módulos para realizar sus respectivas tareas de análisis, validación y sobrescritura de datos.


---

## Archivo: ./graphify-out/cache/ast/92831e8dc24ad42b677abae249e3eadd21d6a1a31e22e210b750e340c3314a08.json

### Resumen Funcional
El archivo `package.json` del proyecto de WMS contiene la configuración y dependencias necesarias para el desarrollo y ejecución del sistema.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: `puppeteer`
- **Flujo de datos**: El archivo `package.json` importa la dependencia `puppeteer`.


---

## Archivo: ./graphify-out/cache/ast/92b6fc5c26b266056ec4bb1504831d2d8ae4387779cca708b63e376bfbbfabc7.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `tasks.py` contiene la implementación de un repositorio para el dominio de Warehouse Tasks e interacciones de usuario. Define métodos para obtener resúmenes diarios, horarios, inactividades, mapas térmicos y movimientos de usuarios.

### Catálogo de Funciones y Clases
- **TasksRepository** - Repositorio que hereda de `BaseRepository` y contiene métodos para interactuar con la base de datos.
  - `.get_available_dates()`
  - `_get_daily_summary()`
  - `_get_hourly_trend()`
  - `_get_inactivity_gaps()`
  - `_get_activity_heatmap()`
  - `.get_user_movements_daily_summary()`
  - `.get_user_movements_daily_details()`
  - `_get_monthly_summary()`
  - `_get_monthly_shifts()`
  - `_get_monthly_heatmap()`
  - `.get_user_movements_monthly_summary()`
  - `.get_user_movements_monthly_details()`
  - `.get_tasks_summary()`
  - `.get_tasks_trend()`
  - `.get_tasks_by_user()`
  - `.get_tasks_by_type_dest()`
  - `.get_recent_tasks()`
  - `.get_non_palletized_movements()`
  - `.get_non_palletized_count()`
  - `.get_non_palletized_summary()`

### Interacción con Base de Datos
- **Motor**: SQLite
- **TABLAS**:
  - No se especifican explícitamente las tablas, pero los métodos interactúan con la base de datos para obtener y manipular datos.
- **COLUMNAS**:
  - No se especifican explícitamente las columnas, pero los métodos utilizan consultas SQL que implican varias columnas.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno mencionadas en el código proporcionado.

### Dependencias y Flujo
- **Librerías Externas**:
  - `logging`
  - `pandas`
  - `sqlalchemy`
- **Archivos del Proyecto que Importan a Este Archivo (lo consumen)**:
  - No se especifican archivos que importen directamente este archivo.
- **Flujo de Datos**: El flujo de datos fluye desde los métodos del repositorio hacia la base de datos para leer y escribir datos, y luego hacia el servicio o controlador que lo consume.


---

## Archivo: ./graphify-out/cache/ast/9742e8f505e0c6e7a22bee3c481e6f2e2b8bf062a4d24b2f148900af3ef72162.json

### Resumen Funcional
El archivo `check_query.py` es un script que realiza consultas a una base de datos SQLite y procesa los resultados utilizando la biblioteca pandas.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (se supone que las tablas se especifican en el código no proporcionado)
- **Columnas**: Ninguna (se supone que las columnas se especifican en el código no proporcionado)

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para procesar los resultados de las consultas.
  - `sys` y `os`: Para operaciones del sistema y manejo de archivos, respectivamente.
- **Archivos Importados por Este Archivo**:
  - Ninguno
- **Archivos que Importan a Este Archivo**:
  - Ninguno

El flujo de datos es simple: el script importa las bibliotecas necesarias, realiza consultas a la base de datos SQLite utilizando `sqlite3`, procesa los resultados con pandas, y no interactúa directamente con otros archivos o servicios dentro del proyecto.


---

## Archivo: ./graphify-out/cache/ast/9799d9fa4c3ad9179fe69a77d84f0f273a805fc4cec4422fecc5f41d59145002.json

### Resumen Funcional
El archivo `config.py` contiene funciones para validar la configuración del sistema y asegurar la estructura del proyecto.

### Catálogo de Funciones y Clases
- `validate_config()` - Realiza comprobaciones de salud en la configuración.
- `ensure_project_structure()` - Crea los directorios necesarios para el funcionamiento de la app si no existen.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `os`, `logging`, `typing`, `pathlib`
- **Archivos Importados por este Archivo**:
  - Ninguno
- **Archivos que Importan a este Archivo**:
  - Ninguno


---

## Archivo: ./graphify-out/cache/ast/97a6f6a5225f6f3647cb58765f640cbc92e9013f91f47cf90f44b0e4fa3db713.json

### Resumen Funcional
El archivo `test_mock.py` contiene una función de prueba que utiliza SQLite y el módulo `unittest.mock` para realizar pruebas unitarias.

### Catálogo de Funciones y Clases
- `test_mock()` - Breve propósito: Realiza pruebas unitarias utilizando SQLite y el módulo `unittest.mock`.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna
- Columnas: Ninguna
- Consultas SQL crudas o llamadas a ORM: 
  - `connect()` - Se llama tres veces en la función `test_mock()`.
  - `patch()` - Se llama una vez en la función `test_mock()`.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `sqlite3`
  - `unittest.mock`

- Archivos del proyecto que este archivo importa (consume):
  - Ninguno

- Archivos del proyecto que importan a este archivo (lo consumen):
  - Ninguno

- Dirección del flujo de datos: El archivo `test_mock.py` importa `sqlite3` y `unittest.mock`, luego realiza pruebas unitarias utilizando estos módulos.


---

## Archivo: ./graphify-out/cache/ast/99ebae81be068909bb52edbc099a6f0a7f09032c9131533d852998675cae5290.json

### Resumen Funcional
El archivo `print_query_details.py` contiene código que realiza una consulta a la base de datos SQLite y luego imprime los detalles de esa consulta.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna (La consulta SQL está directamente en el código)
- Columnas: Ninguna (La consulta SQL está directamente en el código)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas: `sqlite3`
- Archivos del proyecto que importan a este archivo: Ninguno
- Archivos del proyecto que este archivo importa: Ninguno
- Flujo de datos: El archivo importa la librería `sqlite3` para realizar una consulta SQL y luego imprime los detalles de esa consulta.


---

## Archivo: ./graphify-out/cache/ast/9b7ac37b72b0e2c41d7ee6a023049a35a1b760ad5d471a5f7953e86dc517d01a.json

### Resumen Funcional
El archivo `query_engine.py` es un módulo que actúa como una fachada para el motor de SQL, proporcionando una interfaz simplificada y segura para realizar consultas en la base de datos.

### Catálogo de Funciones y Clases
- **Ninguna**

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (El archivo no contiene consultas SQL directas ni llamadas a ORM)
- **Columnas**: Ninguna

### Estado y Variables Globales
- **Ninguna**

### Dependencias y Flujo
- **Librerías Externas**:
  - `core_query_validators`
  - `core_query_utils`
  - `core_query_builder`

- **Archivos del Proyecto que Importan a Este Archivo**: Ninguno

- **Archivos del Proyecto que Este Archivo Importa**: Ninguno

- **Flujo de Datos**: El archivo importa módulos auxiliares (`core_query_validators`, `core_query_utils`, `core_query_builder`) para proporcionar una interfaz simplificada y segura para realizar consultas en la base de datos.


---

## Archivo: ./graphify-out/cache/ast/9bf240441d5ca7bf44b13f9124b4aaed34347ec728b50eceb36090792cf5ab21.json

### Resumen Funcional
El archivo `run_tests.sh` es un script de Bash que se ejecuta para correr pruebas en el sistema de monitoreo de almacén (WMS). Este script está ubicado en la carpeta `setup`.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías externas**: No se mencionan librerías externas específicas.
- **Archivos del proyecto que IMPORTA a este archivo (lo consumen)**: Ninguno
- **Archivos del proyecto que ESTE archivo IMPORTA (consume)**: Ninguno

El flujo de datos es simple, ya que el script `run_tests.sh` no depende de ninguna otra función o clase dentro del proyecto.


---

## Archivo: ./graphify-out/cache/ast/9bf25396ed6731406f1f2edfa1a977d07569eeb7d272b8f85a87b9be65e8e09a.json

### Resumen Funcional
El archivo `test_sla_monthly_compiled.py` es un script que realiza operaciones de monitoreo y análisis en un sistema de almacén (WMS) utilizando FastAPI, SQLAlchemy y SQLite.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- Motor: SQLite
- Tablas: Ninguna
- Columnas: Ninguna
- Consultas SQL crudas o llamadas a ORM: Ninguna

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `sqlite3`: Importada para interactuar con la base de datos SQLite.
  - `pandas`: Importada para el análisis de datos.

- Archivos del proyecto que este archivo importa (consume): Ninguno
- Archivos del proyecto que importan a este archivo (lo consumen): Ninguno

**Flujo de Datos:**
El script `test_sla_monthly_compiled.py` se ejecuta directamente y no depende de otros archivos o servicios dentro del proyecto. No realiza llamadas a otras funciones ni consume datos de otros componentes.


---

## Archivo: ./graphify-out/cache/ast/9d971d3e628599149fa1c11da8a1c6bd93049dd8bfba43374794d1ec90e12948.json

### Resumen Funcional
El archivo `test_ui_smoke.py` contiene pruebas de humo para un sistema de monitoreo de almacén (WMS). Las pruebas verifican la presencia de componentes visuales, manejo de errores y funcionalidades específicas del modal visual.

### Catálogo de Funciones y Clases
- `test_ui_smoke_components_presence()` - Verifica la presencia de componentes visuales.
- `test_ui_smoke_error_handling()` - Verifica que el servidor maneje correctamente las peticiones a rutas inexistente.
- `test_ui_smoke_analytics_studio_modal_components()` - Verifica que el modal visual exponga los selectores correctos y ejecute el SQL.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: `pytest`, `typing`
- **Archivos Importados por este Archivo**:
  - `tests/test_ui_smoke.py` (L1)
- **Archivos que Importan a este Archivo**: Ninguno

El flujo de datos es simple: el archivo `test_ui_smoke.py` importa las dependencias necesarias y contiene funciones que realizan pruebas específicas del sistema.


---

## Archivo: ./graphify-out/cache/ast/9ec5a58022289d00eb806477d5332a4cc7305b5150c1173de08ea12ff32a1624.json

### Resumen Funcional
El archivo `models_auth.py` contiene la definición del modelo ORM para los usuarios en el sistema de monitoreo de almacén (WMS). Este modelo incluye métodos y atributos necesarios para representar a un usuario, su rol y estado de activación.

### Catálogo de Funciones y Clases
- `User(base)` - Define la clase del modelo ORM para los usuarios.
  - `__repr__()` - Método que devuelve una representación en cadena del objeto `User`.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `users` (Tabla de usuarios del sistema)
- Columnas:
  - Roles ('admin', 'viewer')
  - Estado de desactivación

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**:
  - `datetime`
  - `sqlalchemy`
  - `sqlalchemy_orm`

- **Archivos del Proyecto que Importan a Este Archivo (`core/models_auth.py`)**:
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa (`core/models_auth.py`)**:
  - `database.py`

**Flujo de Datos**: El archivo `models_auth.py` importa las dependencias necesarias y define la clase `User`, que hereda de `Base`. La clase `User` incluye un método `__repr__()` para representar los objetos del modelo.


---

## Archivo: ./graphify-out/cache/ast/9f8e515e94a2bbe5d03bc612d9dd004df07f1dcdb947ed90befe5344aefe80fb.json

### Resumen Funcional
El archivo `query_ontime.py` contiene funciones para realizar consultas en una base de datos SQLite y procesar los resultados utilizando pandas.

### Catálogo de Funciones y Clases
- **Ninguna**

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** Ninguna (No hay consultas SQL explícitas)
- **Columnas:** Ninguna (No hay consultas SQL explícitas)

### Estado y Variables Globales
- **Ninguna**

### Dependencias y Flujo
- **Librerías Externas:**
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `json`: Para manejar operaciones JSON.
  - `pandas`: Para procesar los resultados de las consultas.

- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen):** Ninguna

- **Flujo de Datos:** El archivo importa librerías externas y no realiza ninguna interacción directa con el proyecto o la base de datos.


---

## Archivo: ./graphify-out/cache/ast/a12995f41d8a03f4ed3d4bccb51b752bf7807f0a47006ce375ea30845b24a3c7.json

### Resumen Funcional
El archivo `test_monthly_trend.py` contiene código que realiza un análisis de tendencias mensuales en el sistema de monitoreo de almacén (WMS). Es probablemente una prueba unitaria o integración para validar la funcionalidad relacionada con las tendencias mensuales.

### Catálogo de Funciones y Clases
Ninguna función o clase específica detectada en este fragmento.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna
- **Columnas**: Ninguna

El archivo no contiene consultas SQL crudas ni llamadas a ORM. Solo importa el módulo `sqlite3` para interactuar con la base de datos.

### Estado y Variables Globales
Ninguna variable global, de sesión o de entorno detectada en este fragmento.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `sys`
  - `sqlite3`

- **Archivos del Proyecto que IMPORTAN a Este Archivo**:
  - Ninguno

- **Archivos del Proyecto que ESTE Archivo IMPORTA**:
  - `core_queries_deliveries`

El flujo de datos es desde `test_monthly_trend.py` hacia los módulos importados (`sys`, `sqlite3`) y hacia el módulo `core_queries_deliveries`.


---

## Archivo: ./graphify-out/cache/ast/a3c4bc5b9154f3d0c90adefdd17b3bd588eebeb396ae769e559da03ba8539d30.json

### Resumen Funcional
El archivo `check_ollama.py` es un script que realiza operaciones relacionadas con el monitoreo de almacén (WMS). Es parte del sistema desarrollado con FastAPI, SQLAlchemy y SQLite.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: El archivo importa el módulo `ollama`.
- **Flujo de Datos**: No se proporcionan detalles específicos sobre cómo fluyen los datos en este fragmento.


---

## Archivo: ./graphify-out/cache/ast/a415e39ab77c0af4b8daf7b02dda0ddf5cb00e05d9a0fd6f117379cf3c2387aa.json

### Resumen Funcional
El archivo `consumos.py` contiene definiciones de rutas y métodos para el manejo de consumos en un sistema de monitoreo de almacén (WMS). Define endpoints para obtener los consumos agrupados por material, listar materiales consumidos por CeCos, y obtener el consumo mensual de un material específico.

### Catálogo de Funciones y Clases
- `MaterialesRequest` - Modelo Pydantic que representa una solicitud de materiales.
- `MaterialTrendRequest` - Modelo Pydantic que representa una solicitud de tendencia de materiales.
- `get_consumos_ceco()` - Obtiene los consumos (CMV 201) agrupados por material para un CeCo específico.
- `get_consumos_materiales()` - Obtiene que CeCos han consumido (CMV 201) una lista de materiales. Usa deduplicación.
- `get_material_trend()` - Devuelve el consumo mensual (CMV 201) de un material específico, filtrado por año.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas:
  - **Tabla:** `InventoryRepository` (No se especifican columnas específicas en la documentación proporcionada)
- Consultas SQL Crudas o Llamadas a ORM:
  - Se hace uso del repositorio `InventoryRepository` para obtener datos de inventario.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas:**
  - FastAPI
  - SQLAlchemy ORM
  - SQLAlchemy
  - Typing
  - Pydantic
  - Pandas
  - Core Database
  - Core Auth
  - Logging
  - Datetime

- **Flujo de Datos:**
  - `consumos.py` importa varios módulos y dependencias necesarias para su funcionamiento.
  - Los endpoints (`get_consumos_ceco`, `get_consumos_materiales`, `get_material_trend`) utilizan el repositorio `InventoryRepository` para interactuar con la base de datos SQLite.
  - Los métodos devuelven respuestas HTTP basadas en los resultados obtenidos del repositorio.

**Nota:** La documentación proporcionada no incluye detalles específicos sobre las consultas SQL o las columnas de la tabla `InventoryRepository`.


---

## Archivo: ./graphify-out/cache/ast/a4f8550fca26313fee016304a407c7aae994b81fa145487fb59adcc6b42cecce.json

### Resumen Funcional
El archivo `__init__.py` en la carpeta `services/etl` contiene funciones para procesar diferentes tipos de archivos relacionados con el inventario, tareas y entregas. Cada función parece estar diseñada para manejar un tipo específico de archivo y realizar operaciones de ETL (Extract, Transform, Load) sobre ellos.

### Catálogo de Funciones y Clases
- `process_inventory_folder()`: Procesa una carpeta de archivos relacionados con el inventario.
- `process_inventory_file()`: Procesa un archivo específico del inventario.
- `process_tasks_file()`: Procesa un archivo de tareas.
- `process_lx02_pendientes()`: Procesa un archivo de pendientes.
- `process_deliveries_file()`: Procesa un archivo de entregas.

### Interacción con Base de Datos
Ninguna. El código no interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno explícitamente mencionadas en el fragmento proporcionado.

### Dependencias y Flujo
- **Dependencias**: 
  - `InventoryMovementAdapter`
  - `WarehouseTaskAdapter`
  - `StockLevelAdapter`
  - `OutboundDeliveryAdapter`

- **Flujo de Datos**:
  - El archivo `__init__.py` importa varias clases (`InventoryMovementAdapter`, `WarehouseTaskAdapter`, `StockLevelAdapter`, `OutboundDeliveryAdapter`) y las utiliza dentro de sus funciones para procesar archivos.
  - Cada función llama a métodos como `process_directory()` o `process_and_save()` en estas clases adaptadoras.

El flujo general es que el archivo `__init__.py` coordina la llamada a diferentes adaptadores para procesar diferentes tipos de archivos, lo que sugiere una arquitectura modular y separada de preocupaciones.


---

## Archivo: ./graphify-out/cache/ast/a51baa519bf19235a8f8606a35cb8eaff5fd7089cefb186c8953005a3b2d320b.json

### Resumen Funcional
El archivo `update_dirs.py` es un script que realiza operaciones relacionadas con la actualización de directorios en el sistema de monitoreo de almacén (WMS). No contiene ninguna interacción explícita con una base de datos.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite3
- **Tablas**: Ninguna
- **Columnas**: Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `sqlite3`
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno
- **Archivos del Proyecto que Este Archivo Importa**: Ninguno
- **Flujo de Datos**: El archivo importa la librería `sqlite3` y no realiza ninguna operación con una base de datos.


---

## Archivo: ./graphify-out/cache/ast/a68814848abf03efe4787c8174f3b6993408716cf4ca76ea651ef3532a8ab34b.json

### Resumen Funcional
El archivo `tasks.py` contiene la implementación del adaptador para procesar el formato WMS Tareas (órdenes de transporte). Define una clase `WarehouseTaskAdapter` que hereda de `BaseWMSProcessor`, y métodos para validar archivos, obtener columnas requeridas, obtener claves primarias y limpiar un DataFrame.

### Catálogo de Funciones y Clases
- **Clase:** `WarehouseTaskAdapter`
  - **Método:** `.validate_file(file_path: Path) -> bool` - Valida el archivo según ciertos criterios.
  - **Método:** `._get_required_columns() -> List[str]` - Devuelve las columnas requeridas para el procesamiento.
  - **Método:** `._get_primary_keys() -> List[str]` - Devuelve las claves primarias del DataFrame.
  - **Método:** `._clean_dataframe(df: DataFrame) -> DataFrame` - Limpia y normaliza el DataFrame.

- **Clase:** `BaseWMSProcessor`
  (No se proporciona implementación en este fragmento)

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas:**
  - `pandas`
  - `pathlib`
  - `typing`

- **Archivos del Proyecto que Importan a Este Archivo (`services/etl/tasks.py`):**
  - No se proporciona información sobre los archivos que importan a este archivo.

- **Archivos del Proyecto que Este Archivo Importa:**
  - `users_christianykelly_desktop_monitorweb_services_etl_base_py`

- **Flujo de Datos:**
  El archivo `tasks.py` es importado por otros módulos, y utiliza métodos y clases definidos en él para procesar archivos WMS Tareas.


---

## Archivo: ./graphify-out/cache/ast/a6b37b42a7be88d390753feb2d6df3c445433887f218e9f119b0e0260928f928.json

### Resumen Funcional
El archivo `dashboard_service.py` contiene la definición de la clase `DashboardService`, que es responsable del orquestador del dashboard principal de Entregas (vista operativa). La clase incluye métodos para obtener el contexto completo del dashboard.

### Catálogo de Funciones y Clases
- **DashboardService()** - Constructor de la clase.
  - Parámetros: `session` (Tipo: Session)
- **get_full_context()** - Método que retorna un contexto completo del dashboard.
  - Parámetros: Ninguno
  - Retorno: Tipo: str, Any

### Interacción con Base de Datos
No se especifican consultas SQL crudas o llamadas a ORM en este archivo. La interacción con la base de datos se realiza a través de la clase `DeliveriesRepository`.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - logging
  - sqlalchemy.orm
  - typing
  - datetime
- **Archivos Importados**:
  - repositories.deliveries (DeliveriesRepository)
- **Archivos que Importan a Este Archivo**: Ninguno.

El flujo de datos fluye desde el archivo `dashboard_service.py` hacia la clase `DeliveriesRepository` para obtener los datos necesarios y luego se procesan en el método `get_full_context()` para construir el contexto del dashboard.


---

## Archivo: ./graphify-out/cache/ast/ae171fdce99e467dfe04fcaf020f10002786f4642de3564e9e28a5be68c79c97.json

### Resumen Funcional
El archivo `task_manager.py` contiene la implementación del gestor de tareas en segundo plano (Background Task Queue) para el sistema de monitoreo de almacén (WMS). Define clases y métodos para manejar el estado, registro e interacción con las tareas.

### Catálogo de Funciones y Clases
- **TaskStatus** - Enumeración que define los estados posibles de una tarea.
- **TaskRecord** - Clase que representa un registro inmutable de una tarea ejecutada o en ejecución.
- **TaskManager** - Clase principal que gestiona el encolamiento, ejecución y estado de las tareas.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `uuid`, `logging`, `datetime`, `concurrent.futures`, `dataclasses`, `enum`, `typing`, `threading`
- **Archivos Importados por este Archivo**:
  - Ninguno
- **Archivos que Importan a este Archivo**:
  - Ninguno

El flujo de datos se centra en la interacción entre las clases y métodos definidos, utilizando objetos como `TaskRecord` para almacenar el estado de las tareas y un `ThreadPoolExecutor` para ejecutar tareas en segundo plano.


---

## Archivo: ./graphify-out/cache/ast/b382729f7f3fb246a2d27c6a164f100abc5262e21745b4a51d5334a7c82bbfd8.json

### Resumen Funcional
El archivo `config.py` contiene la configuración centralizada de las rutas para el sistema de monitoreo de almacén (WMS) construido con FastAPI. Registra todos los routers de la aplicación de forma centralizada.

### Catálogo de Funciones y Clases
- **register_routes()** - Registra todos los routers de la aplicaciónde forma centralizada.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: FastAPI, typing
- **Archivos Importados por este Archivo**:
  - `logging`
  - `fastapi`
  - `typing`
  - `users_christianykelly_desktop_monitorweb_routes_init_py`
- **Archivos que Importan a este Archivo**: Ninguno

El flujo de datos es desde `config.py` hacia las funciones y clases importadas, específicamente hacia `FastAPI` para la configuración de rutas.


---

## Archivo: ./graphify-out/cache/ast/b44958fcbb00e0f75a5baf55d458b9a749d2fcf81ffcf4c089f883cd132e5c21.json

### Resumen Funcional
El archivo `debug_streaming.py` es un módulo que importa las bibliotecas `ollama` y `time`. No contiene ninguna función o clase definida explícitamente.

### Catálogo de Funciones y Clases
Ninguna.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: `ollama`, `time`
- **Flujo de datos**: El archivo importa las bibliotecas mencionadas pero no realiza ninguna operación específica que involucre funciones, clases o consultas a una base de datos.


---

## Archivo: ./graphify-out/cache/ast/b4c6552984ca65fc0b751b88a1107f25d073949379dfbe576129132fb769d368.json

### Resumen Funcional
El archivo `app_instance.py` es el punto de entrada del sistema, donde se configura y ejecuta la instancia principal de la aplicación utilizando FastAPI.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `pathlib`, `fastapi`, `fastapi_templating`
- **Archivos Importados por Este Archivo**:
  - `config` (importado en la línea 4)
- **Archivos que Importan a Este Archivo**: Ninguno

El flujo de datos es simple: el archivo `app_instance.py` importa las dependencias necesarias y configura la instancia principal de FastAPI.


---

## Archivo: ./graphify-out/cache/ast/b6c5a257816e454f4dd7ce7bdbd479f0213aeddcdde66e78d5c66b893168e199.json

### Resumen Funcional
El archivo `core/wms_config.py` contiene la configuración de lógica de negocio y mapeos WMS (SaaS Dinámico). Incluye funciones para validar los mapeos definidos.

### Catálogo de Funciones y Clases
- `validate_wms_maps()` - Valida la integridad de los mapeos definidos.
- `__getattr__()` - Maneja el acceso a atributos dinámicamente.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `typing`
  - `users_christianykelly_desktop_monitorweb_core_db_config_manager_py`

- **Flujo de Datos**:
  - `core/wms_config.py` importa `typing` y `users_christianykelly_desktop_monitorweb_core_db_config_manager_py`.
  - `validate_wms_maps()` llama a funciones como `get_status_mapping`, `ValueError`, `get_cost_center_mapping`, y `items`.
  - `__getattr__()` llama a funciones como `get_status_mapping`, `get_cost_center_mapping`, `get_setting`, y `AttributeError`.


---

## Archivo: ./graphify-out/cache/ast/b86003582c38796a8641e51ce613371fe2f07266eab2a0ec4281824e0ff97b87.json

### Resumen Funcional
El archivo `run_sync.py` es un script que realiza operaciones de sincronización en el sistema de monitoreo de almacén (WMS). No contiene ninguna lógica específica, solo importa módulos y configuraiones necesarias para la ejecución del sistema.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `sys`, `os`, `pathlib`, `logging`
- **Archivos Importados por este Archivo**:
  - `core_db_config_manager` (L13)
  - `routes_sync` (L17)
- **Archivos que Importan a este Archivo**: Ninguno

El archivo `run_sync.py` solo importa módulos y no realiza ninguna operación específica, por lo tanto, no interactúa con la base de datos ni tiene funciones definidas.


---

## Archivo: ./graphify-out/cache/ast/baf0e02fef0e872c8b7015942cb6266d9df1968305338d7efe0c7bc6b3ac6fb7.json

### Resumen Funcional
El archivo `widgets.json` contiene datos de configuración para widgets en el sistema de monitoreo de almacén (WMS). Este JSON se utiliza para inicializar los widgets en la interfaz web.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna


---

## Archivo: ./graphify-out/cache/ast/bbe8fba0598f812263746337209ef980788a2253525f2cf77f90e1d12f18241b.json

### Resumen Funcional
El archivo `test_modal_query.py` contiene una función de prueba que realiza consultas SQL contra una base de datos SQLite.

### Catálogo de Funciones y Clases
- `test_query()` - Realiza consultas SQL para obtener datos de la base de datos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:** No se especifican columnas específicas, solo indica que realiza operaciones CRUD.
- **Consultas SQL Crudas:** 
  - `execute("SELECT * FROM table_name")`
  - `fetchall()`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas:** Ninguna.
- **Archivos Importados por este Archivo:** `sqlite3`
- **Archivos que Importan a este Archivo:** Ninguno.


---

## Archivo: ./graphify-out/cache/ast/bcd344c6625ed9ef8aeb660b216431d084d22622ae5997150983d8eb81e5b77b.json

### Resumen Funcional
Este archivo es el punto de entrada para los servicios en el sistema de monitoreo de almacén (WMS). Contiene la configuración y la definición de las dependencias necesarias para que los servicios puedan funcionar.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: No se especifican dependencias directas en el fragmento proporcionado.
- **Flujo**: Este archivo no importa ni es importado por otros archivos. Es el punto de entrada para los servicios, lo que significa que los demás archivos (routes, repositories) deben importar este archivo para acceder a las funcionalidades definidas aquí.

Este archivo es crucial para la configuración inicial y la definición de dependencias globales en el sistema WMS, pero no realiza ninguna operación específica relacionada con la base de datos o la lógica de negocio.


---

## Archivo: ./graphify-out/cache/ast/bf234d835321cd0470b7ee1749d5807d30042464c9a3fa919e5438f788e6eb2b.json

### Resumen Funcional
El archivo `test_enrichment.py` contiene pruebas unitarias para el módulo de enriquecimiento del sistema de monitoreo de almacén (WMS). Las pruebas cubren la creación de una base de datos con datos de prueba, la aplicación de lógica de autorización, la recarga de entregas desde movimientos, el enriquecimiento de entregas con existencias y la actualización del SLA usando tareas de bodega.

### Catálogo de Funciones y Clases
- `db_with_data(connection)` - Prepara una base de datos con datos de prueba para los procesos de enriquecimiento.
- `test_learn_and_apply_author_logic()` - Verifica que el sistema aprenda que USER_A pertenece a PRODUCCION y lo aplique.
- `test_backfill_from_movements()` - Verifica que Entregas recupere el autor y centro de costo desde Movimientos.
- `test_enrichment_from_stock()` - Verifica que se crucen las descripciones de material y ubicaciones desde el maestro.
- `test_update_sla_with_tasks()` - Verifica que el SLA se actualice correctamente usando las tareas de bodega.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: `Movimientos`
    - Columna: `autor`, `centro_costo`
  - Tabla: `Entregas`
    - Columna: `id`, `material`, `ubicacion`
  - Tabla: `SLA`
    - Columna: `id`, `tarea_bodega`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `pytest`, `sqlite3`, `typing`
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:**
  - `db_enrichment` (Módulo que contiene funciones relacionadas con el enriquecimiento)

El flujo de datos es desde las pruebas hasta la ejecución de métodos que interactúan con la base de datos para realizar operaciones como `execute`, `commit`, `rollback`, y `fetchone`.


---

## Archivo: ./graphify-out/cache/ast/c23f2fe4b174b95d33b5c3e9866f3945a6db338af5b7f29369fd525fda11327e.json

### Resumen Funcional
El archivo `fix_descriptions.py` contiene una función llamada `manual_fix()` que realiza operaciones de base de datos para corregir descripciones en un sistema de almacén.

### Catálogo de Funciones y Clases
- `manual_fix()` - Realiza la lógica principal para corregir las descripciones en el sistema de almacén.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas Modificadas:**
  - Tabla: Ninguna específica mencionada.
  - Columna: Ninguna específica mencionada.
- **Consultas SQL Crudas o Llamadas a ORM:**
  - `connect()`
  - `fetchone()`
  - `execute()`
  - `backfill_material_texts()`

### Estado y Variables Globales
- Ninguna variable global, de sesión o diccionario quemado en el código que almacene estado crítico.

### Dependencias y Flujo
- **Librerías Externas:**
  - `sqlite3`
- **Archivos del Proyecto que Importan a este Archivo (lo consumen):**
  - Ninguno mencionado.
- **Archivos del Proyecto que Este Archivo Importa (consume):**
  - `db_enrichment`
  - `config`

**Flujo de Datos:**
1. El archivo `fix_descriptions.py` importa las dependencias necesarias (`sqlite3`, `db_enrichment`, `config`).
2. La función `manual_fix()` se ejecuta.
3. Dentro de `manual_fix()`, se realizan operaciones de base de datos utilizando funciones como `connect()`, `fetchone()`, y `execute()`.
4. Llama a la función `backfill_material_texts()` para realizar la lógica específica de corrección.
5. Finalmente, cierra la conexión con la base de datos usando `close()`.


---

## Archivo: ./graphify-out/cache/ast/c6369523a35d0fd10bc77e07324d719e0fc3fe8abd6e108a82974ede400776fe.json

### Resumen Funcional
El archivo `deliveries_service.py` contiene la definición de una clase `DeliveriesService` que probablemente se encarga de gestionar operaciones relacionadas con las entregas en un sistema de almacén (WMS). La clase incluye métodos para obtener el contexto completo y posiblemente otras operaciones relacionadas.

### Catálogo de Funciones y Clases
- `DeliveriesService()` - Constructor de la clase.
- `.get_full_context()` - Método que probablemente recupera el contexto completo del sistema.

### Interacción con Base de Datos
El archivo interactúa con una base de datos utilizando SQLAlchemy ORM. Las tablas y columnas específicas no se mencionan explícitamente, pero se utilizan métodos como `query`, `like`, `fetchall`, `execute` y `update`, lo que sugiere operaciones en tablas relacionadas con las entregas.

### Estado y Variables Globales
No hay variables globales, de sesión o diccionarios quemados en el código proporcionado.

### Dependencias y Flujo
- **Dependencias**: El archivo importa módulos como `sqlalchemy_orm`, `logging` y `typing`.
- **Flujo de Datos**: El archivo se importa por otros archivos del proyecto, pero no se mencionan específicamente qué archivos lo consumen.


---

## Archivo: ./graphify-out/cache/ast/c6651364f972da4c7b3f539da937474a15c6e5d2e5b74d33b7ec8f4ca2448792.json

### Resumen Funcional
El archivo `dashboard.py` contiene funciones relacionadas con el manejo del dashboard en un sistema de monitoreo de almacén (WMS). Incluye endpoints para obtener ubicaciones y una vista principal del dashboard con KPIs.

### Catálogo de Funciones y Clases
- **get_ubicaciones(str, Session, AppState)** - Obtiene ubicaciones.
- **dashboard(Request, Session, AppState)** - Vista principal del Dashboard con KPIs y búsqueda rápida.
- **dashboard_api(Session, AppState)** - API JSON para el Dashboard con KPIs y búsqueda rápida.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas y Columnas**:
  - Tabla: `ubicaciones`
    - Columna: `id`, `nombre`, `ubicacion`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - logging
  - sqlite3
  - itertools
  - pandas
  - datetime
  - typing
  - fastapi
  - fastapi_responses
  - core_database
  - sqlalchemy_orm
  - sqlalchemy
  - core_state
  - core_auth
  - core_app_instance
  - services_dashboard_service
  - core_schemas

- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno

- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno


---

## Archivo: ./graphify-out/cache/ast/c9a2e6284ae1fb0bb05cf560d5f4f625c95b499c17aee158f2db2edd806f0d64.json

### Resumen Funcional
El archivo `check_server.py` contiene una función llamada `check_server()` que realiza operaciones de red y procesamiento de datos para monitorear el estado de un servidor.

### Catálogo de Funciones y Clases
- **check_server()** - Realiza la lógica principal del script, incluyendo solicitudes HTTP y análisis de respuestas.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `urllib.request`, `json`, `re`
- **Archivos Importados por Este Archivo**: Ninguno
- **Archivos que Importan a Este Archivo**: Ninguno
- **Flujo de Datos**: El flujo comienza con la importación de las librerías necesarias, luego se ejecuta la función `check_server()`, que realiza una solicitud HTTP y procesa la respuesta.


---

## Archivo: ./graphify-out/cache/ast/ca48e7c22dd9c8b95961caf538090e46ed93f0789cdf1ec0f5e2cfd3b2273138.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `sync.py` contiene funciones relacionadas con la sincronización de datos en un sistema de almacén (WMS). Incluye endpoints para obtener la URL del túnel, el estado de la sincronización, iniciar la sincronización, listar tareas y consultar el estado de una tarea específica.

### Catálogo de Funciones y Clases
- `get_tunnel_url(appstate: AppState)` - Retorna la URL pубlica del túnel (Ngrok).
- `get_sync_status(appstate: AppState)` - Retorna el estado actual de la sincronización.
- `sync_data(appstate: AppState)` - Inicia el proceso de sincronización de datos. Encola la tarea en el TaskManager.
- `list_tasks(limit: int, appstate: AppState)` - Lista las tareas recientes del sistema.
- `get_task(task_id: str, appstate: AppState)` - Consulta el estado de una tarea específica por su ID.
- `_run_sync_pipeline(appstate: AppState)` - Ejecuta el pipeline completo de limpieza y consolidación.
- `_reset_directory(directory_path: str)` - Elimina y recrea un directorio de forma segura.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno quemadas en el código.

### Dependencias y Flujo
- **Librerías Externas**: `logging`, `shutil`, `pathlib`, `typing`, `fastapi`, `core_auth`, `config`, `core_state`, `core_task_manager`, `db_consolidator`.
- **Archivos Importados por este Archivo**:
  - `routes/sync.py` importa varias clases y funciones de otros archivos del proyecto.
- **Archivos que Importan a este Archivo**: No hay información sobre qué archivos importan a `sync.py`.

El flujo de datos es principalmente entre las funciones definidas en `sync.py`, utilizando objetos como `AppState` para compartir el estado del sistema.


---

## Archivo: ./graphify-out/cache/ast/cb7b0d02adac684714ccb754d1e09d30f5abc3528c018ed2e018ec2f5b384adf.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `routes/widgets.py` contiene endpoints para obtener datos de widgets y detalles subyacentes. Incluye funciones que ejecutan consultas SQL, manipulan datos y manejan errores.

### Catálogo de Funciones y Clases
- **get_widget_data()** - Obtiene datos de un widget.
- **get_widget_drilldown()** - Obtiene detalles subyacentes de un segmento de un widget.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** No especificadas explícitamente en el fragmento, pero se hace referencia a `WidgetRepository`.
- **Columnas:** No especificadas explícitamente en el fragmento.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno mencionadas.

### Dependencias y Flujo
- **Dependencias Externas:**
  - `fastapi`
  - `sqlalchemy_orm`
  - `core_database`
  - `core_models`
  - `core_auth`
  - `core_helpers_dynamic_executor`
  - `core_utils`
  - `core_state`

- **Archivos Importados por este Archivo:** Ninguno

- **Archivos que Importan a este Archivo:** Ninguno


---

## Archivo: ./graphify-out/cache/ast/cbbc3f651a1613a4f3ec8136ed98a535a1fb66d0a70ff714d073f44415f17e0a.json

### Resumen Funcional
Este archivo es el punto de entrada para la configuración y inicialización de la base de datos en un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Contiene la definición del motor de base de datos y la creación de las tablas necesarias.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna (el archivo solo inicializa el motor, no crea o modifica tablas)
- **Consultas SQL Crudas/ORM**: Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: SQLAlchemy
- **Archivos del Proyecto que Importan a este Archivo**: Ninguno
- **Archivos del Proyecto que Este Archivo Importa**: Repositories, Models (dependencia implícita a través de SQLAlchemy)
- **Dirección del Flujo de Datos**: El archivo se importa por otros archivos para configurar la base de datos.


---

## Archivo: ./graphify-out/cache/ast/ce5231446f6376685a1145238b9d71f4eac28cde5fc6a1b963d24ae59dd4aeec.json

### Resumen Funcional
El archivo `run_deliveries_context.py` contiene el contexto necesario para ejecutar operaciones relacionadas con las entregas en un sistema de monitoreo de almacén (WMS). Importa varias bibliotecas y módulos necesarios para su funcionamiento.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `sqlite3`, `pandas`, `logging`, `sys`
- **Módulos del Proyecto Importados**:
  - `routes_deliveries`
  - `traceback`

El archivo `run_deliveries_context.py` importa estas dependencias y módulos para su uso en el contexto de ejecutar operaciones relacionadas con las entregas. No realiza ninguna interacción directa con una base de datos ni utiliza variables globales.


---

## Archivo: ./graphify-out/cache/ast/d0c253d9963e39693ebd33bdbe38f32befb1802887646c16622128658d97c72b.json

### Resumen Funcional
El archivo `update_eff.py` es un script que realiza operaciones de actualización en una base de datos SQLite.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna
- **Columnas**: Ninguna
- **Consultas SQL Crudas o Llamadas a ORM**: No hay consultas SQL crudas ni llamadas a ORM explícitas.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Importada para interactuar con la base de datos SQLite.
  - `json`: Importada para manejar operaciones JSON (probablemente para leer o escribir archivos JSON).
  
- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno

**Flujo de Datos**: El archivo `update_eff.py` importa las bibliotecas necesarias y realiza operaciones relacionadas con la base de datos SQLite, pero no hay detalles específicos sobre qué funciones o métodos se utilizan para interactuar con la BD.


---

## Archivo: ./graphify-out/cache/ast/d245f9cdf70e1c6b963d8ce6c2570b5be09e0d83e2b8ad72e954af56f4b8b9cd.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `doc_generator.py` contiene funciones para generar documentación de proyectos utilizando un modelo de lenguaje llamado Ollama. El sistema analiza la estructura del proyecto, genera una representación en texto del árbol del proyecto, y luego documenta cada archivo con el modelo Ollama.

### Catálogo de Funciones y Clases
- `load_gitignore()`: Carga las reglas de `.gitignore`.
- `sanitize_output()`: Sanitiza la salida para evitar caracteres no deseados.
- `load_state()`: Carga el estado actual del sistema desde un archivo.
- `save_state()`: Guarda el estado actual del sistema en un archivo.
- `get_file_info()`: Obtiene información sobre un archivo, como su hash y tamaño.
- `get_cache_path()`: Genera una ruta única dentro de la caché para cada archivo.
- `should_process()`: Determina si un archivo debe ser procesado basándose en sus características.
- `generate_project_tree()`: Genera una representación en texto del árbol del proyecto.
- `chunk_text()`: Divide el texto en fragmentos con un solapamiento de líneas para mantener contexto.
- `calculate_num_ctx()`: Calcula num_ctx dinámicamente basándose en la cantidad de líneas y tamaño del código.
- `call_ollama_with_retry()`: Llamada a Ollama unificada usando la librería oficial. Si no se proporciona el modelo, intenta usar uno por defecto.
- `format_seconds()`: Convierte segundos a formato HH:MM:SS.
- `document_file()`: Procesa un archivo, mide el tiempo y retorna True si tuvo éxito.
- `analyze_structure_pre_flight()`: Genera el árbol del proyecto y realiza el análisis arquitectónico estructural.
- `generate_audit_post_flight()`: Genera la Auditoría Global analizando la documentación ya generada en la caché.
- `compile_master_file()`: Une todos los fragmentos de la caché en los archivos maestros en orden.
- `compile_by_folders()`: Compila la documentación y mejoras agrupándolas por carpetas del proyecto.
- `prepare_model()`: Verifica si Ollama está activo y si el modelo solicitado existe.
- `cleanup_orphaned_cache()`: Elimina de la caché los archivos que ya no existen en el proyecto.
- `purge_empty_cache_files()`: Busca y elimina archivos en `.doc_cache` que estén vacíos o corruptos para forzar su eliminación.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `os`, `sys`, `time`, `json`, `ollama`, `hashlib`, `tqdm`
- **Archivos del Proyecto que Este Archivo Importa (consume)**: No aplica
- **Archivos del Proyecto que Importan a Este Archivo (lo consumen)**: No aplica

**Flujo de Datos**: El archivo `doc_generator.py` se ejecuta como parte del flujo principal del sistema, llamando a varias funciones para procesar y documentar el proyecto.


---

## Archivo: ./graphify-out/cache/ast/d297121c31a0f65d30e0c80825d81c969e1f244a6a9d8c7532089be22905fd72.json

### Resumen Funcional
El archivo `test_traceback.py` contiene una función `run()` que realiza operaciones relacionadas con la conexión a una base de datos SQLite, prepara un análisis de tendencias de consumo planificado y maneja excepciones.

### Catálogo de Funciones y Clases
- `run()` - Realiza operaciones de conexión a la base de datos, preparación de análisis de tendencias de consumo planificado y manejo de excepciones.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:** Ninguna (No hay consultas SQL explícitas o llamadas a ORM)
- **Consultas SQL Crudas/LLamadas a ORM:** Ninguna

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `sqlite3`
  - `traceback`
  - `logging`

- **Archivos del Proyecto que IMPORTAN a este archivo (lo consumen):** Ninguno
- **Archivos del Proyecto que ESTE archivo IMPORTA (consume):** Ninguno

- **Flujo de Datos:**
  - El archivo importa las bibliotecas necesarias (`sqlite3`, `traceback`, `logging`).
  - La función `run()` realiza operaciones relacionadas con la base de datos SQLite.
  - Se manejan excepciones utilizando `traceback.print_exc()`.
  - No hay interacción explícita con tablas o columnas específicas en la BD.


---

## Archivo: ./graphify-out/cache/ast/d34ce2e8af578f86ed77a620faaca8c4847b1939f59c2ca8abe8834c32e58a3b.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `routes/transporte.py` contiene funciones relacionadas con la gestión de transporte en el sistema de monitoreo de almacén (WMS). Incluye lógica para sincronizar datos, buscar y servir PDFs.

### Catálogo de Funciones y Clases
- **sync_transporte_logic(session: Session)** - Lógica core para sincronizar la base de datos externa de OneDrive a local.
- **sync_transporte()** - Sincroniza datos de transporte manualmente.
- **get_transporte_data()** - Retorna los datos consolidados diarios ordenados cronológicamente.
- **search_transporte(query: str)** - Busca en la tabla cruda de transporte_entregas por OT, GD o OC.
- **serve_pdf(filename: str)** - Sirve el archivo PDF desde el disco.
- **get_pending_transporte()** - Busca en transporte_entregas los documentos del año actual que NO han sido ingresados.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `transporte_entregas`
- Columnas (ejemplos):
  - `id`, `ot`, `gd`, `oc`, `fecha`, `archivo_pdf`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**:
  - `os`
  - `sqlite3`
  - `logging`
  - `typing`
  - `fastapi`
  - `fastapi_responses`
  - `sqlalchemy_orm`
  - `sqlalchemy`

- **Flujo de Datos**:
  - El archivo importa varias bibliotecas y módulos necesarios para su funcionamiento.
  - Las funciones utilizan la sesión de SQLAlchemy (`session`) para interactuar con la base de datos.
  - Llamadas a métodos como `execute`, `fetchall`, `commit` y `rollback` se realizan en las funciones para realizar operaciones CRUD en la base de datos.


---

## Archivo: ./graphify-out/cache/ast/d36c74aa7b763b4f4e82ab690b1d8254f7b539c193ec263bef95a20109b156ae.json

### Resumen Funcional
La clase `AppState` en el archivo `state.py` gestiona el estado mutable y la caché de forma centralizada, proporcionando métodos para configurar y obtener límites de caché, manejar sincronización, acceder a y modificar datos en caché, y limpiar caché.

### Catálogo de Funciones y Clases
- **Clase:** `AppState`
  - **Método:** `__init__()`
    - Propósito: Inicializa el estado del objeto.
  - **Método:** `max_cache_size()`
    - Parámetros: `size` (int)
    - Propósito: Devuelve o configura el límite máximo de entradas en caché.
  - **Método:** `sync_lock()`
    - Propósito: Devuelve el lock de sincronización para operaciones atómicas.
  - **Método:** `is_syncing()`
    - Parámetros: `is_syncing` (bool)
    - Propósito: Verifica si hay un proceso de sincronización activo.
  - **Método:** `cache_size()`
    - Propósito: Devuelve el número actual de entradas en la caché.
  - **Método:** `get_cache()`
    - Parámetros: `key` (str)
    - Propósito: Recupera un valor del caché.
  - **Método:** `set_cache()`
    - Parámetros: `key` (str), `value` (any)
    - Propósito: Guarda un valor en el caché, respetando los límites de tamaño.
  - **Método:** `clear_cache()`
    - Propósito: Limpia una entrada específcica o todo el caché.
  - **Método:** `clear_cache_prefix()`
    - Parámetros: `prefix` (str)
    - Propósito: Limpia todas las entradas de caché que comiencen con el prefijo dado.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas:** `fastapi`, `logging`, `threading`, `typing`
- **Archivos Importados por este Archivo:**
  - Ninguno
- **Archivos que Importan a este Archivo:**
  - Ninguno


---

## Archivo: ./graphify-out/cache/ast/d39615dd01370c6263d23a26234b550b372dee31ad1ed0986baf0a503344a781.json

### Resumen Funcional
El archivo `test_queries.py` contiene pruebas unitarias para funciones relacionadas con consultas y operaciones de base de datos en un sistema de monitoreo de almacén (WMS). Las pruebas incluyen la obtención de estadísticas, conteos de días activos y cálculos de KPIs.

### Catálogo de Funciones y Clases
- `MockConnectionWrapper` - Clase que simula una conexión a la base de datos.
  - `.__init__()` - Inicializa el objeto.
- `MockSession` - Clase que simula una sesión de base de datos.
  - `.__init__()` - Inicializa el objeto.
  - `.connection()` - Devuelve una simulación de conexión.
  - `.execute()` - Ejecuta una consulta SQL.
- `test_get_total_active_days()` - Prueba la obtención del conteo total de días activos.
- `test_get_total_active_days_empty()` - Prueba el comportamiento cuando no hay datos para contar.
- `test_get_area_stats()` - Prueba la obtención de estadísticas por área.
- `test_area_expr_fallback_locations()` - Prueba el manejo de expresiones fallidas en áreas.
- `test_query_engine_compiles_ast_correctly()` - Prueba que el motor de consultas compile correctamente el AST.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQLite. Las tablas y columnas específicas no se mencionan explícitamente, pero las pruebas implican operaciones en la base de datos para obtener estadísticas y contar días activos.

### Estado y Variables Globales
No hay variables globales, de sesión o diccionarios quemados en el código que almacenen estado crítico.

### Dependencias y Flujo
- **Librerías Externas**: `pytest`, `sqlite3`, `pandas`.
- **Archivos del Proyecto Importados**:
  - `repositories_deliveries` (se importa desde `tests/test_queries.py`)
- **Archivos que Importan a Este Archivo**: Ninguno.
- **Flujo de Datos**: El archivo consume funciones y clases de otros archivos para realizar pruebas unitarias, incluyendo la simulación de una conexión y sesión de base de datos.


---

## Archivo: ./graphify-out/cache/ast/d7671e63795698e7a7f01364d50480a7aaacbb5c7f34a55d2a9738faba99d8a0.json (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `core/wms_utils.py` contiene funciones utilitarias vectorizadas para transformación de datos, incluyendo la normalización de strings, mapeo de estados WMS, clasificación de ubicaciones en áreas de negocio, estandarización de fechas y cálculo de retrasos SLA.

### Catálogo de Funciones y Clases
- `sanitize_string(str)`: Normaliza un string para usarlo como encabezado de columna (snake_case).
- `map_wms_status(dataframe)`: Concatena columnas de estado y mapea al valor legible de negocio.
- `apply_cost_center_mapping(dataframe)`: Clasifica ubicaciones WMS en áreas de negocio de forma vectorizada.
- `normalize_date_columns(dataframe)`: Estandariza formatos de fecha WMS a dd-mm-yyyy de forma eficiente.
- `calculate_sla_delays(dataframe)`: Calcula días hábiles de retraso usando lógica vectorizada de NumPy.
- `generate_time_labels(dataframe)`: Genera etiquetas de semana ISO para visualización y analítica.
- `_manifest_execute(str)`: Ejecuta una query de manifiesto sobre Session SQLAlchemy o sqlite3.Connection.
- `is_file_changed(path)`: Verifica si un archivo ha cambiado desde la última sincronización. Acepta SQLAlchemy Session.
- `mark_file_processed(path, int)`: Marca un archivo como procesado en el manifiesto. Acepta SQLAlchemy Session.

### Interacción con Base de Datos
No se utiliza ninguna base de datos explícita. Todas las operaciones son realizadas sobre DataFrames de pandas o consultas SQL directas a través de SQLAlchemy.

### Estado y Variables Globales
Ninguna variable global, de sesión ni diccionario quemado en código que almacene estado crítico.

### Dependencias y Flujo
- **Librerías Externas**: `numpy`, `pandas`, `datetime`, `pathlib`, `typing`.
- **Archivos del Proyecto Importados**:
  - `core_wms_config`
  - `core_db_config_manager`
  - `sqlalchemy_orm`
  - `sqlalchemy`
- **Archivos que Importan a Este Archivo**: Ninguno.

El flujo de datos fluye desde las funciones utilitarias hasta la ejecución de consultas SQL y manipulación de DataFrames.


---

## Archivo: ./graphify-out/cache/ast/d7f3c3d4f2f27ae9f02b3b36ebe206cc405e57d624b56bcb2ef4484abb331fa9.json

### Resumen Funcional
El archivo `test_diag.py` contiene una función llamada `diag()` que realiza operaciones de base de datos utilizando SQLite.

### Catálogo de Funciones y Clases
- `diag()` - Realiza consultas a la base de datos para obtener información.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:** Ninguna (se supone que las tablas y columnas son específicas del contexto de la consulta SQL, pero no se proporcionan detalles adicionales).
- **Consultas SQL Crudas:** 
  - `connect()`
  - `cursor()`
  - `execute("SELECT * FROM table_name")` (donde `table_name` es una tabla específica)
  - `fetchall()`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas:** Ninguna.
- **Archivos Importados por este Archivo:** Ninguno.
- **Archivos que Importan a este Archivo:** Ninguno.
- **Flujo de Datos:** El archivo `test_diag.py` importa el módulo `sqlite3`, realiza una conexión a la base de datos, ejecuta una consulta y recupera los resultados.


---

## Archivo: ./graphify-out/cache/ast/db2f152027ef2d98ee4f249514ec07c6e58b6d59b1f7948fbf0d66f1bbaa1d6b.json

### Resumen Funcional
El archivo `security.py` contiene una función que valida el nombre de una tabla contra una lista blanca para prevenir SQL Injection.

### Catálogo de Funciones y Clases
- **validate_table(table_name: str)** - Valida el nombre de la tabla contra la lista blanca para prevenir SQL Injection.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: Importa `typing` (línea 4).
- **Flujo de Datos**: La función `validate_table` recibe un parámetro `table_name` del tipo `str`. Si el nombre de la tabla no está en la lista blanca, lanza una excepción `ValueError`.

**Nota**: El archivo no interactúa con ninguna base de datos ni utiliza variables globales.


---

## Archivo: ./graphify-out/cache/ast/e156816584b886e6a32669fc0110a876cb385245b93fa37d18b82c4f1564d64b.json

### Resumen Funcional
El archivo `test_api.py` contiene pruebas unitarias para diferentes endpoints de la API del sistema de monitoreo de almacén (WMS). Las pruebas cubren funcionalidades como el acceso a la raíz, obtención de URL de túnel, sincronización de datos, acceso a páginas analíticas y generación de consultas SQL.

### Catálogo de Funciones y Clases
- `test_read_root()` - Verifica que el endpoint raíz responda correctamente.
- `test_get_tunnel_url()` - Verifica que el endpoint `/url` devuelva la dirección del túnel ngrok.
- `test_post_sync_endpoint()` - Verifica que el endpoint de sincronización inicie el pipeline correctamente.
- `test_analytics_page_access()` - Verifica que la página de analíticas sea accesible.
- `test_build_sql_sla_efficiency()` - Verifica que el generador de consultas SQL compile correctamente la métrica SLA.
- `test_analytics_sla_route()` - Verifica que la ruta de auditoría SLA resuelva dinámicamente las áreas de negocio.
- `test_api_query_preview_returns_json_and_no_sql()` - Verifica que la consulta de vista previa devuelva JSON y no texto SQL.
- `test_api_settings_query_rejects_raw_sql()` - Verifica protección contra inyección y que el endpoint solo acepte visual_state.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno quemadas en el código.

### Dependencias y Flujo
- **Dependencias Externas**: `pytest`, `unittest_mock`
- **Archivos Importados por este Archivo**:
  - `core_state` (importado desde `tests/test_api.py`)
- **Archivos que Importan a este Archivo**: Ninguno

El flujo de datos es simple: el archivo `test_api.py` importa bibliotecas y dependencias necesarias, luego define funciones de prueba que interactúan con endpoints de la API.


---

## Archivo: ./graphify-out/cache/ast/e3289655a57b0dff9a163cda9b75334b04eb44af84af9fd502f37948163e7725.json

### Resumen Funcional
El archivo `update_kpis.py` es un script que realiza operaciones relacionadas con la actualización de indicadores clave (KPIs) en el sistema de monitoreo de almacén (WMS). No contiene ninguna interacción explícita con una base de datos ni con funciones específicas.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: `sqlite3`, `json`
  - `sqlite3`: Importada para interactuar con la base de datos SQLite.
  - `json`: Importada para manejar operaciones JSON.

- **Archivos del Proyecto que IMPORTAN a este archivo**:
  - Ninguno

- **Archivos del Proyecto que ESTE archivo IMPORTA**:
  - Ninguno

- **Flujo de Datos**: El archivo importa las librerías `sqlite3` y `json`, pero no realiza ninguna operación específica con ellas.


---

## Archivo: ./graphify-out/cache/ast/e459973c50264df86f7828c1b56f40f1a937975a6c409477e75ac0fd2c1e9c85.json

### Resumen Funcional
El archivo `watcher.py` contiene la implementación de un observador de archivos que monitorea cambios en el sistema de archivos y realiza acciones específicas cuando ocurren eventos como la creación o modificación de archivos.

### Catálogo de Funciones y Clases
- **AwaitWriteFinishHandler** - Clase principal que hereda de `FileSystemEventHandler` y maneja los eventos de archivos.
  - `__init__()`
  - `_should_track(path: str) -> bool`
  - `.on_created(event)`
  - `.on_modified(event)`
  - `_add_file(file_path: str)`
  - `_poll_files()`
  - `.stop()`

- **start_watcher()**
- **stop_watcher()**

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
**Librerías Externas:**
- `os`
- `time`
- `logging`
- `threading`
- `watchdog.observers`
- `watchdog.events`
- `config`
- `core_task_manager`
- `routes_sync`

**Flujo de Datos:**
- **Entrada:** Eventos de archivos (creación, modificación).
- **Procesamiento:** Determina si el archivo debe ser rastreado, realiza acciones según el evento.
- **Salida:** No hay salida explícita, pero se realizan acciones como la adición de archivos y la actualización del estado.

**Flujo Interno:**
- `AwaitWriteFinishHandler` hereda de `FileSystemEventHandler`.
- Los métodos de `AwaitWriteFinishHandler` manejan eventos específicos.
- `start_watcher()` e `stop_watcher()` controlan el ciclo de vida del observador.


---

## Archivo: ./graphify-out/cache/ast/e47cd6669325a7c7a307c27e8ab523c961fc4ec5a35eecbb8b60509207404cd6.json

### Resumen Funcional
El archivo `query_validators.py` contiene funciones que validan identificadores y columnas en un sistema de monitoreo de almacén (WMS) utilizando SQLAlchemy para interactuar con una base de datos SQLite.

### Catálogo de Funciones y Clases
- **validate_identifier(id: str, session: Session) -> bool** - Valida que un identificador (tabla o tabla.columna) pertenezca a la lista blanca.
- **validate_column(table_name: str, column_name: str, session: Session) -> bool** - Valida que una columna pertenezca a una tabla permitida, consultando el esquema de la base de datos.
- **get_table_columns(table_name: str, session: Session) -> List[str]** - Retorna la lista de columnas de una tabla permitida. Devuelve lista vacía si no se encuentra la tabla.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas y Columnas**:
  - Tabla `table_name` (columna `column_name`)
- **Consultas SQL Crudas o Llamadas a ORM**:
  - Uso de métodos como `execute`, `text`, `add` en consultas SQLAlchemy.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: 
  - `sqlalchemy`
  - `sqlalchemy.orm`
  - `typing`
  - `logging`
- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno
- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno

El flujo de datos es unidireccional, con `query_validators.py` importando librerías necesarias y dependiendo de funciones internas para realizar validaciones.


---

## Archivo: ./graphify-out/cache/ast/e85eb32ef10c069c6eef5a018dfdc2808ecacf1d5f2cbd56cbdf3e76445f4be3.json

### Resumen Funcional
El archivo `__init__.py` en la carpeta `core` es el punto de entrada para el módulo `monitorweb`, inicializando posiblemente las dependencias y configuraciones necesarias.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna


---

## Archivo: ./graphify-out/cache/ast/e878f13cc945dcdfa7302e48f804e0858f9de5265c3c8353486c908d91dec155.json

### Resumen Funcional
El archivo `test_cm.py` es un script que realiza operaciones de análisis y consulta en una base de datos SQLite utilizando la biblioteca SQLAlchemy, junto con pandas para el manejo de datos tabulares.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna especificada directamente. Se espera que las consultas SQL se realicen a través de SQLAlchemy.
- **Columnas**: Ninguna especificada directamente. Se espera que las consultas SQL se realicen a través de SQLAlchemy.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `pandas`: Para el manejo de datos tabulares.
- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno especificado directamente en el fragmento.
- **Archivos del Proyecto que ESTE archivo IMPORTA**:
  - `config`
  - `core_analytics_queries`

El flujo de datos es desde `test_cm.py` hacia las dependencias mencionadas, y luego hacia la base de datos SQLite a través de SQLAlchemy.


---

## Archivo: ./graphify-out/cache/ast/eb4d24dfe418cef1ec604234d00e2232517c6e34ccca76e43ce3af225fbe0b12.json

### Resumen Funcional
El archivo `macros.py` contiene una función que inyecta macros globales registradas en un string SQL proporcionado.

### Catálogo de Funciones y Clases
- `inject_macros(sql: str) -> str` - Inyecta todas las macros globales registradas en el string SQL proporcionado.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: No se mencionan dependencias externas específicas.
- **Flujo de Datos**: La función `inject_macros` toma un string SQL como parámetro, realiza una operación (reemplazo) y devuelve el string modificado.


---

## Archivo: ./graphify-out/cache/ast/eba4d9e4ac59c7b8e5eb66da74b15f2a548643403f8a4bc3e9e77de489092a44.json

### Resumen Funcional
El archivo `wrap_js.py` contiene una función que envuelve código JavaScript en un Immediately Invoked Function Expression (IIFE) y realiza operaciones de lectura, escritura y procesamiento de cadenas.

### Catálogo de Funciones y Clases
- **wrap_iife()** - Breve propósito: Envuelve el contenido del archivo `wrap_js.py` en un IIFE.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: 
  - `os`: Importada para operaciones del sistema.
  
- **Flujo de Datos**:
  - El archivo `wrap_js.py` importa el módulo `os`.
  - La función `wrap_iife()` realiza operaciones en cadenas y archivos, pero no interactúa con una base de datos.


---

## Archivo: ./graphify-out/cache/ast/f23cc18a8e0d9c04793802187c4118b71d8df4d86d0acbee63d88c685b75e5d1.json

### Resumen Funcional
El archivo `auth.py` contiene endpoints para autenticación y gestión de usuarios en un sistema de monitoreo de almacén (WMS). Incluye funciones para login, logout, obtener información del usuario, cambiar contraseña, registrar nuevos usuarios y listar todos los usuarios.

### Catálogo de Funciones y Clases
- `login(oauth2_password_request_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends())` - Autentica un usuario con username/password y retorna un JWT.
- `logout(response: Response, appstate: AppState) - Limpia la cookie de autenticación.
- `get_me(user: User = Depends(get_current_user), appstate: AppState) - Retorna la información del usuario autenticado.
- `change_password(changepasswordrequest: ChangePasswordRequest, dbsession: DBSession, user: User = Depends(get_current_user)) - Cambia la contraseña del usuario autenticado.
- `register_user(usercreate: UserCreate, dbsession: DBSession, appstate: AppState) - Crea un nuevo usuario. Solo accesible por administradores.
- `list_users(dbsession: DBSession, user: User = Depends(get_current_user), appstate: AppState) - Lista todos los usuarios del sistema.
- `login_page(request: Request, appstate: AppState) - Renderiza la página de login.

### Interacción con Base de Datos
No se especifican consultas SQL crudas o llamadas a ORM explícitas en el fragmento proporcionado. Sin embargo, las funciones que interactúan con la base de datos implican operaciones como `query`, `first`, `commit`, `add` y `flush`.

### Estado y Variables Globales
No se identifican variables globales, de sesión o de entorno quemadas en el código proporcionado.

### Dependencias y Flujo
- **Dependencias Externas**: `fastapi`, `fastapi_responses`, `fastapi_security`, `sqlalchemy_orm`.
- **Archivos Importados por este Archivo**:
  - `logging`
  - `typing`
  - `core_database`
  - `core_models_auth`
  - `core_auth`
  - `core_app_instance`
  - `core_state`
- **Archivos que Importan a este Archivo**: Ninguno.
- **Flujo de Datos**: El flujo de datos pasa por las funciones mencionadas, interactuando con la base de datos para realizar operaciones CRUD y devolviendo respuestas HTTP según los resultados.


---

## Archivo: ./graphify-out/cache/ast/f3ce044d9cbbbeb228c4c3f901b305805e328f7ff7a23f9fc986499af5d77f18.json

### Resumen Funcional
El archivo `test_mtime_precision.py` contiene pruebas unitarias para verificar la precisión de los tiempos de modificación (`mtime`) en el sistema de almacén (WMS). No se especifica un propósito más detallado.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**: Ninguna
- **Columnas**: Ninguna
- **Consultas SQL Crudas/ORM**: Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `sqlite3`: Importado para interactuar con la base de datos SQLite.
  - `pathlib`: Importado para manejar rutas de archivos.

- **Archivos del Proyecto que IMPORTAN a este archivo**: Ninguno

- **Archivos del Proyecto que ESTE archivo IMPORTA**: Ninguno

- **Dirección del Flujo de Datos**: El archivo importa las bibliotecas `sqlite3` y `pathlib`, lo que indica que estas dependencias son necesarias para su ejecución.


---

## Archivo: ./graphify-out/cache/ast/f52999a54296b96e7d25aa575def4ba07a75ef1c71d30a25a486ef66aa983973.json

### Resumen Funcional
El archivo `schemas.py` contiene definiciones de esquemas para diferentes tipos de respuestas y objetos en el sistema de monitoreo de almacén (WMS). Estos esquemas utilizan Pydantic para la validación y serialización de datos.

### Catálogo de Funciones y Clases
- `DashboardResponse` - Define el esquema para una respuesta del panel de control.
- `AnalyticsDeliveriesResponse` - Define el esquema para una respuesta de análisis de entregas.
- `AnalyticsInventoryResponse` - Define el esquema para una respuesta de análisis de inventario.
- `AnalyticsTasksResponse` - Define el esquema para una respuesta de análisis de tareas.
- `JoinDef` - Define la estructura para una definición de unión en consultas SQL.
- `FilterDef` - Define la estructura para una definición de filtro en consultas SQL.
- `MetricCondition` - Define la estructura para una condición de métrica en consultas SQL.
- `MetricDef` - Define la estructura para una definición de métrica en consultas SQL.
- `TimeAxisDef` - Define la estructura para una definición del eje temporal en consultas SQL.
- `SecondMetricDef` - Define la estructura para una segunda definición de métrica en consultas SQL.
- `VisualQueryBuilderPayload` - Define el esquema para un payload de generador visual de consultas.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias Externas**: Pydantic, typing
- **Flujo de Datos**: El archivo `schemas.py` se importa por otros archivos del proyecto que necesitan utilizar estos esquemas para la validación y serialización de datos.


---

## Archivo: ./graphify-out/cache/ast/f6d3286ac44aa7031a690381512408924043c8768a3ee8d5580c815428a7b962.json

### Resumen Funcional
El archivo `search_logs.py` es un módulo que importa el formato JSON para su uso en la aplicación de monitoreo de almacén (WMS). No contiene ninguna función o clase definida explícitamente.

### Catálogo de Funciones y Clases
Ninguna.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: Importa el formato JSON.
- **Flujo de datos**: No hay interacciones directas con archivos o bases de datos.


---

## Archivo: ./graphify-out/cache/ast/f7e524c4c2347e1dbf7e5bf20ca8294ad570d17e790156315aabb13526024d42.json

### Resumen Funcional
El archivo `__init__.py` en la carpeta `routes` es el punto de entrada para las rutas del sistema de monitoreo de almacén (WMS). No contiene ninguna lógica funcional específica, solo importaciones.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías externas**: Ninguna
- **Archivos del proyecto que IMPORTA a este archivo (lo consumen)**: Ninguno
- **Archivos del proyecto que este archivo IMPORTA**: Ninguno


---

## Archivo: ./graphify-out/cache/ast/f8a18ea70b89b9f58e13ee9fe2fffd3882fe54616a05ab3db15eff712e5011c1.json

### Resumen Funcional
El archivo `test_maintenance.py` contiene pruebas unitarias para funciones relacionadas con la gestión del mantenimiento en el sistema de monitoreo de almacén (WMS). Las pruebas cubren la funcionalidad de cierre de aplicación, generación de documentación y lógica de filtrado.

### Catálogo de Funciones y Clases
- `test_quit_app_success()` - Prueba que la función `quit_app` retorne `True` cuando el comando de sistema tiene éxito.
- `test_quit_app_failure()` - Prueba que la función `quit_app` retorne `False` cuando ocurre un error de proceso o excepción.
- `test_doc_generator_filtering_logic()` - Prueba la lógica de exclusión de archivos en el generador de documentación.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias Externas**: `pytest`, `subprocess`, `unittest.mock`
- **Archivos Importados por este Archivo**:
  - `scripts_free_ram`
  - `scripts_doc_generator`
- **Archivos que Importan a este Archivo**: Ninguno.

El flujo de datos es simple: el archivo importa las dependencias necesarias y luego define las funciones de prueba, cada una utilizando mocks y assertions para verificar el comportamiento esperado de las funciones bajo pruebas.


---

