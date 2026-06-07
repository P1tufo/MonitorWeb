## Archivo: ./core/watcher.py

### Resumen Funcional
El archivo `watcher.py` es un componente del sistema de monitoreo de almacén (WMS) que utiliza la biblioteca `watchdog` para observar cambios en archivos dentro de directorios específicos. El objetivo principal es detectar cuando los archivos se han estabilizado y, en ese caso, disparar una sincronización de datos.

### Catálogo de Funciones y Clases
- **AwaitWriteFinishHandler(stability_seconds=3.0, poll_interval=1.0)** - Maneja eventos de sistema de archivos para detectar cuando los archivos se han estabilizado.
  - `on_created(event)` - Llama a `_add_file` cuando un archivo es creado.
  - `on_modified(event)` - Llama a `_add_file` cuando un archivo es modificado.
  - `_should_track(path: str) -> bool` - Determina si un archivo debe ser rastreado basándose en su nombre y extensión.
  - `_add_file(path: str)` - Agrega o actualiza la información del archivo en `tracked_files`.
  - `_poll_files()` - Monitorea los archivos para detectar cambios estables y disparar la sincronización si es necesario.
  - `stop()` - Detiene el rastreo de archivos.

- **start_watcher()** - Inicia el observador de archivos y configura el manejador para comenzar a monitorear los directorios especificados.

- **stop_watcher()** - Detiene el observador de archivos y limpia las variables globales relacionadas.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- `_observer` - Instancia del `Observer` de `watchdog`.
- `_handler` - Instancia de `AwaitWriteFinishHandler`.

### Dependencias y Flujo
- **Dependencias**: 
  - `logging`
  - `os`
  - `threading`
  - `time`
  - `watchdog.events`
  - `watchdog.observers`

- **Flujo**:
  - `start_watcher()` importa a `AwaitWriteFinishHandler` y `Observer`, luego configura y inicia el observador.
  - `stop_watcher()` detiene el observador y limpia las variables globales.

El archivo `watcher.py` se encarga de monitorear cambios en archivos dentro de los directorios especificados, detectar cuando estos archivos se han estabilizado y disparar una sincronización de datos utilizando la biblioteca `watchdog`.

