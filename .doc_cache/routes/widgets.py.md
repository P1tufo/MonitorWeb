## Archivo: ./routes/widgets.py

### Resumen Funcional
El archivo `widgets.py` contiene endpoints FastAPI que manejan la lógica de negocio para obtener datos de widgets y realizar drilldowns. Los endpoints interactúan con una base de datos para recuperar configuraciones de widgets y ejecutar consultas SQL dinámicas.

### Catálogo de Funciones y Clases
- `get_widget_data(query_id: str, year: Optional[str] = None, area: Optional[str] = None, granularity: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user), state: AppState = Depends(get_app_state))` - Endpoint para obtener datos de un widget.
- `get_widget_drilldown(query_id: str, segment: str, material: Optional[str] = None, year: Optional[str] = None, area: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user))` - Endpoint para obtener el detalle subyacente de un segmento de un widget.

### Interacción con Base de Datos
- **Motor:** SQLAlchemy ORM.
- **Tablas:** `ConfigQuery`.
- **Columnas:** `query_id`, `visual_state`, `sql_text`.

### Estado y Variables Globales
- No aplica.

### Dependencias y Flujo
- **Librerías Externas:** FastAPI, SQLAlchemy, Pandas, logging.
- **Flujo Interno:** El archivo interactúa con otros módulos como `core.database`, `core.models`, `core.auth`, `core.helpers.dynamic_executor`, `core.utils`, `core.state`, y `repositories.deliveries`.

