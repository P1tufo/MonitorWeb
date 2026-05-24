## Archivo: ./core/db_config_manager.py (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
Este archivo `db_config_manager.py` es el administrador de configuraciones dinámicas SaaS. Se encarga de la inicialización, semillas y carga de configuraciones en memoria para mejorar el rendimiento.

### Catálogo de Funciones y Clases
- `init_config_db()` - Crea las tablas de configuración SaaS via SQLAlchemy si no existen.
- `seed_initial_config()` - Inserta valores por defecto si las tablas están vacías.
- `load_config_to_memory()` - No definida en el fragmento.

### Interacción con Base de Datos
- Motor: SQLAlchemy
- Tablas:
  - `StatusMapping`
  - `CostCenterMapping`
  - `AppSetting`
  - `Holiday`
  - `ConfigQuery`
- Columnas:
  - `config_queries` → `visual_state`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas: SQLAlchemy, logging
- Comunicación con otros archivos del proyecto: No mencionado

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `db_config_manager.py` contiene configuraciones de consultas SQL y funciones para cargar estas configuraciones en una sesión de base de datos. También incluye funciones para recuperar diferentes tipos de configuración desde la base de datos.

### Catálogo de Funciones y Clases
- `ConfigQuery(query_id, sql_text, visual_state)` - Define una consulta con un ID único, texto SQL y estado visual.
- `initial_queries` - Lista de instancias de `ConfigQuery`.
- `load_config_to_memory(session=None)` - Carga las consultas iniciales en la sesión de base de datos. Obsoleta y no hace nada.
- `_ensure_loaded()` - No hace nada, función auxiliar obsoleta.
- `get_setting(key: str, default: Any = None) -> Any` - Recupera un valor de configuración por clave.
- `get_status_mapping() -> Dict[str, str]` - Devuelve un mapeo de códigos a etiquetas para estados.
- `get_cost_center_mapping() -> Dict[str, str]` - Devuelve un mapeo de códigos de centro de costo a áreas de negocio.
- `get_holidays() -> List[str]` - Devuelve una lista de fechas festivas.
- `get_query(query_id: str) -> str` - Recupera el texto SQL asociado a un ID de consulta. Obsoleta, usar `get_query_visual_state()` en su lugar.
- `get_query_visual_state(query_id: str) -> str` - Recupera el estado visual JSON de una consulta.

### Interacción con Base de Datos
- Motor: No especificado (se infiere que es SQLAlchemy basado en la sintaxis).
- Tablas:
  - `ConfigQuery`
  - `AppSetting`
  - `StatusMapping`
  - `CostCenterMapping`
  - `Holiday`
- Columnas:
  - `ConfigQuery.query_id`, `sql_text`, `visual_state`
  - `AppSetting.key`, `typed_value()`
  - `StatusMapping.code`, `label`
  - `CostCenterMapping.center_code`, `business_area`
  - `Holiday.date_str`

### Estado y Variables Globales
- No aplica.

### Dependencias y Flujo
- Librerías externas: SQLAlchemy.
- Comunicación con otros archivos del proyecto:
  - `get_session()` - Se asume que esta función está definida en otro archivo para obtener una sesión de base de datos.

