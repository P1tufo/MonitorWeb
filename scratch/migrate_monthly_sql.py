"""
Migra el SQL de vl_sla_monthly_trend en la BD de configuración
al nuevo formato estándar: fecha, categoria, valor
"""
import sqlite3
import json

DB_PATH = "/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db"

NEW_SQL = """SELECT 
  substr(outbound_deliveries.fecha_carga, 7, 4) || '-' || substr(outbound_deliveries.fecha_carga, 4, 2) AS fecha,
  'Total' AS categoria,
  ROUND(SUM(CASE WHEN outbound_deliveries.dias_retraso <= 2 THEN 100.0 ELSE 0.0 END) / COUNT(*), 1) AS valor
FROM (SELECT entrega, MAX(outbound_deliveries.dias_retraso) as dias_retraso, fecha_carga FROM outbound_deliveries WHERE outbound_deliveries.dias_retraso IS NOT NULL GROUP BY entrega) AS outbound_deliveries
WHERE outbound_deliveries.fecha_carga LIKE ?
GROUP BY fecha
ORDER BY fecha ASC;"""

NEW_VISUAL_STATE = json.dumps({
    "baseTable": "outbound_deliveries",
    "joins": [],
    "filters": [
        {
            "column": "outbound_deliveries.fecha_carga",
            "operator": "contains",
            "value": "2026"
        }
    ],
    "metric": {
        "column": "outbound_deliveries.dias_retraso",
        "aggregation": "SLA_EFFICIENCY",
        "format": "percent"
    },
    "timeAxis": {
        "column": "outbound_deliveries.fecha_carga",
        "granularity": "MONTH"
    },
    "breakdown": "",
    "chartType": "line"
})

conn = sqlite3.connect(DB_PATH)
conn.execute(
    "UPDATE config_queries SET sql_text = ?, visual_state = ? WHERE query_id = 'vl_sla_monthly_trend'",
    (NEW_SQL, NEW_VISUAL_STATE)
)
conn.commit()

# Verificar
row = conn.execute("SELECT query_id, sql_text, visual_state FROM config_queries WHERE query_id = 'vl_sla_monthly_trend'").fetchone()
print("Actualizado:", row[0])
print("SQL:\n", row[1])
print("\nVisual State:", row[2])

# Test: ejecutar con %2026%
import pandas as pd
df = pd.read_sql(NEW_SQL, conn, params=("%2026%",))
print("\nResultado:")
print(df.to_string())

conn.close()
