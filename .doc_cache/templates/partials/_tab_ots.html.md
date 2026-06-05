## Archivo: ./templates/partials/_tab_ots.html (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
Este fragmento HTML corresponde a la pestaña de gestión de Ordenes de Transporte (OTs) en el sistema de monitoreo de almacén. Muestra estadísticas, gráficos y tablas interactivas para visualizar y gestionar OTs pendientes, movimientos no paletizados y productividad.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML.

### Interacción con Base de Datos
- **Motor**: SQLite
- **TABLAS**:
  - `inventory_movements` (Tabla donde se identifican movimientos no paletizados)
- **COLUMNAS**:
  - `doc_mat`
  - `clase_mov`
  - `user`
  - `qty`
  - `source`
  - `dest`
  - `created_at`

### Estado y Variables Globales
No se detectan variables globales, de sesión o de entorno quemadas en el código.

### Dependencias y Flujo
- **Librerías Externas**: No se importan librerías externas específicas.
- **Archivos del Proyecto que Importa a este Archivo**: Ninguno.
- **Archivos del Proyecto que Este Archivo Importa**: Ninguno.
- **Dirección del Flujo de Datos**: El fragmento HTML consume datos desde el backend (FastAPI) y los presenta en la interfaz web. No hay interacción directa con APIs externas.

Este fragmento es una vista HTML que se renderiza en el navegador, consumiendo datos desde el backend para mostrar estadísticas, gráficos y tablas interactivas relacionadas con las OTs y movimientos de almacén.

#### --- PARTE 2 de 2 ---

### Resumen Funcional
Este fragmento HTML es una interfaz de usuario para mostrar detalles de movimientos en un sistema de almacén (WMS). Incluye tablas para visualizar operaciones diarias y mensuales, con opciones para expandir los detalles de las operaciones.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
Ninguna

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
Ninguna

