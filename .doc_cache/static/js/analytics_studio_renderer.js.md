## Archivo: ./static/js/analytics_studio_renderer.js

### Resumen Funcional
La función `renderPreviewChart` se encarga de renderizar un gráfico o tabla en el navegador basado en los datos proporcionados. El tipo de visualización (gráfico, tabla, KPI) y sus configuraciones son determinadas por parámetros del usuario.

### Catálogo de Funciones y Clases
- `renderPreviewChart(payload)` - Renderiza un gráfico o tabla según el tipo de dato proporcionado en `payload`.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `studioChartInstance` - Variable global que almacena la instancia actual del gráfico renderizado.

### Dependencias y Flujo
- **Dependencias**: 
  - `window.Chart` - Librería para crear gráficos.
  
- **Flujo de Datos**:
  - El archivo se importa en otros archivos JavaScript dentro del proyecto.
  - Otros archivos JavaScript pueden llamar a la función `renderPreviewChart(payload)` con los datos necesarios para renderizar el gráfico o tabla.

