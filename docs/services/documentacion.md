# Documentación Técnica - Directorio: services
Compilado el: 2026-06-05 03:03:51
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./services/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./services/dashboard_service.py

### Resumen Funcional
El archivo `dashboard_service.py` contiene la lógica del servicio para el dashboard principal de entregas en un sistema de monitoreo de almacén (WMS). El servicio delega todas las operaciones de base de datos a la clase `DeliveriesRepository`, y proporciona métodos para obtener datos necesarios para renderizar el dashboard, incluyendo gráficos de intensidad semanal, indicadores clave de rendimiento (KPIs), selectores del dashboard y transacciones recientes.

### Catálogo de Funciones y Clases
- `DashboardService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - **Parámetros**: 
    - `session`: Sesión de SQLAlchemy para interactuar con la base de datos.
  
- `get_full_context()` - Obtiene el contexto completo necesario para renderizar el dashboard.
  - **Retorno**:
    - Un diccionario que contiene gráficos de intensidad semanal, KPIs, selectores del dashboard y transacciones recientes.

### Interacción con Base de Datos
- **Motor**: SQLite (implícito a través de SQLAlchemy).
- **Tablas y Columnas**:
  - `DeliveriesRepository` interactúa con las siguientes tablas y columnas:
    - Tabla: `deliveries`
      - Columnas: Dependientes de la implementación de `get_weekly_intensity_chart`, `get_filtered_kpis`, `get_dashboard_selectors`, y `get_filtered_transactions`.
    - Tabla: `kpis`
      - Columnas: Dependientes de la implementación de `get_filtered_kpis`.
    - Tabla: `transactions`
      - Columnas: Dependientes de la implementación de `get_filtered_transactions`.

### Estado y Variables Globales
- **Ninguna**: No se utilizan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Librerías Externas**:
  - `logging`
  - `sqlalchemy.orm.Session`
  - `typing.Dict`, `typing.Any`, `typing.List`
  - `datetime.datetime`

- **Archivos del Proyecto que Importan a este Archivo (lo consumen)**:
  - Ninguna.

- **Archivos del Proyecto que Este Archivo IMPORTA (consume)**:
  - `repositories.deliveries.DeliveriesRepository`

- **Dirección del Flujo de Datos**:
  - El servicio recibe una sesión de base de datos y delega las operaciones de base de datos a `DeliveriesRepository`.
  - Los métodos de `DeliveriesRepository` interactúan con la base de datos para obtener los datos necesarios.
  - El servicio procesa estos datos y los devuelve en un formato que puede ser utilizado por la vista del dashboard.


---

## Archivo: ./services/deliveries_service.py

### Resumen Funcional
El archivo `deliveries_service.py` contiene la lógica del servicio de entregas para un sistema de monitoreo de almacén (WMS). Este servicio se encarga de generar el contexto completo para las entregas, incluyendo información sobre áreas de negocio y widgets configurados.

### Catálogo de Funciones y Clases
- `DeliveriesService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - **Propósito**: Prepara el servicio para interactuar con la base de datos proporcionada.
  
- `get_full_context() -> Dict[str, Any]` - Genera y devuelve un contexto completo para las entregas.
  - **Propósito**: Recopila y organiza información relevante desde la base de datos y otros servicios para proporcionar un contexto detallado.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `outbound_deliveries`
- **Columnas**:
  - `area_negocio`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**: 
  - `sqlalchemy.orm.Session`
  - `logging`
  - `typing.Dict`, `typing.Any`
  
- **Archivos del Proyecto que Importan a este Archivo**:
  - `routes.inventory.get_inventory_context`
  - `routes.tasks.get_tasks_context`
  - `routes.analytics_proyecciones.get_proyecciones_context`

- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno

- **Flujo de Datos**: 
  - El servicio recibe una sesión de base de datos y utiliza esta para consultar la tabla `outbound_deliveries`.
  - Luego, intenta cargar contextos adicionales desde otros servicios (`inventory`, `tasks`, `analytics_proyecciones`) y los combina en el contexto final.


---

## Archivo: ./services/inventory_service.py

### Resumen Funcional
El archivo `inventory_service.py` contiene la lógica de negocio para el servicio de inventario en un sistema de gestión de almacén (WMS). Genera un contexto completo que incluye estadísticas de eficiencia, datos históricos y otros detalles relevantes para el dashboard de movimientos.

