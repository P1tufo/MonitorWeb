## Archivo: ./routes/deliveries.py

### Resumen Funcional
Este archivo contiene rutas y funciones para el módulo de análisis de entregas en un sistema de gestión de almacén (WMS). Ofrece endpoints para renderizar páginas web con datos de análisis y una API JSON que devuelve los mismos datos.

### Catálogo de Funciones y Clases
- `save_analytics_snapshot(session: Session, key: str, data: Dict[str, Any])` - Guarda una captura de las analíticas en la base de datos para carga instantánea.
- `load_analytics_snapshot(session: Session, key: str) -> Optional[Dict[str, Any]]` - Recupera la última captura de analíticas desde la base de datos.
- `analytics(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Renderiza la página principal de analíticas con caché multinivel (Memoria -> DB -> Cálculo).
- `sla_details(request: Request, type: str = "late", date: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Vista detallada de auditoría SLA.
- `get_non_palletized_details(user: str, clase_mov: str, db: Session = Depends(get_session_dep), current_user: Dict[str, Any] = Depends(get_current_user))` - Obtiene el listado detallado (hasta 200) de movimientos no paletizados para un usuario y tipo de movimiento específicos.
- `analytics_deliveries_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - API JSON para analíticas de Entregas (Outbound Deliveries).

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - `analytics_snapshots`: 
    - `key` (TEXT, PRIMARY KEY)
    - `data` (TEXT)
    - `updated_at` (TIMESTAMP)
  - `lx02_pendientes`
    - `otcuanto` (OTCQUANTO)
    - `material` (MATERIAL)
    - `stock_disp` (STOCK_DISP)
  - `inventory_movements`
    - `doc_mat` (DOC_MAT)
    - `usuario` (USUARIO)
    - `cmv` (CMV)
    - `alm` (ALM)
    - `ce` (CE)
    - `fe_contab` (FE_CONTAB)
    - `hora` (HORA)

### Estado y Variables Globales
- **Variables Globales:** Ninguna.
- **Estado de Sesión:** Utiliza el estado de la aplicación (`AppState`) para almacenar y recuperar datos en caché.

### Dependencias y Flujo
- **Librerías Externas:**
  - `logging`
  - `sqlite3`
  - `pandas`
  - `json`
  - `datetime`
  - `typing`
  - `sqlalchemy`
  - `fastapi`
  - `core.database`
  - `sqlalchemy.orm`
  - `core.state`
  - `core.app_instance`
  - `core.schemas`
  - `repositories`
  - `routes.inventory`
  - `routes.tasks`
  - `routes.analytics_proyecciones`
  - `core.auth`
  - `core.utils`
  - `services.deliveries_service`

- **Archivos del Proyecto que Importan a Este Archivo:**
  - `routes/inventory.py`
  - `routes/tasks.py`
  - `routes/analytics_proyecciones.py`
  - `services/deliveries_service.py`

- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno.

**Flujo de Datos:** El archivo importa y utiliza funciones y clases de otros archivos para procesar datos, interactuar con la base de datos y renderizar vistas.

