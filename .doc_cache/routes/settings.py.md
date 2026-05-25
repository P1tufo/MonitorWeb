## Archivo: ./routes/settings.py

### Resumen Funcional
El archivo `settings.py` define una API para la gestión dinámica de configuraciones SaaS utilizando SQLAlchemy ORM. Permite crear, actualizar y eliminar configuraciones como mapeos de estado, centros de costo y feriados, así como consultar y modificar consultas SQL.

### Catálogo de Funciones y Clases
- `invalidate_caches(db: Session)` - Limpia el caché global en memoria y elimina todos los snapshots de base de datos.
- `SettingUpdate(key: str, value: str)` - Modelo Pydantic para actualizar configuraciones individuales.
- `StatusMappingUpdate(code: str, label: str)` - Modelo Pydantic para actualizar mapeos de estado.
- `CostCenterMappingUpdate(center_code: str, business_area: str)` - Modelo Pydantic para actualizar centros de costo.
- `HolidayAdd(date_str: str)` - Modelo Pydantic para agregar feriados.
- `QueryUpdate(query_id: str, visual_state: str)` - Modelo Pydantic para actualizar el estado visual de consultas.

### Interacción con Base de Datos
- Motor: SQLAlchemy ORM (Pilar 3)
- Tablas:
  - `analytics_snapshots`
- Columnas:
  - No se especifican columnas específicas en las consultas SQL, pero se hace referencia a la tabla `analytics_snapshots`.

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: `fastapi`, `pydantic`, `sqlalchemy`, `logging`, `pandas`, `holidays`.
- Comunicación con otros archivos del proyecto:
  - `core.auth.require_admin`
  - `core.database.get_session_dep`
  - `core.models.StatusMapping`, `CostCenterMapping`, `AppSetting`, `Holiday`, `ConfigQuery`
  - `core.db_config_manager.load_config_to_memory`, `get_setting`, `get_status_mapping`, `get_cost_center_mapping`, `get_holidays`
  - `core.app_instance.templates`
  - `core.utils.sanitize_for_json`
  - `core.state.AppState`, `get_app_state`
  - `core.query_engine.build_sql_from_payload`

