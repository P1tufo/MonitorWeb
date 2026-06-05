## Archivo: ./templates/partials/_sidebar.html

### Resumen Funcional
El archivo `_sidebar.html` es un fragmento de interfaz de usuario que contiene filtros y controles para interactuar con el sistema de monitoreo de almacén (WMS). Permite seleccionar fechas, áreas, centros, estados OT, realizar búsquedas y generar reportes PDF.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
- `dates`: Lista de fechas disponibles para filtrar.
- `default_dates`: Lista de fechas seleccionadas por defecto.
- `areas`: Lista de áreas disponibles para filtrar.
- `area_centro_map`: Diccionario que mapea áreas a centros.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas directamente mencionadas en el código.
- **Flujo de Datos**:
  - El archivo se importa por otros archivos HTML para renderizar la interfaz del sidebar.
  - Los eventos de los controles (checkboxes, radios, input) invocan funciones JavaScript (`toggleSidebar`, `toggleMulti`, `handleSmartCheckbox`, `applyCentroFilter`, `applyFilters`, `downloadBulk`) que pueden interactuar con el backend a través de llamadas AJAX o directamente manipular el DOM.

Este fragmento es una parte integral del frontend, proporcionando la interfaz para los usuarios interactivos y controladores para manejar las acciones del usuario.

