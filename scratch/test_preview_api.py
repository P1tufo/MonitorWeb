import sys
import json
from fastapi.testclient import TestClient

sys.path.append("/Users/christianykelly/Desktop/MonitorWeb")
from main import app

client = TestClient(app)

# Login
login_response = client.post(
    "/api/auth/login",
    data={"username": "admin", "password": "admin"}
)
if login_response.status_code != 200:
    print("Login failed:", login_response.text)
    sys.exit(1)

token = login_response.json()["access_token"]
client.headers.update({"Authorization": f"Bearer {token}"})

# Test weekly trend
visual_state = {
    "baseTable": "outbound_deliveries",
    "joins": [],
    "filters": [
        {
            "column": "outbound_deliveries.fecha_carga",
            "operator": "contains",
            "value": "2026",
            "valueType": "value"
        }
    ],
    "metric": {
        "column": "outbound_deliveries.dias_retraso",
        "aggregation": "SLA_EFFICIENCY",
        "format": "percent"
    },
    "timeAxis": {
        "column": "outbound_deliveries.fecha_carga",
        "granularity": "WEEK"
    },
    "breakdown": "",
    "chartType": "line"
}

build_response = client.post("/api/studio/build_sql", json=visual_state)
build_data = build_response.json()

# Test preview using built sql and params
preview_payload = {
    "query_id": "vl_sla_trend",
    "sql_text": build_data["sql_text"],
    "params": build_data["bound_params"]
}

preview_response = client.post("/api/studio/preview", json=preview_payload)
preview_data = preview_response.json()
print("SLA Weekly Trend Preview size:", len(preview_data))
print("SLA Weekly Trend Preview data:")
print(json.dumps(preview_data[:5], indent=2))
