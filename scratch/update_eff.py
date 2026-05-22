import sqlite3
import json

db_path = "data/wms_transactions.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Update Eficiencia de Bodega (vl_kpi_eff) SQL and Visual State
eff_sql = """SELECT ROUND(COUNT(DISTINCT CASE WHEN max_diff <= 2 THEN entrega END) * 100.0 / COUNT(DISTINCT entrega), 1) as efficiency
FROM (
  SELECT 
    entrega, 
    (julianday(substr(fecha_sm_real, 7, 4) || '-' || substr(fecha_sm_real, 4, 2) || '-' || substr(fecha_sm_real, 1, 2)) - julianday(substr(fecha_carga, 7, 4) || '-' || substr(fecha_carga, 4, 2) || '-' || substr(fecha_carga, 1, 2))) as max_diff
  FROM outbound_deliveries
  WHERE substr(fecha_carga, 7, 4) = (SELECT MAX(substr(fecha_carga, 7, 4)) FROM outbound_deliveries)
)"""

eff_visual = {
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
    "aggregation": "COUNT_DISTINCT",
    "format": "percent"
  },
  "timeAxis": {
    "column": "outbound_deliveries.fecha_carga",
    "granularity": "YEAR"
  },
  "breakdown": "",
  "chartType": "kpi"
}

cursor.execute(
    "UPDATE config_queries SET sql_text = ?, visual_state = ? WHERE query_id = 'vl_kpi_eff'",
    (eff_sql, json.dumps(eff_visual))
)

conn.commit()
conn.close()
print("Eficiencia de Bodega KPI updated and aligned successfully!")
