# Documentación Técnica - Directorio: services
Compilado el: 2026-05-23 00:11:14
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
El archivo `deliveries_service.py` contiene una clase `DeliveriesService` que se encarga de generar un contexto completo para las entregas, incluyendo estadísticas, KPIs y datos relacionados con autores, ubicaciones y materiales. Utiliza SQLAlchemy para interactuar con la base de datos y pandas para procesar los datos.

### Catálogo de Funciones y Clases
- `DeliveriesService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `get_full_context()` - Genera el contexto completo para las entregas, incluyendo estadísticas, KPIs y datos relacionados.
- `_prepare_area_stats(year, month_str)` - Prepara el DataFrame de estadísticas por área.
- `_calculate_kpis(sla_df, area_stats_df, total_dias)` - Calcula el diccionario de KPIs globales de forma segura.
- `_prepare_authors(year, month_str)` - Obtiene ranking de autores con comparativa mensual.
- `_prepare_locations(year, month_str)` - Obtiene ranking de ubicaciones con comparativa mensual.
- `_prepare_materials_by_area(year, month_str)` - Estructura el ranking de materiales por cada área de negocio.

### Interacción con Base de Datos
El archivo interactúa con una base de datos utilizando SQLAlchemy. Las tablas y columnas específicas son:
- Tabla: `outbound_deliveries`
  - Columna: `fecha_carga`
- Tabla: `config_queries`
  - Columnas: `query_id`, `sql_text`, `visual_state`
- Tabla: `area_stats`
  - Columnas: `area`, `total_entregas`, `dias_activos`
- Tabla: `top_authors`
  - Columnas: `name`, `entregas`
- Tabla: `top_locations`
  - Columnas: `ubicacion`, `num_items`
- Tabla: `top_materials_by_area`
  - Columnas: `area`, `material`, `frequency`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
Dependencias:
- `sqlalchemy.orm.Session` - Para la sesión de base de datos.
- `pandas` - Para procesar los datos.
- `logging` - Para el registro de errores.
- `datetime` - Para manejar fechas.
- `typing` - Para tipos de datos.
- `core.utils.sanitize_for_json` - Para sanitizar datos para JSON.
- `core.state.get_app_state` - Para obtener el estado de la aplicación.
- `repositories.DeliveriesRepository` - Para interactuar con la base de datos.
- `core.query_engine.get_bound_params_from_visual_state` - Para obtener parámetros de consulta.
- `core.query_engine.extract_metric_value` - Para extraer métricas de los resultados de consulta.

Flujo:
El archivo se comunica con otros archivos del proyecto a través de las siguientes importaciones:
- `routes.inventory.get_inventory_context`
- `routes.tasks.get_tasks_context`
- `routes.analytics_proyecciones.get_proyecciones_context`

Estas funciones son llamadas para obtener contextos adicionales que se incluyen en el contexto final.


---

## Archivo: ./services/inventory_service.py (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `inventory_service.py` contiene una clase `InventoryService` que proporciona métodos para calcular y preparar diversos KPIs (Indicadores Clave de Desempeño) relacionados con el inventario, incluyendo ingresos, consumos, traspasos, devoluciones y eficiencia de bodega. Utiliza una base de datos SQL para obtener los datos necesarios.

### Catálogo de Funciones y Clases
- `InventoryService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `_get_latest_data_period()` - Obtiene el período más reciente de datos disponibles en la tabla `inventory_movements`.
- `_prepare_volume_kpis(anio, mes)` - Calcula KPIs relacionados con los volúmenes de ingresos y consumos.
- `_prepare_abc_analytics(anio, mes)` - Realiza análisis ABC para determinar el impacto de diferentes materiales en el inventario.
- `_prepare_area_analytics(anio, mes)` - Calcula estadísticas de consumo por área con promedios diarios robustos.
- `_prepare_trend_analytics(anio, mes)` - Genera tendencias de movimientos de inventario a nivel semanal y mensual.
- `_prepare_user_location_analytics(anio, mes)` - Estadísticas detalladas de usuarios y ubicaciones con actividad mensual.
- `_prepare_planned_consumption_trend()` - Calcula la tendencia de consumos planificados vs desplanificados.

### Interacción con Base de Datos
- Motor: SQLite (inferred from the use of `text` for SQL queries)
- Tablas:
  - `inventory_movements`
- Columnas:
  - `fe_contab`, `cmv`, `tipo_operacion`, `material`, `qty`, `registrado`, `usuario`, `alm`, `texto_cab_documento`, `referencia`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sqlalchemy`
  - `pandas`
  - `logging`
  - `datetime`
  - `numpy`
- Comunicación con otros archivos del proyecto:
  - `repositories.InventoryRepository` (para obtener datos de inventario)
  - `core.utils.sanitize_for_json` (para sanitizar datos para JSON)
  - `core.state.get_app_state` (no se usa en este fragmento)
  - `core.wms_config.COST_CENTER_MAPPING` (no se usa en este fragmento)

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `inventory_service.py` contiene funciones para preparar y obtener el contexto de datos necesario para un dashboard de movimientos en una aplicación de inventario. Incluye la generación de indicadores clave (KPIs), análisis de volumen, área, ABC, usuarios, tendencias y proyecciones.

### Catálogo de Funciones y Clases
- `_prepare_planned_consumption_trend()` - Prepara los datos para el gráfico de consumo planificado.
- `_get_empty_context()` - Devuelve un contexto vacío con valores iniciales.
- `get_full_context()` - Genera el contexto completo para el dashboard, incluyendo KPIs, análisis y proyecciones.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Depende de la clase `InventoryRepository` para interactuar con la base de datos.
- Comunica con el archivo `routes.analytics_proyecciones.py` para obtener contexto de proyecciones.
- Utiliza funciones como `get_app_state()`, `set_cache()`, y `save_analytics_snapshot()` que no se muestran en el fragmento.


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

