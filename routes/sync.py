"""
routes/sync.py — Rutas de sincronización de datos con gestión de concurrencia.
Usa TaskManager (Pilar 4) para ejecución trazable en segundo plano.
"""
import logging
import shutil
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException

    DB_PATH,
    DELIVERIES_DIR,
    INVENTORY_DIR,
    STOCK_DIR,
    TASKS_DIR,
    TUNNEL_URL_FILE,
)
from core.auth import require_auth
from core.state import CacheManager, SyncStateManager, get_cache_manager, get_sync_manager
from core.task_manager import task_manager
from db.consolidator import DataConsolidator

logger = logging.getLogger("routes-sync")
router = APIRouter()

# ─── Rutas ───────────────────────────────────────────────────────────────────

@router.get("/url")
async def get_tunnel_url():
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
async def get_sync_status(sync: SyncStateManager = Depends(get_sync_manager)):
    """Retorna el estado actual de la sincronización."""
    return {
        "is_syncing": sync.is_syncing,
        "status": "busy" if sync.is_syncing else "idle"
    }

@router.post("/sync")
async def sync_data(sync: SyncStateManager = Depends(get_sync_manager), admin = Depends(require_auth)):
    """
    Inicia el proceso de sincronización de datos.
    Encola la tarea en el TaskManager para ejecución trazable en segundo plano.
    """
    logger.info(">>> [POST /sync] Petición de sincronización recibida.")

    if sync.is_syncing or task_manager.has_running_task("sync_data"):
        return {"status": "error", "message": "Sincronización en curso."}

    task_id = task_manager.submit_task("sync_data", _run_sync_pipeline)

    return {
        "status": "success",
        "message": "Proceso iniciado en segundo plano.",
        "task_id": task_id,
    }

# ─── API: Monitoreo de Tareas ────────────────────────────────────────────────

@router.get("/api/tasks")
async def list_tasks(limit: int = 20, admin = Depends(require_auth)):
    """Lista las tareas recientes del sistema."""
    return {"tasks": task_manager.list_tasks(limit)}

@router.get("/api/tasks/{task_id}")
async def get_task(task_id: str, admin = Depends(require_auth)):
    """Consulta el estado de una tarea específica por su ID."""
    status = task_manager.get_task_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return status

# ─── Lógica de Fondo (Pipeline) ──────────────────────────────────────────────

