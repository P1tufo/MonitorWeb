## Archivo: ./core/schemas.py

### Resumen Funcional
Este archivo define esquemas de datos utilizando Pydantic para representar diferentes tipos de respuestas y payloads en un sistema de monitoreo de almacén (WMS). Los esquemas incluyen estructuras para respuestas del dashboard, análisis de entregas, inventario y tareas, así como definiciones para consultas visuales avanzadas.

### Catálogo de Funciones y Clases
- `DashboardResponse(data: Dict[str, Any], is_syncing: bool) -> None`: Representa la respuesta del dashboard.
- `AnalyticsDeliveriesResponse(data: Dict[str, Any], is_syncing: bool) -> None`: Representa la respuesta del análisis de entregas.
- `AnalyticsInventoryResponse(data: Dict[str, Any], is_syncing: bool) -> None`: Representa la respuesta del análisis de inventario.
- `AnalyticsTasksResponse(data: Dict[str, Any], is_syncing: bool) -> None`: Representa la respuesta del análisis de tareas.
- `JoinDef(table: str, onLeft: str, onRight: str) -> None`: Define una relación JOIN para consultas visuales avanzadas.
- `FilterDef(column: str, operator: str, value: Optional[Any] = "", valueType: Optional[str] = "value", compareColumn: Optional[str] = None, offsetValue: Optional[str] = None, diffOp: Optional[str] = None) -> None`: Define un filtro para consultas visuales avanzadas.
- `MetricCondition(column: str, operator: str, value: Any) -> None`: Define una condición de métrica para consultas visuales avanzadas.
- `MetricDef(column: str, aggregation: str, format: Optional[str] = "number", label: Optional[str] = "", condition: Optional[MetricCondition] = None, customExpr: Optional[str] = None) -> None`: Define una métrica para consultas visuales avanzadas.
- `TimeAxisDef(column: Optional[str] = None, granularity: Optional[str] = "NONE") -> None`: Define el eje de tiempo para consultas visuales avanzadas.
- `SecondMetricDef(column: str = "", aggregation: str = "", label: str = "") -> None`: Define una segunda métrica para consultas visuales avanzadas.
- `VisualQueryBuilderPayload(baseTable: Optional[str] = None, datasetId: Optional[str] = None, joins: list[JoinDef] = [], filters: list[FilterDef] = [], metric: Optional[MetricDef] = None, timeAxis: Optional[TimeAxisDef] = None, breakdown: Optional[str] = None, secondMetric: Optional[SecondMetricDef] = None, metrics: list[MetricDef] = [], chartType: Optional[str] = "bar") -> None`: Define el payload para consultas visuales avanzadas.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
No aplica.

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- **Librerías Externas**: `pydantic`, `typing`
- **Archivos del Proyecto que Importan a este Archivo**: No aplica.
- **Archivos del Proyecto que Este Archivo Importa**: No aplica.

