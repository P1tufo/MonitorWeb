## Archivo: ./core/models_transaccional.py

### Resumen Funcional
Este archivo define modelos SQLAlchemy para representar tablas en una base de datos SQLite utilizada por el sistema de monitoreo de almacén (WMS). Cada clase corresponde a una tabla y contiene atributos que corresponden a las columnas de la tabla.

### Catálogo de Funciones y Clases
- `WarehouseTask` - Representa tareas en el almacén.
- `InventoryMovement` - Representa movimientos de inventario.
- `OutboundDelivery` - Representa entregas salientes.
- `StockLevel` - Representa niveles de stock.
- `Lx02Pendiente` - Representa pendientes de LX02.
- `SyncManifest` - Representa manifiestos de sincronización.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `warehouse_tasks`
  - `inventory_movements`
  - `outbound_deliveries`
  - `stock_levels`
  - `lx02_pendientes`
  - `sync_manifest`
- Columnas:
  - `warehouse_tasks`: `numero_ot`, `pos`, `material`, etc.
  - `inventory_movements`: `doc_mat`, `ej_mat`, `pos`, etc.
  - `outbound_deliveries`: `entrega`, `pos_`, `material`, etc.
  - `stock_levels`: `material`, `lote`, `alm_`, etc.
  - `lx02_pendientes`: `material`, `lote`, `alm_`, etc., `otcuanto`.
  - `sync_manifest`: `file_path`, `last_modified`, `file_size`, etc.

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Dependencias**: SQLAlchemy, FastAPI.
- **Flujo de Datos**:
  - Archivos del proyecto que importan a este archivo: Ninguno.
  - Archivos del proyecto que este archivo importa: Ninguno.

