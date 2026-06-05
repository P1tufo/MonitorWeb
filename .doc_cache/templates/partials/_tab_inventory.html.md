## Archivo: ./templates/partials/_tab_inventory.html

### Resumen Funcional
Este fragmento HTML es una pestaña que muestra el análisis de movimientos en un sistema de monitoreo de almacén (WMS). Incluye un selector para cambiar entre vistas anuales y semanales, KPIs (indicadores clave de rendimiento) como ingresos, consumo de producción, mantenimiento, tasa de reabastecimiento, traspasos, tasas desplanificadas y devoluciones, así como tablas dinámicas que muestran la capacidad operativa y eficiencia.

### Catálogo de Funciones y Clases
- Ninguna función o clase detectada directamente en el fragmento HTML proporcionado.

### Interacción con Base de Datos
- **Motor:** SQLite (implícito, ya que se menciona "SQLite" en el contexto del proyecto).
- **Tablas y Columnas:**
  - No hay consultas SQL crudas o llamadas a ORM explícitas en este fragmento HTML. Las tablas y columnas específicas se obtienen a través de variables pasadas al template (como `ingresos_eff_stats`, `consumos_eff_stats`, etc.).

### Estado y Variables Globales
- **Variables Globales:** Ninguna variable global detectada directamente en el fragmento HTML proporcionado.
- **Estado Crítico:** Las variables que contienen datos dinámicos como `kpi_devoluciones` son pasadas al template desde el backend.

### Dependencias y Flujo
- **Librerías Externas:**
  - Font Awesome (`fas fa-layer-group`, `fas fa-cog`, etc.)
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno.
- **Archivos del Proyecto que Este Archivo Importa:** Ninguno.

**Flujo de Datos:**
El fragmento HTML consume datos desde el backend (probablemente a través de una vista o endpoint FastAPI) y los muestra en la interfaz. Los datos incluyen KPIs, estadísticas de eficiencia y gráficos que se actualizan según la selección del usuario.

**Nota:** El contenido HTML es principalmente estético y interactivo, sin funciones o consultas directas a la base de datos.

