## Archivo: ./core/models_transaccional.py

### Resumen Funcional
Este archivo define modelos de datos para una base de datos SQLite utilizada en un sistema de monitoreo de almacén (WMS). Los modelos representan diferentes entidades como tareas de almacenamiento, movimientos de inventario, entregas salientes y niveles de stock.

### Catálogo de Funciones y Clases
- `WarehouseTask` - Representa una tarea de almacenamiento con varios campos.
- `InventoryMovement` - Representa un movimiento de inventario con detalles del material, cantidad y ubicación.
- `OutboundDelivery` - Representa una entrega saliente con información sobre el material, la ubicación y los tiempos de carga.
- `StockLevel` - Representa el nivel de stock para diferentes materiales y lotes.
- `Lx02Pendiente` - Representa pendientes en un sistema específico (LX02) con detalles del material y la ubicación.
- `SyncManifest` - Representa un manifiesto de sincronización con información sobre archivos procesados.
- `AnalyticsSnapshot` - Representa una instantánea de análisis con datos y tiempos de actualización.
- `AutorAreaMapping` - Representa el mapeo entre autores y áreas de negocio.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQLite. Las tablas definidas son:
- `warehouse_tasks`
- `inventory_movements`
- `outbound_deliveries`
- `stock_levels`
- `lx02_pendientes`
- `sync_manifest`
- `analytics_snapshots`
- `autor_area_mapping`

### Estado y Variables Globales
No hay variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
Dependencias:
- `sqlalchemy` - Para ORM y definición de modelos.
- `core.database.Base` - Clase base para todos los modelos.

Flujo:
- Este archivo es importado por otros archivos que necesitan interactuar con la base de datos, como servicios o repositorios.

