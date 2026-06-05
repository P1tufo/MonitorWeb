## Archivo: ./core/wms_config.py

### Resumen Funcional
Este archivo contiene la configuración y lógica de negocio para el mapeo WMS (SaaS Dinámico). Define funciones para validar los mapeos de estado, centro de costo y feriados. También proporciona soporte para cargar dinámicamente atributos como `STATUS_MAPPING` y `COST_CENTER_MAPPING`.

### Catálogo de Funciones y Clases
- `validate_wms_maps()` - Valida la integridad de los mapeos definidos.
- `__getattr__(name: str) -> Any` - Soporte para carga dinámica de atributos.

### Interacción con Base de Datos
Ninguna. No se realiza ninguna interacción directa con una base de datos en este archivo.

### Estado y Variables Globales
No hay variables globales, de sesión o de entorno definidas en este archivo.

### Dependencias y Flujo
- **Dependencias**: 
  - `get_setting`, `get_status_mapping`, `get_cost_center_mapping`, `get_holidays` (de `db_config_manager.py`)
  
- **Flujo de Datos**:
  - Este archivo es consumido por otros archivos que necesiten acceso a los mapeos WMS y la configuración dinámica.
  - Los atributos como `STATUS_MAPPING` y `COST_CENTER_MAPPING` se cargan dinámicamente cuando son accedidos.

Este archivo es crucial para mantener la integridad de los mapeos WMS y proporcionar acceso a estos mapeos de manera dinámica en el sistema.

