## Archivo: ./core/schemas.py

### Resumen Funcional
Este archivo define esquemas de datos (schemas) utilizando Pydantic para la validación y serialización de objetos en un sistema de monitoreo de almacén (WMS). Los esquemas incluyen respuestas para diferentes tipos de análisis y definiciones para consultas visuales.

### Catálogo de Funciones y Clases
- `DashboardResponse(data: Dict[str, Any], is_syncing: bool)` - Define la estructura de respuesta para el panel de control.
- `AnalyticsDeliveriesResponse(data: Dict[str, Any], is_syncing: bool)` - Define la estructura de respuesta para análisis de entregas.
- `AnalyticsInventoryResponse(data: Dict[str, Any], is_syncing: bool)` - Define la estructura de respuesta para análisis de inventario.
- `AnalyticsTasksResponse(data: Dict[str, Any], is_syncing: bool)` - Define la estructura de respuesta para análisis de tareas.
- `JoinDef(table: str, onLeft: str, onRight: str)` - Define una definición de unión (join) para consultas SQL.
- `FilterDef(column: str, operator: str, value: Optional[Any] = "", valueType: Optional[str] = "value", compareColumn: Optional[str] = None, offsetValue: Optional[str] = None, diffOp: Optional[str] = None)` - Define una definición de filtro para consultas SQL.
- `MetricCondition(column: str, operator: str, value: Any)` - Define una condición para métricas en consultas visuales.
- `MetricDef(column: str, aggregation: str, format: Optional[str] = "number", label: Optional[str] = "", condition: Optional[MetricCondition] = None, customExpr: Optional[str] = None)` - Define una definición de métrica para consultas visuales.
- `TimeAxisDef(column: Optional[str] = None, granularity: Optional[str] = "NONE")` - Define la configuración del eje temporal en consultas visuales.
- `SecondMetricDef(column: str = "", aggregation: str = "", label: str = "")` - Define una segunda métrica para consultas visuales.
- `VisualQueryBuilderPayload(baseTable: Optional[str] = None, datasetId: Optional[str] = None, joins: list[JoinDef] = [], filters: list[FilterDef] = [], metric: Optional[MetricDef] = None, timeAxis: Optional[TimeAxisDef] = None, breakdown: Optional[str] = None, secondMetric: Optional[SecondMetricDef] = None, metrics: list[MetricDef] = [], chartType: Optional[str] = "bar")` - Define el payload para consultas visuales.

### Interacción con Base de Datos
Ninguna. Este archivo no interactúa directamente con la base de datos.

### Estado y Variables Globales
Ninguna. No se definen variables globales, de sesión o de entorno en este archivo.

### Dependencias y Flujo
- **Dependencias**: `pydantic`
- **Archivos que importan a este archivo**: Ninguno.
- **Archivos que este archivo importa**: Ninguno.
- **Flujo de datos**: Este archivo define esquemas de datos que pueden ser utilizados por otros componentes del sistema, como los servicios o las rutas.

