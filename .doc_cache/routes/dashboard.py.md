## Archivo: ./routes/dashboard.py

### Resumen Funcional
El archivo `dashboard.py` define rutas para un panel de control (dashboard) que incluye endpoints para obtener ubicaciones de materiales y cargar la vista principal del dashboard con KPIs y búsqueda rápida. También proporciona una API JSON para el mismo propósito.

### Catálogo de Funciones y Clases
- `get_ubicaciones(material: str, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Obtiene las ubicaciones de un material específico.
- `dashboard(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Vista principal del dashboard con KPIs y búsqueda rápida.
- `dashboard_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - API JSON para el dashboard con KPIs y búsqueda rápida.

### Interacción con Base de Datos
- Motor de base de datos: SQLite
- Tablas:
  - `stock_levels`
  - `warehouse_tasks`
- Columnas:
  - `ubicacion_bin`, `ubicacin`, `ubicacion` (dependiendo del origen de la importación)
  - `denominacion`, `texto_breve_de_material`
  - `fecha_conf`, `fe_creac`, `material`, `tp_dest`, `ubic_dest`, `stock_disp`, `umb`, `ubic_actual`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `logging`
  - `sqlite3`
  - `itertools`
  - `pandas`
  - `datetime`
  - `timedelta`
  - `typing`
  - `fastapi`
  - `sqlalchemy`
  - `core.database`
  - `core.state`
  - `core.auth`
  - `core.app_instance`
  - `services.dashboard_service`
  - `core.wms_config`
  - `core.schemas`

- Flujo de comunicación:
  - El archivo interactúa con el servicio `DashboardService` para obtener el contexto de negocio.
  - Utiliza la sesión de base de datos (`Session`) proporcionada por `get_session_dep`.
  - Recupera y establece en caché los contextos del dashboard utilizando `AppState`.

