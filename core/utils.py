"""
core/utils.py — Utilidades transversales y gestión de señales del sistema.
"""
import signal
import sys
import logging
import pandas as pd
import math
from typing import Final, Any

logger = logging.getLogger("app-utils")

# Flag interno para evitar registros múltiples
_handlers_registered = False

def setup_signal_handlers() -> None:
    """Configura los manejadores de señales (SIGINT, SIGTERM) para un cierre limpio."""
    global _handlers_registered
    if _handlers_registered: return

    def _handle_exit(sig: int, frame: object) -> None:
        logger.info(f"Señal de cierre recibida ({sig}). Finalizando procesos...")
        try:
            from services.tunnel import stop_tunnel
            stop_tunnel()
        except: pass
        sys.exit(0)

    try:
        signal.signal(signal.SIGINT, _handle_exit)
        signal.signal(signal.SIGTERM, _handle_exit)
        _handlers_registered = True
    except: pass

def log_startup_banner():
    logger.info("MonitorWeb Core Utility Module Initialized.")

def sanitize_for_json(data: Any) -> Any:
    """
    Limpia datos para serialización JSON segura de forma recursiva y exhaustiva.
    Convierte NaNs, Infs y Timestamps a formatos compatibles con JSON.
    """
    # 1. Manejo de tipos complejos de Pandas
    if isinstance(data, pd.DataFrame):
        return sanitize_for_json(data.to_dict(orient="records"))
    if isinstance(data, pd.Series):
        return sanitize_for_json(data.to_dict())

    # 2. Manejo de estructuras de datos (Recursión)
    if isinstance(data, list):
        return [sanitize_for_json(item) for item in data]
    if isinstance(data, dict):
        return {str(k): sanitize_for_json(v) for k, v in data.items()}

    # 3. Manejo de valores atómicos (Hojas)
    if isinstance(data, float):
        if math.isnan(data) or math.isinf(data):
            return None
        return data
    
    # Manejo de fechas de pandas (Timestamp)
    if hasattr(data, 'isoformat'):
        return data.isoformat()

    return data

def _get_bound_params_from_visual_state(visual_state_str: str) -> list:
    """
    Alias de compatibilidad → core/query_engine.get_bound_params_from_visual_state.
    La implementación canónica vive en el motor para evitar duplicación.
    """
    from core.query_engine import get_bound_params_from_visual_state
    return get_bound_params_from_visual_state(visual_state_str)

def _extract_metric_value(df, active_year: str = None) -> Any:
    """
    Alias de compatibilidad → core/query_engine.extract_metric_value.
    La implementación canónica vive en el motor para evitar duplicación.
    """
    from core.query_engine import extract_metric_value
    return extract_metric_value(df, active_year)
