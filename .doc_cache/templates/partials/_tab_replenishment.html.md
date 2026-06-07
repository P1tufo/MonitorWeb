## Archivo: ./templates/partials/_tab_replenishment.html

### Resumen Funcional
Este fragmento HTML es una interfaz de usuario para mostrar sugerencias de pedido en un sistema de monitoreo de almacén (WMS). Muestra una tabla con detalles sobre el material, su descripción, UMB, stock inicial y actual, consumo mensual, frecuencia de retiros, autonomía en meses y clasificación ABC. Incluye filtros para la frecuencia de pedido y un botón para exportar los datos a Excel.

### Catálogo de Funciones y Clases
Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** Ninguna (El fragmento HTML no interactúa directamente con una base de datos. Los datos se cargan desde un endpoint API).
- **Columnas:** Ninguna (No hay consultas SQL o ORM explícitas en el fragmento HTML).

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- **Librerías Externas:** `fas fa-exclamation-triangle`, `fas fa-file-excel`
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno (Este archivo no importa otros archivos).
- **Archivos del Proyecto que Este Archivo Importa:** Ninguno (No hay imports en el fragmento HTML).

**Flujo de Datos:**
El fragmento HTML se carga en la interfaz del usuario. Los datos para llenar la tabla se obtienen a través de una solicitud GET al endpoint `/api/inventory/replenishment-suggestions/export`.

