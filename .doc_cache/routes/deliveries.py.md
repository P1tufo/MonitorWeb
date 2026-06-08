## Archivo: ./routes/deliveries.py

### Resumen Funcional
Este archivo contiene rutas para el sistema de monitoreo de almacén (WMS) que proporcionan análisis y detalles sobre entregas. Incluye endpoints para renderizar páginas web con datos de entrega, obtener detalles detallados de movimientos no paletizados y proporcionar una API JSON con analíticas de entregas.

### Catálogo de Funciones y Clases
- `analytics(request: Request, user=Depends(get_current_user), session: Session=Depends(get_session_dep))` - Renderiza la página principal de analíticas.
- `sla_details(request: Request, type: str="late", date: Optional[str]=None, area: Optional[str]=None, centro: Optional[str]=None, has_ots_filter: Optional[str]=None, session: Session=Depends(get_session_dep))` - Vista detallada de auditoría SLA.
- `get_non_palletized_details(user: str, clase_mov: str, db: Session=Depends(get_session_dep), current_user: Dict[str, Any]=Depends(get_current_user))` - Obtiene el listado detallado de movimientos no paletizados para un usuario y tipo de movimiento específicos.
- `analytics_deliveries_api(user=Depends(get_current_user), session: Session=Depends(get_session_dep), sync: SyncStateManager=Depends(get_sync_manager))` - API JSON para analíticas de Entregas con caché multinivel.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - `lx02_pendientes`: `otcuanto`, `material`, `stock_disp`
  - `inventory_movements`: `doc_mat`, `usuario`, `cmv`, `alm`, `ce`, `fe_contab`, `hora`

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `fastapi`
  - `sqlalchemy`
  - `logging`
  - `datetime`
  - `json`
  - `typing`

- **Archivos del Proyecto que Importan a este Archivo (lo consumen):** Ninguno

- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.app_instance.templates`
  - `core.auth.get_current_user`
  - `core.database.get_session_dep`
  - `core.schemas.AnalyticsDeliveriesResponse`
  - `core.state.SyncStateManager.get_sync_manager`
  - `core.utils.sanitize_for_json`
  - `repositories.DeliveriesRepository`
  - `services.deliveries_service.DeliveriesService`

- **Dirección del Flujo de Datos:**
  - Desde el endpoint hasta la base de datos para obtener los datos necesarios.
  - Desde la base de datos hasta el servicio para procesar y formatear los datos.
  - Desde el servicio hasta las vistas para renderizar la información.

