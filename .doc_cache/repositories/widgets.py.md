## Archivo: ./repositories/widgets.py

### Resumen Funcional
El archivo `widgets.py` contiene métodos para ejecutar visualizaciones de datos en un sistema de monitoreo de almacén (WMS). Los métodos procesan solicitudes de usuario, aplican filtros y generan gráficos basados en los datos del almacén.

### Catálogo de Funciones y Clases
- `execute_widget(query_id: str, visual_state: str, year: Optional[str], area: Optional[str], granularity: Optional[str]) -> Dict[str, Any]` - Ejecuta una consulta para generar un gráfico basado en los filtros proporcionados.
- `execute_drilldown(query_id: str, visual_state: str, segment: str, material: Optional[str], year: Optional[str]) -> list` - Realiza una exploración adicional de datos para obtener detalles más específicos.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: `outbound_deliveries`
    - Columnas: `fecha_carga`, `entrega`, `pos_`, `cantidad`, `dias_retraso`, `material`, `denominacion`
  - Tabla: `tareas` (implícita en el código)
    - Columna: `dim_fecha`

### Estado y Variables Globales
- **Variables Globales:** Ninguna

### Dependencias y Flujo
- **Librerías Externas:** pandas, sqlalchemy, json, logging, datetime
- **Archivos del Proyecto que Importan a este Archivo:** Ninguno
- **Archivos del Proyecto que Este Archivo Importa:**
  - `core.helpers.dynamic_executor.execute_visual_query`
  - `core.query_engine.build_sql_from_payload`
  - `core.schemas.VisualQueryBuilderPayload`
  - `core.utils.sanitize_for_json`
  - `base.BaseRepository`

**Flujo de Datos:**
1. `widgets.py` importa funciones y clases necesarias.
2. Los métodos `execute_widget` y `execute_drilldown` procesan los datos según las solicitudes del usuario.
3. Utilizan `pandas` para leer y manipular los datos desde la base de datos SQLite.
4. Generan gráficos o listas de datos basados en los filtros aplicados.

Este archivo es crucial para el funcionamiento del sistema de monitoreo de almacén, proporcionando funcionalidades avanzadas de visualización y exploración de datos.

