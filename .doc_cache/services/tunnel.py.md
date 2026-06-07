## Archivo: ./services/tunnel.py

### Resumen Funcional
El archivo `tunnel.py` contiene la implementación del servicio de túnel utilizando ngrok, que se utiliza para exponer el servidor local (escuchando en el puerto 8000) a Internet. El servicio es gestionado de manera segura y thread-safe mediante un singleton.

### Catálogo de Funciones y Clases
- `NgrokService(bin_path=NGROK_BIN, tunnel_file=TUNNEL_URL_FILE)` - Inicializa el objeto del servicio de ngrok.
  - Propósito: Configura las rutas del binario de ngrok y el archivo donde se guardará la URL pública.

- `_validate_bin()` - Valida si el binario de ngrok existe y tiene permisos de ejecución.
  - Propósito: Asegura que el binario de ngrok esté disponible y accesible.

- `_save_url(url)` - Guarda la URL pública en un archivo especificado.
  - Propósito: Almacena la URL del túnel público para su uso posterior.

- `_get_public_url()` - Obtiene la URL pública del túnel a través de la API de ngrok.
  - Propósito: Recupera la URL pública del túnel desde el servidor local de ngrok.

- `start()` - Inicia el servicio de ngrok en un hilo separado.
  - Propósito: Lanza el proceso de ngrok y espera hasta que se obtenga la URL pública.

- `stop()` - Detiene el servicio de ngrok.
  - Propósito: Termina el proceso de ngrok y limpia los recursos asociados.

- `_run_loop()` - Bucle principal del servicio de ngrok, encargado de iniciar y gestionar el túnel.
  - Propósito: Maneja la creación y reinicio del túnel hasta que se solicite su detención.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `_service_lock` - Lock para proteger el acceso al servicio global.
- `_global_service` - Variable global que almacena la instancia singleton del servicio de ngrok.

### Dependencias y Flujo
- **Librerías Externas**: `json`, `logging`, `os`, `subprocess`, `threading`, `time`, `urllib.request`.
- **Archivos Importados**: `config.py` (para constantes como `NGROK_BIN` y `TUNNEL_URL_FILE`).
- **Flujo de Datos**:
  - El archivo se importa por otros módulos para iniciar o detener el servicio de túnel.
  - Los métodos `_run_loop`, `start`, y `stop` manejan la creación, reinicio y finalización del proceso de ngrok en un hilo separado.

