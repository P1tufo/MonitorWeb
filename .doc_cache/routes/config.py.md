## Archivo: ./routes/config.py

### Resumen Funcional
El archivo `config.py` es un módulo que se encarga de registrar todos los routers de una aplicación FastAPI. Incluye manejo básico de errores para evitar que un router mal configurado detenga el arranque completo del servidor.

### Catálogo de Funciones y Clases
- `register_routes(app: FastAPI) -> None` - Registra todos los routers de la aplicación de forma centralizada, incluyendo manejo de errores básico.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- `fastapi`: Se utiliza para crear y gestionar la aplicación FastAPI.
- `logging`: Se utiliza para registrar mensajes de depuración y error.
- Importa varios módulos de ruta (`dashboard`, `deliveries`, `inventory`, etc.) desde el mismo directorio.

El archivo no depende de ninguna base de datos ni variables globales.

