## Archivo: ./templates/dashboard.html

### Resumen Funcional
El archivo `dashboard.html` es una plantilla HTML para el panel de control del sistema de monitoreo de almacén (WMS). Contiene la interfaz de usuario principal que incluye encabezado, indicadores clave (KPIs), menú lateral y tabla de datos.

### Catálogo de Funciones y Clases
Ninguna.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `INITIAL_USER_GROUPS`: Variable global que almacena los grupos de usuario en formato JSON.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas directamente en este archivo.
- **Archivos del Proyecto Importados**:
  - `partials/_styles.html`
  - `partials/_modals.html`
  - `partials/_sidebar.html`
  - `partials/_table.html`
  - `partials/_scripts.html`
- **Archivos que Importan a Este Archivo**: Ninguno.

El flujo de datos se realiza a través de la inclusión de parciales HTML, lo que permite modularizar el código y mantener una estructura organizada.

