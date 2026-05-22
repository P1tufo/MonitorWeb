import sqlite3
import pandas as pd

conn = sqlite3.connect("/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db")

query = """
SELECT 
    substr(fecha_carga, 7, 4) as year,
    substr(fecha_carga, 4, 2) as month,
    COUNT(*) as total_rows,
    COUNT(DISTINCT entrega) as distinct_deliveries,
    SUM(CASE WHEN dias_retraso IS NOT NULL THEN 1 ELSE 0 END) as non_null_delay
FROM outbound_deliveries
GROUP BY year, month
ORDER BY year, month;
"""

df = pd.read_sql(query, conn)
print(df)

conn.close()
