#!/usr/bin/env python3
import shutil
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT_DIR / "graphify-out"
DEST_DIR = ROOT_DIR / "static" / "docs"

TRANSLATIONS = {
    'placeholder="Search nodes..."': 'placeholder="Buscar archivos o funciones..."',
    '<h3>Node Info</h3>': '<h3>Información</h3>',
    '>Click a node to inspect it<': '>Haz clic en un elemento para ver sus detalles<',
    '<h3>Communities</h3>': '<h3>Grupos de Código</h3>',
    '>Select All<': '>Mostrar Todo<',
    'nodes &middot;': 'elementos &middot;',
    'edges &middot;': 'conexiones &middot;',
    ' communities<': ' grupos<',
    '<div class="field">Type:': '<div class="field">Tipo:',
    '<div class="field">Community:': '<div class="field">Grupo:',
    '<div class="field">Source:': '<div class="field">Archivo origen:',
    '<div class="field">Degree:': '<div class="field">Conexiones:',
    '>Neighbors (': '>Relacionados (',
    '"Community ': '"Grupo '
}

def prepare_environment():
    """Limpia el directorio anterior y prepara la configuración."""
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)

    ignore_path = ROOT_DIR / ".graphifyignore"
    ignore_path.write_text("*.md\n", encoding="utf-8")

def execute_graphify():
    """Ejecuta el CLI de graphify."""
    import os
    env = os.environ.copy()
    env["GRAPHIFY_VIZ_NODE_LIMIT"] = "10000"

    try:
        subprocess.run(
            ["graphify", "update", "."],
            cwd=str(ROOT_DIR),
            env=env,
            check=True
        )
    except FileNotFoundError:
        print("Error: 'graphify' no está instalado o no se encuentra en el PATH.")
        print("Por favor instala graphify ejecutando: pip install graphify")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar graphify: {e}")
        return False
    return True

def process_and_move_html():
    """Lee el HTML generado, lo traduce y lo guarda en su destino."""
    source_html = OUT_DIR / "graph.html"
    dest_html = DEST_DIR / "graph.html"

    if not source_html.exists():
        print(f"\nError: No se encontró el archivo generado en {source_html}")
        print("Verifica si Graphify cambió la ubicación de salida.")
        return

    DEST_DIR.mkdir(parents=True, exist_ok=True)

    # Leer archivo origen
    html_content = source_html.read_text(encoding="utf-8")

    # Aplicar traducciones
    for old, new in TRANSLATIONS.items():
        html_content = html_content.replace(old, new)

    # Inyectar CSS y JS para hacer el menú y info-panel plegables
    mobile_css_js = """
  /* Botón para desplegar el sidebar en móvil */
  #mobile-sidebar-toggle { display: none; position: absolute; top: 10px; right: 10px; z-index: 1000; padding: 8px 12px; background: rgba(44, 62, 80, 0.9); color: white; border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 5px; cursor: pointer; font-size: 14px; box-shadow: 0 2px 5px rgba(0,0,0,0.5); backdrop-filter: blur(5px); }
  
  /* Ajustes para evitar saturación de info-panel */
  #info-panel { max-height: 40vh; overflow-y: auto; }

  /* Hacer el info-panel plegable (accordion) */
  #info-panel h3 { cursor: pointer; display: flex; justify-content: space-between; align-items: center; user-select: none; }
  #info-panel h3::after { content: '▼'; font-size: 10px; transition: transform 0.2s; }
  #info-panel.collapsed h3::after { transform: rotate(-90deg); }
  #info-panel.collapsed #info-content { display: none; }
  
  @media (max-width: 768px) {
    #mobile-sidebar-toggle { display: block; }
    #sidebar { position: absolute; top: 0; right: -280px; height: 100%; transition: right 0.3s ease; z-index: 999; box-shadow: -2px 0 10px rgba(0,0,0,0.5); }
    #sidebar.open { right: 0; }
  }
</style>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    var infoPanel = document.getElementById('info-panel');
    var h3 = infoPanel.querySelector('h3');
    h3.addEventListener('click', function() {
      infoPanel.classList.toggle('collapsed');
    });
  });
</script>"""
    html_content = html_content.replace('</style>', mobile_css_js)

    sidebar_html = """<button id="mobile-sidebar-toggle" onclick="document.getElementById('sidebar').classList.toggle('open')">☰ Menú</button>\n<div id="sidebar">"""
    html_content = html_content.replace('<div id="sidebar">', sidebar_html)

    # Escribir directamente en el destino
    dest_html.write_text(html_content, encoding="utf-8")

    print(f"\n¡Éxito! Mapa interactivo generado y movido a: {dest_html}")
    print("El mapa está listo para ser visualizado en la aplicación web.")

def run_graphify():
    print("Iniciando escaneo con Graphify...")
    prepare_environment()
    if execute_graphify():
        process_and_move_html()

if __name__ == "__main__":
    run_graphify()
