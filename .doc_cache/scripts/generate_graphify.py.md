## Archivo: ./scripts/generate_graphify.py

### Resumen Funcional
El archivo `generate_graphify.py` es un script que prepara y ejecuta el proceso de generación de un mapa interactivo utilizando la herramienta `graphify`. El script limpia el directorio de salida, ejecuta el CLI de `graphify`, procesa el HTML generado para aplicar traducciones y finalmente mueve el archivo HTML resultante a una ubicación específica dentro del proyecto.

### Catálogo de Funciones y Clases
- `prepare_environment()` - Limpia el directorio anterior y prepara la configuración.
- `execute_graphify()` - Ejecuta el CLI de graphify.
- `process_and_move_html()` - Lee el HTML generado, lo traduce y lo guarda en su destino.
- `run_graphify()` - Inicia el escaneo con Graphify.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `ROOT_DIR` - Directorio raíz del proyecto.
- `OUT_DIR` - Directorio donde se genera el HTML por `graphify`.
- `DEST_DIR` - Directorio de destino para el archivo HTML final.
- `TRANSLATIONS` - Diccionario con traducciones para elementos HTML.

### Dependencias y Flujo
- **Dependencias**: `shutil`, `subprocess`, `pathlib`.
- **Flujo**:
  - `generate_graphify.py` importa `shutil`, `subprocess` y `pathlib`.
  - No hay archivos del proyecto que importen a este archivo.
  - El flujo de datos es desde el script hasta la ejecución del CLI de `graphify`, procesamiento del HTML y finalmente su movimiento al directorio de destino.

