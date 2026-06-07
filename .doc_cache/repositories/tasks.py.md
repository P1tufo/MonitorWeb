## Archivo: ./repositories/tasks.py

### Resumen Funcional
El archivo `tasks.py` contiene métodos para obtener resúmenes y detalles de tareas en un sistema de almacén (WMS). Estos métodos interactúan con una base de datos SQLite para recuperar información sobre las tareas, incluyendo estadísticas de resumen, tendencias diarias, usuarios que realizan más tareas, tipos de movimiento, tareas recientes y movimientos no palletizados.

### Catálogo de Funciones y Clases
- `get_tasks_summary()` - Devuelve un DataFrame con el resumen de las tareas agrupadas por tipo.
- `get_tasks_trend()` - Devuelve un DataFrame con la tendencia diaria de creación y confirmación de tareas.
- `get_tasks_by_user()` - Devuelve un DataFrame con las tareas realizadas por cada usuario en el último mes.
- `get_tasks_by_type_dest()` - Devuelve un DataFrame con el resumen de las tareas agrupadas por tipo de movimiento.
- `get_recent_tasks()` - Devuelve un DataFrame con las tareas recientes que no han sido confirmadas.
- `get_non_palletized_movements()` - Devuelve un DataFrame con los movimientos no palletizados más recientes.
- `get_non_palletized_count()` - Devuelve el número de movimientos no palletizados.
- `get_non_palletized_summary()` - Devuelve un DataFrame con el resumen de los movimientos no palletizados, incluyendo la fecha más antigua y más reciente.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `warehouse_tasks`
  - `lx02_pendientes`
  - `inventory_movements`
- Columnas:
  - `cl_mov`, `clase_mov`, `COUNT(*)`, `SUM(ctd_teor_dsd)`, `fe_creac`, `fecha_conf`, `usuario`, `usuario_conf`, `numero_ot`, `material`, `texto_breve_material`, `ubic_proc`, `ubic_dest`, `hora`, `otcuanto`, `pos`, `stock_disp`, `alm`, `ce`, `cmv`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías externas: `pandas`
- Archivos del proyecto que importan a este archivo:
  - Ninguno
- Archivos del proyecto que este archivo importa:
  - `base.py` (clase base `BaseRepository`)
- Flujo de datos: El archivo consume métodos y funciones de la clase base para interactuar con la base de datos y procesar los resultados en DataFrames de pandas.

