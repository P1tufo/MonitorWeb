## Archivo: ./core/db_config_manager.py

### Resumen Funcional
Este archivo gestiona la configuración dinámica del Sistema de Monitoreo de Almacén (WMS) en tiempo de ejecución, utilizando SQLAlchemy para interactuar con una base de datos SQLite. Incluye funciones para inicializar la base de datos, poblarla con valores por defecto y cargar la configuración en caché para un acceso rápido.

### Catálogo de Funciones y Clases
- `init_config_db()` - Crea las tablas de configuración SaaS via SQLAlchemy si no existen.
- `seed_initial_config()` - Inserta los valores por defecto si las tablas están vacías.
- `load_config_to_memory(session=None)` - Carga la configuración en caché (deprecated).
- `_ensure_loaded()` - No-op para compatibilidad hacia atrás.
- `get_setting(key: str, default: Any = None) -> Any` - Recupera un valor de configuración por clave.
- `get_status_mapping() -> Dict[str, str]` - Devuelve el mapeo de estados en formato diccionario.
- `get_cost_center_mapping() -> Dict[str, str]` - Devuelve el mapeo de centros de costo en formato diccionario.
- `get_holidays() -> List[str]` - Devuelve la lista de feriados.
- `get_query_visual_state(query_id: str) -> str` - Recupera el visual_state JSON de una consulta.
- `get_user_groups() -> Dict[str, List[str]]` - Devuelve un diccionario de grupos de usuarios.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - `app_setting`
  - `config_query`
  - `cost_center_mapping`
  - `holiday`
  - `status_mapping`
  - `user_group`
- Columnas:
  - `app_setting`: `key`, `value`, `type`
  - `config_query`: `query_id`, `visual_state`
  - `cost_center_mapping`: `center_code`, `business_area`
  - `holiday`: `date_str`
  - `status_mapping`: `code`, `label`
  - `user_group`: `group_name`, `users`

### Estado y Variables Globales
- No hay variables globales explícitas.

### Dependencias y Flujo
- Importa librerías internas del proyecto (`database.py`, `models.py`).
- No se importan archivos del proyecto que lo consuman.
- El flujo de datos es desde el archivo hacia la base de datos para lectura y escritura.

