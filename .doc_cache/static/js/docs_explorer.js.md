## Archivo: ./static/js/docs_explorer.js

### Resumen Funcional
El archivo `docs_explorer.js` es un script que se encarga de cargar y renderizar una estructura de árbol de documentos en la interfaz web. Este árbol permite navegar por los archivos y carpetas, y al seleccionar un archivo, carga su contenido en el área de visualización.

### Catálogo de Funciones y Clases
- `initDocs()` - Inicializa la exploración de documentos, cargando la estructura del árbol desde una API y renderizando los nodos.
- `loadFile(path)` - Carga el contenido de un archivo específico en el área de visualización.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- **Dependencias**: El script utiliza la librería `fetch` para hacer solicitudes HTTP a una API. También depende de la librería `marked` si está disponible, para procesar el contenido del archivo como Markdown.
- **Flujo**: El flujo comienza con la carga del documento (`DOMContentLoaded`), luego se ejecuta `initDocs()`. Este método llama a `loadFile()` cuando se selecciona un archivo en el árbol.

