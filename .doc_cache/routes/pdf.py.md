## Archivo: ./routes/pdf.py

### Resumen Funcional
Este archivo contiene rutas para generar reportes PDF en un sistema WMS (Warehouse Management System). Ofrece dos endpoints: uno para generar un PDF individual y otro para generar un reporte masivo con múltiples entregas.

### Catálogo de Funciones y Clases
- `generate_pdf(entrega, include_logo, action, session)` - Genera un PDF para una única entrega.
- `generate_pdf_bulk(date, entrega_query, area, centro, has_ots_filter, include_logo, action, session)` - Genera un reporte masivo con índice y picking list.

### Interacción con Base de Datos
- Motor: SQLite (inferred from the use of SQLAlchemy)
- Tablas:
  - `outbound_deliveries`
  - Consultas SQL crudas para leer datos de estas tablas.
- Columnas:
  - Todas las columnas de la tabla `outbound_deliveries` se leen en los métodos.

### Estado y Variables Globales
No aplica

### Dependencias y Flujo
- Librerías externas utilizadas: `pandas`, `fastapi`, `sqlalchemy`, `logging`.
- Comunicación con otros archivos del proyecto:
  - `core.database.get_session_dep` para obtener la sesión de base de datos.
  - `core.pdf_engine.WMS_Landscape_PDF` y sus métodos (`draw_delivery_page`, `get_ots_for_delivery`) para generar el PDF.
  - `core.pdf_queries` para consultas SQL relacionadas con las entregas.
  - `core.pdf_reports` para dibujar tablas y listas en el PDF.

