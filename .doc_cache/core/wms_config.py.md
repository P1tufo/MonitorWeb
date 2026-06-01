## Archivo: ./core/wms_config.py

### Resumen Funcional
Este archivo contiene la configuración de lógica de negocio y mapeos específicos para el Sistema de Monitoreo de Almacén (WMS). Define funciones para validar la integridad de los mapeos y proporciona soporte para cargar dinámicamente atributos.

### Catálogo de Funciones y Clases
- `validate_wms_maps() -> None` - Valida la integridad de los mapeos definidos.
  - Lanza excepciones específicas: `ValueError`

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
No aplica.

### Caché y Estado
No aplica.

### Lógica de Negocio y Reglas
- **STATUS_MAPPING**: Mapeo de estados. No puede estar vacío.
- **COST_CENTER_MAPPING**: Mapeo de áreas de negocio. No puede estar vacía, y cada valor debe ser no nulo.

### Dependencias y Flujo
- Importa: `get_setting`, `get_status_mapping`, `get_cost_center_mapping`, `get_holidays`, `get_query` desde `db_config_manager`.
- Exporta: `STATUS_MAPPING`, `COST_CENTER_MAPPING`

Flujo de datos:
1. **Entrada**: No aplica.
2. **Procesamiento**: Valida los mapeos y carga dinámicamente atributos.
3. **Salida**: No aplica.

Este archivo es crucial para garantizar la integridad de los mapeos utilizados en el sistema WMS, asegurando que todos los valores necesarios estén presentes y válidos antes de su uso en cualquier parte del sistema.

