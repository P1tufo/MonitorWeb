## Archivo: ./routes/dashboard.py

### Resumen Funcional
El archivo `dashboard.py` contiene rutas para el dashboard de un sistema de monitoreo de almacén (WMS). Ofrece endpoints para obtener ubicaciones de materiales y cargar la vista principal del dashboard con KPIs.

### Catálogo de Funciones y Clases
- `get_ubicaciones(material: str, user = Depends(get_current_user), session: Session = Depends(get_session_dep))` - Obtiene las ubicaciones de un material específico.
- `dashboard(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager), sync: SyncStateManager = Depends(get_sync_manager))` - Vista principal del Dashboard con KPIs y búsqueda rápida.
- `dashboard_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager), sync: SyncStateManager = Depends(get_sync_manager))` - API JSON para el Dashboard con KPIs y búsqueda rápida.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `stock_levels`, `warehouse_tasks`
- **Columnas:**
  - `stock_levels`: `ubicacion_bin`, `Ubicación`, `ubicacin`, `denominacion`, `Texto breve de material`, `stock_disp`, `umb`, `ubic_actual`
  - `warehouse_tasks`: `ubic_dest`, `fecha_conf`, `fe_creac`, `material`, `tp_dest`, `ubic_dest`

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `fastapi`
  - `sqlalchemy`
  - `logging`
- **Archivos del Proyecto que Importan a este Archivo (`dashboard.py`):** Ninguno
- **Archivos del Proyecto que Este Archivo Importa (`dashboard.py`):**
  - `core.app_instance.templates`
  - `core.auth.get_current_user`
  - `core.database.get_session_dep`
  - `core.schemas.DashboardResponse`
  - `core.state.CacheManager`, `core.state.SyncStateManager`, `get_cache_manager`, `get_sync_manager`
  - `services.dashboard_service.DashboardService`

**Flujo de Datos:**
1. **Entrada:** Requiere un usuario autenticado y una sesión de base de datos.
2. **Procesamiento:**
   - Para `get_ubicaciones`: Consulta la tabla `stock_levels` para obtener las ubicaciones del material especificado.
   - Para `dashboard` y `dashboard_api`: Utiliza el servicio `DashboardService` para obtener el contexto completo del negocio, que luego se almacena en caché.
3. **Salida:** Devuelve los datos en formato JSON o HTML según la solicitud.

**Nota:** El archivo no utiliza consultas SQL crudas directamente; en su lugar, usa SQLAlchemy ORM y pandas para manipular los datos.

