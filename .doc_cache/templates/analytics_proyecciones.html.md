## Archivo: ./templates/analytics_proyecciones.html

### Resumen Funcional
El archivo `analytics_proyecciones.html` es una plantilla HTML para la interfaz de usuario de un módulo de análisis predictivo, que muestra información sobre desplanificaciones y predicciones de demanda. Incluye gráficos interactivos y tablas para visualizar datos relevantes.

### Catálogo de Funciones y Clases
No se detectan funciones o clases definidas en este archivo HTML.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
- `user.username`: Almacena el nombre de usuario actual.
- `error_msg`: Almacena un mensaje de error si ocurre algún problema.
- `alerts`: Lista de alertas de desplanificación.
- `scatter_data`: Datos para el gráfico de dispersión "Frecuencia vs Volumen".
- `combos`: Datos para la visualización de combinaciones frecuentes (Market Basket Analysis).

### Dependencias y Flujo
- **Librerías Externas**: 
  - `Chart.js` para crear gráficos interactivos.
- **Archivos del Proyecto**:
  - `_styles.html`: Incluye estilos CSS adicionales.
  - `_analytics_proyecciones_modals.html`: Contiene modales adicionales.
  - `_scripts.html`: Incluye scripts adicionales.
  - `analytics_proyecciones.js`: Script personalizado para el módulo de análisis predictivo.

