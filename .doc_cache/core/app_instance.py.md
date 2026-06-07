## Archivo: ./core/app_instance.py

### Resumen Funcional
Inicializa la instancia de la aplicación FastAPI con configuraciones específicas y establece el directorio para las plantillas Jinja2.

### Catálogo de Funciones y Clases
- `FastAPI()` - Crea una instancia de la aplicación FastAPI.
- `Jinja2Templates(directory=str(templates_path))` - Configura el motor de plantillas Jinja2 con el directorio especificado.

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `app: FastAPI` - Instancia principal de la aplicación FastAPI.
- `templates_path: Path` - Ruta al directorio de las plantillas.
- `templates: Jinja2Templates` - Motor de plantillas configurado.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directamente importadas en este archivo.
- **Flujo de Datos**: Este archivo no consume ni produce datos. Es una configuración inicial para la aplicación FastAPI y el motor de plantillas Jinja2.

