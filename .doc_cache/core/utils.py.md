## Archivo: ./core/utils.py

### Resumen Funcional
Este archivo contiene utilidades transversales y gestión de señales del sistema. Se encarga de configurar manejadores de señales para un cierre limpio, registrar mensajes de inicio y sanitizar datos para su serialización JSON segura.

### Catálogo de Funciones y Clases
- `setup_signal_handlers() -> None` - Configura los manejadores de señales (SIGINT, SIGTERM) para un cierre limpio.
- `log_startup_banner() -> None` - Registra un mensaje de inicio del módulo de utilidades.
- `sanitize_for_json(data: Any) -> Any` - Limpia datos para serialización JSON segura de forma recursiva y exhaustiva.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
- Variables globales: `_handlers_registered` - Flag interno para evitar registros múltiples.
- Variables de entorno o sesión utilizadas: No aplica.

### Lógica de Negocio y Reglas
No aplica.

### Dependencias y Flujo
- Librerías externas:
  - `signal`
  - `sys`
  - `logging`
  - `pandas`
  - `math`
  - `typing`

- Archivos del proyecto que IMPORTA a este archivo (lo consumen):
  - `services.tunnel.stop_tunnel()`
  - `core.query_engine.get_bound_params_from_visual_state(visual_state_str)`
  - `core.query_engine.extract_metric_value(df, active_year)`

- Archivos del proyecto que este archivo IMPORTA:
  - No aplica

El flujo de datos es desde las funciones hacia los archivos dependientes.

