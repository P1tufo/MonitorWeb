## Archivo: ./core/db_config_manager.py

### Resumen Funcional
Este archivo `db_config_manager.py` es el administrador de configuraciones dinámicas SaaS para un sistema de monitoreo de almacén (WMS). Se encarga de la inicialización, carga y acceso a las configuraciones almacenadas en una base de datos SQLite utilizando SQLAlchemy. Ofrece funciones públicas para obtener mapeos de estados, centros de costo, configuraciones generales y consultas SQL.

### Catálogo de Funciones y Clases
- `init_config_db()` - Crea las tablas de configuración SaaS via SQLAlchemy si no existen.
- `seed_initial_config()` - Inserta los valores por defecto si las tablas están vacías.
- `load_config_to_memory(session=None)` - Carga en caché las configuraciones desde la BD (deprecated).
- `_ensure_loaded()` - No-op para compatibilidad hacia atrás.
- `get_setting(key: str, default: Any = None) -> Any` - Recupera el valor de una configuración por clave.
- `get_status_mapping() -> Dict[str, str]` - Devuelve un mapeo de códigos de estado a etiquetas.
- `get_cost_center_mapping() -> Dict[str, str]` - Devuelve un mapeo de códigos de centro de costo a áreas de negocio.
- `get_holidays() -> List[str]` - Devuelve una lista de fechas festivas.
- `get_query_visual_state(query_id: str) -> str` - Recupera el visual_state JSON de una consulta.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - `app_setting`
  - `config_query`
  - `cost_center_mapping`
  - `holiday`
  - `status_mapping`
- Columnas:
  - `app_setting`: `key`, `value`, `type`
  - `config_query`: `query_id`, `visual_state`
  - `cost_center_mapping`: `center_code`, `business_area`
  - `holiday`: `date_str`
  - `status_mapping`: `code`, `label`

### Estado y Variables Globales
- No hay variables globales, de sesión o de entorno explícitas.

### Dependencias y Flujo
- Importa: `logging`, `typing`, `sqlalchemy`, `fastapi`, `sqlalchemy.orm`
- Exporta: Todas las funciones públicas mencionadas.
- No se importan ni se exportan archivos del proyecto adicionalmente.

