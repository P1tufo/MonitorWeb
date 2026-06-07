## Archivo: ./templates/partials/_tab_inventory.html

### Resumen Funcional
Este fragmento HTML es una pestaña de análisis de movimientos en el sistema de monitoreo de almacén (WMS). Muestra estadísticas clave como ingresos, consumos y traspasos, junto con gráficos que representan la eficiencia operativa y tendencias de consumo.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - No se especifican consultas SQL o llamadas a ORM en este fragmento HTML. Todas las estadísticas y datos son presentados directamente desde el contexto del backend.

### Estado y Variables Globales
- `user.role`: Rol del usuario actual.
- `ingresos_eff_stats`, `ingresos_eff_stats_weekly`: Datos de eficiencia operativa para ingresos (mensuales y semanales).
- `consumos_eff_stats`, `consumos_eff_stats_weekly`: Datos de eficiencia operativa para consumos (mensuales y semanales).
- `kpi_devoluciones`: Tasa de devoluciones.

### Dependencias y Flujo
- **Dependencias Externas:** Font Awesome (`fas fa-layer-group`, `fas fa-cog`, etc.)
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:** Ninguno

El flujo de datos es unidireccional, con el backend proporcionando los datos necesarios para renderizar la vista en el frontend.

