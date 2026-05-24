## Archivo: ./tests/test_ui_smoke.py

### Resumen Funcional
El archivo `test_ui_smoke.py` contiene pruebas unitarias para verificar la funcionalidad de componentes UI en diferentes rutas de una aplicación web. Las pruebas comprueban que los elementos esperados estén presentes y que el servidor responda correctamente a las solicitudes.

### Catálogo de Funciones y Clases
- `test_ui_smoke_components_presence(auth_client, path: str, markers: List[Tuple[str, str]])` - Prueba la presencia de componentes UI críticos en diferentes rutas.
- `test_ui_smoke_error_handling(client)` - Verifica que el servidor maneje correctamente las peticiones a rutas inexistentes.
- `test_ui_smoke_analytics_studio_modal_components(auth_client)` - Verifica que el modal visual exponga los selectores correctos y aísle el SQL.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías Externas**: `pytest`, `typing`
- **Flujo Interno**: El archivo interactúa con un cliente autenticado (`auth_client`) para realizar solicitudes HTTP a diferentes rutas de la aplicación. Las respuestas se validan para asegurar que contengan los componentes UI esperados y que el servidor responda con códigos de estado correctos (200, 404).

