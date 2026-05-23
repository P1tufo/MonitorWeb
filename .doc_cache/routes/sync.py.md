## Archivo: ./routes/sync.py

### Resumen Funcional
El archivo `sync.py` contiene rutas para la gestión de sincronización de datos en una aplicación web. Permite iniciar y monitorear procesos de sincronización asíncrona utilizando un `TaskManager`, y proporciona endpoints para obtener la URL del túnel, el estado de la sincronización actual y detalles sobre las tareas en ejecución.

### Catálogo de Funciones y Clases
- `get_tunnel_url(state: AppState = Depends(get_app_state))` - Retorna la URL pública del túnel (Ngrok).
- `get_sync_status(state: AppState = Depends(get_app_state))` - Retorna el estado actual de la sincronización.
- `sync_data(state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Inicia el proceso de sincronización de datos y lo encola en el `TaskManager`.
- `list_tasks(limit: int = 20, state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Lista las tareas recientes del sistema.
- `get_task(task_id: str, state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Consulta el estado de una tarea específica por su ID.
- `_run_sync_pipeline()` - Ejecuta el pipeline completo de limpieza y consolidación.

### Interacción con Base de Datos
El archivo interactúa con la base de datos a través del módulo `db.consolidator.DataConsolidator`. Se realizan operaciones en las tablas `stock_levels` y otras dependiendo de los archivos procesados. No se especifica el motor de base de datos.

### Estado y Variables Globales
- `state.is_syncing`: Indica si la sincronización está en curso.
- `state.sync_lock`: Un bloqueo para evitar ejecuciones duplicadas de la sincronización.

### Dependencias y Flujo
- **Librerías Externas**: `fastapi`, `logging`, `shutil`, `pathlib`, `typing`.
- **Flujo Interno**: El archivo se comunica con otros módulos como `core.auth`, `config`, `core.state`, `core.task_manager`, `db.consolidator`, `core.database`, `core.wms_utils`, y `services.etl`.

