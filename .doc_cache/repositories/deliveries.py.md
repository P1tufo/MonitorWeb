## Archivo: ./repositories/deliveries.py

### Resumen Funcional
El archivo `deliveries.py` contiene métodos para interactuar con la base de datos SQLite y obtener registros relacionados con entregas en un sistema de almacén (WMS). Los métodos permiten consultar registros de entrega, realizar auditorías SLA, obtener detalles de entregas por lotes y recuperar información sobre áreas de negocio.

### Catálogo de Funciones y Clases
- `DeliveriesRepository(BaseRepository)` - Repositorio para el dominio de Entregas (outbound_deliveries).
  - `_sql(query_id: str, fallback: str) -> str` - Obtiene SQL desde config_queries con fallback explícito.
  - `_get_sla_threshold() -> int` - Retorna el umbral SLA configurado en la base de datos.
  - `get_sla_audit_records(year: str, late: bool = True, limit: int = 500, where_clause: str = None, where_params: dict = None) -> pd.DataFrame` - Obtiene registros de auditoría SLA para entregas.
  - `get_deliveries_for_bulk(date: str = None, area: str = None, centro: str = None, has_ots_filter: str = None, entrega_query: str = None) -> pd.DataFrame` - Obtiene detalles de entregas por lotes.
  - `get_area_lookup() -> pd.DataFrame` - Obtiene una lista de áreas de negocio asociadas a las entregas.
  - `get_picking_items(entrega_ids: list) -> pd.DataFrame` - Obtiene los elementos de picking para un conjunto de entregas.
  - `get_delivery_by_id(entrega: str) -> pd.DataFrame` - Obtiene detalles de una entrega específica por su ID.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - `outbound_deliveries`
  - `warehouse_tasks`
  - `DeliverySummary`
- Columnas:
  - `entrega`, `autor`, `area_negocio`, `creado_el`, `fecha_sm_real`, `material`, `denominacion`, `dias_retraso`, `sla_limit`, `has_ots` en `outbound_deliveries`
  - `entrega_id`, `entrega`, `autor`, `ubicacion_bin`, `material`, `descripcion`, `cantidad`, `umb`, `area`, `entrega` en `warehouse_tasks`
  - `entrega_id`, `entrega`, `area_negocio` en `DeliverySummary`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas:
  - `pandas`
  - `sqlalchemy`
- Archivos del proyecto que IMPORTA a este archivo (`deliveries.py`):
  - `core.db_config_manager`
  - `core.macros`
  - `repositories.base`
- Archivos del proyecto que este archivo IMPORTA (`deliveries.py`):
  - Ninguno
- Flujo de datos:
  - El archivo importa y utiliza métodos de otras clases para interactuar con la base de datos y procesar los resultados en formato DataFrame.

