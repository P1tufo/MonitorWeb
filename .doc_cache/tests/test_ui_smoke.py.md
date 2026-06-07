## Archivo: ./tests/test_ui_smoke.py

### Resumen Funcional
El archivo `test_ui_smoke.py` contiene pruebas unitarias para verificar la funcionalidad y la interfaz de usuario (UI) de un sistema de monitoreo de almacén (WMS). Las pruebas incluyen la verificación de la presencia de componentes UI críticos en diferentes rutas, manejo de errores para rutas inexistentes, y validación de componentes específicos en el modal del AST.

### Catálogo de Funciones y Clases
- `test_ui_smoke_components_presence(auth_client, path: str, markers: List[Tuple[str, str]])` - Prueba la presencia de componentes UI críticos en diferentes rutas.
- `test_ui_smoke_error_handling(client)` - Verifica que el servidor maneje correctamente las peticiones a rutas inexistentes.
- `test_ui_smoke_analytics_studio_modal_components(auth_client)` - Valida la presencia de selectores visuales del AST y asegura que no exista el textarea de SQL crudo.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: `pytest`
- **Archivos Importados**:
  - `test_ui_smoke.py` importa `pytest`.
- **Archivos que Importan a este Archivo**: Ninguno.
- **Flujo de Datos**: El archivo no realiza ninguna operación que implique el flujo de datos entre diferentes componentes del sistema.

