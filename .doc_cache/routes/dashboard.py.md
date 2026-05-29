## Archivo: ./routes/dashboard.py

### Resumen Funcional
El archivo `dashboard.py` define rutas para un dashboard que incluye endpoints para obtener ubicaciones de materiales y la vista principal del dashboard con KPIs. Utiliza FastAPI para definir las rutas, SQLAlchemy para interactuar con una base de datos SQLite, y pandas para procesar los resultados.

### Catálogo de Funciones y Clases
- `get_ubicaciones(material: str, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Obtiene las ubicaciones de un material específico.
- `dashboard(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Vista principal del dashboard con KPIs y búsqueda rápida.
- `dashboard_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - API JSON para el dashboard con KPIs y búsqueda rápida.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `stock_levels`
- Columnas:
  - `ubicacion_bin`, `Ubicación`, `ubicacin`, `denominacion`, `Texto breve de material`, `material`, `UMB`, `Stock disp`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: `logging`, `sqlite3`, `itertools`, `pandas`, `datetime`, `timedelta`, `typing`, `fastapi`, `sqlalchemy`, `core.database`, `core.state`, `core.auth`, `core.app_instance`, `services.dashboard_service`, `core.wms_config`, `core.schemas`
- Flujo: El archivo interactúa con el servicio `DashboardService` para obtener datos de negocio y los presenta a través de endpoints FastAPI. Utiliza una sesión de base de datos SQLAlchemy para ejecutar consultas SQL y pandas para procesar los resultados.

