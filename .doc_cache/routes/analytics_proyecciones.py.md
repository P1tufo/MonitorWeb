## Archivo: ./routes/analytics_proyecciones.py

### Resumen Funcional
Este archivo define rutas para obtener analíticas de proyecciones utilizando FastAPI. Incluye una función que genera predicciones y las almacena en caché, así como una ruta GET que devuelve estos datos.

### Catálogo de Funciones y Clases
- `get_proyecciones_context()` - Obtiene el contexto de proyecciones, priorizando la caché.
- `get_analytics_proyecciones(request: Request, force_refresh: bool = False, state: AppState = Depends(get_app_state))` - Retorna los datos de proyecciones en formato JSON.

### Interacción con Base de Datos
- Motor: No aplica (No hay interacción directa con bases de datos).
- Tablas y Columnas: No aplica (No hay consultas SQL crudas o llamadas a ORM).

### Estado y Variables Globales
- `AppState` - Almacena el estado del sistema, incluyendo la caché.
- `_DB` - Ruta de la base de datos definida en `config`.

### Dependencias y Flujo
- Librerías externas: FastAPI, SQLAlchemy (a través de `db.predictive_engine`).
- Comunicación con otros archivos:
  - `core.auth.get_current_user` - Para autenticación.
  - `core.state.get_app_state` - Para obtener el estado del sistema.
  - `db.predictive_engine.generate_predictions(_DB)` - Para generar predicciones.

