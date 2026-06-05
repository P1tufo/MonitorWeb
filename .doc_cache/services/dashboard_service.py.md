## Archivo: ./services/dashboard_service.py

### Resumen Funcional
El archivo `dashboard_service.py` contiene la lógica del servicio para el dashboard principal de entregas en un sistema de monitoreo de almacén (WMS). El servicio delega todas las operaciones de base de datos a la clase `DeliveriesRepository`, y proporciona métodos para obtener datos necesarios para renderizar el dashboard, incluyendo gráficos de intensidad semanal, indicadores clave de rendimiento (KPIs), selectores del dashboard y transacciones recientes.

### Catálogo de Funciones y Clases
- `DashboardService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - **Parámetros**: 
    - `session`: Sesión de SQLAlchemy para interactuar con la base de datos.
  
- `get_full_context()` - Obtiene el contexto completo necesario para renderizar el dashboard.
  - **Retorno**:
    - Un diccionario que contiene gráficos de intensidad semanal, KPIs, selectores del dashboard y transacciones recientes.

### Interacción con Base de Datos
- **Motor**: SQLite (implícito a través de SQLAlchemy).
- **Tablas y Columnas**:
  - `DeliveriesRepository` interactúa con las siguientes tablas y columnas:
    - Tabla: `deliveries`
      - Columnas: Dependientes de la implementación de `get_weekly_intensity_chart`, `get_filtered_kpis`, `get_dashboard_selectors`, y `get_filtered_transactions`.
    - Tabla: `kpis`
      - Columnas: Dependientes de la implementación de `get_filtered_kpis`.
    - Tabla: `transactions`
      - Columnas: Dependientes de la implementación de `get_filtered_transactions`.

### Estado y Variables Globales
- **Ninguna**: No se utilizan variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Librerías Externas**:
  - `logging`
  - `sqlalchemy.orm.Session`
  - `typing.Dict`, `typing.Any`, `typing.List`
  - `datetime.datetime`

- **Archivos del Proyecto que Importan a este Archivo (lo consumen)**:
  - Ninguna.

- **Archivos del Proyecto que Este Archivo IMPORTA (consume)**:
  - `repositories.deliveries.DeliveriesRepository`

- **Dirección del Flujo de Datos**:
  - El servicio recibe una sesión de base de datos y delega las operaciones de base de datos a `DeliveriesRepository`.
  - Los métodos de `DeliveriesRepository` interactúan con la base de datos para obtener los datos necesarios.
  - El servicio procesa estos datos y los devuelve en un formato que puede ser utilizado por la vista del dashboard.

