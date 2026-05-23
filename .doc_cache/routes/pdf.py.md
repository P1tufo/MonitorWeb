## Archivo: ./routes/pdf.py

### Resumen Funcional
Este archivo contiene rutas para generar reportes PDF en un sistema WMS (Warehouse Management System), incluyendo una versión individual y una versión masiva de entregas.

### Catálogo de Funciones y Clases
- `generate_pdf(entrega: str, include_logo: bool = False, action: str = "previsualizar", session: Session = Depends(get_session_dep))` - Genera un PDF para una única entrega.
- `generate_pdf_bulk(date: Optional[str] = None, entrega_query: Optional[str] = None, area: Optional[str] = None, centro: Optional[str] = None, has_ots_filter: Optional[str] = None, include_logo: bool = False, action: str = "previsualizar", session: Session = Depends(get_session_dep))` - Genera un reporte masivo con índice y picking list.

### Interacción con Base de Datos
- Motor: SQLite (deducido del uso de `get_session_dep()` que probablemente se conecta a una base de datos SQLite).
- Tablas:
  - `outbound_deliveries`
  - `area_lookup`
- Columnas:
  - `entrega` en `outbound_deliveries`
  - `entrega`, `area_negocio`, `autor` en `area_lookup`

### Estado y Variables Globales
No aplica.

### Dependencias y Flujo
- Librerías externas utilizadas: `pandas`, `fastapi`, `sqlalchemy`.
- Comunicación con otros archivos del proyecto:
  - `core.database.get_session_dep`
  - `core.pdf_engine.WMS_Landscape_PDF`
  - `core.pdf_queries.get_deliveries_for_bulk`, `get_area_lookup`, `get_picking_items`
  - `core.pdf_reports.draw_annex_table`, `draw_picking_list`

