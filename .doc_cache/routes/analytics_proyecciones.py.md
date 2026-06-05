## Archivo: ./routes/analytics_proyecciones.py

### Resumen Funcional
Este archivo define las rutas para obtener analíticas de proyecciones en un sistema de monitoreo de almacén (WMS). Permite refrescar los datos si es necesario y utiliza una caché para mejorar el rendimiento.

### Catálogo de Funciones y Clases
- `get_proyecciones_context()` - Obtiene el contexto de proyecciones, priorizando la caché.
- `get_analytics_proyecciones(request: Request, force_refresh: bool = False, state: AppState = Depends(get_app_state))` - Retorna los datos de proyecciones en formato JSON.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas y Columnas: Ninguna (se utiliza `generate_predictions(_DB)` que es una función externa)

### Estado y Variables Globales
- `AppState` - Almacena el estado del sistema, incluyendo la caché.
- `get_app_state()` - Función para obtener el estado actual del sistema.

### Dependencias y Flujo
- Librerías Externas: FastAPI, SQLAlchemy (a través de `generate_predictions(_DB)`).
- Archivos Importados:
  - `./core/auth.py` - Para la autenticación.
  - `./core/state.py` - Para el manejo del estado del sistema.
  - `./db/predictive_engine.py` - Para generar predicciones.
  - `./config.py` - Para obtener la ruta de la base de datos.

- Flujo de Datos:
  1. El usuario hace una solicitud a `/analytics/proyecciones`.
  2. La función `get_analytics_proyecciones` verifica si se debe forzar el refresco de los datos.
  3. Si no se fuerza el refresco, intenta obtener los datos desde la caché.
  4. Si la caché está vacía o se requiere un refresco, llama a `get_proyecciones_context()`.
  5. `get_proyecciones_context()` genera las predicciones utilizando `generate_predictions(_DB)`.
  6. Las predicciones se almacenan en la caché y se devuelven como respuesta JSON.

Este archivo es crucial para el monitoreo de proyecciones en el sistema WMS, asegurando que los datos sean actualizados regularmente y accesibles rápidamente a través de una interfaz RESTful.

