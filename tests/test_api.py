import pytest
from unittest.mock import patch, PropertyMock
from core.state import AppState

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
    with patch.object(AppState, 'is_syncing', new_callable=PropertyMock) as mock_sync:
        mock_sync.return_value = False
        with patch("routes.sync._run_sync_pipeline") as mock_pipeline:
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
    sql = data["sql_text"]
    
    # Comprobar que el SQL generado contenga las columnas correctas dentro de la subconsulta
    assert "area_negocio" in sql
    assert "fecha_carga" in sql
    assert "outbound_deliveries.area_negocio AS categoria" in sql
    assert "FROM (SELECT entrega, MAX(outbound_deliveries.dias_retraso) as dias_retraso, fecha_carga, area_negocio" in sql


def test_analytics_sla_route(auth_client, test_db):
    """
    Verifica que la ruta de auditoría SLA resuelva dinámicamente las áreas
    de negocio y que no muestre 'OTRO'.
    """
    from datetime import datetime
    current_year = str(datetime.now().year)

    # Insertamos datos de prueba en la tabla outbound_deliveries
    test_db.execute(
        "INSERT INTO outbound_deliveries (entrega, fecha_carga, ubicacion_area, area_negocio, dias_retraso) "
        "VALUES (?, ?, ?, ?, ?)",
        ('8001', f'01-05-{current_year}', 'MOLTR1-106', 'OTRO', 5)
    )
    test_db.execute(
        "INSERT INTO outbound_deliveries (entrega, fecha_carga, ubicacion_area, area_negocio, dias_retraso) "
        "VALUES (?, ?, ?, ?, ?)",
        ('8002', f'01-05-{current_year}', 'UNMAPPED-XXX', 'OTRO', 5)
    )
    test_db.commit()

    response = auth_client.get("/analytics/sla?type=late")
    assert response.status_code == 200
    
    # Comprobar que MOLDURAS aparece resuelto para la entrega 8001
    assert "MOLDURAS" in response.text
    # Comprobar que S/N aparece para la entrega 8002 (no mapeado)
    assert "S/N" in response.text
    # Comprobar que "OTRO" NO aparece como área de negocio para estas entregas
    # (El texto completo de la tabla no debe tener la insignia de "OTRO")
    assert '<span class="area-badge">OTRO</span>' not in response.text


