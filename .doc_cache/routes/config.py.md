## Archivo: ./routes/config.py

### Resumen Funcional
El archivo `config.py` es un módulo que se encarga de registrar todos los routers de la aplicación FastAPI de forma centralizada. Incluye manejo de errores básico para evitar que un router mal configurado detenga el arranque completo del servidor.

### Catálogo de Funciones y Clases
- `register_routes(app: FastAPI) -> None` - Registra todos los routers de la aplicación de forma centralizada, incluyendo manejo de errores.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `ROUTER_MODULES: List[str]` - Lista declarativa de nombres de módulos de routers a importar dinámicamente.
- `ROUTERS: List[APIRouter]` - Lista que almacena los objetos `APIRouter` registrados.

### Dependencias y Flujo
- **Dependencias**: Importa `importlib`, `logging`, `typing.List` desde el módulo estándar de Python. Importa `FastAPI` y `APIRouter` desde `fastapi`.
- **Flujo**: El archivo importa dinámicamente los módulos de routers especificados en `ROUTER_MODULES`, intenta registrar cada router con la aplicación FastAPI, y registra errores si ocurren durante el proceso.

