## Archivo: ./services/productivity_monthly.py

### Resumen Funcional
El archivo `productivity_monthly.py` contiene servicios para calcular y obtener datos de productividad mensuales en un sistema de almacén (WMS). Ofrece métodos para obtener resúmenes y detalles de movimientos de usuarios por mes.

### Catálogo de Funciones y Clases
- `ProductivityMonthlyService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - `get_monthly_productivity_data(target_month: str) -> Dict[str, Any]` - Calcula y devuelve los KPIs de productividad para un mes específico (YYYY-MM).
  - `get_user_movements_monthly_summary(target_month: str, usuario: str) -> list` - Obtiene el resumen de movimientos mensuales por usuario.
  - `get_user_movements_monthly_details(target_month: str, usuario: str, operacion: str) -> list` - Obtiene los detalles de movimientos mensuales por usuario y operación.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - Ninguna (se asume que las consultas SQL están definidas en el repositorio `ProductivityRepository`)
- Consultas SQL Crudas o ORM:
  - `_get_monthly_summary(month_sap)`
  - `_get_monthly_shifts(month_sap)`
  - `_get_monthly_heatmap(month_sap)`
  - `get_user_movements_monthly_summary(target_month, usuario)`
  - `get_user_movements_monthly_details(target_month, usuario, operacion)`

### Estado y Variables Globales
- Ninguna

### Dependencias y Flujo
- Librerías Externas:
  - `logging`
  - `typing`
  - `sqlalchemy.orm.Session`
- Archivos del Proyecto que Importan a este Archivo (lo Consumen):
  - Ninguno
- Archivos del Proyecto que Este Archivo Importa (consume):
  - `repositories.productivity.ProductivityRepository`

**Flujo de Datos:**
1. El servicio `ProductivityMonthlyService` se inicializa con una sesión de base de datos.
2. Los métodos `get_monthly_productivity_data`, `get_user_movements_monthly_summary`, y `get_user_movements_monthly_details` llaman a los métodos correspondientes del repositorio `ProductivityRepository`.
3. El repositorio ejecuta consultas SQL para obtener los datos de productividad y movimientos.
4. Los resultados se procesan y devuelven al servicio, que finalmente los devuelve al cliente.

