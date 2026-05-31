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
- Importa varios módulos desde el mismo directorio (`./routes/`), cada uno probablemente contenga un router específico para una parte del sistema.

Este archivo es crucial para la configuración centralizada de rutas en una aplicación FastAPI, asegurando que todos los endpoints estén disponibles y manejando errores de manera graciaosa.

