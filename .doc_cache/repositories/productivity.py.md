## Archivo: ./repositories/productivity.py

### Resumen Funcional
El archivo `productivity.py` contiene métodos para obtener resúmenes diarios y mensuales de la productividad de usuarios en un sistema de almacén, utilizando datos de movimientos de inventario y tareas del almacén. Los resultados se devuelven como listas de diccionarios.

### Catálogo de Funciones y Clases
- `_get_raw_activities_cte(is_monthly=False)`: Genera una Common Table Expression (CTE) con todos los eventos de actividad, unificando datos de movimientos de inventario y tareas del almacén.
- `get_available_dates()`: Devuelve una lista ordenada de fechas únicas en formato YYYY-MM-DD que tienen movimientos generados o confirmados.
- `get_all_users()`: Retorna la lista completa de usuarios con actividad para poblar filtros y agrupaciones.
- `_get_daily_summary(date_sap)`: Calcula el resumen diario de productividad por usuario, incluyendo movimientos generados, tareas confirmadas, tiempo total en minutos.
- `_get_hourly_trend(date_sap)`: Genera un trend horario de actividad por usuario.
- `_get_inactivity_gaps(date_sap)`: Identifica los huecos de inactividad por usuario.
- `_get_activity_heatmap(date_sap)`: Crea un mapa de calor de actividad por franja horaria y usuario.
- `get_user_movements_daily_summary(target_date, usuario)`: Devuelve el resumen diario de movimientos para un usuario específico.
- `get_user_movements_daily_details(target_date, usuario, operacion)`: Detalla los movimientos diarios para un usuario y una operación específica.
- `_get_monthly_summary(month_sap)`: Calcula el resumen mensual de productividad por usuario, incluyendo días trabajados y promedio de actividad diaria.
- `_get_monthly_shifts(month_sap)`: Genera un resumen de turnos (mañana, tarde, noche) por usuario y fecha.
- `_get_monthly_heatmap(month_sap)`: Crea un mapa de calor de actividad mensual por día de la semana y usuario.
- `get_user_movements_monthly_summary(target_month, usuario)`: Devuelve el resumen mensual de movimientos para un usuario específico.
- `get_user_movements_monthly_details(target_month, usuario, operacion)`: Detalla los movimientos mensuales para un usuario y una operación específica.
- `_format_date_sap(target_date)`: Formatea una fecha en formato SAP (DD.MM.YYYY).
- `_format_month_sap(target_month)`: Formatea un mes en formato SAP (MM.YYYY).

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `inventory_movements`
  - `warehouse_tasks`
- Columnas:
  - `inventory_movements`: `usuario`, `registrado`, `hora`, `doc_mat`, `tipo_operacion`, `texto_cab_documento`, `cmv`, `material`, `texto_breve_material`, `cantidad`
  - `warehouse_tasks`: `usuario_conf`, `fecha_conf`, `hor_conf`, `numero_ot`, `ctd_teor_dsd`

### Estado y Variables Globales
- No hay variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- Librerías externas: `logging`, `re`, `pandas`
- Archivos del proyecto que importa:
  - `core.macros`: `EXCLUDED_USERS_INACTIVITY`
  - `.base`: `BaseRepository`
- Archivos del proyecto que son importados por este archivo:
  - Ninguno
- Flujo de datos: El archivo consume datos de la base de datos y los procesa para devolver resultados en formato de lista de diccionarios.

