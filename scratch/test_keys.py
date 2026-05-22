import sqlite3
from routes.analytics_mb51 import get_mb51_context
from config import DB_PATH

conn = sqlite3.connect(DB_PATH)
ctx = get_mb51_context(conn)
print([k for k in ctx.keys() if 'top_materials' in k])
