import logging
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Importar configuraciones globales
try:
    from config import DELIVERIES_DIR, INVENTORY_DIR, MB5B_DIR, ONEDRIVE_PATH, STOCK_DIR
    from config import DB_PATH as DATABASE_PATH
    IW39_DIR = "/Users/christianykelly/Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Transacciones/IW39"
except ImportError:
    # Fallback si no se puede importar config (no debería pasar si PROJECT_ROOT está bien)
    DELIVERIES_DIR  = "/Users/christianykelly/Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Transacciones/Entregas" # type: ignore
    STOCK_DIR       = "/Users/christianykelly/Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Transacciones/Stock" # type: ignore
    INVENTORY_DIR   = "/Users/christianykelly/Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Transacciones/Movimientos" # type: ignore
    IW39_DIR        = "/Users/christianykelly/Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Transacciones/IW39" # type: ignore
    MB5B_DIR        = "/Users/christianykelly/Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Transacciones/MB5B" # type: ignore
    # CLEANSED_DIR ya no se utiliza
    DATABASE_PATH   = "/Users/christianykelly/Desktop/MonitorWeb/data/wms_transactions.db" # type: ignore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_pipeline():
    """Executes the complete WMS Analysis and Consolidation pipeline."""

    print("\n" + "="*60)
    print("🚀 INICIANDO PROCESADOR MAESTRO WMS")
    print("="*60)

    # 0. Validación de Entrada (Seguridad y Robustez)
    for path_name, path_val in [("Origen Entregas", DELIVERIES_DIR), ("Stock Stock", STOCK_DIR), ("Movimientos Movimientos", INVENTORY_DIR), ("IW39 Órdenes", IW39_DIR)]:
        if not Path(str(path_val)).exists():
            logger.error(f"Error de validación: El directorio de {path_name} no existe: {path_val}")
            print(f"  ❌ Abortando: No se encuentra {path_name}")
            return

    # ── Fase 1: Entregas y Fase 2: Stock ───────────────────────────────────────
    try:
        from db.consolidator import DataConsolidator
        
        logger.info(f"[Entregas] Ejecutando pipeline para: {DELIVERIES_DIR}")
        with DataConsolidator(str(DATABASE_PATH)) as con:
            processed_count = con.consolidate_folder(str(DELIVERIES_DIR))
            logger.info(f"[Entregas] Fase completada. Registros procesados: {processed_count}")

            # ── Fase 2: Stock (Stock) ─────────────────────────────────────────
            logger.info("[Stock] Procesando stock...")
            con.overwrite_with_latest(str(STOCK_DIR), table_name="stock_levels")

            # ── Fase 3: Enriquecimiento Entregas × Stock ─────────────────────────
            logger.info("[Enrich] Cruzando Entregas con Stock...")
            from db.db_enrichment import enrich_deliveries_with_stock
            enrich_deliveries_with_stock(con.conn)

    except Exception as e:
        logger.error(f"[Entregas/Stock] Fallo crítico: {e}", exc_info=True)

    # ── Fase 4: Movimientos (Movimientos) ────────────────────────────────────────────
    print("\n" + "-"*60)
    print("📦 PROCESANDO Movimientos (Movimientos de Material)")
    print("-"*60)
    try:
        from services.etl.movements import InventoryMovementAdapter
        processor = InventoryMovementAdapter()
        import sqlite3
        with sqlite3.connect(DATABASE_PATH) as conn:
            total = processor.process_directory(str(INVENTORY_DIR), str(DATABASE_PATH), "inventory_movements", conn)
        print(f"  ✅  Movimientos completado: {total:,} filas en inventory_movements")
    except Exception as e:
        logger.error(f"[Movimientos] Fallo: {e}", exc_info=True)
        print(f"  ❌  Movimientos falló: {e}")

    # ── Fase 5: IW39 (Órdenes PM) ────────────────────────────────────────────
    print("\n" + "-"*60)
    print("⚙️  PROCESANDO IW39 (Órdenes PM)")
    print("-"*60)
    try:
        from services.etl.iw39 import IW39Processor
        processor_iw39 = IW39Processor()
        with sqlite3.connect(DATABASE_PATH) as conn:
            total = processor_iw39.process_directory(str(IW39_DIR), str(DATABASE_PATH), "iw39_orders", conn)

            # Enriquecer inventarios con IW39 (Cruza 'Orden')
            from db.db_enrichment import enrich_movements_with_iw39
            enrich_movements_with_iw39(conn)

        print(f"  ✅  IW39 completado: {total:,} filas en iw39_orders")
    except Exception as e:
        logger.error(f"[IW39] Fallo: {e}", exc_info=True)
        print(f"  ❌  IW39 falló: {e}")

    # ── Fase 6: MB5B (Stock Inicial) ────────────────────────────────────────────
    print("\n" + "-"*60)
    print("📦 PROCESANDO MB5B (Stock Inicial)")
    print("-"*60)
    try:
        from services.etl.mb5b import MB5BProcessor
        processor_mb5b = MB5BProcessor()
        with sqlite3.connect(DATABASE_PATH) as conn:
            total = processor_mb5b.process_directory(str(MB5B_DIR), str(DATABASE_PATH), "mb5b_initial_stock", conn)
        print(f"  ✅  MB5B completado: {total:,} filas en mb5b_initial_stock")
    except Exception as e:
        logger.error(f"[MB5B] Fallo: {e}", exc_info=True)
        print(f"  ❌  MB5B falló: {e}")

    # ── Resumen final ─────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("✅ PIPELINE COMPLETADO")
    print(f"🗄️  Base de datos actualizada: {DATABASE_PATH}")
    print("="*60)

if __name__ == "__main__":
    run_pipeline()
