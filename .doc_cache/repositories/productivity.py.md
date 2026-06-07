## Archivo: ./repositories/productivity.py

### Resumen Funcional
El archivo `productivity.py` contiene métodos para obtener resúmenes diarios, mensuales y detalles de movimientos de usuarios en un sistema de almacén (WMS). Utiliza SQLAlchemy para interactuar con una base de datos SQLite y pandas para procesar los resultados.

### Catálogo de Funciones y Clases
- `_get_raw_activities_cte(is_monthly=False)`: Genera una Common Table Expression (CTE) que une todos los eventos de actividad desde diferentes tablas.
- `get_available_dates()`: Devuelve una lista ordenada de fechas únicas en formato YYYY-MM-DD con movimientos generados o confirmados.
- `_get_daily_summary(date_sap: str)`: Obtiene un resumen diario de movimientos y actividades por usuario.
- `_get_hourly_trend(date_sap: str)`: Genera una tendencia horaria de las actividades por usuario.
- `_get_inactivity_gaps(date_sap: str)`: Identifica los huecos de inactividad en el movimiento de usuarios.
- `_get_activity_heatmap(date_sap: str)`: Crea un mapa de calor de las actividades diarias por usuario y franja horaria.
- `get_user_movements_daily_summary(target_date: str, usuario: str)`: Obtiene un resumen diario de movimientos por operación para un usuario específico.
- `get_user_movements_daily_details(target_date: str, usuario: str, operacion: str)`: Detalla los movimientos diarios de un usuario para una operación específica.
- `_get_monthly_summary(month_sap: str)`: Obtiene un resumen mensual de movimientos y actividades por usuario.
- `_get_monthly_shifts(month_sap: str)`: Genera un resumen mensual de las actividades por usuario y turno.
- `_get_monthly_heatmap(month_sap: str)`: Crea un mapa de calor de las actividades mensuales por usuario y día de la semana.
- `get_user_movements_monthly_summary(target_month: str, usuario: str)`: Obtiene un resumen mensual de movimientos por operación para un usuario específico.
- `get_user_movements_monthly_details(target_month: str, usuario: str, operacion: str)`: Detalla los movimientos mensuales de un usuario para una operación específica.
- `_format_date_sap(target_date: str)`: Formatea una fecha en formato SAP (DD.MM.YYYY).
- `_format_month_sap(target_month: str)`: Formatea un mes en formato SAP (MM.YYYY).

### Interacción con Base de Datos
- Motor de BD: SQLite.
- Tablas:
  - `inventory_movements`
  - `warehouse_tasks`
- Columnas:
  - `inventory_movements`: `usuario`, `registrado`, `hora`, `doc_mat`, `tipo_operacion`, `texto_cab_documento`, `cmv`, `material`, `texto_breve_material`, `cantidad`.
  - `warehouse_tasks`: `usuario_conf`, `fecha_conf`, `hor_conf`, `numero_ot`, `ctd_teor_dsd`.

### Estado y Variables Globales
- No hay variables globales, de sesión o de entorno definidas en este archivo.

### Dependencias y Flujo
- Librerías externas: `logging`, `re`, `pandas`.
- Archivos del proyecto que importan a este archivo:
  - `core.macros`
  - `repositories.base.BaseRepository`
- Archivos del proyecto que este archivo importa:
  - Ninguno.
- Flujo de datos: El archivo consume datos desde la base de datos SQLite y los procesa con pandas, luego devuelve resultados en formato JSON.

