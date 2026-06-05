## Archivo: ./routes/docs.py

### Resumen Funcional
El archivo `docs.py` proporciona endpoints para generar y obtener la documentación del sistema de monitoreo de almacén (WMS). Ofrece una vista jerárquica de los archivos del proyecto con indicadores de si tienen documentación, así como la capacidad de leer el contenido de las documentaciones en formato Markdown.

### Catálogo de Funciones y Clases
- `get_docs_tree(state: AppState = Depends(get_app_state))` - Genera un árbol de archivos del proyecto indicando cuáles tienen documentación.
- `get_doc_content(path: str, state: AppState = Depends(get_app_state))` - Obtiene el contenido de la documentación (.md) para un archivo específico.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa con ninguna base de datos.

### Estado y Variables Globales
- `BASE_DIR` - Directorio base del proyecto.
- `CACHE_DIR` - Directorio donde se almacenan las copias en caché de la documentación.

### Dependencias y Flujo
- **Dependencias**: Importa `os`, `fastapi`, `config`, `core.state`.
- **Flujo**:
  - `docs.py` importa a otros archivos del proyecto (`config.py`, `core/state.py`) para obtener dependencias globales y configuraciones.
  - Los endpoints son invocados por el framework FastAPI, que maneja las solicitudes HTTP.

El flujo de datos es unidireccional: los endpoints procesan las solicitudes HTTP y devuelven respuestas JSON.

