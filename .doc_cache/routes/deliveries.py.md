## Archivo: ./routes/deliveries.py

### Resumen Funcional
Este archivo contiene rutas y funciones para el módulo de análisis de entregas en un sistema de gestión de almacén (WMS). Ofrece endpoints para renderizar páginas web con datos de análisis, así como una API JSON que devuelve los mismos datos.

### Catálogo de Funciones y Clases
- `save_analytics_snapshot(session: Session, key: str, data: Dict[str, Any])` - Guarda una captura de las analíticas en la base de datos para carga instantánea.
- `load_analytics_snapshot(session: Session, key: str) -> Optional[Dict[str, Any]]` - Recupera la última captura de analíticas desde la base de datos.
- `analytics(request: Request, user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager))` - Renderiza la página principal de analíticas con caché multinivel (Memoria -> DB -> Cálculo).
- `sla_details(request: Request, type: str = "late", date: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Vista detallada de auditoría SLA.
- `get_non_palletized_details(user: str, clase_mov: str, db: Session = Depends(get_session_dep), current_user: Dict[str, Any] = Depends(get_current_user))` - Obtiene el listado detallado (hasta 200) de movimientos no paletizados para un usuario y tipo de movimiento específicos.
- `analytics_deliveries_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager), sync: SyncStateManager = Depends(get_sync_manager))` - API JSON para analíticas de Entregas (Outbound Deliveries).

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - `analytics_snapshots`: 
    - `key` (TEXT, PRIMARY KEY)
    - `data` (TEXT)
    - `updated_at` (TIMESTAMP)
  - `inventory_movements`: 
    - `doc_mat`
    - `usuario`
    - `cmv`
    - `alm`
    - `ce`
    - `fe_contab`
    - `hora`

### Estado y Variables Globales
- **Variables Globales:** Ninguna.
- **Estado de Sesión:** Ninguna.
- **Estado de Entorno:** Ninguna.
- **Diccionarios Quemados en Código:** Ninguno.

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `fastapi`
  - `sqlalchemy`
  - `logging`
  - `json`
  - `datetime`
  - `typing`

- **Archivos del Proyecto que Este Archivo IMPORTA (consume):**
  - `core.app_instance`
  - `core.auth`
  - `core.database`
  - `core.schemas`
  - `core.state`
  - `core.utils`
  - `repositories.DeliveriesRepository`
  - `routes.analytics_proyecciones`
  - `routes.inventory`
  - `routes.tasks`
  - `services.deliveries_service`

- **Archivos del Proyecto que IMPORTAN a Este Archivo (lo consumen):**
  - Ninguno.

**Flujo de Datos:**
1. **Entrada:** Solicitudes HTTP a las rutas definidas.
2. **Procesamiento:** Llamadas a funciones y servicios para obtener datos, aplicar caché y guardar capturas en la base de datos.
3. **Salida:** Renderizado de plantillas HTML o respuesta JSON con los datos procesados.

Este archivo es crucial para el rendimiento y la eficiencia del sistema de análisis de entregas, ya que implementa un mecanismo de caché multinivel y persistente en la base de datos.

