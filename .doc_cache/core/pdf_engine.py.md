## Archivo: ./core/pdf_engine.py

### Resumen Funcional
El archivo `pdf_engine.py` es un motor optimizado para la generación de documentos PDF en formato horizontal (landscape) para el sistema de monitoreo de almacén (WMS). Permite crear reportes detallados de entregas, incluyendo códigos de barras y tablas de materiales.

### Catálogo de Funciones y Clases
- `WMS_Landscape_PDF(FPDF)` - Clase base para reportes WMS en formato horizontal.
  - `__init__()`: Inicializa la clase con configuraciones específicas para PDFs horizontales.
  - `get_column_x(col: int) -> float`: Calcula la posición X de una columna específica.
  - `draw_dotted_line(x1: float, y: float, x2: float) -> None`: Dibuja una línea punteada sutil.

- `get_ots_for_delivery(entrega_id: str, conn: sqlite3.Connection) -> List[str]` - Consulta las OTs asociadas a una entrega.
  - Parámetros:
    - `entrega_id`: Identificador de la entrega.
    - `conn`: Conexión a la base de datos SQLite.
  - Retorna: Lista de números de OT.

- `_generate_barcode_stream(data: str, options: Optional[dict] = None) -> io.BytesIO` - Genera un código de barras en memoria (BytesIO).
  - Parámetros:
    - `data`: Datos a codificar en el código de barras.
    - `options`: Opciones adicionales para la generación del código de barras.
  - Retorna: Flujo de bytes con el código de barras.

- `draw_delivery_page(pdf: WMS_Landscape_PDF, header: pd.Series, items: pd.DataFrame, include_logo: bool = True, ots_list: Optional[List[str]] = None) -> None` - Dibuja una página de entrega completa.
  - Parámetros:
    - `pdf`: Instancia de la clase `WMS_Landscape_PDF`.
    - `header`: Encabezado de la entrega en formato pandas Series.
    - `items`: Tabla de materiales en formato pandas DataFrame.
    - `include_logo`: Indica si incluir el logo en el encabezado (opcional).
    - `ots_list`: Lista de números de OT (opcional).

- `_draw_page_header(pdf: WMS_Landscape_PDF, h: pd.Series, include_logo: bool)` - Dibuja el encabezado superior, logo y código de barras de la entrega.
  - Parámetros:
    - `pdf`: Instancia de la clase `WMS_Landscape_PDF`.
    - `h`: Encabezado de la entrega en formato pandas Series.
    - `include_logo`: Indica si incluir el logo en el encabezado.

- `_draw_info_block(pdf: WMS_Landscape_PDF, h: pd.Series)` - Dibuja el bloque de información principal de la entrega.
  - Parámetros:
    - `pdf`: Instancia de la clase `WMS_Landscape_PDF`.
    - `h`: Encabezado de la entrega en formato pandas Series.

- `_draw_table(pdf: WMS_Landscape_PDF, items_df: pd.DataFrame)` - Dibuja la tabla de materiales con ordenamiento por ubicación.
  - Parámetros:
    - `pdf`: Instancia de la clase `WMS_Landscape_PDF`.
    - `items_df`: Tabla de materiales en formato pandas DataFrame.

- `_draw_ot_barcodes(pdf: WMS_Landscape_PDF, ots: List[str])` - Dibuja los códigos de barras de las OTs en el lateral derecho.
  - Parámetros:
    - `pdf`: Instancia de la clase `WMS_Landscape_PDF`.
    - `ots`: Lista de números de OT.

- `_draw_signature_block(pdf: WMS_Landscape_PDF)` - Dibuja los cuadros de firma al final de la página.
  - Parámetros:
    - `pdf`: Instancia de la clase `WMS_Landscape_PDF`.

### Interacción con Base de Datos
- Motor de BD: SQLite
- Tablas y Columnas:
  - Tabla: `warehouse_tasks`
  - Columnas: `numero_ot`, `entrega`

### Estado y Variables Globales
- No hay variables globales declaradas en este archivo.

### Dependencias y Flujo
- Librerías externas:
  - `io`, `logging`, `sqlite3`, `datetime`, `pathlib`, `typing`
  - `numpy`, `pandas`
  - `barcode`, `fpdf`

- Archivos del proyecto que importan a este archivo (`pdf_engine.py`):
  - Ninguno

- Archivos del proyecto que este archivo importa:
  - `config`

Flujo de datos: El archivo se utiliza para generar PDFs, por lo tanto, los datos necesarios (encabezado y detalles de entrega) provienen de otros componentes del sistema (probablemente desde el servicio o repositorio correspondientes).

