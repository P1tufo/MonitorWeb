## Archivo: ./main.py

### Resumen Funcional
El archivo `main.py` es el punto de entrada oficial del sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Su rol es configurar e iniciar los servicios de la plataforma, incluyendo la activación de un túnel remoto para acceso remoto y el lanzamiento del servidor web utilizando Uvicorn.

### Catálogo de Funciones y Clases
- `start_application() -> None` - Configura e inicia los servicios de la plataforma. Lanza excepciones específicas como `KeyboardInterrupt` y cualquier otra excepción crítica.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
- Variables globales y de módulo: `APP_HOST`, `APP_PORT`, `APP_RELOAD`.
- Mecanismos de invalidación de caché: No aplica.
- Variables de entorno o sesión utilizadas: No aplica.

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- Librerías externas:
  - `uvicorn`
  - `logging`
- Archivos del proyecto que este archivo importa (`app`, `config`, `services.tunnel`).
- Archivos del proyecto que importan a este archivo: No aplica.
- Dirección del flujo de datos: El archivo es el punto de entrada principal, no consume ni produce datos directamente.

