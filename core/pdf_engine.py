"""
core/pdf_engine.py — Motor optimizado de generación de PDFs WMS.
"""
import io
import logging
import sqlite3
from datetime import datetime
from typing import Final, List, Optional
from pathlib import Path

import numpy as np
import pandas as pd
from fpdf import FPDF
from barcode import Code128
from barcode.writer import ImageWriter

from config import TEMP_DIR

# Configuración de Logging
logger = logging.getLogger("pdf-engine")

# Constantes de Diseño
MARGIN_X: Final[float] = 10.0
MARGIN_Y: Final[float] = 10.0
TABLE_Y_START: Final[float] = 58.0
ROW_HEIGHT: Final[float] = 6.0
MAX_ROWS: Final[int] = 25
BARCODE_W: Final[float] = 35.0
BARCODE_H: Final[float] = 10.0

class WMS_Landscape_PDF(FPDF):
    """Clase base para reportes WMS en formato horizontal."""
    def __init__(self):
        super().__init__(orientation='L', unit='mm', format='Letter')
        self.set_margins(MARGIN_X, MARGIN_Y, MARGIN_X)
        self.f_factor = 1.58
        self.cols = {
            2: 10.33 * self.f_factor, 3: 14.16 * self.f_factor, 4: 15.5 * self.f_factor,
            5: 15.16 * self.f_factor, 6: 16.16 * self.f_factor,
            7: 13.0 * self.f_factor, 8: 13.0 * self.f_factor, 9: 13.0 * self.f_factor,
            10: 13.0 * self.f_factor, 11: 13.0 * self.f_factor,
            12: 14.5 * self.f_factor, 13: 2.5 * self.f_factor,
        }

    def get_column_x(self, col: int) -> float:
        """Calcula la posición X de una columna específica."""
        return MARGIN_X + sum(self.cols.get(c, 0) for c in range(2, col))

    def draw_dotted_line(self, x1: float, y: float, x2: float) -> None:
        """Dibuja una línea punteada sutil."""
        self.set_line_width(0.1)
        self.dashed_line(x1, y, x2, y, dash_length=0.5, space_length=0.5)

def get_ots_for_delivery(entrega_id: str, conn: sqlite3.Connection) -> List[str]:
    """Consulta las OTs asociadas a una entrega y las devuelve como lista de strings."""
    query = """
    SELECT DISTINCT numero_ot
    FROM warehouse_tasks
    WHERE ltrim(CAST(entrega AS TEXT), '0') = ?
    """
    try:
        clean_id = str(entrega_id).lstrip('0')
        df = pd.read_sql(query, conn, params=[clean_id])
        return [str(int(x)) for x in df['numero_ot'].dropna() if int(x) != 0]
    except Exception as e:
        logger.error(f"Error consultando OTs para {entrega_id}: {e}")
        return []

def _generate_barcode_stream(data: str, options: Optional[dict] = None) -> io.BytesIO:
    """Genera un código de barras en memoria (BytesIO)."""
    fp = io.BytesIO()
    writer = ImageWriter()
    bc = Code128(str(data), writer=writer)
    bc.write(fp, options=options or {})
    fp.seek(0)
    return fp

def draw_delivery_page(
    pdf: WMS_Landscape_PDF,
    header: pd.Series,
    items: pd.DataFrame,
    include_logo: bool = True,
    ots_list: Optional[List[str]] = None
) -> None:
    """Dibuja una página de entrega completa utilizando sub-métodos modulares."""
    
    _draw_page_header(pdf, header, include_logo)
    _draw_info_block(pdf, header)
    _draw_table(pdf, items)
    
    if ots_list:
        _draw_ot_barcodes(pdf, ots_list)
    
    _draw_signature_block(pdf)

def _draw_page_header(pdf: WMS_Landscape_PDF, h: pd.Series, include_logo: bool):
    """Dibuja el encabezado superior, logo y código de barras de la entrega."""
    if include_logo:
        pdf.set_font("Helvetica", 'B', 36)
        pdf.set_text_color(80, 80, 80)
        pdf.text(12, 22, "arauco")

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", '', 8)
    pdf.text(245, 12, f"Impreso {datetime.now().strftime('%d-%m-%y')}")
    pdf.set_font("Helvetica", 'B', 16)
    pdf.text(230, 28, "PRODUCCIÓN")

    # Entrega Barcode (En memoria)
    try:
        bc_stream = _generate_barcode_stream(str(h.get('entrega', '')))
        pdf.image(bc_stream, x=235, y=14, w=BARCODE_W, h=BARCODE_H)
    except Exception as e:
        logger.warning(f"No se pudo generar barcode de entrega: {e}")

    # Referencia y Generador
    pdf.set_font("Helvetica", '', 9)
    pdf.text(80, 18, "Referencia")
    pdf.set_font("Helvetica", 'B', 9)
    pdf.text(105, 18, str(h.get('referencia', '')))

    pdf.set_font("Helvetica", '', 9)
    pdf.text(80, 26, "Generador")
    pdf.set_font("Helvetica", 'B', 9)
    pdf.text(105, 26, str(h.get('autor', '')))

