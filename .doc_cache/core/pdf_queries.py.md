## Archivo: ./core/pdf_queries.py

### Resumen Funcional
Este archivo contiene funciones para construir y ejecutar consultas SQL en una base de datos SQLite, específicamente para generar reportes PDF. Las funciones manejan filtros dinámicos para entregas, áreas y centros, y recuperan información detallada sobre los materiales por entrega.

### Catálogo de Funciones y Clases
- `get_deliveries_for_bulk(conn: sqlite3.Connection, date: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, entrega_query: Optional[str] = None) -> pd.DataFrame` - Construye y ejecuta la query dinámica para filtrar entregas en reportes masivos.
- `get_area_lookup(conn: sqlite3.Connection) -> pd.DataFrame` - Obtiene el área de negocio dominante para cada entrega.
- `get_picking_items(conn: sqlite3.Connection, entrega_ids: List[str]) -> pd.DataFrame` - Obtiene materiales por entrega (desglosado) para el picking list, asegurando cantidades visibles.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - `outbound_deliveries`
- Columnas:
  - `entrega`, `autor`, `fecha_carga`, `fecha_sm_real`, `creado_el`, `week_sort`, `estado_wms`, `material`, `denominacion`, `cantidad`, `umb`, `ubicacion_bin`, `ubicacion_area`, `ubicacion_bin_1`
- Consultas SQL crudas:
  - `get_deliveries_for_bulk` construye consultas dinámicas basadas en los filtros proporcionados.
  - `get_area_lookup` y `get_picking_items` ejecutan consultas estáticas para obtener áreas de negocio y materiales por entrega, respectivamente.

### Estado y Variables Globales
- No aplica

### Dependencias y Flujo
- Librerías externas utilizadas:
  - `logging`
  - `pandas`
  - `sqlite3`
  - `typing` (para tipos de datos)
- Flujo interno:
  - Las funciones interactúan con la base de datos SQLite para recuperar y procesar información.
  - Utilizan expresiones SQL complejas para filtrar y agrupar datos.

