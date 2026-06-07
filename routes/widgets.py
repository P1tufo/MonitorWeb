import json
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
import io
import pandas as pd
from sqlalchemy.orm import Session

from core.database import get_session_dep
from core.models import ConfigQuery
from core.auth import get_current_user
from core.helpers.dynamic_executor import execute_visual_query
from core.utils import sanitize_for_json
from core.state import get_app_state, AppState

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
    state: AppState = Depends(get_app_state)
):
    """
    Endpoint universal de Server-Driven UI.
    Ejecuta el VisualQueryBuilderPayload y retorna la data estructurada.
    """
    cache_key = f"widget_{query_id}_{year}_{area}_{granularity}"
    cached = state.get_cache(cache_key)
    if cached:
        return cached

    row = db.query(ConfigQuery).filter(ConfigQuery.query_id == query_id).first()
    if not row or not row.visual_state:
        raise HTTPException(status_code=404, detail="Widget not found or not initialized properly")

    try:
        from repositories.widgets import WidgetRepository
        repo = WidgetRepository(db)
        result = repo.execute_widget(query_id, row.visual_state, year, area, granularity)
        state.set_cache(cache_key, result)
        return result
    except Exception as e:
        logger.error(f"Error procesando widget {query_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

    try:
        payload_dict = json.loads(row.visual_state)
        filters = payload_dict.get("filters", [])
        
        # Sobrescritura con Filtros Globales (Intersección)
        if year:
            date_col_updated = False
            for f in filters:
                if f.get("valueType") == "value" and f.get("operator") == "contains" and ("fecha" in f.get("column", "") or "fe_contab" in f.get("column", "")):
                    f["value"] = year
                    date_col_updated = True
            
            if not date_col_updated:
                # Si no existía, inyectamos uno heurístico
                base_table = payload_dict.get("baseTable", "outbound_deliveries")
                date_col = f"{base_table}.fecha_carga" if base_table == "outbound_deliveries" else f"{base_table}.fe_contab"
                filters.append({
                    "column": date_col,
                    "operator": "contains",
                    "value": year,
                    "valueType": "value"
                })
        
        # Inyectar filtro de área dinámico (evaluando AREA_EXPR en WHERE)
        if area and area.strip() != "":
            base_table = payload_dict.get("baseTable", "outbound_deliveries")
            if base_table == "outbound_deliveries":
                filters.append({
                    "column": "__AREA_EXPR__",
                    "operator": "in",
                    "value": area,
                    "valueType": "value"
                })
        
        if granularity and "timeAxis" in payload_dict and payload_dict["timeAxis"]:
            if query_id != "inv_dow_stats":
                payload_dict["timeAxis"]["granularity"] = granularity
            
        payload_dict["filters"] = filters
        
        chart_type = payload_dict.get("chartType", "bar")
        
        # Ejecutar SQL dinámico
        df = execute_visual_query(payload_dict, db)
        
        # Formatear salida para el Frontend
        labels = []
        datasets = []
        raw_data = []
        
        if not df.empty:
            raw_data = sanitize_for_json(df)
            
            # Eliminar el eje de tiempo dummy si no hay granularidad real
            if "fecha" in df.columns and (df["fecha"] == "Total").all():
                df = df.drop(columns=["fecha"])

            # Formatear para Chart.js si hay desglose o ejes de tiempo
            if "categoria" in df.columns or "fecha" in df.columns:
                # Si hay fecha y categoría (series múltiples)
                if "fecha" in df.columns and "categoria" in df.columns:
                    pivot = df.pivot_table(index="fecha", columns="categoria", values=df.columns[-1], aggfunc="sum").fillna(0)
                    labels = pivot.index.tolist()
                    for col in pivot.columns:
                        datasets.append({
                            "label": str(col),
                            "data": pivot[col].tolist()
                        })
                # Si solo hay categoría (ej. Doughnut, Bar simple)
                elif "categoria" in df.columns:
                    labels = df["categoria"].tolist()
                    metric_cols = [c for c in df.columns if c not in ("fecha", "categoria")]
                    for col in metric_cols:
                        datasets.append({
                            "label": str(col),
                            "data": df[col].tolist()
                        })
                # Si solo hay tiempo (ej. Line chart global)
                elif "fecha" in df.columns:
                    labels = df["fecha"].tolist()
                    metric_cols = [c for c in df.columns if c != "fecha"]
                    for col in metric_cols:
                        datasets.append({
                            "label": str(col),
                            "data": df[col].tolist()
                        })
            else:
                # KPI numérico o tabla sin agrupación explícita
                pass

        metrics_list = payload_dict.get("metrics", [])
        if not metrics_list:
            if payload_dict.get("metric"):
                metrics_list.append(payload_dict.get("metric"))
            if payload_dict.get("secondMetric"):
                metrics_list.append(payload_dict.get("secondMetric"))
        
        dataset_formats = {}
        for m in metrics_list:
            if m and m.get("label"):
                dataset_formats[m.get("label")] = m.get("format", "number")

        format_type = payload_dict.get("metric", {}).get("format", "number")
        result = {
            "query_id": query_id,
            "chartType": chart_type,
            "title": query_id.replace("_", " ").title(),
            "labels": labels,
            "datasets": datasets,
            "raw_data": raw_data,
            "isEmpty": df.empty,
            "format": format_type,
            "dataset_formats": dataset_formats
        }
        
        state.set_cache(cache_key, result)
        return result

    except Exception as e:
        logger.error(f"Error procesando widget {query_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

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
        raise HTTPException(status_code=500, detail=str(e))

    try:
        payload_dict = json.loads(row.visual_state)
        filters = payload_dict.get("filters", [])
        
        # Sobrescritura con Filtros Globales (Intersección)
        if year:
            date_col_updated = False
            for f in filters:
                if f.get("valueType") == "value" and f.get("operator") == "contains" and ("fecha" in f.get("column", "") or "fe_contab" in f.get("column", "")):
                    f["value"] = year
                    date_col_updated = True
            
            if not date_col_updated:
                # Si no existía, inyectamos uno heurístico
                base_table = payload_dict.get("baseTable", "outbound_deliveries")
                date_col = f"{base_table}.fecha_carga" if base_table == "outbound_deliveries" else f"{base_table}.fe_contab"
                filters.append({
                    "column": date_col,
                    "operator": "contains",
                    "value": year,
                    "valueType": "value"
                })
        
        # Inyectar filtro de área dinámico (evaluando AREA_EXPR en WHERE)
        if area and area.strip() != "":
            base_table = payload_dict.get("baseTable", "outbound_deliveries")
            if base_table == "outbound_deliveries":
                filters.append({
                    "column": "__AREA_EXPR__",
                    "operator": "in",
                    "value": area,
                    "valueType": "value"
                })
        
        if granularity and "timeAxis" in payload_dict and payload_dict["timeAxis"]:
            if query_id != "inv_dow_stats":
                payload_dict["timeAxis"]["granularity"] = granularity
            
        payload_dict["filters"] = filters
        
        chart_type = payload_dict.get("chartType", "bar")
        
        # Ejecutar SQL dinámico
        df = execute_visual_query(payload_dict, db)
        
        # Formatear salida para el Frontend
        labels = []
        datasets = []
        raw_data = []
        
        if not df.empty:
            raw_data = sanitize_for_json(df)
            
            # Eliminar el eje de tiempo dummy si no hay granularidad real
            if "fecha" in df.columns and (df["fecha"] == "Total").all():
                df = df.drop(columns=["fecha"])

            # Formatear para Chart.js si hay desglose o ejes de tiempo
            if "categoria" in df.columns or "fecha" in df.columns:
                # Si hay fecha y categoría (series múltiples)
                if "fecha" in df.columns and "categoria" in df.columns:
                    pivot = df.pivot_table(index="fecha", columns="categoria", values=df.columns[-1], aggfunc="sum").fillna(0)
                    labels = pivot.index.tolist()
                    for col in pivot.columns:
                        datasets.append({
                            "label": str(col),
                            "data": pivot[col].tolist()
                        })
                # Si solo hay categoría (ej. Doughnut, Bar simple)
                elif "categoria" in df.columns:
                    labels = df["categoria"].tolist()
                    metric_cols = [c for c in df.columns if c not in ("fecha", "categoria")]
                    for col in metric_cols:
                        datasets.append({
                            "label": str(col),
                            "data": df[col].tolist()
                        })
                # Si solo hay tiempo (ej. Line chart global)
                elif "fecha" in df.columns:
                    labels = df["fecha"].tolist()
                    metric_cols = [c for c in df.columns if c != "fecha"]
                    for col in metric_cols:
                        datasets.append({
                            "label": str(col),
                            "data": df[col].tolist()
                        })
            else:
                # KPI numérico o tabla sin agrupación explícita
                pass

        metrics_list = payload_dict.get("metrics", [])
        if not metrics_list:
            if payload_dict.get("metric"):
                metrics_list.append(payload_dict.get("metric"))
            if payload_dict.get("secondMetric"):
                metrics_list.append(payload_dict.get("secondMetric"))
        
        dataset_formats = {}
        for m in metrics_list:
            if m and m.get("label"):
                dataset_formats[m.get("label")] = m.get("format", "number")

        format_type = payload_dict.get("metric", {}).get("format", "number")
        result = {
            "query_id": query_id,
            "chartType": chart_type,
            "title": query_id.replace("_", " ").title(),
            "labels": labels,
            "datasets": datasets,
            "raw_data": raw_data,
            "isEmpty": df.empty,
            "format": format_type,
            "dataset_formats": dataset_formats
        }
        
        state.set_cache(cache_key, result)
        return result

    except Exception as e:
        logger.error(f"Error procesando widget {query_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

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
        from core.schemas import VisualQueryBuilderPayload
        from sqlalchemy import text
        import pandas as pd
        
        payload_dict = json.loads(row.visual_state)
        filters = payload_dict.get("filters", [])
        if year:
            date_col_updated = False
            for f in filters:
                if f.get("valueType") == "value" and f.get("operator") == "contains" and ("fecha" in f.get("column", "") or "fe_contab" in f.get("column", "")):
                    f["value"] = year
                    date_col_updated = True
            if not date_col_updated:
                base_table = payload_dict.get("baseTable", "outbound_deliveries")
                date_col = f"{base_table}.fecha_carga" if base_table == "outbound_deliveries" else f"{base_table}.fe_contab"
                filters.append({
                    "column": date_col,
                    "operator": "contains",
                    "value": year,
                    "valueType": "value"
                })
        payload_dict["filters"] = filters

        if query_id in ("vl_sla_area_monthly_trend", "vl_sla_area_trend") and segment:
            from core.macros import AREA_EXPR as AREA_EXPR_MACRO
            if material:
                sql = """
                SELECT 
                    fecha_carga AS "Fecha",
                    entrega AS "Entrega",
                    pos_ AS "Pos",
                    cantidad AS "Cantidad",
                    dias_retraso AS "Días Retraso"
                FROM outbound_deliveries
                WHERE __AREA_EXPR__ = ? AND material = ? AND fecha_carga IS NOT NULL AND fecha_carga != ''
                """
                bound_params = [segment, material]
                if year:
                    sql += " AND fecha_carga LIKE ?"
                    bound_params.append(f"%{year}%")
                sql += " ORDER BY substr(fecha_carga, 7, 4) || '-' || substr(fecha_carga, 4, 2) || '-' || substr(fecha_carga, 1, 2) DESC LIMIT 50"
                sql = sql.replace("__AREA_EXPR__", AREA_EXPR_MACRO.replace("v.", "outbound_deliveries."))
            else:
                sql = """
                SELECT 
                    material AS "Material",
                    MAX(denominacion) AS "Descripción",
                    COUNT(*) AS "Frecuencia (Veces)",
                    ROUND((julianday(MAX(substr(fecha_carga, 7, 4) || '-' || substr(fecha_carga, 4, 2) || '-' || substr(fecha_carga, 1, 2))) - 
                           julianday(MIN(substr(fecha_carga, 7, 4) || '-' || substr(fecha_carga, 4, 2) || '-' || substr(fecha_carga, 1, 2)))) / NULLIF(COUNT(*) - 1, 0), 1) AS "Frecuencia en Días (Prom)",
                    ROUND(ABS(AVG(cantidad)), 1) AS "Cant. Prom. por Solicitud"
                FROM outbound_deliveries
                WHERE __AREA_EXPR__ = ? AND fecha_carga IS NOT NULL AND fecha_carga != ''
                """
                bound_params = [segment]
                if year:
                    sql += " AND fecha_carga LIKE ?"
                    bound_params.append(f"%{year}%")
                
                sql += """
                GROUP BY material
                ORDER BY "Frecuencia (Veces)" DESC
                LIMIT 50
                """
                sql = sql.replace("__AREA_EXPR__", AREA_EXPR_MACRO.replace("v.", "outbound_deliveries."))
        else:
            from core.query_engine import build_sql_from_payload
            payload = VisualQueryBuilderPayload(**payload_dict)
            sql, bound_params = build_sql_from_payload(payload, db, drilldown_segment=segment, drilldown_material=material)
        
        df = pd.read_sql(sql, db.connection().connection, params=tuple(bound_params))
        
        raw_data = sanitize_for_json(df) if not df.empty else []
        return raw_data
    except Exception as e:
        logger.error(f"Error procesando drilldown para widget {query_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

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
    from core.macros import AREA_EXPR as AREA_EXPR_MACRO
    from sqlalchemy import text
    import pandas as pd

    try:
        # Base table: inventory_movements
        # Filtro: cmv = 201
        
        # Filtro de tipo planificado:
        if plan_type.lower() == "planificado":
            plan_filter = '''(
                (inventory_movements.referencia GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR inventory_movements.referencia GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR
                inventory_movements.texto_cab_documento GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR inventory_movements.texto_cab_documento GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*')
            )'''
        else: # Desplanificado
            plan_filter = '''NOT (
                (COALESCE(inventory_movements.referencia, '') GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR COALESCE(inventory_movements.referencia, '') GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR
                COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*')
            ) AND
            COALESCE(inventory_movements.texto_cab_documento, '') NOT LIKE '%cierre%' AND
            COALESCE(inventory_movements.texto_cab_documento, '') NOT LIKE '%dev%' AND
            COALESCE(inventory_movements.texto_cab_documento, '') NOT LIKE '%mes%' AND
            COALESCE(inventory_movements.referencia, '') NOT LIKE '%cierre%' AND
            COALESCE(inventory_movements.referencia, '') NOT LIKE '%dev%' AND
            COALESCE(inventory_movements.referencia, '') NOT LIKE '%mes%'
            '''

        area_expr = "COALESCE((SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(inventory_movements.ce_coste, 1, 6)), 'Mantencion')"
        
        sql = f"""
        SELECT 
            {area_expr} AS area_negocio,
            substr(inventory_movements.fe_contab, 7, 4) || '-' || substr(inventory_movements.fe_contab, 4, 2) AS mes,
            COUNT(inventory_movements.material) AS cantidad
        FROM inventory_movements
        WHERE inventory_movements.cmv = '201' 
          AND {plan_filter}
        """
        
        bound_params = []
        if year:
            sql += " AND inventory_movements.fe_contab LIKE ?"
            bound_params.append(f"%{year}%")
            
        sql += """
        GROUP BY 1, 2
        ORDER BY 1, 2
        """
        
        df = pd.read_sql(sql, db.connection().connection, params=tuple(bound_params))
        
        if df.empty:
            return []
            
        return sanitize_for_json(df)
        
    except Exception as e:
        logger.error(f"Error procesando cmv201_summary: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/custom/cmv201_area_details")
def get_cmv201_area_details(
    plan_type: str = Query("planificado", description="'planificado' o 'desplanificado'"),
    area: str = Query(..., description="Area de negocio filtrada"),
    mes: str = Query(None, description="Mes en formato YYYY-MM. Si no se provee, no se filtra por mes."),
    year: str = Query(None, description="Año"),
    db: Session = Depends(get_session_dep)
):
    import pandas as pd

    try:
        if plan_type.lower() == "planificado":
            plan_filter = '''(
                (COALESCE(inventory_movements.referencia, '') GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR COALESCE(inventory_movements.referencia, '') GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR
                COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*')
            )'''
        else:
            plan_filter = '''NOT (
                (COALESCE(inventory_movements.referencia, '') GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR COALESCE(inventory_movements.referencia, '') GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR
                COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*')
            ) AND
            COALESCE(inventory_movements.texto_cab_documento, '') NOT LIKE '%cierre%' AND
            COALESCE(inventory_movements.texto_cab_documento, '') NOT LIKE '%dev%' AND
            COALESCE(inventory_movements.texto_cab_documento, '') NOT LIKE '%mes%' AND
            COALESCE(inventory_movements.referencia, '') NOT LIKE '%cierre%' AND
            COALESCE(inventory_movements.referencia, '') NOT LIKE '%dev%' AND
            COALESCE(inventory_movements.referencia, '') NOT LIKE '%mes%'
            '''

        area_expr = "COALESCE((SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(inventory_movements.ce_coste, 1, 6)), 'Mantencion')"
        
        sql = f"""
        SELECT 
            inventory_movements.material,
            inventory_movements.texto_breve_material,
            COUNT(*) AS frecuencia,
            ROUND(AVG(inventory_movements.cantidad * -1), 2) AS promedio_retiro,
            ROUND(30.0 / COUNT(*), 1) AS dias_frecuencia
        FROM inventory_movements
        WHERE inventory_movements.cmv = '201' 
          AND {plan_filter}
        """
        
        bound_params = []
        if area:
            sql += f" AND {area_expr} = ?"
            bound_params.append(area)

        if mes:
            sql += " AND (substr(inventory_movements.fe_contab, 7, 4) || '-' || substr(inventory_movements.fe_contab, 4, 2)) = ?"
            bound_params.append(mes)
        elif year:
            sql += " AND inventory_movements.fe_contab LIKE ?"
            bound_params.append(f"%{year}%")
            
        sql += """
        GROUP BY inventory_movements.material, inventory_movements.texto_breve_material
        ORDER BY frecuencia DESC
        """
        
        df = pd.read_sql(sql, db.connection().connection, params=tuple(bound_params))
        
        if df.empty:
            return []
            
        return sanitize_for_json(df)
        
    except Exception as e:
        logger.error(f"Error procesando cmv201_area_details: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/custom/cmv261_summary")
def get_cmv261_summary(
    plan_type: str = Query("planificado", description="'planificado' o 'desplanificado'"),
    year: str = Query(None, description="Año"),
    db: Session = Depends(get_session_dep)
):
    import pandas as pd

    try:
        # Filtro de tipo planificado para CMV 261:
        # Se excluye explicitamente PGP porque es mantencion anual
        if plan_type.lower() == "planificado":
            plan_filter = '''(
                (COALESCE(inventory_movements.referencia, '') = '' AND COALESCE(inventory_movements.texto_cab_documento, '') = '')
                OR COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*PGE*' 
                OR COALESCE(inventory_movements.referencia, '') GLOB '*PGE*'
            ) AND COALESCE(inventory_movements.texto_cab_documento, '') NOT GLOB '*PGP*' AND COALESCE(inventory_movements.referencia, '') NOT GLOB '*PGP*' '''
        else: # Desplanificado
            plan_filter = '''NOT (
                (COALESCE(inventory_movements.referencia, '') = '' AND COALESCE(inventory_movements.texto_cab_documento, '') = '')
                OR COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*PGE*' 
                OR COALESCE(inventory_movements.referencia, '') GLOB '*PGE*'
            ) AND COALESCE(inventory_movements.texto_cab_documento, '') NOT GLOB '*PGP*' AND COALESCE(inventory_movements.referencia, '') NOT GLOB '*PGP*' '''

        area_expr = "COALESCE((SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(COALESCE(NULLIF(inventory_movements.ceco_resp, ''), NULLIF(inventory_movements.ce_coste, '')), 1, 6)), 'Mantencion')"
        
        sql = f"""
        SELECT 
            {area_expr} AS area_negocio,
            substr(inventory_movements.fe_contab, 7, 4) || '-' || substr(inventory_movements.fe_contab, 4, 2) AS mes,
            COUNT(inventory_movements.material) AS cantidad
        FROM inventory_movements
        WHERE inventory_movements.cmv = '261' 
          AND {plan_filter}
        """
        
        bound_params = []
        if year:
            sql += " AND inventory_movements.fe_contab LIKE ?"
            bound_params.append(f"%{year}%")
            
        sql += """
        GROUP BY 1, 2
        ORDER BY 1, 2
        """
        
        df = pd.read_sql(sql, db.connection().connection, params=tuple(bound_params))
        
        if df.empty:
            return []
            
        return sanitize_for_json(df)
        
    except Exception as e:
        logger.error(f"Error procesando cmv261_summary: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/custom/cmv261_area_details")
def get_cmv261_area_details(
    plan_type: str = Query("planificado", description="'planificado' o 'desplanificado'"),
    area: str = Query(..., description="Area de negocio filtrada"),
    mes: str = Query(None, description="Mes en formato YYYY-MM. Si no se provee, no se filtra por mes."),
    year: str = Query(None, description="Año"),
    db: Session = Depends(get_session_dep)
):
    import pandas as pd

    try:
        if plan_type.lower() == "planificado":
            plan_filter = '''(
                (COALESCE(inventory_movements.referencia, '') = '' AND COALESCE(inventory_movements.texto_cab_documento, '') = '')
                OR COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*PGE*' 
                OR COALESCE(inventory_movements.referencia, '') GLOB '*PGE*'
            ) AND COALESCE(inventory_movements.texto_cab_documento, '') NOT GLOB '*PGP*' AND COALESCE(inventory_movements.referencia, '') NOT GLOB '*PGP*' '''
        else:
            plan_filter = '''NOT (
                (COALESCE(inventory_movements.referencia, '') = '' AND COALESCE(inventory_movements.texto_cab_documento, '') = '')
                OR COALESCE(inventory_movements.texto_cab_documento, '') GLOB '*PGE*' 
                OR COALESCE(inventory_movements.referencia, '') GLOB '*PGE*'
            ) AND COALESCE(inventory_movements.texto_cab_documento, '') NOT GLOB '*PGP*' AND COALESCE(inventory_movements.referencia, '') NOT GLOB '*PGP*' '''

        area_expr = "COALESCE((SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(COALESCE(NULLIF(inventory_movements.ceco_resp, ''), NULLIF(inventory_movements.ce_coste, '')), 1, 6)), 'Mantencion')"
        
        sql = f"""
        SELECT 
            inventory_movements.material,
            inventory_movements.texto_breve_material,
            COUNT(*) AS frecuencia,
            ROUND(AVG(inventory_movements.cantidad * -1), 2) AS promedio_retiro,
            ROUND(30.0 / COUNT(*), 1) AS dias_frecuencia
        FROM inventory_movements
        WHERE inventory_movements.cmv = '261' 
          AND {plan_filter}
        """
        
        bound_params = []
        if area:
            sql += f" AND {area_expr} = ?"
            bound_params.append(area)

        if mes:
            sql += " AND (substr(inventory_movements.fe_contab, 7, 4) || '-' || substr(inventory_movements.fe_contab, 4, 2)) = ?"
            bound_params.append(mes)
        elif year:
            sql += " AND inventory_movements.fe_contab LIKE ?"
            bound_params.append(f"%{year}%")
            
        sql += """
        GROUP BY inventory_movements.material, inventory_movements.texto_breve_material
        ORDER BY frecuencia DESC
        """
        
        df = pd.read_sql(sql, db.connection().connection, params=tuple(bound_params))
        
        if df.empty:
            return []
            
        return sanitize_for_json(df)
        
    except Exception as e:
        logger.error(f"Error procesando cmv261_area_details: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/inventory/replenishment-suggestions")
async def get_replenishment_suggestions(
    freq: str = Query("all", description="Filtro de frecuencia: all, 1, 3, 6, 12"),
    db: Session = Depends(get_session_dep)
):
    """
    Calcula sugerencias de pedido basándose en el stock inicial MB5B y el ritmo de consumo.
    Muestra los materiales con autonomía < 1 mes.
    """
    
    freq_filter = "AND (SELECT m_count FROM MonthCount) / c.n_retiros <= 12.0" # Default
    if freq == "1":
        freq_filter = "AND (SELECT m_count FROM MonthCount) / c.n_retiros <= 1.0"
    elif freq == "3":
        freq_filter = "AND (SELECT m_count FROM MonthCount) / c.n_retiros > 1.0 AND (SELECT m_count FROM MonthCount) / c.n_retiros <= 3.0"
    elif freq == "6":
        freq_filter = "AND (SELECT m_count FROM MonthCount) / c.n_retiros > 3.0 AND (SELECT m_count FROM MonthCount) / c.n_retiros <= 6.0"
    elif freq == "12":
        freq_filter = "AND (SELECT m_count FROM MonthCount) / c.n_retiros > 6.0 AND (SELECT m_count FROM MonthCount) / c.n_retiros <= 12.0"
    
    sql = f"""
    WITH MonthCount AS (
        SELECT CAST(COUNT(DISTINCT substr(fe_contab, 4, 7)) AS REAL) AS m_count 
        FROM inventory_movements
        WHERE alm = '0060'
    ),
    Consumption AS (
        SELECT 
            TRIM(material) AS material,
            MAX(texto_breve_material) AS descripcion,
            MAX(umb) AS umb,
            SUM(CASE WHEN cantidad < 0 AND cmv IN ('201', '261', '221') THEN ABS(cantidad) ELSE 0 END) AS consumo_total,
            COUNT(CASE WHEN cantidad < 0 AND cmv IN ('201', '261', '221') THEN 1 END) AS n_retiros
        FROM inventory_movements
        WHERE cantidad < 0 AND cmv IN ('201', '261', '221') AND alm = '0060'
        GROUP BY TRIM(material)
    ),
    TotalBalance AS (
        SELECT 
            TRIM(material) AS material,
            SUM(cantidad) AS balance
        FROM inventory_movements
        WHERE alm = '0060'
        GROUP BY TRIM(material)
    )
    SELECT 
        c.material,
        c.descripcion,
        COALESCE(c.umb, i.umb) AS umb,
        COALESCE(i.stock_inicial, 0) AS stock_inicial,
        ROUND(COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0), 2) AS stock_actual,
        ROUND(c.consumo_total / (SELECT m_count FROM MonthCount), 2) AS consumo_mensual,
        CASE WHEN c.n_retiros > 0 THEN ROUND((SELECT m_count FROM MonthCount) / c.n_retiros, 2) ELSE 0 END AS frec_meses,
        CASE WHEN c.n_retiros > 0 THEN ROUND(c.consumo_total / c.n_retiros, 2) ELSE 0 END AS prom_retiro,
        ROUND((COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0)) / NULLIF(c.consumo_total / (SELECT m_count FROM MonthCount), 0), 2) AS autonomia_meses,
        CASE 
            WHEN (c.consumo_total / (SELECT m_count FROM MonthCount)) >= 5.0 THEN 'A'
            WHEN (c.consumo_total / (SELECT m_count FROM MonthCount)) >= 1.0 THEN 'B'
            ELSE 'C'
        END AS clasificacion_abc
    FROM Consumption c
    LEFT JOIN TotalBalance b ON c.material = b.material
    LEFT JOIN mb5b_initial_stock i ON c.material = TRIM(i.material)
    WHERE c.consumo_total > 0
      AND (COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0)) / NULLIF(c.consumo_total / (SELECT m_count FROM MonthCount), 0) < 1.0
      AND NOT (UPPER(COALESCE(c.umb, i.umb)) IN ('KG', 'GLN') AND (c.consumo_total / (SELECT m_count FROM MonthCount)) > 300)
      {freq_filter}
    ORDER BY autonomia_meses ASC, consumo_mensual DESC
    LIMIT 100;
    """
    
    try:
        from sqlalchemy import text
        result = db.execute(text(sql)).mappings().fetchall()
        # Convert to a list of dicts safely
        data = [dict(row) for row in result]
        return {"data": data}
    except Exception as e:
        logger.error(f"Error fetching replenishment suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/inventory/replenishment-suggestions/export")
async def export_replenishment_suggestions(db: Session = Depends(get_session_dep)):
    """
    Exporta todas las sugerencias de pedido (Autonomía < 1) a un archivo Excel.
    """
    sql = """
    WITH MonthCount AS (
        SELECT CAST(COUNT(DISTINCT substr(fe_contab, 4, 7)) AS REAL) AS m_count 
        FROM inventory_movements
        WHERE alm = '0060'
    ),
    Consumption AS (
        SELECT 
            TRIM(material) AS material,
            MAX(texto_breve_material) AS descripcion,
            MAX(umb) AS umb,
            SUM(CASE WHEN cantidad < 0 AND cmv IN ('201', '261', '221') THEN ABS(cantidad) ELSE 0 END) AS consumo_total,
            COUNT(CASE WHEN cantidad < 0 AND cmv IN ('201', '261', '221') THEN 1 END) AS n_retiros
        FROM inventory_movements
        WHERE cantidad < 0 AND cmv IN ('201', '261', '221') AND alm = '0060'
        GROUP BY TRIM(material)
    ),
    TotalBalance AS (
        SELECT 
            TRIM(material) AS material,
            SUM(cantidad) AS balance
        FROM inventory_movements
        WHERE alm = '0060'
        GROUP BY TRIM(material)
    )
    SELECT 
        c.material AS "Material",
        c.descripcion AS "Descripción",
        COALESCE(c.umb, i.umb) AS "UMB",
        COALESCE(i.stock_inicial, 0) AS "Stock Inicial MB5B",
        ROUND(COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0), 2) AS "Stock Actual Calculado",
        ROUND(c.consumo_total / (SELECT m_count FROM MonthCount), 2) AS "Consumo Promedio Mensual",
        CASE WHEN c.n_retiros > 0 THEN ROUND((SELECT m_count FROM MonthCount) / c.n_retiros, 2) ELSE 0 END AS "Frecuencia de Retiro (Meses)",
        CASE WHEN c.n_retiros > 0 THEN ROUND(c.consumo_total / c.n_retiros, 2) ELSE 0 END AS "Promedio por Retiro",
        ROUND((COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0)) / NULLIF(c.consumo_total / (SELECT m_count FROM MonthCount), 0), 2) AS "Autonomía Global (Meses)",
        CASE 
            WHEN (c.consumo_total / (SELECT m_count FROM MonthCount)) >= 5.0 THEN 'A'
            WHEN (c.consumo_total / (SELECT m_count FROM MonthCount)) >= 1.0 THEN 'B'
            ELSE 'C'
        END AS "Clasificación ABC"
    FROM Consumption c
    LEFT JOIN TotalBalance b ON c.material = b.material
    LEFT JOIN mb5b_initial_stock i ON c.material = TRIM(i.material)
    WHERE c.consumo_total > 0
      AND (COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0)) / NULLIF(c.consumo_total / (SELECT m_count FROM MonthCount), 0) < 1.0
      AND NOT (UPPER(COALESCE(c.umb, i.umb)) IN ('KG', 'GLN') AND (c.consumo_total / (SELECT m_count FROM MonthCount)) > 300)
    ORDER BY "Autonomía Global (Meses)" ASC, "Consumo Promedio Mensual" DESC;
    """
    
    sql_areas = """
    WITH MonthCount AS (
        SELECT CAST(COUNT(DISTINCT substr(fe_contab, 4, 7)) AS REAL) AS m_count 
        FROM inventory_movements
        WHERE alm = '0060'
    ),
    AreaMapping AS (
        SELECT 
            TRIM(material) AS material,
            MAX(texto_breve_material) AS descripcion,
            CASE 
                WHEN cmv = '261' THEN COALESCE((SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(ceco_resp, 1, 6)), 'Mantencion')
                WHEN cmv IN ('201', '221') THEN COALESCE((SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(ce_coste, 1, 6)), 'Mantencion')
                ELSE 'Otros'
            END AS area_negocio,
            SUM(ABS(cantidad)) AS area_consumo_total,
            COUNT(1) AS area_n_retiros
        FROM inventory_movements
        WHERE cantidad < 0 AND cmv IN ('201', '261', '221') AND alm = '0060'
        GROUP BY TRIM(material), area_negocio
    ),
    TotalBalance AS (
        SELECT TRIM(material) AS material, SUM(cantidad) AS balance
        FROM inventory_movements WHERE alm = '0060' GROUP BY TRIM(material)
    ),
    GlobalConsumption AS (
        SELECT 
            TRIM(material) AS material,
            SUM(CASE WHEN cantidad < 0 AND cmv IN ('201', '261', '221') THEN ABS(cantidad) ELSE 0 END) AS global_consumo_total,
            COUNT(CASE WHEN cantidad < 0 AND cmv IN ('201', '261', '221') THEN 1 END) AS global_n_retiros
        FROM inventory_movements
        WHERE cantidad < 0 AND cmv IN ('201', '261', '221') AND alm = '0060'
        GROUP BY TRIM(material)
    )
    SELECT 
        a.area_negocio AS "Área de Negocio",
        a.material AS "Material",
        a.descripcion AS "Descripción",
        COALESCE(i.umb, '') AS "UMB",
        ROUND(COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0), 2) AS "Stock Global Actual",
        ROUND(a.area_consumo_total / (SELECT m_count FROM MonthCount), 2) AS "Consumo Local (Mes)",
        CASE WHEN a.area_n_retiros > 0 THEN ROUND((SELECT m_count FROM MonthCount) / a.area_n_retiros, 2) ELSE 0 END AS "Frecuencia Local (Meses)",
        CASE WHEN a.area_n_retiros > 0 THEN ROUND(a.area_consumo_total / a.area_n_retiros, 2) ELSE 0 END AS "Promedio Retiro Local",
        ROUND((COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0)) / NULLIF(a.area_consumo_total / (SELECT m_count FROM MonthCount), 0), 2) AS "Autonomía Local (Meses)"
    FROM AreaMapping a
    LEFT JOIN TotalBalance b ON a.material = b.material
    LEFT JOIN mb5b_initial_stock i ON a.material = TRIM(i.material)
    LEFT JOIN GlobalConsumption g ON a.material = g.material
    WHERE g.global_consumo_total > 0
      AND (COALESCE(i.stock_inicial, 0) + COALESCE(b.balance, 0)) / NULLIF(g.global_consumo_total / (SELECT m_count FROM MonthCount), 0) < 1.0
      AND NOT (UPPER(COALESCE(i.umb, '')) IN ('KG', 'GLN') AND (g.global_consumo_total / (SELECT m_count FROM MonthCount)) > 300)
      AND (SELECT m_count FROM MonthCount) / g.global_n_retiros <= 12.0
    ORDER BY a.area_negocio ASC, "Autonomía Local (Meses)" ASC;
    """
    
    try:
        from sqlalchemy import text
        result_main = db.execute(text(sql)).mappings().fetchall()
        result_areas = db.execute(text(sql_areas)).mappings().fetchall()
        
        df_main = pd.DataFrame([dict(row) for row in result_main])
        df_areas = pd.DataFrame([dict(row) for row in result_areas])
        
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
        logger.error(f"Error exporting replenishment suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

