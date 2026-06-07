import logging
import os
from pathlib import Path

logger = logging.getLogger("bundler")

# Orden estricto para evitar errores de referencias (Dependencies first)
JS_FILES_ORDER = [
    "core_ui.js",
    "dashboard_api.js",
    "dashboard_core.js",
    "dashboard_saas.js",
    "saas_engine_core.js",
    "saas_engine_drilldown.js",
    "deliveries.js",
    "consumos.js",
    "transporte.js",
    "tasks.js",
    "inventory.js",
    "analytics_proyecciones.js",
    "docs_explorer.js",
    "productivity_daily.js",
    "productivity_monthly.js",
    "productivity_modals.js"
]

def bundle_js():
    """Concatena múltiples archivos JS en un solo bundle.js para producción."""
    base_dir = Path(__file__).resolve().parent.parent
    js_dir = base_dir / "static" / "js"
    output_file = js_dir / "bundle.js"

    if not js_dir.exists():
        logger.warning(f"Directorio {js_dir} no encontrado. Omitiendo bundler.")
        return

    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write("/* WMS-MM Auto-generated Bundle */\n")

            for file_name in JS_FILES_ORDER:
                file_path = js_dir / file_name
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(f"\n/* --- {file_name} --- */\n")
                        outfile.write(infile.read())
                        outfile.write("\n")
                else:
                    logger.warning(f"Archivo JS faltante en el bundler: {file_name}")

        logger.info(f"Frontend bundling completado: {output_file.name} generado exitosamente.")
    except Exception as e:
        logger.error(f"Error generando el bundle JS: {e}", exc_info=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bundle_js()
