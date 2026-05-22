import sys
import sqlite3

sys.path.append("/Users/christianykelly/Desktop/MonitorWeb")

conn = sqlite3.connect("/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db")

from core.queries_deliveries import get_sla_monthly_trend

print("=== Test get_sla_monthly_trend ===")
df = get_sla_monthly_trend(conn)
print(f"Columnas: {df.columns.tolist()}")
print(df.to_string())

conn.close()
