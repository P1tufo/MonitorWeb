## Archivo: ./core/task_manager.py

### Resumen Funcional
Este archivo define el `TaskManager`, un gestor de tareas en segundo plano para un sistema de monitoreo de almacén (WMS). Permite encolar, rastrear y gestionar el estado de las tareas ejecutadas en segundo plano.

### Catálogo de Funciones y Clases
- **submit_task(name: str, fn: Callable, *args, **kwargs) -> str**: Encola una tarea para ejecución en segundo plano.
- **get_task_status(task_id: str) -> Optional[Dict[str, Any]]**: Retorna el estado de una tarea por su ID.
- **list_tasks(limit: int = 20) -> List[Dict[str, Any]]**: Lista las tareas más recientes (más nueva primero).
- **has_running_task(name: str) -> bool**: Verifica si hay una tarea con el nombre dado en estado RUNNING.
- **_trim_history()**: Elimina las tareas completadas más antiguas si se supera el límite.
- **shutdown(wait: bool = True)**: Cierre graceful del pool de threads.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
1. **Entrada**: Recibe una función `fn` y sus argumentos.
2. **Transformación**: Crea un `TaskRecord` para la tarea, lo encola en el `ThreadPoolExecutor`, y actualiza su estado según el resultado de la ejecución.
3. **Salida**: No produce datos de salida directamente.

### Caché y Estado
- **Variables globales y de módulo**: `task_manager`
- **Caché en memoria**: Diccionarios `_tasks` y `_futures`
- **Mecanismos de invalidación de caché**: `_trim_history()`
- **Variables de entorno o sesión utilizadas**: No aplica.

### Lógica de Negocio y Reglas
- **Constantes de negocio**: `MAX_HISTORY = 50`
- **Reglas de validación**: Verifica si hay una tarea con el nombre dado en estado RUNNING (`has_running_task`).

### Dependencias y Flujo
- **Librerías externas**: `concurrent.futures`, `dataclasses`, `enum`, `typing`, `threading`, `logging`
- **Archivos del proyecto que este archivo importa (consume)**: No aplica.
- **Archivos del proyecto que importan a este archivo (lo consumen)**: `routes` (por ejemplo, `/api/tasks`)
- **Dirección del flujo de datos**: Desde las rutas hasta el `TaskManager`, y desde el `TaskManager` hasta la ejecución de tareas en segundo plano.