### Catálogo de Funciones y Clases
- `InventoryService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `fmt_num(val)` - Formatea un número como una cadena con separadores de miles.
- `_get_latest_data_period()` - Obtiene el período más reciente de datos disponibles en la tabla `inventory_movements`.
- `_get_empty_context()` - Devuelve un contexto vacío con valores por defecto.
- `get_full_context()` - Genera y devuelve el contexto completo para el dashboard de movimientos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `inventory_movements`
- **Columnas:**
  - `fe_contab` (Fecha del movimiento)
  - `tipo_operacion` (Tipo de operación, ej. Ingreso/Consumo)
  - `registrado` (Fecha de registro)

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `pandas`, `numpy`
- **Archivos del Proyecto que Importan a este Archivo:**
  - `repositories.InventoryRepository`
  - `core.utils.sanitize_for_json`
  - `core.state.get_app_state`
  - `core.wms_config.COST_CENTER_MAPPING`
- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno

**Flujo de Datos:**
1. El archivo se importa y se utiliza en el servicio principal.
2. Se inicia una sesión de base de datos (`InventoryService`).
3. Se ejecutan consultas SQL para obtener los datos necesarios.
4. Los resultados son procesados y formateados usando `pandas`.
5. El contexto completo es generado y almacenado en caché.

Este archivo es crucial para el funcionamiento del sistema de monitoreo de almacén, proporcionando las estadísticas y datos necesarios para el análisis y visualización de los movimientos de inventario.


---

## Archivo: ./services/productivity_daily.py

### Resumen Funcional
El archivo `productivity_daily.py` contiene el servicio para calcular y devolver los KPIs de productividad diarios basados en las tareas asignadas. El servicio utiliza una sesión de SQLAlchemy para interactuar con la base de datos y un repositorio de tareas para obtener los datos necesarios.

### Catálogo de Funciones y Clases
- `ProductivityDailyService(session: Session)` - Inicializa el servicio con una sesión de SQLAlchemy.
  - Parámetros:
    - `session`: Sesión de SQLAlchemy para interactuar con la base de datos.
- `get_available_dates()` - Devuelve las fechas disponibles en los registros de tareas.
- `get_productivity_data(target_date: str)` - Retorna todos los KPIs de productividad para una fecha específica (YYYY-MM-DD).
  - Parámetros:
    - `target_date`: Fecha objetivo en formato YYYY-MM-DD.
  - Propósito: Calcula y devuelve los KPIs de productividad para la fecha especificada, incluyendo resúmen diario, tendencia horaria, brechas de inactividad y mapa de actividad.
- `get_user_movements_daily_summary(target_date: str, usuario: str)` - Devuelve el resumen de movimientos diarios por usuario.
  - Parámetros:
    - `target_date`: Fecha objetivo en formato YYYY-MM-DD.
    - `usuario`: Nombre del usuario.
- `get_user_movements_daily_details(target_date: str, usuario: str, operacion: str)` - Devuelve los detalles de los movimientos diarios por usuario y operación específica.
  - Parámetros:
    - `target_date`: Fecha objetivo en formato YYYY-MM-DD.
    - `usuario`: Nombre del usuario.
    - `operacion`: Tipo de operación.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas:
  - **tasks_repo.get_available_dates()**: Lee las fechas disponibles en la tabla `tasks`.
  - **tasks_repo._get_daily_summary(date_sap)**, **tasks_repo._get_hourly_trend(date_sap)**, **tasks_repo._get_inactivity_gaps(date_sap)**, **tasks_repo._get_activity_heatmap(date_sap)**: Lee datos de las tablas `tasks`, `inventory_movements`, y posiblemente otras dependiendo del contexto.
  - **tasks_repo.get_user_movements_daily_summary(target_date, usuario)**, **tasks_repo.get_user_movements_daily_details(target_date, usuario, operacion)**: Leerán datos de la tabla `tasks` y posiblemente otras tablas relacionadas.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías Externas:
  - `logging`
  - `typing`
  - `sqlalchemy.orm`
  - `re` (módulo de expresiones regulares)
- Archivos del Proyecto que Importan a este archivo (`productivity_daily.py`):
  - Ninguno
- Archivos del Proyecto que Este Archivo Importa:
  - `repositories.tasks`

**Flujo de Datos:**
1. **Entrada**: Fecha objetivo (YYYY-MM-DD).
2. **Procesamiento**:
   - Convierte la fecha al formato SAP (DD.MM.YYYY) si es necesario.
   - Llama a métodos del repositorio para obtener resúmen diario, tendencia horaria, brechas de inactividad y mapa de actividad.
3. **Salida**: Diccionario con los KPIs de productividad.

**Flujo Inverso:**
- No aplica


---

## Archivo: ./services/productivity_monthly.py

### Resumen Funcional
El archivo `productivity_monthly.py` contiene servicios para calcular y obtener datos de productividad mensuales en un sistema de almacén (WMS). Ofrece métodos para obtener resúmenes de productividad mensuales, movimientos diarios de usuarios y detalles específicos de operaciones.

### Catálogo de Funciones y Clases
- `ProductivityMonthlyService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - `get_monthly_productivity_data(target_month: str) -> Dict[str, Any]` - Calcula y devuelve los KPIs de productividad para un mes específico (YYYY-MM).
  - `get_user_movements_monthly_summary(target_month: str, usuario: str) -> list` - Obtiene el resumen de movimientos diarios de un usuario para un mes.
  - `get_user_movements_monthly_details(target_month: str, usuario: str, operacion: str) -> list` - Obtiene los detalles específicos de una operación de movimiento diario de un usuario para un mes.

