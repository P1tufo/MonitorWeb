## Archivo: ./core/schemas.py

### Resumen Funcional
Este archivo define esquemas de datos utilizando Pydantic, que son clases que describen la estructura y los tipos de datos esperados en las respuestas de API y payloads de consultas visuales.

### Catálogo de Funciones y Clases
- `DashboardResponse(data: Dict[str, Any], is_syncing: bool)` - Define la estructura de la respuesta para un panel de control.
- `AnalyticsDeliveriesResponse(data: Dict[str, Any], is_syncing: bool)` - Define la estructura de la respuesta para análisis de entregas.
- `AnalyticsInventoryResponse(data: Dict[str, Any], is_syncing: bool)` - Define la estructura de la respuesta para análisis de inventario.
- `AnalyticsTasksResponse(data: Dict[str, Any], is_syncing: bool)` - Define la estructura de la respuesta para análisis de tareas.
- `JoinDef(table: str, onLeft: str, onRight: str)` - Define la estructura para una definición de unión en consultas visuales.
- `FilterDef(column: str, operator: str, value: Optional[Any] = "", valueType: Optional[str] = "value", compareColumn: Optional[str] = None, offsetValue: Optional[str] = None, diffOp: Optional[str] = None)` - Define la estructura para una definición de filtro en consultas visuales.
- `MetricCondition(column: str, operator: str, value: Any)` - Define la estructura para una condición de métrica en consultas visuales.
- `MetricDef(column: str, aggregation: str, format: Optional[str] = "number", label: Optional[str] = "", condition: Optional[MetricCondition] = None, customExpr: Optional[str] = None)` - Define la estructura para una definición de métrica en consultas visuales.
- `TimeAxisDef(column: Optional[str] = None, granularity: Optional[str] = "NONE")` - Define la estructura para la definición del eje temporal en consultas visuales.
- `SecondMetricDef(column: str = "", aggregation: str = "", label: str = "")` - Define la estructura para una segunda métrica en consultas visuales.
- `VisualQueryBuilderPayload(baseTable: str, joins: list[JoinDef] = [], filters: list[FilterDef] = [], metric: Optional[MetricDef] = None, timeAxis: Optional[TimeAxisDef] = None, breakdown: Optional[str] = None, secondMetric: Optional[SecondMetricDef] = None, metrics: list[MetricDef] = [])` - Define la estructura del payload para el generador de consultas visuales.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- `pydantic` - Librería utilizada para definir los esquemas de datos.
- No se comunica con otros archivos del proyecto.

