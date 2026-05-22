## Archivo: ./core/wms_config.py

### Resumen Funcional
Este archivo contiene la configuración y las funciones de validación para los mapeos utilizados en la lógica de negocio del sistema WMS (SaaS Dinámico). Define funciones para cargar y validar mapeos como STATUS_MAPPING y COST_CENTER_MAPPING, así como soporte para carga dinámica de atributos.

### Catálogo de Funciones y Clases
- `validate_wms_maps()` - Valida la integridad de los mapeos definidos.
- `__getattr__(name: str) -> Any` - Soporta carga dinámica de atributos.

### Interacción con Base de Datos
No aplica

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencia directa:
- `get_setting`, `get_status_mapping`, `get_cost_center_mapping`, `get_holidays`, `get_query` - Funciones desde el módulo `db_config_manager`.

