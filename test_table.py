from routes.filters import _build_unified_where
where_clause, params = _build_unified_where(None, None, "Paneles", "OT_ABIERTA", "2026-21")
print(where_clause)
print(params)

from core.database import get_session
import pandas as pd
with get_session() as session:
    q = f"SELECT v.entrega FROM outbound_deliveries v {where_clause}"
    df = pd.read_sql(q, session.connection().connection, params=params)
    print("Num entregas en tabla:", len(df))
