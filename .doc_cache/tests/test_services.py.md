## Archivo: ./tests/test_services.py

### Resumen Funcional
El archivo `test_services.py` contiene pruebas unitarias para funciones y servicios relacionados con la gestión del estado de la aplicación y el manejo de túneles en un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite.

### Catálogo de Funciones y Clases
- `app_state()` - Proporciona una instancia limpia de AppState configurada para pruebas.
- `cleanup_tunnel()` - Garantiza la limpieza del estado global del túnel tras cada test.
- `test_state_cache_respects_limits(app_state: AppState)` - Verifica que el gestor de estado respete los límites de memoria.
- `test_state_sync_flag_reactivity(app_state: AppState)` - Valida que la propiedad reactiva de sincronización cambie su estado de forma consistente.
- `test_start_tunnel_manages_singleton_instance(mock_access, mock_exists, mock_popen)` - Verifica que `start_tunnel` inicialice correctamente el servicio de túnel.
- `test_stop_tunnel_releases_global_reference(mock_run)` - Valida que `stop_tunnel` limpie las referencias globales de forma segura.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `TEST_MAX_CACHE_SIZE` - Constante que establece el límite de caché para pruebas.
- `app_state.max_cache_size` - Variable global que almacena el límite de caché en la instancia de AppState.

### Dependencias y Flujo
- **Librerías Externas**: `pytest`, `unittest.mock`.
- **Archivos del Proyecto Importados**:
  - `services.tunnel`: Para las funciones `start_tunnel` y `stop_tunnel`.
  - `core.state`: Para la clase `AppState`.
- **Archivos del Proyecto que Importan a Este Archivo**: Ninguno.

El flujo de datos se centra en la ejecución de pruebas unitarias para asegurar el correcto funcionamiento de los servicios y funciones relacionados con el estado de la aplicación y el manejo de túneles.

