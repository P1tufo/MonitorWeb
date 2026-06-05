## Archivo: ./routes/config.py

### Resumen Funcional
El archivo `config.py` es un módulo que se encarga de registrar todos los routers de la aplicación FastAPI en una instancia de `FastAPI`. Incluye manejo básico de errores para evitar que un router mal configurado detenga el arranque completo del servidor.

### Catálogo de Funciones y Clases
- `register_routes(app: FastAPI) -> None` - Registra todos los routers de la aplicación en una instancia de `FastAPI`.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `ROUTERS: List[APIRouter]` - Una lista declarativa de routers con tipado estático que se registran en la aplicación.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directamente mencionadas.
- **Flujo**: El archivo importa varios módulos de ruta (`dashboard`, `deliveries`, etc.) y registra sus routers en una instancia de `FastAPI`.

