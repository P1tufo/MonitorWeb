## Archivo: ./scripts/generate_graphify.py

### Resumen Funcional
El archivo `generate_graphify.py` es un script que prepara y ejecuta el proceso de generación de un mapa interactivo utilizando la herramienta `graphify`. El script limpia cualquier salida previa, ejecuta el CLI de `graphify`, traduce el HTML generado y lo mueve al directorio estático para su visualización en la aplicación web.

### Catálogo de Funciones y Clases
- `prepare_environment()` - Limpia el directorio anterior y prepara la configuración.
- `execute_graphify()` - Ejecuta el CLI de graphify.
- `process_and_move_html()` - Lee el HTML generado, lo traduce y lo guarda en su destino.
- `run_graphify()` - Inicia el escaneo con Graphify.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `ROOT_DIR` - Directorio raíz del proyecto.
- `OUT_DIR` - Directorio donde se genera la salida de `graphify`.
- `DEST_DIR` - Directorio donde se mueve el archivo HTML final.
- `TRANSLATIONS` - Diccionario con traducciones para elementos HTML.

### Dependencias y Flujo
- **Dependencias**: `shutil`, `subprocess`, `pathlib`.
- **Flujo de Datos**:
  - `generate_graphify.py` importa `shutil`, `subprocess` y `pathlib`.
  - `graphify-out` es el directorio donde se genera la salida de `graphify`.
  - El archivo HTML generado se mueve a `static/docs`.

El flujo comienza con la ejecución del script, que llama a `run_graphify()`, que en su turno llama a `prepare_environment()`, `execute_graphify()` y finalmente `process_and_move_html()`.

