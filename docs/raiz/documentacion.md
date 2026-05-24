# Documentación Técnica - Directorio: raiz
Compilado el: 2026-05-24 00:59:57
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./app.py

### Resumen Funcional
El archivo `app.py` es el punto de entrada para la configuración y ejecución de una aplicación FastAPI. Se encarga de montar rutas, recursos estáticos y gestionar el ciclo de vida de la aplicación, incluyendo la inicialización de bases de datos y la carga de snapshots.

### Catálogo de Funciones y Clases
- `lifespan(fastapi_app: FastAPI)` - Manejador del ciclo de vida de la aplicación, que se ejecuta al iniciar y detener el servidor.
- `initialize_app(fastapi_app: FastAPI) -> None` - Configura y prepara la aplicación FastAPI.

### Interacción con Base de Datos
- Motor de BD: SQLite (implicado en las consultas SQL crudas).
- Tablas modificadas/leídas:
  - `analytics_snapshots`
- Columnas modificadas/leídas:
  - `data`

### Estado y Variables Globales
- No aplica.

### Dependencias y Flujo
- Librerías utilizadas: FastAPI, SQLAlchemy, pandas.
- Comunicación con otros archivos del proyecto:
  - `config.py`: Para configuraciones globales.
  - `core.app_instance`: Para la instancia de la aplicación FastAPI.
  - `routes.config`: Para el registro de rutas.
  - `core.auth`, `core.db_config_manager`, `core.state`, `core.task_manager`, `routes.tasks`, `services.deliveries_service`, `services.inventory_service`: Para la inicialización y gestión del estado global, tareas asíncronas y servicios.


---

## Archivo: ./config.py

### Resumen Funcional
Este archivo config.py define y gestiona las configuraciones globales del proyecto, incluyendo rutas de directorios, parámetros del servidor y variables de entorno. También realiza comprobaciones de salud en la configuración y asegura la estructura del proyecto al importar el módulo.

### Catálogo de Funciones y Clases
- `validate_config()` - Realiza comprobaciones de salud en la configuración.
- `ensure_project_structure()` - Crea los directorios necesarios para el funcionamiento de la app si no existen.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `BASE_DIR` - Directorio raíz del proyecto.
- `DB_PATH` - Ruta a la base de datos.
- `PDF_STORAGE` - Ruta para almacenar PDFs generados.
- `CLEANSED_DIR` - Ruta para archivos limpios.
- `TEMP_DIR` - Ruta para directorios temporales.
- `CACHE_DIR_NAME` - Nombre del directorio de caché.
- `CACHE_DIR` - Ruta al directorio de caché.
- `TUNNEL_URL_FILE` - Ruta al archivo que contiene la URL del túnel.
- `NGROK_BIN` - Ruta al binario de ngrok.
- `LOG_FILE` - Ruta al archivo de registro del servidor.
- `APP_HOST` - Host del servidor.
- `APP_PORT` - Puerto del servidor.
- `APP_RELOAD` - Indica si el servidor debe reiniciarse automáticamente.
- `DEFAULT_ONEDRIVE` - Ruta predeterminada a OneDrive.
- `ONEDRIVE_PATH` - Ruta a OneDrive.
- `DELIVERIES_DIR`, `STOCK_DIR`, `TASKS_DIR`, `INVENTORY_DIR` - Subdirectorios de transacciones WMS.

### Dependencias y Flujo
- Librerías utilizadas: `os`, `logging`, `typing`, `pathlib`.
- No comunica con otros archivos del proyecto.


---

## Archivo: ./main.py

### Resumen Funcional
El archivo `main.py` es el punto de entrada oficial para la aplicación MonitorWeb Analytics. Inicializa y configura los servicios necesarios, incluyendo el inicio de un túnel Ngrok para acceso remoto y el lanzamiento del servidor web utilizando Uvicorn.

### Catálogo de Funciones y Clases
- `start_application()` - Configura e inicia los servicios de la plataforma.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: `uvicorn`, `logging`
- **Flujo Interno**: El archivo se comunica con el módulo `app` para iniciar la aplicación web, con el módulo `config` para obtener configuraciones como host, puerto y modo de recarga, y con el módulo `services.tunnel` para gestionar el túnel Ngrok.


---

## Archivo: ./test_api_kpis.py

### Resumen Funcional
El archivo `test_api_kpis.py` es un script de prueba para la API que expone los KPIs. Realiza una solicitud GET a la ruta `/api/kpis` con parámetros de filtro vacíos y verifica el estado de respuesta.

