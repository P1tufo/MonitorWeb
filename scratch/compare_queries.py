import sqlite3
import pandas as pd

conn = sqlite3.connect("/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db")

# 1. Ver SQL actual en la BD para vl_sla_monthly_trend
row = conn.execute("SELECT query_id, sql_text FROM config_queries WHERE query_id = 'vl_sla_monthly_trend'").fetchone()
print("=== SQL en BD ===")
print(row[1])
print()

# 2. Ejecutar ese SQL con SLA_THRESHOLD=2 (como en el codigo)
sql_old = row[1]
print("=== Resultado con params=(2,) ===")
df_old = pd.read_sql(sql_old, conn, params=(2,))
print(df_old.to_string())
print()

# 3. Comparar con el SQL nuevo del Visual Builder
sql_new = """
SELECT 
  substr(outbound_deliveries.fecha_carga, 7, 4) || '-' || substr(outbound_deliveries.fecha_carga, 4, 2) AS fecha,
  'Total' AS categoria,
  ROUND(SUM(CASE WHEN outbound_deliveries.dias_retraso <= 2 THEN 100.0 ELSE 0.0 END) / COUNT(*), 1) AS valor
FROM (SELECT entrega, MAX(outbound_deliveries.dias_retraso) as dias_retraso, fecha_carga FROM outbound_deliveries WHERE outbound_deliveries.dias_retraso IS NOT NULL GROUP BY entrega) AS outbound_deliveries
WHERE outbound_deliveries.fecha_carga LIKE ?
GROUP BY fecha
ORDER BY fecha ASC;
"""
print("=== Resultado SQL nuevo con '%2026%' ===")
df_new = pd.read_sql(sql_new, conn, params=("%2026%",))
print(df_new.to_string())

conn.close()
