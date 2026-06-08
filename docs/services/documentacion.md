# Documentación Técnica - Directorio: services
Compilado el: 2026-06-07 18:34:58
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./services/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./services/background_tasks.py

### Resumen Funcional
El archivo `background_tasks.py` contiene una tarea de fondo que se encarga de refrescar las analíticas del sistema. Esta tarea ejecuta métodos de los servicios de entregas y inventario para recalcular su contexto completo.

### Catálogo de Funciones y Clases
- `refresh_analytics()` - Refresca las analíticas (ejecutado como tarea de fondo trazable).

### Interacción con Base de Datos
- Motor: SQLite
- Tablas modificadas:
  - Ninguna (se supone que los métodos llamados internamente interactúan directamente con la base de datos).
- Consultas SQL crudas o llamadas a ORM: Sí, se usan métodos de `DeliveriesService` y `InventoryService`, que probablemente contienen consultas SQL o llamadas a ORM.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `logging`
- Archivos del proyecto que importan a este archivo (`background_tasks.py`):
  - Ninguno
- Archivos del proyecto que este archivo importa (`background_tasks.py`):
  - `core.database.get_session`
  - `routes.tasks.get_tasks_context`
  - `services.deliveries_service.DeliveriesService`
  - `services.inventory_service.InventoryService`

**Flujo de datos:**
1. `refresh_analytics()` se ejecuta.
2. Se obtiene una sesión de base de datos usando `get_session()`.
3. Se crea una instancia de `DeliveriesService` y se llama a su método `get_full_context()`, que probablemente realiza consultas a la base de datos para recalcular el contexto de las entregas.
4. Se crea una instancia de `InventoryService` y se llama a su método `get_full_context()`, que probablemente realiza consultas a la base de datos para recalcular el contexto del inventario.
5. Se llama a `get_tasks_context(session)`, que también probablemente realiza consultas a la base de datos.
6. Si ocurre un error, se registra con nivel de error en el logger.

Este flujo asegura que todas las operaciones relacionadas con el refresco de analíticas interactúen directamente con la base de datos a través de los servicios correspondientes.


---

## Archivo: ./services/dashboard_service.py

### Resumen Funcional
El archivo `dashboard_service.py` contiene la lógica del servicio para el dashboard principal de entregas en un sistema de monitoreo de almacén (WMS). El servicio se encarga de obtener y formatear datos necesarios para mostrar en el dashboard, incluyendo gráficos de intensidad semanal, indicadores clave de rendimiento (KPIs), selectores y transacciones recientes.

### Catálogo de Funciones y Clases
- `DashboardService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - **Propósito**: Configura la instancia del servicio para interactuar con la base de datos a través del repositorio `DashboardRepository`.

- `get_full_context()` - Obtiene y formatea los datos necesarios para el contexto del dashboard.
  - **Propósito**: Recupera gráficos de intensidad semanal, KPIs filtrados, selectores y transacciones recientes, y los devuelve en un formato adecuado para la vista.

### Interacción con Base de Datos
- **Motor de BD**: SQLite
- **Tablas y Columnas**:
  - `get_weekly_intensity_chart(iso_year)` - Recupera datos para el gráfico de intensidad semanal.
    - Tabla: No especificada (implícita en la consulta SQL).
    - Columnas: No especificadas (implícitas en la consulta SQL).

  - `get_filtered_kpis(None, None, None, min_week, iso_year)` - Recupera KPIs filtrados por semana y año.
    - Tabla: No especificada (implícita en la consulta SQL).
    - Columnas: No especificadas (implícitas en la consulta SQL).

  - `get_dashboard_selectors(min_week)` - Recupera selectores para el dashboard.
    - Tabla: No especificada (implícita en la consulta SQL).
    - Columnas: No especificadas (implícitas en la consulta SQL).

  - `get_filtered_transactions(None, None, None, None, None, min_week)` - Recupera transacciones recientes filtradas por semana.
    - Tabla: No especificada (implícita en la consulta SQL).
    - Columnas: No especificadas (implícitas en la consulta SQL).

### Estado y Variables Globales
- **Variables Globales**: Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `logging`
  - `datetime`
  - `typing`

- **Archivos del Proyecto que Importan a este Archivo (lo consumen)**: Ninguno

- **Archivos del Proyecto que Este Archivo Importa (consume)**:
  - `repositories.dashboard.DashboardRepository`

- **Dirección del Flujo de Datos**:
  - El servicio recibe una sesión de base de datos y utiliza el repositorio para obtener los datos necesarios.
  - Los datos obtenidos se formatean y devuelven en un diccionario que representa el contexto completo del dashboard.


---

## Archivo: ./services/deliveries_service.py

### Resumen Funcional
El archivo `deliveries_service.py` contiene la lógica de negocio para el servicio de entregas en un sistema de monitoreo de almacén (WMS). Este servicio se encarga de generar un contexto completo con metadatos ligeros, incluyendo áreas de negocio y widgets configurados.

### Catálogo de Funciones y Clases
- `DeliveriesService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - **Propósito**: Prepara el servicio para interactuar con la base de datos proporcionada.
  
