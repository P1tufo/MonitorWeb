"""
routes/sync.py — Rutas de sincronización de datos con gestión de concurrencia.
Usa TaskManager (Pilar 4) para ejecución trazable en segundo plano.
"""
import logging
import shutil
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import APIRouter, HTTPException, Depends
from core.auth import require_auth

from config import (
    DB_PATH, CLEANSED_DIR, PDF_STORAGE, DELIVERIES_DIR, STOCK_DIR, TASKS_DIR,
    INVENTORY_DIR, TUNNEL_URL_FILE,
)
from core.state import AppState, get_app_state

from core.task_manager import task_manager
from db.consolidator import DataConsolidator

logger = logging.getLogger("routes-sync")
router = APIRouter(dependencies=[Depends(require_auth)])

# ─── Rutas ───────────────────────────────────────────────────────────────────

@router.get("/url")
async def get_tunnel_url(state: AppState = Depends(get_app_state)):
    """Retorna la URL pública del túnel (Ngrok)."""
    tunnel_file = Path(TUNNEL_URL_FILE)
    if tunnel_file.exists():
        try:
            url = tunnel_file.read_text().strip()
            return {"url": url, "local": "http://localhost:8000"}
        except Exception as e:
            logger.error(f"Error leyendo archivo de túnel: {e}")
            
    return {"url": None, "local": "http://localhost:8000", "message": "Túnel no activo."}
    
@router.get("/status")
async def get_sync_status(state: AppState = Depends(get_app_state)):
    """Retorna el estado actual de la sincronización."""
    return {
        "is_syncing": state.is_syncing,
        "status": "busy" if state.is_syncing else "idle"
    }

@router.post("/sync")
async def sync_data(state: AppState = Depends(get_app_state)):
    """
    Inicia el proceso de sincronización de datos.
    Encola la tarea en el TaskManager para ejecución trazable en segundo plano.
    """
    logger.info(">>> [POST /sync] Petición de sincronización recibida.")
    
    if state.is_syncing or task_manager.has_running_task("sync_data"):
        return {"status": "error", "message": "Sincronización en curso."}

    task_id = task_manager.submit_task("sync_data", _run_sync_pipeline)
    
    return {
        "status": "success", 
        "message": "Proceso iniciado en segundo plano.",
        "task_id": task_id,
    }

# ─── API: Monitoreo de Tareas ────────────────────────────────────────────────

@router.get("/api/tasks")
async def list_tasks(limit: int = 20, state: AppState = Depends(get_app_state)):
    """Lista las tareas recientes del sistema."""
    return {"tasks": task_manager.list_tasks(limit)}

@router.get("/api/tasks/{task_id}")
async def get_task(task_id: str, state: AppState = Depends(get_app_state)):
    """Consulta el estado de una tarea específica por su ID."""
    status = task_manager.get_task_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return status

# ─── Lógica de Fondo (Pipeline) ──────────────────────────────────────────────

