# Documentación Técnica - Directorio: services
Compilado el: 2026-05-22 16:53:13
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./services/__init__.py

Este archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.


---

## Archivo: ./services/dashboard_service.py

### Resumen Funcional
El archivo `dashboard_service.py` contiene una clase `DashboardService` que se encarga de cargar y preparar los datos necesarios para un dashboard. Esta clase interactúa con una base de datos SQL utilizando SQLAlchemy y pandas para procesar los datos.

### Catálogo de Funciones y Clases
- **DashboardService(session: Session)** - Inicializa la instancia con una sesión de base de datos.
- **get_full_context()** - Orquesta la carga de todos los datos necesarios para el dashboard, incluyendo gráficos, KPIs, selectores y transacciones recientes.
- **_prepare_weekly_chart(year: int)** - Prepara los datos para el gráfico de intensidad semanal.
- **_calculate_dashboard_kpis(start_week: str, year_str: str)** - Calcula los indicadores clave de rendimiento (KPIs) desde una semana base.
- **_prepare_selectors(min_week: str)** - Obtiene listas únicas de fechas y áreas, además de mapeos de autores y centros.
- **_get_recent_transactions(week_str: str)** - Obtiene el listado de las últimas entregas para la tabla principal.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQL utilizando SQLAlchemy. Las tablas utilizadas son:
- `outbound_deliveries`
- `config_cost_center_mapping`
- `autor_area_mapping`

Las columnas específicas que se están leyendo o modificando incluyen:
- `week_sort`, `week_label`, `area_negocio` y otras columnas de `outbound_deliveries`.
- `business_area`, `center_code` y otras columnas de `config_cost_center_mapping`.
- `autor`, `area_negocio` y otras columnas de `autor_area_mapping`.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
Las dependencias externas utilizadas son:
- `sqlalchemy`
- `pandas`

El archivo se comunica con otros archivos del proyecto a través de la clase `DashboardService`, que es instanciada y utilizada para obtener los datos necesarios para el dashboard.


---

## Archivo: ./services/deliveries_service.py

### Resumen Funcional
El archivo `deliveries_service.py` contiene una clase `DeliveriesService` que se encarga de generar un contexto completo para las entregas, incluyendo estadísticas, KPIs y datos relacionados con áreas, autores, ubicaciones y materiales. Utiliza SQLAlchemy para interactuar con la base de datos y pandas para procesar los datos.

### Catálogo de Funciones y Clases
- `DeliveriesService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `_get_bound_params_from_visual_state(visual_state_str: str) -> list` - Extrae parámetros de un estado visual en formato JSON.
- `_extract_metric_value(df, active_year: str = None) -> Any` - Extrae el valor numérico de una métrica de un DataFrame de forma segura.
- `get_full_context() -> Dict[str, Any]` - Genera el contexto completo para Entregas.
- `_prepare_area_stats(year, month_str)` - Prepara el DataFrame de estadísticas por área.
- `_calculate_kpis(sla_df, area_stats_df, total_dias)` - Calcula el diccionario de KPIs globales de forma segura.
- `_prepare_authors(year, month_str)` - Obtiene ranking de autores con comparativa mensual.
- `_prepare_locations(year, month_str)` - Obtiene ranking de ubicaciones con comparativa mensual.
- `_prepare_materials_by_area(year, month_str)` - Estructura el ranking de materiales por cada área de negocio.

### Interacción con Base de Datos
El archivo interactúa con una base de datos utilizando SQLAlchemy. Las tablas y columnas específicas son:
- Tablas: `outbound_deliveries`, `config_queries`
- Columnas: `fecha_carga`, `sql_text`, `visual_state`, `area`, `mes`, `semana`, `autor`, `centro`, `fecha`, `valor`, `total_qty`, `efficiency`, `ontime_qty`, `late_qty`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas: `sqlalchemy`, `pandas`, `logging`, `datetime`, `typing`.
- Comunicación con otros archivos del proyecto:
  - `core.utils.sanitize_for_json`
  - `core.state.get_app_state`
  - `repositories.DeliveriesRepository`
  - `routes.inventory.get_inventory_context`
  - `routes.tasks.get_tasks_context`
  - `routes.analytics_proyecciones.get_proyecciones_context`


---

## Archivo: ./services/inventory_service.py (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
El archivo `inventory_service.py` contiene una clase `InventoryService` que proporciona métodos para calcular y preparar diversos KPIs (Indicadores Clave de Desempeño) relacionados con el inventario. Estos KPIs incluyen ingresos, consumos, traspasos, devoluciones, eficiencia de bodega, análisis ABC, estadísticas por área y tendencias de consumo planificado vs desplanificado.

### Catálogo de Funciones y Clases
- `InventoryService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
- `_get_latest_data_period()` - Obtiene el período más reciente de datos disponibles en la tabla `inventory_movements`.
- `_prepare_volume_kpis(anio, mes)` - Calcula KPIs relacionados con el volumen de movimientos de inventario.
- `_prepare_abc_analytics(anio, mes)` - Realiza análisis ABC para determinar la importancia relativa de los materiales según su consumo.
- `_prepare_area_analytics(anio, mes)` - Calcula estadísticas de consumo por área.
- `_prepare_trend_analytics(anio, mes)` - Genera tendencias de consumo a nivel semanal y mensual.
- `_prepare_user_location_analytics(anio, mes)` - Analiza la actividad de usuarios y ubicaciones según el inventario.
- `_prepare_planned_consumption_trend()` - Calcula la tendencia de consumos planificados vs desplanificados.

