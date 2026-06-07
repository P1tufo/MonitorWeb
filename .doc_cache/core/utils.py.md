## Archivo: ./core/utils.py

### Resumen Funcional
Este archivo contiene utilidades transversales y gestión de señales del sistema. Incluye funciones para configurar manejadores de señales, registrar un banner de inicio y limpiar datos para su serialización JSON segura.

### Catálogo de Funciones y Clases
- `setup_signal_handlers()` - Configura los manejadores de señales (SIGINT, SIGTERM) para un cierre limpio.
- `log_startup_banner()` - Registra un banner de inicio del módulo de utilidades.
- `sanitize_for_json(data: Any) -> Any` - Limpia datos para su serialización JSON segura de forma recursiva y exhaustiva.
- `_get_bound_params_from_visual_state(visual_state_str: str) -> list` - Alias de compatibilidad para obtener parámetros enlazados desde un estado visual.
- `_extract_metric_value(df, active_year: str = None) -> Any` - Alias de compatibilidad para extraer un valor métrico de un DataFrame.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `_handlers_registered` (booleano): Flag interno para evitar registros múltiples de manejadores de señales.

### Dependencias y Flujo
- **Dependencias Externas**: `logging`, `math`, `signal`, `sys`, `pandas`.
- **Archivos del Proyecto que Importan a este Archivo**:
  - `services.tunnel.stop_tunnel()`
  - `core.query_engine.get_bound_params_from_visual_state`
  - `core.query_engine.extract_metric_value`
- **Archivos del Proyecto que Este Archivo Importa**: Ninguno.

El flujo de datos es unidireccional, con este archivo consumiendo funciones y servicios externos para su funcionalidad.

