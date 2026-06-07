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
    env = subprocess.os.environ.copy()
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
