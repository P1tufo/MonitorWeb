import uvicorn
from config import app
import threading
import time
import requests

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="critical")

t = threading.Thread(target=run_server, daemon=True)
t.start()

time.sleep(3)
try:
    resp = requests.get("http://127.0.0.1:8001/analytics")
    print(f"Status: {resp.status_code}")
except Exception as e:
    print(f"Error: {e}")

