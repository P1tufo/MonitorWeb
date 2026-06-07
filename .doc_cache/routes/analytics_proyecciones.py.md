## Archivo: ./routes/analytics_proyecciones.py

### Resumen Funcional
Este archivo define las rutas para obtener analíticas de proyecciones en un sistema de monitoreo de almacén (WMS). Permite refrescar los datos si es necesario y utiliza una caché para mejorar el rendimiento.

### Catálogo de Funciones y Clases
- `get_proyecciones_context()` - Obtiene el contexto de proyecciones, priorizando la caché.
- `get_analytics_proyecciones(request: Request, force_refresh: bool = False, cache: CacheManager = Depends(get_cache_manager))` - Retorna los datos de proyecciones en formato JSON.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna (el archivo no interactúa directamente con la base de datos).

### Estado y Variables Globales
- `DB_PATH` - Ruta a la base de datos SQLite.
- `CacheManager` - Gestor de caché utilizado para almacenar los resultados de las proyecciones.

### Dependencias y Flujo
- Librerías externas: FastAPI, SQLAlchemy, config.py, core.auth, core.state, db.predictive_engine.
- Archivos del proyecto que importan a este archivo: Ninguno.
- Archivos del proyecto que este archivo importa:
  - `config.py` - Para obtener la ruta de la base de datos.
  - `core/auth.py` - Para autenticar el usuario actual.
  - `core/state.py` - Para gestionar la caché.
  - `db/predictive_engine.py` - Para generar las predicciones.

El flujo de datos es: el cliente hace una solicitud a `/analytics/proyecciones`, que luego llama a `get_proyecciones_context()` para obtener los datos. Si `force_refresh` es True, se limpia la caché antes de obtener los nuevos datos. Los datos son generados por `generate_predictions(_DB)` y almacenados en caché si no hay errores. Finalmente, los datos se devuelven al cliente en formato JSON.

