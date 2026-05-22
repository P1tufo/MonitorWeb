"""core/pdf_reports.py — Lógica de construcción de secciones complejas de PDF (Anexos y Picking)."""
from datetime import datetime

def _parse_qty(val):
    """Sanitiza y convierte a float valores de cantidad de WMS."""
    if val is None or val == "":
        return 0.0
    try:
        s = str(val).strip().replace(' ', '')
        if not s:
            return 0.0
        
        # Manejo de separadores WMS (punto para miles, coma para decimales)
        if ',' in s:
            if '.' in s:
                # Caso 1.234,56 -> 1234.56
                s = s.replace('.', '').replace(',', '.')
            else:
                # Caso 1234,56 -> 1234.56
                s = s.replace(',', '.')
        elif s.count('.') > 1:
            # Caso 1.234.567 -> 1234567
            s = s.replace('.', '')
        elif s.count('.') == 1:
            # Caso ambiguo: 1.234 puede ser mil o decimal. 
            # Si tiene 3 dígitos después del punto, asumimos miles (WMS standard)
            parts = s.split('.')
            if len(parts[1]) == 3 and len(parts[0]) > 0:
                 s = s.replace('.', '')
        
        return float(s)
    except (ValueError, TypeError): 
        return 0.0

def _fmt_qty(val):
    """Formatea cantidades para mostrar en el PDF de forma legible."""
    try:
        v = _parse_qty(val)
        return str(int(v)) if v == int(v) else f"{v:.2f}"
    except (ValueError, TypeError):
        return str(val) if val else "0"


def draw_annex_table(pdf, grouped_data):
    """
    Dibuja la tabla de índice (anexo) de entregas agrupadas.
    """
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 20)
    pdf.cell(0, 20, "ANEXO DE DESPACHOS CONSOLIDADOS", align='C', ln=True)
    pdf.set_font("Helvetica", '', 10)
    pdf.cell(0, 10, f"Fecha Reporte: {datetime.now().strftime('%d/%m/%Y %H:%M')}", align='C', ln=True)
    pdf.ln(5)

    def _draw_annex_header():
        pdf.set_fill_color(220, 220, 220)
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(70, 10, "Autor / Referencia", border=1, fill=True)
        pdf.cell(50, 10, "Area", border=1, fill=True)
        pdf.cell(60, 10, "Entregas", border=1, fill=True)
        pdf.cell(30, 10, "Paginas", border=1, fill=True)
        pdf.ln()
        pdf.set_font("Helvetica", '', 9)

    _draw_annex_header()

    ROW_H = 8
    pdf.set_auto_page_break(False)
    page_bottom = pdf.h - pdf.b_margin
    pdf.set_font("Helvetica", '', 9)

    def _draw_annex_row(row):
        pdf.cell(70, ROW_H, str(row['autor']), border=1)
        pdf.cell(50, ROW_H, str(row['area']), border=1)
        pdf.set_text_color(0, 0, 255)
        pdf.cell(60, ROW_H, str(row['entregas'])[:30] + ("..." if len(str(row['entregas'])) > 30 else ""), border=1, link=row['link'])
        pdf.cell(30, ROW_H, str(row['range']), border=1, align='C', link=row['link'])
        pdf.set_text_color(0, 0, 0)
        pdf.ln()

    for row in grouped_data:
        if pdf.get_y() + ROW_H > page_bottom:
            pdf.add_page()
            pdf.set_font("Helvetica", 'B', 10)
            pdf.cell(0, 8, "ANEXO DE DESPACHOS CONSOLIDADOS (cont.)", align='C', ln=True)
            pdf.ln(2)
            _draw_annex_header()
        _draw_annex_row(row)
    pdf.set_auto_page_break(True)

