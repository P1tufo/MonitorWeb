import sqlite3

from fastapi import Depends


# Importar dependencias directas para FastAPI
def get_db():
    from core.database import get_session
    with get_session() as session:
        yield session

from .base import BaseRepository
from .deliveries import DeliveriesRepository
from .inventory import InventoryRepository
from .productivity import ProductivityRepository
from .tasks import TasksRepository


from sqlalchemy.orm import Session

def get_deliveries_repo(session: Session = Depends(get_db)) -> DeliveriesRepository:
    return DeliveriesRepository(session)

def get_inventory_repo(session: Session = Depends(get_db)) -> InventoryRepository:
    return InventoryRepository(session)

def get_tasks_repo(session: Session = Depends(get_db)) -> TasksRepository:
    return TasksRepository(session)

def get_productivity_repo(session: Session = Depends(get_db)) -> ProductivityRepository:
    return ProductivityRepository(session)

__all__ = [
    "BaseRepository",
    "DeliveriesRepository",
    "InventoryRepository",
    "TasksRepository",
    "ProductivityRepository",
    "get_db",
    "get_deliveries_repo",
    "get_inventory_repo",
    "get_tasks_repo",
    "get_productivity_repo"
]
