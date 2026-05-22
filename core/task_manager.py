"""
core/task_manager.py — Gestor de Tareas en Segundo Plano (Background Task Queue).

Pilar 4 del Roadmap SaaS: Procesamiento en Segundo Plano.

Arquitectura:
  - ThreadPoolExecutor con pool configurable (default: 3 workers).
  - Cada tarea recibe un ID UUID y se puede rastrear vía /api/tasks.
  - El estado de cada tarea (pending → running → done/failed) se mantiene
    en memoria con límite de historial para evitar fugas.
  - API pública simple: submit_task(), get_task_status(), list_tasks().

Migración futura a Celery:
  - Reemplazar submit_task() por .delay() de Celery.
  - Los endpoints API no cambian.
"""
import uuid
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Any, Optional
from threading import Lock

logger = logging.getLogger("task-manager")


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


@dataclass
class TaskRecord:
    """Registro inmutable de una tarea ejecutada o en ejecución."""
    task_id: str
    name: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "name": self.name,
            "status": self.status.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "result": self.result,
            "error": self.error,
        }


class TaskManager:
    """
    Pool de hilos para ejecutar tareas pesadas sin bloquear el event loop de FastAPI.

    Uso:
        from core.task_manager import task_manager

        task_id = task_manager.submit_task("sync_data", my_sync_function, arg1, arg2)
        status  = task_manager.get_task_status(task_id)
    """

    MAX_HISTORY = 50  # Máximo de tareas completadas en memoria

    def __init__(self, max_workers: int = 3):
        self._max_workers = max_workers
        self._executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="bg-task")
        self._tasks: Dict[str, TaskRecord] = {}
        self._futures: Dict[str, Future] = {}
        self._lock = Lock()
        self._shutdown = False
        logger.info(f"TaskManager inicializado con {max_workers} workers.")

    def submit_task(self, name: str, fn: Callable, *args, **kwargs) -> str:
        """
        Encola una tarea para ejecución en segundo plano.

        Args:
            name: Nombre descriptivo de la tarea (ej. "sync_data", "generate_pdf").
            fn:   Función callable a ejecutar.
            *args, **kwargs: Argumentos para la función.

        Returns:
            task_id: UUID único de la tarea para rastreo.
        """
        task_id = str(uuid.uuid4())[:8]  # Corto para legibilidad en logs y UI
        record = TaskRecord(task_id=task_id, name=name)

        # Re-inicializar si el pool fue cerrado (e.g. entre ciclos de test)
        if self._shutdown:
            self._executor = ThreadPoolExecutor(
                max_workers=self._max_workers, thread_name_prefix="bg-task"
            )
            self._shutdown = False

        with self._lock:
            self._tasks[task_id] = record
            self._trim_history()

        def _wrapped():
            record.status = TaskStatus.RUNNING
            record.started_at = datetime.now().isoformat()
            logger.debug(f"[Task {task_id}] Iniciando: {name}")
            try:
                result = fn(*args, **kwargs)
                record.status = TaskStatus.DONE
                record.result = str(result) if result else "OK"
                logger.debug(f"[Task {task_id}] Completada: {name}")
            except Exception as e:
                record.status = TaskStatus.FAILED
                record.error = str(e)
                logger.error(f"[Task {task_id}] Falló: {name} — {e}", exc_info=True)
            finally:
                record.finished_at = datetime.now().isoformat()

        future = self._executor.submit(_wrapped)
        with self._lock:
            self._futures[task_id] = future

        logger.debug(f"[Task {task_id}] Encolada: {name}")
        return task_id

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retorna el estado de una tarea por su ID."""
        record = self._tasks.get(task_id)
        return record.to_dict() if record else None

    def list_tasks(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Lista las tareas más recientes (más nueva primero)."""
        with self._lock:
            records = sorted(
                self._tasks.values(),
                key=lambda t: t.created_at,
                reverse=True,
            )
        return [r.to_dict() for r in records[:limit]]

    def has_running_task(self, name: str) -> bool:
        """Verifica si hay una tarea con el nombre dado en estado RUNNING."""
        with self._lock:
            return any(
                t.name == name and t.status == TaskStatus.RUNNING
                for t in self._tasks.values()
            )

    def _trim_history(self):
        """Elimina las tareas completadas más antiguas si se supera el límite."""
        completed = [
            (tid, t) for tid, t in self._tasks.items()
            if t.status in (TaskStatus.DONE, TaskStatus.FAILED)
        ]
        if len(completed) > self.MAX_HISTORY:
            # Ordenar por fecha y eliminar las más antiguas
            completed.sort(key=lambda x: x[1].created_at)
            for tid, _ in completed[:len(completed) - self.MAX_HISTORY]:
                del self._tasks[tid]
                self._futures.pop(tid, None)

    def shutdown(self, wait: bool = True):
        """Cierre graceful del pool de threads."""
        if not self._shutdown:
            logger.info("TaskManager cerrándose...")
            self._executor.shutdown(wait=wait)
            self._shutdown = True


# ─── Singleton global ─────────────────────────────────────────────────────────
task_manager = TaskManager(max_workers=3)
