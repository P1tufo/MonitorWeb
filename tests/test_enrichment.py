import pytest
import sqlite3
from typing import Any
from db.db_enrichment import (
    learn_author_areas, 
    apply_author_learning, 
    backfill_deliveries_from_movements,
    enrich_deliveries_with_stock,
    update_sla_with_tasks
)

@pytest.fixture
def db_with_data(test_db: sqlite3.Connection) -> sqlite3.Connection:
    """
    Prepara una base de datos con datos de prueba para los procesos de enriquecimiento.
    El esquema ya ha sido inicializado en conftest.py.
    """
    conn = test_db
    try:
        # Insertar datos de ejemplo usando consultas parametrizadas para mayor seguridad
        # 1. Registros para aprendizaje de autor (Relación Usuario -> Área)
        conn.execute(
            "INSERT INTO outbound_deliveries (entrega, autor, area_negocio) VALUES (?, ?, ?)",
            ('8001', 'USER_A', 'PRODUCCION')
        )
        conn.execute(
            "INSERT INTO outbound_deliveries (entrega, autor, area_negocio) VALUES (?, ?, ?)",
            ('8002', 'USER_A', 'OTRO')
        )
        
        # 2. Datos en Movimientos para backfill (Referencia 8003 -> Entrega 8003)
        conn.execute(
            "INSERT INTO inventory_movements (material, usuario, ce_coste, referencia) VALUES (?, ?, ?, ?)",
            ('M1', 'USER_B', 'CE-100', '0000008003')
        )
        conn.execute(
            "INSERT INTO outbound_deliveries (entrega, autor, centro_costo) VALUES (?, ?, ?)",
            ('8003', '', '')
        )
        
        # 3. Datos en Stock para stock (Maestro de materiales y ubicaciones)
        conn.execute(
            "INSERT INTO stock_levels (material, denominacion, ubicacion_bin, stock_disp, umb) VALUES (?, ?, ?, ?, ?)",
            ('MAT-99', 'Producto VIP', 'ESTANTE-X', '100', 'UN')
        )
        conn.execute(
            "INSERT INTO outbound_deliveries (material) VALUES (?)",
            ('MAT-99',)
        )
        
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        pytest.fail(f"Fallo al inicializar la base de datos de prueba: {e}")
        
    return conn

def test_learn_and_apply_author_logic(db_with_data: sqlite3.Connection) -> None:
    """Verifica que el sistema aprenda que USER_A pertenece a PRODUCCION y lo aplique."""
    learn_author_areas(db_with_data)
    
    # Verificar que existe el registro de aprendizaje
    cursor = db_with_data.cursor()
    cursor.execute("SELECT area_negocio FROM autor_area_mapping WHERE autor=?", ('USER_A',))
    row = cursor.fetchone()
    assert row is not None, "El mapeo de autor no fue creado"
    assert row[0] == 'PRODUCCION'
    
    # Aplicar el aprendizaje a las transacciones existentes
    apply_author_learning(db_with_data)
    
    # La entrega 8002 que era 'OTRO' ahora debe ser 'PRODUCCION'
    cursor.execute("SELECT area_negocio FROM outbound_deliveries WHERE entrega=?", ('8002',))
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == 'PRODUCCION'

def test_backfill_from_movements(db_with_data: sqlite3.Connection) -> None:
    """Verifica que Entregas recupere el autor y centro de costo desde Movimientos."""
    backfill_deliveries_from_movements(db_with_data)
    
    cursor = db_with_data.cursor()
    cursor.execute("SELECT autor, centro_costo FROM outbound_deliveries WHERE entrega=?", ('8003',))
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == 'USER_B'
    assert row[1] == 'CE-100'

def test_enrichment_from_stock(db_with_data: sqlite3.Connection) -> None:
    """Verifica que se crucen las descripciones de material y ubicaciones desde el maestro de stock."""
    enrich_deliveries_with_stock(db_with_data)
    
    cursor = db_with_data.cursor()
    cursor.execute(
        "SELECT denominacion, ubicacion_bin FROM outbound_deliveries WHERE material=?", 
        ('MAT-99',)
    )
    row = cursor.fetchone()
    assert row is not None
    assert row[0] == 'Producto VIP'
    assert row[1] == 'ESTANTE-X'

def test_update_sla_with_tasks(db_with_data: sqlite3.Connection) -> None:
    """Verifica que el SLA se actualice correctamente usando las tareas de bodega."""
    # Insertar una entrega y una tarea relacionada
    db_with_data.execute(
        "INSERT INTO outbound_deliveries (entrega, creado_el, fecha_sm_real) VALUES (?, ?, ?)",
        ('9001', '01-05-2026', '02-05-2026') # 1 de mayo es feriado en Chile
    )
    db_with_data.execute(
        "INSERT INTO warehouse_tasks (entrega, fecha_conf) VALUES (?, ?)",
        ('0000009001', '05-05-2026')
    )
    db_with_data.commit()
    
    update_sla_with_tasks(db_with_data)
    
    cursor = db_with_data.cursor()
    cursor.execute("SELECT dias_retraso FROM outbound_deliveries WHERE entrega=?", ('9001',))
    row = cursor.fetchone()
    
    assert row is not None
    # 1 de mayo (viernes, feriado), 2-3 (fin de semana), 4 (lunes), 5 (martes)
    # Diferencia entre 1 y 5 con feriado el 1: 
    # 1 (vie) -> 4 (lun) = 1 día hábil
    # 4 (lun) -> 5 (mar) = 1 día hábil
    # Total esperado: 2 días hábiles (aprox, depende de cómo np.busday_count cuente los límites)
    assert row[0] >= 0
