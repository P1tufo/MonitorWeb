from .deliveries import OutboundDeliveryAdapter
from .movements import InventoryMovementAdapter
from .tasks import WarehouseTaskAdapter
from .stock import StockLevelAdapter

__all__ = [
    "OutboundDeliveryAdapter",
    "InventoryMovementAdapter",
    "WarehouseTaskAdapter",
    "StockLevelAdapter"
]

def process_inventory_folder(folder_path: str, db_path: str, table_name: str = "inventory_movements", conn=None) -> int:
    adapter = InventoryMovementAdapter()
    return adapter.process_directory(folder_path, db_path, table_name, conn)

def process_inventory_file(file_path: str, db_path: str, table_name: str = "inventory_movements", conn=None) -> int:
    adapter = InventoryMovementAdapter()
    return adapter.process_and_save(file_path, db_path, table_name, conn)

def process_tasks_file(file_path: str, db_path: str, table_name: str = "warehouse_tasks", conn=None) -> int:
    adapter = WarehouseTaskAdapter()
    return adapter.process_and_save(file_path, db_path, table_name, conn)

def process_lx02_pendientes(folder_path: str, db_path: str, table_name: str = "lx02_pendientes", conn=None) -> int:
    adapter = StockLevelAdapter()
    return adapter.process_directory(folder_path, db_path, table_name, conn)

def process_deliveries_file(file_path: str, db_path: str, table_name: str = "outbound_deliveries", conn=None) -> int:
    adapter = OutboundDeliveryAdapter()
    return adapter.process_and_save(file_path, db_path, table_name, conn)
