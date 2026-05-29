## Archivo: ./routes/config.py

### Resumen Funcional
El archivo `config.py` es un módulo que se encarga de registrar todos los routers de una aplicación FastAPI. Estos routers corresponden a diferentes funcionalidades del sistema, como autenticación, dashboards, entregas, inventario, análisis proyecciones, filtros, PDFs, sincronización, documentos, configuraciones, tareas, widgets, consumos y transporte.

### Catálogo de Funciones y Clases
- `register_routes(app: FastAPI) -> None` - Registra todos los routers de la aplicación de forma centralizada. Maneja errores para evitar que un router mal configurado detenga el arranque completo del servidor.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `ROUTERS: List[APIRouter]` - Una lista declarativa de routers con tipado estático. Almacena todos los routers que se van a registrar en la aplicación FastAPI.

### Dependencias y Flujo
- **Dependencias**: 
  - `fastapi`: Se utiliza para crear y gestionar la aplicación FastAPI.
  - `logging`: Para el registro de errores y mensajes de depuración.
  
- **Flujo**:
  - El archivo importa varios módulos que contienen routers específicos (`dashboard`, `deliveries`, etc.).
  - La función `register_routes` itera sobre la lista de routers, intentando registrar cada uno en la aplicación FastAPI.
  - Si ocurre un error al registrar un router, se registra el error y continúa con el siguiente router.

Este archivo es crucial para mantener una estructura organizada y modular de los endpoints de la API, facilitando su mantenimiento y escalabilidad.