- `get_full_context()` - Genera un contexto completo con metadatos ligeros.
  - **Propósito**: Recopila y devuelve información relevante como áreas de negocio, widgets configurados, y otros datos necesarios para el monitoreo del almacén.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `outbound_deliveries`
- **Columnas**:
  - `area_negocio`

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: 
  - `logging`, `typing`, `sqlalchemy.orm`
  
- **Archivos del Proyecto que Importan a este Archivo**:
  - `routes.analytics_proyecciones.get_proyecciones_context()`
  - `routes.inventory.get_inventory_context()`
  - `routes.tasks.get_tasks_context()`

- **Archivos del Proyecto que Este Archivo Importa**:
  - `core.cache_decorator.analytics_cache`
  - `core.models.ConfigQuery`
  
- **Dirección del Flujo de Datos**: 
  - El archivo importa funciones desde otros archivos y utiliza la sesión de base de datos para consultar información.


---

## Archivo: ./services/inventory_service.py

### Resumen Funcional
El archivo `inventory_service.py` contiene la lógica de negocio para el servicio de inventario en un sistema de gestión de almacén (WMS). Define una clase `InventoryService` que interactúa con la base de datos para obtener y procesar datos de movimientos de inventario, calculando estadísticas de eficiencia y generando un contexto completo para el dashboard.

### Catálogo de Funciones y Clases
- **Clase: InventoryService**
  - **Método:** `__init__(self, session: Session)`
    - **Propósito:** Inicializa la instancia con una sesión de base de datos.
  
  - **Método:** `fmt_num(self, val)`
    - **Propósito:** Formatea un número para mostrarlo como una cadena con separadores de miles y decimales.

  - **Método:** `_get_latest_data_period(self) -> Tuple[str, str]`
    - **Propósito:** Obtiene el período más reciente de datos disponibles en la base de datos.

  - **Método:** `_get_empty_context(self) -> Dict[str, Any]`
    - **Propósito:** Devuelve un contexto vacío con valores por defecto para las estadísticas y métricas del inventario.

  - **Método:** `get_full_context(self) -> Dict[str, Any]`
    - **Propósito:** Genera el contexto completo para el dashboard de Movimientos (Fase 3: SaaS), incluyendo estadísticas de eficiencia y datos históricos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `inventory_movements`
- **Columnas:** 
  - `fe_contab` (Fecha del movimiento)
  - `tipo_operacion` (Tipo de operación: Ingreso/Consumo)
  - `registrado` (Fecha de registro)

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:** 
  - `pandas`
  - `numpy`
  - `sqlalchemy`

- **Archivos del Proyecto que Importan a este Archivo:**
  - `repositories.InventoryRepository`

- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.cache_decorator.analytics_cache`
  - `core.state.get_cache_manager`
  - `core.utils.sanitize_for_json`
  - `core.wms_config.COST_CENTER_MAPPING`
  - `repositories.InventoryRepository`

**Flujo de Datos:** 
1. El archivo se importa por otros archivos del proyecto.
2. Se crea una instancia de `InventoryService` pasando una sesión de base de datos.
3. Llama al método `get_full_context()` para generar el contexto completo.
4. Este método interactúa con la base de datos para obtener y procesar los datos necesarios.
5. Los resultados se almacenan en caché para mejorar el rendimiento.

Este archivo es crucial para el funcionamiento del sistema de gestión de inventario, proporcionando las estadísticas y datos necesarios para el dashboard de Movimientos.


---

## Archivo: ./services/productivity_daily.py

### Resumen Funcional
El archivo `productivity_daily.py` contiene el servicio para gestionar los datos de productividad diaria en un sistema de almacén (WMS). Ofrece métodos para obtener fechas disponibles, datos de productividad por fecha específica y detalles de movimientos diarios de usuarios.

### Catálogo de Funciones y Clases
- `ProductivityDailyService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - `get_available_dates()` - Retorna las fechas disponibles para los KPIs de productividad.
  - `get_productivity_data(target_date: str) -> Dict[str, Any]` - Obtiene todos los KPIs de productividad para una fecha específica (YYYY-MM-DD).
  - `get_user_movements_daily_summary(target_date: str, usuario: str) -> list` - Retorna el resumen diario de movimientos de un usuario.
  - `get_user_movements_daily_details(target_date: str, usuario: str, operacion: str) -> list` - Retorna los detalles diarios de movimientos de un usuario para una operación específica.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas y Columnas:
  - `get_available_dates()`: No especifica consultas directas.
  - `get_productivity_data(target_date: str)`: Llama a `_get_daily_summary`, `_get_hourly_trend`, `_get_inactivity_gaps`, y `_get_activity_heatmap` en `ProductivityRepository`.
    - `_get_daily_summary(date_sap)`
    - `_get_hourly_trend(date_sap)`
    - `_get_inactivity_gaps(date_sap)`
    - `_get_activity_heatmap(date_sap)`
  - `get_user_movements_daily_summary(target_date: str, usuario: str)`: Llama a `get_user_movements_daily_summary` en `ProductivityRepository`.
  - `get_user_movements_daily_details(target_date: str, usuario: str, operacion: str)`: Llama a `get_user_movements_daily_details` en `ProductivityRepository`.

### Estado y Variables Globales
- No hay variables globales declaradas.

### Dependencias y Flujo
- Librerías externas:
  - `logging`
  - `typing`
  - `re` (módulo estándar de Python)
- Archivos del proyecto que importan a este archivo (`productivity_daily.py`):
  - Ninguna.
- Archivos del proyecto que este archivo importa (`productivity_daily.py`):
  - `repositories.productivity.ProductivityRepository`
- Flujo de datos:
  - El servicio recibe una sesión de base de datos y utiliza un repositorio para interactuar con la BD.
  - Los métodos devuelven datos estructurados en formato JSON.


---

## Archivo: ./services/productivity_monthly.py

### Resumen Funcional
El archivo `productivity_monthly.py` contiene servicios para calcular y obtener datos de productividad mensuales en un sistema de almacén (WMS). Ofrece métodos para obtener resúmenes y detalles de movimientos de usuarios por mes.

