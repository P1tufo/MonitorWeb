## Archivo: ./templates/partials/_tab_inventory.html

### Resumen Funcional
Este fragmento HTML es una pestaña que muestra un análisis de movimientos en una interfaz web, incluyendo estadísticas clave y gráficos interactivos. Permite a los usuarios cambiar la vista entre "Vista Operativa (Anual)" y "Vista Semanal (Histórico)", y proporciona detalles sobre diferentes KPIs como ingresos, consumos de producción, mantenimiento, tasa de reabastecimiento, traspasos, devoluciones y eficiencia de bodega. También incluye gráficos que muestran la distribución de materiales según la curva ABC, tendencias de consumo, volumen operacional y carga semanal.

### Catálogo de Funciones y Clases
- `switchInventarioView(value)` - Cambia la vista del inventario según el valor seleccionado.
- `openEditQueryModal(id, title)` - Abre un modal para editar una consulta SQL específica.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
- `user.role` - Rol del usuario actual.
- `kpi_ingresos`, `kpi_consumos_prod`, `kpi_consumos_mant`, `rate_reabast`, `kpi_traspasos`, `rate_devolucion`, `rate_eficiencia` - Valores de KPIs calculados.
- `top_materials_quick` - Lista de materiales más consumidos.
- `top_users` - Lista de usuarios con mayor frecuencia de despachos.

### Dependencias y Flujo
- Librerías utilizadas: `FontAwesome` para iconos.
- Comunicación con otros archivos del proyecto:
  - `_tab_inventory.js` (posiblemente contiene la lógica detrás de las funciones `switchInventarioView` y `openEditQueryModal`).

