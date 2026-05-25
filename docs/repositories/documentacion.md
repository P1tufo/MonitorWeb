# Documentación Técnica - Directorio: repositories
Compilado el: 2026-05-24 14:59:18
Modelo: qwen2.5-coder:7b | Separado por Carpetas

---

## Archivo: ./repositories/__init__.py

### Resumen Funcional
Este archivo es el punto de entrada para la configuración y la inyección de dependencias de los repositorios en una aplicación FastAPI que utiliza SQLite como base de datos.

### Catálogo de Funciones y Clases
- `get_db()` - Establece una conexión a la base de datos SQLite y la devuelve. La conexión se cierra automáticamente al finalizar el contexto.
- `get_deliveries_repo(conn: sqlite3.Connection = Depends(get_db))` - Crea e inicializa un repositorio para operaciones relacionadas con entregas.
- `get_inventory_repo(conn: sqlite3.Connection = Depends(get_db))` - Crea e inicializa un repositorio para operaciones relacionadas con el inventario.
- `get_tasks_repo(conn: sqlite3.Connection = Depends(get_db))` - Crea e inicializa un repositorio para operaciones relacionadas con tareas.

### Interacción con Base de Datos
- Motor de base de datos: SQLite
- Tablas y Columnas: No aplica (se asume que las tablas y columnas están definidas en los repositorios `DeliveriesRepository`, `InventoryRepository` y `TasksRepository`)
- Consultas SQL Crudas o ORM: Se utiliza el módulo `sqlite3` para interactuar con la base de datos.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sqlite3`: Para interactuar con la base de datos SQLite.
  - `fastapi`: Para manejar las dependencias en FastAPI.
- Comunicación con otros archivos del proyecto:
  - Importa clases y funciones desde los módulos `base.py`, `deliveries.py`, `inventory.py` y `tasks.py`.


---

## Archivo: ./repositories/base.py

### Resumen Funcional
La clase `BaseRepository` proporciona una estructura base para interactuar con bases de datos mediante SQLAlchemy. Define métodos para obtener consultas SQL y verificar el estado visual de las mismas.

### Catálogo de Funciones y Clases
- `__init__(self, session: Session)` - Inicializa la instancia con una sesión de SQLAlchemy.
- `_sql(self, query_id: str, fallback: str) -> str` - Obtiene un SQL desde la base de datos de configuración o devuelve un fallback hardcodeado si no existe.
- `_has_visual_state(self, query_id: str) -> bool` - Verifica si una consulta tiene un estado visual JSON almacenado.

### Interacción con Base de Datos
- Motor: SQLAlchemy
- Tablas: `config_queries`
- Columnas: `query_id`, `sql_text`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `sqlalchemy.orm.Session`
  - `core.wms_config.get_query`
  - `core.db_config_manager.get_query_visual_state`
- Comunicación con otros archivos del proyecto:
  - `core/query_engine.build_sql_from_payload()` (mencionado en la documentación, pero no implementado)


---

## Archivo: ./repositories/deliveries.py

### Resumen Funcional
Este archivo define un repositorio para el dominio de Entregas (outbound_deliveries), que utiliza consultas SQL personalizadas y una expresión segura para determinar el área empresarial.

### Catálogo de Funciones y Clases
- `DeliveriesRepository(BaseRepository)` - Repositorio para el dominio de Entregas.
  - `_sql(query_id: str, fallback: str) -> str` - Obtiene SQL desde config_queries con fallback explícito.
  - `_get_sla_threshold() -> int` - Obtiene el umbral de SLA (Service Level Agreement).

### Interacción con Base de Datos
- Motor de BD: No especificado.
- Tablas y Columnas: No aplica.

### Estado y Variables Globales
- `AREA_EXPR` - Expresión segura para determinar el área empresarial, definida como una constante de clase.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas`
  - `sqlalchemy`
- Flujo hacia otros archivos del proyecto: No aplica.


---

## Archivo: ./repositories/inventory.py

### Resumen Funcional
El archivo `inventory.py` contiene una clase `InventoryRepository` que se encarga de interactuar con la base de datos para gestionar los movimientos del inventario. La clase proporciona métodos para obtener configuraciones específicas y verificar la existencia de una tabla en la base de datos.

### Catálogo de Funciones y Clases
- `get_cmv_prod()` - Devuelve el valor de la configuración "CMV_PROD".
- `get_cmv_mant()` - Devuelve el valor de la configuración "CMV_MANT".
- `get_cmv_consumos()` - Devuelve una tupla con los valores de las configuraciones "CMV_PROD" y "CMV_MANT".
- `get_cmv_reversas()` - Devuelve una tupla con los valores de la configuración "CMV_REVERSAS", separados por comas.
- `check_table_exists()` - Verifica si la tabla 'inventory_movements' existe en la base de datos.

### Interacción con Base de Datos
- Motor: SQLite (deducido del uso de `sqlite_master`).
- Tablas: `inventory_movements`.
- Consulta SQL: `SELECT name FROM sqlite_master WHERE type='table' AND name='inventory_movements'`.

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `pandas` (importado como `pd`)
  - `sqlalchemy` (importado para el uso de `text`)
  - `typing` (para definir tipos)
- Depende de la clase base `BaseRepository`.
- Utiliza funciones y configuraciones definidas en `core.wms_config`.


---

## Archivo: ./repositories/tasks.py

### Resumen Funcional
Este archivo contiene un repositorio de datos para el dominio de tareas de almacén, que proporciona métodos para obtener resúmenes y tendencias de las tareas, así como detalles específicos sobre las tareas.

### Catálogo de Funciones y Clases
- `get_tasks_summary()` - Obtiene un resumen de las tareas agrupadas por código y nombre.
- `get_tasks_trend()` - Obtiene una tendencia diaria de creación y confirmación de tareas.
- `get_tasks_by_user()` - Obtiene el número de tareas creadas y confirmadas por usuario.
- `get_tasks_by_type_dest()` - Obtiene un resumen de las tareas agrupadas por tipo de destino.
- `get_recent_tasks()` - Obtiene las tareas recientes que no han sido confirmadas.
- `get_non_palletized_movements()` - Obtiene los movimientos no paletizados más recientes.
- `get_non_palletized_count()` - Cuenta el número de movimientos no paletizados.
- `get_non_palletized_summary()` - Obtiene un resumen de los movimientos no paletizados, incluyendo detalles sobre la fecha más antigua y más reciente.

### Interacción con Base de Datos
- Motor: PostgreSQL (deducido del uso de SQLAlchemy).
- Tablas:
  - `warehouse_tasks`
  - `lx02_pendientes`
  - `inventory_movements`
- Columnas:
  - `cl_mov`, `clase_mov`, `COUNT(*)`, `SUM(ctd_teor_dsd)`, `fe_creac`, `fecha_conf`, `usuario`, `material`, `texto_breve_material`, `ubic_proc`, `ubic_dest`, `hora`, `otcuanto`, `pos`, `denominacion`, `stock_disp`, `alm`, `ce`, `doc_mat`, `cmv`, `usuario_conf`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas: `pandas`, `sqlalchemy`.
- No se comunica con otros archivos del proyecto.


---

