"""
core/wms_config.py — Configuración de lógica de negocio y mapeos WMS (SaaS Dinámico).
"""
from typing import Dict, Any
from .db_config_manager import get_setting, get_status_mapping, get_cost_center_mapping, get_holidays, get_query

def validate_wms_maps():
    """Valida la integridad de los mapeos definidos."""
    if not get_status_mapping():
        raise ValueError("STATUS_MAPPING no puede estar vacío.")
    if not get_cost_center_mapping():
        raise ValueError("COST_CENTER_MAPPING no puede estar vacío.")
    
    for k, v in get_cost_center_mapping().items():
        if not v:
            raise ValueError(f"El área de negocio para {k} está vacía.")

# Soporte para carga dinámica (Python 3.7+)
def __getattr__(name: str) -> Any:
    if name == 'STATUS_MAPPING':
        return get_status_mapping()
    elif name == 'COST_CENTER_MAPPING':
        return get_cost_center_mapping()
    
    val = get_setting(name, default=None)
    if val is not None:
        return val
        
    raise AttributeError(f"Módulo '{__name__}' no tiene el atributo '{name}'")

