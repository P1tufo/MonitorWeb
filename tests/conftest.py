import os
import secrets
from pathlib import Path

# TEST_SESSION_ID: Identificador criptográficamente seguro para evitar colisiones.
TEST_SESSION_ID = secrets.token_hex(16)
# MEMORY_DB_URI: Almacenado en Temp_Assets para no ensuciar la raíz.
# Forzamos DATABASE_URL ANTES de cualquier importación de la app para que SQLAlchemy lo use
db_file_dir = Path(__file__).resolve().parent.parent / "Temp_Assets"
db_file_dir.mkdir(parents=True, exist_ok=True)
db_file_path = db_file_dir / f"memdb_session_{TEST_SESSION_ID}"
MEMORY_DB_URI = f"file:{db_file_path}?mode=memory&cache=shared"
os.environ["DATABASE_URL"] = f"sqlite:///{MEMORY_DB_URI}&uri=true"

import sqlite3
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

import config
from app import app

# Configuración de la base de datos de pruebas volátil
# ---------------------------------------------------

@pytest.fixture(autouse=True)
def skip_warmup():
    """
    Nota: El warm_up ahora ocurre dentro del lifespan. 
    Si se desea desactivar, se podría usar una variable de entorno.
    Por ahora, simplemente eliminamos el patch que fallaba.
    """
    yield


@pytest.fixture(scope="session")
def session_db():
    """
    Crea e inicializa la base de datos maestra compartida para toda la sesión de pruebas.
    
    Funcionalidad:
    - Crea una base de datos SQLite en memoria con 'cache=shared'.
    - Inicializa el esquema completo (tablas de transacciones, maestros y snapshots).
    - Mantiene una conexión persistente para evitar que SQLite libere la memoria.
    
    Retorna:
    - sqlite3.Connection: Conexión maestra a la base de datos inicializada.
    """
    # Conexión maestra: actua como guardián de la base de datos en memoria compartida
    # Se utiliza uri=True para permitir el uso de parámetros como 'cache=shared'
    conn = sqlite3.connect(MEMORY_DB_URI, uri=True, check_same_thread=False)
    
    # Aplicar el esquema base de forma atómica
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS outbound_deliveries (
            entrega INTEGER, pos_ INTEGER, material TEXT, denominacion TEXT,
            cantidad TEXT, umb TEXT, fecha_carga TEXT, fecha_sm_real TEXT,
            creado_el TEXT, autor TEXT, centro_costo TEXT, centro TEXT,
            area_negocio TEXT, ubicacion_bin TEXT, ubicacion_area TEXT,
            estado_wms TEXT, dias_retraso INTEGER, week_sort TEXT, week_label TEXT,
            referencia TEXT, ops TEXT, mm TEXT, c TEXT, source_file TEXT,
            ingested_at TEXT, fecha_sm_real_1 TEXT, ubicacion_bin_1 TEXT
        );
        CREATE TABLE IF NOT EXISTS inventory_movements (
            fe_contab TEXT, alm TEXT, ce TEXT, cmv TEXT, referencia TEXT, 
            texto_cab_documento TEXT, texto_breve_material TEXT, material TEXT, 
            cantidad REAL, umb TEXT, doc_mat TEXT, ej_mat TEXT, pos TEXT, 
            registrado TEXT, hora TEXT, usuario TEXT, pedido TEXT, pos_extra TEXT, 
            ce_coste TEXT, importe_ml REAL, mon TEXT, proveedor TEXT, 
            tipo_operacion TEXT, PRIMARY KEY (doc_mat, ej_mat, pos)
        );
        CREATE TABLE IF NOT EXISTS stock_levels (
            material TEXT, denominacion TEXT, ubicacion_bin TEXT, 
            stock_disp TEXT, umb TEXT, week_sort TEXT, week_label TEXT,
            source_file TEXT, ingested_at TEXT
        );
        CREATE TABLE IF NOT EXISTS warehouse_tasks (
            numero_ot TEXT, pos TEXT, material TEXT, texto_breve_material TEXT,
            tp_proc TEXT, ubic_proc TEXT, ctd_teor_dsd REAL, uma TEXT,
            tp_dest TEXT, ubic_dest TEXT, fe_creac TEXT, hora TEXT,
            usuario TEXT, lote TEXT, cl_mov TEXT, clase_mov TEXT,
            doc_mat TEXT, usuario_conf TEXT, fecha_conf TEXT, hor_conf TEXT,
            ce TEXT, entrega TEXT, PRIMARY KEY (numero_ot, pos)
        );
        CREATE TABLE IF NOT EXISTS autor_area_mapping (
            autor TEXT PRIMARY KEY, area_negocio TEXT, frequency INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS analytics_snapshots (
            key TEXT PRIMARY KEY, data TEXT, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS auth_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    
    from core.db_config_manager import init_config_db, seed_initial_config
    from core.auth import init_auth_db
    init_auth_db()
    init_config_db()
    seed_initial_config()
    
    yield conn
    conn.close()

@pytest.fixture(scope="function")
def test_db(session_db):
    """
    Proporciona aislamiento de datos entre pruebas individuales.
    
    Lógica:
    - Antes de cada test, vacía (DELETE) todas las tablas de la base de datos de sesión.
    - Esto garantiza que cada prueba comience con una BD vacía pero con el esquema ya cargado.
    """
    # Lista de tablas a limpiar para evitar contaminación cruzada (Cross-test contamination)
    tables = [
        "outbound_deliveries", "inventory_movements", "stock_levels", 
        "warehouse_tasks", "autor_area_mapping", "analytics_snapshots",
        "auth_users"
    ]
    for table in tables:
        if table == "auth_users":
            session_db.execute(f"DELETE FROM {table} WHERE username != 'admin'")
        else:
            session_db.execute(f"DELETE FROM {table}")
    session_db.commit()
    
    return session_db

@pytest.fixture
def client(test_db):
    """
    Cliente de pruebas de FastAPI configurado para interactuar con la BD de sesión.
    
    Implementación:
    - Parchea dinámicamente 'sqlite3.connect' en toda la aplicación.
    - Redirige cualquier intento de conexión a la URI de la base de datos de pruebas.
    """
    original_connect = sqlite3.connect
    
    def mocked_connect(path, *args, **kwargs):
        # Interceptamos conexiones a la BD configurada en config.py o a BDs temporales
        if path == config.DB_PATH or path == ":memory:":
            return original_connect(MEMORY_DB_URI, *args, **kwargs, uri=True)
        return original_connect(path, *args, **kwargs)

    with patch("sqlite3.connect", side_effect=mocked_connect):
        with TestClient(app) as c:
            yield c


@pytest.fixture
def auth_client(client):
    """Proporciona un cliente con token de administrador pre-autenticado."""
    # Aseguramos que el admin existe (por si acaso la limpieza falló o el lifespan no corrió)
    from core.auth import ensure_admin_exists
    ensure_admin_exists()
    
    response = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "admin"},
    )
    if response.status_code != 200:
        pytest.fail(f"Fallo login admin en test: {response.text}")
        
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
