## Archivo: ./routes/pdf.py

### Resumen Funcional
Este archivo contiene rutas FastAPI para generar PDFs relacionados con el sistema de monitoreo de almacén (WMS). Ofrece dos endpoints: uno para generar un PDF individual y otro para generar un reporte masivo.

### Catálogo de Funciones y Clases
- `generate_pdf(entrega, include_logo, action, session)` - Genera un PDF para una única entrega.
- `generate_pdf_bulk(date, entrega_query, area, centro, has_ots_filter, include_logo, action, session)` - Genera un reporte masivo con índice y picking list.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:**
  - `DeliveriesRepository` interactúa con la tabla que contiene los detalles de las entregas.
- **Columnas:**
  - En `generate_pdf`, se accede a columnas como `entrega`, `include_logo`, `action`.
  - En `generate_pdf_bulk`, se acceden a columnas como `date`, `entrega_query`, `area`, `centro`, `has_ots_filter`.

### Estado y Variables Globales
- **Variables Globales:** Ninguna.
- **Variables de Sesión:** Ninguna.
- **Diccionarios Quemados:** Ninguno.

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `fastapi`
  - `sqlalchemy`
  - `logging`
  - `io`
  - `datetime`
  - `typing`
- **Archivos del Proyecto que Importa a este Archivo:** Ninguno.
- **Archivos del Proyecto que Este Archivo Importa:**
  - `config.DB_PATH`
  - `config.PDF_STORAGE`
  - `core.database.get_session_dep`
  - `core.pdf_engine.WMS_Landscape_PDF`
  - `core.pdf_engine.draw_delivery_page`
  - `core.pdf_engine.get_ots_for_delivery`
  - `core.pdf_reports.draw_annex_table`
  - `core.pdf_reports.draw_picking_list`
  - `repositories.deliveries.DeliveriesRepository`

**Flujo de Datos:**
1. **Entrada:** Parámetros del formulario.
2. **Procesamiento:**
   - Consulta a la base de datos para obtener los datos necesarios.
   - Generación del PDF utilizando las funciones definidas en `core.pdf_engine` y `core.pdf_reports`.
3. **Salida:** Respuesta HTTP con el contenido del PDF.

Este flujo asegura que los datos se procesen correctamente y se generen los PDFs según los parámetros proporcionados.

