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
  - `io`, `logging`, `pandas`, `datetime`, `typing`, `fastapi`, `sqlalchemy`, `text`.
- **Archivos del Proyecto que Importa a este Archivo (Consumo):** Ninguno.
- **Archivos del Proyecto que Este Archivo Importa (Lo Consumen):**
  - `core.database.get_session_dep`
  - `repositories.deliveries.DeliveriesRepository`
  - `core.pdf_engine.WMS_Landscape_PDF`, `draw_delivery_page`, `get_ots_for_delivery`
  - `core.pdf_reports.draw_annex_table`, `draw_picking_list`

**Flujo de Datos:**
1. **Entrada:** Parámetros del formulario.
2. **Procesamiento:**
   - Consulta a la base de datos para obtener los datos necesarios.
   - Generación del PDF utilizando las funciones definidas en `core.pdf_engine` y `core.pdf_reports`.
3. **Salida:** Respuesta HTTP con el contenido del PDF.

**Flujo Inverso:**
1. **Entrada:** Archivos del proyecto que consumen este archivo.
2. **Procesamiento:** No aplica.
3. **Salida:** No aplica.

