## Archivo: ./routes/productivity.py

### Resumen Funcional
El archivo `productivity.py` contiene endpoints para obtener datos de productividad diaria y mensual en un sistema de almacén (WMS) utilizando FastAPI. Los endpoints permiten consultar fechas disponibles, resúmenes diarios y mensuales de movimientos de usuarios, así como detalles específicos de estos movimientos.

### Catálogo de Funciones y Clases
- `get_available_dates(user: User, session: Session)` - Retorna las fechas disponibles para el análisis de productividad.
- `get_productivity_dashboard(date: str = Query(None), user: User, session: Session, cache: CacheManager, sync: SyncStateManager)` - Retorna los datos del dashboard de productividad para una fecha específica o por defecto "Ayer".
- `get_monthly_productivity(month: str = Query(None), user: User, session: Session, cache: CacheManager, sync: SyncStateManager)` - Retorna los KPIs mensuales de productividad.
- `get_user_movements_summary(date: str, usuario: str, user: User, session: Session)` - Retorna el resumen diario de movimientos de un usuario para una fecha específica.
- `get_user_movements_details(date: str, usuario: str, operacion: str, user: User, session: Session)` - Retorna los detalles diarios de movimientos de un usuario para una fecha específica y tipo de operación.
- `get_user_movements_monthly_summary(month: str, usuario: str, user: User, session: Session)` - Retorna el resumen mensual de movimientos de un usuario para un mes específico.
- `get_user_movements_monthly_details(month: str, usuario: str, operacion: str, user: User, session: Session)` - Retorna los detalles mensuales de movimientos de un usuario para un mes específico y tipo de operación.

### Interacción con Base de Datos
El archivo interactúa con una base de datos SQLite a través de SQLAlchemy. Las consultas específicas no están detalladas en el código proporcionado, pero se infiere que las funciones `get_available_dates`, `get_productivity_data`, `get_monthly_productivity_data`, `get_user_movements_daily_summary`, `get_user_movements_daily_details`, `get_user_movements_monthly_summary`, y `get_user_movements_monthly_details` realizan consultas a la base de datos para obtener los datos necesarios.

### Estado y Variables Globales
No se detectaron variables globales, de sesión o de entorno en el código proporcionado.

### Dependencias y Flujo
- **Dependencias**: El archivo importa dependencias desde `core.auth`, `core.database`, `services.productivity_daily`, y `services.productivity_monthly`.
- **Flujo de Datos**: Los datos fluyen a través del endpoint, se procesan en los servicios correspondientes (`ProductivityDailyService` y `ProductivityMonthlyService`), y luego se devuelven al cliente. El flujo incluye la obtención de datos desde la base de datos, su procesamiento y almacenamiento en caché si es necesario.

Este archivo es una parte integral del sistema de monitoreo de almacén, proporcionando endpoints para obtener diversos tipos de datos de productividad, con un enfoque en la eficiencia y el seguimiento de los movimientos de usuarios.

