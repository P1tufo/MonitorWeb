## Archivo: ./routes/dashboard.py

### Resumen Funcional
El archivo `dashboard.py` contiene rutas para el dashboard de un sistema de monitoreo de almacén (WMS). Ofrece endpoints para obtener ubicaciones de materiales y cargar la vista principal del dashboard con KPIs.

### Catálogo de Funciones y Clases
- `get_ubicaciones(material: str, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Obtiene las ubicaciones de un material específico.
- `dashboard(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Vista principal del Dashboard con KPIs y búsqueda rápida.
- `dashboard_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - API JSON para el Dashboard con KPIs y búsqueda rápida.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `stock_levels`, `warehouse_tasks`
- **Columnas:**
  - `stock_levels`: `ubicacion_bin`, `Ubicación`, `ubicacin`, `denominacion`, `Texto breve de material`, `material`, `UMB`, `Stock disp`, `ubic_actual`
  - `warehouse_tasks`: `ubic_dest`, `fecha_conf`, `fe_creac`, `texto_breve_material`, `material`, `tp_dest`, `ubic_dest`

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `logging`
  - `sqlite3`
  - `itertools`
  - `pandas`
  - `datetime`
  - `timedelta`
  - `typing`
  
- **Archivos del Proyecto que Importan a este Archivo (`dashboard.py`):** Ninguno

- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.database.get_session_dep`
  - `fastapi.APIRouter`
  - `fastapi.Request`
  - `fastapi.Depends`
  - `fastapi.HTTPException`
  - `fastapi.responses.HTMLResponse`
  - `core.state.get_app_state`
  - `core.auth.get_current_user`
  - `core.app_instance.templates`
  - `services.dashboard_service.DashboardService`
  - `core.schemas.DashboardResponse`

- **Dirección del Flujo de Datos:**
  - Desde el endpoint hasta la base de datos para obtener los datos.
  - Desde el servicio hacia el endpoint para proporcionar el contexto del negocio.

