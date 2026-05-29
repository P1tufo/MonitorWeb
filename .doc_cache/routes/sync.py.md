## Archivo: ./routes/sync.py

### Resumen Funcional
Este archivo contiene rutas para la sincronización de datos con gestión de concurrencia. Utiliza `TaskManager` para ejecutar tareas en segundo plano y proporciona endpoints para iniciar, monitorear y obtener el estado de las sincronizaciones.

### Catálogo de Funciones y Clases
- `get_tunnel_url(state: AppState = Depends(get_app_state))` - Retorna la URL pública del túnel (Ngrok).
- `get_sync_status(state: AppState = Depends(get_app_state))` - Retorna el estado actual de la sincronización.
- `sync_data(state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Inicia el proceso de sincronización de datos y lo encola en `TaskManager`.
- `list_tasks(limit: int = 20, state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Lista las tareas recientes del sistema.
- `get_task(task_id: str, state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Consulta el estado de una tarea específica por su ID.
- `_run_sync_pipeline()` - Ejecuta el pipeline completo de limpieza y consolidación.

### Interacción con Base de Datos
- Motor: No aplica (No hay consultas SQL crudas o llamadas a ORM).
- Tablas: `analytics_snapshots` (se intenta eliminar en la sincronización finalizada).

### Estado y Variables Globales
- `state.is_syncing`: Indica si una sincronización está en curso.
- `state.sync_lock`: Bloqueo para evitar ejecuciones duplicadas de la sincronización.

### Dependencias y Flujo
- Librerías externas: `logging`, `shutil`, `pathlib`, `typing`.
- Comunicación con otros archivos:
  - `core.auth.require_auth` (para autenticación).
  - `config.DB_PATH`, etc. (para configuraciones globales).
  - `core.state.AppState` y `get_app_state()` (para el estado de la aplicación).
  - `core.task_manager.task_manager` (para gestionar tareas en segundo plano).
  - `db.consolidator.DataConsolidator` (para consolidación de datos).
  - `core.database.get_session` (para obtener sesiones de base de datos).
  - `core.wms_utils.is_file_changed`, `mark_file_processed` (para manejo de archivos).
  - `services.etl.OutboundDeliveryAdapter`, etc. (para procesamiento de datos ETL).
  - `routes.transporte.sync_transporte_logic` (para sincronización de transporte).

