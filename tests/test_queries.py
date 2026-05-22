import pytest
import sqlite3
import pandas as pd
from core.queries_deliveries import get_total_active_days, get_area_stats

# Constantes de prueba para evitar magic strings y facilitar el mantenimiento
TEST_YEAR = "%2026"  # Las queries usan LIKE ?, así que el wildcard es necesario
AREA_A = "ASERRADERO"
AREA_B = "MOLDURAS"

# Fechas en formato WMS procesado (DD-MM-YYYY) para compatibilidad con la lógica LIKE
DATE_1 = "01-05-2026"
DATE_2 = "02-05-2026"

def test_get_total_active_days(test_db: sqlite3.Connection) -> None:
    """Verifica el conteo de días únicos con actividad filtrado por año usando fechas ISO."""
    # 1. Insertar datos de prueba (3 registros en 2 días distintos)
    data = [
        ('1001', DATE_1, 'A', 1),
        ('1002', DATE_1, 'B', 0),
        ('1003', DATE_2, 'A', 5)
    ]
    # Se usa el context manager de la conexión para asegurar el commit/rollback automático
    with test_db:
        test_db.executemany(
            "INSERT INTO outbound_deliveries (entrega, fecha_carga, area_negocio, dias_retraso) VALUES (?,?,?,?)", 
            data
        )

    # 2. Ejecutar consulta para el año configurado
    result = get_total_active_days(test_db, TEST_YEAR)

    # 3. Validar: Deberían ser 2 días únicos (DATE_1 y DATE_2)
    assert result == 2, f"Se esperaban 2 días activos para {TEST_YEAR}, se obtuvo {result}"

def test_get_total_active_days_empty(test_db: sqlite3.Connection) -> None:
    """Verifica que el conteo de días activos devuelva 0 cuando la tabla está vacía."""
    # La tabla ya existe por conftest.py, pero está vacía al inicio de cada función de test
    result = get_total_active_days(test_db, TEST_YEAR)
    assert result == 0, "Debería retornar 0 si no hay registros en el año consultado"

def test_get_area_stats(test_db: sqlite3.Connection) -> None:
    """
    Verifica el cálculo de KPIs (ontime/late) agrupados por área de negocio.
    Utiliza validaciones robustas sobre el DataFrame para evitar fallos por ordenamiento.
    """
    # Preparación de datos:
    # Area A: 1 a tiempo (retraso 1 <= 2), 1 tarde (retraso 5 > 2)
    # Area B: 1 a tiempo (retraso 0 <= 2)
    data = [
        ('1001', DATE_1, AREA_A, 1), # ontime
        ('1002', DATE_1, AREA_A, 5), # late
        ('1003', DATE_1, AREA_B, 0), # ontime
    ]
    with test_db:
        test_db.executemany(
            "INSERT INTO outbound_deliveries (entrega, fecha_carga, area_negocio, dias_retraso) VALUES (?,?,?,?)", 
            data
        )

    # Ejecutar la consulta de estadísticas por área
    df = get_area_stats(test_db, TEST_YEAR)

    # 1. Validar resultados para Area A sin depender del índice iloc
    df_a = df[df['area'] == AREA_A]
    assert not df_a.empty, f"No se encontraron resultados para el área {AREA_A}"
    stats_a = df_a.squeeze() # Convierte el DataFrame de una sola fila en una Serie
    assert stats_a['total_entregas'] == 2
    assert stats_a['ontime'] == 1
    assert stats_a['late'] == 1

    # 2. Validar resultados para Area B
    df_b = df[df['area'] == AREA_B]
    assert not df_b.empty, f"No se encontraron resultados para el área {AREA_B}"
    stats_b = df_b.squeeze()
    assert stats_b['total_entregas'] == 1
    assert stats_b['ontime'] == 1
    assert stats_b['late'] == 0

def test_area_expr_fallback_locations(test_db: sqlite3.Connection) -> None:
    """Verifica que el mapeo de área resuelva correctamente usando las columnas de fallback."""
    # MOLTR1 -> MOLDURAS (por cost center mapping)
    # PATRU2 -> LINEA 2 (por cost center mapping)
    data = [
        # entrega, fecha_carga, area_negocio, ubicacion_area, ubicacion_bin_1, ubicacion_bin, dias_retraso
        ('8001', DATE_1, None, None, 'MOLTR1-104', 'Q1C02A', 1), # MOLTR1-104 en ubicacion_bin_1 -> MOLDURAS
        ('8002', DATE_1, None, None, None, 'PATRU2-201', 1), # PATRU2-201 en ubicacion_bin -> LINEA 2
        ('8003', DATE_1, None, 'ASERRADERO', None, None, 1), # ASERRADERO en ubicacion_area -> ASERRADERO
        ('8004', DATE_1, None, None, None, None, 1), # Todo NULL -> S/N
    ]
    with test_db:
        test_db.executemany(
            "INSERT INTO outbound_deliveries (entrega, fecha_carga, area_negocio, ubicacion_area, ubicacion_bin_1, ubicacion_bin, dias_retraso) VALUES (?,?,?,?,?,?,?)", 
            data
        )

    df = get_area_stats(test_db, TEST_YEAR)
    
    # Validar MOLDURAS
    molduras = df[df['area'] == 'MOLDURAS']
    assert not molduras.empty
    assert molduras.squeeze()['total_entregas'] == 1

    # Validar LINEA 2
    linea2 = df[df['area'] == 'LINEA 2']
    assert not linea2.empty
    assert linea2.squeeze()['total_entregas'] == 1

    # Validar ASERRADERO
    aserradero = df[df['area'] == 'ASERRADERO']
    assert not aserradero.empty
    assert aserradero.squeeze()['total_entregas'] == 1

    # Validar S/N
    sn = df[df['area'] == 'S/N']
    assert not sn.empty
    assert sn.squeeze()['total_entregas'] == 1

