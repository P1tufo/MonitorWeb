from typing import Optional
# ─── Utilidades de ejecución: parámetros y extracción de métricas ─────────────

def get_bound_params_from_visual_state(visual_state_str: str) -> list:
    """
    Extrae los bind params (?) de un visual_state JSON serializado.

    Lee la lista `filters` del VisualQueryBuilderPayload y produce la lista
    de valores en el mismo orden en que build_sql_from_payload los emite.
    Solo procesa filtros con valueType == "value" (valores literales).

    Esta es la versión canónica. Reemplaza:
      - core/utils.py::_get_bound_params_from_visual_state  (mantenida como alias)
      - DeliveriesService._get_bound_params_from_visual_state (versión obsoleta
        que leía claves legacy "area", "mes", "semana" — ya no existen en el payload)
    """
    import json
    if not visual_state_str:
        return []
    try:
        state = json.loads(visual_state_str)
        filters = state.get("filters", [])
        bound_params = []
        for f in filters:
            if f.get("valueType", "value") != "value":
                continue
            op = f.get("operator", "").lower()
            val = f.get("value", "")
            if op in {
                "equals", "notequals", "greaterthan", "lessthan",
                "greaterthanequal", "greaterthanequals",
                "lessthanequal", "lessthanequals",
            }:
                bound_params.append(val)
            elif op in {"contains", "notcontains"}:
                bound_params.append(f"%{val}%")
            elif op == "in":
                bound_params.extend([v.strip() for v in str(val).split(",") if v.strip()])
            # isnull / isnotnull no generan bind params
        return bound_params
    except Exception:
        return []


def extract_metric_value(df, active_year: Optional[str] = None):
    """
    Extrae el valor numérico principal de un DataFrame de resultado de query.

    Estrategia:
      - Si se provee active_year y el DataFrame tiene columna "fecha",
        filtra las filas que contengan el año y devuelve el valor de la
        primera coincidencia.
      - Si no hay coincidencia temporal, devuelve el primer valor de la
        primera columna numérica conocida (valor, total_qty, efficiency…).

    Esta es la versión canónica. Reemplaza:
      - core/utils.py::_extract_metric_value              (mantenida como alias)
      - DeliveriesService._extract_metric_value           (copia exacta eliminada)
    """
    if df.empty:
        return None

    if active_year and "fecha" in df.columns:
        active_year_str = str(active_year).replace("%", "").strip()
        mask = df["fecha"].astype(str).str.contains(active_year_str, na=False)
        matched_df = df[mask]
        if not matched_df.empty:
            target_row = matched_df.iloc[0]
            for col in ("valor", "total_qty", "efficiency", "ontime_qty", "late_qty"):
                if col in matched_df.columns:
                    return target_row[col]
            return target_row.iloc[-1]

    for col in ("valor", "total_qty", "efficiency", "ontime_qty", "late_qty"):
        if col in df.columns:
            return df.iloc[0][col]
    return df.iloc[0, -1]

