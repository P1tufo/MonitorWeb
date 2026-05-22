## Archivo: ./core/db_config_manager.py (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
Este archivo `db_config_manager.py` es el administrador de configuraciones dinámicas SaaS. Se encarga de la inicialización, carga y mantenimiento de tablas en una base de datos utilizando SQLAlchemy, así como la inserción de valores por defecto si las tablas están vacías.

### Catálogo de Funciones y Clases
- `init_config_db()` - Crea las tablas de configuración SaaS via SQLAlchemy si no existen.
- `seed_initial_config()` - Inserta los valores por defecto si las tablas están vacías.

### Interacción con Base de Datos
- Motor: SQLAlchemy
- Tablas:
  - `StatusMapping`
  - `CostCenterMapping`
  - `AppSetting`
  - `Holiday`
  - `ConfigQuery`
- Columnas:
  - `StatusMapping.code`, `label`
  - `CostCenterMapping.center_code`, `business_area`
  - `AppSetting.key`, `value`, `type`
  - `Holiday.date_str`
  - `ConfigQuery.query_id`, `sql_text`

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: SQLAlchemy, logging
- Comunicación con otros archivos del proyecto:
  - `database.py` (para obtener el motor de base de datos y la sesión)
  - `models.py` (para definir las clases de modelos)

#### --- PARTE 2 de 2 ---

### Resumen Funcional
El archivo `db_config_manager.py` contiene configuraciones de consultas SQL y funciones para cargar estas configuraciones en una sesión de base de datos. También incluye funciones públicas para obtener diferentes tipos de configuración desde la base de datos.

### Catálogo de Funciones y Clases
- `ConfigQuery(query_id, sql_text, visual_state)` - Define una consulta con un ID único, texto SQL y estado visual.
- `initial_queries` - Lista de instancias de `ConfigQuery`.
- `load_config_to_memory(session=None)` - Carga las consultas iniciales en la sesión de base de datos. Esta función está obsoleta y no realiza ninguna operación.
- `_ensure_loaded()` - Función interna que no hace nada.
- `get_setting(key, default=None)` - Obtiene un valor de configuración basado en una clave, con un valor predeterminado opcional.
- `get_status_mapping()` - Devuelve un mapeo de códigos de estado a etiquetas.
- `get_cost_center_mapping()` - Devuelve un mapeo de códigos de centro de costo a áreas de negocio.
- `get_holidays()` - Devuelve una lista de fechas festivas.
- `get_query(query_id)` - Obtiene el texto SQL de una consulta basada en su ID.

### Interacción con Base de Datos
- Motor: No especificado (se infiere que es SQLAlchemy).
- Tablas:
  - `inventory_movements`
  - `warehouse_tasks`
  - `AppSetting`
  - `StatusMapping`
  - `CostCenterMapping`
  - `Holiday`
- Columnas:
  - `inventory_movements.cmv`, `inventory_movements.fe_contab`, `inventory_movements.material`, `inventory_movements.tipo_operacion`, `inventory_movements.registrado`
  - `warehouse_tasks.usuario`, `warehouse_tasks.fe_creac`, `warehouse_tasks.fecha_conf`
  - `AppSetting.key`, `AppSetting.typed_value()`
  - `StatusMapping.code`, `StatusMapping.label`
  - `CostCenterMapping.center_code`, `CostCenterMapping.business_area`
  - `Holiday.date_str`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas: SQLAlchemy.
- Comunicación con otros archivos del proyecto:
  - No se menciona ninguna comunicación específica entre este archivo y otros.