### Catálogo de Funciones y Clases
- `client.get("/api/kpis?date=&entrega=&area=&centro=&has_ots_filter=")` - Realiza una solicitud GET a la API para obtener los KPIs con parámetros de filtro vacíos.
- `print(response.status_code)` - Imprime el código de estado de la respuesta.
- `if response.status_code != 200:` - Verifica si el código de estado no es 200 y, en ese caso, imprime el contenido de la respuesta.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales, de sesión o de entorno en este archivo.

### Dependencias y Flujo
- `fastapi.testclient.TestClient` - Librería utilizada para realizar solicitudes a la API FastAPI.
- Comunicación con el archivo `main.py`, que contiene la definición de la aplicación FastAPI (`app`).


---

## Archivo: ./test_both.py

### Resumen Funcional
El archivo `test_both.py` es un script de prueba que ejecuta funciones para filtrar transacciones y obtener KPIs en una área específica ("ASERRADERO"). Utiliza una sesión de base de datos para interactuar con la base de datos.

### Catálogo de Funciones y Clases
- `run()` - Ejecuta las pruebas para `filter_transactions` y `get_kpis`, imprimiendo el número de resultados obtenidos.
- `filter_transactions(request=None, area="ASERRADERO", session=SessionLocal())` - Filtra transacciones en una área específica.
- `get_kpis(area="ASERRADERO", session=SessionLocal())` - Obtiene KPIs para una área específica.

### Interacción con Base de Datos
- Motor: No especificado (se espera que `SessionLocal()` configure el motor).
- Tablas y Columnas: No se mencionan explícitamente, pero se asume que interactúa con tablas relacionadas con transacciones y KPIs.
- Consultas SQL Crudas o ORM: Se espera que las funciones `filter_transactions` y `get_kpis` utilicen consultas SQL o ORM para acceder a la base de datos.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías Externas:
  - `asyncio`
  - `sys`
- Comunicación con otros archivos del proyecto:
  - Importa funciones desde `core.database` y `routes.filters`.

El script se ejecuta directamente si es el archivo principal, iniciando una sesión de base de datos y ejecutando las pruebas asincrónicas para filtrar transacciones y obtener KPIs.


---

## Archivo: ./test_braces.py

### Resumen Funcional
El archivo `test_braces.py` realiza una verificación básica de los paréntesis `{}` en un archivo JavaScript (`dashboard.js`). Ignora los comentarios y verifica que todos los paréntesis abiertos tengan su correspondiente cierre.

### Catálogo de Funciones y Clases
- `main()` - No se define explícitamente, pero el código principal está dentro del bloque `if __name__ == "__main__":`.

### Interacción con Base de Datos
No aplica. El archivo no interactúa con ninguna base de datos.

### Estado y Variables Globales
- `text` - Almacena el contenido del archivo `dashboard.js`.
- `stack` - Una lista que almacena las posiciones de los paréntesis `{` sin cierre.
- `lines` - Lista de líneas del archivo `dashboard.js`.

### Dependencias y Flujo
- `re` - Librería estándar de Python para operaciones regulares (no utilizada en este fragmento).
- El código se comunica con el archivo `dashboard.js` ubicado en la ruta `static/js/dashboard.js`.


---

## Archivo: ./test_browser.js

### Resumen Funcional
El archivo `test_browser.js` es un script que automatiza el lanzamiento de un servidor Python en segundo plano y luego utiliza Playwright para abrir un navegador Chromium, navegar a una página web local, desmarcar un checkbox y cerrar el navegador.

### Catálogo de Funciones y Clases
- `main()` - Función principal que coordina la ejecución del script.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con bases de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- `playwright` - Librería utilizada para controlar el navegador Chromium.
- `child_process` - Módulo Node.js utilizado para ejecutar comandos del sistema operativo (lanzar el servidor Python).
- El script se comunica con otros archivos del proyecto a través de la ejecución del comando `python3 main.py`, lo que implica que debe haber un archivo `main.py` en el mismo directorio o en una ruta relativa.


---

## Archivo: ./test_deliveries.py

### Resumen Funcional
El archivo `test_deliveries.py` es un script de prueba que interactúa con una base de datos para obtener y mostrar el contexto completo de entregas.

### Catálogo de Funciones y Clases
- `svc.get_full_context()` - Obtiene el contexto completo de entregas.

### Interacción con Base de Datos
- **Motor:** No especificado.
- **Tablas:** No aplica.
- **Columnas:** No aplica.
- **Consultas SQL Crudas/ORM:** Sí, utiliza `DeliveriesService` que probablemente realiza consultas a la base de datos.

### Estado y Variables Globales
- `db` - Variable global que almacena una instancia de la sesión de la base de datos.

### Dependencias y Flujo
- **Librerías Externas:** `sys`, `logging`.
- **Flujo Interno:** El script crea una instancia de `DeliveriesService`, obtiene el contexto completo de entregas, e imprime las claves del contexto. Si ocurre un error, se imprime la traza de excepción.

