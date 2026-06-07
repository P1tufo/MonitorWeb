"""
core/query_engine.py — Facade para el motor de SQL.
"""
from core.query_builder import AREA_EXPR_MACRO, build_sql_from_payload
from core.query_utils import extract_metric_value, get_bound_params_from_visual_state
from core.query_validators import ALLOWED_AGGREGATIONS, ALLOWED_GRANULARITIES, ALLOWED_TABLES, validate_identifier