def _draw_info_block(pdf: WMS_Landscape_PDF, h: pd.Series):
    """Dibuja el bloque de información principal de la entrega."""
    pdf.set_fill_color(220, 220, 220)
    pdf.rect(10, 32, 259, 8, 'F')
    pdf.set_font("Helvetica", 'B', 12)
    pdf.set_xy(10, 32)
    pdf.cell(259, 8, "RESERVA / SALIDA DE BODEGA", border=1, align='C')

    pdf.set_font("Helvetica", '', 10)
    pdf.text(20, 50, "Nº Entrega:")
    pdf.set_font("Helvetica", 'B', 10)
    pdf.text(45, 50, str(h.get('entrega', '')))

    pdf.set_font("Helvetica", 'B', 10)
    pdf.text(20, 55, "Centro/Almacen:")
    pdf.set_font("Helvetica", '', 10)
    pdf.text(50, 55, "TA04 - Trupan Cholguan | Bodega Central")

    pdf.set_font("Helvetica", 'B', 10)
    pdf.text(80, 50, "Clase Motivo: 201 - SM centro costo")
    pdf.text(170, 50, f"Centro Costo: {h.get('centro_costo', '')}")
    pdf.text(235, 50, f"Fecha: {h.get('fecha_carga', '')}")

def _draw_table(pdf: WMS_Landscape_PDF, items_df: pd.DataFrame):
    """Dibuja la tabla de materiales con ordenamiento por ubicación."""
    # Header de tabla
    pdf.set_xy(10, TABLE_Y_START)
    pdf.set_line_width(0.5)
    pdf.line(10, TABLE_Y_START, 269, TABLE_Y_START)
    pdf.line(10, TABLE_Y_START + 8, 269, TABLE_Y_START + 8)

    pdf.set_font("Helvetica", '', 9)
    headers = ["Pos.", "Ubi.", "Material", "Denominación", "Cantidad", "Cant.Desp"]
    cols_idx = [2, 3, 4, 5, 9, 10]
    for i, idx in enumerate(cols_idx):
        pdf.set_xy(pdf.get_column_x(idx), TABLE_Y_START + 1)
        w = pdf.cols.get(idx) if idx != 5 else pdf.cols.get(5) * 4
        pdf.cell(w, 6, headers[i], align='C' if i != 3 else 'L')

    # Datos ordenados
    df = items_df.copy()
    if 'ubicacion_bin' in df.columns:
        df['u_sort'] = df['ubicacion_bin'].replace(r'^\s*$', np.nan, regex=True)
        df = df.sort_values(by='u_sort', na_position='last').reset_index(drop=True)

    y = TABLE_Y_START + 10
    pdf.set_font("Helvetica", '', 8)
    
    for i, row in df.iterrows():
        if i >= MAX_ROWS: break
        
        pdf.set_xy(pdf.get_column_x(2), y)
        pdf.cell(pdf.cols.get(2), ROW_HEIGHT, str(row.get('pos_', i + 1)), align='C')
        pdf.cell(pdf.cols.get(3), ROW_HEIGHT, str(row.get('ubicacion_bin', '')), align='C')
        pdf.cell(pdf.cols.get(4), ROW_HEIGHT, str(row.get('material', '')), align='C')
        pdf.cell(pdf.cols.get(5) * 4, ROW_HEIGHT, str(row.get('denominacion', ''))[:75], align='L')
        pdf.set_xy(pdf.get_column_x(9), y)
        pdf.cell(pdf.cols.get(9), ROW_HEIGHT, f"{row.get('cantidad', '')} {row.get('umb', '')}".strip(), align='R')
        
        y += ROW_HEIGHT
        pdf.draw_dotted_line(15, y, 260)

def _draw_ot_barcodes(pdf: WMS_Landscape_PDF, ots: List[str]):
    """Dibuja los códigos de barras de las OTs en el lateral derecho."""
    ot_x, ot_y = 230, 65
    opts = {"write_text": True, "module_width": 0.4, "module_height": 5, "font_size": 7}
    
    for i, ot in enumerate(ots[:8]): # Límite de 8 barcodes por página
        try:
            bc_stream = _generate_barcode_stream(ot, options=opts)
            pdf.image(bc_stream, x=ot_x, y=ot_y, w=BARCODE_W, h=0)
            ot_y += 15
        except Exception as e:
            logger.warning(f"Error barcode OT {ot}: {e}")

def _draw_signature_block(pdf: WMS_Landscape_PDF):
    """Dibuja los cuadros de firma al final de la página."""
    f_y = 165
    pdf.set_line_width(0.6)
    pdf.rect(20, f_y, 80, 25)
    pdf.rect(110, f_y, 80, 25)
    pdf.rect(200, f_y, 60, 25)

    pdf.set_font("Helvetica", 'B', 9)
    pdf.text(45, f_y + 22, "Autorizado por")
    pdf.text(135, f_y + 22, "Recibi Conforme")
    pdf.text(220, f_y + 22, "Procesado")
