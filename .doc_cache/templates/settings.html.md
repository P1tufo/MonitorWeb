## Archivo: ./templates/settings.html

### Resumen Funcional
El archivo `settings.html` es una página web que permite la configuración dinámica de parámetros globales del sistema, mapeos de estados de entrega y centros de costo a áreas de negocio, así como el manejo de feriados. Permite visualizar, editar y guardar cambios en estos elementos.

### Catálogo de Funciones y Clases
- `updateSetting(key)` - Actualiza un parámetro global.
- `updateStatus(code)` - Actualiza una etiqueta de estado de entrega.
- `addStatus()` - Añade un nuevo mapeo de estado de entrega.
- `deleteStatus(code)` - Elimina un mapeo de estado de entrega.
- `updateCostCenter(code)` - Actualiza el área de negocio asociada a un centro de costo.
- `addCostCenter()` - Añade un nuevo mapeo de centro de costo a área de negocio.
- `deleteCostCenter(code)` - Elimina un mapeo de centro de costo a área de negocio.
- `syncHolidays()` - Sincroniza los feriados nacionales de Chile para el año actual y el próximo.
- `addHoliday()` - Añade una nueva fecha de feriado manual.
- `deleteHoliday(date_str)` - Elimina una fecha de feriado.
- `updateQuery(id)` - Actualiza un query almacenado.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias:
- `fetch` (API para hacer solicitudes HTTP)
- `async/await` (para manejar operaciones asíncronas)

Flujo:
- La página interactúa con el backend a través de endpoints como `/api/settings/update`, `/api/settings/status`, etc., utilizando la función `apiCall`.
- Los cambios en los inputs son enviados al servidor para ser procesados y guardados.

