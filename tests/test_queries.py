import pytest
import sqlite3
import pandas as pd
from repositories.deliveries import DeliveriesRepository

# Constantes de prueba para evitar magic strings y facilitar el mantenimiento
TEST_YEAR = "%2026"  # Las queries usan LIKE ?, así que el wildcard es necesario
AREA_A = "ASERRADERO"
AREA_B = "MOLDURAS"

# Fechas en formato WMS procesado (DD-MM-YYYY) para compatibilidad con la lógica LIKE
DATE_1 = "01-05-2026"
DATE_2 = "02-05-2026"

class MockConnectionWrapper:
    def __init__(self, conn):
        self.connection = conn

class MockSession:
    def __init__(self, conn):
        self._conn = conn
    def connection(self):
        return MockConnectionWrapper(self._conn)
    def execute(self, stmt):
        class Result:
            def all(self):
                cur = self._conn.execute(str(stmt))
                return cur.fetchall()
        r = Result()
        r._conn = self._conn
        return r


def test_get_total_active_days(test_db: sqlite3.Connection) -> None:
    """Verifica el conteo de días únicos con actividad filtrado por año usando fechas ISO."""
    data = [
        ('1001', DATE_1, 'A', 1),
        ('1002', DATE_1, 'B', 0),
        ('1003', DATE_2, 'A', 5)
    ]
    with test_db:
        test_db.executemany(
            "INSERT INTO outbound_deliveries (entrega, fecha_carga, area_negocio, dias_retraso) VALUES (?,?,?,?)", 
            data
        )

    repo = DeliveriesRepository(MockSession(test_db))
    result = repo.get_total_active_days(TEST_YEAR)
    assert result == 2, f"Se esperaban 2 días activos para {TEST_YEAR}, se obtuvo {result}"

def test_get_total_active_days_empty(test_db: sqlite3.Connection) -> None:
    repo = DeliveriesRepository(MockSession(test_db))
    result = repo.get_total_active_days(TEST_YEAR)
    assert result == 0, "Debería retornar 0 si no hay registros"

def test_get_area_stats(test_db: sqlite3.Connection) -> None:
    """
    Verifica el cálculo de KPIs (ontime/late) agrupados por área de negocio (ahora a través del motor AST).
    """
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

    repo = DeliveriesRepository(MockSession(test_db))
    df = repo.get_area_stats(TEST_YEAR)

    # Validar resultados para Area A
    df_a = df[df['area'] == AREA_A]
    assert not df_a.empty, f"No se encontraron resultados para el área {AREA_A}"
    stats_a = df_a.squeeze()
    assert stats_a['total_entregas'] == 2
    assert stats_a['ontime'] == 1
    assert stats_a['late'] == 1

    # Validar resultados para Area B
    df_b = df[df['area'] == AREA_B]
    assert not df_b.empty, f"No se encontraron resultados para el área {AREA_B}"
    stats_b = df_b.squeeze()
    assert stats_b['total_entregas'] == 1
    assert stats_b['ontime'] == 1
    assert stats_b['late'] == 0

def test_area_expr_fallback_locations(test_db: sqlite3.Connection) -> None:
    data = [
        ('8001', DATE_1, None, None, 'MOLTR1-104', 'Q1C02A', 1), # -> MOLDURAS
        ('8002', DATE_1, None, None, None, 'PATRU2-201', 1), # -> LINEA 2
        ('8003', DATE_1, None, 'ASERRADERO', None, None, 1), # -> ASERRADERO
        ('8004', DATE_1, None, None, None, None, 1), # -> S/N
    ]
    with test_db:
        test_db.executemany(
            "INSERT INTO outbound_deliveries (entrega, fecha_carga, area_negocio, ubicacion_area, ubicacion_bin_1, ubicacion_bin, dias_retraso) VALUES (?,?,?,?,?,?,?)", 
            data
        )

    repo = DeliveriesRepository(MockSession(test_db))
    df = repo.get_area_stats(TEST_YEAR)
    
    assert df[df['area'] == 'MOLDURAS'].squeeze()['total_entregas'] == 1
    assert df[df['area'] == 'LINEA 2'].squeeze()['total_entregas'] == 1
    assert df[df['area'] == 'ASERRADERO'].squeeze()['total_entregas'] == 1
    assert df[df['area'] == 'S/N'].squeeze()['total_entregas'] == 1

def test_query_engine_compiles_ast_correctly(test_db: sqlite3.Connection) -> None:
    from core.query_engine import build_sql_from_payload
    from core.schemas import VisualQueryBuilderPayload, MetricDef, TimeAxisDef, FilterDef
    
    payload = VisualQueryBuilderPayload(
        baseTable="outbound_deliveries",
        metric=MetricDef(column="outbound_deliveries.entrega", aggregation="COUNT"),
        timeAxis=TimeAxisDef(column="outbound_deliveries.fecha_carga", granularity="MONTH"),
        filters=[FilterDef(column="outbound_deliveries.dias_retraso", operator="lessthan", value="3")],
        metrics=[]
    )

    sql, params = build_sql_from_payload(payload, MockSession(test_db))
    
    sql_upper = sql.upper()
    assert "SELECT" in sql_upper
    assert "COUNT(" in sql_upper
    assert "WHERE" in sql_upper
    assert "<" in sql_upper and "?" in sql_upper

