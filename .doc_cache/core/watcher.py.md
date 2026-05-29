## Archivo: ./core/watcher.py

### Resumen Funcional
El archivo `watcher.py` es un observador de archivos que monitorea cambios en un directorio especificado (`ONEDRIVE_PATH`). Cuando detecta archivos estables (sin cambios durante 3 segundos), dispara una sincronización de datos mediante la ejecución de `_run_sync_pipeline`.

### Catálogo de Funciones y Clases
- `AwaitWriteFinishHandler(stability_seconds=3.0, poll_interval=1.0)` - Maneja eventos de archivos y monitorea cambios para disparar la sincronización.
  - `_should_track(path: str) -> bool` - Determina si un archivo debe ser rastreado.
  - `on_created(event)` - Llama a `_add_file` cuando se crea un nuevo archivo.
  - `on_modified(event)` - Llama a `_add_file` cuando se modifica un archivo existente.
  - `_add_file(path: str)` - Añade o actualiza la información del archivo en el diccionario `tracked_files`.
  - `_poll_files()` - Monitorea los archivos rastreados y dispara la sincronización si es necesario.
  - `stop()` - Detiene el hilo de monitoreo y limpia los recursos.

- `start_watcher()` - Inicia el observador en el directorio especificado (`ONEDRIVE_PATH`).
- `stop_watcher()` - Detiene el observador y limpia los recursos.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `_observer`
- `_handler`

### Dependencias y Flujo
- `watchdog.observers.Observer` y `watchdog.events.FileSystemEventHandler` para la monitorización de archivos.
- `config.ONEDRIVE_PATH` para el directorio a observar.
- `core.task_manager.task_manager` y `routes.sync._run_sync_pipeline` para la ejecución de la sincronización.

