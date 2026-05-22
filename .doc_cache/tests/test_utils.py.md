## Archivo: ./tests/test_utils.py

### Resumen Funcional
El archivo `test_utils.py` contiene pruebas unitarias para verificar el comportamiento seguro e idempotente del registro de manejadores de señales en una aplicación.

### Catálogo de Funciones y Clases
- `test_setup_signal_handlers_safety()` - Verifica que el registro de manejadores de señales sea seguro e idempotente, asegurando que llamadas repetidas no provoquen excepciones en el sistema de señales.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- `pytest` - Framework para pruebas unitarias.
- `core.utils.setup_signal_handlers()` - Función que se prueba.

