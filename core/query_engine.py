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

from repositories.deliveries import DeliveriesRepository
AREA_EXPR_MACRO = DeliveriesRepository.AREA_EXPR

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
    if name == "__AREA_EXPR__":
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

    unified_metrics = []
    if getattr(payload, "metrics", None):
        unified_metrics.extend(payload.metrics)
    else:
        if getattr(payload, "metric", None):
            unified_metrics.append(payload.metric)
        if getattr(payload, "secondMetric", None) and getattr(payload.secondMetric, "column", None):
            unified_metrics.append(payload.secondMetric)

    for m in unified_metrics:
        custom_expr = getattr(m, "customExpr", None)
        m_col = getattr(m, "column", None)
        if custom_expr:
            if custom_expr != "__AREA_EXPR__":
                raise HTTPException(status_code=400, detail="customExpr no permitido")
        elif m_col:
            if not validate_identifier(m_col, db):
                raise HTTPException(status_code=400, detail=f"Columna de métrica no válida: {m_col}")
        
        m_agg = getattr(m, "aggregation", "").upper()
        if m_agg and m_agg not in ALLOWED_AGGREGATIONS and not custom_expr:
            raise HTTPException(status_code=400, detail=f"Operación de agregación no válida: {m_agg}")

        m_cond = getattr(m, "condition", None)
        if m_cond and m_cond.column:
            if not validate_identifier(m_cond.column, db):
                raise HTTPException(status_code=400, detail=f"Columna de condición de métrica no válida: {m_cond.column}")

    if payload.timeAxis and payload.timeAxis.column:
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
    if payload.timeAxis and payload.timeAxis.column:
        col = payload.timeAxis.column
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
        b_expr = AREA_EXPR_MACRO.replace("v.", f"{payload.baseTable}.") if payload.breakdown == "__AREA_EXPR__" else payload.breakdown
        breakdown_select = f"{b_expr} AS categoria,\n  "
        breakdown_groupby = ", categoria"

    # ── 6. Filtros parametrizados (bind params) ───────────────────────────────
    where_clauses = []
    bound_params: List = []
    # Las métricas se procesan después para poder apendear a bound_params
    metric_selects = []
    
    for i, m in enumerate(unified_metrics):
        custom_expr = getattr(m, "customExpr", None)
        m_label = getattr(m, "label", "")
        if not m_label:
            m_label = "valor" if i == 0 else f"metrica_{i}"
            
        if custom_expr:
            m_expr = AREA_EXPR_MACRO.replace("v.", f"{payload.baseTable}.") if custom_expr == "__AREA_EXPR__" else "NULL"
            metric_selects.append(f'{m_expr} AS "{m_label}"')
            continue

        metric_col = getattr(m, "column", "*") or "*"
        agg_upper = getattr(m, "aggregation", "COUNT").upper()
        condition = getattr(m, "condition", None)
        
        cond_str = ""
        if condition:
            op = condition.operator.lower()
            val = condition.value
            col = condition.column
            op_map = {
                "equals": "=", "notequals": "!=",
                "greaterthan": ">", "lessthan": "<",
                "greaterthanequal": ">=", "lessthanequal": "<="
            }
            sql_op = op_map.get(op, "=")
            bound_params.append(val)
            cond_str = f"CASE WHEN {col} {sql_op} ? THEN "
                
        if agg_upper == "COUNT_DISTINCT":
            if cond_str:
                m_expr = f"COUNT(DISTINCT {cond_str} {metric_col} ELSE NULL END)"
            else:
                m_expr = "COUNT(*)" if metric_col == "*" else f"COUNT(DISTINCT {metric_col})"
        elif agg_upper in ("SUM", "AVG", "MIN", "MAX", "COUNT"):
            if cond_str:
                if agg_upper == "COUNT":
                    m_expr = f"SUM({cond_str} 1 ELSE 0 END)"
                else:
                    m_expr = f"{agg_upper}({cond_str} {metric_col} ELSE NULL END)"
            else:
                m_expr = f"{agg_upper}({metric_col})"
        elif agg_upper == "SLA_EFFICIENCY":
            m_expr = f"ROUND(SUM(CASE WHEN {metric_col} <= 2 THEN 100.0 ELSE 0.0 END) / NULLIF(COUNT(*), 0), 1)"
        elif agg_upper == "REPLENISHMENT_RATE":
            m_expr = (f"ROUND(SUM(CASE WHEN {metric_col} LIKE '%Ingreso%' THEN 100.0 ELSE 0.0 END) "
                      f"/ NULLIF(SUM(CASE WHEN {metric_col} LIKE '%Centro Costo%' "
                      f"OR {metric_col} LIKE '%Orden/Reserva%' THEN 1.0 ELSE 0.0 END), 0), 1)")
        elif agg_upper == "RETURN_RATE":
            m_expr = (f"ROUND(SUM(CASE WHEN TRIM(cmv) IN ('202', '262') THEN 100.0 ELSE 0.0 END) "
                      f"/ NULLIF(SUM(CASE WHEN {metric_col} LIKE '%Centro Costo%' "
                      f"OR {metric_col} LIKE '%Orden/Reserva%' THEN 1.0 ELSE 0.0 END), 0), 1)")
        else:
            m_expr = f"{agg_upper}({metric_col})"
            
        metric_selects.append(f'{m_expr} AS "{m_label}"')

    metrics_select_str = ",\n  ".join(metric_selects) if metric_selects else "1 AS dummy"



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

                # Solo estas columnas guardan fecha ISO real
                _ISO_COLS = {"ingested_at", "created_at", "updated_at"}

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
    if payload.timeAxis and payload.timeAxis.column:
        groupby_clauses.append("fecha")
    if payload.breakdown:
        groupby_clauses.append("categoria")
    groupby_str = ("\nGROUP BY " + ", ".join(groupby_clauses)) if groupby_clauses else ""

    # ── 8. SQL final ─────────────────────────────────────────────────────────
    if payload.breakdown:
        sql = (
            f"SELECT \n"
            f"  {time_func} AS fecha,\n"
            f"  {breakdown_select}{metrics_select_str}\n"
            f"FROM {from_clause}{where_str}{groupby_str}\n"
            f"ORDER BY fecha ASC;"
        )
    else:
        # Si no hay timeAxis ni breakdown, evitamos seleccionar y ordenar por 'fecha' ('Total')
        if not (payload.timeAxis and payload.timeAxis.column):
            sql = (
                f"SELECT \n"
                f"  {metrics_select_str}\n"
                f"FROM {from_clause}{where_str}{groupby_str};"
            )
        else:
            sql = (
                f"SELECT \n"
                f"  {time_func} AS fecha,\n"
                f"  {metrics_select_str}\n"
                f"FROM {from_clause}{where_str}{groupby_str}\n"
                f"ORDER BY fecha ASC;"
            )

    logger.debug(f"QueryEngine: SQL compilado para tabla '{payload.baseTable}' ({len(bound_params)} params)")
    return sql, bound_params
