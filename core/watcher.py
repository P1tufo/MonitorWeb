import logging
import os
import threading
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from config import ONEDRIVE_PATH
from core.task_manager import task_manager
from routes.sync import _run_sync_pipeline

logger = logging.getLogger("watcher")

class AwaitWriteFinishHandler(FileSystemEventHandler):
    def __init__(self, stability_seconds=3.0, poll_interval=1.0):
        super().__init__()
        self.stability_seconds = stability_seconds
        self.poll_interval = poll_interval

        self.tracked_files = {}  # filepath -> {"size": int, "time": float}
        self.lock = threading.Lock()

        self.sync_pending = False

        self.polling_thread = threading.Thread(target=self._poll_files, daemon=True)
        self.running = True
        self.polling_thread.start()

    def _should_track(self, path: str) -> bool:
        filename = os.path.basename(path)
        if filename.startswith('~') or filename.startswith('.'):
            return False
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ['.txt', '.csv', '.xlsx', '.xls', '.pdf', '.db', '.sqlite']:
            return False
        return True

    def on_created(self, event):
        if not event.is_directory and self._should_track(event.src_path):
            self._add_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and self._should_track(event.src_path):
            self._add_file(event.src_path)

    def _add_file(self, path: str):
        with self.lock:
            try:
                size = os.path.getsize(path)
                self.tracked_files[path] = {"size": size, "time": time.time()}
            except Exception:
                # File might be locked or deleted
                pass

    def _poll_files(self):
        while self.running:
            time.sleep(self.poll_interval)

            with self.lock:
                files_to_remove = []
                stable_files_detected = False

                for path, data in self.tracked_files.items():
                    try:
                        current_size = os.path.getsize(path)
                        if current_size == data["size"]:
                            if time.time() - data["time"] >= self.stability_seconds:
                                stable_files_detected = True
                                files_to_remove.append(path)
                        else:
                            self.tracked_files[path] = {"size": current_size, "time": time.time()}
                    except Exception:
                        files_to_remove.append(path)

                for path in files_to_remove:
                    del self.tracked_files[path]

                if stable_files_detected:
                    self.sync_pending = True

                if self.sync_pending and len(self.tracked_files) == 0:
                    self.sync_pending = False

                    if not task_manager.has_running_task("sync_data"):
                        logger.info("Watcher: Archivos estables. Disparando _run_sync_pipeline en segundo plano.")
                        task_manager.submit_task("sync_data", _run_sync_pipeline)
                    else:
                        logger.info("Watcher: Archivos estables, pero ya hay una sincro en curso. Ignorado.")

    def stop(self):
        self.running = False
        self.polling_thread.join(timeout=2.0)


_observer = None
_handler = None

def start_watcher():
    global _observer, _handler
    if _observer is not None:
        return

    path_to_watch = ONEDRIVE_PATH
    avanti_pdf_path = "/Users/christianykelly/Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Pruebas/Avanti/PDFs_por_fecha"

    _handler = AwaitWriteFinishHandler(stability_seconds=3.0)
    _observer = Observer()

    scheduled = False

    if os.path.exists(path_to_watch):
        _observer.schedule(_handler, path=path_to_watch, recursive=True)
        scheduled = True
    else:
        logger.warning(f"Watcher: Directorio {path_to_watch} no existe.")

    if os.path.exists(avanti_pdf_path):
        _observer.schedule(_handler, path=avanti_pdf_path, recursive=True)
        scheduled = True
    else:
        logger.warning(f"Watcher: Directorio de PDFs {avanti_pdf_path} no existe.")

    if scheduled:
        _observer.start()
        logger.info("Watcher iniciado (recursive=True, awaitWriteFinish=3.0s)")
    else:
        logger.warning("Watcher cancelado, no hay directorios válidos.")

def stop_watcher():
    global _observer, _handler
    if _observer is not None:
        logger.info("Deteniendo Watcher...")
        _observer.stop()
        if _handler:
            _handler.stop()
        _observer.join()
        _observer = None
        _handler = None
