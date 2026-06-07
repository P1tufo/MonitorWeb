import logging
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.auth import get_current_user
from core.database import get_session_dep

logger = logging.getLogger("routes-consumos")
router = APIRouter(prefix="/api/consumos", tags=["Consumos"])

class MaterialesRequest(BaseModel):
    materiales: List[str]

class MaterialTrendRequest(BaseModel):
    material: str
    area_negocio: str = ""
    ceco: str = ""

# La tabla inventory_movements tiene PRIMARY KEY (doc_mat, ej_mat, pos)
# con columnas normalizadas (TRIM aplicado en el ETL), por lo que los
# duplicados son rechazados automaticamente en la insercion.

@router.get("/ceco/{ceco}")
async def get_consumos_ceco(ceco: str, user=Depends(get_current_user), session: Session=Depends(get_session_dep)):
    """
    Obtiene los consumos (CMV 201) agrupados por material para un CeCo específico.
    Retorna el histórico completo y el mes actual.
    Usa deduplicación por doc_mat para evitar doble conteo de archivos cargados.
    """
    try:
        from repositories.inventory import InventoryRepository
        repo = InventoryRepository(session)
        return repo.get_consumos_ceco(ceco)
    except Exception as e:
        logger.error(f"Error fetching consumos for CeCo {ceco}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching consumos por CeCo")

@router.post("/materiales")
async def get_consumos_materiales(req: MaterialesRequest, user=Depends(get_current_user), session: Session=Depends(get_session_dep)):
    """
    Obtiene que CeCos han consumido (CMV 201) una lista de materiales.
    Usa deduplicacion por doc_mat para evitar doble conteo de archivos cargados.
    """
    try:
        from repositories.inventory import InventoryRepository
        repo = InventoryRepository(session)
        return repo.get_consumos_materiales(req.materiales)
    except Exception as e:
        logger.error(f"Error fetching consumos for Materiales: {e}")
        raise HTTPException(status_code=500, detail="Error fetching consumos por Materiales")


@router.post("/materiales/tendencia")
async def get_material_trend(req: MaterialTrendRequest, user=Depends(get_current_user), session: Session=Depends(get_session_dep)):
    """
    Devuelve el consumo mensual (CMV 201) de un material especifico, filtrado por area de negocio.
    Se usa para el grafico de lineas al hacer click en una fila de la tabla de materiales.
    """
    try:
        from repositories.inventory import InventoryRepository
        repo = InventoryRepository(session)
        return repo.get_material_trend(req.material, req.area_negocio, req.ceco)
    except Exception as e:
        logger.error(f"Error fetching trend for material {req.material}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching tendencia de material")
