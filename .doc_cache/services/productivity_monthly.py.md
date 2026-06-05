## Archivo: ./services/productivity_monthly.py

### Resumen Funcional
El archivo `productivity_monthly.py` contiene servicios para calcular y obtener datos de productividad mensuales en un sistema de almacén (WMS). Ofrece métodos para obtener resúmenes de productividad mensuales, movimientos diarios de usuarios y detalles específicos de operaciones.

### Catálogo de Funciones y Clases
- `ProductivityMonthlyService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - `get_monthly_productivity_data(target_month: str) -> Dict[str, Any]` - Calcula y devuelve los KPIs de productividad para un mes específico (YYYY-MM).
  - `get_user_movements_monthly_summary(target_month: str, usuario: str) -> list` - Obtiene el resumen de movimientos diarios de un usuario para un mes.
  - `get_user_movements_monthly_details(target_month: str, usuario: str, operacion: str) -> list` - Obtiene los detalles específicos de una operación de movimiento diario de un usuario para un mes.

### Interacción con Base de Datos
- Motor de BD: SQLite.
- Tablas y Columnas:
  - `tasks_repo._get_monthly_summary(month_sap)` - Lee datos de la tabla que contiene resúmenes mensuales de tareas.
  - `tasks_repo._get_monthly_shifts(month_sap)` - Lee datos de la tabla que contiene información sobre los turnos diarios.
  - `tasks_repo._get_monthly_heatmap(month_sap)` - Lee datos de la tabla que contiene mapas térmicos de productividad.

### Estado y Variables Globales
- Ninguna.

### Dependencias y Flujo
- Librerías externas: `logging`, `typing`.
- Archivos del proyecto que importa:
  - `repositories.tasks` - Importado en el constructor de la clase `ProductivityMonthlyService`.
- Archivos del proyecto que son importados por este archivo:
  - Ninguno.
- Flujo de datos:
  - El servicio recibe una sesión de base de datos y utiliza un repositorio para acceder a los datos necesarios. Los resultados se procesan y devuelven en formato JSON.

Este archivo es parte de la capa de servicios del sistema, donde se encapsulan las lógicas de negocio relacionadas con el cálculo y obtención de datos de productividad mensuales.

