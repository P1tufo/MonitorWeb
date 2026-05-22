import sqlite3
import json
import pandas as pd

db_path = "/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get vl_kpi_ontime
res = cursor.execute("SELECT query_id, sql_text, visual_state FROM config_queries WHERE query_id = 'vl_kpi_ontime'").fetchone()
if res:
    query_id, sql_text, visual_state = res
    print("=== vl_kpi_ontime ===")
    print("SQL Text:\n", sql_text)
    print("Visual State:\n", visual_state)
else:
    print("vl_kpi_ontime not found!")

# Let's also check the actual count of deliveries using both methods:
# Method 1: The direct SQL seeded in the database
if res:
    try:
        # Check actual values in the database for fecha_carga contains 2026
        # First: max year in outbound_deliveries
        max_yr = cursor.execute("SELECT MAX(substr(fecha_carga, 7, 4)) FROM outbound_deliveries").fetchone()[0]
        print("\nMax year in outbound_deliveries:", max_yr)
        
        # Count using SQL Text:
        # If there are '?' in sql_text:
        params = ()
        if sql_text.count("?") > 0:
            import json
            if visual_state:
                state = json.loads(visual_state)
                filters = state.get("filters", [])
                bound_params = []
                for f in filters:
                    if f.get("valueType", "value") != "value":
                        continue
                    op = f.get("operator", "").lower()
                    val = f.get("value", "")
                    if op in ["equals", "notequals", "greaterthan", "lessthan", "greaterthanequal", "greaterthanequals", "lessthanequal", "lessthanequals"]:
                        bound_params.append(val)
                    elif op in ["contains", "notcontains"]:
                        bound_params.append(f"%{val}%")
                params = tuple(bound_params)
                if len(params) != sql_text.count("?"):
                    params = (f"%{max_yr}",) if sql_text.count("?") == 1 else ()
            else:
                params = (f"%{max_yr}",) if sql_text.count("?") == 1 else ()
        
        df = pd.read_sql(sql_text, conn, params=params)
        print("\nResult using SQL Text in DB:", df.to_dict(orient='records'))
    except Exception as e:
        print("\nError running SQL Text:", e)

# Method 2: Let's count direct records in outbound_deliveries
try:
    total_distinct = cursor.execute("SELECT COUNT(DISTINCT entrega) FROM outbound_deliveries").fetchone()[0]
    print("\nTotal distinct deliveries in DB:", total_distinct)
    
    ontime_direct = cursor.execute("""
        SELECT SUM(CASE WHEN max_retraso <= 2 THEN 1 ELSE 0 END) as ontime_qty 
        FROM (
            SELECT entrega, MAX(dias_retraso) as max_retraso 
            FROM outbound_deliveries 
            WHERE dias_retraso IS NOT NULL 
              AND substr(fecha_carga, 7, 4) = (SELECT MAX(substr(fecha_carga, 7, 4)) FROM outbound_deliveries) 
            GROUP BY entrega
        )
    """).fetchone()[0]
    print("On-time direct count (Method 1 sql):", ontime_direct)
except Exception as e:
    print("Error counting direct:", e)

conn.close()
