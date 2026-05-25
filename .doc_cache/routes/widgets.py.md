## Archivo: ./routes/widgets.py

### Resumen Funcional
El archivo `widgets.py` define un endpoint FastAPI que ejecuta consultas SQL dinámicas y devuelve datos estructurados para visualización en una interfaz de usuario. El endpoint maneja tanto widgets modernos (que utilizan JSON) como legacy (que solo contienen texto SQL).

### Catálogo de Funciones y Clases
- `get_widget_data(query_id: str, year: Optional[str] = None, area: Optional[str] = None, db: Session = Depends(get_session_dep), user = Depends(get_current_user), state: AppState = Depends(get_app_state))` - Endpoint que ejecuta consultas SQL dinámicas y devuelve datos para visualización.

### Interacción con Base de Datos
- **Motor:** SQLAlchemy
- **Tablas:** `ConfigQuery`
- **Columnas:** `query_id`, `visual_state`, `sql_text`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- **Librerías Externas:** FastAPI, SQLAlchemy, Pandas, logging
- **Flujo Interno:** El archivo interactúa con el estado de la aplicación (`AppState`), ejecuta consultas SQL utilizando `execute_visual_query`, y utiliza `sanitize_for_json` para limpiar los datos antes de devolverlos.

