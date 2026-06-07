## Archivo: ./routes/transporte.py

### Resumen Funcional
Este archivo contiene rutas para la sección de Transporte en un sistema de monitoreo de almacén (WMS). Permite la sincronización de datos desde una base de datos externa, consulta de datos consolidados, búsqueda y descarga de PDFs.

### Catálogo de Funciones y Clases
- `sync_transporte_logic(session: Session)` - Lógica core para sincronizar la base de datos externa a local.
- `sync_transporte(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta para sincronizar datos de transporte manualmente.
- `get_transporte_data(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Retorna los datos consolidados diarios ordenados cronológicamente.
- `search_transporte(q: str, session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Busca en la tabla cruda de transporte_entregas por OT, GD o OC.
- `serve_pdf(filename: str, user=Depends(get_current_user))` - Sirve el archivo PDF desde el disco.
- `get_pending_transporte(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Busca en transporte_entregas los documentos del año actual que NO han sido ingresados al inventario SAP.

### Interacción con Base de Datos
- Motor: SQLite
- Tablas:
  - `transporte_entregas`
    - Columnas: ot, proveedor, gd, oc, bulto, servicio, archivo, fecha
  - `transporte_diario`
    - Columnas: fecha, total_entregas, pdf_path
- Consultas SQL crudas y llamadas a ORM:
  - Creación de tablas si no existen.
  - Lectura de datos desde la base de datos externa.
  - Inserción de datos en `transporte_entregas`.
  - Consolidación de datos en `transporte_diario`.
  - Mapeo de PDFs.

### Estado y Variables Globales
- `EXTERNAL_DB_PATH` - Ruta a la base de datos externa SQLite.
- `PDF_DIR_PATH` - Directorio donde se almacenan los archivos PDF.

### Dependencias y Flujo
- Librerías externas: `logging`, `os`, `sqlite3`, `typing`.
- Archivos del proyecto que importan este archivo:
  - `core.auth`
  - `core.database`
- Archivos del proyecto que son importados por este archivo:
  - No aplica.
- Flujo de datos: El archivo consume y produce datos para las rutas definidas, interactuando con la base de datos SQLite y proporcionando respuestas en formato JSON.

