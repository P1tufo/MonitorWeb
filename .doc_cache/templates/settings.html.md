## Archivo: ./templates/settings.html

### Resumen Funcional
El archivo `settings.html` es una página web que permite la gestión dinámica de parámetros globales del sistema, mapeos de estados de entrega y centros de costo a áreas de negocio, así como la sincronización de feriados. La interfaz presenta tablas interactivas para editar y guardar cambios en estos elementos.

### Catálogo de Funciones y Clases
- `openPasswordModal()` - Abre el modal para cambiar la contraseña.
- `closePasswordModal()` - Cierra el modal para cambiar la contraseña.
- `changePassword()` - Maneja el cambio de contraseña, validando los campos y haciendo una solicitud a la API.
- `updateSetting(key)` - Actualiza un parámetro global en la base de datos.
- `updateStatus(code)` - Actualiza un mapeo de estado de entrega en la base de datos.
- `addStatus()` - Añade un nuevo mapeo de estado de entrega a la base de datos.
- `deleteStatus(code)` - Elimina un mapeo de estado de entrega de la base de datos.
- `updateCostCenter(code)` - Actualiza un mapeo de centro de costo a área de negocio en la base de datos.
- `addCostCenter()` - Añade un nuevo mapeo de centro de costo a área de negocio a la base de datos.
- `deleteCostCenter(code)` - Elimina un mapeo de centro de costo a área de negocio de la base de datos.
- `syncHolidays()` - Sincroniza los feriados nacionales de Chile para el año actual y el próximo.
- `addHoliday()` - Añade una nueva fecha de feriado manualmente.
- `deleteHoliday(date_str)` - Elimina una fecha de feriado de la base de datos.
- `updateQuery(id)` - No se menciona en el código proporcionado.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- `fetch` para hacer solicitudes HTTP a la API.
- `apiCall(url, method, data = null)` - Función auxiliar para manejar las solicitudes HTTP.

Flujo:
- La página interactúa con el backend a través de endpoints como `/api/auth/change-password`, `/api/settings/update`, `/api/settings/status`, etc., para realizar operaciones CRUD en los parámetros globales, mapeos y feriados.