### Interacción con Base de Datos
- Motor de BD: SQLite.
- Tablas y Columnas:
  - `tasks_repo._get_monthly_summary(month_sap)` - Lee datos de la tabla que contiene resúmenes mensuales de tareas.
  - `tasks_repo._get_monthly_shifts(month_sap)` - Lee datos de la tabla que contiene información sobre los turnos diarios.
  - `tasks_repo._get_monthly_heatmap(month_sap)` - Lee datos de la tabla que contiene mapas térmicos de productividad.

### Estado y Variables Globales
- Ninguna.

### Dependencias y Flujo
- Librerías externas: `logging`, `typing`.
- Archivos del proyecto que importa:
  - `repositories.tasks` - Importado en el constructor de la clase `ProductivityMonthlyService`.
- Archivos del proyecto que son importados por este archivo:
  - Ninguno.
- Flujo de datos:
  - El servicio recibe una sesión de base de datos y utiliza un repositorio para acceder a los datos necesarios. Los resultados se procesan y devuelven en formato JSON.

Este archivo es parte de la capa de servicios del sistema, donde se encapsulan las lógicas de negocio relacionadas con el cálculo y obtención de datos de productividad mensuales.


---

## Archivo: ./services/tasks_service.py

### Resumen Funcional
El archivo `tasks_service.py` contiene la lógica del servicio para gestionar y analizar las Operaciones Técnicas (OTs) en el sistema de monitoreo de almacén (WMS). Genera un contexto analítico que incluye resúmenes, tendencias, usuarios involucrados, tipos de OTs, movimientos no paletizados y KPIs dinámicos.

### Catálogo de Funciones y Clases
- `TasksService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `get_full_context()` - Genera y cachea el contexto analítico para la gestión de OTs.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: `config_queries`
    - Columnas: `sql_text`, `visual_state`, `query_id`
  - Tabla: No especificadas explícitamente, pero se usan consultas SQL crudas para leer datos.
- **Consultas SQL Crudas:** Se realizan consultas SQL para obtener resúmenes y KPIs dinámicos.

### Estado y Variables Globales
- **Variables Globales:** Ninguna.
- **Estado de Sesión:** Utiliza `get_app_state()` para acceder al estado de la aplicación, que incluye el caché.
- **Diccionarios Quemados:** Ninguno.

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `sqlalchemy`
  - `logging`
  - `datetime`
- **Archivos del Proyecto que Importa:**
  - `repositories/TasksRepository.py`
  - `core/state.py`
  - `core/utils.py`
- **Archivos del Proyecto que Son Importados por Este Archivo:**
  - Ninguno.
- **Dirección del Flujo de Datos:** El flujo de datos comienza con la solicitud de contexto, pasa a través del servicio para generar los datos necesarios y finalmente devuelve el contexto analítico.


---

## Archivo: ./services/tunnel.py

### Resumen Funcional
El archivo `tunnel.py` contiene la implementación del servicio de túnel utilizando ngrok, que se utiliza para exponer el servidor local (escuchando en el puerto 8000) a Internet. El servicio es gestionado de manera segura y thread-safe mediante un singleton.

### Catálogo de Funciones y Clases
- `NgrokService(bin_path=NGROK_BIN, tunnel_file=TUNNEL_URL_FILE)` - Inicializa el objeto del servicio de ngrok.
  - Propósito: Configura las rutas del binario de ngrok y el archivo donde se guardará la URL pública.

- `_validate_bin()` - Valida si el binario de ngrok existe y tiene permisos de ejecución.
  - Propósito: Asegura que el binario de ngrok esté disponible y accesible.

- `_save_url(url)` - Guarda la URL pública en un archivo especificado.
  - Propósito: Almacena la URL del túnel público para su uso posterior.

- `_get_public_url()` - Obtiene la URL pública del túnel a través de la API de ngrok.
  - Propósito: Recupera la URL pública del túnel desde el servidor local de ngrok.

- `start()` - Inicia el servicio de ngrok en un hilo separado.
  - Propósito: Lanza el proceso de ngrok y espera hasta que se obtenga la URL pública.

- `stop()` - Detiene el servicio de ngrok.
  - Propósito: Termina el proceso de ngrok y limpia los recursos asociados.

- `_run_loop()` - Bucle principal del servicio de ngrok.
  - Propósito: Maneja el ciclo de vida del túnel, reiniciándolo si es necesario.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa con ninguna base de datos.

### Estado y Variables Globales
- `_service_lock` - Un objeto `threading.Lock()` para proteger el acceso al servicio global.
- `_global_service` - Una variable global que almacena la instancia singleton del servicio de ngrok.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `os`, `subprocess`, `threading`, `time`, `urllib.request`, `json`, `logging`
  
- **Archivos Importados**:
  - `config.py` (para las constantes `NGROK_BIN` y `TUNNEL_URL_FILE`)
  
- **Flujo de Datos**:
  - El archivo se importa por otros archivos del proyecto para iniciar o detener el servicio de túnel.
  - Los métodos `_run_loop`, `start`, y `stop` manejan la lógica interna del servicio, mientras que las funciones `start_tunnel` y `stop_tunnel` proporcionan una interfaz segura y thread-safe para interactuar con el servicio.


---

