## Archivo: ./core/models.py

### Resumen Funcional
Este archivo define modelos ORM SQLAlchemy para el esquema de configuración SaaS, incluyendo mapeos de estados WMS, centros de costo, parámetros globales, feriados y consultas SQL gestionadas via UI.

### Catálogo de Funciones y Clases
- `StatusMapping(code: str, label: str)` - Mapea códigos internos del WMS a etiquetas legibles por humanos.
- `CostCenterMapping(center_code: str, business_area: str)` - Asocia un código de centro de costo del WMS con un Área de Negocio.
- `AppSetting(key: str, value: str, type: str = "str")` - Parámetros de comportamiento del sistema.
  - `typed_value()` - Retorna el valor con el tipo Python correcto.
- `Holiday(date_str: str)` - Días no hábiles para el cálculo de SLA (días de retraso).
- `ConfigQuery(query_id: str, sql_text: str, visual_state: str = None)` - Almacena queries SQL nombradas para el dominio de inventario/entregas.

### Interacción con Base de Datos
- Motor: SQLAlchemy
- Tablas:
  - `config_status_mapping`
  - `config_cost_center_mapping`
  - `app_settings`
  - `config_holidays`
  - `config_queries`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
Dependencia única: `sqlalchemy`

