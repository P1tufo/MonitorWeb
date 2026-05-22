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
