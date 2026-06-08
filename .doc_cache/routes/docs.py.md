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
- **Dependencias**: No hay dependencias externas directamente importadas.
- **Flujo de Datos**:
  - `get_docs_tree()` genera un árbol jerárquico de archivos del proyecto, identificando cuáles tienen documentación.
  - `get_doc_content(path: str)` intenta leer el contenido de una documentación desde la carpeta real o desde el caché, y devuelve su contenido.

**Flujo detallado**:
1. **`get_docs_tree()`**:
   - Recorre los archivos del proyecto, ignorando ciertos directorios y extensiones.
   - Construye un árbol jerárquico con información sobre cada archivo/documentación.
   - Ordena el árbol primero por carpetas y luego por archivos, alfabéticamente.
   - Añade una opción destacada para la documentación global.

2. **`get_doc_content(path: str)`**:
   - Intenta leer el contenido de un archivo `.md` desde la carpeta real del proyecto.
   - Si no existe en la carpeta real, intenta leerlo desde el caché.
   - Devuelve el contenido del archivo si lo encuentra, o lanza una excepción `HTTPException` 404 si no se encuentra.

