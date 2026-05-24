## Archivo: ./routes/settings.py

### Resumen Funcional
El archivo `settings.py` define una API para la gestión dinámica de configuraciones SaaS utilizando SQLAlchemy ORM. Permite crear, actualizar y eliminar configuraciones como estados, centros de costo y feriados, así como consultar y previsualizar consultas SQL.

### Catálogo de Funciones y Clases
- `invalidate_caches(db: Session)` - Limpia el caché global en memoria y elimina todos los snapshots de base de datos.
- `SettingUpdate(key: str, value: str)` - Modelo Pydantic para actualizar una configuración.
- `StatusMappingUpdate(code: str, label: str)` - Modelo Pydantic para actualizar un estado de mapeo.
- `CostCenterMappingUpdate(center_code: str, business_area: str)` - Modelo Pydantic para actualizar un centro de costo de mapeo.
- `HolidayAdd(date_str: str)` - Modelo Pydantic para agregar un feriado.
- `QueryUpdate(query_id: str, sql_text: Optional[str] = None, params: Optional[List[Any]] = None, visual_state: Optional[str] = None)` - Modelo Pydantic para actualizar una consulta.

### Interacción con Base de Datos
- Motor: SQLAlchemy ORM (Pilar 3)
- Tablas:
  - `analytics_snapshots`
- Columnas:
  - No se especifican columnas específicas en el código proporcionado.
- Consultas SQL Crudas:
  - `DELETE FROM analytics_snapshots`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías Externas: FastAPI, SQLAlchemy, Pydantic, Pandas, holidays
- Comunicación con otros archivos del proyecto:
  - `core.auth.require_admin`
  - `core.database.get_session_dep`
  - `core.models.StatusMapping`, `CostCenterMapping`, `AppSetting`, `Holiday`, `ConfigQuery`
  - `core.db_config_manager.load_config_to_memory`, `get_setting`, `get_status_mapping`, `get_cost_center_mapping`, `get_holidays`
  - `core.app_instance.templates`
  - `core.utils.sanitize_for_json`
  - `core.state.AppState`, `get_app_state`
  - `core.query_engine.build_sql_from_payload`

