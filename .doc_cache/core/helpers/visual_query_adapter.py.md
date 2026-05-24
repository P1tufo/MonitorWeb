## Archivo: ./core/helpers/visual_query_adapter.py

### Resumen Funcional
Este archivo contiene funciones que construyen payloads para consultas visuales, utilizando un esquema definido en `core.schemas`. Cada función genera un objeto `VisualQueryBuilderPayload` con diferentes configuraciones de tablas, filtros y métricas.

### Catálogo de Funciones y Clases
- `build_area_stats_payload(year: str, sla_threshold: int) -> VisualQueryBuilderPayload`: Construye un payload para estadísticas agrupadas por área de negocio.
- `build_sla_stats_payload(year: str, sla_threshold: int) -> VisualQueryBuilderPayload`: Construye un payload para resumen global de SLA.
- `build_dates_counts_payload(year: str) -> VisualQueryBuilderPayload`: Construye un payload para conteo por fechas y área.
- `build_top_materials_payload(year: str) -> VisualQueryBuilderPayload`: Construye un payload para ranking de materiales por área.
- `build_wms_status_payload(year: str) -> VisualQueryBuilderPayload`: Construye un payload para el estado del WMS.

### Interacción con Base de Datos
No aplica. El archivo no realiza ninguna interacción con una base de datos.

### Estado y Variables Globales
No aplica. No se definen variables globales, de sesión o de entorno en este archivo.

### Dependencias y Flujo
- **Librerías Externas**: `logging`
- **Flujo Interno**: Las funciones dependen del módulo `core.schemas` para definir los payloads.

