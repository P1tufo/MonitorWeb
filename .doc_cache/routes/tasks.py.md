## Archivo: ./routes/tasks.py

### Resumen Funcional
El archivo `tasks.py` contiene la definición de una ruta FastAPI para proporcionar analíticas sobre las tareas del almacén. La ruta permite a un usuario autenticado obtener datos detallados sobre las tareas, excluyendo ciertos campos sensibles.

### Catálogo de Funciones y Clases
- `get_tasks_context(session: Session) -> dict` - Obtiene el contexto completo de las tareas utilizando el servicio `TasksService`.
- `analytics_tasks_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), sync: SyncStateManager = Depends(get_sync_manager))` - Ruta FastAPI que devuelve analíticas sobre las tareas en formato JSON.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas directas a la base de datos. Utiliza el repositorio `TasksRepository` y el servicio `TasksService`, pero no interactúa explícitamente con la BD.

### Estado y Variables Globales
- Ninguna variable global, de sesión o diccionario quemado en código que almacene estado crítico.

### Dependencias y Flujo
- **Librerías externas**: `pandas`, `fastapi`, `sqlalchemy`.
- **Archivos del proyecto que IMPORTA (consume)**: 
  - `core.auth.get_current_user`
  - `core.database.get_session_dep`
  - `core.schemas.AnalyticsTasksResponse`
  - `core.state.SyncStateManager`
  - `core.utils.sanitize_for_json`
  - `repositories.TasksRepository`
  - `services.tasks_service.TasksService`
- **Archivos del proyecto que IMPORTAN a este archivo (lo consumen)**: Ninguno.
- **Dirección del flujo de datos**: El flujo comienza con la solicitud HTTP, pasa por el middleware de autenticación y dependencias, luego se procesa en `analytics_tasks_api`, donde se obtiene el contexto de las tareas y se devuelve como respuesta JSON.

