## Archivo: ./repositories/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene métodos para interactuar con la base de datos SQLite y obtener registros relacionados con entregas en un sistema de monitoreo de almacén (WMS). Los métodos permiten consultar registros de entrega, realizar auditorías SLA, obtener detalles de entregas por lotes y recuperar información sobre áreas de negocio.

### Catálogo de Funciones y Clases
- `DeliveriesRepository(BaseRepository)` - Repositorio para el dominio de Entregas (outbound_deliveries).
  - `_sql(query_id: str, fallback: str) -> str` - Obtiene SQL desde config_queries con fallback explícito.
  - `_get_sla_threshold() -> int` - Retorna el umbral SLA configurado en la base de datos.
  - `get_sla_audit_records(year: str, late: bool = True, limit: int = 500, where_clause: Optional[str] = None, where_params: Optional[dict] = None) -> pd.DataFrame` - Obtiene registros de auditoría SLA para entregas.
  - `get_deliveries_for_bulk(date: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, entrega_query: Optional[str] = None) -> pd.DataFrame` - Obtiene detalles de entregas por lotes.
  - `get_area_lookup() -> pd.DataFrame` - Obtiene un mapeo de entregas a áreas de negocio.
  - `get_picking_items(entrega_ids: list) -> pd.DataFrame` - Obtiene los elementos de picking para una lista de entregas.
  - `get_delivery_by_id(entrega: str) -> pd.DataFrame` - Obtiene detalles de una entrega específica por su ID.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: `outbound_deliveries`
    - Columnas: `entrega`, `autor`, `area_negocio`, `creado_el`, `fecha_sm_real`, `material`, `denominacion`, `dias_retraso`, `estado_wms`, `ubicacion_bin`, `cantidad`, `umb`, `week_sort`.
  - Tabla: `warehouse_tasks`
    - Columnas: `entrega`.
  - Tabla: `DeliverySummary`
    - Columnas: `entrega_id`.

### Estado y Variables Globales
- **Variables Globales:** Ninguna.
- **Variables de Sesión:** Ninguna.
- **Diccionarios Quemados en Código:** Ninguno.

### Dependencias y Flujo
- **Librerías Externas:** pandas, sqlalchemy
- **Archivos del Proyecto que Importan a este Archivo:**
  - `core.db_config_manager`
  - `core.macros`
  - `repositories.base`
- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno.

**Flujo de Datos:** El archivo interactúa con la base de datos SQLite para ejecutar consultas SQL y devolver resultados en formato DataFrame.

