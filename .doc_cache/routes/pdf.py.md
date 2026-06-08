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
- **Sesiones de Usuario:** Ninguna.
- **Entorno:** Ninguna.
- **Diccionarios Quemados:** Ninguno.

### Dependencias y Flujo
- **Librerías Externas:**
  - `pandas`
  - `fastapi`
  - `sqlalchemy`
  - `logging`
  - `io`

- **Archivos del Proyecto que Importa a este Archivo (Consumo):**
  - `config.py` (para constantes como `DB_PATH`, `PDF_STORAGE`)
  - `core.database.get_session_dep` (dependencia para obtener la sesión de base de datos)
  - `core.pdf_engine.WMS_Landscape_PDF`
  - `core.pdf_reports.draw_annex_table`
  - `core.pdf_reports.draw_picking_list`
  - `repositories.deliveries.DeliveriesRepository`

- **Archivos del Proyecto que este Archivo Importa (Lo Consumen):**
  - Ninguno.

**Flujo de Datos:**
1. El usuario accede a las rutas `/generate-pdf` o `/generate-pdf-bulk`.
2. Se inicia una sesión de base de datos.
3. Se obtienen los datos necesarios desde la base de datos usando `DeliveriesRepository`.
4. Se genera el PDF utilizando `WMS_Landscape_PDF` y funciones auxiliares (`draw_delivery_page`, `get_ots_for_delivery`, etc.).
5. El PDF se devuelve al usuario como una respuesta HTTP con tipo MIME `application/pdf`.

