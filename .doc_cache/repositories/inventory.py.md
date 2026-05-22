## Archivo: ./repositories/inventory.py

### Resumen Funcional
El archivo `inventory.py` contiene una clase `InventoryRepository` que proporciona métodos para obtener estadísticas y datos de inventario desde una base de datos SQLite. Los métodos incluyen consultas para volumen, área, materiales consumidos, usuarios activos, tendencias temporales, días hábiles y tipos de material.

### Catálogo de Funciones y Clases
- `InventoryRepository(BaseRepository)` - Repositorio para el dominio de Inventario (ex-Movimientos).
  - `get_cmv_prod()` - Devuelve el valor de la configuración "CMV_PROD".
  - `get_cmv_mant()` - Devuelve el valor de la configuración "CMV_MANT".
  - `get_cmv_consumos()` - Devuelve una tupla con los valores de "CMV_PROD" y "CMV_MANT".
  - `get_cmv_reversas()` - Devuelve una tupla con los valores de "CMV_REVERSAS".
  - `check_table_exists()` - Verifica si la tabla 'inventory_movements' existe en la base de datos.
  - `_FALLBACK_QUERIES` - Diccionario con consultas SQL para diferentes estadísticas.
  - `_sql(query_id: str, fallback: str = "") -> str` - Obtiene una consulta SQL a partir del diccionario o devuelve una consulta de respaldo si no se encuentra.
  - `get_volumen_stats()` - Devuelve un DataFrame con las estadísticas de volumen de movimientos.
  - `get_area_stats_prod()` - Devuelve un DataFrame con las estadísticas de área para materiales de producción.
  - `get_material_consumos_abc()` - Devuelve un DataFrame con las estadísticas de consumo ABC.
  - `get_top_users(start_year: str = '2026') -> pd.DataFrame` - Devuelve un DataFrame con los usuarios más activos.
  - `get_trend_stats(start_year: str = '2025') -> pd.DataFrame` - Devuelve un DataFrame con las tendencias temporales de movimientos.
  - `get_dow_stats()` - Devuelve un DataFrame con las estadísticas de días hábiles.
  - `get_pm_type_material_records()` - Devuelve un DataFrame con los tipos de material según el tipo de mantenimiento.
  - `get_area_material_mapping_201()` - Devuelve un DataFrame con la asignación de materiales por área para CMV 201.
  - `get_user_material_mapping(users: Tuple[str, ...]) -> pd.DataFrame` - Devuelve un DataFrame con la asignación de materiales por usuario y tipo de movimiento.
  - `get_location_material_summary()` - Devuelve un DataFrame con las estadísticas de resumen de ubicaciones de materiales.
  - `get_total_active_days()` - Devuelve el número total de días activos en los movimientos.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `inventory_movements`
- Columnas:
  - `tipo_operacion`, `material`, `cantidad`, `fe_contab`, `usuario`, `alm`, `cmv`, `ce_coste`, `texto_breve_material`, `texto_cab_documento`, `referencia`

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas:
  - `pandas`
  - `sqlalchemy`
- Flujo interno: La clase interactúa con una instancia de `BaseRepository` para obtener la sesión de base de datos y ejecutar consultas SQL.

