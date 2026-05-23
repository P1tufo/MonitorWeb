## Archivo: ./routes/deliveries.py

### Resumen Funcional
Este archivo contiene rutas para el análisis de entregas optimizadas y seguras. Incluye endpoints para renderizar páginas web y proporcionar datos en formato JSON.

### Catálogo de Funciones y Clases
- `save_analytics_snapshot(session: Session, key: str, data: Dict[str, Any])` - Guarda una captura de las analíticas en la base de datos.
- `load_analytics_snapshot(session: Session, key: str) -> Optional[Dict[str, Any]]` - Recupera la última captura de analíticas desde la base de datos.
- `analytics(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Renderiza la página principal de analíticas con caché multinivel.
- `sla_details(request: Request, type: str = "late", session: Session = Depends(get_session_dep))` - Vista detallada de auditoría SLA.
- `get_non_palletized_details(user: str, clase_mov: str, db: Session = Depends(get_session_dep), current_user: Dict[str, Any] = Depends(get_current_user))` - Obtiene el listado detallado de movimientos no paletizados para un usuario y tipo de movimiento específicos.
- `analytics_deliveries_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - API JSON para analíticas de Entregas (Outbound Deliveries).

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `analytics_snapshots`
- Columnas:
  - `key`, `data`, `updated_at`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
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

- Flujo hacia otros archivos del proyecto:
  - `core.database.get_session_dep`
  - `core.state.get_app_state`
  - `templates.TemplateResponse`
  - `DeliveriesRepository`
  - `get_inventory_context`
  - `get_tasks_context`
  - `get_proyecciones_context`
  - `get_current_user`
  - `sanitize_for_json`
  - `DeliveriesService`

