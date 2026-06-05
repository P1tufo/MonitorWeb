## Archivo: ./repositories/widgets.py

### Resumen Funcional
El archivo `widgets.py` contiene métodos para ejecutar consultas dinámicas y generar visualizaciones de datos en un sistema de monitoreo de almacén (WMS). Los métodos permiten filtrar y procesar datos según parámetros como año, área y granularidad.

### Catálogo de Funciones y Clases
- `execute_widget(query_id: str, visual_state: str, year: Optional[str], area: Optional[str], granularity: Optional[str]) -> Dict[str, Any]` - Ejecuta una consulta dinámica para generar una visualización.
- `execute_drilldown(query_id: str, visual_state: str, segment: str, material: Optional[str], year: Optional[str]) -> list` - Realiza un drilldown en los datos según el segmento y material proporcionados.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:** `outbound_deliveries`
- **Columnas:** 
  - `fecha_carga`, `entrega`, `pos_`, `cantidad`, `dias_retraso`, `material`, `denominacion`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- **Librerías Externas:**
  - `logging`
  - `json`
  - `pandas`
  - `sqlalchemy`
  - `typing`
- **Archivos del Proyecto que Importan a este Archivo:** 
  - `core.helpers.dynamic_executor.execute_visual_query`
  - `core.schemas.VisualQueryBuilderPayload`
  - `core.query_engine.build_sql_from_payload`
  - `core.utils.sanitize_for_json`
- **Archivos del Proyecto que Este Archivo Importa:**
  - `base.BaseRepository`

**Flujo de Datos:**
1. `widgets.py` importa funciones y clases necesarias.
2. Los métodos `execute_widget` y `execute_drilldown` son llamados desde otros archivos del proyecto.
3. Estos métodos interactúan con la base de datos para ejecutar consultas SQL dinámicas y procesar los resultados.
4. Los resultados se formatean y devuelven como un diccionario o lista según el método utilizado.

Este archivo es crucial para la generación de visualizaciones en el sistema WMS, permitiendo una interacción dinámica con los datos del almacén.

