## Archivo: ./repositories/inventory.py

### Resumen Funcional
El archivo `inventory.py` contiene una clase `InventoryRepository` que se encarga de interactuar con la base de datos para obtener estadísticas y datos relacionados con el inventario, utilizando SQL queries y pandas DataFrames.

### Catálogo de Funciones y Clases
- **Clase:** `InventoryRepository`
  - **Métodos:**
    - `get_cmv_prod()`: Devuelve el valor configurado para CMV_PROD.
    - `get_cmv_mant()`: Devuelve el valor configurado para CMV_MANT.
    - `get_cmv_consumos()`: Devuelve una tupla con los valores de CMV_PROD y CMV_MANT.
    - `get_cmv_reversas()`: Devuelve una tupla con los valores configurados para CMV_REVERSAS.
    - `check_table_exists()`: Verifica si la tabla 'inventory_movements' existe en la base de datos.
    - `get_volumen_stats()`: Obtiene estadísticas de volumen del inventario.
    - `get_area_stats_prod()`: Obtiene estadísticas por área para el producto.
    - `get_material_consumos_abc()`: Obtiene estadísticas de materiales consumidos en ABC.
    - `get_top_users(start_year='2026')`: Obtiene los usuarios con más movimientos.
    - `get_trend_stats(start_year='2025')`: Obtiene tendencias de movimientos por período.
    - `get_dow_stats()`: Obtiene estadísticas diarias de movimiento.
    - `get_pm_type_material_records()`: Obtiene registros de tipo PM y material.
    - `get_area_material_mapping_201()`: Obtiene mapeo de área para el producto 201.
    - `get_user_material_mapping(users: Tuple[str, ...])`: Obtiene mapeo de usuario y material.
    - `get_location_material_summary()`: Obtiene resumen de materiales por ubicación.
    - `get_total_active_days()`: Obtiene el número total de días activos en los movimientos.

### Interacción con Base de Datos
- **Motor:** SQLite (inferred from the use of `sqlite_master`).
- **Tablas:** `inventory_movements`.
- **Columnas:**
  - `tipo_operacion`
  - `material`
  - `num_tx`
  - `business_area`
  - `ce_coste`
  - `cmv`
  - `fe_contab`
  - `alm`
  - `usuario`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- **Librerías Externas:** pandas, sqlalchemy.
- **Flujo Interno:** Utiliza métodos de la clase base `BaseRepository` para interactuar con la base de datos.

