## Archivo: ./routes/sync.py

### Resumen Funcional
Este archivo contiene rutas para la sincronización de datos en un sistema de monitoreo de almacén (WMS). Permite obtener la URL del túnel, el estado de la sincronización y iniciar procesos de sincronización. También proporciona endpoints para listar y consultar el estado de tareas.

### Catálogo de Funciones y Clases
- `get_tunnel_url()` - Retorna la URL pública del túnel (Ngrok).
- `get_sync_status(sync: SyncStateManager = Depends(get_sync_manager))` - Retorna el estado actual de la sincronización.
- `sync_data(sync: SyncStateManager = Depends(get_sync_manager), admin = Depends(require_auth))` - Inicia el proceso de sincronización de datos y lo encola en el TaskManager para ejecución trazable en segundo plano.
- `list_tasks(limit: int = 20, admin = Depends(require_auth))` - Lista las tareas recientes del sistema.
- `get_task(task_id: str, admin = Depends(require_auth))` - Consulta el estado de una tarea específica por su ID.
- `_run_sync_pipeline()` - Ejecuta el pipeline completo de limpieza y consolidación.

### Interacción con Base de Datos
- Motor: SQLite (indicado por `DB_PATH`)
- Tablas modificadas:
  - `analytics_snapshots` (se borra en caso de cambios)
- Columnas modificadas:
  - Todas las tablas que se procesan a través del `DataConsolidator`

### Estado y Variables Globales
- No hay variables globales explícitas mencionadas.

### Dependencias y Flujo
- **Dependencias Externas**: 
  - `logging`
  - `shutil`
  - `pathlib`
  - `typing`
  - `fastapi`
  
- **Archivos del Proyecto Importados**:
  - `config.py` (para constantes de rutas y archivos)
  - `core.auth` (para autenticación)
  - `core.state` (para gestionar estado de sincronización y caché)
  - `core.task_manager` (para manejo de tareas)
  - `db.consolidator` (para consolidación de datos)

- **Archivos del Proyecto que Importan a Este Archivo**:
  - `routes/transporte.py` (importado dentro de `_run_sync_pipeline` para sincronizar transporte)

El flujo de datos es desde el endpoint `/sync`, que inicia la tarea de sincronización, hasta la ejecución de `_run_sync_pipeline` en segundo plano mediante `TaskManager`. Este proceso incluye la lectura y procesamiento de archivos en varios directorios, la consolidación de datos en la base de datos SQLite, y la actualización del estado de las tareas.

