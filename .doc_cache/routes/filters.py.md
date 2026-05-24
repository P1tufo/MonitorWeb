## Archivo: ./routes/filters.py

### Resumen Funcional
El archivo `filters.py` contiene funciones y rutas para filtrar entregas y calcular KPIs dinámicos en un sistema de gestión de materiales. Ofrece endpoints para obtener datos filtrados por múltiples criterios y calcular indicadores clave de rendimiento (KPIs) basados en estos filtros.

### Catálogo de Funciones y Clases
- `_build_unified_where(date: str, area: str, centro: str, has_ots_filter: str, min_week: Optional[str])` - Construye la cláusula WHERE a nivel de MATERIAL con seguridad contra SQL Injection.
- `filter_transactions(request: Request, date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Filtra entregas basándose en múltiples criterios.
- `get_kpis(date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Calcula KPIs dinámicos filtrados por área para el dashboard.
- `api_widget_data(query_id: str, request: Request, session: Session = Depends(get_session_dep))` - Endpoint de carga asíncrona para los componentes del Dashboard.

### Interacción con Base de Datos
- Motor de BD: SQLAlchemy
- Tablas:
  - `outbound_deliveries`
  - `config_cost_center_mapping`
  - `warehouse_tasks`
- Columnas:
  - `v.entrega`
  - `v.week_sort`
  - `v.area_negocio`
  - `v.ubicacion_area`
  - `v.ubicacion_bin_1`
  - `v.ubicacion_bin`
  - `v.estado_wms`
  - `v.dias_retraso`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas`
  - `fastapi`
  - `sqlalchemy`
  - `logging`
- Comunicación con otros archivos del proyecto:
  - `core.database.get_session_dep`
  - `core.models.ConfigQuery`
  - `core.query_engine.build_sql_from_payload`
  - `core.schemas.VisualQueryBuilderPayload`
  - `repositories.deliveries.DeliveriesRepository`