def _run_sync_pipeline():
    """Ejecuta el pipeline completo de limpieza y consolidación."""
    state = get_app_state()
    # Intentar adquirir el bloqueo sin esperar (non-blocking)
    if not state.sync_lock.acquire(blocking=False):
        logger.warning("Intento de sincronización duplicado detectado.")
        return

    try:
        state.is_syncing = True
        logger.info(">>> Iniciando Pipeline de Sincronización Global...")

        from core.database import get_session
        from core.wms_utils import is_file_changed, mark_file_processed
        
        has_changes = False

        # 1. Obtener Rutas Dinámicas (SaaS Config)
        from core import wms_config
        
        base_path = Path(wms_config.ONEDRIVE_PATH)
        deliveries_path = base_path / wms_config.DIR_DELIVERIES
        stock_path = base_path / wms_config.DIR_STOCK
        tasks_path = base_path / wms_config.DIR_TASKS
        inventory_path = base_path / wms_config.DIR_MOVEMENTS
        try:
            lx02_pendientes_path = base_path / wms_config.DIR_LX02_PENDIENTES
        except AttributeError:
            lx02_pendientes_path = base_path / "LX02_Pendientes"

        # 2. Preparar directorios
        Path(CLEANSED_DIR).mkdir(parents=True, exist_ok=True)
        _reset_directory(PDF_STORAGE) 

        # 3. Limpieza de archivos (Fase Incremental)
        if deliveries_path.exists():
            with get_session() as session:
                for f in deliveries_path.iterdir():
                    if f.suffix.lower() in ['.xlsx', '.xls', '.txt']:
                        out_f = Path(CLEANSED_DIR) / f"clean_{f.name}.xlsx"
                        
                        # Solo procesar si el archivo fuente cambió o el destino no existe
                        if is_file_changed(session, f) or not out_f.exists():
                            logger.info(f"Procesando cambio en: {f.name}")
                            from services.etl import OutboundDeliveryAdapter
                            df_clean = OutboundDeliveryAdapter().read_and_clean_data(f)
                            if not df_clean.empty:
                                df_clean.to_excel(out_f, index=False)
                            rows = len(df_clean) if df_clean is not None else 0
                            mark_file_processed(session, f, row_count=rows)
                            has_changes = True
                        else:
                            logger.debug(f"Sin cambios en fuente: {f.name}")

        # 3. Consolidación en Base de Datos
        with DataConsolidator(DB_PATH) as con:
            # Entregas (Ya es incremental dentro de con.consolidate_folder)
            processed_count = con.consolidate_folder(CLEANSED_DIR)
            if processed_count > 0:
                has_changes = True

            # Stock
            if stock_path.exists():
                # Encontrar el archivo más reciente para ver si cambió
                files = [f for f in stock_path.iterdir() if f.suffix.lower() in {'.txt', '.xlsx'} and '_' in f.name]
                if files:
                    latest = sorted(files, key=con._parse_file_date, reverse=True)[0]
                    if is_file_changed(con.conn, latest):
                        rows = con.overwrite_with_latest(str(stock_path), table_name="stock_levels")
                        con.enrich_deliveries_with_stock()
                        mark_file_processed(con.conn, latest, row_count=rows)
                        has_changes = True
                    else:
                        logger.debug(f"Stock sin cambios ({latest.name})")

            # Inventario
            # Inventario
            if inventory_path.exists():
                from db.inventory_processor import process_inventory_file
                for mb_file in inventory_path.glob("*"):
                    if mb_file.suffix.lower() in ['.txt', '.csv', '.xlsx'] and not mb_file.name.startswith('~'):
                        if is_file_changed(con.conn, mb_file):
                            rows = process_inventory_file(str(mb_file), str(DB_PATH), conn=con.conn)
                            mark_file_processed(con.conn, mb_file, row_count=rows)
                            has_changes = True
                        else:
                            logger.debug(f"Movimientos sin cambios ({mb_file.name})")

            # Tareas de Bodega
            if tasks_path.exists():
                from db.warehouse_tasks_processor import process_tasks_file
                for lt_file in tasks_path.glob("*"):
                    if lt_file.suffix.lower() in ['.txt', '.csv', '.xlsx'] and not lt_file.name.startswith('~'):
                        if is_file_changed(con.conn, lt_file):
                            rows = process_tasks_file(str(lt_file), str(DB_PATH), conn=con.conn)
                            mark_file_processed(con.conn, lt_file, row_count=rows)
                            has_changes = True
                        else:
                            logger.debug(f"Tareas sin cambios ({lt_file.name})")

            # Documentos No Paletizados (LX02_Pendientes)
            if lx02_pendientes_path.exists():
                from db.lx02_processor import process_lx02_pendientes
                cambios_lx02 = False
                for lx_file in lx02_pendientes_path.glob("*"):
                    if lx_file.suffix.lower() in ['.txt', '.csv', '.xlsx'] and not lx_file.name.startswith('~'):
                        if is_file_changed(con.conn, lx_file):
                            cambios_lx02 = True
                            mark_file_processed(con.conn, lx_file, row_count=0)
                
                if cambios_lx02:
                    rows = process_lx02_pendientes(str(lx02_pendientes_path), str(DB_PATH), conn=con.conn)
                    if rows > 0:
                        has_changes = True
            
            # Enriquecimiento final cruzado (Solo si hubo cambios en algo)
            if has_changes:
                con.backfill_from_movements()
                con.backfill_texts()  # <-- Asegura descripciones en picking list
                con.update_sla_with_tasks()  # <-- Cruce automático de Tareas para SLA
                
                # 4. Limpiar caché global para forzar recarga de gráficos
                state.clear_cache()
                try:
                    con.conn.execute("DELETE FROM analytics_snapshots")
                    logger.info("Snapshots de base de datos eliminados tras sincronización de nuevos datos.")
                except Exception as e:
                    logger.warning(f"No se pudo limpiar la tabla de snapshots en consolidación: {e}")
                logger.info(">>> Sincronización finalizada exitosamente. Datos actualizados y caché invalidada.")
            else:
                # Incluso si no hubo cambios en archivos, corremos backfill por seguridad
                con.backfill_texts()
                con.update_sla_with_tasks()
                logger.info(">>> Sincronización finalizada: No se detectaron cambios en los archivos fuente.")

    except Exception as e:
        logger.error(f"Fallo crítico en el pipeline de sincronización: {e}", exc_info=True)
        raise  # Re-raise para que TaskManager capture el error
    finally:
        state.is_syncing = False
        state.sync_lock.release()

def _reset_directory(path: str):
    """Elimina y recrea un directorio de forma segura."""
    p = Path(path)
    if p.exists():
        shutil.rmtree(p)
    p.mkdir(parents=True, exist_ok=True)
