"""routes/analytics_proyecciones.py — Rutas de analíticas de proyecciones."""
from fastapi import APIRouter, Request, Depends
from core.auth import get_current_user
from fastapi.responses import JSONResponse
from core.state import AppState, get_app_state
from db.predictive_engine import generate_predictions
from config import DB_PATH as _DB

router = APIRouter()

def get_proyecciones_context():
    """Obtiene el contexto de proyecciones, priorizando la caché."""
    state = get_app_state()
    cached = state.get_cache("/analytics/proyecciones")
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
    state.set_cache("/analytics/proyecciones", context)
    return context

@router.get("/analytics/proyecciones")
def get_analytics_proyecciones(request: Request, force_refresh: bool = False, state: AppState = Depends(get_app_state)):
    """Retorna los datos de proyecciones en formato JSON."""
    if force_refresh:
        state.clear_cache("/analytics/proyecciones")
        
    context = get_proyecciones_context()
    return JSONResponse(content=context)
