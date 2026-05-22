import sqlite3
from pathlib import Path

db_path = "data/wms_transactions.db"
file_path = Path("/Users/christianykelly/Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Transacciones/Entregas/VL06o_5.txt")

stats = file_path.stat()
mtime = stats.st_mtime
size = stats.st_size
path_str = str(file_path.absolute())

print("On disk:")
print("  mtime:", mtime)
print("  size:", size)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute(
    "SELECT last_modified, file_size FROM sync_manifest WHERE file_path = ?", 
    (path_str,)
)
row = cursor.fetchone()
print("In DB:")
if row:
    db_mtime, db_size = row
    print("  db_mtime:", db_mtime)
    print("  db_size:", db_size)
    print("  db_mtime == mtime:", db_mtime == mtime)
    print("  db_size == size:", db_size == size)
    
    # Try selecting with format/casting
    cursor.execute(
        "SELECT CAST(last_modified AS TEXT), last_modified FROM sync_manifest WHERE file_path = ?", 
        (path_str,)
    )
    txt_mtime, real_mtime = cursor.fetchone()
    print("  as text in query:", txt_mtime)
    print("  real value:", real_mtime)
else:
    print("  Not found in DB")
conn.close()
