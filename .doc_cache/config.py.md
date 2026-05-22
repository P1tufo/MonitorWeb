## Archivo: ./config.py

### Resumen Funcional
Este archivo config.py define y gestiona las configuraciones globales del proyecto, incluyendo rutas de directorios, parámetros del servidor y variables de entorno. También realiza comprobaciones de salud en la configuración y asegura la estructura del proyecto al importar el módulo.

### Catálogo de Funciones y Clases
- `validate_config()` - Realiza comprobaciones de salud en la configuración.
- `ensure_project_structure()` - Crea los directorios necesarios para el funcionamiento de la app si no existen.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `BASE_DIR` - Directorio raíz del proyecto.
- `DB_PATH` - Ruta a la base de datos.
- `PDF_STORAGE` - Ruta para almacenar PDFs generados.
- `CLEANSED_DIR` - Ruta para archivos limpios.
- `TEMP_DIR` - Ruta para directorios temporales.
- `CACHE_DIR_NAME` - Nombre del directorio de caché.
- `CACHE_DIR` - Ruta al directorio de caché.
- `TUNNEL_URL_FILE` - Ruta al archivo que contiene la URL del túnel.
- `NGROK_BIN` - Ruta al binario de ngrok.
- `LOG_FILE` - Ruta al archivo de registro del servidor.
- `APP_HOST` - Host del servidor.
- `APP_PORT` - Puerto del servidor.
- `APP_RELOAD` - Indica si el servidor debe reiniciarse automáticamente.
- `DEFAULT_ONEDRIVE` - Ruta predeterminada a OneDrive.
- `ONEDRIVE_PATH` - Ruta a OneDrive.
- `DELIVERIES_DIR`, `STOCK_DIR`, `TASKS_DIR`, `INVENTORY_DIR` - Subdirectorios de transacciones WMS.

### Dependencias y Flujo
- Librerías utilizadas: `os`, `logging`, `typing`, `pathlib`.
- No comunica con otros archivos del proyecto.

