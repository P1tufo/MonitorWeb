## Archivo: ./routes/widgets.py

### Resumen Funcional
El archivo `widgets.py` contiene endpoints FastAPI que manejan la lógica de negocio para obtener datos de widgets y realizar drilldowns. Los endpoints interactúan con una base de datos SQL para recuperar y procesar los datos, y utilizan un estado global para almacenar en caché resultados recientes.

### Catálogo de Funciones y Clases
- `get_widget_data(query_id: str, year: Optional[str] = None, area: Optional[str] = None, granularity: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user), state: AppState = Depends(get_app_state))` - Ejecuta el VisualQueryBuilderPayload y retorna la data estructurada.
- `get_widget_drilldown(query_id: str, segment: str, material: Optional[str] = None, year: Optional[str] = None, area: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user))` - Obtiene el detalle subyacente de un segmento de un widget.

### Interacción con Base de Datos
- **Motor:** SQLAlchemy ORM.
- **Tablas:** `ConfigQuery`, `outbound_deliveries`.
- **Columnas:**
  - `ConfigQuery`: `query_id`, `visual_state`, `sql_text`.
  - `outbound_deliveries`: `fecha_carga`, `entrega`, `pos_`, `cantidad`, `dias_retraso`, `material`.

### Estado y Variables Globales
- **Variables Globales:** No aplica.

### Dependencias y Flujo
- **Librerías Externas:** FastAPI, SQLAlchemy, Pandas.
- **Flujo Interno:**
  - Los endpoints dependen de funciones como `get_session_dep`, `get_current_user`, `execute_visual_query`, `sanitize_for_json`, y `build_sql_from_payload`.
  - Utilizan el estado global `AppState` para almacenar en caché resultados.

