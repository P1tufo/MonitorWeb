"""
routes/transporte.py — Rutas para la nueva sección de Transporte (Avanti).
"""
import os
import sqlite3
import logging
from typing import List, Dict, Any
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from core.app_instance import templates
from core.database import get_session_dep
from core.auth import get_current_user

logger = logging.getLogger("routes-transporte")
router = APIRouter()

# Rutas externas
EXTERNAL_DB_PATH = "/Users/christianykelly/Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Pruebas/Avanti/entregas.db"
PDF_DIR_PATH = "/Users/christianykelly/Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Pruebas/Avanti/PDFs_por_fecha"

def sync_transporte_logic(session: Session):
    """Lógica core para sincronizar la base de datos externa de OneDrive a local."""
    if not os.path.exists(EXTERNAL_DB_PATH):
        logger.warning("Base de datos externa de transporte no encontrada. Saltando sincronización.")
        return False

    try:
        # 1. Crear tablas si no existen
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS transporte_entregas (
                ot TEXT,
                proveedor TEXT,
                gd TEXT,
                oc TEXT,
                bulto TEXT,
                servicio TEXT,
                archivo TEXT,
                fecha TEXT
            )
        """))
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS transporte_diario (
                fecha TEXT PRIMARY KEY,
                total_entregas INTEGER,
                pdf_path TEXT
            )
        """))
        session.commit()

        # 2. Conectarse a SQLite externa y leer datos
        ext_conn = sqlite3.connect(EXTERNAL_DB_PATH)
        ext_cursor = ext_conn.cursor()
        ext_cursor.execute("SELECT OT, Proveedor, GD, OC, BULTO, Servicio, __archivo__, Fecha FROM entregas")
        rows = ext_cursor.fetchall()
        ext_conn.close()

        # 3. Insertar datos crudos
        session.execute(text("DELETE FROM transporte_entregas"))
        
        insert_query = text("""
            INSERT INTO transporte_entregas (ot, proveedor, gd, oc, bulto, servicio, archivo, fecha) 
            VALUES (:ot, :proveedor, :gd, :oc, :bulto, :servicio, :archivo, :fecha)
        """)
        
        params_list = [
            {"ot": r[0], "proveedor": r[1], "gd": r[2], "oc": r[3], "bulto": r[4], "servicio": r[5], "archivo": r[6], "fecha": r[7]}
            for r in rows
        ]
        
        if params_list:
            session.execute(insert_query, params_list)
        
        # 4. Consolidar datos
        session.execute(text("DELETE FROM transporte_diario"))
        
        consolidation_query = text("""
            INSERT INTO transporte_diario (fecha, total_entregas, total_bultos, pdf_path)
            SELECT fecha, COUNT(*) as total_entregas, SUM(CAST(bulto AS INTEGER)) as total_bultos, NULL
            FROM transporte_entregas
            WHERE fecha IS NOT NULL AND TRIM(fecha) != ''
            GROUP BY fecha
        """)
        session.execute(consolidation_query)
        
        # 5. Mapear PDFs
        fechas = session.execute(text("SELECT fecha FROM transporte_diario")).fetchall()
        for f_row in fechas:
            fecha_str = f_row[0]
            expected_pdf_name = f"Reporte_{fecha_str}.pdf"
            full_pdf_path = os.path.join(PDF_DIR_PATH, expected_pdf_name)
            
            if os.path.exists(full_pdf_path):
                session.execute(text("UPDATE transporte_diario SET pdf_path = :path WHERE fecha = :fecha"), {"path": expected_pdf_name, "fecha": fecha_str})
                
        session.commit()
        return True

    except Exception as e:
        session.rollback()
        logger.error(f"Error sincronizando transporte: {e}")
        raise

@router.post("/api/transporte/sync")
def sync_transporte(session: Session = Depends(get_session_dep), user=Depends(get_current_user)):
    """(Mantenido por compatibilidad) Sincroniza datos de transporte manualmente."""
    try:
        success = sync_transporte_logic(session)
        if not success:
            raise HTTPException(status_code=404, detail="Base de datos externa no encontrada.")
        return {"status": "success", "message": "Datos sincronizados correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/api/transporte/data")
def get_transporte_data(session: Session = Depends(get_session_dep), user=Depends(get_current_user)):
    """Retorna los datos consolidados diarios ordenados cronológicamente."""
    try:
        session.execute(text("""
            CREATE TABLE IF NOT EXISTS transporte_diario (
                fecha TEXT PRIMARY KEY,
                total_entregas INTEGER,
                total_bultos INTEGER,
                pdf_path TEXT
            )
        """))
        session.commit()

        # Asegurar que la columna total_bultos existe en tablas antiguas
        try:
            session.execute(text("ALTER TABLE transporte_diario ADD COLUMN total_bultos INTEGER"))
            session.commit()
        except Exception:
            pass # Si ya existe, ignorar error

        query = text("""
            SELECT fecha, total_entregas, total_bultos, pdf_path 
            FROM transporte_diario 
            ORDER BY fecha ASC
        """)
        res = session.execute(query).fetchall()
        
        data = []
        for r in res:
            data.append({
                "fecha": r[0],
                "total_entregas": r[1],
                "total_bultos": r[2] or 0,
                "has_pdf": r[3] is not None,
                "pdf_filename": r[3]
            })
            
        return {"data": data}
    except Exception as e:
        logger.warning(f"Aviso de datos de transporte: {e}")
        return {"data": []}

@router.get("/api/transporte/search")
def search_transporte(q: str, session: Session = Depends(get_session_dep), user=Depends(get_current_user)):
    """Busca en la tabla cruda de transporte_entregas por OT, GD o OC."""
    if not q or len(q) < 3:
        return {"data": []}
    
    try:
        search_query = f"%{q}%"
        query = text("""
            SELECT fecha, ot, gd, oc, proveedor, bulto, servicio 
            FROM transporte_entregas 
            WHERE ot LIKE :q OR gd LIKE :q OR oc LIKE :q
            ORDER BY fecha DESC
            LIMIT 5
        """)
        res = session.execute(query, {"q": search_query}).fetchall()
        
        data = []
        for r in res:
            data.append({
                "fecha": r[0] or "-",
                "ot": r[1] or "-",
                "gd": r[2] or "-",
                "oc": r[3] or "-",
                "proveedor": r[4] or "-",
                "bultos": r[5] or "0",
                "servicio": r[6] or "-"
            })
            
        return {"data": data}
    except Exception as e:
        logger.warning(f"Error en búsqueda de transporte: {e}")
        return {"data": []}

@router.get("/api/transporte/pdf/{filename}")
def serve_pdf(filename: str, user=Depends(get_current_user)):
    """Sirve el archivo PDF desde el disco."""
    # Validación básica de seguridad
    if ".." in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="Nombre de archivo inválido.")
        
    full_path = os.path.join(PDF_DIR_PATH, filename)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="El archivo PDF no existe en el servidor.")
        
    return FileResponse(full_path, media_type="application/pdf", headers={"Content-Disposition": f'inline; filename="{filename}"'})
