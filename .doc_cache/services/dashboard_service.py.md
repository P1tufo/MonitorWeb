## Archivo: ./services/dashboard_service.py

### Resumen Funcional
El archivo `dashboard_service.py` contiene la lógica del servicio para el dashboard principal de entregas en un sistema de monitoreo de almacén (WMS). El servicio se encarga de obtener y formatear datos necesarios para mostrar en el dashboard, incluyendo gráficos de intensidad semanal, indicadores clave de rendimiento (KPIs), selectores y transacciones recientes.

### Catálogo de Funciones y Clases
- `DashboardService(session: Session)` - Inicializa el servicio con una sesión de base de datos.
  - **Propósito**: Configura la instancia del servicio para interactuar con la base de datos a través del repositorio `DashboardRepository`.

- `get_full_context()` - Obtiene y formatea los datos necesarios para el contexto del dashboard.
  - **Propósito**: Recupera gráficos de intensidad semanal, KPIs filtrados, selectores y transacciones recientes, y los devuelve en un formato adecuado para la vista.

### Interacción con Base de Datos
- **Motor de BD**: SQLite
- **Tablas y Columnas**:
  - `get_weekly_intensity_chart(iso_year)` - Recupera datos para el gráfico de intensidad semanal.
    - Tabla: No especificada (implícita en la consulta SQL).
    - Columnas: No especificadas (implícitas en la consulta SQL).

  - `get_filtered_kpis(None, None, None, min_week, iso_year)` - Recupera KPIs filtrados por semana y año.
    - Tabla: No especificada (implícita en la consulta SQL).
    - Columnas: No especificadas (implícitas en la consulta SQL).

  - `get_dashboard_selectors(min_week)` - Recupera selectores para el dashboard.
    - Tabla: No especificada (implícita en la consulta SQL).
    - Columnas: No especificadas (implícitas en la consulta SQL).

  - `get_filtered_transactions(None, None, None, None, None, min_week)` - Recupera transacciones recientes filtradas por semana.
    - Tabla: No especificada (implícita en la consulta SQL).
    - Columnas: No especificadas (implícitas en la consulta SQL).

### Estado y Variables Globales
- **Variables Globales**: Ninguna

### Dependencias y Flujo
- **Librerías Externas**:
  - `logging`
  - `datetime`
  - `typing`

- **Archivos del Proyecto que Importan a este Archivo (lo consumen)**: Ninguno

- **Archivos del Proyecto que Este Archivo Importa (consume)**:
  - `repositories.dashboard.DashboardRepository`

- **Dirección del Flujo de Datos**:
  - El servicio recibe una sesión de base de datos y utiliza el repositorio para obtener los datos necesarios.
  - Los datos obtenidos se formatean y devuelven en un diccionario que representa el contexto completo del dashboard.

