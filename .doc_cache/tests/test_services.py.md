## Archivo: ./tests/test_services.py

### Resumen Funcional
El archivo `test_services.py` contiene pruebas unitarias para funciones y clases relacionadas con la gestión del estado de caché y el manejo de túneles en un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite.

### Catálogo de Funciones y Clases
- `cache_manager()` - Proporciona una instancia limpia de CacheManager configurada para pruebas.
- `sync_manager()` - Proporciona una instancia limpia de SyncStateManager.
- `cleanup_tunnel()` - Garantiza la limpieza del estado global del túnel tras cada test.
- `test_state_cache_respects_limits(cache_manager: CacheManager)` - Verifica que el gestor de estado respete los límites de memoria.
- `test_state_sync_flag_reactivity(sync_manager: SyncStateManager)` - Valida que la propiedad reactiva de sincronización cambie su estado de forma consistente.
- `test_start_tunnel_manages_singleton_instance(mock_access, mock_exists, mock_popen)` - Verifica que start_tunnel inicialice correctamente el servicio de túnel.
- `test_stop_tunnel_releases_global_reference(mock_run)` - Valida que stop_tunnel limpie las referencias globales de forma segura.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `TEST_MAX_CACHE_SIZE` - Constante que establece el límite de caché para pruebas.
- `cache_manager.max_cache_size` - Variable global que almacena el tamaño máximo de la caché.

### Dependencias y Flujo
- **Librerías Externas**: `unittest.mock`, `pytest`.
- **Archivos del Proyecto Importados**:
  - `core.state.CacheManager`
  - `core.state.SyncStateManager`
  - `services.tunnel.start_tunnel`
  - `services.tunnel.stop_tunnel`
- **Archivos que Importan a Este Archivo**: Ninguno.
- **Dirección del Flujo de Datos**: El flujo de datos se centra en la creación y gestión de instancias de clases, así como en las pruebas unitarias para validar su comportamiento.

