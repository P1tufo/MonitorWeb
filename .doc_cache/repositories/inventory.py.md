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

