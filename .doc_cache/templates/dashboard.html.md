## Archivo: ./templates/dashboard.html

### Resumen Funcional
El archivo `dashboard.html` es una plantilla HTML para el panel de control del sistema de monitoreo de almacén (WMS). Contiene la interfaz de usuario principal que incluye encabezado, indicadores clave (KPIs), menú de acciones y contenido principal dividido en sidebar y tabla.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada directamente en este archivo HTML. Todas las interacciones son realizadas a través de JavaScript y eventos del usuario.

### Interacción con Base de Datos
Ninguna. El archivo no contiene consultas SQL ni llamadas a ORM para interactuar con una base de datos.

### Estado y Variables Globales
- `is_syncing`: Variable que indica si la sincronización está en curso.
- `user`: Objeto que contiene información del usuario autenticado, incluyendo su nombre de usuario y rol.
- `kpi_deliveries`, `sub_del_abierta`, `sub_del_no_tratada`, `sub_del_reunido`, `sub_del_atrasado`, `sub_del_critico`: Variables que almacenan los valores de KPIs relacionados con las entregas.
- `kpi_materials`, `sub_mat_abierta`, `sub_mat_no_tratada`, `sub_mat_reunido`, `sub_mat_atrasado`, `sub_mat_critico`: Variables que almacenan los valores de KPIs relacionados con los materiales solicitados.

### Dependencias y Flujo
- **Dependencias**: No se importan librerías externas directamente en este archivo.
- **Flujo de Datos**: El flujo de datos pasa por el servidor (FastAPI) que renderiza esta plantilla HTML, pasando los valores de las variables globales como contexto. Los eventos del usuario (clics en botones, cambios en la interfaz) se manejan con JavaScript.

Este archivo es una vista HTML que presenta información y permite interacciones al usuario, pero no realiza ninguna operación directamente relacionada con la base de datos o el backend del sistema.

