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

- `_run_loop()` - Bucle principal del servicio de ngrok.
  - Propósito: Maneja el ciclo de vida del túnel, reiniciándolo si es necesario.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa con ninguna base de datos.

### Estado y Variables Globales
- `_service_lock` - Un objeto `threading.Lock()` para proteger el acceso al servicio global.
- `_global_service` - Una variable global que almacena la instancia singleton del servicio de ngrok.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `os`, `subprocess`, `threading`, `time`, `urllib.request`, `json`, `logging`
  
- **Archivos Importados**:
  - `config.py` (para las constantes `NGROK_BIN` y `TUNNEL_URL_FILE`)
  
- **Flujo de Datos**:
  - El archivo se importa por otros archivos del proyecto para iniciar o detener el servicio de túnel.
  - Los métodos `_run_loop`, `start`, y `stop` manejan la lógica interna del servicio, mientras que las funciones `start_tunnel` y `stop_tunnel` proporcionan una interfaz segura y thread-safe para interactuar con el servicio.

