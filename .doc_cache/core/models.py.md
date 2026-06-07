## Archivo: ./core/models.py

### Resumen Funcional
Este archivo define los modelos ORM SQLAlchemy para las tablas de configuración dinámica del sistema WMS, incluyendo mapeos de estados, centros de costo, parámetros globales, feriados y consultas SQL gestionadas via UI.

### Catálogo de Funciones y Clases
- `StatusMapping(code: str, label: str)` - Representa el mapeo de códigos internos del WMS a etiquetas legibles.
- `CostCenterMapping(center_code: str, business_area: str)` - Asocia un código de centro de costo con un Área de Negocio.
- `AppSetting(key: str, value: str, type: str = "str")` - Almacena parámetros de comportamiento del sistema con deserialización correcta.
- `Holiday(date_str: str)` - Representa los días no hábiles para el cálculo de SLA.
- `ConfigQuery(query_id: str, visual_state: str)` - Almacena el estado visual (JSON) de las consultas del Analytics Studio.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `config_status_mapping`
  - `config_cost_center_mapping`
  - `app_settings`
  - `config_holidays`
  - `config_queries`

### Estado y Variables Globales
Ninguna

### Dependencias y Flujo
- Importa de `sqlalchemy` para definir los tipos de datos y ORM.
- Importa de `.database.Base` para la herencia de modelos.
- No se importan archivos del proyecto que lo consuman.

