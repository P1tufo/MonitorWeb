import sqlite3

DB_PATH = "data/wms_transactions.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(outbound_deliveries)")
for col in cursor.fetchall():
    print(col)
conn.close()
