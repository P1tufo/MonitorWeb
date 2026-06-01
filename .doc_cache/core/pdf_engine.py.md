## Archivo: ./core/pdf_engine.py

### Resumen Funcional
El archivo `pdf_engine.py` es un motor optimizado para la generación de documentos PDF en el sistema de monitoreo de almacén (WMS). Se encarga de crear reportes WMS en formato horizontal utilizando la biblioteca FPDF y otros componentes como pandas y barcode.

### Catálogo de Funciones y Clases
- `get_ots_for_delivery(entrega_id: str, conn: sqlite3.Connection) -> List[str]`
  - Consulta las OTs asociadas a una entrega y las devuelve como lista de strings.
  
- `_generate_barcode_stream(data: str, options: Optional[dict] = None) -> io.BytesIO`
  - Genera un código de barras en memoria (BytesIO).

- `draw_delivery_page(pdf: WMS_Landscape_PDF, header: pd.Series, items: pd.DataFrame, include_logo: bool = True, ots_list: Optional[List[str]] = None) -> None`
  - Dibuja una página de entrega completa utilizando sub-métodos modulares.

- `_draw_page_header(pdf: WMS_Landscape_PDF, h: pd.Series, include_logo: bool)`
  - Dibuja el encabezado superior, logo y código de barras de la entrega.
  
- `_draw_info_block(pdf: WMS_Landscape_PDF, h: pd.Series)`
  - Dibuja el bloque de información principal de la entrega.

- `_draw_table(pdf: WMS_Landscape_PDF, items_df: pd.DataFrame)`
  - Dibuja la tabla de materiales con ordenamiento por ubicación.
  
- `_draw_ot_barcodes(pdf: WMS_Landscape_PDF, ots: List[str])`
  - Dibuja los códigos de barras de las OTs en el lateral derecho.

- `_draw_signature_block(pdf: WMS_Landscape_PDF)`
  - Dibuja los cuadros de firma al final de la página.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
- **Motor:** SQLite
- **Operaciones SQL:**
  - `SELECT DISTINCT numero_ot FROM warehouse_tasks WHERE ltrim(CAST(entrega AS TEXT), '0') = ?`

### Flujo de Datos y Pipeline
1. **Entrada:** Recibe un ID de entrega (`entrega_id`) y una conexión a la base de datos SQLite (`conn`).
2. **Transformaciones:**
   - Consulta las OTs asociadas a la entrega desde la tabla `warehouse_tasks`.
   - Genera códigos de barras para la entrega y las OTs.
3. **Salida:** Produce un documento PDF con la información de la entrega, los códigos de barras y una firma.

### Caché y Estado
No aplica.

### Lógica de Negocio y Reglas
- **Constantes de Diseño:**
  - Margen X e Y.
  - Posición inicial de la tabla.
  - Altura de las filas.
  - Número máximo de filas.
  - Dimensiones del código de barras.

### Dependencias y Flujo
- **Librerías Externas:** `numpy`, `pandas`, `fpdf`, `barcode`
- **Archivos Importados:**
  - `config.py` (para la configuración temporal)
- **Flujo de Datos:** El archivo se importa en otros archivos para generar PDFs, lo que indica que es un componente consumido por otros servicios o rutas del sistema.

