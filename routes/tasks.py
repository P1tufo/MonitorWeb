import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
import pandas as pd
from datetime import datetime
from core.state import AppState, get_app_state

from core.utils import sanitize_for_json
from repositories import TasksRepository
from services.tasks_service import TasksService

from fastapi import APIRouter, Depends, HTTPException
from core.database import get_session_dep
from core.auth import get_current_user
from core.schemas import AnalyticsTasksResponse

logger = logging.getLogger("routes-analytics-tasks")
router = APIRouter()


def get_tasks_context(session: Session) -> dict:
    return TasksService(session).get_full_context()

@router.get("/api/v1/analytics/tasks", response_model=AnalyticsTasksResponse)
async def analytics_tasks_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state)):
    """API JSON para analíticas de Tareas (Warehouse Tasks)."""
    
    # Intentar recuperar de caché (limpiado de request/user)
    cached_ctx = state.get_cache("/api/v1/analytics/tasks")
    if cached_ctx:
        return AnalyticsTasksResponse(data=cached_ctx, is_syncing=state.is_syncing)

    try:
        service = TasksService(session)
        context = service.get_full_context()
        clean_context = {k: v for k, v in context.items() if k not in ('request', 'user', 'is_syncing')}
        
        state.set_cache("/api/v1/analytics/tasks", clean_context.copy())
        return AnalyticsTasksResponse(data=clean_context, is_syncing=state.is_syncing)

    except Exception as e:
        logger.error(f"Error cargando API tasks: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error cargando los datos de las tareas.")
