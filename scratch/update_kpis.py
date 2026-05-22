import sqlite3
import json

db_path = "data/wms_transactions.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Update vl_kpi_ontime (Entregadas a tiempo)
ontime_sql = """SELECT 
  substr(outbound_deliveries.fecha_carga, 7, 4) AS fecha,
  'Total' AS categoria,
  COUNT(DISTINCT outbound_deliveries.entrega) AS valor
FROM outbound_deliveries
WHERE (julianday(substr(outbound_deliveries.fecha_sm_real, 7, 4) || '-' || substr(outbound_deliveries.fecha_sm_real, 4, 2) || '-' || substr(outbound_deliveries.fecha_sm_real, 1, 2)) - julianday(substr(outbound_deliveries.fecha_carga, 7, 4) || '-' || substr(outbound_deliveries.fecha_carga, 4, 2) || '-' || substr(outbound_deliveries.fecha_carga, 1, 2))) <= 2
GROUP BY fecha
ORDER BY fecha ASC;"""

ontime_visual = {
  "baseTable": "outbound_deliveries",
  "joins": [],
  "filters": [
    {
      "column": "outbound_deliveries.fecha_carga",
      "operator": "lessthanequal",
      "value": "",
      "valueType": "date_diff",
      "compareColumn": "outbound_deliveries.fecha_sm_real",
      "offsetValue": "2"
    }
  ],
  "metric": {
    "column": "outbound_deliveries.entrega",
    "aggregation": "COUNT_DISTINCT"
  },
  "timeAxis": {
    "column": "outbound_deliveries.fecha_carga",
    "granularity": "YEAR"
  },
  "breakdown": "",
  "chartType": "kpi"
}

cursor.execute(
    "UPDATE config_queries SET sql_text = ?, visual_state = ? WHERE query_id = 'vl_kpi_ontime'",
    (ontime_sql, json.dumps(ontime_visual))
)

# 2. Update vl_kpi_late (Entregas atrasadas)
late_sql = """SELECT 
  substr(outbound_deliveries.fecha_carga, 7, 4) AS fecha,
  'Total' AS categoria,
  COUNT(DISTINCT outbound_deliveries.entrega) AS valor
FROM outbound_deliveries
WHERE (julianday(substr(outbound_deliveries.fecha_sm_real, 7, 4) || '-' || substr(outbound_deliveries.fecha_sm_real, 4, 2) || '-' || substr(outbound_deliveries.fecha_sm_real, 1, 2)) - julianday(substr(outbound_deliveries.fecha_carga, 7, 4) || '-' || substr(outbound_deliveries.fecha_carga, 4, 2) || '-' || substr(outbound_deliveries.fecha_carga, 1, 2))) > 2
GROUP BY fecha
ORDER BY fecha ASC;"""

late_visual = {
  "baseTable": "outbound_deliveries",
  "joins": [],
  "filters": [
    {
      "column": "outbound_deliveries.fecha_carga",
      "operator": "greaterthan",
      "value": "",
      "valueType": "date_diff",
      "compareColumn": "outbound_deliveries.fecha_sm_real",
      "offsetValue": "2"
    }
  ],
  "metric": {
    "column": "outbound_deliveries.entrega",
    "aggregation": "COUNT_DISTINCT"
  },
  "timeAxis": {
    "column": "outbound_deliveries.fecha_carga",
    "granularity": "YEAR"
  },
  "breakdown": "",
  "chartType": "kpi"
}

cursor.execute(
    "UPDATE config_queries SET sql_text = ?, visual_state = ? WHERE query_id = 'vl_kpi_late'",
    (late_sql, json.dumps(late_visual))
)

conn.commit()
conn.close()
print("KPI queries updated and aligned successfully!")
