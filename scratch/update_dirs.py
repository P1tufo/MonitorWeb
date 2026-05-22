import sqlite3

db_path = "data/wms_transactions.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

settings = [
    ("DIR_DELIVERIES", "VL06O"),
    ("DIR_STOCK", "LX02"),
    ("DIR_TASKS", "LT22"),
    ("DIR_MOVEMENTS", "MB51")
]

for key, value in settings:
    cursor.execute(
        "UPDATE app_settings SET value = ? WHERE key = ?",
        (value, key)
    )
    print(f"Updated {key} to {value}. Rows affected: {cursor.rowcount}")

conn.commit()
conn.close()
print("Done.")
