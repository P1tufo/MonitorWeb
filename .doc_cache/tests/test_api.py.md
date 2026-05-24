## Archivo: ./tests/test_api.py

### Resumen Funcional
El archivo `test_api.py` contiene pruebas unitarias para verificar la funcionalidad de varios endpoints de una API, incluyendo el inicio de sesión, obtención de URLs de túnel, sincronización de datos, acceso a páginas de análisis y generación de consultas SQL.

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
- Motor: No aplica (No hay interacción directa con bases de datos en este archivo).
- Tablas: No aplica.
- Columnas: No aplica.

### Estado y Variables Globales
- No aplica (No se definen variables globales).

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pytest`
  - `unittest.mock`
  - `fastapi.testclient.TestClient` (a través de `auth_client`)
- Comunicación con otros archivos del proyecto:
  - `core.state.AppState`
  - `routes.sync.TUNNEL_URL_FILE`
  - `routes.sync._run_sync_pipeline`
  - `routes.sync.task_manager`

