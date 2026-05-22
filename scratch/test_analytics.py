import sqlite3
import traceback
from config import DB_PATH
from routes.analytics_vl06o import analytics

class FakeRequest:
    pass

try:
    res = analytics(FakeRequest())
    print("Success")
except Exception as e:
    traceback.print_exc()
