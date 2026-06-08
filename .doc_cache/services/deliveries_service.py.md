## Archivo: ./services/deliveries_service.py

### Resumen Funcional
El archivo `deliveries_service.py` contiene la lógica de negocio para el servicio de entregas en un sistema de monitoreo de almacén (WMS). Este servicio se encarga de generar un contexto completo con metadatos ligeros, incluyendo áreas de negocio y widgets configurados.

### Catálogo de Funciones y Clases
- `DeliveriesService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - **Propósito**: Prepara el servicio para interactuar con la base de datos proporcionada.
  
- `get_full_context()` - Genera un contexto completo con metadatos ligeros.
  - **Propósito**: Recopila y devuelve información relevante como áreas de negocio, widgets configurados, y otros datos necesarios para el monitoreo del almacén.

### Interacción con Base de Datos
- **Motor**: SQLite
- **Tablas**:
  - `outbound_deliveries`
- **Columnas**:
  - `area_negocio`

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas**: 
  - `logging`, `typing`, `sqlalchemy.orm`
  
- **Archivos del Proyecto que Importan a este Archivo**:
  - `routes.analytics_proyecciones.get_proyecciones_context()`
  - `routes.inventory.get_inventory_context()`
  - `routes.tasks.get_tasks_context()`

- **Archivos del Proyecto que Este Archivo Importa**:
  - `core.cache_decorator.analytics_cache`
  - `core.models.ConfigQuery`
  
- **Dirección del Flujo de Datos**: 
  - El archivo importa funciones desde otros archivos y utiliza la sesión de base de datos para consultar información.

