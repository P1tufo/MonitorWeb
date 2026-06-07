"""routes/analytics_proyecciones.py — Rutas de analíticas de proyecciones."""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from config import DB_PATH as _DB
from core.auth import get_current_user
from core.state import CacheManager, get_cache_manager
from db.predictive_engine import generate_predictions

router = APIRouter()

def get_proyecciones_context():
    """Obtiene el contexto de proyecciones, priorizando la caché."""
    cache = get_cache_manager()
    cached = cache.get_cache("/analytics/proyecciones")
    if cached:
        return cached.copy()

    predictions = generate_predictions(_DB)
    if "error" in predictions:
        return {"error_msg": predictions["error"], "combos": [], "scatter_data": [], "alerts": []}

    context = {
        "combos": predictions.get("combos", []),
        "scatter_data": predictions.get("scatter_data", []),
        "alerts": predictions.get("alerts", [])
    }

    # Guardar en caché si es exitoso
    cache.set_cache("/analytics/proyecciones", context)
    return context

@router.get("/analytics/proyecciones")
def get_analytics_proyecciones(request: Request, force_refresh: bool = False, cache: CacheManager = Depends(get_cache_manager)):
    """Retorna los datos de proyecciones en formato JSON."""
    if force_refresh:
        cache.clear_cache("/analytics/proyecciones")

    context = get_proyecciones_context()
    return JSONResponse(content=context)
