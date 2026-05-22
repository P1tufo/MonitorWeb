## Archivo: ./templates/partials/_tab_inventory.html

### Resumen Funcional
Este fragmento HTML es una pestaña que muestra un análisis de movimientos en una interfaz web, incluyendo estadísticas clave y gráficos interactivos.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este fragmento HTML. Todas las interacciones son realizadas a través de JavaScript y eventos del usuario.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `user.role`: Rol del usuario actual.
- `kpi_ingresos`, `kpi_consumos_prod`, `kpi_consumos_mant`, `rate_reabast`, `kpi_traspasos`, `rate_devolucion`, `rate_eficiencia`: Valores de KPIs que se muestran en la interfaz.
- `top_materials_quick`: Lista de materiales más consumidos (Top Consumidos).
- `top_users`: Lista de usuarios con mayor frecuencia de despachos.

### Dependencias y Flujo
Dependencias:
- JavaScript: Se utilizan funciones como `switchInventarioView`, `openEditQueryModal`, `openModal`, `openModalUserInventario`.

Flujo:
Este fragmento HTML se comunica con otros archivos a través de llamadas a funciones JavaScript que pueden estar definidas en otros archivos del proyecto. No hay interacción directa con bases de datos ni dependencias externas adicionales mencionadas.

