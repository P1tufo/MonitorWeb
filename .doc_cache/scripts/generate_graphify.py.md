## Archivo: ./scripts/generate_graphify.py

### Resumen Funcional
El archivo `generate_graphify.py` es un script que ejecuta el proceso de generación y procesamiento de un mapa interactivo utilizando la herramienta Graphify. El script limpia cualquier salida anterior, configura las variables de entorno necesarias, ejecuta Graphify para generar el mapa, y luego realiza una serie de reemplazos en el HTML generado para adaptarlo al español e incluir traducciones específicas.

### Catálogo de Funciones y Clases
- `run_graphify()` - Inicia el escaneo con Graphify, limpia la salida anterior, ejecuta Graphify, y procesa el archivo HTML generado.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `ROOT_DIR` - Directorio raíz del proyecto.

### Dependencias y Flujo
- **Dependencias**: 
  - `os`
  - `subprocess`
  - `shutil`

- **Flujo**:
  - El archivo se ejecuta directamente (`if __name__ == "__main__":`).
  - Llama a la función `run_graphify()`.

El flujo de datos es simple: el script ejecuta Graphify, procesa su salida y guarda el resultado en un directorio específico dentro del proyecto.