def _run_sync_pipeline():
    """Ejecuta el pipeline completo de limpieza y consolidación."""
    cache = get_cache_manager()
    sync = get_sync_manager()
    # Intentar adquirir el bloqueo sin esperar (non-blocking)
    if not sync.sync_lock.acquire(blocking=False):
        logger.warning("Intento de sincronización duplicado detectado.")
        return

    try:
        sync.is_syncing = True
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

        try:
            iw39_path = base_path / wms_config.DIR_IW39
        except AttributeError:
            iw39_path = base_path / "IW39"

        # 2. (Vacío por remoción de PDF_STORAGE)

        # 3. Consolidación en Base de Datos
        with DataConsolidator(DB_PATH) as con:
            # Entregas (Procesa directamente desde OneDrive sin copias intermedias)
            if deliveries_path.exists():
                processed_count = con.consolidate_folder(str(deliveries_path))
                if processed_count > 0:
                    has_changes = True

            # Stock
            if stock_path.exists():
                # Encontrar el archivo más reciente para ver si cambió
                files = [f for f in stock_path.iterdir() if f.suffix.lower() in {'.txt', '.xlsx'} and '_' in f.name]
                if files:
                    latest = sorted(files, key=con._parse_file_date, reverse=True)[0]
                    with get_session() as _sess_stock:
                        changed = is_file_changed(_sess_stock, latest)
                    if changed:
                        rows = con.overwrite_with_latest(str(stock_path), table_name="stock_levels")
                        con.enrich_deliveries_with_stock()
                        with get_session() as _sess_stock:
                            mark_file_processed(_sess_stock, latest, row_count=rows)
                        has_changes = True
                    else:
                        logger.debug(f"Stock sin cambios ({latest.name})")

            # Inventario (services/etl/movements.py → InventoryMovementAdapter)
            if inventory_path.exists():
                from services.etl import process_inventory_file
                for mb_file in inventory_path.glob("*"):
                    if mb_file.suffix.lower() in ['.txt', '.csv', '.xlsx'] and not mb_file.name.startswith('~'):
                        with get_session() as _sess_inv:
                            changed = is_file_changed(_sess_inv, mb_file)
                        if changed:
                            rows = process_inventory_file(str(mb_file), str(DB_PATH), conn=con.conn)
                            with get_session() as _sess_inv:
                                mark_file_processed(_sess_inv, mb_file, row_count=rows)
                            has_changes = True
                        else:
                            logger.debug(f"Movimientos sin cambios ({mb_file.name})")

            # Tareas de Bodega (services/etl/tasks.py → WarehouseTaskAdapter)
            if tasks_path.exists():
                from services.etl import process_tasks_file
                for lt_file in tasks_path.glob("*"):
                    if lt_file.suffix.lower() in ['.txt', '.csv', '.xlsx'] and not lt_file.name.startswith('~'):
                        with get_session() as _sess_tasks:
                            changed = is_file_changed(_sess_tasks, lt_file)
                        if changed:
                            rows = process_tasks_file(str(lt_file), str(DB_PATH), conn=con.conn)
                            with get_session() as _sess_tasks:
                                mark_file_processed(_sess_tasks, lt_file, row_count=rows)
                            has_changes = True
                        else:
                            logger.debug(f"Tareas sin cambios ({lt_file.name})")

            # Documentos No Paletizados (services/etl/stock.py → StockLevelAdapter)
            if lx02_pendientes_path.exists():
                from services.etl import process_lx02_pendientes
                cambios_lx02 = False
                for lx_file in lx02_pendientes_path.glob("*"):
                    if lx_file.suffix.lower() in ['.txt', '.csv', '.xlsx'] and not lx_file.name.startswith('~'):
                        with get_session() as _sess_lx:
                            changed = is_file_changed(_sess_lx, lx_file)
                        if changed:
                            cambios_lx02 = True
                            with get_session() as _sess_lx:
                                mark_file_processed(_sess_lx, lx_file, row_count=0)

                if cambios_lx02:
                    rows = process_lx02_pendientes(str(lx02_pendientes_path), str(DB_PATH), conn=con.conn)
                    if rows > 0:
                        has_changes = True

            # IW39 (Órdenes PM)
            if iw39_path.exists():
                from services.etl.iw39 import IW39Processor
                processor_iw39 = IW39Processor()
                for iw39_file in iw39_path.glob("*"):
                    if iw39_file.suffix.lower() in ['.txt', '.csv', '.xlsx'] and not iw39_file.name.startswith('~'):
                        with get_session() as _sess_iw39:
                            changed = is_file_changed(_sess_iw39, iw39_file)
                        if changed:
                            rows = processor_iw39.process_and_save(str(iw39_file), str(DB_PATH), "iw39_orders", con.conn)
                            with get_session() as _sess_iw39:
                                mark_file_processed(_sess_iw39, iw39_file, row_count=rows)
                            has_changes = True
                        else:
                            logger.debug(f"IW39 sin cambios ({iw39_file.name})")

            # Sincronización de Transporte (Avanti)
            from routes.transporte import sync_transporte_logic
            with get_session() as _sess_transporte:
                logger.info("Sincronizando base de datos de Transporte (Avanti)...")
                if sync_transporte_logic(_sess_transporte):
                    has_changes = True

            # Enriquecimiento final cruzado (Solo si hubo cambios en algo)
            if has_changes:
                con.enrich_movements_with_iw39()
                con.backfill_from_movements()
                con.backfill_texts()  # <-- Asegura descripciones en picking list
                con.update_sla_with_tasks()  # <-- Cruce automático de Tareas para SLA

                # 4. Limpiar caché global para forzar recarga de gráficos
                cache.clear_cache()
                try:
                    con.conn.execute("DELETE FROM analytics_snapshots")
                    logger.info("Snapshots de base de datos eliminados tras sincronización de nuevos datos.")
                except Exception as e:
                    logger.warning(f"No se pudo limpiar la tabla de snapshots en consolidación: {e}")
                logger.info(">>> Sincronización finalizada exitosamente. Datos actualizados y caché invalidada.")
            else:
                # Incluso si no hubo cambios en archivos, corremos backfill por seguridad
                con.enrich_movements_with_iw39()
                con.backfill_texts()
                con.update_sla_with_tasks()
                logger.info(">>> Sincronización finalizada: No se detectaron cambios en los archivos fuente.")

    except Exception as e:
        logger.error(f"Fallo crítico en el pipeline de sincronización: {e}", exc_info=True)
        raise  # Re-raise para que TaskManager capture el error
    finally:
        sync.is_syncing = False
        sync.sync_lock.release()

def _reset_directory(path: str):
    """Elimina y recrea un directorio de forma segura."""
    p = Path(path)
    if p.exists():
        shutil.rmtree(p)
    p.mkdir(parents=True, exist_ok=True)
