## Archivo: ./static/js/saas_engine_core.js

### Resumen Funcional
El archivo `saas_engine_core.js` es un motor SaaS V2 que se encarga de leer contenedores con la clase `.saas-widget-v2`, renderizar gráficos o KPIs según los parámetros proporcionados, y actualizarlos dinámicamente.

### Catálogo de Funciones y Clases
- `initSaaSWidgetsV2(params = null, rootElement = document)` - Inicializa los widgets SaaS V2 en el elemento raíz especificado o en todo el documento si no se proporciona ninguno. Recibe parámetros para filtrar los datos.

### Interacción con Base de Datos
- **Motor**: Ninguna.
- **Tablas y Columnas**: No hay consultas SQL explícitas ni llamadas a ORM detectadas en este archivo.

### Estado y Variables Globales
- `window.saasChartInstancesV2` - Almacena instancias de gráficos Chart.js para widgets individuales.

### Dependencias y Flujo
- **Librerías Externas**: 
  - `ChartDataLabels` (plugin para Chart.js).
- **Archivos del Proyecto que Importan a este Archivo**:
  - Ninguno.
- **Archivos del Proyecto que Este Archivo Importa**:
  - Ninguno.

El flujo de datos es el siguiente: el archivo se ejecuta al cargar la página, inicia los widgets SaaS V2 y actualiza dinámicamente sus contenidos según los parámetros proporcionados.

