import sqlite3
import pandas as pd

DB_PATH = "data/wms_transactions.db"
conn = sqlite3.connect(DB_PATH)

deliveries = ('819224843', '819224818', '819224817', '819227365', '819227364')
query = f"""
    SELECT entrega, ubicacion_area, area_negocio, centro 
    FROM outbound_deliveries 
    WHERE entrega IN {deliveries}
"""
df = pd.read_sql(query, conn)
print(df.to_string())
conn.close()
