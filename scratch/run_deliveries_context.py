import sqlite3
import pandas as pd
import logging
import sys

# Configure logging to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Add the project directory to path
sys.path.append("/Users/christianykelly/Desktop/MonitorWeb")

from routes.deliveries import get_deliveries_context

db_path = "/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db"
conn = sqlite3.connect(db_path)

try:
    ctx = get_deliveries_context(conn)
    print("Context generated successfully!")
    print(f"Keys in context: {list(ctx.keys())}")
    print(f"sla_monthly_labels: {ctx.get('sla_monthly_labels')}")
    print(f"sla_monthly_data: {ctx.get('sla_monthly_data')}")
except Exception as e:
    import traceback
    print("EXCEPTION OCCURRED:")
    traceback.print_exc()

conn.close()
