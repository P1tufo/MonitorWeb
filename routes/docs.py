import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from config import BASE_DIR, CACHE_DIR
from core.state import AppState, get_app_state

router = APIRouter(prefix="/api/docs", tags=["Documentation"])

@router.get("/tree")
async def get_docs_tree(state: AppState = Depends(get_app_state)):
    """Genera un árbol de archivos del proyecto indicando cuáles tienen documentación."""
    ignore_dirs = {".git", "__pycache__", "venv", "node_modules", "PDFs_Generados", "Temp_Assets", "scratch", ".doc_cache"}
    allowed_exts = {".py", ".js", ".html", ".css", ".md", ".json", ".sql", ".txt"}
    
    tree = []
    
    def build_tree(path, parent_list):
        try:
            items = sorted(os.listdir(path))
        except OSError:
            return

        for item in items:
            if item in ignore_dirs or item.startswith("."):
                continue
                
            full_path = os.path.join(path, item)
            rel_path = os.path.relpath(full_path, BASE_DIR)
            
            node = {
                "name": item,
                "path": rel_path,
                "is_dir": os.path.isdir(full_path),
                "has_doc": False,
                "children": []
            }
            
            if node["is_dir"]:
                build_tree(full_path, node["children"])
                if node["children"]: # Solo añadir carpetas que tengan archivos válidos
                    parent_list.append(node)
            else:
                ext = os.path.splitext(item)[1].lower()
                if ext in allowed_exts:
                    # Verificar si existe doc en caché
                    cache_name = rel_path + ".md"
                    cache_path = os.path.join(BASE_DIR, CACHE_DIR, cache_name)
                    node["has_doc"] = os.path.exists(cache_path)
                    
                    # Solo añadir si tiene documentación o si es un markdown real en docs/
                    if node["has_doc"] or (rel_path.startswith("docs") and ext == ".md"):
                        node["has_doc"] = True
                        parent_list.append(node)

    build_tree(BASE_DIR, tree)
    
    # Función para ordenar recursivamente el árbol (Carpetas primero, luego Archivos, orden alfabético)
    def sort_tree_nodes(nodes):
        nodes.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        for node in nodes:
            if node["children"]:
                sort_tree_nodes(node["children"])
                
    sort_tree_nodes(tree)
    
    # Añadir Documentación Global como opción seleccionable destacada al principio de todo el árbol
    global_doc_rel = "docs/documentacion_global.md"
    if os.path.exists(os.path.join(BASE_DIR, global_doc_rel)):
        global_node = {
            "name": "📝 Documentación Global (Sistema Completo)",
            "path": global_doc_rel,
            "is_dir": False,
            "has_doc": True,
            "children": []
        }
        tree.insert(0, global_node)
        
    return tree

@router.get("/content/{path:path}")
async def get_doc_content(path: str, state: AppState = Depends(get_app_state)):
    """Obtiene el contenido de la documentación (.md) para un archivo específico."""
    # 1. Intentar leerlo directamente si es un archivo real en la carpeta `docs` (como docs/documentacion_global.md)
    real_path = os.path.join(BASE_DIR, path)
    if os.path.exists(real_path) and os.path.isfile(real_path) and real_path.endswith(".md"):
        try:
            with open(real_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Si es la documentación global, ocultar la estructura del proyecto redundante en el visor
            if path == "docs/documentacion_global.md":
                import re
                pattern = r"### Estructura del Proyecto.*?(?=## Análisis de Arquitectura Global)"
                replacement = (
                    "### 🛠️ Estructura del Proyecto\n\n"
                    "> [!NOTE]\n"
                    "> *La visualización del árbol de carpetas textual ha sido ocultada en esta vista para optimizar el espacio vertical, "
                    "ya que cuentas con la **Estructura del Proyecto interactiva y desplegable** disponible en el panel izquierdo de este explorador.*\n\n"
                    "---\n\n"
                )
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                
            return {"doc": content}
        except Exception as e:
            pass

    # 2. De lo contrario, ir al fallback de cache
    cache_path = os.path.join(BASE_DIR, CACHE_DIR, path + ".md")
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return {"doc": f.read()}
            
    raise HTTPException(status_code=404, detail="Documentación no encontrada")

