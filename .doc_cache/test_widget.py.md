## Archivo: ./test_widget.py

### Resumen Funcional
El archivo `test_widget.py` realiza una consulta SQL a partir de un payload JSON, construye la consulta utilizando el motor de consultas y luego ejecuta la consulta para obtener categorías únicas.

### Catálogo de Funciones y Clases
- `get_session()` - Obtiene una sesión de base de datos.
- `ConfigQuery.filter_by(query_id='vl_sla_area_monthly_trend').first()` - Filtra y obtiene el primer registro de la tabla `ConfigQuery` con el ID especificado.
- `json.loads(q.visual_state)` - Convierte el JSON almacenado en `visual_state` a un diccionario.
- `VisualQueryBuilderPayload(**vs_dict)` - Crea una instancia de `VisualQueryBuilderPayload` a partir del diccionario.
- `build_sql_from_payload(payload, session)` - Construye la consulta SQL y los parámetros a partir del payload y la sesión.
- `_build_unified_where('', 'ASERRADERO', '', '', None)` - Construye una cláusula WHERE unificada.
- `pd.read_sql(text(sql), session.connection(), params=params_dict)['categoria'].unique()` - Ejecuta la consulta SQL y obtiene las categorías únicas.

### Interacción con Base de Datos
- Motor: No especificado (se infiere que es SQLAlchemy).
- Tablas: `ConfigQuery`
- Columnas: `query_id`, `visual_state`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `json` - Para manejar JSON.
  - `pandas` - Para procesar datos.
  - `sqlalchemy` - Para interactuar con la base de datos.
- Comunicación con otros archivos del proyecto:
  - `core.database.get_session()` - Obtiene una sesión de base de datos.
  - `core.models.ConfigQuery` - Define el modelo para la tabla `ConfigQuery`.
  - `core.schemas.VisualQueryBuilderPayload` - Define el esquema para el payload.
  - `core.query_engine.build_sql_from_payload(payload, session)` - Construye la consulta SQL y los parámetros.
  - `routes.filters._build_unified_where('', 'ASERRADERO', '', '', None)` - Construye una cláusula WHERE unificada.
  - `repositories.deliveries.DeliveriesRepository.AREA_EXPR` - Accede a una expresión definida en el repositorio de entregas.

