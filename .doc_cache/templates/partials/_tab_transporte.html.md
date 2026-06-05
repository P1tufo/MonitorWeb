## Archivo: ./templates/partials/_tab_transporte.html

### Resumen Funcional
Este fragmento HTML es una sección de la interfaz de usuario para el sistema de monitoreo de almacén (WMS), que muestra gráficos y tablas relacionados con las entregas. Incluye un filtro por tiempo, un gráfico de líneas, alertas de OTs pendientes de ingreso en SAP, un buscador rápido de entregas y una tabla con los últimos 25 registros y reportes PDF.

### Catálogo de Funciones y Clases
- Ninguna

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:**
  - `transporte` (Tabla que almacena información sobre las entregas)
- **Columnas:**
  - `id`
  - `fecha`
  - `ot`
  - `gd`
  - `oc`
  - `bultos`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:** Ninguna
- **Archivos del Proyecto que Importan a este Archivo:**
  - `routes.py` (Consumen el fragmento para mostrarlo en la interfaz de usuario)
- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno

El flujo de datos es unidireccional, con el archivo HTML consumido por otros componentes del sistema para renderizar la interfaz de usuario.

