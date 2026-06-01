## Archivo: ./core/watcher.py

### Resumen Funcional
Este archivo implementa un observador de archivos que monitorea cambios en un directorio especificado (ONEDRIVE_PATH) y ejecuta una sincronización de datos cuando se detectan archivos estables. Es parte del sistema de monitoreo de almacén (WMS) y utiliza la arquitectura Routes → Services → Repositories → DB.

### Catálogo de Funciones y Clases
- `AwaitWriteFinishHandler(stability_seconds=3.0, poll_interval=1.0)` -> Maneja eventos de archivos y monitorea estabilidad.
  - Métodos principales: `_should_track(path)`, `on_created(event)`, `on_modified(event)`, `_add_file(path)`, `_poll_files()`, `stop()`
- `start_watcher()` -> Inicia el observador de archivos.
- `stop_watcher()` -> Detiene el observador de archivos.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
1. **Entrada**: Directorio a monitorear (`ONEDRIVE_PATH`).
2. **Transformaciones**:
   - Monitorea eventos de creación y modificación de archivos.
   - Verifica si los archivos son estables (sin cambios durante `stability_seconds`).
3. **Salida**: Dispara la ejecución de `_run_sync_pipeline()` cuando se detectan archivos estables.

### Caché y Estado
- Variables globales: `_observer`, `_handler`
- No aplica caché en memoria o persistente.
- Mecanismos de invalidación de caché: No aplica.
- Variables de entorno o sesión utilizadas: `ONEDRIVE_PATH`

### Lógica de Negocio y Reglas
- **Reglas de negocio**:
  - Solo se monitorean archivos con extensiones `.txt`, `.csv`, `.xlsx`, `.xls`.
  - Archivos que comienzan con `~` o `.` no son monitoreados.
  - Se espera una estabilidad de `stability_seconds` antes de considerar un archivo como estable.

### Dependencias y Flujo
- **Librerías externas**: `watchdog`, `logging`, `threading`
- **Archivos del proyecto que importa**:
  - `config.py`: Para obtener `ONEDRIVE_PATH`.
  - `core/task_manager.py`: Para gestionar tareas.
  - `routes/sync.py`: Para ejecutar `_run_sync_pipeline()`.
- **Archivos del proyecto que son importados por este archivo**: No aplica.

