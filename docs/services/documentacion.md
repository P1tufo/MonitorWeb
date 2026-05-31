# Documentación Técnica - Directorio: services
Compilado el: 2026-05-30 00:23:08
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./services/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./services/dashboard_service.py

### Resumen Funcional
Este archivo contiene el servicio `DashboardService` que se encarga de cargar la página principal del dashboard. Orquesta la carga de todos los datos necesarios para el dashboard, incluyendo gráficos, indicadores clave de rendimiento (KPIs) y listas únicas de fechas y áreas.

### Catálogo de Funciones y Clases
- `DashboardService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `get_full_context()` - Orquesta la carga de todos los datos necesarios para el dashboard.
- `_prepare_weekly_chart(year: int)` - Prepara los datos para el gráfico de intensidad semanal.
- `_calculate_dashboard_kpis(start_week: str, year_str: str)` - Calcula los indicadores clave de rendimiento (KPIs) desde una semana base.
- `_prepare_selectors(min_week: str)` - Obtiene listas únicas de fechas y áreas, además de mapeos de autores y centros.
- `_get_recent_transactions(week_str: str)` - Obtiene el listado de las últimas entregas para la tabla principal.

### Interacción con Base de Datos
- Motor: SQLite (inferred from `pd.read_sql`)
- Tablas:
  - `outbound_deliveries`
  - `config_cost_center_mapping`
  - `autor_area_mapping`
- Columnas:
  - `outbound_deliveries`: `week_sort`, `week_label`, `area_negocio`, `entrega`, `material`, `estado_wms`, `dias_retraso`, `fecha_carga`, `fecha_sm_real`, `creado_el`
  - `config_cost_center_mapping`: `center_code`, `business_area`
  - `autor_area_mapping`: `autor`, `area_negocio`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `logging`
  - `sqlalchemy.orm.Session`
  - `pandas as pd`
  - `itertools`
  - `typing`
  - `datetime`
- No comunica con otros archivos del proyecto directamente.


---

## Archivo: ./services/deliveries_service.py

### Resumen Funcional
El archivo `deliveries_service.py` contiene una clase `DeliveriesService` que se encarga de generar un contexto completo para las entregas en un sistema SaaS. Este contexto incluye información sobre widgets, áreas de negocio, y otros datos relevantes.

### Catálogo de Funciones y Clases
- **DeliveriesService(session: Session)** - Inicializa el servicio con una sesión de base de datos.
- **get_full_context() -> Dict[str, Any]** - Genera un contexto completo para las entregas, incluyendo widgets, áreas de negocio, y otros datos.

### Interacción con Base de Datos
- **Motor:** SQLite (deducido del uso de `Session` de SQLAlchemy).
- **Tablas:** `outbound_deliveries`.
- **Columnas:** `area_negocio`.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- **Librerías Externas:** `sqlalchemy`, `logging`, `typing`.
- **Flujo Interno:** El servicio depende de funciones externas definidas en otros archivos (`routes.inventory.get_inventory_context`, `routes.tasks.get_tasks_context`, `routes.analytics_proyecciones.get_proyecciones_context`).


---

## Archivo: ./services/inventory_service.py

### Resumen Funcional
El archivo `inventory_service.py` contiene la lógica del servicio de inventario, que se encarga de generar el contexto necesario para un dashboard de movimientos en una aplicación SaaS. El servicio interactúa con una base de datos SQL y utiliza ORM SQLAlchemy.

### Catálogo de Funciones y Clases
- **InventoryService(session: Session)** - Inicializa el servicio con una sesión de base de datos.
- **fmt_num(val)** - Formatea un número para mostrarlo como una cadena con separadores de miles.
- **_get_latest_data_period()** - Obtiene el período más reciente de datos disponibles en la tabla `inventory_movements`.
- **_get_empty_context()** - Devuelve un contexto vacío con valores por defecto.
- **get_full_context()** - Genera el contexto completo para el dashboard, incluyendo el período más reciente y otros datos relevantes.

### Interacción con Base de Datos
- **Motor**: SQLAlchemy ORM
- **Tablas**: `inventory_movements`
- **Columnas**: `fe_contab`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: `sqlalchemy`, `pandas`, `logging`, `datetime`, `typing`
- **Flujo Interno**: El servicio interactúa con el repositorio de inventario para verificar la existencia de la tabla, obtiene el período más reciente de datos y genera un contexto completo.


---

## Archivo: ./services/productivity_service.py

### Resumen Funcional
El archivo `productivity_service.py` contiene una clase `ProductivityService` que proporciona métodos para obtener datos de productividad, incluyendo fechas disponibles, KPIs diarios, horarios de tendencia, huecos de inactividad y mapas de actividad. Estos datos se obtienen a partir de dos tablas: `inventory_movements` y `warehouse_tasks`.

### Catálogo de Funciones y Clases
- **ProductivityService(session: Session)** - Inicializa el servicio con una sesión de base de datos.
- **get_available_dates()** - Devuelve una lista ordenada de fechas únicas (YYYY-MM-DD) que tienen movimientos generados o confirmados.
- **get_productivity_data(target_date: str)** - Retorna todos los KPIs de productividad para una fecha específica.
- **_get_daily_summary(date_sap: str)** - Calcula el resumen diario de actividad.
- **_get_hourly_trend(date_sap: str)** - Calcula la tendencia horaria de actividad.
- **_get_inactivity_gaps(date_sap: str)** - Identifica los huecos de inactividad en la actividad.
- **_get_activity_heatmap(date_sap: str)** - Genera un mapa de actividad basado en franjas horarias.
- **get_monthly_productivity_data(target_month: str)** - Retorna todos los KPIs de productividad para un mes específico.
- **_get_monthly_summary(month_sap: str)** - Calcula el resumen mensual de actividad.
- **_get_monthly_shifts(month_sap: str)** - Identifica las horas de trabajo por turno en un mes.
- **_get_monthly_heatmap(month_sap: str)** - Genera un mapa de actividad basado en días de la semana.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQL utilizando SQLAlchemy. Las tablas involucradas son:
- `inventory_movements`
  - Columnas utilizadas: `registrado`, `hora`, `usuario`, `doc_mat`
- `warehouse_tasks`
  - Columnas utilizadas: `fecha_conf`, `hor_conf`, `usuario_conf`, `numero_ot`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
Dependencias:
- `logging` - Para el registro de errores.
- `pandas` - Para la manipulación de datos.
- `sqlalchemy.orm.Session` - Para la gestión de sesiones de base de datos.
- `sqlalchemy.text` - Para ejecutar consultas SQL.

Flujo interno:
- La clase `ProductivityService` se comunica con el archivo principal del proyecto a través de sus métodos públicos, que realizan consultas a las tablas mencionadas y devuelven los resultados procesados.


---

## Archivo: ./services/tasks_service.py

### Resumen Funcional
El archivo `tasks_service.py` contiene una clase `TasksService` que se encarga de generar y cachear el contexto analítico para la gestión de Operaciones Técnicas (OTs). Este contexto incluye datos resumidos, tendencias, usuarios, tipos de almacenamiento, movimientos no paletizados y KPIs dinámicos.

### Catálogo de Funciones y Clases
- `TasksService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `get_full_context() -> dict` - Genera y cachea el contexto analítico para la gestión de OTs.

