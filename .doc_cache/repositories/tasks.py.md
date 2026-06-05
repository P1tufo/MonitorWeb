## Archivo: ./repositories/tasks.py (Procesado en 2 partes)

#### --- PARTE 1 de 2 ---

### Resumen Funcional
Este archivo contiene métodos para obtener resúmenes diarios, horarios, inactividades y calorímetros de movimientos en el sistema de almacén. También incluye funciones para obtener detalles diarios y mensuales de los movimientos realizados por usuarios específicos.

### Catálogo de Funciones y Clases
- `get_available_dates()` - Devuelve una lista ordenada de fechas únicas con movimientos generados o confirmados.
- `_get_daily_summary(date_sap)` - Calcula el resumen diario de movimientos para un usuario específico.
- `_get_hourly_trend(date_sap)` - Genera un trend horario de los movimientos.
- `_get_inactivity_gaps(date_sap)` - Identifica los huecos de inactividad en los movimientos.
- `_get_activity_heatmap(date_sap)` - Crea un mapa de calor basado en la actividad diaria.
- `get_user_movements_daily_summary(target_date, usuario)` - Obtiene el resumen diario de movimientos para un usuario específico.
- `get_user_movements_daily_details(target_date, usuario, operacion)` - Detalla los movimientos diarios para un usuario y una operación específica.
- `_get_monthly_summary(month_sap)` - Calcula el resumen mensual de movimientos.
- `_get_monthly_shifts(month_sap)` - Genera un trend por turnos mensuales.
- `_get_monthly_heatmap(month_sap)` - Crea un mapa de calor basado en la actividad mensual.
- `get_user_movements_monthly_summary(target_month, usuario)` - Obtiene el resumen mensual de movimientos para un usuario específico.
- `get_user_movements_monthly_details(target_month, usuario, operacion)` - Detalla los movimientos mensuales para un usuario y una operación específica.
- `get_tasks_summary()` - Devuelve un resumen de tareas por clase de movimiento.
- `get_tasks_trend()` - Genera un trend de las tareas.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `inventory_movements`
    - Columnas: `registrado`, `hora`, `usuario`, `tipo_operacion`, `texto_cab_documento`, `doc_mat`, `cmv`, `material`, `texto_breve_material`, `cantidad`
  - `warehouse_tasks`
    - Columnas: `fecha_conf`, `hor_conf`, `usuario_conf`, `numero_ot`, `ctd_teor_dsd`, `cl_mov`, `clase_mov`, `fe_creac`, `hora`

### Estado y Variables Globales
- No hay variables globales declaradas.

### Dependencias y Flujo
- Librerías externas: `pandas`
- Archivos del proyecto que importan a este archivo:
  - `./services/tasks_service.py` (consume)
- Archivos del proyecto que este archivo importa:
  - `./base.py` (consumido por `TasksRepository`)
  - `./models.py` (no se muestra en el fragmento, pero probablemente contiene modelos SQLAlchemy)

#### --- PARTE 2 de 2 ---

### Resumen Funcional
Este archivo contiene funciones que interactúan con una base de datos SQLite para recuperar y procesar datos relacionados con tareas en un sistema de almacén (WMS). Las funciones devuelven datos en formato DataFrame de pandas.

### Catálogo de Funciones y Clases
- `get_tasks_trend()` - Recupera el trend de tareas por mes.
- `get_tasks_by_user()` - Recupera las tareas agrupadas por usuario.
- `get_tasks_by_type_dest()` - Recupera las tareas agrupadas por tipo de movimiento y destino.
- `get_recent_tasks()` - Recupera las tareas recientes que no han sido confirmadas.
- `get_non_palletized_movements()` - Recupera los movimientos no palletizados.
- `get_non_palletized_count()` - Cuenta el número de movimientos no palletizados.
- `get_non_palletized_summary()` - Resumen de movimientos no palletizados.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `warehouse_tasks`
  - `lx02_pendientes`
  - `inventory_movements`
- Columnas:
  - `warehouse_tasks`: `fe_creac`, `fecha_conf`, `usuario`, `usuario_conf`, `clase_mov`, `ctd_teor_dsd`, `ubic_proc`, `ubic_dest`, `hora`, `numero_ot`, `material`, `texto_breve_material`
  - `lx02_pendientes`: `otcuanto`, `stock_disp`
  - `inventory_movements`: `doc_mat`, `usuario`, `cmv`, `fe_contab`, `hora`

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- Librerías externas: pandas, sqlalchemy.
- Archivos del proyecto que importan a este archivo:
  - Ninguno.
- Archivos del proyecto que este archivo importa:
  - Ninguno.

