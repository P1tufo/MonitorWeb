## Archivo: ./core/db_config_manager.py (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
Este archivo `db_config_manager.py` es el punto de acceso a la configuración WMS en tiempo de ejecución. Utiliza SQLAlchemy para interactuar con una base de datos PostgreSQL y mantiene una caché en memoria para mejorar el rendimiento.

### Catálogo de Funciones y Clases
- `init_config_db()` - Crea las tablas de configuración SaaS via SQLAlchemy si no existen.
- `seed_initial_config()` - Inserta valores por defecto si las tablas están vacías.

### Interacción con Base de Datos
- Motor: PostgreSQL
- Tablas:
  - `config_queries`
  - `status_mapping`
  - `cost_center_mapping`
  - `app_setting`
  - `holiday`
- Columnas:
  - `config_queries`: `query_id`, `sql_text`, `visual_state`
  - `status_mapping`: `code`, `label`
  - `cost_center_mapping`: `center_code`, `business_area`
  - `app_setting`: `key`, `value`, `type`
  - `holiday`: `date_str`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: `sqlalchemy`, `logging`
- Comunicación con otros archivos del proyecto:
  - `database.py` (para obtener el motor de base de datos y la sesión)
  - `models.py` (para definir las clases ORM)

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `db_config_manager.py` contiene configuraciones de consultas SQL y funciones para cargar estas configuraciones en una sesión de base de datos. También incluye funciones para recuperar diferentes tipos de configuración desde la base de datos.

### Catálogo de Funciones y Clases
- `ConfigQuery(query_id, sql_text, visual_state)` - Define una consulta con un ID único, texto SQL y estado visual.
- `initial_queries` - Lista de consultas iniciales a cargar en la sesión.
- `load_config_to_memory(session=None)` - Carga las configuraciones iniciales en la memoria. Obsoleta y no realiza ninguna acción.
- `_ensure_loaded()` - No hace nada, función auxiliar obsoleta.
- `get_setting(key: str, default: Any = None) -> Any` - Recupera un valor de configuración por clave.
- `get_status_mapping() -> Dict[str, str]` - Devuelve un mapeo de códigos a etiquetas para estados.
- `get_cost_center_mapping() -> Dict[str, str]` - Devuelve un mapeo de códigos de centro de costo a áreas de negocio.
- `get_holidays() -> List[str]` - Devuelve una lista de fechas festivas.
- `get_query(query_id: str) -> str` - Recupera el texto SQL asociado a un ID de consulta. Utiliza la versión visual_state si está disponible, sino devuelve sql_text.
- `get_query_visual_state(query_id: str) -> str` - Recupera el estado visual JSON de una consulta.

### Interacción con Base de Datos
- Motor de base de datos: No especificado en el código.
- Tablas:
  - `ConfigQuery`
  - `AppSetting`
  - `StatusMapping`
  - `CostCenterMapping`
  - `Holiday`
  - `warehouse_tasks`
  - `inventory_movements`
- Columnas:
  - `ConfigQuery`: `query_id`, `sql_text`, `visual_state`
  - `AppSetting`: `key`, `value`
  - `StatusMapping`: `code`, `label`
  - `CostCenterMapping`: `center_code`, `business_area`
  - `Holiday`: `date_str`
  - `warehouse_tasks`: `usuario`, `fecha_conf`, `fe_creac`
  - `inventory_movements`: `tipo_operacion`, `material`, `cmv`, `fe_contab`, `registrado`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas: No se mencionan librerías específicas.
- Comunicación con otros archivos del proyecto:
  - `get_session()` - Se asume que esta función está definida en otro archivo para obtener una sesión de base de datos.

