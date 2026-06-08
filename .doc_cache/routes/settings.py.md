## Archivo: ./routes/settings.py

### Resumen Funcional
El archivo `settings.py` contiene endpoints para la gestión dinámica de configuraciones en un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Permite actualizar y gestionar configuraciones generales, grupos de usuarios, feriados, estados, costos centrales y consultas SQL.

### Catálogo de Funciones y Clases
- `invalidate_caches(db: Session)` - Limpia el caché global en memoria y elimina todos los snapshots de base de datos.
- `settings_view(request: Request, db: DBSession, repo: ProductivityRepository = Depends(get_productivity_repo))` - Renderiza el panel de control de configuraciones SaaS.
- `api_get_settings()` - Retorna las configuraciones generales.
- `api_update_setting(update: SettingUpdate, db: DBSession)` - Actualiza una configuración general.
- `api_upsert_status(update: StatusMappingUpdate, db: DBSession)` - Inserta o actualiza un estado.
- `api_delete_status(code: str, db: DBSession)` - Elimina un estado.
- `api_upsert_cost_center(update: CostCenterMappingUpdate, db: DBSession)` - Inserta o actualiza un centro de costo.
- `api_delete_cost_center(code: str, db: DBSession)` - Elimina un centro de costo.
- `api_upsert_user_group(update: UserGroupAdd, db: DBSession)` - Inserta o actualiza un grupo de usuarios.
- `api_delete_user_group(group_name: str, db: DBSession)` - Elimina un grupo de usuarios.
- `api_add_holiday(h: HolidayAdd, db: DBSession)` - Añade un feriado.
- `api_sync_holidays(db: DBSession)` - Sincroniza automáticamente los feriados nacionales (Chile).
- `api_delete_holiday(date_str: str, db: DBSession)` - Elimina un feriado.
- `api_get_query(query_id: str, db: DBSession)` - Retorna el estado visual de una consulta del Analytics Studio.
- `api_update_query(update: QueryUpdate, db: DBSession, cache: CacheManager = Depends(get_cache_manager))` - Persiste el estado visual de una consulta.
- `api_get_schema(db: DBSession)` - Retorna el catálogo semántico de datos para el editor.
- `api_preview_table(dataset_id: str, db: DBSession)` - Previsualiza una tabla.
- `api_query_preview(update: QueryUpdate, db: DBSession)` - Ejecuta una consulta temporal y retorna datos para previsualización.
- `api_build_sql(payload: VisualQueryBuilderPayload, db: DBSession)` - Compila el estado visual del constructor en SQL parametrizado seguro.
- `api_export_missing_orders(db: DBSession)` - Exporta órdenes sin ceco a un archivo Excel.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - `analytics_snapshots` (DELETE)
  - `app_settings`
  - `cost_center_mapping`
  - `holiday`
  - `status_mapping`
  - `user_group`

### Estado y Variables Globales
- No hay variables globales explícitas.

### Dependencias y Flujo
- **Dependencias Externas:** FastAPI, SQLAlchemy, Pandas, Holidays (librería de feriados)
- **Archivos del Proyecto que Importan a este Archivo:**
  - `core.auth.require_admin`
  - `core.database.get_session_dep`
  - `core.db_config_manager.*`
  - `core.models.*`
  - `core.state.CacheManager`
  - `core.utils.sanitize_for_json`
- **Archivos del Proyecto que Este Archivo Importa:**
  - `routes/settings.py` (se importa a sí mismo)
  - `repositories.get_productivity_repo`
  - `core.schemas.*`
  - `core.query_engine.build_sql_from_payload`

El flujo de datos es principalmente entre el endpoint, la base de datos y los modelos de datos.

