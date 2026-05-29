## Archivo: ./routes/transporte.py

### Resumen Funcional
Este archivo contiene rutas para la sección de Transporte (Avanti), que incluyen funciones para sincronizar datos desde una base de datos externa SQLite, obtener datos consolidados diarios, buscar en los datos de transporte y servir archivos PDF.

### Catálogo de Funciones y Clases
- `sync_transporte_logic(session: Session)` - Lógica core para sincronizar la base de datos externa de OneDrive a local.
- `sync_transporte(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta POST para sincronizar datos de transporte manualmente.
- `get_transporte_data(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta GET para obtener los datos consolidados diarios ordenados cronológicamente.
- `search_transporte(q: str, session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta GET para buscar en la tabla cruda de transporte_entregas por OT, GD o OC.
- `serve_pdf(filename: str, user=Depends(get_current_user))` - Ruta GET para servir el archivo PDF desde el disco.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `transporte_entregas`
    - Columnas: `ot`, `proveedor`, `gd`, `oc`, `bulto`, `servicio`, `archivo`, `fecha`
  - `transporte_diario`
    - Columnas: `fecha`, `total_entregas`, `pdf_path`
- Consultas SQL crudas:
  - Creación de tablas si no existen
  - Lectura de datos desde la base de datos externa
  - Inserción de datos en las tablas locales
  - Consolidación de datos
  - Mapeo de PDFs

### Estado y Variables Globales
- `EXTERNAL_DB_PATH` - Ruta a la base de datos externa SQLite.
- `PDF_DIR_PATH` - Directorio donde se almacenan los archivos PDF.

### Dependencias y Flujo
- Librerías utilizadas: `os`, `sqlite3`, `logging`, `typing`, `fastapi`, `sqlalchemy`.
- Comunicación con otros archivos del proyecto:
  - `core.app_instance.templates` (no se muestra el contenido, pero probablemente para renderizar plantillas HTML).
  - `core.database.get_session_dep` y `core.auth.get_current_user` (para manejar la sesión y autenticación).

