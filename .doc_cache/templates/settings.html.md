## Archivo: ./templates/settings.html

### Resumen Funcional
El archivo `settings.html` es una página web que permite la gestión dinámica de parámetros globales del sistema WMS, incluyendo mapeos de estados de entrega, centros de costo a áreas de negocio, calendario de feriados y opciones de exportación de datos. La interfaz permite editar valores, guardar cambios, agregar y eliminar registros, así como sincronizar datos.

### Catálogo de Funciones y Clases
- `openPasswordModal()` - Abre el modal para cambiar la contraseña.
- `closePasswordModal()` - Cierra el modal para cambiar la contraseña.
- `changePassword()` - Maneja el cambio de contraseña a través de una API.
- `updateSetting(key)` - Actualiza un parámetro global.
- `updateStatus(code)` - Actualiza un mapeo de estado de entrega.
- `addStatus()` - Añade un nuevo mapeo de estado de entrega.
- `deleteStatus(code)` - Elimina un mapeo de estado de entrega.
- `updateCostCenter(code)` - Actualiza un mapeo de centro de costo a área de negocio.
- `addCostCenter()` - Añade un nuevo mapeo de centro de costo a área de negocio.
- `deleteCostCenter(code)` - Elimina un mapeo de centro de costo a área de negocio.
- `syncHolidays()` - Sincroniza los feriados nacionales de Chile.
- `addHoliday()` - Añade una nueva fecha de feriado manual.
- `deleteHoliday(date_str)` - Elimina una fecha de feriado manual.

### Interacción con Base de Datos
Ninguna. El archivo no realiza consultas SQL ni interactúa directamente con la base de datos.

### Estado y Variables Globales
No hay variables globales explícitas definidas en el código.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas específicas.
- **Archivos del Proyecto Importados**:
  - `partials/_styles.html` - Estilos CSS adicionales.
  - `partials/_logout.html` - Código para cerrar sesión.
- **Archivos que Importan a Este Archivo**: Ninguno.

El flujo de datos se gestiona principalmente a través de eventos de clic en botones y llamadas AJAX a endpoints definidos en el backend (FastAPI).

