import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.auth import get_current_user
from core.database import get_session_dep
from core.state import CacheManager, SyncStateManager, get_cache_manager, get_sync_manager
from services.productivity_daily import ProductivityDailyService
from services.productivity_monthly import ProductivityMonthlyService

logger = logging.getLogger("routes-productivity")
router = APIRouter()

@router.get("/api/v1/analytics/productivity/available-dates")
async def get_available_dates(
    user = Depends(get_current_user),
    session: Session = Depends(get_session_dep)
):
    service = ProductivityDailyService(session)
    dates = service.get_available_dates()
    return {"data": dates}

@router.get("/api/v1/analytics/productivity")
async def get_productivity_dashboard(
    date: str = Query(None, description="Fecha objetivo en formato YYYY-MM-DD"),
    user = Depends(get_current_user),
    session: Session = Depends(get_session_dep),
    cache: CacheManager = Depends(get_cache_manager),
    sync: SyncStateManager = Depends(get_sync_manager)
):
    """
    Retorna todos los datos necesarios para el dashboard de productividad MB51.
    """
    if not date:
        # Por defecto "Ayer"
        ayer = datetime.now() - timedelta(days=1)
        date = ayer.strftime("%Y-%m-%d")

    cache_key = f"/api/v1/analytics/productivity?date={date}"

    # Intentar recuperar de caché si no estamos sincronizando
    # if not state.is_syncing:
    #     cached_ctx = state.get_cache(cache_key)
    #     if cached_ctx:
    #         return {"data": cached_ctx, "is_syncing": False}

    try:
        service = ProductivityDailyService(session)
        data = service.get_productivity_data(date)

        cache.set_cache(cache_key, data)
        return {"data": data, "is_syncing": sync.is_syncing}

    except Exception as e:
        logger.error(f"Error cargando API productivity: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error cargando los datos de productividad.")

@router.get("/api/v1/analytics/productivity/monthly")
async def get_monthly_productivity(
    month: str = Query(None, description="Mes objetivo en formato YYYY-MM"),
    user = Depends(get_current_user),
    session: Session = Depends(get_session_dep),
    cache: CacheManager = Depends(get_cache_manager),
    sync: SyncStateManager = Depends(get_sync_manager)
):
    """
    Retorna los KPIs mensuales de productividad.
    """
    if not month:
        # Por defecto mes actual
        month = datetime.now().strftime("%Y-%m")

    cache_key = f"/api/v1/analytics/productivity/monthly?month={month}"

    # if not state.is_syncing:
    #     cached_ctx = state.get_cache(cache_key)
    #     if cached_ctx:
    #         return {"data": cached_ctx, "is_syncing": False}

    try:
        service = ProductivityMonthlyService(session)
        data = service.get_monthly_productivity_data(month)

        cache.set_cache(cache_key, data)
        return {"data": data, "is_syncing": sync.is_syncing}

    except Exception as e:
        logger.error(f"Error cargando API productivity monthly: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error cargando los datos mensuales.")

@router.get("/api/v1/analytics/productivity/user-movements-summary")
async def get_user_movements_summary(
    date: str = Query(..., description="Fecha objetivo en formato YYYY-MM-DD"),
    usuario: str = Query(..., description="ID del usuario"),
    user = Depends(get_current_user),
    session: Session = Depends(get_session_dep)
):
    try:
        service = ProductivityDailyService(session)
        data = service.get_user_movements_daily_summary(date, usuario)
        return {"data": data}
    except Exception as e:
        logger.error(f"Error cargando resumen diario de {usuario}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error cargando el resumen diario.")

@router.get("/api/v1/analytics/productivity/user-movements-details")
async def get_user_movements_details(
    date: str = Query(..., description="Fecha objetivo en formato YYYY-MM-DD"),
    usuario: str = Query(..., description="ID del usuario"),
    operacion: str = Query(..., description="Tipo de operación"),
    user = Depends(get_current_user),
    session: Session = Depends(get_session_dep)
):
    try:
        service = ProductivityDailyService(session)
        data = service.get_user_movements_daily_details(date, usuario, operacion)
        return {"data": data}
    except Exception as e:
        logger.error(f"Error cargando detalle diario de {usuario}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error cargando el detalle diario.")

@router.get("/api/v1/analytics/productivity/user-movements-monthly-summary")
async def get_user_movements_monthly_summary(
    month: str = Query(..., description="Mes objetivo en formato YYYY-MM"),
    usuario: str = Query(..., description="ID del usuario"),
    user = Depends(get_current_user),
    session: Session = Depends(get_session_dep)
):
    try:
        service = ProductivityMonthlyService(session)
        data = service.get_user_movements_monthly_summary(month, usuario)
        return {"data": data}
    except Exception as e:
        logger.error(f"Error cargando resumen mensual de {usuario}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error cargando el resumen mensual.")

@router.get("/api/v1/analytics/productivity/user-movements-monthly-details")
async def get_user_movements_monthly_details(
    month: str = Query(..., description="Mes objetivo en formato YYYY-MM"),
    usuario: str = Query(..., description="ID del usuario"),
    operacion: str = Query(..., description="Tipo de operación"),
    user = Depends(get_current_user),
    session: Session = Depends(get_session_dep)
):
    try:
        service = ProductivityMonthlyService(session)
        data = service.get_user_movements_monthly_details(month, usuario, operacion)
        return {"data": data}
    except Exception as e:
        logger.error(f"Error cargando detalle mensual de {usuario}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error cargando el detalle mensual.")
