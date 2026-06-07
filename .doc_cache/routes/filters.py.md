## Archivo: ./routes/filters.py

### Resumen Funcional
El archivo `filters.py` contiene endpoints para filtrar entregas y calcular KPIs dinámicos en un sistema de monitoreo de almacén (WMS). Utiliza FastAPI, SQLAlchemy y SQLite para interactuar con la base de datos.

### Catálogo de Funciones y Clases
- `_build_unified_where(date: str = None, area: str = None, centro: str = None, has_ots: str = None, min_week: str = None) -> tuple[str, dict]` - Construye una cláusula WHERE unificada basada en los criterios de filtro proporcionados.
- `filter_transactions(request: Request, date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Filtra entregas basándose en múltiples criterios.
- `get_kpis(date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Calcula KPIs dinámicos filtrados por área para el dashboard.
- `api_widget_data(query_id: str, request: Request, session: Session = Depends(get_session_dep))` - Endpoint de carga asíncrona para los componentes del Dashboard.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - `warehouse_tasks`
  - `deliveries`
  - `dashboard`
  - `config_query`
- Columnas:
  - `v.fecha_carga`, `v.fecha_sm_real`, `v.creado_el` (de la tabla `deliveries`)
  - `l.entrega` (de la tabla `warehouse_tasks`)
  - `v.week_sort` (de la tabla `dashboard`)
  - `v.visual_state`, `v.sql_text` (de la tabla `config_query`)
- Consultas SQL crudas: Sí, se utilizan consultas SQL generadas dinámicamente.

### Estado y Variables Globales
- `DATE_EXPR`: Expresión para obtener la fecha de carga.
- `ALLOWED_OTS_STATES`: Conjunto de estados OT permitidos como filtro.

### Dependencias y Flujo
- Librerías externas: `pandas`, `fastapi`, `sqlalchemy`
- Archivos del proyecto que importan a este archivo:
  - `core.database`
  - `core.models`
  - `core.query_engine`
  - `core.schemas`
  - `core.utils`
  - `repositories.deliveries`
  - `repositories.dashboard`
- Archivos del proyecto que este archivo importa:
  - `config`
  - `core.macros`

**Flujo de datos:**
1. **Entrada**: Parámetros de filtro desde el cliente.
2. **Procesamiento**:
   - Construcción dinámica de consultas SQL basadas en los criterios de filtro.
   - Ejecución de consultas SQL contra la base de datos SQLite.
3. **Salida**: Datos filtrados o KPIs calculados en formato JSON.

Este archivo es crucial para el funcionamiento del sistema de monitoreo de almacén, proporcionando endpoints para obtener datos filtrados y calcular indicadores clave de rendimiento (KPIs) dinámicamente.

