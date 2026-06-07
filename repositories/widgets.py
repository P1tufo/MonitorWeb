import json
import logging
from typing import Any, Dict, Optional

import pandas as pd
from sqlalchemy import text

from core.helpers.dynamic_executor import execute_visual_query
from core.query_engine import build_sql_from_payload
from core.schemas import VisualQueryBuilderPayload
from core.utils import sanitize_for_json

from .base import BaseRepository

logger = logging.getLogger("repo-widgets")

class WidgetRepository(BaseRepository):
    """Repositorio especializado para ejecutar Data Visualizations (Server-Driven UI)."""

    def execute_widget(self, query_id: str, visual_state: str, year: Optional[str], area: Optional[str], granularity: Optional[str]) -> Dict[str, Any]:
        payload_dict = json.loads(visual_state)
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

        # Filtro estricto para ignorar el mes en curso para los gráficos de SLA
        if query_id in ("vl_sla_monthly_trend", "vl_sla_trend", "vl_sla_area_monthly_trend", "vl_sla_area_trend"):
            from datetime import datetime
            curr = datetime.now()
            curr_str = f"{curr.month:02d}-{curr.year}"
            base_t = payload_dict.get("baseTable", "outbound_deliveries")
            filters.append({
                "column": f"{base_t}.fecha_carga",
                "operator": "notcontains",
                "value": curr_str,
                "valueType": "value"
            })

        payload_dict["filters"] = filters
        chart_type = payload_dict.get("chartType", "bar")

        # Executes dynamic visual query (using pandas / execute_visual_query)
        df = execute_visual_query(payload_dict, self.session)

        labels = []
        datasets = []
        raw_data = []

        if not df.empty:
            if "categoria" in df.columns:
                df = df[df["categoria"] != "Otro"]

            raw_data = sanitize_for_json(df)
            if "fecha" in df.columns and (df["fecha"] == "Total").all():
                df = df.drop(columns=["fecha"])

            if "categoria" in df.columns or "fecha" in df.columns:
                if "fecha" in df.columns and "categoria" in df.columns:
                    pivot = df.pivot_table(index="fecha", columns="categoria", values=df.columns[-1], aggfunc="sum").fillna(0)
                    labels = pivot.index.tolist()
                    for col in pivot.columns:
                        datasets.append({"label": str(col), "data": pivot[col].tolist()})
                elif "categoria" in df.columns:
                    labels = df["categoria"].tolist()
                    metric_cols = [c for c in df.columns if c not in ("fecha", "categoria")]
                    for col in metric_cols:
                        datasets.append({"label": str(col), "data": df[col].tolist()})
                elif "fecha" in df.columns:
                    labels = df["fecha"].tolist()
                    metric_cols = [c for c in df.columns if c != "fecha"]
                    for col in metric_cols:
                        datasets.append({"label": str(col), "data": df[col].tolist()})

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
        return {
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

    def execute_drilldown(self, query_id: str, visual_state: str, segment: str, material: Optional[str], year: Optional[str]) -> list:
        payload_dict = json.loads(visual_state)
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
            payload = VisualQueryBuilderPayload(**payload_dict)
            sql, bound_params = build_sql_from_payload(payload, self.session, drilldown_segment=segment, drilldown_material=material)

        df = pd.read_sql(sql, self.session.connection().connection, params=tuple(bound_params))
        return sanitize_for_json(df) if not df.empty else []
