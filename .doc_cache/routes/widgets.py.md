## Archivo: ./routes/widgets.py

### Resumen Funcional
Este archivo contiene endpoints para obtener datos de widgets y sugerencias de reabastecimiento en un sistema de monitoreo de almacén (WMS). Los endpoints permiten consultar datos estructurados, ejecutar consultas personalizadas, y exportar sugerencias de pedido a formato Excel.

### Catálogo de Funciones y Clases
- `get_widget_data(query_id: str, year: Optional[str] = None, area: Optional[str] = None, granularity: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user), cache: CacheManager = Depends(get_cache_manager))` - Ejecuta una consulta visual y devuelve los datos estructurados.
- `get_widget_drilldown(query_id: str, segment: str, material: Optional[str] = None, year: Optional[str] = None, area: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user))` - Obtiene el detalle subyacente de un segmento de un widget.
- `get_cmv201_summary(plan_type: str = Query(..., description="Planificado o Desplanificado"), year: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user))` - Muestra la cantidad de materiales solicitados por área de negocio y mes para el CMV 201.
- `get_cmv201_area_details(plan_type: str = Query("planificado", description="'planificado' o 'desplanificado'"), area: str = Query(..., description="Area de negocio filtrada"), mes: str = Query(None, description="Mes en formato YYYY-MM. Si no se provee, no se filtra por mes."), year: str = Query(None, description="Año"), db: Session = Depends(get_session_dep))` - Muestra los detalles del CMV 201 para una área de negocio específica.
- `get_cmv261_summary(plan_type: str = Query("planificado", description="'planificado' o 'desplanificado'"), year: Optional[str] = None, db: Session = Depends(get_session_dep))` - Muestra la cantidad de materiales solicitados por área de negocio y mes para el CMV 261.
- `get_cmv261_area_details(plan_type: str = Query("planificado", description="'planificado' o 'desplanificado'"), area: str = Query(..., description="Area de negocio filtrada"), mes: str = Query(None, description="Mes en formato YYYY-MM. Si no se provee, no se filtra por mes."), year: str = Query(None, description="Año"), db: Session = Depends(get_session_dep))` - Muestra los detalles del CMV 261 para una área de negocio específica.
- `get_replenishment_suggestions(freq: str = Query("all", description="Filtro de frecuencia: all, 1, 3, 6, 12"), db: Session = Depends(get_session_dep))` - Calcula sugerencias de pedido basándose en el stock inicial MB5B y el ritmo de consumo.
- `export_replenishment_suggestions(db: Session = Depends(get_session_dep))` - Exporta todas las sugerencias de pedido (Autonomía < 1) a un archivo Excel.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `ConfigQuery`
- Columnas:
  - `query_id`, `visual_state`

### Estado y Variables Globales
- No hay variables globales, de sesión o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- Librerías externas: `pandas`
- Archivos del proyecto que IMPORTA:
  - `core.auth.get_current_user`
  - `core.database.get_session_dep`
  - `core.helpers.dynamic_executor.execute_visual_query`
  - `core.models.ConfigQuery`
  - `core.state.CacheManager.get_cache_manager`
  - `core.utils.sanitize_for_json`
- Archivos del proyecto que IMPORTAN a este archivo:
  - Ninguno
- Flujo de datos: Los endpoints consumen y producen datos estructurados, interactuando con la base de datos para obtener los datos necesarios.

