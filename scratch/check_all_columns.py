import sqlite3
import pandas as pd

DB_PATH = "data/wms_transactions.db"
conn = sqlite3.connect(DB_PATH)

query = "SELECT * FROM outbound_deliveries WHERE entrega = '819224843'"
df = pd.read_sql(query, conn)
for col in df.columns:
    print(f"{col}: {df[col].iloc[0]}")
conn.close()
