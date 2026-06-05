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

