## Archivo: ./templates/analytics_proyecciones.html

### Resumen Funcional
El archivo `analytics_proyecciones.html` es una plantilla HTML para la interfaz de usuario de un módulo de análisis predictivo, que muestra información sobre desplanificaciones y correlaciones entre materiales. Incluye gráficos interactivos y tablas para visualizar datos relevantes.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo HTML.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `user`: Objeto que contiene información del usuario autenticado.
- `error_msg`: Mensaje de error a mostrar en la interfaz.
- `alerts`: Lista de alertas de desplanificación.
- `scatter_data`: Datos para el gráfico de dispersión.
- `combos`: Lista de combinaciones frecuentes (Market Basket Analysis).

### Dependencias y Flujo
- **Librerías Externas**: 
  - `Chart.js` para gráficos interactivos.
- **Archivos Incluidos**:
  - `_styles.html`: Estilos CSS adicionales.
  - `_analytics_proyecciones_modals.html`: Modales adicionales.
  - `_scripts.html`: Scripts adicionales.
- **Scripts Internos**: 
  - `analytics_proyecciones.js`: Script específico para este módulo.

