## Archivo: ./services/productivity_daily.py

### Resumen Funcional
El archivo `productivity_daily.py` contiene el servicio para gestionar los datos de productividad diaria en un sistema de almacén (WMS). Ofrece métodos para obtener fechas disponibles, datos de productividad por fecha específica y detalles de movimientos diarios de usuarios.

### Catálogo de Funciones y Clases
- `ProductivityDailyService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - `get_available_dates()` - Retorna las fechas disponibles para los KPIs de productividad.
  - `get_productivity_data(target_date: str) -> Dict[str, Any]` - Obtiene todos los KPIs de productividad para una fecha específica (YYYY-MM-DD).
  - `get_user_movements_daily_summary(target_date: str, usuario: str) -> list` - Retorna el resumen diario de movimientos de un usuario.
  - `get_user_movements_daily_details(target_date: str, usuario: str, operacion: str) -> list` - Retorna los detalles diarios de movimientos de un usuario para una operación específica.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas y Columnas:
  - `get_available_dates()`: No especifica consultas directas.
  - `get_productivity_data(target_date: str)`: Llama a `_get_daily_summary`, `_get_hourly_trend`, `_get_inactivity_gaps`, y `_get_activity_heatmap` en `ProductivityRepository`.
    - `_get_daily_summary(date_sap)`
    - `_get_hourly_trend(date_sap)`
    - `_get_inactivity_gaps(date_sap)`
    - `_get_activity_heatmap(date_sap)`
  - `get_user_movements_daily_summary(target_date: str, usuario: str)`: Llama a `get_user_movements_daily_summary` en `ProductivityRepository`.
  - `get_user_movements_daily_details(target_date: str, usuario: str, operacion: str)`: Llama a `get_user_movements_daily_details` en `ProductivityRepository`.

### Estado y Variables Globales
- No hay variables globales declaradas.

### Dependencias y Flujo
- Librerías externas:
  - `logging`
  - `typing`
  - `re` (módulo estándar de Python)
- Archivos del proyecto que importan a este archivo (`productivity_daily.py`):
  - Ninguna.
- Archivos del proyecto que este archivo importa (`productivity_daily.py`):
  - `repositories.productivity.ProductivityRepository`
- Flujo de datos:
  - El servicio recibe una sesión de base de datos y utiliza un repositorio para interactuar con la BD.
  - Los métodos devuelven datos estructurados en formato JSON.

