## Archivo: ./routes/settings.py

### Resumen Funcional
El archivo `settings.py` define una API para la gestión dinámica de configuraciones SaaS utilizando SQLAlchemy ORM. Permite crear, actualizar y eliminar configuraciones como estados, centros de costo y feriados, así como consultar y ejecutar consultas SQL.

### Catálogo de Funciones y Clases
- `invalidate_caches(db: Session)` - Limpia el caché global en memoria y elimina todos los snapshots de base de datos.
- `SettingUpdate(key: str, value: str)` - Modelo Pydantic para actualizar una configuración.
- `StatusMappingUpdate(code: str, label: str)` - Modelo Pydantic para actualizar un estado.
- `CostCenterMappingUpdate(center_code: str, business_area: str)` - Modelo Pydantic para actualizar un centro de costo.
- `HolidayAdd(date_str: str)` - Modelo Pydantic para agregar un feriado.
- `QueryUpdate(query_id: str, sql_text: Optional[str], params: Optional[List[Any]], visual_state: Optional[str])` - Modelo Pydantic para actualizar una consulta.
- `JoinDef(table: str, onLeft: str, onRight: str)` - Modelo Pydantic para definir una unión de tablas.
- `FilterDef(column: str, operator: str, value: Optional[str], valueType: Optional[str], compareColumn: Optional[str], offsetValue: Optional[str])` - Modelo Pydantic para definir un filtro.
- `MetricDef(column: str, aggregation: str, format: Optional[str])` - Modelo Pydantic para definir una métrica.
- `TimeAxisDef(column: str, granularity: str)` - Modelo Pydantic para definir el eje de tiempo.
- `SecondMetricDef(column: str = "", aggregation: str = "", label: str = "")` - Modelo Pydantic para definir una segunda métrica.
- `VisualQueryBuilderPayload(baseTable: str, joins: list[JoinDef], filters: list[FilterDef], metric: MetricDef, timeAxis: TimeAxisDef, breakdown: str | None, secondMetric: Optional[SecondMetricDef])` - Modelo Pydantic para definir el payload del constructor de consultas visuales.
- `settings_view(request: Request, db: DBSession, state: AppState = Depends(get_app_state))` - Vista que renderiza el panel de control de configuraciones SaaS.
- `api_get_settings(state: AppState = Depends(get_app_state))` - API para obtener las configuraciones generales.
- `api_update_setting(update: SettingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - API para actualizar una configuración.
- `api_upsert_status(update: StatusMappingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - API para insertar o actualizar un estado.
- `api_delete_status(code: str, db: DBSession, state: AppState = Depends(get_app_state))` - API para eliminar un estado.
- `api_upsert_cost_center(update: CostCenterMappingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - API para insertar o actualizar un centro de costo.
- `api_delete_cost_center(code: str, db: DBSession, state: AppState = Depends(get_app_state))` - API para eliminar un centro de costo.
- `api_add_holiday(h: HolidayAdd, db: DBSession, state: AppState = Depends(get_app_state))` - API para agregar un feriado.
- `api_sync_holidays(db: DBSession, state: AppState = Depends(get_app_state))` - API para sincronizar automáticamente los feriados nacionales (Chile).
- `api_delete_holiday(date_str: str, db: DBSession, state: AppState = Depends(get_app_state))` - API para eliminar un feriado.
- `api_get_query(query_id: str, db: DBSession, state: AppState = Depends(get_app_state))` - API para obtener el estado visual de una consulta del Analytics Studio.
- `api_update_query(update: QueryUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - API para actualizar el estado visual de una consulta.
- `api_get_schema(db: DBSession, state: AppState = Depends(get_app_state))` - API para obtener el listado de tablas y sus columnas para el editor.
- `api_query_preview(update: QueryUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - API para ejecutar una consulta temporal y retornar datos para previsualización.
- `api_build_sql(payload: VisualQueryBuilderPayload, db: DBSession, state: AppState = Depends(get_app_state))` - API para compilar el estado visual del constructor en SQL parametrizado seguro.

### Interacción con Base de Datos
El archivo interactúa con la base de datos utilizando SQLAlchemy ORM. Las tablas y columnas afectadas incluyen:
- `AppSetting`
- `StatusMapping`
- `CostCenterMapping`
- `Holiday`
- `ConfigQuery`

No hay consultas SQL crudas explícitas.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
Dependencias externas utilizadas:
- `fastapi`
- `pydantic`
- `sqlalchemy`
- `pandas`
- `holidays`

El archivo se comunica con otros archivos del proyecto a través de dependencias como `get_session_dep`, `require_admin`, `load_config_to_memory`, `get_setting`, `get_status_mapping`, `get_cost_center_mapping`, `get_holidays`, y `sanitize_for_json`.

