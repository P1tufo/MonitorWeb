## Archivo: ./repositories/widgets.py

### Resumen Funcional
El archivo `widgets.py` contiene métodos para ejecutar consultas dinámicas y generar visualizaciones de datos en un sistema de monitoreo de almacén (WMS). Utiliza FastAPI, SQLAlchemy y SQLite para interactuar con la base de datos.

### Catálogo de Funciones y Clases
- `execute_widget(query_id: str, visual_state: str, year: Optional[str], area: Optional[str], granularity: Optional[str]) -> Dict[str, Any]` - Ejecuta una consulta dinámica para generar una visualización de datos.
- `execute_drilldown(query_id: str, visual_state: str, segment: str, material: Optional[str], year: Optional[str]) -> list` - Realiza un drilldown en los datos para obtener detalles adicionales.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas y Columnas:**
  - Tabla: `outbound_deliveries`
    - Columnas: `fecha_carga`, `entrega`, `pos_`, `cantidad`, `dias_retraso`, `material`, `denominacion`

### Estado y Variables Globales
- No hay variables globales, de sesión o diccionarios quemados en el código.

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `sqlalchemy`
  - `json`
  - `logging`
  - `typing`

- **Archivos del Proyecto que Importan a este Archivo (lo consumen):**
  - No se mencionan archivos específicos.

- **Flujo de Datos:**
  - El archivo importa funciones y clases desde otros módulos (`core.helpers.dynamic_executor`, `core.query_engine`, `core.schemas`, `core.utils`) para ejecutar consultas dinámicas y generar visualizaciones.
  - Los métodos `execute_widget` y `execute_drilldown` interactúan con la base de datos mediante SQLAlchemy y pandas, procesando los resultados para generar visualizaciones.

