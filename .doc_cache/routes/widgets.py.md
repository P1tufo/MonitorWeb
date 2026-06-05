## Archivo: ./routes/widgets.py

### Resumen Funcional
El archivo `widgets.py` contiene endpoints FastAPI que manejan la lógica de negocio para obtener datos de widgets en un sistema de monitoreo de almacén (WMS). Los endpoints permiten recuperar datos estructurados y detalles subyacentes de los widgets, aplicando filtros dinámicos basados en parámetros como año, área y segmentos.

### Catálogo de Funciones y Clases
- `get_widget_data(query_id: str, year: Optional[str] = None, area: Optional[str] = None, granularity: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user), state: AppState = Depends(get_app_state))` - Ejecuta el VisualQueryBuilderPayload y retorna la data estructurada.
- `get_widget_drilldown(query_id: str, segment: str, material: Optional[str] = None, year: Optional[str] = None, area: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user))` - Obtiene el detalle subyacente de un segmento de un widget.

### Interacción con Base de Datos
- **Motor:** SQLite
- **TABLAS:** `ConfigQuery`, `outbound_deliveries`
- **COLUMNAS:**
  - `ConfigQuery`: `query_id`, `visual_state`
  - `outbound_deliveries`: `fecha_carga`, `entrega`, `pos_`, `cantidad`, `dias_retraso`, `material`

### Estado y Variables Globales
- No se detectan variables globales, de sesión o de entorno.

### Dependencias y Flujo
- **Librerías Externas:** `fastapi`, `sqlalchemy`, `pandas`
- **Archivos del Proyecto que IMPORTA:**
  - `core.database`: `get_session_dep`
  - `core.models`: `ConfigQuery`
  - `core.auth`: `get_current_user`
  - `core.helpers.dynamic_executor`: `execute_visual_query`
  - `core.utils`: `sanitize_for_json`
  - `core.state`: `get_app_state`, `AppState`
- **Archivos del Proyecto que IMPORTAN a este archivo:**
  - No se detectan archivos que importen directamente a este archivo.

**Flujo de Datos:**
1. Los endpoints son invocados por clientes externos.
2. Se realizan consultas a la base de datos para obtener los estados visuales de los widgets y los datos necesarios.
3. Se aplican filtros dinámicos basados en los parámetros proporcionados.
4. Se ejecuta una consulta SQL dinámica o se utiliza un generador de consultas (`build_sql_from_payload`).
5. Los resultados son procesados y formateados para su presentación en el frontend.
6. Los datos procesados y formateados se devuelven al cliente.

**Nota:** Existe una duplicidad en la definición del endpoint `get_widget_drilldown`, lo cual debe ser corregido para evitar conflictos de rutas.

