"""
routes/pdf.py — Rutas optimizadas para generación de reportes WMS.
"""
import io
import logging
from core.database import get_session_dep
from sqlalchemy.orm import Session
from sqlalchemy import text
import pandas as pd
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Form, Depends, HTTPException, Response
from fastapi.responses import FileResponse

from config import DB_PATH, PDF_STORAGE
from core.pdf_engine import WMS_Landscape_PDF, draw_delivery_page, get_ots_for_delivery
from core.pdf_queries import get_deliveries_for_bulk, get_area_lookup, get_picking_items
from core.pdf_reports import draw_annex_table, draw_picking_list

logger = logging.getLogger("routes-pdf")
router = APIRouter()

# ─── Dependencias ─────────────────────────────────────────────────────────────

# ─── Rutas ───────────────────────────────────────────────────────────────────

@router.post("/generate-pdf")
async def generate_pdf(
    entrega: str = Form(...),
    include_logo: bool = Form(False),
    action: str = Form("previsualizar"),
    session: Session = Depends(get_session_dep)
):
    """Genera un PDF para una única entrega."""
    try:
        # 1. Obtener datos de la entrega
        df = pd.read_sql(text("SELECT * FROM outbound_deliveries WHERE entrega = :entrega"), session.connection(), params={"entrega": entrega})
        if df.empty:
            raise HTTPException(status_code=404, detail="Entrega no encontrada.")

        # 2. Generar PDF en memoria
        pdf = WMS_Landscape_PDF()
        ots_list = get_ots_for_delivery(entrega, session.connection().connection)
        
        pdf.add_page()
        draw_delivery_page(pdf, df.iloc[0], df, include_logo, ots_list)
        
        # 3. Stream de respuesta
        pdf_bytes = bytes(pdf.output(dest='S')) # Forzar conversión a bytes
        disposition = "attachment" if action == "descargar" else "inline"
        filename = f"Entrega_{entrega}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'{disposition}; filename="{filename}"'}
        )

    except Exception as e:
        logger.error(f"Error generando PDF para entrega {entrega}: {e}")
        raise HTTPException(status_code=500, detail="Error interno generando el reporte.")

@router.post("/generate-pdf-bulk")
async def generate_pdf_bulk(
    date: Optional[str] = Form(None),
    entrega_query: Optional[str] = Form(None),
    area: Optional[str] = Form(None),
    centro: Optional[str] = Form(None),
    has_ots_filter: Optional[str] = Form(None),
    include_logo: bool = Form(False),
    action: str = Form("previsualizar"),
    session: Session = Depends(get_session_dep)
):
    """Genera un reporte masivo con índice y picking list."""
    try:
        # 1. Consultar entregas a procesar
        all_deliveries = get_deliveries_for_bulk(session.connection().connection, date, area, centro, has_ots_filter, entrega_query)
        if all_deliveries.empty:
            return {"error": "No hay datos que coincidan con los filtros."}
            
        area_lookup = get_area_lookup(session.connection().connection)
        all_deliveries = all_deliveries.merge(area_lookup, on='entrega', how='left')

        # Rellenar NaN para evitar errores en groupby y desempaquetado de tuplas
        all_deliveries['area_negocio'] = all_deliveries['area_negocio'].fillna('SIN ÁREA')
        all_deliveries['autor'] = all_deliveries['autor'].fillna('SIN AUTOR')

        all_deliveries_sorted = all_deliveries.sort_values(by=['area_negocio', 'autor'])

        # 2. Preparar índice (Agrupación por área/autor)
        grouped_data = []
        current_p = 2 # El anexo es la pág 1, el picking la pág 2...
        pdf = WMS_Landscape_PDF()
        
        for (area_val, autor), group in all_deliveries_sorted.groupby(['area_negocio', 'autor'], dropna=False):
            area_val = area_val or 'SIN ÁREA'
            autor    = autor    or 'SIN AUTOR'
            entry_list = group['entrega'].tolist()
            num_pages = len(entry_list)
            end_p = current_p + num_pages - 1
            page_range = f"{current_p}" if current_p == end_p else f"{current_p}-{end_p}"
            
            link_id = pdf.add_link()
            pdf.set_link(link_id, page=current_p)
            
            grouped_data.append({
                'autor': autor,
                'area': area_val,
                'entregas': ", ".join(map(str, entry_list)),
                'range': page_range,
                'items': entry_list,
                'link': link_id,
            })
            current_p += num_pages


        # 3. Dibujar Secciones Especiales
        draw_annex_table(pdf, grouped_data)
        
        all_entrega_ids = [e for row in grouped_data for e in row['items']]
        picking_df = get_picking_items(session.connection().connection, all_entrega_ids)
        draw_picking_list(pdf, picking_df)

        # 4. Dibujar Páginas de Entrega
        for row in grouped_data:
            for entrega_id in row['items']:
                try:
                    items_df = pd.read_sql(text("SELECT * FROM outbound_deliveries WHERE entrega = :entrega"), session.connection(), params={"entrega": entrega_id})
                    if not items_df.empty:
                        ots = get_ots_for_delivery(str(entrega_id), session.connection().connection)
                        pdf.add_page()
                        draw_delivery_page(pdf, items_df.iloc[0], items_df, include_logo, ots)
                except Exception as page_err:
                    logger.warning(f"Saltando entrega {entrega_id} por error: {page_err}")
                    continue


        # 5. Respuesta
        pdf_bytes = bytes(pdf.output(dest='S'))
        disposition = "attachment" if action == "descargar" else "inline"
        filename = f"Reporte_Masivo_{datetime.now().strftime('%d%m%y')}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'{disposition}; filename="{filename}"'}
        )

    except Exception as e:
        logger.error(f"Error en generación masiva de PDFs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Fallo en la generación masiva.")
