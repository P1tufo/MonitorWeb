import sqlite3
import json

db_path = "/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Update vl_kpi_ontime
vs_ontime = json.dumps({
    "baseTable": "outbound_deliveries",
    "joins": [],
    "filters": [
        {"column": "outbound_deliveries.fecha_carga", "operator": "contains", "value": "2026"},
        {"column": "outbound_deliveries.dias_retraso", "operator": "lessthan", "value": "3"}
    ],
    "metric": {"column": "outbound_deliveries.entrega", "aggregation": "COUNT_DISTINCT"},
    "timeAxis": {"column": "", "granularity": "MONTH"},
    "breakdown": "",
    "chartType": "kpi"
})
sql_ontime = "SELECT COUNT(DISTINCT outbound_deliveries.entrega) as valor FROM outbound_deliveries WHERE (outbound_deliveries.dias_retraso IS NOT NULL AND outbound_deliveries.dias_retraso < 3) AND (outbound_deliveries.fecha_carga LIKE ?)"

cursor.execute(
    "UPDATE config_queries SET sql_text = ?, visual_state = ? WHERE query_id = 'vl_kpi_ontime'",
    (sql_ontime, vs_ontime)
)
print("Updated vl_kpi_ontime:", cursor.rowcount)

# 2. Update vl_kpi_late
vs_late = json.dumps({
    "baseTable": "outbound_deliveries",
    "joins": [],
    "filters": [
        {"column": "outbound_deliveries.fecha_carga", "operator": "contains", "value": "2026"},
        {"column": "outbound_deliveries.dias_retraso", "operator": "greaterthan", "value": "2"}
    ],
    "metric": {"column": "outbound_deliveries.entrega", "aggregation": "COUNT_DISTINCT"},
    "timeAxis": {"column": "", "granularity": "MONTH"},
    "breakdown": "",
    "chartType": "kpi"
})
sql_late = "SELECT COUNT(DISTINCT outbound_deliveries.entrega) as valor FROM outbound_deliveries WHERE (outbound_deliveries.dias_retraso IS NOT NULL AND outbound_deliveries.dias_retraso > 2) AND (outbound_deliveries.fecha_carga LIKE ?)"

cursor.execute(
    "UPDATE config_queries SET sql_text = ?, visual_state = ? WHERE query_id = 'vl_kpi_late'",
    (sql_late, vs_late)
)
print("Updated vl_kpi_late:", cursor.rowcount)

conn.commit()
conn.close()
