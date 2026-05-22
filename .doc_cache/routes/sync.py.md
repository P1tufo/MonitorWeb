## Archivo: ./routes/sync.py

### Resumen Funcional
Este archivo contiene rutas para la sincronización de datos con gestión de concurrencia. Utiliza `TaskManager` para ejecutar tareas en segundo plano y proporciona endpoints para iniciar, monitorear y obtener el estado de las sincronizaciones.

### Catálogo de Funciones y Clases
- `get_tunnel_url(state: AppState = Depends(get_app_state))` - Retorna la URL pública del túnel (Ngrok).
- `get_sync_status(state: AppState = Depends(get_app_state))` - Retorna el estado actual de la sincronización.
- `sync_data(state: AppState = Depends(get_app_state))` - Inicia el proceso de sincronización de datos y lo encola en `TaskManager`.
- `list_tasks(limit: int = 20, state: AppState = Depends(get_app_state))` - Lista las tareas recientes del sistema.
- `get_task(task_id: str, state: AppState = Depends(get_app_state))` - Consulta el estado de una tarea específica por su ID.
- `_run_sync_pipeline()` - Ejecuta el pipeline completo de limpieza y consolidación.

### Interacción con Base de Datos
- Motor: No aplica (No hay consultas SQL crudas o llamadas a ORM explícitas).
- Tablas: `analytics_snapshots` (se borra en `_run_sync_pipeline()`).

### Estado y Variables Globales
- `state.is_syncing`: Indica si la sincronización está en curso.
- `state.sync_lock`: Bloqueo para evitar ejecuciones duplicadas de la sincronización.

### Dependencias y Flujo
- Librerías externas: `fastapi`, `logging`, `shutil`, `pathlib`, `typing`.
- Comunicación con otros archivos:
  - `core.auth.require_auth` (autenticación).
  - `config` (variables de configuración).
  - `core.state.AppState` y `get_app_state()` (estado global).
  - `core.task_manager.task_manager` (gestión de tareas).
  - `db.consolidator.DataConsolidator` (consolidación de datos).
  - `core.database.get_session` (obtención de sesión de base de datos).
  - `core.wms_utils.is_file_changed` y `mark_file_processed` (utilidades para archivos).
  - `services.etl.OutboundDeliveryAdapter` (adaptador ETL).
  - `db.inventory_processor.process_inventory_file` (procesamiento de inventario).
  - `db.warehouse_tasks_processor.process_tasks_file` (procesamiento de tareas de bodega).
  - `db.lx02_processor.process_lx02_pendientes` (procesamiento de documentos no paletizados).

