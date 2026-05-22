import subprocess
import sys
from pathlib import Path
import logging

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Importar configuraciones globales
try:
    from config import (
        DELIVERIES_DIR, 
        STOCK_DIR, 
        INVENTORY_DIR,
        CLEANSED_DIR, 
        DB_PATH as DATABASE_PATH,
        ONEDRIVE_PATH
    )
except ImportError:
    # Fallback si no se puede importar config (no debería pasar si PROJECT_ROOT está bien)
    DELIVERIES_DIR  = "/Users/christianykelly/Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Transacciones/Entregas"
    STOCK_DIR       = "/Users/christianykelly/Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Transacciones/Stock"
    INVENTORY_DIR   = "/Users/christianykelly/Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Transacciones/Movimientos"
    CLEANSED_DIR    = "/Users/christianykelly/Desktop/MonitorWeb/DELIVERIES_cleansed"
    DATABASE_PATH   = "/Users/christianykelly/Desktop/MonitorWeb/wms_transactions.db"

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
    for path_name, path_val in [("Origen Entregas", DELIVERIES_DIR), ("Stock Stock", STOCK_DIR), ("Movimientos Movimientos", INVENTORY_DIR)]:
        if not Path(path_val).exists():
            logger.error(f"Error de validación: El directorio de {path_name} no existe: {path_val}")
            print(f"  ❌ Abortando: No se encuentra {path_name}")
            return

    # ── Fase 1: Entregas ────────────────────────────────────────────────────────
    # Buscar analyze_folder.py en scripts/ o en la raíz
    analyze_script = PROJECT_ROOT / "scripts" / "analyze_folder.py"
    if not analyze_script.exists():
        analyze_script = PROJECT_ROOT / "analyze_folder.py"
        
    if not analyze_script.exists():
        logger.error(f"No se encontró analyze_folder.py en {PROJECT_ROOT} o {PROJECT_ROOT}/scripts")
        return

    cmd = [
        sys.executable, str(analyze_script),
        str(DELIVERIES_DIR),
        "--output", str(CLEANSED_DIR),
        "--db", str(DATABASE_PATH)
    ]
    
    logger.info(f"[Entregas] Ejecutando pipeline para: {DELIVERIES_DIR}")
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end='')
        process.wait()
        
        if process.returncode == 0:
            logger.info("[Entregas] Fase completada.")

            # ── Fase 2: Stock (Stock) ─────────────────────────────────────────
            logger.info("[Stock] Procesando stock...")
            from db.consolidator import DataConsolidator
            with DataConsolidator(str(DATABASE_PATH)) as con:
                con.overwrite_with_latest(str(STOCK_DIR), table_name="stock_levels")

                # ── Fase 3: Enriquecimiento Entregas × Stock ─────────────────────────
                logger.info("[Enrich] Cruzando Entregas con Stock...")
                from db.db_enrichment import enrich_deliveries_with_stock
                enrich_deliveries_with_stock(con.conn)
            
        else:
            logger.error(f"[Entregas] Pipeline terminó con errores (Código: {process.returncode})")

    except Exception as e:
        logger.error(f"[Entregas] Fallo crítico: {e}", exc_info=True)

    # ── Fase 4: Movimientos (Movimientos) ────────────────────────────────────────────
    print("\n" + "-"*60)
    print("📦 PROCESANDO Movimientos (Movimientos de Material)")
    print("-"*60)
    try:
        from db.inventory_folder_processor import process_inventory_folder
        total = process_inventory_folder(str(INVENTORY_DIR), str(DATABASE_PATH))
        print(f"  ✅  Movimientos completado: {total:,} filas en inventory_movements")
    except Exception as e:
        logger.error(f"[Movimientos] Fallo: {e}", exc_info=True)
        print(f"  ❌  Movimientos falló: {e}")

    # ── Resumen final ─────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("✅ PIPELINE COMPLETADO")
    print(f"📍 Datos limpios en:          {CLEANSED_DIR}")
    print(f"🗄️  Base de datos actualizada: {DATABASE_PATH}")
    print("="*60)

if __name__ == "__main__":
    run_pipeline()
