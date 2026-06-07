"""
core/macros.py — Centralización de reglas de negocio y macros SQL.

Fuente única de verdad para expresiones complejas y lógicas de negocio
que deban inyectarse en el código SQL en múltiples capas de la aplicación.
"""

AREA_EXPR = """CASE
    WHEN (SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(COALESCE(NULLIF(v.centro_costo, ''), NULLIF(v.ubicacion_bin_1, ''), NULLIF(v.ubicacion_bin, '')), 1, 6)) IS NOT NULL
    THEN (SELECT business_area FROM config_cost_center_mapping WHERE center_code = SUBSTR(COALESCE(NULLIF(v.centro_costo, ''), NULLIF(v.ubicacion_bin_1, ''), NULLIF(v.ubicacion_bin, '')), 1, 6))
    WHEN v.area_negocio IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.area_negocio
    WHEN v.centro_costo IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.centro_costo
    WHEN v.ubicacion_bin_1 IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin_1
    WHEN v.ubicacion_bin IN ('ASERRADERO', 'LINEA 1', 'LINEA 2', 'MOLDURAS', 'PLANTA_ENERGIA', 'RANURADO', 'REMANUFACTURA', 'VIGAS') THEN v.ubicacion_bin
    ELSE 'S/N'
END"""

# Usuarios genéricos o del sistema excluidos explícitamente de las métricas de inactividad
EXCLUDED_USERS_INACTIVITY = ('cvalderrama', 'e_sperezb', 'gmolina')
def inject_macros(sql: str) -> str:
    """
    Inyecta todas las macros globales registradas en el string SQL
    proporcionado. Evita realizar múltiples .replace() esparcidos por el código.
    """
    if sql and "{AREA_EXPR}" in sql:
        sql = sql.replace("{AREA_EXPR}", AREA_EXPR)
    return sql