### Interacción con Base de Datos
- Motor: SQLite (inferred from the use of `Session` and `text`)
- Tablas:
  - `inventory_movements`
- Columnas:
  - `fe_contab`
  - `tipo_operacion`
  - `material`
  - `cmv`
  - `usuario`
  - `alm`
  - `texto_cab_documento`
  - `referencia`
  - `registrado`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sqlalchemy`
  - `pandas`
  - `logging`
  - `datetime`
  - `typing`
  - `numpy`
- Comunicación con otros archivos del proyecto:
  - `repositories.InventoryRepository` (se importa y se usa para obtener datos)
  - `core.utils.sanitize_for_json` (se importa y se usa para sanitizar datos JSON)
  - `core.state.get_app_state` (se importa pero no se usa en el fragmento proporcionado)
  - `core.wms_config.COST_CENTER_MAPPING` (se importa pero no se usa en el fragmento proporcionado)

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `inventory_service.py` contiene funciones para preparar y obtener el contexto de datos necesario para un dashboard de movimientos en una aplicación de inventario. Incluye la generación de indicadores clave (KPIs), análisis de volumen, área, ABC, usuarios, tendencias, proyecciones, mapeos detallados y gráficos planificados vs desplanificados.

### Catálogo de Funciones y Clases
- `_prepare_planned_consumption_trend()` - Prepara los datos para el gráfico de tendencia de consumo planificado.
- `_get_empty_context()` - Devuelve un contexto vacío con valores iniciales.
- `get_full_context()` - Genera el contexto completo para el dashboard de movimientos, incluyendo KPIs, análisis y mapeos.

### Interacción con Base de Datos
El archivo interactúa con una base de datos a través del repositorio `InventoryRepository`. Las tablas y columnas específicas no se mencionan explícitamente en el código proporcionado. Sin embargo, se hacen llamadas a métodos como `check_table_exists()`, `get_location_material_summary()`, `get_area_material_mapping_201()`, `get_user_material_mapping()`, `get_pm_type_material_records()` y otras que implican la lectura de datos.

### Estado y Variables Globales
No aplica. El código no define variables globales, de sesión o de entorno.

### Dependencias y Flujo
- **Librerías Externas**: No se mencionan librerías externas específicas en el fragmento proporcionado.
- **Flujo Interno**: El archivo interactúa con otros archivos del proyecto a través de llamadas como `get_proyecciones_context()` y `save_analytics_snapshot()`.


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

