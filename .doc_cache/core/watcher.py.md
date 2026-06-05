## Archivo: ./core/watcher.py

### Resumen Funcional
El archivo `watcher.py` implementa un observador de archivos que monitorea cambios en directorios especificados, como OneDrive y otro directorio local. Cuando detecta archivos estables (sin cambios durante 3 segundos), dispara una sincronización del almacén.

### Catálogo de Funciones y Clases
- `AwaitWriteFinishHandler(stability_seconds=3.0, poll_interval=1.0)` - Maneja eventos de sistema de archivos y monitorea estabilidad de los archivos.
  - `_should_track(path: str) -> bool` - Determina si un archivo debe ser rastreado.
  - `on_created(event)` - Llama a `_add_file` cuando se crea un nuevo archivo.
  - `on_modified(event)` - Llama a `_add_file` cuando se modifica un archivo existente.
  - `_add_file(path: str)` - Añade o actualiza la información del archivo en el diccionario `tracked_files`.
  - `_poll_files()` - Monitorea los archivos rastreados y dispara una sincronización si es necesario.
  - `stop()` - Detiene el observador y las operaciones de monitoreo.

- `start_watcher()` - Inicia el observador en los directorios especificados.
- `stop_watcher()` - Detiene el observador.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `_observer` - Instancia del observador de archivos.
- `_handler` - Instancia del manejador de eventos de archivos.

### Dependencias y Flujo
- **Librerías Externas**: `watchdog`, `logging`, `threading`.
- **Archivos Importados**:
  - `config.py`: Para obtener el camino de OneDrive.
  - `core.task_manager`: Para gestionar tareas asincrónicas.
  - `routes.sync`: Para ejecutar la sincronización del almacén.

El flujo de datos es el siguiente:
1. `start_watcher()` se llama para iniciar el observador en los directorios especificados.
2. El observador (`_observer`) monitorea los eventos de archivos en los directorios rastreados.
3. Cuando un archivo es modificado y alcanza la estabilidad requerida, `_poll_files()` detecta esto y dispara `task_manager.submit_task("sync_data", _run_sync_pipeline)`.
4. `stop_watcher()` se llama para detener el observador y las operaciones de monitoreo.

Este flujo asegura que los cambios en los archivos sean sincronizados con el almacén solo cuando estos son estables, evitando la sobrecarga del sistema con sincronizaciones innecesarias.