### Notas Adicionales
El archivo no realiza ninguna interacción directa con tablas o columnas específicas en la base de datos; en su lugar, utiliza un servicio para obtener el contexto completo de entregas.


---

## Archivo: ./test_filter.py

### Resumen Funcional
El archivo `test_filter.py` es un script de prueba que ejecuta una función para filtrar transacciones en la base de datos y muestra los resultados.

### Catálogo de Funciones y Clases
- `run()` - Ejecuta la función `filter_transactions` con parámetros específicos y maneja la sesión de la base de datos.

### Interacción con Base de Datos
- Motor: No aplica (el archivo no interactúa directamente con una base de datos).
- Tablas y Columnas: No aplica (no hay consultas SQL ni interacciones con tablas).

### Estado y Variables Globales
- No aplica (no se definen variables globales, de sesión o diccionarios quemados en el código).

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sys` - Para manipular los parámetros del sistema.
  - `asyncio` - Para manejar la ejecución asíncrona.
- Comunicación con otros archivos:
  - Importa `SessionLocal` desde `core.database`.
  - Importa `filter_transactions` desde `routes.filters`.


---

## Archivo: ./test_kpis.py

### Resumen Funcional
El archivo `test_kpis.py` es un script que ejecuta una función para obtener KPIs (Indicadores Clave de Desempeño) utilizando una sesión de base de datos y luego imprime los resultados.

### Catálogo de Funciones y Clases
- `run()` - Asincrónica, inicia una sesión de base de datos, ejecuta la función `get_kpis` para obtener KPIs, e imprime el resultado o cualquier error que ocurra.

### Interacción con Base de Datos
- Motor: SQLAlchemy (implícito a través de `SessionLocal`)
- Tablas y Columnas: No se especifican explícitamente en el fragmento proporcionado.
- Consultas SQL Crudas/ORM: Se hace uso de una función llamada `get_kpis` que probablemente realiza consultas ORM para obtener los KPIs.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías Externas:
  - `asyncio`
  - `sqlalchemy`
- Comunicación con otros archivos del proyecto:
  - Importa `SessionLocal` desde `core.database`
  - Importa `get_kpis` desde `routes.filters`

Este archivo es un ejemplo de cómo se pueden realizar pruebas asincrónicas para obtener y mostrar datos utilizando una base de datos a través de SQLAlchemy.


---

## Archivo: ./test_widget.py

### Resumen Funcional
El archivo `test_widget.py` realiza una consulta SQL a partir de un payload JSON, construye la consulta utilizando el motor de consultas y luego ejecuta la consulta para obtener categorías únicas.

### Catálogo de Funciones y Clases
- `get_session()` - Obtiene una sesión de base de datos.
- `ConfigQuery.filter_by(query_id='vl_sla_area_monthly_trend').first()` - Filtra y obtiene el primer registro de la tabla `ConfigQuery` con el ID especificado.
- `json.loads(q.visual_state)` - Convierte el JSON almacenado en `visual_state` a un diccionario.
- `VisualQueryBuilderPayload(**vs_dict)` - Crea una instancia de `VisualQueryBuilderPayload` a partir del diccionario.
- `build_sql_from_payload(payload, session)` - Construye la consulta SQL y los parámetros a partir del payload y la sesión.
- `_build_unified_where('', 'ASERRADERO', '', '', None)` - Construye una cláusula WHERE unificada.
- `pd.read_sql(text(sql), session.connection(), params=params_dict)['categoria'].unique()` - Ejecuta la consulta SQL y obtiene las categorías únicas.

### Interacción con Base de Datos
- Motor: No especificado (se infiere que es SQLAlchemy).
- Tablas: `ConfigQuery`
- Columnas: `query_id`, `visual_state`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `json` - Para manejar JSON.
  - `pandas` - Para procesar datos.
  - `sqlalchemy` - Para interactuar con la base de datos.
- Comunicación con otros archivos del proyecto:
  - `core.database.get_session()` - Obtiene una sesión de base de datos.
  - `core.models.ConfigQuery` - Define el modelo para la tabla `ConfigQuery`.
  - `core.schemas.VisualQueryBuilderPayload` - Define el esquema para el payload.
  - `core.query_engine.build_sql_from_payload(payload, session)` - Construye la consulta SQL y los parámetros.
  - `routes.filters._build_unified_where('', 'ASERRADERO', '', '', None)` - Construye una cláusula WHERE unificada.
  - `repositories.deliveries.DeliveriesRepository.AREA_EXPR` - Accede a una expresión definida en el repositorio de entregas.


---

