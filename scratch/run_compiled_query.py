import sqlite3
import pandas as pd

conn = sqlite3.connect("/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db")
query = """
SELECT 
  substr(outbound_deliveries.fecha_carga, 7, 4) || '-' || substr(outbound_deliveries.fecha_carga, 4, 2) AS fecha,
  'Total' AS categoria,
  ROUND(SUM(CASE WHEN outbound_deliveries.dias_retraso <= 2 THEN 100.0 ELSE 0.0 END) / COUNT(*), 1) AS valor
FROM (SELECT entrega, MAX(outbound_deliveries.dias_retraso) as dias_retraso, fecha_carga FROM outbound_deliveries WHERE outbound_deliveries.dias_retraso IS NOT NULL GROUP BY entrega) AS outbound_deliveries
WHERE outbound_deliveries.fecha_carga LIKE '%2026%'
GROUP BY fecha
ORDER BY fecha ASC;
"""
try:
    df = pd.read_sql(query, conn)
    print("DataFrame for '%2026%':")
    print(df)
except Exception as e:
    print(f"Error: {e}")

# Also try with '2026%'
query2 = """
SELECT 
  substr(outbound_deliveries.fecha_carga, 7, 4) || '-' || substr(outbound_deliveries.fecha_carga, 4, 2) AS fecha,
  'Total' AS categoria,
  ROUND(SUM(CASE WHEN outbound_deliveries.dias_retraso <= 2 THEN 100.0 ELSE 0.0 END) / COUNT(*), 1) AS valor
FROM (SELECT entrega, MAX(outbound_deliveries.dias_retraso) as dias_retraso, fecha_carga FROM outbound_deliveries WHERE outbound_deliveries.dias_retraso IS NOT NULL GROUP BY entrega) AS outbound_deliveries
WHERE outbound_deliveries.fecha_carga LIKE '2026%'
GROUP BY fecha
ORDER BY fecha ASC;
"""
try:
    df2 = pd.read_sql(query2, conn)
    print("\nDataFrame for '2026%':")
    print(df2)
except Exception as e:
    print(f"Error: {e}")

conn.close()
