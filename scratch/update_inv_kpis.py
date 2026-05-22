import sqlite3
import json

db_path = "/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Traspasos (inv_kpi_traspasos)
sql_trasp = "SELECT COUNT(*) as total_qty FROM inventory_movements WHERE TRIM(cmv) IN ('301', '303') AND (inventory_movements.fe_contab LIKE ?)"
vs_trasp = json.dumps({
    "baseTable": "inventory_movements",
    "joins": [],
    "filters": [
        {"column": "inventory_movements.cmv", "operator": "contains", "value": "30"},
        {"column": "inventory_movements.fe_contab", "operator": "contains", "value": "2026"}
    ],
    "metric": {"column": "inventory_movements.material", "aggregation": "COUNT"},
    "timeAxis": {"column": "", "granularity": "YEAR"},
    "breakdown": "",
    "chartType": "kpi"
})

# 2. Tasa Devoluciones (inv_kpi_rate_devolucion)
sql_dev = "SELECT ROUND(SUM(CASE WHEN TRIM(cmv) IN ('202', '262') THEN 1.0 ELSE 0.0 END) * 100.0 / COALESCE(NULLIF(SUM(CASE WHEN inventory_movements.tipo_operacion LIKE '%Centro Costo%' OR inventory_movements.tipo_operacion LIKE '%Orden/Reserva%' THEN 1.0 ELSE 0.0 END), 0), 1), 1) as valor FROM inventory_movements WHERE (inventory_movements.fe_contab LIKE ?)"
vs_dev = json.dumps({
    "baseTable": "inventory_movements",
    "joins": [],
    "filters": [
        {"column": "inventory_movements.fe_contab", "operator": "contains", "value": "2026"}
    ],
    "metric": {"column": "inventory_movements.tipo_operacion", "aggregation": "RETURN_RATE", "format": "percent"},
    "timeAxis": {"column": "", "granularity": "YEAR"},
    "breakdown": "",
    "chartType": "kpi"
})

# 3. Eficiencia de Bodega (inv_kpi_rate_eficiencia)
sql_eff = "SELECT ROUND(SUM(CASE WHEN (julianday(substr(registrado, 7, 4) || '-' || substr(registrado, 4, 2) || '-' || substr(registrado, 1, 2)) - julianday(substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) || '-' || substr(fe_contab, 1, 2))) <= 3.0 THEN 100.0 ELSE 0.0 END) / COUNT(*), 1) as valor FROM inventory_movements WHERE fe_contab IS NOT NULL AND registrado IS NOT NULL AND length(fe_contab) >= 10 AND length(registrado) >= 10 AND (inventory_movements.fe_contab LIKE ?)"
vs_eff = json.dumps({
    "baseTable": "inventory_movements",
    "joins": [],
    "filters": [
        {"column": "inventory_movements.fe_contab", "operator": "contains", "value": "2026"}
    ],
    "metric": {"column": "inventory_movements.tipo_operacion", "aggregation": "INV_EFFICIENCY", "format": "percent"},
    "timeAxis": {"column": "", "granularity": "YEAR"},
    "breakdown": "",
    "chartType": "kpi"
})

# Execute updates
cursor.execute("UPDATE config_queries SET sql_text = ?, visual_state = ? WHERE query_id = 'inv_kpi_traspasos'", (sql_trasp, vs_trasp))
print("Updated traspasos:", cursor.rowcount)

cursor.execute("UPDATE config_queries SET sql_text = ?, visual_state = ? WHERE query_id = 'inv_kpi_rate_devolucion'", (sql_dev, vs_dev))
print("Updated dev rate:", cursor.rowcount)

cursor.execute("UPDATE config_queries SET sql_text = ?, visual_state = ? WHERE query_id = 'inv_kpi_rate_eficiencia'", (sql_eff, vs_eff))
print("Updated inventory efficiency:", cursor.rowcount)

# Double check 2026 values
cursor.execute(sql_trasp, ("%2026%",))
print("Tested Traspasos 2026:", cursor.fetchone()[0])

cursor.execute(sql_dev, ("%2026%",))
print("Tested Dev Rate 2026:", cursor.fetchone()[0])

cursor.execute(sql_eff, ("%2026%",))
print("Tested Inv Efficiency 2026:", cursor.fetchone()[0])

conn.commit()
conn.close()
