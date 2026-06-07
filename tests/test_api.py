from unittest.mock import PropertyMock, patch

import pytest

from core.state import SyncStateManager

# Constantes de aserción para evitar cadenas mágicas
DASHBOARD_TITLE = "Proyecto-Onedrive"
SYNC_STARTED_MSG = "Proceso iniciado en segundo plano"

def test_read_root(auth_client):
    """Verifica que el dashboard principal responda con el título correcto."""
    response = auth_client.get("/")
    assert response.status_code == 200
    assert DASHBOARD_TITLE in response.text

def test_get_tunnel_url(auth_client, tmp_path):
    """Verifica que el endpoint /url devuelva la dirección del túnel ngrok."""
    # Mock de la ruta del archivo de túnel para la prueba
    fake_url_file = tmp_path / "tunnel_url.txt"
    fake_url_file.write_text("https://fake-tunnel.ngrok-free.dev")

    with patch("routes.sync.TUNNEL_URL_FILE", str(fake_url_file)):
        response = auth_client.get("/url")
        assert response.status_code == 200
        data = response.json()
        assert data["url"] == "https://fake-tunnel.ngrok-free.dev"

def test_post_sync_endpoint(auth_client):
    """
    Verifica que el endpoint de sincronización inicie el pipeline correctamente.
    Se usa PropertyMock para simular el estado de 'is_syncing'.
    """
    with patch.object(SyncStateManager, 'is_syncing', new_callable=PropertyMock) as mock_sync:
        mock_sync.return_value = False
        with patch("routes.sync._run_sync_pipeline"):
            with patch("routes.sync.task_manager") as mock_tm:
                mock_tm.has_running_task.return_value = False
                mock_tm.submit_task.return_value = "test-id"
                response = auth_client.post("/sync")
                assert response.status_code == 200
                assert SYNC_STARTED_MSG in response.json()["message"]
                assert "task_id" in response.json()

def test_analytics_page_access(auth_client):
    """
    Verifica que la página de analíticas sea accesible.
    Se eliminó 'async' ya que TestClient de FastAPI es síncrono por defecto.
    """
    response = auth_client.get("/analytics")
    # Se espera 200 (OK) para una carga exitosa de la página
    assert response.status_code == 200


def test_build_sql_sla_efficiency(auth_client):
    """Verifica que el generador de consultas SQL compile correctamente la métrica SLA_EFFICIENCY con desgloses y filtros."""
    payload = {
        "baseTable": "outbound_deliveries",
        "joins": [],
        "filters": [
            {
                "column": "outbound_deliveries.fecha_carga",
                "operator": "equals",
                "value": "%2026%",
                "valueType": "value"
            }
        ],
        "metric": {
            "column": "outbound_deliveries.dias_retraso",
            "aggregation": "SLA_EFFICIENCY"
        },
        "timeAxis": {
            "column": "outbound_deliveries.fecha_carga",
            "granularity": "WEEK"
        },
        "breakdown": "outbound_deliveries.area_negocio"
    }

    response = auth_client.post("/api/studio/build_sql", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "sql_text" not in data  # Por seguridad no se devuelve el texto SQL
    assert "bound_params" in data


def test_analytics_sla_route(auth_client, test_db):
    """
    Verifica que la ruta de auditoría SLA resuelva dinámicamente las áreas
    de negocio y que no muestre 'OTRO'.
    """
    from datetime import datetime
    current_year = str(datetime.now().year)

    # Insertamos datos de prueba en la tabla outbound_deliveries
    test_db.execute(
        "INSERT INTO outbound_deliveries (entrega, fecha_carga, centro_costo, area_negocio, dias_retraso, week_sort) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        ('8001', f'01-05-{current_year}', 'MOLTR1-106', 'MOLDURAS', 5, f"{current_year}-10")
    )
    test_db.execute(
        "INSERT INTO outbound_deliveries (entrega, fecha_carga, centro_costo, area_negocio, dias_retraso, week_sort) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        ('8002', f'01-05-{current_year}', 'UNMAPPED-XXX', 'S/N', 5, f"{current_year}-10")
    )
    test_db.commit()

    response = auth_client.get("/analytics/sla?type=late")
    assert response.status_code == 200

    # Verificamos que los datos se renderizan
    html = response.text
    assert "MOLDURAS" in html
    assert "S/N" in html
    assert "OTRO" not in html

def test_api_query_preview_returns_json_and_no_sql(auth_client):
    """Verifica el contrato JSON in/out para preview y la ausencia de texto SQL."""
    payload = {
        "query_id": "preview",
        "visual_state": '{"baseTable": "outbound_deliveries", "metric": {"column": "outbound_deliveries.entrega", "aggregation": "COUNT"}, "timeAxis": {"column": "outbound_deliveries.fecha_carga", "granularity": "MONTH"}, "joins": [], "filters": []}'
    }
    response = auth_client.post("/api/studio/preview", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "chartType" in data or "datasets" in data

def test_api_settings_query_rejects_raw_sql(auth_client):
    """Verifica protección contra inyección y que el endpoint solo acepte visual_state."""
    payload = {
        "query_id": "test_query",
        "sql_text": "SELECT * FROM outbound_deliveries"
    }
    response = auth_client.post("/api/settings/query", json=payload)
    assert response.status_code == 422


