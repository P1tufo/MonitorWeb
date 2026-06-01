"""
core/query_engine.py — Facade para el motor de SQL.
"""
from core.query_validators import (
    validate_identifier,
    validate_column,
    get_table_columns,
    ALLOWED_TABLES,
    ALLOWED_AGGREGATIONS,
    ALLOWED_GRANULARITIES
)
from core.query_utils import (
    get_bound_params_from_visual_state,
    extract_metric_value
)
from core.query_builder import (
    build_sql_from_payload,
    AREA_EXPR_MACRO
)
