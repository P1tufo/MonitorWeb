import pytest
import pandas as pd
import io
import sqlite3
from typing import List
from unittest.mock import MagicMock, patch
from core.pdf_engine import (
    WMS_Landscape_PDF, 
    _generate_barcode_stream, 
    draw_delivery_page,
    get_ots_for_delivery
)

# Constantes de dimensiones estándar para papel Letter (279.4mm x 215.9mm)
LETTER_WIDTH_MIN, LETTER_WIDTH_MAX = 279, 280
LETTER_HEIGHT_MIN, LETTER_HEIGHT_MAX = 215, 216

@pytest.fixture
def pdf_instance() -> WMS_Landscape_PDF:
    """Proporciona una instancia limpia de WMS_Landscape_PDF para cada test, garantizando aislamiento del buffer."""
    return WMS_Landscape_PDF()

@pytest.fixture
def sample_header() -> pd.Series:
    """Genera datos de cabecera de entrega ficticios para pruebas de renderizado de metadatos."""
    return pd.Series({
        "entrega": "80123456",
        "referencia": "REF-001",
        "autor": "TEST_USER",
        "centro_costo": "BOD-01",
        "fe_carga": "10-05-2024"
    })

@pytest.fixture
def sample_items() -> pd.DataFrame:
    """Genera un listado de materiales ficticios para validar el cuerpo dinámico del PDF."""
    return pd.DataFrame([{
        "pos_": "10",
        "ubicacion_fisica_stock": "A-01-B",
        "material": "123456",
        "texto_breve_de_material": "Material de prueba",
        "ctdentrega": 10,
        "umb": "UN"
    }])

def test_pdf_instantiation(pdf_instance: WMS_Landscape_PDF) -> None:
    """
    Verifica que la clase PDF se instancie con la orientación Landscape y dimensiones Letter.
    Crítico para asegurar que los reportes impresos mantengan el formato correcto de WMS.
    """
    assert pdf_instance.def_orientation.value == 'L', "La orientación predeterminada debe ser Landscape (Horizontal)"
    assert LETTER_WIDTH_MIN < pdf_instance.w < LETTER_WIDTH_MAX, f"Ancho incorrecto detectado: {pdf_instance.w}"
    assert LETTER_HEIGHT_MIN < pdf_instance.h < LETTER_HEIGHT_MAX, f"Alto incorrecto detectado: {pdf_instance.h}"

@pytest.mark.parametrize("barcode_data", ["12345678", "80000000", "TEST-BARCODE"])
def test_barcode_generation(barcode_data: str) -> None:
    """
    Valida que la utilidad de códigos de barras produzca un stream binario válido.
    Se prueba con diversos inputs para asegurar la robustez del generador de imágenes interno.
    """
    stream = _generate_barcode_stream(barcode_data)
    assert isinstance(stream, io.BytesIO), "Debe retornar un objeto BytesIO compatible con el motor FPDF"
    assert stream.getbuffer().nbytes > 0, "El stream del código de barras no debe estar vacío"

def test_get_ots_logic() -> None:
    """
    Verifica la lógica de recuperación de OTs filtrando valores inválidos (0 o nulos).
    Asegura que el reporte final solo muestre identificadores de órdenes de transporte reales.
    """
    mock_conn = MagicMock(spec=sqlite3.Connection)
    mock_data = pd.DataFrame({"numero_ot": [1001, 1002, 0, None]})
    
    with patch("pandas.read_sql", return_value=mock_data):
        ots = get_ots_for_delivery("8000123", mock_conn)
        assert "1001" in ots
        assert "1002" in ots
        assert "0" not in ots, "La lógica debe excluir OTs con valor numérico 0"
        assert all(isinstance(ot, str) for ot in ots), "Todos los IDs de OT deben ser convertidos a string"

def test_draw_delivery_page_generates_content(pdf_instance: WMS_Landscape_PDF, 
                                              sample_header: pd.Series, 
                                              sample_items: pd.DataFrame) -> None:
    """
    Valida que el motor de dibujo escriba contenido binario en el buffer del PDF.
    Asegura la orquestación correcta entre cabecera, items de entrega y lista de OTs.
    """
    pdf_instance.add_page()
    
    # Ejecutar el dibujo
    draw_delivery_page(pdf_instance, sample_header, sample_items, ots_list=["1001", "1002"])
    
    # Validar salida
    pdf_output = pdf_instance.output()
    assert len(pdf_output) > 0, "El PDF resultante no contiene datos tras el proceso de dibujo"
