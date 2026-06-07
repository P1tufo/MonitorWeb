## Archivo: ./main.py

### Resumen Funcional
El archivo `main.py` es el punto de entrada oficial del sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Inicializa y gestiona la ejecución del servidor web utilizando Uvicorn, configurando servicios adicionales como un túnel Ngrok para acceso remoto.

### Catálogo de Funciones y Clases
- `start_application()` - Configura e inicia los servicios de la plataforma, incluyendo el inicio del túnel Ngrok y el lanzamiento del servidor web con Uvicorn.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
- `APP_HOST` - Dirección IP o nombre de host donde se ejecutará el servidor.
- `APP_PORT` - Puerto en el que se escuchará el servidor.
- `APP_RELOAD` - Indica si el servidor debe reiniciarse automáticamente al detectar cambios.

### Dependencias y Flujo
- **Dependencias Externas**: `uvicorn`, `logging`
- **Archivos Importados**:
  - `app` desde `app`
  - `start_tunnel` y `stop_tunnel` desde `services.tunnel`
- **Archivos que Importan a este Archivo**: Ninguno.
- **Flujo de Datos**: El archivo inicia el servidor web utilizando Uvicorn, configurando previamente un túnel Ngrok para acceso remoto.

