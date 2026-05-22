## Archivo: ./tests/test_api.py

### Resumen Funcional
Este archivo contiene pruebas unitarias utilizando `pytest` para verificar el funcionamiento de varios endpoints y funcionalidades del sistema. Las pruebas cubren la lectura de un dashboard principal, la obtención de una URL de túnel, la iniciación de un proceso de sincronización, el acceso a una página de analíticas, la generación de consultas SQL para métricas SLA, y la resolución dinámica de áreas de negocio en rutas de auditoría.

### Catálogo de Funciones y Clases
- `test_read_root(auth_client)` - Verifica que el dashboard principal responda con el título correcto.
- `test_get_tunnel_url(auth_client, tmp_path)` - Verifica que el endpoint `/url` devuelva la dirección del túnel ngrok.
- `test_post_sync_endpoint(auth_client)` - Verifica que el endpoint de sincronización inicie el pipeline correctamente.
- `test_analytics_page_access(auth_client)` - Verifica que la página de analíticas sea accesible.
- `test_build_sql_sla_efficiency(auth_client)` - Verifica que el generador de consultas SQL compile correctamente la métrica SLA_EFFICIENCY con desgloses y filtros.
- `test_analytics_sla_route(auth_client, test_db)` - Verifica que la ruta de auditoría SLA resuelva dinámicamente las áreas de negocio y que no muestre 'OTRO'.

### Interacción con Base de Datos
- Motor: No aplica (No hay interacción directa con bases de datos en este archivo).
- Tablas: `outbound_deliveries`
- Columnas: `entrega`, `fecha_carga`, `ubicacion_area`, `area_negocio`, `dias_retraso`

### Estado y Variables Globales
- No aplica (No hay variables globales definidas en este archivo).

### Dependencias y Flujo
- Librerías externas utilizadas: `pytest`, `unittest.mock`.
- Comunicación con otros archivos del proyecto:
  - `core.state.AppState`
  - `routes.sync.TUNNEL_URL_FILE`
  - `routes.sync._run_sync_pipeline`
  - `routes.sync.task_manager`

