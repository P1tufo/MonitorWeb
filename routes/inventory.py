"""
routes/analytics_inventory.py — Rutas y lógica de analíticas Movimientos optimizadas.
"""
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.auth import get_current_user
from core.database import get_session_dep
from core.schemas import AnalyticsInventoryResponse
from core.state import CacheManager, SyncStateManager, get_cache_manager, get_sync_manager
from core.utils import sanitize_for_json
from core.wms_config import COST_CENTER_MAPPING
from repositories import InventoryRepository
from routes.analytics_proyecciones import get_proyecciones_context
from services.inventory_service import InventoryService

logger = logging.getLogger("routes-analytics-inventory")
router = APIRouter()

@router.get("/inventory")
async def analytics_inventory_redirect(request: Request):
    return RedirectResponse(url="/analytics?tab=inventory")


def get_inventory_context(session: Session) -> Dict[str, Any]:
    return InventoryService(session).get_full_context()

@router.get("/api/v1/analytics/inventory", response_model=AnalyticsInventoryResponse)
async def analytics_inventory_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager), sync: SyncStateManager = Depends(get_sync_manager)):
    """API JSON para analíticas de Inventario."""

    # Intentar recuperar de caché (limpiado de request/user)
    cached_ctx = cache.get_cache("/api/v1/analytics/inventory")
    if cached_ctx:
        return AnalyticsInventoryResponse(data=cached_ctx, is_syncing=sync.is_syncing)

    try:
        service = InventoryService(session)
        context = service.get_full_context()
        clean_context = {k: v for k, v in context.items() if k not in ('request', 'user', 'is_syncing')}

        cache.set_cache("/api/v1/analytics/inventory", clean_context.copy())
        return AnalyticsInventoryResponse(data=clean_context, is_syncing=sync.is_syncing)

    except Exception as e:
        logger.error(f"Error cargando API inventory: {e}", exc_info=True)
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="Error cargando los datos del inventario.")
