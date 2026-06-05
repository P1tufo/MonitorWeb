## Archivo: ./routes/sync.py

### Resumen Funcional
Este archivo contiene rutas para la sincronización de datos en un sistema de monitoreo de almacén (WMS). Permite iniciar y gestionar procesos de sincronización en segundo plano utilizando `TaskManager`, y proporciona endpoints para consultar el estado de las tareas.

### Catálogo de Funciones y Clases
- `get_tunnel_url(state: AppState = Depends(get_app_state))` - Retorna la URL pública del túnel (Ngrok).
- `get_sync_status(state: AppState = Depends(get_app_state))` - Retorna el estado actual de la sincronización.
- `sync_data(state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Inicia el proceso de sincronización de datos y lo encola en `TaskManager`.
- `list_tasks(limit: int = 20, state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Lista las tareas recientes del sistema.
- `get_task(task_id: str, state: AppState = Depends(get_app_state), admin=Depends(require_auth))` - Consulta el estado de una tarea específica por su ID.
- `_run_sync_pipeline()` - Ejecuta el pipeline completo de limpieza y consolidación.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - `analytics_snapshots`
  - Tablas específicas dependen del contenido de los directorios (`deliveries_path`, `stock_path`, `tasks_path`, `inventory_path`, `lx02_pendientes_path`) que se procesan en `_run_sync_pipeline`.
- **Consultas SQL Crudas:** No hay consultas SQL crudas directamente en este archivo. Se utilizan métodos de ORM.

### Estado y Variables Globales
- **Variables Globales:**
  - `DB_PATH`
  - `CLEANSED_DIR`
  - `PDF_STORAGE`
  - `DELIVERIES_DIR`
  - `STOCK_DIR`
  - `TASKS_DIR`
  - `INVENTORY_DIR`
  - `TUNNEL_URL_FILE`

### Dependencias y Flujo
- **Librerías Externas:**
  - `logging`
  - `shutil`
  - `pathlib`
  - `typing`
  - `fastapi`
  - `core.auth`
  - `config`
  - `core.state`
  - `core.task_manager`
  - `db.consolidator`

- **Archivos del Proyecto que Importan a este Archivo:**
  - `routes/transporte.py` (importado dentro de `_run_sync_pipeline`)

- **Archivos del Proyecto que Este Archivo Importa:**
  - No hay imports directos desde otros archivos en este fragmento.

- **Dirección del Flujo de Datos:**
  - Los datos fluyen a través de los endpoints para iniciar y gestionar la sincronización, luego se procesan en `_run_sync_pipeline` que interactúa con las tablas de la base de datos y realiza operaciones de ETL.

