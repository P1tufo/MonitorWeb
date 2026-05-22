## Archivo: ./tests/test_ui_smoke.py

### Resumen Funcional
Este archivo contiene pruebas de humo (smoke tests) para verificar la presencia de componentes UI críticos en diferentes endpoints de una aplicación web. Las pruebas aseguran que los servidores respondan correctamente y que el HTML contenga los IDs necesarios para la inicialización de scripts frontend.

### Catálogo de Funciones y Clases
- `test_ui_smoke_components_presence(auth_client, path: str, markers: List[Tuple[str, str]])` - Prueba de humo parametrizada que verifica la presencia de componentes visuales críticos en diferentes endpoints.
- `test_ui_smoke_error_handling(client)` - Verifica que el servidor maneje correctamente las peticiones a rutas inexistentes.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Librerías externas utilizadas**: `pytest`, `typing`
- **Flujo**: El archivo interactúa con un cliente autenticado (`auth_client`) para realizar peticiones a diferentes endpoints y verifica la presencia de componentes UI específicos en el HTML de las respuestas. También interactúa con un cliente no autenticado (`client`) para verificar el manejo de rutas inexistentes.

