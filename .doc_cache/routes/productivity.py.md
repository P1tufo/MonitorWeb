## Archivo: ./routes/productivity.py

### Resumen Funcional
Este archivo contiene endpoints para obtener datos de productividad, incluyendo fechas disponibles, un resumen diario y KPIs mensuales. Utiliza FastAPI para definir las rutas y SQLAlchemy para interactuar con la base de datos.

### Catálogo de Funciones y Clases
- `get_available_dates(user: User, session: Session)` - Retorna las fechas disponibles para el análisis de productividad.
- `get_productivity_dashboard(date: str = Query(None), user: User, session: Session, state: AppState)` - Retorna los datos necesarios para el dashboard de productividad MB51.
- `get_monthly_productivity(month: str = Query(None), user: User, session: Session, state: AppState)` - Retorna los KPIs mensuales de productividad.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `AppState` - Almacena el estado del sistema, incluyendo la sincronización y el caché.
- `cache_key` - Clave utilizada para almacenar y recuperar datos en el caché.

### Dependencias y Flujo
- **Librerías Externas**: FastAPI, SQLAlchemy, logging.
- **Flujo Interno**: 
  - Cada endpoint depende de `get_current_user`, `get_session_dep`, y `get_app_state`.
  - Utiliza `ProductivityService` para obtener los datos necesarios.
  - Maneja la sincronización y el caché mediante `AppState`.

