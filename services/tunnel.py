import os
import subprocess
import threading
import time
import urllib.request
import json
import logging
from config import NGROK_BIN, TUNNEL_URL_FILE

# Configurar logs básicos
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ngrok-service")

# Lock para proteger el acceso al servicio global
_service_lock = threading.Lock()
_global_service = None

class NgrokService:
    def __init__(self, bin_path=NGROK_BIN, tunnel_file=TUNNEL_URL_FILE):
        self.bin_path = bin_path
        self.tunnel_file = tunnel_file
        self.process = None
        self._stop_event = threading.Event()

    def _validate_bin(self):
        if not os.path.exists(self.bin_path):
            logger.error(f"Binario de ngrok no encontrado en: {self.bin_path}")
            return False
        if not os.access(self.bin_path, os.X_OK):
            logger.error(f"El binario en {self.bin_path} no tiene permisos de ejecución.")
            return False
        return True

    def _save_url(self, url):
        try:
            with open(self.tunnel_file, "w") as f:
                f.write(url)
            # Intentar restringir permisos (solo lectura/escritura para el dueño)
            try:
                os.chmod(self.tunnel_file, 0o600)
            except Exception:
                pass
            return True
        except IOError as e:
            logger.error(f"No se pudo escribir en {self.tunnel_file}: {e}")
            return False

    def _get_public_url(self):
        try:
            with urllib.request.urlopen("http://localhost:4040/api/tunnels", timeout=2) as resp:
                data = json.loads(resp.read())
                for t in data.get("tunnels", []):
                    if t.get("proto") == "https":
                        return t["public_url"]
        except Exception:
            pass
        return None

    def start(self):
        if not self._validate_bin():
            return

        thread = threading.Thread(target=self._run_loop, daemon=True)
        thread.start()
        logger.info("Hilo de ngrok iniciado.")

    def stop(self):
        self._stop_event.set()
        if self.process:
            self.process.terminate()
            logger.info("Proceso ngrok terminado.")

    def _run_loop(self):
        retry_count = 0
        max_retries = 10
        
        while not self._stop_event.is_set() and retry_count < max_retries:
            # Verificar y limpiar si ya existe un ngrok corriendo
            try:
                check = subprocess.run(["pgrep", "-f", "ngrok"], capture_output=True)
                if check.returncode == 0 and not self.process:
                    logger.warning("Detectado proceso de ngrok activo. Intentando limpieza...")
                    subprocess.run(["pkill", "-f", "ngrok"])
                    time.sleep(2)
                    continue
            except Exception as e: 
                logger.debug(f"Error verificando procesos: {e}")

            logger.info("Iniciando tunel publico (ngrok)...")
            try:
                self.process = subprocess.Popen(
                    [self.bin_path, "http", "8000", "--log=false"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                
                url = None
                for i in range(15):
                    if self._stop_event.is_set(): break
                    time.sleep(1)
                    url = self._get_public_url()
                    if url: break
                
                if url:
                    retry_count = 0 
                    if self._save_url(url):
                        logger.info(f"\n{'='*55}")
                        logger.info(f"  ENLACE PUBLICO (ngrok): {url}")
                        logger.info(f"  Guardado en: {os.path.basename(self.tunnel_file)}")
                        logger.info(f"  Local:       http://localhost:8000")
                        logger.info(f"{'='*55}\n")
                else:
                    logger.warning("No se pudo obtener la URL publica.")
                
                self.process.wait()
                self.process = None
                logger.info("Tunel cerrado.")
            except Exception as e:
                logger.error(f"Error en bucle ngrok: {e}")
                retry_count += 1
            
            if not self._stop_event.is_set():
                wait_time = min(5 * (2 ** retry_count), 60)
                logger.info(f"Reintentando tunel en {wait_time}s...")
                time.sleep(wait_time)

def start_tunnel():
    """Inicia el servicio de túnel de forma segura y thread-safe."""
    global _global_service
    with _service_lock:
        if _global_service and _global_service.process and _global_service.process.poll() is None:
            logger.info("El servicio de tunel ya esta activo.")
            return _global_service
            
        _global_service = NgrokService()
        _global_service.start()
        return _global_service

def stop_tunnel():
    """Detiene el servicio de túnel de forma segura y thread-safe."""
    global _global_service
    with _service_lock:
        if _global_service:
            _global_service.stop()
            _global_service = None
