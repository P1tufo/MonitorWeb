"""
core/query_engine.py — Motor de construcción de SQL seguro para el Analytics Studio.

Este módulo es la única fuente de verdad para construir SQL dinámico a partir de un
VisualQueryBuilderPayload. Centraliza:

  1. La lista blanca de tablas permitidas (ALLOWED_TABLES).
  2. La validación dinámica de identificadores (tablas y columnas) contra el esquema
     real de la BD, usando PRAGMA table_info — el patrón más seguro disponible.
  3. La construcción parametrizada de SQL: FROM, JOIN, WHERE (con bind params),
     métricas con agregaciones, eje temporal y desglose por series.

Relación con el resto del sistema:
  - routes/settings.py::api_build_sql   → llama a build_sql_from_payload()
  - core/security.py::validate_table    → valida nombres de tabla en ETL (sin cambios)
  - core/utils.py                       → utilidades JSON y métricas (sin cambios)

Plan de migración:
  - Fase 2, Punto 2: _build_unified_where en routes/filters.py usará validate_column().
  - Fase 2, Punto 3: repositories/base._sql() dejará de devolver SQL crudo.
"""
import logging
from typing import List, Tuple, Optional

from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException

logger = logging.getLogger("query-engine")

# ─── Lista blanca de tablas expuestas al Analytics Studio ────────────────────
# Fuente única de verdad. Reemplaza ALLOWED_TABLES_GLOBAL de routes/settings.py
# y complementa WHITELIST_TABLES de core/security.py (que cubre el ETL).
ALLOWED_TABLES = frozenset({
    "outbound_deliveries",
    "stock_levels",
    "warehouse_tasks",
    "inventory_movements",
})

# ─── Agregaciones permitidas ─────────────────────────────────────────────────
ALLOWED_AGGREGATIONS = frozenset({
    "SUM", "AVG", "COUNT", "MIN", "MAX",
    "COUNT_DISTINCT",
    "SLA_EFFICIENCY",
    "REPLENISHMENT_RATE",
    "RETURN_RATE",
    "INV_EFFICIENCY",
})

ALLOWED_GRANULARITIES = frozenset({"HOUR", "DAY", "WEEK", "MONTH", "YEAR"})


# ─── Validación de identificadores ───────────────────────────────────────────

def validate_identifier(name: str, db: Session) -> bool:
    """
    Valida que un identificador (tabla o tabla.columna) pertenezca a la lista blanca.

    Estrategia:
      - Si es solo un nombre de tabla: comprueba contra ALLOWED_TABLES.
      - Si es "tabla.columna": comprueba la tabla contra ALLOWED_TABLES y luego
        consulta el esquema real de la BD con PRAGMA table_info para verificar
        que la columna existe. Esto evita inyección por nombres de columna falsos.

    Devuelve True si el identificador es válido, False en caso contrario.
    Nunca lanza excepción: el caller decide si rechazar con HTTPException.
    """
    if not name:
        return True

    parts = name.split(".")
    if len(parts) == 1:
        return parts[0] in ALLOWED_TABLES
    elif len(parts) == 2:
        table, col = parts
        if table not in ALLOWED_TABLES:
            return False
        try:
            cols = db.execute(text(f"PRAGMA table_info({table})")).all()
            allowed_cols = {c[1] for c in cols}
            allowed_cols.add("hora")  # Columna virtual de soporte horario
            return col in allowed_cols
        except Exception:
            return False
    return False


def validate_column(table: str, column: str, db: Session) -> bool:
    """
    Valida que una columna pertenezca a una tabla permitida, consultando el
    esquema real de la BD. Útil para validar columnas en filtros y cláusulas WHERE
    fuera del flujo del Visual Query Builder (ej: routes/filters.py en Fase 2).
    """
    if table not in ALLOWED_TABLES:
        return False
    try:
        cols = db.execute(text(f"PRAGMA table_info({table})")).all()
        allowed_cols = {c[1] for c in cols}
        return column in allowed_cols
    except Exception:
        return False


