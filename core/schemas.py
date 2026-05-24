from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class DashboardResponse(BaseModel):
    data: Dict[str, Any]
    is_syncing: bool

class AnalyticsDeliveriesResponse(BaseModel):
    data: Dict[str, Any]
    is_syncing: bool

class AnalyticsInventoryResponse(BaseModel):
    data: Dict[str, Any]
    is_syncing: bool

class AnalyticsTasksResponse(BaseModel):
    data: Dict[str, Any]
    is_syncing: bool

# ─── AST / Visual Query Builder Schemas ───────────────────────────────────────

class JoinDef(BaseModel):
    table: str
    onLeft: str
    onRight: str

class FilterDef(BaseModel):
    column: str
    operator: str
    value: Optional[Any] = ""
    valueType: Optional[str] = "value"  # "value", "column", or "date_diff"
    compareColumn: Optional[str] = None
    offsetValue: Optional[str] = None
    diffOp: Optional[str] = None

class MetricCondition(BaseModel):
    column: str
    operator: str
    value: Any

class MetricDef(BaseModel):
    column: str
    aggregation: str
    format: Optional[str] = "number"
    label: Optional[str] = ""
    condition: Optional[MetricCondition] = None
    customExpr: Optional[str] = None

class TimeAxisDef(BaseModel):
    column: Optional[str] = None
    granularity: Optional[str] = "NONE"

class SecondMetricDef(BaseModel):
    column: str = ""
    aggregation: str = ""
    label: str = ""

class VisualQueryBuilderPayload(BaseModel):
    baseTable: str
    joins: list[JoinDef] = []
    filters: list[FilterDef] = []
    metric: Optional[MetricDef] = None
    timeAxis: Optional[TimeAxisDef] = None
    breakdown: Optional[str] = None
    secondMetric: Optional[SecondMetricDef] = None
    metrics: list[MetricDef] = [] # Fase 2: Soporte para tablas anchas
