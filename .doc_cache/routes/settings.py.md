## Archivo: ./routes/settings.py (Procesado en 1 partes)

#### --- PARTE 1 de 1 ---

### Resumen Funcional
El archivo `settings.py` proporciona una API para la gestión dinámica de configuraciones SaaS, utilizando SQLAlchemy ORM para todas las operaciones de escritura. Incluye endpoints para obtener y actualizar configuraciones generales, estados, centros de costo, feriados y consultas SQL.

### Catálogo de Funciones y Clases
- `invalidate_caches(db: Session)` - Limpia el caché global en memoria y elimina todos los snapshots de base de datos.
- `SettingUpdate(key: str, value: str)` - Modelo Pydantic para actualizar configuraciones generales.
- `StatusMappingUpdate(code: str, label: str)` - Modelo Pydantic para actualizar estados.
- `CostCenterMappingUpdate(center_code: str, business_area: str)` - Modelo Pydantic para actualizar centros de costo.
- `HolidayAdd(date_str: str)` - Modelo Pydantic para añadir feriados.
- `QueryUpdate(query_id: str, sql_text: str, params: Optional[List[Any]] = None, visual_state: Optional[str] = None)` - Modelo Pydantic para actualizar consultas SQL.
- `JoinDef(table: str, onLeft: str, onRight: str)` - Modelo Pydantic para definir joins en consultas SQL.
- `FilterDef(column: str, operator: str, value: Optional[str] = "", valueType: Optional[str] = "value", compareColumn: Optional[str] = None, offsetValue: Optional[str] = None)` - Modelo Pydantic para definir filtros en consultas SQL.
- `MetricDef(column: str, aggregation: str, format: Optional[str] = "number")` - Modelo Pydantic para definir métricas en consultas SQL.
- `TimeAxisDef(column: str, granularity: str)` - Modelo Pydantic para definir el eje de tiempo en consultas SQL.
- `SecondMetricDef(column: str = "", aggregation: str = "", label: str = "")` - Modelo Pydantic para definir una segunda métrica adicional en consultas SQL.
- `VisualQueryBuilderPayload(baseTable: str, joins: list[JoinDef] = [], filters: list[FilterDef] = [], metric: MetricDef, timeAxis: TimeAxisDef, breakdown: str | None = None, secondMetric: Optional[SecondMetricDef] = None)` - Modelo Pydantic para construir consultas SQL dinámicamente.
- `settings_view(request: Request, db: DBSession, state: AppState = Depends(get_app_state))` - Vista (UI) que renderiza el panel de control de configuraciones SaaS.
- `api_get_settings(state: AppState = Depends(get_app_state))` - Endpoint para obtener configuraciones generales.
- `api_update_setting(update: SettingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Endpoint para actualizar una configuración general.
- `api_upsert_status(update: StatusMappingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Endpoint para actualizar o insertar un estado.
- `api_delete_status(code: str, db: DBSession, state: AppState = Depends(get_app_state))` - Endpoint para eliminar un estado.
- `api_upsert_cost_center(update: CostCenterMappingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Endpoint para actualizar o insertar un centro de costo.
- `api_delete_cost_center(code: str, db: DBSession, state: AppState = Depends(get_app_state))` - Endpoint para eliminar un centro de costo.
- `api_add_holiday(h: HolidayAdd, db: DBSession, state: AppState = Depends(get_app_state))` - Endpoint para añadir un feriado.
- `api_sync_holidays(db: DBSession, state: AppState = Depends(get_app_state))` - Endpoint para sincronizar automáticamente los feriados nacionales (Chile).
- `api_delete_holiday(date_str: str, db: DBSession, state: AppState = Depends(get_app_state))` - Endpoint para eliminar un feriado.
- `api_get_query(query_id: str, db: DBSession, state: AppState = Depends(get_app_state))` - Endpoint para obtener una consulta SQL.
- `api_update_query(update: QueryUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Endpoint para actualizar una consulta SQL.
- `api_get_schema(db: DBSession, state: AppState = Depends(get_app_state))` - Endpoint que retorna el listado de tablas y sus columnas para el editor.
- `api_query_preview(update: QueryUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Endpoint para ejecutar una consulta temporal y retornar datos para previsualización.
- `validate_identifier(name: str, db: Session) -> bool` - Función que valida de manera segura que un identificador (tabla o columna) pertenezca a la lista blanca.
- `api_build_sql(payload: VisualQueryBuilderPayload, db: DBSession, state: AppState = Depends(get_app_state))` - Endpoint para compilar dinámicamente un objeto JSON del constructor visual en SQL parametrizado seguro.

### Interacción con Base de Datos
El archivo interactúa con la base de datos utilizando SQLAlchemy ORM. Las tablas y columnas que se están leyendo o modificando son:
- Tablas: `AppSetting`, `StatusMapping`, `CostCenterMapping`, `Holiday`, `ConfigQuery`
- Columnas: Todas las columnas correspondientes a estas tablas.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencias externas utilizadas:
- SQLAlchemy ORM
- FastAPI
- Pydantic
- Pandas
- SQLite (a través de SQLAlchemy)

El archivo se comunica con otros archivos del proyecto a través de dependencias como `get_session_dep`, `require_admin`, `load_config_to_memory`, `get_setting`, `get_status_mapping`, `get_cost_center_mapping`, `get_holidays`, y `templates`.

