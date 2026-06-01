## Archivo: ./config.py

### Resumen Funcional
Este archivo `config.py` contiene configuraciones globales y variables de entorno necesarias para el sistema de monitoreo de almacén (WMS). Define rutas, parámetros del servidor, directorios de almacenamiento y realiza validaciones iniciales.

### Catálogo de Funciones y Clases
- `validate_config() -> None` - Realiza comprobaciones de salud en la configuración.
- `ensure_project_structure() -> None` - Crea los directorios necesarios para el funcionamiento de la app si no existen.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
- Variables globales y de módulo: `BASE_DIR`, `DB_PATH`, `PDF_STORAGE`, `CLEANSED_DIR`, `TEMP_DIR`, `CACHE_DIR_NAME`, `CACHE_DIR`, `TUNNEL_URL_FILE`, `NGROK_BIN`, `LOG_FILE`, `APP_HOST`, `APP_PORT`, `APP_RELOAD`, `_home`, `DEFAULT_ONEDRIVE`, `ONEDRIVE_PATH`, `DELIVERIES_DIR`, `STOCK_DIR`, `TASKS_DIR`, `INVENTORY_DIR`.
- Caché en memoria: No aplica.
- Caché persistente: No aplica.
- Mecanismos de invalidación de caché: No aplica.
- Variables de entorno o sesión utilizadas: `DB_PATH`, `PDF_STORAGE`, `CLEANSED_DIR`, `TEMP_DIR`, `CACHE_DIR_NAME`, `APP_HOST`, `APP_PORT`, `APP_RELOAD`, `ONE_DRIVE_PATH`.

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- Librerías externas: `os`, `logging`, `typing`, `pathlib`.
- Archivos del proyecto que ESTE archivo IMPORTA (consume): No aplica.
- Archivos del proyecto que IMPORTAN a este archivo (lo consumen): FastAPI, SQLAlchemy, SQLite.
- Dirección del flujo de datos: El archivo se ejecuta al importarse para configurar y validar el entorno del sistema.

