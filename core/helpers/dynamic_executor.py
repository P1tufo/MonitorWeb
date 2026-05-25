import pandas as pd
import logging
from typing import Dict
from sqlalchemy.orm import Session
from core.query_engine import build_sql_from_payload
from core.schemas import VisualQueryBuilderPayload

logger = logging.getLogger("dynamic-executor")

def execute_visual_query(payload_dict: Dict, db: Session) -> pd.DataFrame:
    """
    Toma un payload JSON crudo desde el frontend, lo valida y compila usando
    el query_engine, y devuelve un DataFrame de Pandas directamente.
    
    Este es "El Gran Ejecutor" de la Fase 2, que reemplaza todos los métodos
    rígidos de los repositorios.
    """
    try:
        payload = VisualQueryBuilderPayload(**payload_dict)
        sql, bound_params = build_sql_from_payload(payload, db)
        
        # Ejecutamos la consulta y la convertimos a DataFrame
        df = pd.read_sql(sql, db.connection().connection, params=tuple(bound_params))
        return df
    except Exception as e:
        logger.error(f"Error ejecutando consulta dinámica: {e}", exc_info=True)
        return pd.DataFrame()
