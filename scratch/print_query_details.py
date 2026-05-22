import sqlite3

db_path = "/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT query_id, sql_text, visual_state FROM config_queries WHERE query_id = 'vl_sla_monthly_trend'")
row = cursor.fetchone()
if row:
    print(f"query_id: {row[0]}")
    print(f"sql_text:\n{row[1]}")
    print(f"visual_state:\n{row[2]}")
else:
    print("Not found!")

conn.close()
