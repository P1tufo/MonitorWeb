## Archivo: ./core/models_transaccional.py

### Resumen Funcional
Este archivo define clases que representan tablas en una base de datos relacional utilizando SQLAlchemy ORM. Cada clase corresponde a una tabla y contiene atributos que corresponden a las columnas de la tabla.

### Catálogo de Funciones y Clases
- `WarehouseTask` - Representa la tabla `warehouse_tasks`.
- `InventoryMovement` - Representa la tabla `inventory_movements`.
- `OutboundDelivery` - Representa la tabla `outbound_deliveries`.
- `StockLevel` - Representa la tabla `stock_levels`.
- `Lx02Pendiente` - Representa la tabla `lx02_pendientes`.
- `SyncManifest` - Representa la tabla `sync_manifest`.
- `AnalyticsSnapshot` - Representa la tabla `analytics_snapshots`.
- `AutorAreaMapping` - Representa la tabla `autor_area_mapping`.

### Interacción con Base de Datos
El archivo interactúa con una base de datos relacional utilizando SQLAlchemy ORM. Las tablas involucradas son:
- `warehouse_tasks`
- `inventory_movements`
- `outbound_deliveries`
- `stock_levels`
- `lx02_pendientes`
- `sync_manifest`
- `analytics_snapshots`
- `autor_area_mapping`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
Depende de la biblioteca SQLAlchemy para el ORM. No comunica con otros archivos del proyecto directamente, solo define clases que representan tablas en la base de datos.

