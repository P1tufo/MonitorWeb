## Archivo: ./tests/test_services.py

### Resumen Funcional
El archivo `test_services.py` contiene pruebas unitarias para funciones y clases relacionadas con servicios de túnel y gestión del estado de la aplicación.

### Catálogo de Funciones y Clases
- `app_state()` - Proporciona una instancia limpia de AppState configurada con un límite de caché.
- `cleanup_tunnel()` - Garantiza la limpieza del estado global del túnel tras cada test.
- `test_state_cache_respects_limits(app_state: AppState)` - Verifica que el gestor de estado respete los límites de memoria.
- `test_state_sync_flag_reactivity(app_state: AppState)` - Valida que la propiedad reactiva de sincronización cambie su estado de forma consistente.
- `test_start_tunnel_manages_singleton_instance(mock_access, mock_exists, mock_popen)` - Verifica que start_tunnel inicialice correctamente el servicio de túnel.
- `test_stop_tunnel_releases_global_reference(mock_run)` - Valida que stop_tunnel limpie las referencias globales de forma segura.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías externas utilizadas**: `pytest`, `unittest.mock`
- **Flujo hacia otros archivos del proyecto**: Se comunica con `services.tunnel` para iniciar y detener servicios de túnel, y con `core.state` para gestionar el estado de la aplicación.

