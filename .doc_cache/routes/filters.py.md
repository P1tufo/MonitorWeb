## Archivo: ./routes/filters.py

### Resumen Funcional
El archivo `filters.py` contiene funciones y rutas para filtrar entregas y calcular KPIs basados en múltiples criterios. Ofrece endpoints para obtener datos filtrados y estadísticas dinámicas.

### Catálogo de Funciones y Clases
- `_build_unified_where(date: str, area: str, centro: str, has_ots_filter: str, min_week: str)` - Construye la cláusula WHERE a nivel de MATERIAL.
- `filter_transactions(request: Request, date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Filtra entregas basándose en múltiples criterios.
- `get_kpis(date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Calcula KPIs dinámicos filtrados por área para el dashboard.

### Interacción con Base de Datos
- Motor de BD: SQLite (deducido del import `from core.database import get_session_dep`)
- Tablas:
  - `outbound_deliveries`
  - `config_cost_center_mapping`
- Columnas:
  - `v.entrega`
  - `v.week_sort`
  - `v.fecha_carga`
  - `v.fecha_sm_real`
  - `v.creado_el`
  - `v.area_negocio`
  - `v.ubicacion_area`
  - `v.ubicacion_bin_1`
  - `v.ubicacion_bin`
  - `v.estado_wms`
  - `v.material`
  - `v.dias_retraso`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `logging`
  - `sqlalchemy`
  - `pandas`
  - `fastapi`
- Comunicación con otros archivos del proyecto:
  - `core.database` (para obtener la sesión de base de datos)
  - `config` (para obtener el camino a la base de datos)

