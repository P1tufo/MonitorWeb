import sqlite3
import pandas as pd

db_path = "/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db"
conn = sqlite3.connect(db_path)

df = pd.read_sql("SELECT DISTINCT fecha_carga FROM outbound_deliveries", conn)
print("Distinct fecha_carga:")
print(df)

df_months = pd.read_sql(
    "SELECT substr(fecha_carga, 7, 4) || '-' || substr(fecha_carga, 4, 2) as month, count(*) as count "
    "FROM outbound_deliveries GROUP BY month",
    conn
)
print("\nCounts by Month:")
print(df_months)

conn.close()
