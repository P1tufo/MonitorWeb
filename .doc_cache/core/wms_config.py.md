## Archivo: ./core/wms_config.py

### Resumen Funcional
Este archivo contiene la configuración y validación de los mapeos utilizados en el sistema de monitoreo de almacén (WMS). Define funciones para obtener mapeos como STATUS_MAPPING y COST_CENTER_MAPPING, y valida su integridad.

### Catálogo de Funciones y Clases
- `validate_wms_maps()` - Valida la integridad de los mapeos definidos.
- `__getattr__(name: str) -> Any` - Soporte para carga dinámica de atributos.

### Interacción con Base de Datos
Ninguna. No hay consultas SQL ni interacciones directas con una base de datos.

### Estado y Variables Globales
No se utilizan variables globales, de sesión o diccionarios quemados en el código que almacenen estado crítico.

### Dependencias y Flujo
- **Dependencias**: 
  - `get_cost_center_mapping()`, `get_holidays()`, `get_setting()`, `get_status_mapping()` (de `db_config_manager.py`).
  
- **Flujo de Datos**:
  - El archivo importa funciones desde `db_config_manager.py`.
  - No hay archivos que importen a este archivo.

Este archivo se encarga de la configuración y validación de mapeos utilizados en el sistema WMS, asegurando que los datos necesarios estén correctamente definidos y no vacíos.

