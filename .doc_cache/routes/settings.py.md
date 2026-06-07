## Archivo: ./routes/settings.py

### Resumen Funcional
El archivo `settings.py` contiene endpoints para la gestión dinámica de configuraciones SaaS en un sistema de monitoreo de almacén (WMS). Utiliza SQLAlchemy ORM para todas las operaciones de escritura y FastAPI para crear una API RESTful.

### Catálogo de Funciones y Clases
- `invalidate_caches(db: Session)` - Limpia el caché global en memoria y elimina todos los snapshots de base de datos.
- `settings_view(request: Request, db: DBSession)` - Renderiza el panel de control de configuraciones SaaS.
- `api_get_settings()` - Retorna las configuraciones generales.
- `api_update_setting(update: SettingUpdate, db: DBSession)` - Actualiza una configuración específica.
- `api_upsert_status(update: StatusMappingUpdate, db: DBSession)` - Inserta o actualiza un mapeo de estado.
- `api_delete_status(code: str, db: DBSession)` - Elimina un mapeo de estado.
- `api_upsert_cost_center(update: CostCenterMappingUpdate, db: DBSession)` - Inserta o actualiza un centro de costo.
- `api_delete_cost_center(code: str, db: DBSession)` - Elimina un centro de costo.
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
- Motor: SQLite
- Tablas:
  - `analytics_snapshots`
- Columnas:
  - `id` (de `analytics_snapshots`)
- Consultas SQL crudas o llamadas a ORM:
  - `DELETE FROM analytics_snapshots`

### Estado y Variables Globales
- No hay variables globales, de sesión, de entorno o diccionarios quemados en código que almacenen estado crítico.

### Dependencias y Flujo
- Librerías externas: `fastapi`, `sqlalchemy`, `pydantic`, `pandas`, `holidays`, `openpyxl`
- Archivos del proyecto que este archivo importa:
  - `core.app_instance`
  - `core.auth`
  - `core.database`
  - `core.db_config_manager`
  - `core.models`
  - `core.state`
  - `core.utils`
  - `core.schemas`
  - `core.semantic_layer`
  - `core.query_engine`
- Archivos del proyecto que importan a este archivo:
  - Ninguno
- Flujo de datos: El archivo es un endpoint de FastAPI que consume y produce datos para la gestión de configuraciones SaaS.

