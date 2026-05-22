## Archivo: ./templates/dashboard.html

### Resumen Funcional
El archivo `dashboard.html` es una plantilla HTML para el panel de control del proyecto Onedrive, que muestra indicadores clave (KPIs) y permite navegar entre diferentes secciones de análisis.

### Catálogo de Funciones y Clases
No aplica

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `is_syncing`: Un booleano que indica si la sincronización está en curso.
- `kpi_deliveries`: Cantidad total de entregas generadas.
- `sub_del_abierta`: Cantidad de entregas en curso.
- `sub_del_no_tratada`: Cantidad de entregas no tratadas.
- `sub_del_reunido`: Cantidad de entregas reunidas a tiempo.
- `sub_del_atrasado`: Cantidad de entregas reunidas atrasadas.
- `sub_del_critico`: Cantidad de entregas críticas (OT abierta atrasada).
- `kpi_materials`: Cantidad total de materiales solicitados.
- `sub_mat_abierta`: Cantidad de picking en curso.
- `sub_mat_no_tratada`: Cantidad de pendientes por generar OT.
- `sub_mat_reunido`: Cantidad de materiales reunidos a tiempo.
- `sub_mat_atrasado`: Cantidad de materiales reunidos atrasados.
- `sub_mat_critico`: Cantidad de materiales críticos (OT abierta atrasada).
- `user.username`: Nombre de usuario actual.
- `user.role`: Rol del usuario actual.

### Dependencias y Flujo
- Utiliza plantillas parciales (`_styles.html`, `_modals.html`, `_sidebar.html`, `_table.html`, `_scripts.html`).
- No depende de ninguna librería externa específica.

