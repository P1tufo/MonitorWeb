## Archivo: ./core/pdf_reports.py

### Resumen Funcional
Este archivo contiene la lógica para construir secciones complejas de PDFs en un sistema de monitoreo de almacén (WMS). Específicamente, define funciones para dibujar tablas de anexos y listas de picking en documentos PDF.

### Catálogo de Funciones y Clases
- `_parse_qty(val) -> float` - Sanitiza y convierte a float valores de cantidad de WMS.
- `_fmt_qty(val) -> str` - Formatea cantidades para mostrar en el PDF de forma legible.
- `draw_annex_table(pdf, grouped_data)` - Dibuja la tabla de índice (anexo) de entregas agrupadas.
- `draw_picking_list(pdf, picking_df)` - Dibuja la lista de picking desglosada por entrega pero con total consolidado.

### Contratos de API / Endpoints
No aplica.

### Interacción con Base de Datos
No aplica.

### Flujo de Datos y Pipeline
1. **Entrada**: Recibe un objeto `pdf` (probablemente una instancia de una biblioteca como ReportLab) y datos agrupados (`grouped_data`) para la tabla de anexos, o un DataFrame (`picking_df`) para la lista de picking.
2. **Transformaciones**:
   - Para `_parse_qty`, limpia y convierte valores de cantidad a float.
   - Para `_fmt_qty`, formatea cantidades para mostrar en el PDF.
   - Para `draw_annex_table`, dibuja una tabla con los datos agrupados, incluyendo encabezado y filas.
   - Para `draw_picking_list`, calcula totales consolidados por área/material, limpia y formatea datos de picking, y dibuja la lista en el PDF.
3. **Salida**: Produce documentos PDF con las tablas de anexos y listas de picking.

### Caché y Estado
No aplica.

### Lógica de Negocio y Reglas
- No hay diccionarios o mapeos hardcoded, constantes de negocio o fórmulas de cálculo específicas en este archivo.

### Dependencias y Flujo
- **Dependencias**: Importa `datetime` desde el módulo estándar de Python.
- **Flujo**: Este archivo no importa a otros archivos del proyecto ni es importado por otros. Es una utilidad compartida dentro del sistema para construir PDFs.

Este archivo es un componente crucial para la generación de documentos PDF en el sistema WMS, proporcionando funciones específicas para crear tablas de anexos y listas de picking de manera eficiente y legible.

