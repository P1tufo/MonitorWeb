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

