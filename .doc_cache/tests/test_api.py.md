## Archivo: ./tests/test_api.py

### Resumen Funcional
El archivo `test_api.py` contiene pruebas unitarias para endpoints de una API de un sistema de monitoreo de almacén (WMS) construido con FastAPI, SQLAlchemy y SQLite. Las pruebas cubren la funcionalidad del dashboard principal, el endpoint de sincronización, la página de analíticas, la generación de consultas SQL, y la protección contra inyección SQL.

### Catálogo de Funciones y Clases
- `test_read_root(auth_client)` - Verifica que el dashboard principal responda con el título correcto.
- `test_get_tunnel_url(auth_client, tmp_path)` - Verifica que el endpoint `/url` devuelva la dirección del túnel ngrok.
- `test_post_sync_endpoint(auth_client)` - Verifica que el endpoint de sincronización inicie el pipeline correctamente.
- `test_analytics_page_access(auth_client)` - Verifica que la página de analíticas sea accesible.
- `test_build_sql_sla_efficiency(auth_client)` - Verifica que el generador de consultas SQL compile correctamente la métrica SLA_EFFICIENCY con desgloses y filtros.
- `test_analytics_sla_route(auth_client, test_db)` - Verifica que la ruta de auditoría SLA resuelva dinámicamente las áreas de negocio y que no muestre 'OTRO'.
- `test_api_query_preview_returns_json_and_no_sql(auth_client)` - Verifica el contrato JSON in/out para preview y la ausencia de texto SQL.
- `test_api_settings_query_rejects_raw_sql(auth_client)` - Verifica protección contra inyección y que el endpoint solo acepte visual_state.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `outbound_deliveries`
- Columnas:
  - `entrega`
  - `fecha_carga`
  - `centro_costo`
  - `area_negocio`
  - `dias_retraso`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- Librerías externas: `pytest`, `unittest.mock`.
- Archivos del proyecto que este archivo importa:
  - `core.state.AppState`
  - `routes.sync.TUNNEL_URL_FILE`
  - `routes.sync._run_sync_pipeline`
  - `routes.sync.task_manager`
- Archivos del proyecto que importan a este archivo: Ninguno.
- Flujo de datos: El archivo consume pruebas unitarias y dependencias para verificar la funcionalidad de los endpoints de la API.

