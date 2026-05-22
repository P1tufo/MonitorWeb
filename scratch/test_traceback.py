import sqlite3
import traceback
import logging

logging.basicConfig(level=logging.DEBUG)

def run():
    import sys
    sys.path.append('.')
    from routes.analytics_mb51 import _prepare_planned_consumption_trend
    from config import DB_PATH
    
    conn = sqlite3.connect(DB_PATH)
    try:
        res = _prepare_planned_consumption_trend(conn)
        print("Success! Keys:", res.keys())
    except Exception as e:
        traceback.print_exc()

run()
