## Archivo: ./core/task_manager.py

### Resumen Funcional
El archivo `task_manager.py` implementa un gestor de tareas en segundo plano utilizando un `ThreadPoolExecutor`. Permite encolar, rastrear y gestionar el estado de las tareas, manteniendo un historial limitado en memoria.

### Catálogo de Funciones y Clases
- **TaskStatus** - Enumeración que define los estados posibles de una tarea (PENDING, RUNNING, DONE, FAILED).
- **TaskRecord** - Clase de datos inmutable que registra la información de una tarea.
  - `task_id`: Identificador único de la tarea.
  - `name`: Nombre descriptivo de la tarea.
  - `status`: Estado actual de la tarea.
  - `created_at`, `started_at`, `finished_at`: Fechas de creación, inicio y finalización de la tarea.
  - `result`, `error`: Resultado o error de la tarea.
- **TaskManager** - Clase que gestiona el encolamiento y ejecución de tareas.
  - `submit_task(name: str, fn: Callable, *args, **kwargs) -> str`: Encola una nueva tarea para ejecución.
  - `get_task_status(task_id: str) -> Optional[Dict[str, Any]]`: Retorna el estado de una tarea por su ID.
  - `list_tasks(limit: int = 20) -> List[Dict[str, Any]]`: Lista las tareas más recientes.
  - `has_running_task(name: str) -> bool`: Verifica si hay una tarea con el nombre dado en estado RUNNING.
  - `_trim_history()`: Elimina las tareas completadas más antiguas si se supera el límite de historial.
  - `shutdown(wait: bool = True)`: Cierra gracefulmente el pool de threads.

### Interacción con Base de Datos
No aplica. El archivo no interactúa con ninguna base de datos.

### Estado y Variables Globales
- **task_manager**: Instancia global de la clase `TaskManager` con 3 workers por defecto.

### Dependencias y Flujo
- **Dependencias**: No utiliza librerías externas adicionales.
- **Flujo**: El archivo se comunica con otros archivos del proyecto a través de su API pública (`submit_task`, `get_task_status`, `list_tasks`).

