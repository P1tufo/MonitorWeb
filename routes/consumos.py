from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any
from pydantic import BaseModel
import pandas as pd
from core.database import get_session_dep
from core.auth import get_current_user
import logging
from datetime import datetime

logger = logging.getLogger("routes-consumos")
router = APIRouter(prefix="/api/consumos", tags=["Consumos"])

class MaterialesRequest(BaseModel):
    materiales: List[str]

@router.get("/ceco/{ceco}")
async def get_consumos_ceco(ceco: str, user=Depends(get_current_user), session: Session=Depends(get_session_dep)):
    """
    Obtiene los consumos (CMV 201) agrupados por material para un CeCo específico.
    Retorna el histórico completo y el mes actual.
    """
    ceco_clean = ceco.strip().upper()
    try:
        # Consulta Histórica
        query_hist = f"""
            SELECT 
                material,
                MAX(texto_breve_material) as descripcion,
                SUM(cantidad) * -1 as cantidad_total,
                SUM(importe_ml) * -1 as costo_total
            FROM inventory_movements
            WHERE cmv = '201' 
              AND UPPER(TRIM(ce_coste)) = :ceco
            GROUP BY material
            ORDER BY costo_total DESC
        """
        df_hist = pd.read_sql(text(query_hist), session.connection(), params={"ceco": ceco_clean})
        df_hist = df_hist.astype(object).where(pd.notnull(df_hist), None)

        # Consulta Mes Actual
        current_month_str = datetime.now().strftime('%m-%Y')
        query_mes = f"""
            SELECT 
                material,
                MAX(texto_breve_material) as descripcion,
                SUM(cantidad) * -1 as cantidad_total,
                SUM(importe_ml) * -1 as costo_total
            FROM inventory_movements
            WHERE cmv = '201' 
              AND UPPER(TRIM(ce_coste)) = :ceco
              AND fe_contab LIKE :month
            GROUP BY material
            ORDER BY costo_total DESC
        """
        df_mes = pd.read_sql(text(query_mes), session.connection(), params={"ceco": ceco_clean, "month": f"%{current_month_str}"})
        df_mes = df_mes.astype(object).where(pd.notnull(df_mes), None)

        return {
            "historico": df_hist.to_dict(orient="records"),
            "mes_actual": df_mes.to_dict(orient="records")
        }
    except Exception as e:
        logger.error(f"Error fetching consumos for CeCo {ceco}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching consumos por CeCo")

@router.post("/materiales")
async def get_consumos_materiales(req: MaterialesRequest, user=Depends(get_current_user), session: Session=Depends(get_session_dep)):
    """
    Obtiene qué CeCos han consumido (CMV 201) una lista de materiales.
    """
    mats_clean = [m.strip().upper() for m in req.materiales if m.strip()]
    if not mats_clean:
        return {"data": []}

    try:
        # SQLite IN clause limitation is around 999, but we expect ~25 from the UI
        placeholders = ",".join([f":m{i}" for i in range(len(mats_clean))])
        params = {f"m{i}": m for i, m in enumerate(mats_clean)}

        current_month_str = datetime.now().strftime('%m-%Y')
        
        query = f"""
            SELECT 
                material,
                MAX(texto_breve_material) as descripcion,
                COALESCE((SELECT MAX(area_negocio) 
                 FROM outbound_deliveries o 
                 WHERE UPPER(TRIM(o.centro_costo)) = UPPER(TRIM(inventory_movements.ce_coste))
                   AND o.area_negocio IS NOT NULL 
                   AND TRIM(o.area_negocio) != ''), 'SIN ÁREA') as area_negocio,
                SUM(CASE WHEN fe_contab LIKE :month THEN cantidad ELSE 0 END) * -1 as cantidad_mes,
                SUM(CASE WHEN fe_contab LIKE :month THEN importe_ml ELSE 0 END) * -1 as costo_mes,
                SUM(cantidad) * -1 as cantidad_total,
                SUM(importe_ml) * -1 as costo_total
            FROM inventory_movements
            WHERE cmv = '201'
              AND UPPER(TRIM(material)) IN ({placeholders})
            GROUP BY material, area_negocio
            ORDER BY material ASC, costo_total DESC
        """
        params["month"] = f"%{current_month_str}"
        df = pd.read_sql(text(query), session.connection(), params=params)
        df = df.astype(object).where(pd.notnull(df), None)

        return {"data": df.to_dict(orient="records")}
    except Exception as e:
        logger.error(f"Error fetching consumos for Materiales: {e}")
        raise HTTPException(status_code=500, detail="Error fetching consumos por Materiales")
