## Archivo: ./routes/config.py

### Resumen Funcional
El archivo `config.py` es un módulo que se encarga de registrar todos los routers de una aplicación FastAPI. Estos routers corresponden a diferentes funcionalidades como autenticación, dashboards, entregas, inventario, análisis proyecciones, filtros, PDFs, sincronización, documentación, configuraciones, tareas y widgets.

### Catálogo de Funciones y Clases
- `register_routes(app: FastAPI) -> None` - Registra todos los routers de la aplicación de forma centralizada. Maneja errores para evitar que un router mal configurado detenga el arranque completo del servidor.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `logger` - Variable global que almacena el objeto de registro de logs.

### Dependencias y Flujo
- **Dependencias**: 
  - `fastapi`: Se utiliza para crear la aplicación FastAPI y los routers.
  - `logging`: Para el registro de errores y mensajes de depuración.
  
- **Flujo**:
  - El archivo importa varios módulos que contienen routers específicos (`dashboard`, `deliveries`, etc.).
  - La función `register_routes` itera sobre una lista de routers y los registra en la aplicación FastAPI, capturando cualquier error que pueda ocurrir durante el proceso.

Este archivo es crucial para mantener la estructura organizada de un proyecto FastAPI, centralizando la configuración de rutas y proporcionando un punto de control para el registro de errores.

