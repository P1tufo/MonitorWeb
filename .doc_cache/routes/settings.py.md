## Archivo: ./routes/settings.py

### Resumen Funcional
El archivo `settings.py` proporciona una API para la gestión dinámica de configuraciones SaaS en un sistema de monitoreo de almacén (WMS). Permite actualizar y consultar configuraciones, estados de mapeo, centros de costo, feriados y consultas SQL.

### Catálogo de Funciones y Clases
- `invalidate_caches(db: Session)` - Limpia el caché global en memoria y elimina todos los snapshots de base de datos.
- `settings_view(request: Request, db: DBSession, state: AppState = Depends(get_app_state))` - Renderiza el panel de control de configuraciones SaaS.
- `api_get_settings(state: AppState = Depends(get_app_state))` - Retorna las configuraciones generales.
- `api_update_setting(update: SettingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Actualiza una configuración específica.
- `api_upsert_status(update: StatusMappingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Inserta o actualiza un estado de mapeo.
- `api_delete_status(code: str, db: DBSession, state: AppState = Depends(get_app_state))` - Elimina un estado de mapeo.
- `api_upsert_cost_center(update: CostCenterMappingUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Inserta o actualiza un centro de costo.
- `api_delete_cost_center(code: str, db: DBSession, state: AppState = Depends(get_app_state))` - Elimina un centro de costo.
- `api_add_holiday(h: HolidayAdd, db: DBSession, state: AppState = Depends(get_app_state))` - Añade un feriado.
- `api_sync_holidays(db: DBSession, state: AppState = Depends(get_app_state))` - Sincroniza automáticamente los feriados nacionales (Chile).
- `api_delete_holiday(date_str: str, db: DBSession, state: AppState = Depends(get_app_state))` - Elimina un feriado.
- `api_get_query(query_id: str, db: DBSession, state: AppState = Depends(get_app_state))` - Retorna el estado visual de una consulta del Analytics Studio.
- `api_update_query(update: QueryUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Persiste el estado visual de una consulta.
- `api_get_schema(db: DBSession, state: AppState = Depends(get_app_state))` - Retorna el catálogo semántico de datos para el editor.
- `api_preview_table(dataset_id: str, db: DBSession, state: AppState = Depends(get_app_state))` - Previsualiza una tabla.
- `api_query_preview(update: QueryUpdate, db: DBSession, state: AppState = Depends(get_app_state))` - Ejecuta una consulta temporal y retorna datos para previsualización.
- `api_build_sql(payload: VisualQueryBuilderPayload, db: DBSession, state: AppState = Depends(get_app_state))` - Compila el estado visual del constructor en SQL parametrizado seguro.
- `api_export_missing_orders(db: DBSession, state: AppState = Depends(get_app_state))` - Exporta órdenes sin ceco a un archivo Excel.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `analytics_snapshots`
  - `status_mapping`
  - `cost_center_mapping`
  - `holiday`
  - `app_setting`
  - `config_query`
- Columnas:
  - `analytics_snapshots`: Todas las columnas de la tabla.
  - `status_mapping`: `code`, `label`.
  - `cost_center_mapping`: `center_code`, `business_area`.
  - `holiday`: `date_str`.
  - `app_setting`: `key`, `value`.
  - `config_query`: `query_id`, `visual_state`.

### Estado y Variables Globales
- No se detectan variables globales, de sesión o de entorno.

### Dependencias y Flujo
- **Dependencias Externas**: FastAPI, SQLAlchemy, Pandas.
- **Archivos del Proyecto que Importa**:
  - `core.auth.require_admin`
  - `core.database.get_session_dep`
  - `core.models.StatusMapping`, `CostCenterMapping`, `AppSetting`, `Holiday`, `ConfigQuery`
  - `core.db_config_manager.load_config_to_memory`, `get_setting`, `get_status_mapping`, `get_cost_center_mapping`, `get_holidays`
  - `core.app_instance.templates`
  - `core.utils.sanitize_for_json`
  - `core.state.AppState`, `get_app_state`
- **Archivos del Proyecto que Son Importados por Este**:
  - No se detectan archivos que importen a este archivo.
- **Flujo de Datos**: El flujo de datos pasa a través de la API, interactúa con la base de datos para leer y escribir datos, y devuelve respuestas al cliente.

