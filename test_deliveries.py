import sys
import logging
logging.basicConfig(level=logging.DEBUG)

from core.database import SessionLocal
from services.deliveries_service import DeliveriesService

db = SessionLocal()
try:
    svc = DeliveriesService(db)
    ctx = svc.get_full_context()
    print("KEYS:", ctx.keys())
    if not ctx:
        print("CONTEXT IS EMPTY!")
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
