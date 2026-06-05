## Archivo: ./static/js/docs_explorer.js

### Resumen Funcional
El archivo `docs_explorer.js` es un componente del sistema de monitoreo de almacén (WMS) que se encarga de cargar y renderizar la estructura de documentos en un árbol visual, permitiendo expandir/colapsar carpetas y cargar el contenido de los archivos seleccionados.

### Catálogo de Funciones y Clases
- `initDocs()` - Inicializa el explorador de documentos, llamando a la API para obtener la estructura del árbol de documentos y renderizarla.
- `loadFile(path)` - Carga el contenido de un archivo específico en la vista principal.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
Ninguna. No se utilizan variables globales, de sesión o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- **Dependencias**: `fetch`, `marked` (si está disponible).
- **Flujo**:
  - El archivo se carga inicialmente (`DOMContentLoaded`).
  - Al hacer clic en la pestaña de "Docs", se ejecuta `initDocs()`.
  - `initDocs()` realiza una solicitud a `/api/docs/tree` para obtener la estructura del árbol y luego llama a `renderNodes(data, treeRoot)` para renderizarla.
  - Al seleccionar un archivo en el árbol, se ejecuta `loadFile(node.path)`, que carga el contenido del archivo en `#docs-content-view`.

El flujo de datos es unidireccional desde la API hasta el cliente y luego hacia la vista.

