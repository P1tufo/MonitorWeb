#!/usr/bin/env python3
import os
import subprocess
import shutil

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def run_graphify():
    print("Iniciando escaneo con Graphify...")
    try:
        # Limpiar salida anterior para forzar la regeneración del mapa HTML
        out_dir = os.path.join(ROOT_DIR, "graphify-out")
        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)

        # Crear .graphifyignore para ignorar archivos markdown (.md)
        ignore_path = os.path.join(ROOT_DIR, ".graphifyignore")
        with open(ignore_path, "w") as f:
            f.write("*.md\n")

        # Ejecuta la extracción de AST (ultra rápida) sin depender del LLM local,
        # y aumenta el límite de visualización ya que el proyecto tiene >5000 nodos.
        env = os.environ.copy()
        env["GRAPHIFY_VIZ_NODE_LIMIT"] = "10000"
        
        subprocess.run(
            ["graphify", "update", "."],
            cwd=ROOT_DIR,
            env=env,
            check=True
        )
    except FileNotFoundError:
        print("Error: 'graphify' no está instalado o no se encuentra en el PATH.")
        print("Por favor instala graphify ejecutando: pip install graphifyy")
        return
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar graphify: {e}")
        return

    # El output suele estar en graphify-out/
    source_html = os.path.join(ROOT_DIR, "graphify-out", "graph.html")
    dest_dir = os.path.join(ROOT_DIR, "static", "docs")
    
    # Crea el directorio de destino si no existe
    os.makedirs(dest_dir, exist_ok=True)
    
    dest_html = os.path.join(dest_dir, "graph.html")

    if os.path.exists(source_html):
        shutil.copy(source_html, dest_html)
        
        # --- POST-PROCESAMIENTO ---
        # Traducir al español y ocultar todo por defecto
        with open(dest_html, "r", encoding="utf-8") as f:
            html_content = f.read()
            
        replacements = {
            'placeholder="Search nodes..."': 'placeholder="Buscar archivos o funciones..."',
            '<h3>Node Info</h3>': '<h3>Información</h3>',
            '>Click a node to inspect it<': '>Haz clic en un elemento para ver sus detalles<',
            '<h3>Communities</h3>': '<h3>Grupos de Código</h3>',
            '>Select All<': '>Mostrar Todo<',
            'nodes &middot;': 'elementos &middot;',
            'edges &middot;': 'conexiones &middot;',
            ' communities<': ' grupos<',
            # Panel de info individual
            '<div class="field">Type:': '<div class="field">Tipo:',
            '<div class="field">Community:': '<div class="field">Grupo:',
            '<div class="field">Source:': '<div class="field">Archivo origen:',
            '<div class="field">Degree:': '<div class="field">Conexiones:',
            '>Neighbors (': '>Relacionados (',
            '"Community ': '"Grupo '  # Cambia 'Community 1' a 'Grupo 1'
        }
        for old, new in replacements.items():
            html_content = html_content.replace(old, new)
            
        with open(dest_html, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        print(f"\n¡Éxito! Mapa interactivo generado y movido a: {dest_html}")
        print("El mapa está listo para ser visualizado en la aplicación web.")
    else:
        print(f"\nError: No se encontró el archivo generado en {source_html}")
        print("Verifica si Graphify cambió la ubicación de salida.")

if __name__ == "__main__":
    run_graphify()
