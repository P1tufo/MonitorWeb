from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import logging
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
    "ABC_ANALYSIS",
    "AVG_TX_PER_DAY",
})

ALLOWED_GRANULARITIES = frozenset({"HOUR", "DAY", "WEEK", "MONTH", "YEAR", "DAY_OF_WEEK"})


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
    if name in ["__AREA_EXPR__", "__PLAN_VS_UNPLAN__", "__ABAST_VS_CONSUMO__", "__PROD_VS_MANT__"]:
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

