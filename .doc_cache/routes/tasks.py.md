## Archivo: ./routes/tasks.py

### Resumen Funcional
El archivo `tasks.py` proporciona una interfaz RESTful para obtener analíticas de tareas en un sistema de almacén (WMS) utilizando FastAPI. La API permite recuperar datos de tareas, almacenándolos en caché para mejorar el rendimiento y gestionando el estado de sincronización.

### Catálogo de Funciones y Clases
- `get_tasks_context(session: Session) -> dict` - Obtiene el contexto completo de las tareas utilizando un servicio.
- `analytics_tasks_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), cache: CacheManager = Depends(get_cache_manager), sync: SyncStateManager = Depends(get_sync_manager))` - Endpoint FastAPI para obtener analíticas de tareas, recuperando datos del caché si es posible.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos. Utiliza un servicio (`TasksService`) que probablemente interactúa con el repositorio de tareas para obtener los datos necesarios.

### Estado y Variables Globales
- `logger` - Objeto de registro utilizado para registrar errores.
- `router` - Instancia de `APIRouter` de FastAPI para definir las rutas del API.

### Dependencias y Flujo
- **Dependencias Importadas**: 
  - `get_current_user`, `get_session_dep`, `get_cache_manager`, `get_sync_manager` - Funciones que proporcionan dependencias como la sesión de base de datos, el manejador de caché y el estado de sincronización.
  
- **Archivos Importados**:
  - `core.auth`: Para autenticación del usuario.
  - `core.database`: Para obtener la sesión de base de datos.
  - `core.schemas`: Para definir los modelos de respuesta.
  - `core.state`: Para gestionar el estado de caché y sincronización.
  - `core.utils`: Para utilidades como la limpieza de datos para JSON.
  - `repositories`: Para interactuar con las tablas de la base de datos.
  - `services.tasks_service`: Para obtener el contexto completo de las tareas.

- **Flujo de Datos**:
  1. El endpoint `analytics_tasks_api` se invoca a través de una solicitud HTTP GET a `/api/v1/analytics/tasks`.
  2. Se intenta recuperar los datos del caché.
  3. Si el dato no está en caché, se obtiene utilizando el servicio `TasksService`.
  4. El contexto obtenido se limpia para eliminar información sensible y se almacena en caché.
  5. Finalmente, se devuelve la respuesta con los datos limpios y el estado de sincronización.

Este archivo es crucial para proporcionar una interfaz eficiente y segura para obtener analíticas de tareas en un sistema de almacén, utilizando técnicas de caché y gestión de estado para mejorar el rendimiento.

