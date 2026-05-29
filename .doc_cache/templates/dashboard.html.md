## Archivo: ./templates/dashboard.html

### Resumen Funcional
El archivo `dashboard.html` es una plantilla HTML para el panel de control del proyecto Onedrive, que muestra información sobre entregas y materiales solicitados. Incluye un encabezado con opciones de navegación, indicadores clave (KPIs) y un menú lateral.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo HTML.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `is_syncing`: Variable que indica si la sincronización está en curso.
- `user.username`: Nombre del usuario actual.
- `user.role`: Rol del usuario actual.
- `kpi_deliveries`: Número total de entregas generadas.
- `sub_del_abierta`, `sub_del_no_tratada`, `sub_del_reunido`, `sub_del_atrasado`, `sub_del_critico`: Contadores para diferentes estados de las entregas.
- `kpi_materials`: Número total de materiales solicitados.
- `sub_mat_abierta`, `sub_mat_no_tratada`, `sub_mat_reunido`, `sub_mat_atrasado`, `sub_mat_critico`: Contadores para diferentes estados de los materiales.

### Dependencias y Flujo
- **Librerías externas**: No se detectan librerías externas utilizadas.
- **Flujo hacia otros archivos**: El archivo incluye parciales HTML (`_styles.html`, `_modals.html`, `_sidebar.html`, `_table.html`, `_scripts.html`) que probablemente contienen el estilo, modales, menú lateral, tabla y scripts necesarios para la funcionalidad del panel de control.

