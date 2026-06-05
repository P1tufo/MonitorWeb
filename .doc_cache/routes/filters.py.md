## Archivo: ./routes/filters.py

### Resumen Funcional
El archivo `filters.py` contiene endpoints para filtrar entregas y calcular KPIs dinámicos en un sistema de monitoreo de almacén (WMS). Utiliza FastAPI para definir las rutas, SQLAlchemy para interactuar con la base de datos SQLite, y pandas para procesar los resultados.

### Catálogo de Funciones y Clases
- `_build_unified_where(date: str = None, area: str = None, centro: str = None, has_ots: str = None, min_week: str = None) -> tuple[str, dict]` - Construye una cláusula WHERE unificada basada en los criterios de filtro proporcionados.
- `filter_transactions(request: Request, date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Filtra entregas basándose en múltiples criterios.
- `get_kpis(date: Optional[str] = None, entrega: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, session: Session = Depends(get_session_dep))` - Calcula KPIs dinámicos filtrados por área para el dashboard.
- `api_widget_data(query_id: str, request: Request, session: Session = Depends(get_session_dep))` - Endpoint de carga asíncrona para los componentes del Dashboard, lee visual_state, compila SQL y retorna los datos JSON directamente.

### Interacción con Base de Datos
- Motor de BD: SQLite.
- Tablas utilizadas:
  - `deliveries`
  - `warehouse_tasks`
- Columnas utilizadas:
  - `fecha_carga`, `fecha_sm_real`, `creado_el` (de la tabla `deliveries`)
  - `entrega` (de la tabla `warehouse_tasks`)
  - `estado_wms` (de la tabla `deliveries`)
  - `area` (de la tabla `deliveries`)
- Consultas SQL crudas: Sí, se utilizan consultas SQL generadas dinámicamente.

### Estado y Variables Globales
- Variables globales:
  - `DATE_EXPR`: Expresión unificada para la fecha de carga.
  - `ALLOWED_OTS_STATES`: Conjunto de estados OT permitidos como filtro.

### Dependencias y Flujo
- Librerías externas: pandas, fastapi, sqlalchemy.
- Archivos del proyecto que importa:
  - `core.database`
  - `core.models`
  - `core.query_engine`
  - `core.schemas`
  - `core.utils`
  - `repositories.deliveries`
- Archivos del proyecto que son importados por este archivo:
  - Ninguno.
- Flujo de datos: El archivo recibe solicitudes HTTP, procesa los parámetros, interactúa con la base de datos para obtener o calcular datos, y devuelve respuestas JSON.

