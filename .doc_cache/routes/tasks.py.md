## Archivo: ./routes/tasks.py

### Resumen Funcional
El archivo `tasks.py` contiene la definición de una ruta FastAPI para obtener analíticas de tareas en un sistema de almacén (WMS). La ruta permite recuperar datos de tareas, aplicar un contexto limpio y almacenar los resultados en caché.

### Catálogo de Funciones y Clases
- `get_tasks_context(session: Session) -> dict` - Obtiene el contexto completo de las tareas utilizando el servicio `TasksService`.
- `analytics_tasks_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Ruta FastAPI que devuelve analíticas de tareas en formato JSON.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos. Utiliza el servicio `TasksService` para obtener los datos necesarios.

### Estado y Variables Globales
- `state.get_cache("/api/v1/analytics/tasks")` - Recupera el contexto de las tareas desde el caché.
- `state.set_cache("/api/v1/analytics/tasks", clean_context.copy())` - Almacena el contexto limpio en el caché.

### Dependencias y Flujo
- **Dependencias Importadas**: 
  - `get_current_user`, `get_session_dep`, `get_app_state` desde `core.auth`, `core.database`, `core.state`.
  - `TasksService` desde `services.tasks_service`.
  - `AnalyticsTasksResponse` desde `core.schemas`.

- **Archivos que Importan a este Archivo**: Ninguno.

- **Flujo de Datos**:
  1. La función `analytics_tasks_api` se invoca cuando un usuario accede a la ruta `/api/v1/analytics/tasks`.
  2. Se intenta recuperar el contexto de las tareas desde el caché.
  3. Si no está en caché, se obtiene el contexto completo utilizando `TasksService`.
  4. El contexto se limpia eliminando ciertas claves (`'request', 'user', 'is_syncing'`).
  5. El contexto limpio se almacena en caché y se devuelve como respuesta JSON.

Este flujo asegura que los datos de tareas sean recuperados eficientemente, utilizando el caché cuando sea posible para mejorar el rendimiento.

