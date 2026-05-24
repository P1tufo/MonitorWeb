from core.pdf_queries import get_deliveries_for_bulk
from core.database import get_session
import pandas as pd
with get_session() as session:
    df = get_deliveries_for_bulk(session.connection().connection, None, None, "Paneles", "OT Abierta", None)
    print("Num entregas:", len(df))
