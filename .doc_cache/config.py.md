## Archivo: ./config.py

### Resumen Funcional
Este archivo `config.py` configura y valida los parámetros de configuración del sistema de monitoreo de almacén (WMS). Define rutas y variables globales para el almacenamiento de datos, la base de datos, el servidor web y las fuentes externas. También incluye funciones para validar la configuración y asegurar la estructura del proyecto.

### Catálogo de Funciones y Clases
- `validate_config()` - Realiza comprobaciones de salud en la configuración.
- `ensure_project_structure()` - Crea los directorios necesarios para el funcionamiento de la app si no existen.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `BASE_DIR` - Directorio raíz del proyecto.
- `DB_PATH` - Ruta a la base de datos SQLite.
- `PDF_STORAGE` - Ruta para almacenar PDFs generados.
- `CLEANSED_DIR` - Ruta para archivos limpios.
- `TEMP_DIR` - Ruta para directorios temporales.
- `CACHE_DIR_NAME` - Nombre del directorio de caché.
- `CACHE_DIR` - Ruta al directorio de caché.
- `TUNNEL_URL_FILE` - Ruta al archivo que contiene la URL del túnel.
- `NGROK_BIN` - Ruta al binario de ngrok.
- `LOG_FILE` - Ruta al archivo de registro del servidor.
- `APP_HOST` - Host del servidor web.
- `APP_PORT` - Puerto del servidor web.
- `APP_RELOAD` - Indica si el servidor debe reiniciarse automáticamente.
- `DEFAULT_ONEDRIVE` - Ruta predeterminada para OneDrive.
- `ONEDRIVE_PATH` - Ruta a la carpeta de transacciones WMS en OneDrive.
- `DELIVERIES_DIR`, `STOCK_DIR`, `TASKS_DIR`, `INVENTORY_DIR`, `MB5B_DIR` - Subdirectorios dentro de OneDrive.

### Dependencias y Flujo
- **Dependencias**: `logging`, `os`, `pathlib`, `typing`.
- **Flujo de Datos**:
  - El archivo se importa por otros archivos del proyecto para obtener las configuraciones necesarias.
  - Otros archivos pueden importar este archivo para utilizar las variables globales y funciones definidas aquí.

