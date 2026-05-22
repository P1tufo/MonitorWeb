import sqlite3
import pandas as pd
import json

db_path = "/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db"
conn = sqlite3.connect(db_path)

df = pd.read_sql("SELECT * FROM config_queries", conn)
for idx, row in df.iterrows():
    print(f"=== Query: {row['query_id']} ===")
    print(f"SQL:\n{row['sql_text']}")
    if row['visual_state']:
        print("Visual State:")
        try:
            print(json.dumps(json.loads(row['visual_state']), indent=2))
        except Exception:
            print(row['visual_state'])
    print("\n" + "="*40 + "\n")

conn.close()