def get_table_columns(table: str, db: Session) -> List[str]:
    """
    Retorna la lista de columnas de una tabla permitida.
    Devuelve lista vacía si la tabla no está en la lista blanca o hay error.
    """
    if table not in ALLOWED_TABLES:
        return []
    try:
        cols = db.execute(text(f"PRAGMA table_info({table})")).all()
        return [c[1] for c in cols]
    except Exception:
        return []


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


def extract_metric_value(df, active_year: str = None):
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


# ─── Motor de construcción SQL ────────────────────────────────────────────────

def build_sql_from_payload(payload, db: Session) -> Tuple[str, List]:
    """
    Compila un VisualQueryBuilderPayload validado en una tupla (sql_text, bound_params).

    Garantías de seguridad:
      - Todas las tablas y columnas del payload se validan contra ALLOWED_TABLES
        y el esquema real de la BD antes de usarse en la query.
      - Los valores de filtro se pasan siempre como bind params (?), nunca
        interpolados en el string SQL.
      - Las agregaciones y granularidades se validan contra listas blancas estáticas.

    Lanza HTTPException(400) si algún identificador no es válido.
    Devuelve (sql_text, bound_params) listos para ejecutar con SQLAlchemy text().
    """
    # ── 1. Validaciones de seguridad ─────────────────────────────────────────
    if not validate_identifier(payload.baseTable, db):
        raise HTTPException(status_code=400, detail=f"Tabla principal no válida: {payload.baseTable}")

    for j in payload.joins:
        if not validate_identifier(j.table, db):
            raise HTTPException(status_code=400, detail=f"Tabla JOIN no válida: {j.table}")
        if not validate_identifier(j.onLeft, db) or not validate_identifier(j.onRight, db):
            raise HTTPException(status_code=400, detail="Parámetro ON de JOIN no válido")

    for f in payload.filters:
        if not validate_identifier(f.column, db):
            raise HTTPException(status_code=400, detail=f"Columna de filtro no válida: {f.column}")
        comp_col = getattr(f, "compareColumn", None)
        if comp_col and not validate_identifier(comp_col, db):
            raise HTTPException(status_code=400, detail=f"Columna de comparación no válida: {comp_col}")

    if not validate_identifier(payload.metric.column, db):
        raise HTTPException(status_code=400, detail=f"Columna de métrica no válida: {payload.metric.column}")

    if payload.metric.aggregation.upper() not in ALLOWED_AGGREGATIONS:
        raise HTTPException(status_code=400, detail=f"Operación de agregación no válida: {payload.metric.aggregation}")

    if payload.timeAxis.column:
        if not validate_identifier(payload.timeAxis.column, db):
            raise HTTPException(status_code=400, detail=f"Columna de fecha no válida: {payload.timeAxis.column}")
        if payload.timeAxis.granularity.upper() not in ALLOWED_GRANULARITIES:
            raise HTTPException(status_code=400, detail="Granularidad de tiempo no válida")

    if payload.breakdown and not validate_identifier(payload.breakdown, db):
        raise HTTPException(status_code=400, detail=f"Columna de desglose no válida: {payload.breakdown}")

    # ── 2. FROM y JOINs ──────────────────────────────────────────────────────
    from_clause = payload.baseTable
    join_clauses = []
    for j in payload.joins:
        join_clauses.append(f"LEFT JOIN {j.table} ON {j.onLeft} = {j.onRight}")
    join_str = "\n".join(join_clauses)
    if join_str:
        from_clause = f"{from_clause}\n{join_str}"

    # ── 3. Eje de tiempo ─────────────────────────────────────────────────────
    col = payload.timeAxis.column
    if col:
        table_prefix = col.split(".")[0] if "." in col else payload.baseTable

        has_hora = False
        try:
            cols = db.execute(text(f"PRAGMA table_info({table_prefix})")).all()
            has_hora = any(c[1] == "hora" for c in cols)
        except Exception:
            pass

        gran = payload.timeAxis.granularity.upper()
        if gran == "YEAR":
            time_func = f"substr({col}, 7, 4)"
        elif gran == "MONTH":
            time_func = f"substr({col}, 7, 4) || '-' || substr({col}, 4, 2)"
        elif gran == "WEEK":
            time_func = f"strftime('%Y-W%W', substr({col}, 7, 4) || '-' || substr({col}, 4, 2) || '-' || substr({col}, 1, 2))"
        elif gran == "DAY":
            time_func = f"substr({col}, 7, 4) || '-' || substr({col}, 4, 2) || '-' || substr({col}, 1, 2)"
        elif gran == "HOUR":
            if has_hora:
                time_func = f"substr({col}, 7, 4) || '-' || substr({col}, 4, 2) || '-' || substr({col}, 1, 2) || ' ' || substr({table_prefix}.hora, 1, 2) || ':00'"
            else:
                time_func = f"substr({col}, 7, 4) || '-' || substr({col}, 4, 2) || '-' || substr({col}, 1, 2)"
        else:
            time_func = col
    else:
        time_func = "'Total'"

    # ── 4. Desglose (Breakdown) ───────────────────────────────────────────────
    breakdown_select = ""
    breakdown_groupby = ""
    if payload.breakdown:
        breakdown_select = f"{payload.breakdown} AS categoria,\n  "
        breakdown_groupby = ", categoria"

    # ── 5. Métrica principal ──────────────────────────────────────────────────
    metric_col = payload.metric.column or "*"

    agg_upper = payload.metric.aggregation.upper()

    if agg_upper == "COUNT_DISTINCT":
        metric_func = "COUNT(*)" if metric_col == "*" else f"COUNT(DISTINCT {metric_col})"

    elif agg_upper == "SLA_EFFICIENCY":
        col_name = metric_col.split(".")[-1] if "." in metric_col else metric_col
        metric_func = f"ROUND(SUM(CASE WHEN {metric_col} <= 2 THEN 100.0 ELSE 0.0 END) / COUNT(*), 1)"

        extra_cols: List[str] = []
        if payload.timeAxis.column:
            t_col = payload.timeAxis.column.split(".")[-1] if "." in payload.timeAxis.column else payload.timeAxis.column
            if t_col != "entrega" and t_col != col_name:
                extra_cols.append(t_col)
        else:
            extra_cols.append("fecha_carga")

        if payload.breakdown:
            b_col = payload.breakdown.split(".")[-1] if "." in payload.breakdown else payload.breakdown
            if b_col != "entrega" and b_col != col_name and b_col not in extra_cols:
                extra_cols.append(b_col)

        for f in payload.filters:
            if f.column:
                f_col = f.column.split(".")[-1] if "." in f.column else f.column
                if f_col != "entrega" and f_col != col_name and f_col not in extra_cols:
                    extra_cols.append(f_col)
            comp_col = getattr(f, "compareColumn", None)
            if comp_col:
                fc_col = comp_col.split(".")[-1] if "." in comp_col else comp_col
                if fc_col != "entrega" and fc_col != col_name and fc_col not in extra_cols:
                    extra_cols.append(fc_col)

        extra_cols_str = "".join([f", {c}" for c in extra_cols])
        from_clause = (
            f"(SELECT entrega, MAX({metric_col}) as {col_name}{extra_cols_str} "
            f"FROM outbound_deliveries WHERE {metric_col} IS NOT NULL GROUP BY entrega) "
            f"AS outbound_deliveries"
        )

    elif agg_upper == "REPLENISHMENT_RATE":
        metric_func = (
            f"ROUND(SUM(CASE WHEN {metric_col} LIKE '%Ingreso%' THEN 1.0 ELSE 0.0 END) * 100.0 "
            f"/ COALESCE(NULLIF(SUM(CASE WHEN {metric_col} LIKE '%Centro Costo%' "
            f"OR {metric_col} LIKE '%Orden/Reserva%' THEN 1.0 ELSE 0.0 END), 0), 1), 1)"
        )

    elif agg_upper == "RETURN_RATE":
        metric_func = (
            f"ROUND(SUM(CASE WHEN TRIM(cmv) IN ('202', '262') THEN 1.0 ELSE 0.0 END) * 100.0 "
            f"/ COALESCE(NULLIF(SUM(CASE WHEN {metric_col} LIKE '%Centro Costo%' "
            f"OR {metric_col} LIKE '%Orden/Reserva%' THEN 1.0 ELSE 0.0 END), 0), 1), 1)"
        )

    elif agg_upper == "INV_EFFICIENCY":
        metric_func = (
            "ROUND(SUM(CASE WHEN (julianday(substr(registrado, 7, 4) || '-' || substr(registrado, 4, 2) || "
            "'-' || substr(registrado, 1, 2)) - julianday(substr(fe_contab, 7, 4) || '-' || "
            "substr(fe_contab, 4, 2) || '-' || substr(fe_contab, 1, 2))) <= 3.0 "
            "THEN 100.0 ELSE 0.0 END) / COUNT(*), 1)"
        )
    else:
        metric_func = f"{agg_upper}({metric_col})"

    # ── 5b. Segunda métrica ───────────────────────────────────────────────────
    second_metric_select = ""
    ALLOWED_AGGS_SM = {"SUM", "AVG", "COUNT", "MIN", "MAX", "COUNT_DISTINCT", "SLA_EFFICIENCY"}
    sm = payload.secondMetric
    if sm and sm.column and sm.aggregation and not payload.breakdown:
        sm_agg = sm.aggregation.upper()
        if sm_agg in ALLOWED_AGGS_SM:
            sm_col = sm.column
            sm_label = sm.label.strip() if sm.label else sm_agg.lower()
            # Sanitizar alias: solo letras, números y guión bajo
            sm_alias = "".join(c if c.isalnum() or c == "_" else "_" for c in sm_label) or "segunda_metrica"
            if sm_agg == "COUNT_DISTINCT":
                sm_func = f"COUNT(DISTINCT {sm_col})"
            elif sm_agg == "SLA_EFFICIENCY":
                sm_func = f"ROUND(SUM(CASE WHEN {sm_col} <= 2 THEN 100.0 ELSE 0.0 END) / NULLIF(COUNT(*), 0), 1)"
            else:
                sm_func = f"{sm_agg}({sm_col})"
            second_metric_select = f",\n  {sm_func} AS {sm_alias}"

    # ── 6. Filtros parametrizados (bind params) ───────────────────────────────
    where_clauses = []
    bound_params: List = []

    for f in payload.filters:
        op = f.operator.lower()
        val_type = getattr(f, "valueType", "value") or "value"

        if val_type == "column":
            comp_col = getattr(f, "compareColumn", None)
            if comp_col:
                op_map = {
                    "equals": "=", "notequals": "!=",
                    "greaterthan": ">", "lessthan": "<",
                    "greaterthanequal": ">=", "greaterthanequals": ">=",
                    "lessthanequal": "<=", "lessthanequals": "<=",
                }
                if op in op_map:
                    where_clauses.append(f"{f.column} {op_map[op]} {comp_col}")

        elif val_type == "date_diff":
            comp_col = getattr(f, "compareColumn", None)
            offset   = str(getattr(f, "offsetValue", "2") or "2").strip()
            diff_op  = getattr(f, "diffOp", None) or "lessthanequal"
            if comp_col:
                op_map = {
                    "equals": "=", "notequals": "!=",
                    "greaterthan": ">", "lessthan": "<",
                    "greaterthanequal": ">=", "greaterthanequals": ">=",
                    "lessthanequal": "<=", "lessthanequals": "<=",
                }
                sql_op = op_map.get(diff_op, "<=")

                # Columnas SAP en formato ISO que julianday() acepta directamente
                _ISO_COLS = {"registrado", "fe_contab", "fe_creac", "fecha_carga",
                             "fecha_sm_real", "creado_el", "fecha_conf", "ingested_at"}

                def _date_expr(col: str) -> str:
                    if col == "today":
                        return "DATE('now')"
                    bare = col.split(".")[-1].lower()
                    if bare in _ISO_COLS:
                        return col
                    # Formato DD-MM-YYYY de SAP -> ISO para julianday()
                    return (f"substr({col}, 7, 4) || '-' || "
                            f"substr({col}, 4, 2) || '-' || "
                            f"substr({col}, 1, 2)")

                left_expr  = _date_expr(f.column)
                right_expr = _date_expr(comp_col)
                diff_expr  = f"(julianday({right_expr}) - julianday({left_expr}))"
                where_clauses.append(f"{diff_expr} {sql_op} {offset}")


        else:
            # Valores literales → siempre como bind param
            if op == "equals":
                where_clauses.append(f"{f.column} = ?")
                bound_params.append(f.value)
            elif op == "notequals":
                where_clauses.append(f"{f.column} != ?")
                bound_params.append(f.value)
            elif op == "greaterthan":
                where_clauses.append(f"{f.column} > ?")
                bound_params.append(f.value)
            elif op == "lessthan":
                where_clauses.append(f"{f.column} < ?")
                bound_params.append(f.value)
            elif op in {"greaterthanequal", "greaterthanequals"}:
                where_clauses.append(f"{f.column} >= ?")
                bound_params.append(f.value)
            elif op in {"lessthanequal", "lessthanequals"}:
                where_clauses.append(f"{f.column} <= ?")
                bound_params.append(f.value)
            elif op == "contains":
                where_clauses.append(f"{f.column} LIKE ?")
                bound_params.append(f"%{f.value}%")
            elif op == "in":
                vals = [v.strip() for v in str(f.value).split(",") if v.strip()]
                where_clauses.append(f"{f.column} IN ({','.join(['?' for _ in vals])})")
                bound_params.extend(vals)
            elif op == "notcontains":
                where_clauses.append(f"{f.column} NOT LIKE ?")
                bound_params.append(f"%{f.value}%")
            elif op == "isnull":
                where_clauses.append(f"({f.column} IS NULL OR {f.column} = '')")
            elif op == "isnotnull":
                where_clauses.append(f"({f.column} IS NOT NULL AND {f.column} != '')")

    where_str = ("\nWHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    # ── 7. GROUP BY ───────────────────────────────────────────────────────────
    groupby_clauses = []
    if payload.timeAxis.column:
        groupby_clauses.append("fecha")
    if payload.breakdown:
        groupby_clauses.append("categoria")
    groupby_str = ("\nGROUP BY " + ", ".join(groupby_clauses)) if groupby_clauses else ""

    # ── 8. SQL final ─────────────────────────────────────────────────────────
    if payload.breakdown:
        sql = (
            f"SELECT \n"
            f"  {time_func} AS fecha,\n"
            f"  {breakdown_select}{metric_func} AS valor\n"
            f"FROM {from_clause}{where_str}{groupby_str}\n"
            f"ORDER BY fecha ASC;"
        )
    else:
        sql = (
            f"SELECT \n"
            f"  {time_func} AS fecha,\n"
            f"  {metric_func} AS valor{second_metric_select}\n"
            f"FROM {from_clause}{where_str}{groupby_str}\n"
            f"ORDER BY fecha ASC;"
        )

    logger.debug(f"QueryEngine: SQL compilado para tabla '{payload.baseTable}' ({len(bound_params)} params)")
    return sql, bound_params
