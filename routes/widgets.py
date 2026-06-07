import io
import json
import logging
from typing import Optional

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from core.auth import get_current_user
from core.database import get_session_dep
from core.helpers.dynamic_executor import execute_visual_query
from core.models import ConfigQuery
from core.state import CacheManager, get_cache_manager
from core.utils import sanitize_for_json

logger = logging.getLogger("routes-widgets")
router = APIRouter()

@router.get("/api/widget/{query_id}")
async def get_widget_data(
    query_id: str,
    year: Optional[str] = None,
    area: Optional[str] = None,
    granularity: Optional[str] = None,
    db: Session = Depends(get_session_dep),
    user = Depends(get_current_user),
    cache: CacheManager = Depends(get_cache_manager)
):
    """
    Endpoint universal de Server-Driven UI.
    Ejecuta el VisualQueryBuilderPayload y retorna la data estructurada.
    """
    cache_key = f"widget_{query_id}_{year}_{area}_{granularity}"
    cached = cache.get_cache(cache_key)
    if cached:
        return cached

    row = db.query(ConfigQuery).filter(ConfigQuery.query_id == query_id).first()
    if not row or not row.visual_state:
        raise HTTPException(status_code=404, detail="Widget not found or not initialized properly")

    try:
        from repositories.widgets import WidgetRepository
        repo = WidgetRepository(db)
        result = repo.execute_widget(query_id, row.visual_state, year, area, granularity)
        cache.set_cache(cache_key, result)
        return result
    except Exception as e:
        logger.error(f"Error procesando widget {query_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ha ocurrido un error interno procesando la solicitud.")

@router.get("/api/widget/{query_id}/drilldown")
async def get_widget_drilldown(
    query_id: str,
    segment: str,
    material: Optional[str] = None,
    year: Optional[str] = None,
    area: Optional[str] = None,
    db: Session = Depends(get_session_dep),
    user = Depends(get_current_user)
):
    """
    Endpoint para obtener el detalle subyacente de un segmento de un widget.
    Actualmente soportado: ABC_ANALYSIS.
    """
    row = db.query(ConfigQuery).filter(ConfigQuery.query_id == query_id).first()
    if not row or not row.visual_state:
        raise HTTPException(status_code=404, detail="Widget no encontrado o sin estado visual")

    try:
        from repositories.widgets import WidgetRepository
        repo = WidgetRepository(db)
        return repo.execute_drilldown(query_id, row.visual_state, segment, material, year)
    except Exception as e:
        logger.error(f"Error procesando drilldown para widget {query_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ha ocurrido un error interno procesando la solicitud.")

@router.get("/api/custom/cmv201_summary")
async def get_cmv201_summary(
    plan_type: str = Query(..., description="Planificado o Desplanificado"),
    year: Optional[str] = None,
    db: Session = Depends(get_session_dep),
    user = Depends(get_current_user)
):
    """
    Endpoint custom para el modal CMV 201 Mensual.
    Muestra la cantidad de materiales solicitados por área de negocio y mes.
    """
    try:
        from repositories.inventory import InventoryRepository
        repo = InventoryRepository(db)
        return repo.get_cmv_summary(cmv_type="201", plan_type=plan_type, year=year)
    except Exception as e:
        logger.error(f"Error en get_cmv201_summary: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ha ocurrido un error interno procesando la solicitud.")

@router.get("/api/custom/cmv201_area_details")
def get_cmv201_area_details(
    plan_type: str = Query("planificado", description="'planificado' o 'desplanificado'"),
    area: str = Query(..., description="Area de negocio filtrada"),
    mes: str = Query(None, description="Mes en formato YYYY-MM. Si no se provee, no se filtra por mes."),
    year: str = Query(None, description="Año"),
    db: Session = Depends(get_session_dep)
):
    try:
        from repositories.inventory import InventoryRepository
        repo = InventoryRepository(db)
        return repo.get_cmv_area_details(cmv_type="201", plan_type=plan_type, area=area, mes=mes, year=year)
    except Exception as e:
        logger.error(f"Error en get_cmv201_area_details: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ha ocurrido un error interno procesando la solicitud.")

