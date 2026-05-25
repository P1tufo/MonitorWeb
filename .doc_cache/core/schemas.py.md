## Archivo: ./core/schemas.py

### Resumen Funcional
Este archivo define esquemas de datos utilizando Pydantic, que son clases que describen la estructura y los tipos de datos para objetos JSON. Estos esquemas se utilizan principalmente para validar y manejar datos en aplicaciones web.

### Catálogo de Funciones y Clases
- `DashboardResponse(data: Dict[str, Any], is_syncing: bool)` - Define la respuesta para un panel de control.
- `AnalyticsDeliveriesResponse(data: Dict[str, Any], is_syncing: bool)` - Define la respuesta para análisis de entregas.
- `AnalyticsInventoryResponse(data: Dict[str, Any], is_syncing: bool)` - Define la respuesta para análisis de inventario.
- `AnalyticsTasksResponse(data: Dict[str, Any], is_syncing: bool)` - Define la respuesta para análisis de tareas.
- `JoinDef(table: str, onLeft: str, onRight: str)` - Define una definición de unión para consultas SQL.
- `FilterDef(column: str, operator: str, value: Optional[Any] = "", valueType: Optional[str] = "value", compareColumn: Optional[str] = None, offsetValue: Optional[str] = None, diffOp: Optional[str] = None)` - Define una definición de filtro para consultas SQL.
- `MetricCondition(column: str, operator: str, value: Any)` - Define una condición para métricas en consultas SQL.
- `MetricDef(column: str, aggregation: str, format: Optional[str] = "number", label: Optional[str] = "", condition: Optional[MetricCondition] = None, customExpr: Optional[str] = None)` - Define una definición de métrica para consultas SQL.
- `TimeAxisDef(column: Optional[str] = None, granularity: Optional[str] = "NONE")` - Define la definición del eje temporal en consultas SQL.
- `SecondMetricDef(column: str = "", aggregation: str = "", label: str = "")` - Define una segunda métrica para consultas SQL.
- `VisualQueryBuilderPayload(baseTable: str, joins: list[JoinDef] = [], filters: list[FilterDef] = [], metric: Optional[MetricDef] = None, timeAxis: Optional[TimeAxisDef] = None, breakdown: Optional[str] = None, secondMetric: Optional[SecondMetricDef] = None, metrics: list[MetricDef] = [], chartType: Optional[str] = "bar")` - Define el payload para el generador de consultas visuales.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- `pydantic`: Librería utilizada para definir esquemas de datos.
- No se comunica con otros archivos del proyecto.