### Catálogo de Funciones y Clases
- `ProductivityMonthlyService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - `get_monthly_productivity_data(target_month: str) -> Dict[str, Any]` - Calcula y devuelve los KPIs de productividad para un mes específico (YYYY-MM).
  - `get_user_movements_monthly_summary(target_month: str, usuario: str) -> list` - Obtiene el resumen de movimientos mensuales por usuario.
  - `get_user_movements_monthly_details(target_month: str, usuario: str, operacion: str) -> list` - Obtiene los detalles de movimientos mensuales por usuario y operación.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - Ninguna (se asume que las consultas SQL están definidas en el repositorio `ProductivityRepository`)
- Consultas SQL Crudas o ORM:
  - `_get_monthly_summary(month_sap)`
  - `_get_monthly_shifts(month_sap)`
  - `_get_monthly_heatmap(month_sap)`
  - `get_user_movements_monthly_summary(target_month, usuario)`
  - `get_user_movements_monthly_details(target_month, usuario, operacion)`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías Externas:
  - `logging`
  - `typing`
  - `sqlalchemy.orm.Session`
- Archivos del Proyecto que Importan a este Archivo (lo Consumen):
  - Ninguno
- Archivos del Proyecto que Este Archivo Importa (consume):
  - `repositories.productivity.ProductivityRepository`

**Flujo de Datos:**
1. El servicio `ProductivityMonthlyService` se inicializa con una sesión de base de datos.
2. Los métodos `get_monthly_productivity_data`, `get_user_movements_monthly_summary`, y `get_user_movements_monthly_details` llaman a los métodos correspondientes del repositorio `ProductivityRepository`.
3. El repositorio ejecuta consultas SQL para obtener los datos de productividad y movimientos.
4. Los resultados se procesan y devuelven al servicio, que finalmente los devuelve al cliente.


---

## Archivo: ./services/tasks_service.py

### Resumen Funcional
El archivo `tasks_service.py` contiene la lógica del servicio para generar el contexto analítico para la gestión de Operaciones Técnicas (OTs) en un sistema de monitoreo de almacén (WMS). Este servicio utiliza SQLAlchemy para interactuar con una base de datos SQLite y pandas para procesar los datos.

### Catálogo de Funciones y Clases
- `TasksService(session: Session)` - Inicializa el servicio con una sesión de la base de datos.
  - **Propósito**: Proporciona métodos para obtener diferentes conjuntos de datos relacionados con las OTs.

- `get_full_context()` - Genera el contexto analítico para la gestión de OTs.
  - **Propósito**: Recopila y procesa datos desde múltiples fuentes (tablas de la base de datos, consultas dinámicas) para generar un diccionario con información relevante.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `config_queries` - Almacena consultas y estados visuales configurados.
- **Columnas**:
  - `sql_text` - Texto de la consulta SQL.
  - `visual_state` - Estado visual de la consulta.
  - `query_id` - Identificador único de la consulta.

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `pandas`
  - `sqlalchemy`
  - `logging`
  - `datetime`

- **Archivos del Proyecto que Importa a este Archivo (lo consumen)**:
  - `repositories/TasksRepository.py` - Para acceder a los datos de las OTs.

- **Archivos del Proyecto que Este Archivo IMPORTA**:
  - `core/cache_decorator.py`
  - `core/state.py`
  - `core/utils.py`

- **Dirección del Flujo de Datos**:
  - Desde el servicio (`TasksService`) se obtienen datos desde la base de datos y las tablas configuradas.
  - Los datos son procesados y transformados en un formato adecuado para su visualización o análisis.
  - El resultado final es un diccionario que contiene los datos procesados, que luego puede ser utilizado por otras partes del sistema.


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

- `_run_loop()` - Bucle principal del servicio de ngrok, encargado de iniciar y gestionar el túnel.
  - Propósito: Maneja la creación y reinicio del túnel hasta que se solicite su detención.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `_service_lock` - Lock para proteger el acceso al servicio global.
- `_global_service` - Variable global que almacena la instancia singleton del servicio de ngrok.

### Dependencias y Flujo
- **Librerías Externas**: `json`, `logging`, `os`, `subprocess`, `threading`, `time`, `urllib.request`.
- **Archivos Importados**: `config.py` (para constantes como `NGROK_BIN` y `TUNNEL_URL_FILE`).
- **Flujo de Datos**:
  - El archivo se importa por otros módulos para iniciar o detener el servicio de túnel.
  - Los métodos `_run_loop`, `start`, y `stop` manejan la creación, reinicio y finalización del proceso de ngrok en un hilo separado.


---

