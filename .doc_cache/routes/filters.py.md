## Archivo: ./routes/filters.py

### Resumen Funcional
El archivo `filters.py` contiene endpoints para filtrar transacciones y calcular KPIs en un sistema de monitoreo de almacén (WMS) utilizando FastAPI, SQLAlchemy y SQLite. Ofrece funcionalidades para obtener datos filtrados por múltiples criterios y calcular indicadores clave de rendimiento (KPIs).

### Catálogo de Funciones y Clases
- `_build_unified_where(date: Optional[str], area: Optional[str], centro: Optional[str], has_ots: Optional[str], min_week: Optional[str]) -> tuple[str, dict]` - Construye una cláusula WHERE unificada basada en los criterios de filtro proporcionados.
- `filter_transactions(request: Request, date: Optional[str], entrega: Optional[str], area: Optional[str], centro: Optional[str], has_ots_filter: Optional[str], session: Session = Depends(get_session_dep))` - Filtra entregas según múltiples criterios y devuelve los resultados.
- `get_kpis(date: Optional[str], entrega: Optional[str], area: Optional[str], centro: Optional[str], has_ots_filter: Optional[str], session: Session = Depends(get_session_dep))` - Calcula KPIs dinámicos filtrados por área para el dashboard.
- `api_widget_data(query_id: str, request: Request, session: Session = Depends(get_session_dep))` - Endpoint de carga asíncrona para los componentes del Dashboard, lee visual_state, compila SQL y retorna los datos JSON directamente.

### Interacción con Base de Datos
- Motor de BD: SQLite.
- Tablas:
  - `warehouse_tasks`
  - `ConfigQuery`
- Columnas:
  - `v.fecha_carga`, `v.fecha_sm_real`, `v.creado_el` (de la tabla `v`)
  - `l.entrega` (de la tabla `warehouse_tasks`)
  - `v.week_sort` (de la tabla `v`)
  - `area_expr` (de la tabla `v`)
  - `entrega` (de la tabla `ConfigQuery`)
  - `visual_state` (de la tabla `ConfigQuery`)
- Consultas SQL crudas: Sí, se utilizan consultas SQL generadas dinámicamente.

### Estado y Variables Globales
- Variables globales:
  - `DATE_EXPR`: Expresión unificada para la fecha de carga.
  - `ALLOWED_OTS_STATES`: Conjunto de estados OT permitidos como filtro.

### Dependencias y Flujo
- Librerías externas: `pandas`, `fastapi`, `sqlalchemy`.
- Archivos del proyecto que importa:
  - `config.py`
  - `core.database`
  - `core.models`
  - `core.query_engine`
  - `core.schemas`
  - `core.utils`
  - `repositories.deliveries`
  - `repositories.dashboard`
- Archivos del proyecto que son importados por este archivo:
  - Ninguno.
- Flujo de datos: El flujo de datos pasa a través de los endpoints, donde se reciben parámetros de filtro, se construyen consultas SQL dinámicas y se ejecutan contra la base de datos SQLite. Los resultados se procesan y devuelven al cliente en formato JSON.

