## Archivo: ./htmlcov/z_57760688d1f824db_pdf_reports_py.html (Procesado en 3 partes)

#### --- PARTE 1 de 3 ---

### Resumen Funcional
El archivo `core/pdf_reports.py` contiene funciones para la construcción de secciones complejas de PDF, específicamente para anexos y picking en un sistema de monitoreo de almacén (WMS). Las funciones incluyen la sanitización y conversión de valores de cantidad (`_parse_qty`) y el formateo de cantidades (`_fmt_qty`). Además, define una función para dibujar una tabla de anexos (`draw_annex_table`), que utiliza una biblioteca PDF como `FPDF`.

### Catálogo de Funciones y Clases
- `_parse_qty(val)` - Sanitiza y convierte a float valores de cantidad de WMS.
- `_fmt_qty(val)` - Formatea cantidades para mostrar en el PDF de forma legible.
- `draw_annex_table(pdf, grouped_data)` - Dibuja la tabla de anexos (anexo) de entregas agrupadas.

### Interacción con Base de Datos
Ninguna. El archivo no interactúa directamente con una base de datos.

### Estado y Variables Globales
No hay variables globales declaradas en el código proporcionado.

### Dependencias y Flujo
- **Dependencias**: 
  - `datetime` (biblioteca estándar de Python)
  - `FPDF` (biblioteca para crear PDFs)

- **Flujo**:
  - El archivo es importado por otros archivos del proyecto.
  - Otros archivos del proyecto pueden llamar a las funciones definidas en este archivo.

Este archivo no depende de ninguna variable global ni de estado crítico almacenado en el entorno.

#### --- PARTE 2 de 3 ---

### Resumen Funcional
El archivo contiene funciones para generar reportes PDF en un sistema de monitoreo de almacén (WMS). Específicamente, se definen métodos para dibujar listas de picking y anexos de despachos consolidados.

### Catálogo de Funciones y Clases
- `ROW_H`: Define la altura de las filas en el PDF.
- `_draw_annex_row(row)`: Dibuja una fila del anexo de despachos consolidados.
- `draw_picking_list(pdf, picking_df)`: Dibuja la lista de picking desglosada por entrega pero con total consolidado.

### Interacción con Base de Datos
Ninguna.

### Estado y Variables Globales
Ninguna.

### Dependencias y Flujo
- **Dependencias**: No se mencionan dependencias específicas en el fragmento proporcionado.
- **Flujo de Datos**:
  - `draw_picking_list` recibe un objeto PDF (`pdf`) y un DataFrame (`picking_df`) como parámetros.
  - Llama a `_draw_picking_header` para dibujar la cabecera de la tabla.
  - Itera sobre las filas del DataFrame, llamando a `_draw_picking_row` para cada fila.

El flujo de datos fluye desde el método `draw_picking_list` hacia `_draw_picking_header` y `_draw_picking_row`, pasando los objetos PDF y los datos necesarios.

