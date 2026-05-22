import sqlite3
from fastapi import Depends

# Importar dependencias directas para FastAPI
def get_db():
    from config import DB_PATH
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

from .base import BaseRepository
from .deliveries import DeliveriesRepository
from .inventory import InventoryRepository
from .tasks import TasksRepository

def get_deliveries_repo(conn: sqlite3.Connection = Depends(get_db)) -> DeliveriesRepository:
    return DeliveriesRepository(conn)

def get_inventory_repo(conn: sqlite3.Connection = Depends(get_db)) -> InventoryRepository:
    return InventoryRepository(conn)

def get_tasks_repo(conn: sqlite3.Connection = Depends(get_db)) -> TasksRepository:
    return TasksRepository(conn)

__all__ = [
    "BaseRepository",
    "DeliveriesRepository",
    "InventoryRepository",
    "TasksRepository",
    "get_db",
    "get_deliveries_repo",
    "get_inventory_repo",
    "get_tasks_repo"
]
