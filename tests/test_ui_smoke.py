import pytest
from typing import List, Tuple

# Configuración de marcadores de UI esperados por endpoint para facilitar el mantenimiento
# El formato es (cadena_buscada, descripción_del_componente)
EXPECTED_UI_MARKERS = {
    "/": [
        ('id="kpiDeliveries"', "KPI de entregas totales"),
        ('onclick="syncData(event)"', "Botón de sincronización de datos"),
        ('href="/analytics"', "Enlace de navegación a analíticas")
    ],
    "/analytics": [
        ('id="monthlyTrendChart"', "Gráfico de Tendencia Mensual"),
        ('id="slaMonthlyTrendChart"', "Gráfico SLA Mensual"),
        ('Entregas', "Etiqueta de entregas")
    ],
    "/inventory": [
        ('id="abcPieChart"', "Gráfico de segmentación ABC"),
        ('id="trendChart"', "Gráfico de tendencia histórica"),
        ('Inventario', "Etiqueta de inventario")
    ],
    "/settings": [
        ('Configuración del Sistema', "Título de configuración"),
        ('id="new-status-code"', "Input de nuevo estado"),
        ('Mapeo de Estados', "Sección de estados")
    ]
}

@pytest.mark.parametrize("path, markers", EXPECTED_UI_MARKERS.items())
def test_ui_smoke_components_presence(auth_client, path: str, markers: List[Tuple[str, str]]) -> None:
    """
    Prueba de humo parametrizada que verifica la presencia de componentes visuales críticos.
    Asegura que el servidor responda correctamente y que el HTML contenga los IDs necesarios 
    para la inicialización de los scripts de frontend (charts, handlers, etc).
    """
    # Realizar la petición al endpoint
    response = auth_client.get(path)
    
    # Validación de disponibilidad (Fail-Fast)
    assert response.status_code == 200, f"Fallo de disponibilidad en {path}. Status: {response.status_code}"
    
    # Búsqueda optimizada sobre el contenido binario para evitar decodificación UTF-8 costosa
    content = response.content
    for marker, description in markers:
        assert marker.encode('utf-8') in content, f"Componente UI faltante en {path}: {description} ({marker})"

def test_ui_smoke_error_handling(client) -> None:
    """Verifica que el servidor maneje correctamente las peticiones a rutas inexistentes."""
    response = client.get("/invalid/route/test")
    assert response.status_code == 404, "El servidor debería retornar 404 para rutas no definidas"

def test_ui_smoke_analytics_studio_modal_components(auth_client) -> None:
    """Verifica que el modal visual exponga los selectores correctos y aísle el SQL."""
    response = auth_client.get("/analytics")
    assert response.status_code == 200
    html = response.text
    
    # Validar presencia de selectores visuales del AST
    assert 'id="qbBaseTable"' in html
    assert 'id="qbMetricColumn"' in html
    
    # Aislamiento de Seguridad: Asegurar que NO existe el textarea de SQL crudo
    # Esto fallará hasta que se ejecute la Fase 1 del Plan Maestro
    assert '<textarea id="editQueryText"' not in html
