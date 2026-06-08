## Archivo: ./static/js/analytics_studio_config.js

### Resumen Funcional
Este archivo JavaScript define un manejador para el estado visual de gráficos en una aplicación de análisis. Permite obtener y establecer el estado visual de diferentes consultas, utilizando un patrón singleton para mantener la instancia única por consulta.

### Catálogo de Funciones y Clases
- `AnalyticsStudioManager.getVisualState(queryId)` - Obtiene el estado visual actualizado para una consulta específica.
- `AnalyticsStudioManager.setVisualState(queryId, state)` - Establece un nuevo estado visual para una consulta específica.

### Interacción con Base de Datos
Ninguna. El archivo no realiza ninguna operación directa en la base de datos.

### Estado y Variables Globales
- `studioChartInstance` - Variable global que almacena una instancia del gráfico.
- `currentSchema` - Objeto que contiene el esquema actual.
- `currentQueryId` - ID de la consulta actualmente seleccionada.
- `serverVisualState` - Estado visual almacenado en el servidor.
- `visualState` - Puntero al estado activo del modal.

### Dependencias y Flujo
- **Dependencias**: No hay dependencias externas mencionadas.
- **Flujo de Datos**: El archivo no importa ni es importado por otros archivos. Es un módulo autónomo que gestiona el estado visual de los gráficos.

