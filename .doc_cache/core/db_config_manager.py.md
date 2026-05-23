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
- `initial_queries` - Lista de consultas iniciales a cargar en la sesión.
- `load_config_to_memory(session=None)` - Carga las configuraciones iniciales en la sesión. Esta función está obsoleta y no realiza ninguna operación.
- `_ensure_loaded()` - No hace nada, es una función auxiliar que no se utiliza.
- `get_setting(key: str, default: Any = None) -> Any` - Recupera un valor de configuración basado en su clave.
- `get_status_mapping() -> Dict[str, str]` - Devuelve un mapeo de códigos de estado a etiquetas.
- `get_cost_center_mapping() -> Dict[str, str]` - Devuelve un mapeo de códigos de centro de costo a áreas de negocio.
- `get_holidays() -> List[str]` - Devuelve una lista de fechas festivas.
- `get_query(query_id: str) -> str` - Recupera el texto SQL asociado a un ID de consulta. Esta función es obsoleta y se recomienda usar `get_query_visual_state()` en su lugar.
- `get_query_visual_state(query_id: str) -> str` - Recupera el estado visual JSON de una consulta.

### Interacción con Base de Datos
- Motor de base de datos: No especificado.
- Tablas:
  - `inventory_movements`
  - `warehouse_tasks`
  - `AppSetting`
  - `StatusMapping`
  - `CostCenterMapping`
  - `Holiday`
- Columnas:
  - `inventory_movements.cmv`, `inventory_movements.fe_contab`, `inventory_movements.material`, `inventory_movements.tipo_operacion`, `inventory_movements.registrado`
  - `warehouse_tasks.usuario`, `warehouse_tasks.fecha_conf`, `warehouse_tasks.fe_creac`
  - `AppSetting.key`, `AppSetting.typed_value()`
  - `StatusMapping.code`, `StatusMapping.label`
  - `CostCenterMapping.center_code`, `CostCenterMapping.business_area`
  - `Holiday.date_str`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas: No especificado.
- Comunicación con otros archivos del proyecto:
  - `get_session()` - Se utiliza para obtener una sesión de base de datos.

