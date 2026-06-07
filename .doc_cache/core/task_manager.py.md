## Archivo: ./core/task_manager.py

### Resumen Funcional
El archivo `task_manager.py` implementa un gestor de tareas en segundo plano para un sistema de monitoreo de almacén (WMS). Permite encolar, rastrear y gestionar el estado de las tareas ejecutadas o en ejecución. Utiliza un pool de hilos (`ThreadPoolExecutor`) para evitar bloquear el event loop de FastAPI.

### Catálogo de Funciones y Clases
- `TaskStatus(str, Enum)` - Define los estados posibles de una tarea (PENDING, RUNNING, DONE, FAILED).
- `TaskRecord` - Registro inmutable de una tarea ejecutada o en ejecución.
  - `task_id`: ID único de la tarea.
  - `name`: Nombre descriptivo de la tarea.
  - `status`: Estado actual de la tarea.
  - `created_at`: Fecha y hora de creación de la tarea.
  - `started_at`: Fecha y hora de inicio de la tarea.
  - `finished_at`: Fecha y hora de finalización de la tarea.
  - `result`: Resultado de la tarea si se completó exitosamente.
  - `error`: Mensaje de error si la tarea falló.
- `TaskManager` - Gestor del pool de hilos para ejecutar tareas en segundo plano.
  - `MAX_HISTORY`: Máximo número de tareas completadas en memoria.
  - `__init__(max_workers: int = 3)`: Inicializa el gestor con un número configurable de trabajadores.
  - `submit_task(name: str, fn: Callable, *args, **kwargs) -> str`: Encola una tarea para ejecución en segundo plano y devuelve su ID.
  - `get_task_status(task_id: str) -> Optional[Dict[str, Any]]`: Retorna el estado de una tarea por su ID.
  - `list_tasks(limit: int = 20) -> List[Dict[str, Any]]`: Lista las tareas más recientes (más nueva primero).
  - `has_running_task(name: str) -> bool`: Verifica si hay una tarea con el nombre dado en estado RUNNING.
  - `_trim_history()`: Elimina las tareas completadas más antiguas si se supera el límite de historial.
  - `shutdown(wait: bool = True)`: Cierra graceful del pool de threads.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- `task_manager`: Instancia global de `TaskManager` con 3 trabajadores por defecto.

### Dependencias y Flujo
- **Dependencias**: 
  - `logging`
  - `uuid`
  - `concurrent.futures.ThreadPoolExecutor`
  - `dataclasses`
  - `datetime`
  - `enum.Enum`
  - `threading.Lock`
  - `typing.Any, Callable, Dict, List, Optional`

- **Flujo de Datos**:
  - El archivo no importa ni es importado por otros archivos dentro del proyecto.
  - Las funciones y métodos se utilizan internamente para gestionar el estado de las tareas y ejecutarlas en segundo plano.

