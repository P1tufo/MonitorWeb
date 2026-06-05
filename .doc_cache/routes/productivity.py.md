## Archivo: ./routes/productivity.py

### Resumen Funcional
Este archivo contiene endpoints para obtener datos de productividad en un sistema de almacén (WMS) utilizando FastAPI. Ofrece información diaria y mensual de productividad, así como detalles sobre movimientos de usuarios.

### Catálogo de Funciones y Clases
- `get_available_dates(user: User, session: Session)` - Retorna las fechas disponibles para el análisis de productividad.
- `get_productivity_dashboard(date: str = Query(None), user: User, session: Session, state: AppState)` - Retorna los datos del dashboard de productividad para una fecha específica o la fecha anterior si no se especifica.
- `get_monthly_productivity(month: str = Query(None), user: User, session: Session, state: AppState)` - Retorna los KPIs mensuales de productividad para un mes específico o el mes actual si no se especifica.
- `get_user_movements_summary(date: str, usuario: str, user: User, session: Session)` - Retorna el resumen diario de movimientos de un usuario.
- `get_user_movements_details(date: str, usuario: str, operacion: str, user: User, session: Session)` - Retorna los detalles diarios de movimientos de un usuario para una operación específica.
- `get_user_movements_monthly_summary(month: str, usuario: str, user: User, session: Session)` - Retorna el resumen mensual de movimientos de un usuario.
- `get_user_movements_monthly_details(month: str, usuario: str, operacion: str, user: User, session: Session)` - Retorna los detalles mensuales de movimientos de un usuario para una operación específica.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas y Columnas:
  - `ProductivityDailyService` interactúa con tablas relacionadas con la productividad diaria.
  - `ProductivityMonthlyService` interactúa con tablas relacionadas con la productividad mensual.

### Estado y Variables Globales
- No hay variables globales explícitas en este archivo. Se utilizan dependencias para obtener el estado de la aplicación (`AppState`) y la sesión de base de datos (`Session`).

### Dependencias y Flujo
- **Librerías Externas**: FastAPI, SQLAlchemy.
- **Archivos del Proyecto que Importa**:
  - `core.database.get_session_dep`
  - `core.auth.get_current_user`
  - `services.productivity_daily.ProductivityDailyService`
  - `services.productivity_monthly.ProductivityMonthlyService`
  - `core.state.get_app_state`
- **Archivos del Proyecto que Son Importados por Este**:
  - Ninguno
- **Dirección del Flujo de Datos**: Los endpoints reciben datos de entrada (fechas, usuarios), los procesan a través de servicios y repositorios, y devuelven resultados al cliente.

