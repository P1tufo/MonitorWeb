## Archivo: ./templates/settings.html (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `settings.html` es una interfaz de usuario para la configuración dinámica del sistema WMS. Permite gestionar parámetros globales, mapeos de estados de entrega y centros de costo a áreas de negocio, así como grupos de usuarios y feriados.

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
- `addHoliday()` - Añade un nuevo feriado manual.
- `deleteHoliday(date_str)` - Elimina un feriado manual.
- `updateUserGroup(oldName, nameId, listId)` - Actualiza el nombre y usuarios de un grupo de usuarios.
- `addUserGroup()` - Añade un nuevo grupo de usuarios.
- `deleteUserGroup(name)` - Elimina un grupo de usuarios.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos. Todas las operaciones CRUD se realizan a través de llamadas a APIs.

### Estado y Variables Globales
No hay variables globales explícitas definidas en el código. Las variables utilizadas son principalmente para almacenar valores temporales como los valores de entrada del usuario o mensajes de toast.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas específicas.
- **Flujo de Datos**:
  - El archivo `settings.html` es consumido por el navegador del cliente.
  - Los scripts JavaScript realizan llamadas a APIs para interactuar con el backend (FastAPI).
  - Las respuestas de las API son utilizadas para actualizar la interfaz de usuario dinámicamente.

El flujo de datos va desde el frontend hacia el backend, donde se realizan operaciones CRUD y luego se reflejan los cambios en la interfaz de usuario.

