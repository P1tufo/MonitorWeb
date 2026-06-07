## Archivo: ./scripts/bundler.py

### Resumen Funcional
El archivo `bundler.py` es un script que concatena múltiples archivos JavaScript en un solo archivo llamado `bundle.js`, lo cual se utiliza para la producción del frontend de un sistema de monitoreo de almacén (WMS).

### Catálogo de Funciones y Clases
- `bundle_js()` - Concatena múltiples archivos JS en un solo bundle.js para producción.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `JS_FILES_ORDER` - Una lista ordenada de nombres de archivos JavaScript que se concatenarán.
- `logger` - Un objeto de registro utilizado para registrar mensajes de información, advertencia y error.

### Dependencias y Flujo
- **Dependencias Externas**: `logging`, `os`, `pathlib`.
- **Archivos del Proyecto Importados por Este Archivo**: Ninguno.
- **Archivos del Proyecto que Importan a Este Archivo**: Ninguno.
- **Flujo de Datos**: El script lee archivos JavaScript desde un directorio específico, los concatena en un solo archivo `bundle.js`, y registra el proceso.

