## Archivo: ./core/utils.py

### Resumen Funcional
Este archivo contiene utilidades transversales y gestión de señales del sistema. Incluye funciones para configurar manejadores de señales, registrar mensajes de inicio y limpiar datos para su serialización JSON segura.

### Catálogo de Funciones y Clases
- `setup_signal_handlers()` - Configura los manejadores de señales (SIGINT, SIGTERM) para un cierre limpio.
- `log_startup_banner()` - Registra un mensaje de inicio del módulo de utilidades del sistema.
- `sanitize_for_json(data: Any) -> Any` - Limpia datos para su serialización JSON segura.
- `_get_bound_params_from_visual_state(visual_state_str: str) -> list` - Extrae parámetros limitados desde una cadena de estado visual.
- `_extract_metric_value(df, active_year: str = None) -> Any` - Extrae el valor numérico de la métrica de un DataFrame de forma segura.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `_handlers_registered` (boolean): Flag interno para evitar registros múltiples de manejadores de señales.

### Dependencias y Flujo
- `signal`: Para manejar señales del sistema.
- `sys`: Para salir del programa.
- `logging`: Para registrar mensajes.
- `pandas`: Para manipular datos en formato DataFrame.
- `math`: Para manejar valores numéricos especiales (NaN, Inf).
- `typing.Final`, `typing.Any`: Para anotaciones de tipos.

