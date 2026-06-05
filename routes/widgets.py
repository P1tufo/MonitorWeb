import json
import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
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
