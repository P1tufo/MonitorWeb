## Archivo: ./core/pdf_queries.py

### Resumen Funcional
Este archivo contiene funciones para construir y ejecutar consultas SQL en una base de datos SQLite, específicamente para generar reportes PDFs relacionados con entregas y materiales. Las funciones manejan filtros dinámicos y validaciones de seguridad.

### Catálogo de Funciones y Clases
- `get_deliveries_for_bulk(conn: sqlite3.Connection, date: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, entrega_query: Optional[str] = None) -> pd.DataFrame` - Construye y ejecuta la query dinámica para filtrar entregas en reportes masivos.
- `get_area_lookup(conn: sqlite3.Connection) -> pd.DataFrame` - Obtiene el área de negocio dominante para cada entrega.
- `get_picking_items(conn: sqlite3.Connection, entrega_ids: List[str]) -> pd.DataFrame` - Obtiene materiales por entrega (desglosado) para el picking list, asegurando cantidades visibles.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas:
  - `outbound_deliveries`
  - `warehouse_tasks`
- Columnas:
  - `entrega`, `autor`, `fecha_carga`, `fecha_sm_real`, `creado_el`, `ubicacion_area`, `ubicacion_bin_1`, `ubicacion_bin`, `area_negocio`, `material`, `denominacion`, `cantidad`, `umb`, `pos_`
- Consultas SQL crudas:
  - Consulta dinámica para filtrar entregas.
  - Consulta para obtener el área de negocio dominante.
  - Consulta para obtener materiales por entrega.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: `logging`, `pandas`, `sqlite3`
- Comunicación con otros archivos del proyecto:
  - No se menciona ninguna comunicación explícita con otros archivos.

