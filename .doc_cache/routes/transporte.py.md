## Archivo: ./routes/transporte.py

### Resumen Funcional
Este archivo contiene rutas para la sección de Transporte en un sistema de monitoreo de almacén (WMS). Permite sincronizar datos desde una base de datos externa, obtener datos consolidados diarios, buscar registros y servir archivos PDF.

### Catálogo de Funciones y Clases
- `sync_transporte_logic(session: Session)` - Lógica core para sincronizar la base de datos externa de OneDrive a local.
- `sync_transporte(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta para sincronizar datos de transporte manualmente.
- `get_transporte_data(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta que retorna los datos consolidados diarios ordenados cronológicamente.
- `search_transporte(q: str, session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta para buscar en la tabla cruda de transporte_entregas por OT, GD o OC.
- `serve_pdf(filename: str, user=Depends(get_current_user))` - Ruta que sirve el archivo PDF desde el disco.
- `get_pending_transporte(session: Session = Depends(get_session_dep), user=Depends(get_current_user))` - Ruta para buscar en transporte_entregas los documentos del año actual que NO han sido ingresados al inventario SAP (inventory_movements).

### Interacción con Base de Datos
- **Motor:** SQLite
- **Tablas:**
  - `transporte_entregas`
    - `ot`
    - `proveedor`
    - `gd`
    - `oc`
    - `bulto`
    - `servicio`
    - `archivo`
    - `fecha`
  - `transporte_diario`
    - `fecha` (PRIMARY KEY)
    - `total_entregas`
    - `pdf_path`
- **Consultas SQL Crudas:**
  - Creación de tablas si no existen.
  - Lectura de datos desde la base de datos externa.
  - Inserción de datos crudos en la tabla local.
  - Consolidación de datos diarios.
  - Mapeo de PDFs.

### Estado y Variables Globales
- `EXTERNAL_DB_PATH` - Ruta a la base de datos externa SQLite.
- `PDF_DIR_PATH` - Directorio donde se almacenan los archivos PDF.

### Dependencias y Flujo
- **Dependencias Externas:** `sqlite3`, `logging`
- **Archivos del Proyecto que Importan a este Archivo:**
  - `core.app_instance`
  - `core.database`
  - `core.auth`
- **Archivos del Proyecto que Este Archivo Importa:**
  - Ninguno
- **Dirección del Flujo de Datos:** El archivo consume datos desde la base de datos externa y los almacena localmente, luego sirve datos a través de las rutas definidas.

