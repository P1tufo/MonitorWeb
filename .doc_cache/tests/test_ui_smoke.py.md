## Archivo: ./tests/test_ui_smoke.py

### Resumen Funcional
El archivo `test_ui_smoke.py` contiene pruebas unitarias para verificar la presencia de componentes UI críticos en diferentes rutas del sistema de monitoreo de almacén (WMS). Las pruebas incluyen verificación de la disponibilidad del servidor, la presencia de elementos HTML específicos y el manejo adecuado de errores.

### Catálogo de Funciones y Clases
- `test_ui_smoke_components_presence(auth_client, path: str, markers: List[Tuple[str, str]])` - Prueba que verifica la presencia de componentes UI críticos en diferentes rutas.
- `test_ui_smoke_error_handling(client)` - Prueba que verifica el manejo correcto del servidor para rutas inexistentes.
- `test_ui_smoke_analytics_studio_modal_components(auth_client)` - Prueba que verifica la presencia de selectores visuales y asegura que no exista el textarea de SQL crudo.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Librerías Externas**: `pytest`, `typing`
- **Archivos del Proyecto Importados**:
  - Ninguno.
- **Archivos del Proyecto que Importan a Este Archivo**:
  - Ninguno.

