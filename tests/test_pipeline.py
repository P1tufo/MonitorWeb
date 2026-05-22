import pytest
from pathlib import Path
from datetime import datetime
import pandas as pd
from db.consolidator import DataConsolidator, TABLE_DELIVERIES, TABLE_STOCK

@pytest.fixture
def consolidator(test_db):
    """Fixture que devuelve un DataConsolidator usando la DB en memoria."""
    # Nota: DataConsolidator necesita un path de archivo, 
    # pero aquí podemos pasarle el objeto connection inyectado o mockear connect
    dc = DataConsolidator(":memory:")
    dc.conn = test_db # Usar la conexión compartida de conftest
    return dc

def test_parse_file_date(consolidator):
    """Verifica que el parsing de fechas sea correcto."""
    path1 = Path("01-05-2024_Entregas.xlsx")
    path2 = Path("15.12.2023_data.xlsx")
    path3 = Path("no_date_file.xlsx")
    
    assert consolidator._parse_file_date(path1) == datetime(2024, 5, 1)
    assert consolidator._parse_file_date(path2) == datetime(2023, 12, 15)
    assert consolidator._parse_file_date(path3) == datetime.min

def test_validate_table_security(consolidator):
    """Verifica la protección contra nombres de tabla no permitidos."""
    consolidator._validate_table(TABLE_DELIVERIES) # No debe fallar
    consolidator._validate_table("inventory_movements") # No debe fallar
    
    with pytest.raises(ValueError):
        consolidator._validate_table("users_passwords")
    with pytest.raises(ValueError):
        consolidator._validate_table("outbound_deliveries; DROP TABLE users;")

def test_overwrite_with_latest_logic(consolidator, tmp_path):
    """Verifica que se tome el archivo más reciente para sobrescribir."""
    # Crear archivos falsos con diferentes fechas
    d1 = tmp_path / "01-01-2023_stock.xlsx"
    d2 = tmp_path / "01-05-2024_stock.xlsx" # El más reciente
    d3 = tmp_path / "15-02-2024_stock.xlsx"
    
    # Crear contenido mínimo para el Excel
    df = pd.DataFrame({"Material": ["A1"], "Stock": [10]})
    df.to_excel(d1, index=False)
    df.to_excel(d2, index=False)
    df.to_excel(d3, index=False)
    
    # Ejecutar lógica de sobrescritura
    # Mockeamos process_file para que devuelva el DF directamente y no cree archivos físicos temp
    from unittest.mock import patch
    with patch("services.etl.OutboundDeliveryAdapter.read_and_clean_data", return_value=df):
        consolidator.overwrite_with_latest(str(tmp_path), TABLE_STOCK)
        
    # Verificar que la tabla existe en la DB
    cursor = consolidator.conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_STOCK}")
    count = cursor.fetchone()[0]
    assert count == 1
    
    # Verificar que el source_file guardado sea el de 2024 (d2)
    cursor.execute(f"SELECT source_file FROM {TABLE_STOCK}")
    source = cursor.fetchone()[0]
    assert source == "01-05-2024_stock.xlsx"