@router.get("/api/custom/cmv261_summary")
def get_cmv261_summary(
    plan_type: str = Query("planificado", description="'planificado' o 'desplanificado'"),
    year: str = Query(None, description="Año"),
    db: Session = Depends(get_session_dep)
):
    try:
        from repositories.inventory import InventoryRepository
        repo = InventoryRepository(db)
        return repo.get_cmv_summary(cmv_type="261", plan_type=plan_type, year=year)
    except Exception as e:
        logger.error(f"Error en get_cmv261_summary: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ha ocurrido un error interno procesando la solicitud.")

@router.get("/api/custom/cmv261_area_details")
def get_cmv261_area_details(
    plan_type: str = Query("planificado", description="'planificado' o 'desplanificado'"),
    area: str = Query(..., description="Area de negocio filtrada"),
    mes: str = Query(None, description="Mes en formato YYYY-MM. Si no se provee, no se filtra por mes."),
    year: str = Query(None, description="Año"),
    db: Session = Depends(get_session_dep)
):
    try:
        from repositories.inventory import InventoryRepository
        repo = InventoryRepository(db)
        return repo.get_cmv_area_details(cmv_type="261", plan_type=plan_type, area=area, mes=mes, year=year)
    except Exception as e:
        logger.error(f"Error en get_cmv261_area_details: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ha ocurrido un error interno procesando la solicitud.")

@router.get("/api/inventory/replenishment-suggestions")
async def get_replenishment_suggestions(
    freq: str = Query("all", description="Filtro de frecuencia: all, 1, 3, 6, 12"),
    db: Session = Depends(get_session_dep)
):
    """
    Calcula sugerencias de pedido basándose en el stock inicial MB5B y el ritmo de consumo.
    Muestra los materiales con autonomía < 1 mes.
    """
    try:
        from repositories.inventory import InventoryRepository
        repo = InventoryRepository(db)
        return repo.get_replenishment_suggestions(freq)
    except Exception as e:
        logger.error(f"Error en get_replenishment_suggestions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ha ocurrido un error interno procesando la solicitud.")

@router.get("/api/inventory/replenishment-suggestions/export")
async def export_replenishment_suggestions(db: Session = Depends(get_session_dep)):
    """
    Exporta todas las sugerencias de pedido (Autonomía < 1) a un archivo Excel.
    """
    try:
        from repositories.inventory import InventoryRepository
        repo = InventoryRepository(db)
        df_main, df_areas = repo.get_replenishment_export_data()

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Hoja Principal
            df_main.to_excel(writer, index=False, sheet_name='Sugerencias Consolidadas')
            worksheet = writer.sheets['Sugerencias Consolidadas']
            for i, col in enumerate(df_main.columns):
                max_length = max(df_main[col].astype(str).map(len).max() if not df_main.empty else 0, len(col)) + 2
                worksheet.column_dimensions[chr(65 + i)].width = min(max_length, 60)

            # Hojas por Área
            if not df_areas.empty:
                areas = df_areas["Área de Negocio"].unique()
                for area in areas:
                    safe_area_name = str(area)[:31] # Excel sheet name limit is 31 chars
                    df_area = df_areas[df_areas["Área de Negocio"] == area].drop(columns=["Área de Negocio"])
                    df_area.to_excel(writer, index=False, sheet_name=safe_area_name)

                    ws = writer.sheets[safe_area_name]
                    for i, col in enumerate(df_area.columns):
                        max_length = max(df_area[col].astype(str).map(len).max() if not df_area.empty else 0, len(col)) + 2
                        ws.column_dimensions[chr(65 + i)].width = min(max_length, 60)

        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=Sugerencias_Pedido_Urgente.xlsx"}
        )
    except Exception as e:
        logger.error(f"Error exporting replenishment suggestions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Ha ocurrido un error interno procesando la solicitud.")
