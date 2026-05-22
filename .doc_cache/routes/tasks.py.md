## Archivo: ./routes/tasks.py

### Resumen Funcional
El archivo `tasks.py` define una ruta para obtener analíticas de tareas utilizando FastAPI. La función principal recupera el contexto completo de las tareas y lo devuelve en formato JSON.

### Catálogo de Funciones y Clases
- `get_tasks_context(session: Session) -> dict` - Obtiene el contexto completo de las tareas.
- `analytics_tasks_api(user = Depends(get_current_user), session: Session = Depends(get_session_dep), state: AppState = Depends(get_app_state))` - Endpoint FastAPI para obtener analíticas de tareas.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción directa con una base de datos.

### Estado y Variables Globales
- `state.get_cache("/api/v1/analytics/tasks")` - Recupera el contexto de las tareas desde la caché.
- `state.set_cache("/api/v1/analytics/tasks", clean_context.copy())` - Almacena el contexto de las tareas en la caché.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `logging`: Para registro de errores.
  - `sqlalchemy.orm.Session`: Para manejar sesiones de base de datos.
  - `pandas`: No se usa directamente, pero podría estar presente en el código omitido.
  - `datetime`: Para manipulación de fechas y horas.
  - `fastapi`: Para definir endpoints y dependencias.
- **Dependencias Internas**:
  - `core.state.AppState` y `get_app_state()`: Para manejar el estado global de la aplicación.
  - `core.utils.sanitize_for_json`: Para sanitizar datos antes de devolverlos en JSON.
  - `repositories.TasksRepository`: No se usa directamente, pero podría estar presente en el código omitido.
  - `services.tasks_service.TasksService`: Servicio que proporciona métodos para obtener contexto de tareas.
- **Flujo**: 
  - La función `analytics_tasks_api` depende de `get_current_user`, `get_session_dep`, y `get_app_state`.
  - Intenta recuperar el contexto de las tareas desde la caché. Si no está disponible, lo recupera del servicio `TasksService`, limpia los datos innecesarios, y lo almacena en la caché antes de devolverlo.

Este archivo es una parte integral del backend que proporciona un endpoint para obtener analíticas de tareas, utilizando servicios y dependencias definidos en otros módulos del proyecto.

