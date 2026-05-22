import sqlite3
import pandas as pd

db_path = "/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db"
conn = sqlite3.connect(db_path)

# Query compiled by builder for vl_sla_monthly_trend
# Eje X: outbound_deliveries.fecha_carga (MONTH)
# Metric: SLA_EFFICIENCY (dias_retraso)
# Filter: outbound_deliveries.fecha_carga contains 2026

sql = """
SELECT 
  substr(outbound_deliveries.fecha_carga, 7, 4) || '-' || substr(outbound_deliveries.fecha_carga, 4, 2) AS fecha,
  'Total' AS categoria,
  ROUND(SUM(CASE WHEN outbound_deliveries.dias_retraso <= 2 THEN 100.0 ELSE 0.0 END) / COUNT(*), 1) AS valor
FROM (SELECT entrega, MAX(outbound_deliveries.dias_retraso) as dias_retraso, fecha_carga FROM outbound_deliveries WHERE outbound_deliveries.dias_retraso IS NOT NULL GROUP BY entrega) AS outbound_deliveries
WHERE outbound_deliveries.fecha_carga LIKE ?
GROUP BY fecha
ORDER BY fecha ASC;
"""

df = pd.read_sql(sql, conn, params=("%2026%",))
print("Result of compiled query:")
print(df)

conn.close()