def draw_picking_list(pdf, picking_df):
    """
    Dibuja la lista de picking desglosada por entrega pero con total consolidado.
    """
    if picking_df.empty:
        return

    pdf.ln(8)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "LISTA DE PICKING - RUTA DE RECOLECCION (DESGLOSADA)", align='C', ln=True)
    pdf.set_font("Helvetica", '', 9)
    pdf.cell(0, 6, f"Total materiales: {len(picking_df)} entregas parciales en {picking_df['ubicacion'].nunique()} ubicaciones", align='C', ln=True)
    pdf.ln(4)

    # Calcular totales consolidados por Area/Material para la columna 'Total'
    totals_map = (
        picking_df
        .assign(qty_num=picking_df['cantidad'].apply(_parse_qty))
        .groupby(['area', 'material'])['qty_num']
        .sum()
    )

    # Anchos de columna (incluyendo columna Total)
    W = {'ubi': 35, 'mat': 22, 'desc': 62, 'cant': 15, 'umb': 12, 'tot': 18, 'area': 35}

    def _draw_picking_header():
        pdf.set_fill_color(50, 50, 50)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", 'B', 8)
        pdf.cell(W['ubi'], 8, "Ubicacion", border=1, fill=True)
        pdf.cell(W['mat'], 8, "Material", border=1, fill=True)
        pdf.cell(W['desc'], 8, "Descripcion", border=1, fill=True)
        pdf.cell(W['cant'], 8, "Cant.", border=1, fill=True, align='C')
        pdf.cell(W['umb'], 8, "Umb", border=1, fill=True, align='C')
        pdf.cell(W['tot'], 8, "Total", border=1, fill=True, align='C')
        pdf.cell(W['area'], 8, "Area", border=1, fill=True)
        pdf.ln()
        pdf.set_text_color(0, 0, 0)

    _draw_picking_header()

    def _draw_picking_row(r, seen_totals, PICK_ROW_H):
        pdf.set_font("Helvetica", '', 7.5)
        pdf.cell(W['ubi'], PICK_ROW_H, str(r['ubicacion'])[:20], border=1)
        pdf.cell(W['mat'], PICK_ROW_H, str(r['material'])[:12], border=1)
        pdf.cell(W['desc'], PICK_ROW_H, str(r['descripcion'])[:34] + ("..." if len(str(r['descripcion'])) > 34 else ""), border=1)
        
        # Cantidad por Entrega (Sanitizada)
        qty_val = _fmt_qty(r['cantidad'])
        pdf.cell(W['cant'], PICK_ROW_H, qty_val, border=1, align='C')
        
        pdf.cell(W['umb'], PICK_ROW_H, str(r['umb'])[:5], border=1, align='C')
        
        # Lógica de Total Consolidado (Solo la primera vez por grupo)
        mat_key = (r['area'], str(r['material']))
        if mat_key not in seen_totals:
            seen_totals.add(mat_key)
            total_val = totals_map.get(mat_key, 0)
            pdf.set_font("Helvetica", 'B', 8)
            pdf.cell(W['tot'], PICK_ROW_H, _fmt_qty(total_val), border=1, align='C', fill=True)
            pdf.set_font("Helvetica", '', 7.5)
        else:
            pdf.cell(W['tot'], PICK_ROW_H, "", border=1)
            
        pdf.cell(W['area'], PICK_ROW_H, str(r['area'])[:15], border=1)
        pdf.ln()

    prev_area = None
    seen_totals = set()
    PICK_ROW_H = 7.5
    pdf.set_auto_page_break(False)
    pick_bottom = pdf.h - pdf.b_margin

    for _, r in picking_df.iterrows():
        if pdf.get_y() + PICK_ROW_H > pick_bottom:
            pdf.add_page()
            pdf.set_font("Helvetica", 'B', 10)
            pdf.cell(0, 8, "LISTA DE PICKING - RUTA DE RECOLECCION (cont.)", align='C', ln=True)
            pdf.ln(2)
            _draw_picking_header()
            prev_area = None

        # Barrido por Área
        if r['area'] != prev_area:
            pdf.set_fill_color(235, 235, 235)
            pdf.set_font("Helvetica", 'B', 8)
            prev_area = r['area']
            pdf.cell(sum(W.values()), 6, f">>> AREA: {prev_area}", border=1, fill=True, ln=True)

        _draw_picking_row(r, seen_totals, PICK_ROW_H)

    pdf.set_auto_page_break(True)
