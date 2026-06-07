## Archivo: ./routes/docs.py

### Resumen Funcional
El archivo `docs.py` proporciona endpoints para generar y obtener la documentación del sistema de monitoreo de almacén (WMS). Ofrece una vista jerárquica de los archivos del proyecto con indicadores de si tienen documentación, así como un endpoint para leer el contenido específico de las documentaciones.

### Catálogo de Funciones y Clases
- `get_docs_tree()` - Genera un árbol de archivos del proyecto indicando cuáles tienen documentación.
- `get_doc_content(path: str)` - Obtiene el contenido de la documentación (.md) para un archivo específico.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `BASE_DIR` - Directorio base del proyecto.
- `CACHE_DIR` - Directorio donde se almacenan las copias en caché de las documentaciones.

### Dependencias y Flujo
- **Dependencias Externas**: No hay dependencias externas directamente importadas.
- **Archivos Importados**:
  - `config.py`: Para obtener los directorios base (`BASE_DIR`, `CACHE_DIR`).
- **Archivos que Importan a este Archivo**: Ninguno.

El flujo de datos es el siguiente:
1. El usuario accede al endpoint `/api/docs/tree` para obtener la estructura del proyecto con indicadores de documentación.
2. El usuario accede al endpoint `/api/docs/content/{path:path}` para leer el contenido específico de una documentación (.md).