### Interacción con Base de Datos
- **Motor:** SQLAlchemy
- **Tablas:** No aplica (se asume que las consultas SQL son ejecutadas directamente contra una base de datos compatible con SQLAlchemy).
- **Columnas:** No aplica (se asume que las consultas SQL son ejecutadas directamente contra una base de datos compatible con SQLAlchemy).

### Estado y Variables Globales
- `state` - Almacena el estado de la aplicación, utilizado para cachear el contexto analítico.

### Dependencias y Flujo
- **Librerías Externas:** 
  - `sqlalchemy`
  - `pandas`
  - `logging`
  - `datetime`
- **Flujo Interno:**
  - La clase `TasksService` depende de la sesión de base de datos para interactuar con el repositorio `TasksRepository`.
  - Utiliza funciones auxiliares como `_get_bound_params_from_visual_state`, `_extract_metric_value` y `sanitize_for_json` definidas en otros módulos (`core.utils`).
  - La clase no depende directamente de archivos específicos del proyecto, sino que interactúa con el repositorio para obtener datos y ejecuta consultas SQL dinámicas.


---

## Archivo: ./services/tunnel.py

### Resumen Funcional
El archivo `tunnel.py` define un servicio para iniciar y gestionar un túnel público utilizando el software ngrok. El servicio se ejecuta en un hilo separado y maneja la creación, reinicio y detención del túnel, guardando la URL pública generada en un archivo.

### Catálogo de Funciones y Clases
- `NgrokService(bin_path=NGROK_BIN, tunnel_file=TUNNEL_URL_FILE)` - Inicializa el servicio con el camino al binario de ngrok y el archivo donde se guarda la URL del túnel.
  - `_validate_bin()` - Valida si el binario de ngrok existe y tiene permisos de ejecución.
  - `_save_url(url)` - Guarda la URL del túnel en un archivo y establece los permisos adecuados.
  - `_get_public_url()` - Obtiene la URL pública del túnel a través de la API de ngrok.
  - `start()` - Inicia el servicio en un hilo separado.
  - `stop()` - Detiene el proceso del túnel y limpia los recursos.
  - `_run_loop()` - Bucle principal que gestiona la creación y reinicio del túnel.

- `start_tunnel()` - Función para iniciar el servicio de túnel de forma segura y thread-safe.
- `stop_tunnel()` - Función para detener el servicio de túnel de forma segura y thread-safe.

### Interacción con Base de Datos
No aplica. El archivo no interactúa con ninguna base de datos.

### Estado y Variables Globales
- `_service_lock` - Lock para proteger el acceso al servicio global.
- `_global_service` - Variable global que almacena la instancia del servicio de túnel.

### Dependencias y Flujo
- `os`, `subprocess`, `threading`, `time`, `urllib.request`, `json`, `logging`: Librerías estándar de Python utilizadas para el manejo de procesos, hilos, tiempo, red, logging, etc.
- `config.py`: Archivo que contiene las configuraciones globales del proyecto, específicamente los caminos al binario de ngrok y al archivo donde se guarda la URL del túnel.


---

