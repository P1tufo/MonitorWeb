## Archivo: ./templates/analytics_proyecciones.html

### Resumen Funcional
El archivo `analytics_proyecciones.html` es una plantilla HTML para la interfaz de usuario del módulo de análisis predictivo en el Sistema de Monitoreo de Almacén (WMS). Muestra información sobre alertas de desplanificación, un gráfico de dispersión y analisis de market basket.

### Catálogo de Funciones y Clases
Ninguna función o clase detectada directamente en este archivo HTML. Todas las interacciones son a través de JavaScript y llamadas a funciones definidas en otros archivos.

### Interacción con Base de Datos
Ninguna. El archivo no contiene consultas SQL ni interacciones con una base de datos.

### Estado y Variables Globales
- `user`: Objeto que contiene información del usuario actual.
- `error_msg`: Mensaje de error a mostrar en la interfaz.
- `alerts`: Lista de alertas de desplanificación.
- `scatter_data`: Datos para el gráfico de dispersión.
- `combos`: Datos para el análisis de market basket.

### Dependencias y Flujo
- **Dependencias**: 
  - Chart.js: Para renderizar gráficos.
  
- **Archivos Importados**:
  - `_styles.html`: Archivo que contiene estilos CSS.
  - `analytics_proyecciones.css`: Hoja de estilo específica para esta página.
  - `_scripts.html`: Archivo que contiene scripts JavaScript generales.
  - `analytics_proyecciones.js`: Script específico para esta página.

- **Archivos Exporados**:
  - No se exportan funciones o clases desde este archivo HTML. Todas las interacciones son a través de eventos y llamadas a funciones en otros archivos JavaScript.

El flujo de datos es principalmente hacia la interfaz del usuario, donde los datos JSON (`data_scatter`, `data_alerts`, `data_combos`) son utilizados para alimentar gráficos y tablas.

