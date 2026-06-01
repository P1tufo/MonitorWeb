## Archivo: ./core/app_instance.py

### Resumen Funcional
Este archivo configura la instancia principal de la aplicación FastAPI, incluyendo su título, descripción y versión. También establece las rutas para la documentación interactiva.

### Catálogo de Funciones y Clases
- `app: FastAPI` -> Instancia principal de la aplicación FastAPI.
- `templates_path: Path` -> Ruta al directorio de plantillas.
- `templates: Jinja2Templates` -> Motor de plantillas configurado con seguridad reforzada.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
No aplica.

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- **Importa**: `pathlib`, `fastapi`, `fastapi.templating`, `config`.
- **Es importado por**: No hay archivos que importen este archivo directamente.
- **Flujo de datos**: Este archivo no consume ni produce datos, solo configura la instancia de FastAPI y el motor de plantillas.

