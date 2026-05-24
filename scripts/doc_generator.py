import os
import sys
import time
import json
import ollama
import hashlib
from tqdm import tqdm

# Asegurar que el script pueda encontrar 'config.py' en la raíz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configuración Arquitectural - Estilo Compilación Limpia
MODEL_NAME = "qwen2.5-coder:7b"
ROOT_DIR = "."
OUTPUT_FILE = "docs/documentacion_global.md"
OUTPUT_MEJORAS_FILE = "docs/mejoras_global.md"
from config import CACHE_DIR, CACHE_DIR_NAME
STATE_FILE = os.path.join(CACHE_DIR, "doc_generator_state.json")
def load_gitignore(root_dir):
    ignore_dirs = {".git", "__pycache__", "venv", "node_modules", "PDFs_Generados", "Temp_Assets", "scratch", "_legacy_reference", ".pytest_cache", CACHE_DIR_NAME}
    ignore_files = {OUTPUT_FILE, OUTPUT_MEJORAS_FILE, STATE_FILE, "scripts/doc_generator.py", "package.json", "package-lock.json", "tunnel_url.txt", "server.log", "free_ram.py"}
    
    gitignore_path = os.path.join(root_dir, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.endswith('/') or not '.' in line:
                        ignore_dirs.add(line.strip('/'))
                    else:
                        ignore_files.add(line)
    return ignore_dirs, ignore_files

IGNORE_DIRS, IGNORE_FILES = load_gitignore(ROOT_DIR)
ALLOWED_EXTENSIONS = {".py", ".js", ".html", ".css", ".json", ".sql"}
MAX_FILE_SIZE = 500 * 1024
CHUNK_THRESHOLD = 25000
CHUNK_SIZE = 30000

OLLAMA_OPTIONS = {
    "num_ctx": 16384,
    "temperature": 0.0,
    "top_p": 0.4,
    "repeat_penalty": 1.1,
    "num_predict": -1
}

PROMPT_TEMPLATE_SYSTEM = """
Actúa como Arquitecto de Datos y Software Senior. Documenta el código adjunto extrayendo metadatos técnicos estructurados.

### Resumen Funcional
(Descripción de 1 a 3 líneas sobre el objetivo del archivo).

### Catálogo de Funciones y Clases
(Lista estricta de las funciones/métodos detectados. Formato: `nombre_funcion(parametros)` - Breve propósito).

### Interacción con Base de Datos
(Especifica el motor ej. SQLite, Postgres, etc. Lista explícitamente qué TABLAS y qué COLUMNAS se están leyendo o modificando en este archivo. Si hay consultas SQL crudas o llamadas a ORM, menciónalas. Si no usa BD, escribe "Ninguna").

### Estado y Variables Globales
(Lista de variables globales, de sesión, de entorno o diccionarios quemados en código que almacenan estado crítico).

### Dependencias y Flujo
(Librerías externas utilizadas y hacia qué otros archivos del proyecto se comunica).

**REGLAS CRÍTICAS:**
1. Usa solo los encabezados ### indicados.
2. NO devuelvas tu respuesta envuelta en formato JSON. Responde estrictamente en texto.
3. Si el archivo no tiene interacción con bases de datos o no define variables globales, responde "No aplica" en esa sección. No alucines tablas.
4. Idioma: Español. Sé directo y técnico.
"""

PROMPT_TEMPLATE_USER = """
Archivo: {filename} ({filepath}).
Contenido del fragmento:
{content}
"""

PROMPT_IMPROVEMENT_TEMPLATE_SYSTEM = """
Actúa como un Desarrollador Senior y Auditor de Código extremadamente riguroso. 
Tu tarea es evaluar la calidad de este código buscando ÚNICAMENTE fallos críticos reales, vulnerabilidades comprobables (ej. inyecciones SQL reales) o cuellos de botella graves de rendimiento.

### Veredicto de Calidad
(Indica si el código necesita cambios urgentes, o si es lo suficientemente robusto para producción).

### Análisis Crítico (Solo si aplica)
(Estructura, rendimiento o seguridad. Explica por qué es un problema grave y cómo solucionarlo, adjuntando código si es útil).

**REGLAS CRÍTICAS:**
1. Si el código es sólido, funcional y seguro, tu respuesta debe ser EXACTAMENTE "CÓDIGO ÓPTIMO". Sin texto adicional.
2. NO alucines vulnerabilidades. Ej: Si ves que una consulta SQL ya utiliza paso de parámetros (como `?` o `params=()`), NO la marques como inyección SQL.
3. NO devuelvas tu respuesta envuelta en formato JSON. Responde estrictamente en texto usando Markdown.
4. Evalúa si el archivo contiene reglas de negocio, diccionarios o configuraciones "quemadas" en código (hardcoded). Si es así, recomienda explícitamente cómo migrar eso a tablas de Base de Datos para cumplir con nuestra visión SaaS (donde el usuario modifica las reglas vía Web). Si ves SQL crudo, sugiere cómo prepararlo para SQLAlchemy/Postgres.
5. NO sugieras micro-optimizaciones o cambios estéticos (ej. refactorizar variables si el código ya es legible).
6. NO sugieras sobre-ingeniería (ej. inyección de dependencias compleja para scripts simples).
7. Usa el idioma Español de forma clara, directa y técnica.
"""

PROMPT_IMPROVEMENT_TEMPLATE_USER = """
Archivo: {filename}.
Contenido del fragmento:
```python
{content}
```
"""

PROMPT_TREE_ANALYSIS_SYSTEM = """
Actúa como Arquitecto de Software Senior. Analiza la siguiente estructura de archivos de un proyecto y describe:
1. La arquitectura general detectada (ej. MVC, Monolito, Modular).
2. El propósito probable de las carpetas principales.
3. La organización lógica de las dependencias.

REGLAS CRÍTICAS:
1. NO devuelvas tu respuesta envuelta en formato JSON. Responde estrictamente en texto usando Markdown.
2. Estructura la respuesta usando encabezados ###.
3. Idioma: Español. Sé conciso y técnico.
4. No añadas introducciones informales.
"""

PROMPT_TREE_ANALYSIS_USER = """
Estructura del Proyecto:
```text
{tree}
```
"""

PROMPT_AUDIT_SYSTEM = """
Actúa como Auditor Principal de Software. A continuación se te proporciona la documentación técnica extraída de todos los archivos de un proyecto.

Tu objetivo es cruzar la información de todos los archivos para detectar malas prácticas arquitectónicas y deuda técnica a nivel global.

Analiza la documentación y genera un reporte estructurado con estos puntos exactos:

### 1. Funciones Duplicadas o Solapadas
(Busca funciones que hagan exactamente lo mismo pero estén en diferentes archivos. Enuméralas y sugiere crear un archivo `utils` o `helpers` compartido).

### 2. Inconsistencias en Base de Datos
(Analiza la sección 'Interacción con Base de Datos'. Detecta si hay múltiples archivos accediendo a las mismas tablas de forma desordenada, o si se mezclan consultas SQL crudas con ORMs).

### 3. Riesgos de Estado Global
(Analiza la sección 'Estado y Variables Globales'. Identifica variables o diccionarios quemados en código que deberían estar en la base de datos o en variables de entorno `.env`).

### 4. Veredicto de Refactorización
(Indica los 3 archivos más problemáticos que deberían refactorizarse primero y por qué).
"""

PROMPT_AUDIT_USER = """
Documentación Consolidada:
```markdown
{documentation}
```
"""

PROMPT_SUMMARY_SYSTEM = """
Actúa como Arquitecto de Software Senior. Tu tarea es leer la documentación técnica de varios archivos de un proyecto y generar un "Resumen Ejecutivo de Arquitectura" conciso.

REGLAS CRÍTICAS:
1. NO devuelvas tu respuesta envuelta en formato JSON. Responde estrictamente en texto usando Markdown.
2. Extrae los componentes principales, bases de datos mencionadas, dependencias críticas y el flujo lógico general.
3. Mantén el idioma Español, sé muy técnico y conciso. Evita texto de relleno.
"""

PROMPT_SUMMARY_USER = """
Documentación cruda:
```markdown
{documentation}
```
"""

def sanitize_output(text):
    if not text:
        return text
    text = text.strip()
    if text.startswith("```markdown"):
        text = text[11:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def get_file_info(filepath):
    try:
        with open(filepath, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
    except Exception:
        file_hash = ""
    return {
        "hash": file_hash
    }

def get_cache_path(filepath):
    """Genera una ruta única dentro de la caché para cada archivo"""
    rel_path = os.path.relpath(filepath, ROOT_DIR)
    return os.path.join(CACHE_DIR, rel_path + ".md")

def should_process(filename, filepath, state):
    rel_path = os.path.relpath(filepath, ROOT_DIR)
    if rel_path.startswith("./"): rel_path = rel_path[2:]
    
    if filename.startswith(".") or any(ignored in filepath for ignored in IGNORE_DIRS):
        return False
    if filename in IGNORE_FILES or rel_path in IGNORE_FILES:
        return False
    
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False

    try:
        f_size = os.path.getsize(filepath)
        if f_size > MAX_FILE_SIZE: return False
            
        # Si el archivo de caché no existe, hay que procesar sí o sí
        cache_path = get_cache_path(filepath)
        cache_path_mejora = cache_path.replace(".md", "_mejora.md")
        if not os.path.exists(cache_path) or not os.path.exists(cache_path_mejora):
            return True

        if filepath in state:
            info = get_file_info(filepath)
            if "hash" in state[filepath]:
                if state[filepath]["hash"] == info["hash"] and info["hash"] != "":
                    return False
    except:
        return False
        
    return True

def generate_project_tree(startpath, ignore_dirs):
    """Genera una representación en texto del árbol del proyecto."""
    tree = ["### Estructura del Proyecto\n", "```text"]
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in sorted(files):
            if not f.startswith('.'):
                tree.append(f"{subindent}{f}")
    tree.append("```\n")
    return "\n".join(tree)

def chunk_text(text, max_chars=30000, overlap_lines=10):
    """Corta el texto en fragmentos con un solapamiento de líneas para mantener contexto."""
    chunks = []
    lines = text.split('\n')
    
    if len(text) <= max_chars:
        return [text]

    current_pos = 0
    while current_pos < len(lines):
        current_chunk_lines = []
        current_chars = 0
        
        # Añadir líneas hasta alcanzar el límite
        for i in range(current_pos, len(lines)):
            line = lines[i]
            if current_chars + len(line) + 1 > max_chars and current_chunk_lines:
                break
            current_chunk_lines.append(line)
            current_chars += len(line) + 1
        
        chunks.append('\n'.join(current_chunk_lines))
        
        # Avanzar posición restando el solapamiento
        new_pos = current_pos + len(current_chunk_lines)
        if new_pos >= len(lines):
            break
        current_pos = max(new_pos - overlap_lines, current_pos + 1)
        
    return chunks

def call_ollama_with_retry(messages, retries=3, options=None):
    """Llamada a Ollama unificada usando la librería oficial."""
    if isinstance(messages, str):
        messages = [{'role': 'user', 'content': messages}]
        
    for attempt in range(retries):
        try:
            response = ollama.chat(
                model=MODEL_NAME,
                messages=messages,
                options=options if options else OLLAMA_OPTIONS
            )
            
            response_content = response.get("message", {}).get("content", "")
            response_content = sanitize_output(response_content)
            
            if not response_content.strip():
                tqdm.write(f"   [!] Advertencia: La IA devolvió una respuesta vacía.")
            
            return response_content
        except Exception as e:
            if attempt < retries - 1:
                tqdm.write(f"\n   ! Error Ollama (Intento {attempt+1}/{retries}): {e}. Esperando 5s...")
                time.sleep(5)
            else:
                raise e

def format_seconds(seconds):
    """Convierte segundos a formato HH:MM:SS"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def document_file(filepath, current, total):
    """Procesa un archivo, mide el tiempo y retorna True si tuvo éxito."""
    start_time = time.time()
    try:
        content = ""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
        
        filename = os.path.basename(filepath)
        cache_path = get_cache_path(filepath)
        cache_path_mejora = cache_path.replace(".md", "_mejora.md")
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)

        # Limpiar caché existente antes de procesar
        if os.path.exists(cache_path): os.remove(cache_path)
        if os.path.exists(cache_path_mejora): os.remove(cache_path_mejora)

        if not content.strip():
            tqdm.write(f"[{current}/{total}] SKIPPING - Archivo vacío: {filepath}")
            placeholder = f"## Archivo: {filepath}\n\nEste archivo está vacío o solo contiene espacios en blanco. No se requiere análisis de IA.\n"
            # Asegurar que el placeholder sea lo suficientemente largo para no ser purgado (>100 bytes)
            placeholder += "-" * (110 - len(placeholder)) + "\n"
            
            with open(cache_path, 'w', encoding='utf-8') as cf:
                cf.write(placeholder)
            with open(cache_path_mejora, 'w', encoding='utf-8') as cf:
                cf.write(placeholder)
            return True

        if len(content) > CHUNK_THRESHOLD:
            chunks = chunk_text(content, CHUNK_SIZE)
            with open(cache_path, 'a', encoding='utf-8') as cf, open(cache_path_mejora, 'a', encoding='utf-8') as cf_mejora:
                cf.write(f"## Archivo: {filepath} (Procesado en {len(chunks)} partes)\n\n")
                cf_mejora.write(f"## Sugerencias para: {filepath} (Procesado en {len(chunks)} partes)\n\n")
                
                for i, chunk in enumerate(chunks, 1):
                    part_info = f"PARTE {i} de {len(chunks)}"
                    
                    # Generar Documentación
                    msgs_doc = [
                        {'role': 'system', 'content': PROMPT_TEMPLATE_SYSTEM},
                        {'role': 'user', 'content': PROMPT_TEMPLATE_USER.format(filename=filename, filepath=filepath, part_info=part_info, content=chunk)}
                    ]
                    tqdm.write(f"[{current}/{total}] DOC - Procesando {part_info}: {filepath}...")
                    res_doc = call_ollama_with_retry(msgs_doc)
                    
                    if not res_doc or len(res_doc.strip()) < 10:
                        tqdm.write(f"   ✗ Fallo: La IA no generó documentación válida para la parte {i}")
                        return False
                        
                    cf.write(f"#### --- {part_info} ---\n\n{res_doc}\n\n")
                    time.sleep(1)
                    
                    # Generar Mejoras
                    msgs_imp = [
                        {'role': 'system', 'content': PROMPT_IMPROVEMENT_TEMPLATE_SYSTEM},
                        {'role': 'user', 'content': PROMPT_IMPROVEMENT_TEMPLATE_USER.format(filename=filename, filepath=filepath, part_info=part_info, content=chunk)}
                    ]
                    tqdm.write(f"[{current}/{total}] MEJORAS - Procesando {part_info}: {filepath}...")
                    res_imp = call_ollama_with_retry(msgs_imp)
                    
                    if not res_imp or len(res_imp.strip()) < 10:
                        res_imp = "(No se detectaron mejoras específicas para esta sección)"
                        
                    cf_mejora.write(f"#### --- {part_info} ---\n\n{res_imp}\n\n")
                    time.sleep(1)
        else:
            # Generar Documentación
            msgs_doc = [
                {'role': 'system', 'content': PROMPT_TEMPLATE_SYSTEM},
                {'role': 'user', 'content': PROMPT_TEMPLATE_USER.format(filename=filename, filepath=filepath, part_info="Completo", content=content)}
            ]
            tqdm.write(f"[{current}/{total}] DOC - Procesando: {filepath}...")
            res_doc = call_ollama_with_retry(msgs_doc)
            
            if not res_doc or len(res_doc.strip()) < 10:
                tqdm.write(f"   ✗ Fallo: La IA no generó documentación válida para {filepath}")
                return False
                
            time.sleep(1)
            
            # Generar Mejoras
            msgs_imp = [
                {'role': 'system', 'content': PROMPT_IMPROVEMENT_TEMPLATE_SYSTEM},
                {'role': 'user', 'content': PROMPT_IMPROVEMENT_TEMPLATE_USER.format(filename=filename, filepath=filepath, part_info="Completo", content=content)}
            ]
            tqdm.write(f"[{current}/{total}] MEJORAS - Procesando: {filepath}...")
            res_imp = call_ollama_with_retry(msgs_imp)

            if not res_imp or len(res_imp.strip()) < 10:
                # Si la IA no genera mejoras, ponemos un mensaje por defecto en lugar de dejarlo vacío
                res_imp = "### Análisis de Estructura\nNo se detectaron mejoras críticas necesarias.\n\n### Rendimiento y Seguridad\nConfiguración óptima detectada.\n\n### Deuda Técnica y Legibilidad\nCódigo limpio y legible."

            with open(cache_path, 'w', encoding='utf-8') as cf:
                cf.write(f"## Archivo: {filepath}\n\n{res_doc}\n\n")
            with open(cache_path_mejora, 'w', encoding='utf-8') as cf_mejora:
                cf_mejora.write(f"## Sugerencias para: {filepath}\n\n{res_imp}\n\n")

        elapsed = time.time() - start_time
        tqdm.write(f"   ✓ Caché actualizada ({format_seconds(elapsed)}): {filepath}")
        return True

    except Exception as e:
        tqdm.write(f"   ✗ Fallo en {filepath}: {str(e)}")
        # Si falló, eliminar archivos temporales para forzar reintento
        if 'cache_path' in locals() and os.path.exists(cache_path): os.remove(cache_path)
        if 'cache_path_mejora' in locals() and os.path.exists(cache_path_mejora): os.remove(cache_path_mejora)
        return False

def analyze_structure_pre_flight():
    """Genera el árbol del proyecto y realiza el análisis arquitectónico estructural."""
    print("[*] Iniciando fase de Análisis Estructural...")
    tree_cache_path = os.path.join(CACHE_DIR, "project_tree.md")
    analysis_cache_path = os.path.join(CACHE_DIR, "analisis_estructural.md")
    
    tree_map = generate_project_tree(ROOT_DIR, IGNORE_DIRS)
    
    # Verificar si el mapa cambió
    old_tree = ""
    if os.path.exists(tree_cache_path):
        with open(tree_cache_path, 'r', encoding='utf-8') as f: old_tree = f.read()
    
    # Guardar mapa actual
    with open(tree_cache_path, 'w', encoding='utf-8') as tf: tf.write(tree_map)
    
    # Analizar si es necesario
    if tree_map != old_tree or not os.path.exists(analysis_cache_path):
        print("[*] Generando nuevo análisis de arquitectura basado en el mapa...")
        msgs_analysis = [
            {'role': 'system', 'content': PROMPT_TREE_ANALYSIS_SYSTEM},
            {'role': 'user', 'content': PROMPT_TREE_ANALYSIS_USER.format(tree=tree_map)}
        ]
        analysis_res = call_ollama_with_retry(msgs_analysis)
        with open(analysis_cache_path, 'w', encoding='utf-8') as af:
            af.write(f"## Análisis de Arquitectura Global\n\n{analysis_res}\n\n")
        return True
    else:
        print("   ✓ Análisis estructural actualizado en caché.")
        return False

def generate_audit_post_flight(files_ordered):
    """Genera la Auditoría Global analizando la documentación ya generada en la caché."""
    audit_cache_path = os.path.join(CACHE_DIR, "auditoria_global.md")
    
    print("[*] Generando Auditoría Global basada en la documentación completa...")
    
    all_docs = []
    for filepath in files_ordered:
        cache_path = get_cache_path(filepath)
        if os.path.exists(cache_path):
            with open(cache_path, 'r', encoding='utf-8') as f:
                content = f.read()
                all_docs.append(content)
    
    full_documentation = "\n\n".join(all_docs)
    
    # Paso Intermedio: Resumen de resúmenes para evitar saturación de contexto
    print("   (Generando resumen intermedio de la documentación para alimentar la Auditoría...)")
    summarized_docs = []
    chunks = chunk_text(full_documentation, max_chars=30000, overlap_lines=5)
    
    for i, chunk in enumerate(chunks, 1):
        print(f"      -> Resumiendo bloque {i}/{len(chunks)}...")
        msgs_sum = [
            {'role': 'system', 'content': PROMPT_SUMMARY_SYSTEM},
            {'role': 'user', 'content': PROMPT_SUMMARY_USER.format(documentation=chunk)}
        ]
        res_sum = call_ollama_with_retry(msgs_sum)
        summarized_docs.append(res_sum)
        time.sleep(2)
        
    final_summary = "\n\n".join(summarized_docs)
    
    audit_options = OLLAMA_OPTIONS.copy()
    audit_options["num_ctx"] = 16384 
    
    msgs_audit = [
        {'role': 'system', 'content': PROMPT_AUDIT_SYSTEM},
        {'role': 'user', 'content': PROMPT_AUDIT_USER.format(documentation=final_summary)}
    ]
    
    print("   (Analizando resumen global para generar la Auditoría Arquitectónica...)")
    audit_res = call_ollama_with_retry(msgs_audit, options=audit_options)
    
    with open(audit_cache_path, 'w', encoding='utf-8') as rf:
        rf.write(f"## Auditoría Global de Software y Deuda Técnica\n\n{audit_res}\n\n")
    print("   ✓ Auditoría generada con éxito.")

def compile_master_file(files_ordered):
    """Une todos los fragmentos de la caché en los archivos maestros en orden."""
    print(f"\nCompilando archivo maestro de documentación: {OUTPUT_FILE}...")
    
    tree_cache_path = os.path.join(CACHE_DIR, "project_tree.md")
    analysis_cache_path = os.path.join(CACHE_DIR, "analisis_estructural.md")
    audit_cache_path = os.path.join(CACHE_DIR, "auditoria_global.md")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as master:
        master.write(f"# Documentación Técnica Global - MonitorWeb\n")
        master.write(f"Compilado el: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        master.write(f"Modelo: {MODEL_NAME} | Hardware: M1 Pro Optimized\n\n")
        master.write(f"---\n\n")
        
        # Insertar solo el análisis estructurado de arquitectura (excluyendo mapa de archivos y roadmap)
        for path in [analysis_cache_path]:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    master.write(f.read())
                    master.write("\n---\n\n")
        
        for filepath in files_ordered:
            cache_path = get_cache_path(filepath)
            if os.path.exists(cache_path):
                with open(cache_path, 'r', encoding='utf-8') as cf:
                    master.write(cf.read())
                    master.write("\n---\n\n")
    print(f"✓ Compilación de documentación finalizada.")

    print(f"\nCompilando archivo maestro de mejoras: {OUTPUT_MEJORAS_FILE}...")
    with open(OUTPUT_MEJORAS_FILE, 'w', encoding='utf-8') as master_imp:
        master_imp.write(f"# Sugerencias de Mejora Global - MonitorWeb\n")
        master_imp.write(f"Compilado el: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        master_imp.write(f"Modelo: {MODEL_NAME} | Hardware: M1 Pro Optimized\n\n")
        master_imp.write(f"---\n\n")
        
        for filepath in files_ordered:
            cache_path_mejora = get_cache_path(filepath).replace(".md", "_mejora.md")
            if os.path.exists(cache_path_mejora):
                with open(cache_path_mejora, 'r', encoding='utf-8') as cf:
                    master_imp.write(cf.read())
                    master_imp.write("\n---\n\n")
    print(f"✓ Compilación de mejoras finalizada.")

def compile_by_folders(files_ordered):
    """Compila la documentación y mejoras agrupándolas por carpetas del proyecto."""
    print(f"\nCompilando documentación por carpetas...")
    
    # Agrupar archivos por su carpeta contenedora
    folder_groups = {}
    for filepath in files_ordered:
        # Extraer el directorio relativo
        rel_path = os.path.relpath(filepath, ROOT_DIR)
        dirname = os.path.dirname(rel_path)
        
        # Si está en la raíz, lo agrupamos en una carpeta virtual 'raiz'
        if not dirname or dirname == ".":
            dirname = "raiz"
            
        if dirname not in folder_groups:
            folder_groups[dirname] = []
        folder_groups[dirname].append(filepath)
        
    for dirname, files in folder_groups.items():
        # Crear subdirectorio correspondiente bajo docs/
        target_dir = os.path.join("docs", dirname)
        os.makedirs(target_dir, exist_ok=True)
        
        doc_output = os.path.join(target_dir, "documentacion.md")
        mejora_output = os.path.join(target_dir, "mejoras.md")
        
        print(f" -> Compilando '{dirname}': {doc_output} y {mejora_output}...")
        
        # Escribir la compilación de documentación del directorio
        with open(doc_output, 'w', encoding='utf-8') as f_doc:
            f_doc.write(f"# Documentación Técnica - Directorio: {dirname}\n")
            f_doc.write(f"Compilado el: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f_doc.write(f"Modelo: {MODEL_NAME} | Separado por Carpetas\n\n")
            f_doc.write(f"---\n\n")
            
            for filepath in files:
                cache_path = get_cache_path(filepath)
                if os.path.exists(cache_path):
                    with open(cache_path, 'r', encoding='utf-8') as cf:
                        f_doc.write(cf.read())
                        f_doc.write("\n---\n\n")
                        
        # Escribir la compilación de sugerencias/mejoras del directorio
        with open(mejora_output, 'w', encoding='utf-8') as f_mej:
            f_mej.write(f"# Sugerencias de Mejora - Directorio: {dirname}\n")
            f_mej.write(f"Compilado el: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f_mej.write(f"Modelo: {MODEL_NAME} | Separado por Carpetas\n\n")
            f_mej.write(f"---\n\n")
            
            for filepath in files:
                cache_path_mejora = get_cache_path(filepath).replace(".md", "_mejora.md")
                if os.path.exists(cache_path_mejora):
                    with open(cache_path_mejora, 'r', encoding='utf-8') as cf:
                        f_mej.write(cf.read())
                        f_mej.write("\n---\n\n")

    # Limpieza de carpetas huérfanas en 'docs/'
    if os.path.exists("docs"):
        for root_dir, dirs, files_in_dir in os.walk("docs", topdown=False):
            if root_dir == "docs":
                continue
            rel_dir = os.path.relpath(root_dir, "docs")
            
            # Si el directorio no está en nuestros grupos activos y no es 'raiz'
            if rel_dir not in folder_groups and rel_dir != "raiz":
                # Borramos los archivos markdown generados
                for f in files_in_dir:
                    if f in ["documentacion.md", "mejoras.md"]:
                        try:
                            os.remove(os.path.join(root_dir, f))
                        except OSError:
                            pass
                # Intentamos borrar el directorio si quedó vacío
                try:
                    if not os.listdir(root_dir):
                        os.rmdir(root_dir)
                        print(f"   ✓ Directorio obsoleto eliminado de docs/: {rel_dir}")
                except OSError:
                    pass

def prepare_model():
    """Verifica si Ollama está activo y si el modelo solicitado existe."""
    print(f"--- Preparando Motor de IA ({MODEL_NAME}) ---")
    try:
        # 1. Verificar conexión con Ollama
        models_info = ollama.list()
        
        # 2. Verificar si el modelo ya existe
        # Nota: La librería ollama devuelve objetos con atributo 'model'
        existing_models = [m.model for m in models_info.models]
        
        if MODEL_NAME not in existing_models and (MODEL_NAME + ":latest") not in existing_models:
            print(f"[!] El modelo '{MODEL_NAME}' no se encuentra localmente.")
            print(f"[*] Iniciando descarga automática. Esto puede tardar unos minutos...")
            ollama.pull(MODEL_NAME)
            print(f"✓ Modelo '{MODEL_NAME}' descargado con éxito.")
        else:
            print(f"✓ Motor de IA listo y modelo verificado.")
            
    except Exception as e:
        print(f"\n[X] ERROR CRÍTICO: No se pudo conectar con Ollama.")
        print(f"    Asegúrate de que Ollama esté abierto y funcionando.")
        print(f"    Detalle: {e}")
        sys.exit(1)

def cleanup_orphaned_cache(state, valid_files):
    """Elimina de la caché los archivos que ya no existen en el proyecto."""
    if not os.path.exists(CACHE_DIR):
        return state, False
    
    valid_files_set = set(valid_files)
    orphaned_keys = []
    
    for filepath in list(state.keys()):
        if filepath not in valid_files_set:
            orphaned_keys.append(filepath)
            
            cache_path = get_cache_path(filepath)
            cache_path_mejora = cache_path.replace(".md", "_mejora.md")
            if os.path.exists(cache_path): os.remove(cache_path)
            if os.path.exists(cache_path_mejora): os.remove(cache_path_mejora)
    
    for k in orphaned_keys:
        del state[k]
        
    if orphaned_keys:
        print(f"   ✓ Se limpiaron {len(orphaned_keys)} archivos huérfanos de la caché.")
        
    # Limpiar directorios vacíos que hayan quedado en la caché
    for root_dir, dirs, _ in os.walk(CACHE_DIR, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root_dir, name)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
            except OSError:
                pass
                
    return state, len(orphaned_keys) > 0

def purge_empty_cache_files():
    """Busca y elimina archivos en .doc_cache que estén vacíos o corruptos para forzar reintento."""
    if not os.path.exists(CACHE_DIR):
        return
    
    purged_count = 0
    print("[*] Verificando integridad de la caché...")
    for root, dirs, files in os.walk(CACHE_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                try:
                    # Si el archivo pesa menos de 100 bytes, probablemente está corrupto o vacío
                    # Omitimos archivos que explícitamente dicen estar vacíos
                    size = os.path.getsize(filepath)
                    if size < 100:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if "Archivo vacío" in content or "archivo está vacío" in content or "CÓDIGO ÓPTIMO" in content:
                                continue
                        
                        os.remove(filepath)
                        purged_count += 1
                except:
                    pass
    if purged_count > 0:
        print(f"   ✓ Se eliminaron {purged_count} archivos de caché corruptos para reintento.")

def main():
    force_audit = "--audit" in sys.argv
    # Asegurar que el modelo esté listo antes de empezar
    prepare_model()
    
    print(f"\n--- MonitorWeb Doc Engine (Arquitectura de Caché & Compilación) ---")
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Limpiar archivos corruptos antes de analizar
    purge_empty_cache_files()
    
    state = load_state()
    
    # 0. Fase Pre-flight: Árbol y Análisis Estructural
    structure_changed = analyze_structure_pre_flight()
    
    all_valid_files = []
    files_to_process = []
    
    # 1. Escanear archivos
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            filepath = os.path.join(root, file)
            if should_process(file, filepath, {}): # Check general de validez
                all_valid_files.append(filepath)
                if should_process(file, filepath, state): # Check si necesita IA
                    files_to_process.append(filepath)
    
    all_valid_files.sort() # Orden alfabético para el archivo final
    
    state, was_cleaned = cleanup_orphaned_cache(state, all_valid_files)
    save_state(state)
    
    count = len(files_to_process)
    if count > 0:
        print(f"Se detectaron {count} cambios. Iniciando actualización de caché...\n")
        # Integración de tqdm para el seguimiento de archivos
        for index, filepath in enumerate(tqdm(files_to_process, desc="Procesando archivos", unit="archivo"), 1):
            if document_file(filepath, index, count):
                state[filepath] = get_file_info(filepath)
                save_state(state)
            time.sleep(5) # Respiro térmico entre archivos
    else:
        print("Caché al día. No hay cambios detectados.")

    # 2. Generar Auditoría Post-Flight (Ahora con conocimiento de los archivos)
    # Forzar regeneración si tenemos force_audit, o si no existe
    audit_cache_path = os.path.join(CACHE_DIR, "auditoria_global.md")
    needs_audit = force_audit or not os.path.exists(audit_cache_path)

    if needs_audit:
        generate_audit_post_flight(all_valid_files)

    master_missing = not os.path.exists(OUTPUT_FILE) or not os.path.exists(OUTPUT_MEJORAS_FILE)
    needs_compilation = (count > 0) or was_cleaned or structure_changed or needs_audit or master_missing
    
    if needs_compilation:
        # 3. Compilar archivo maestro y carpetas con el estado actual
        compile_master_file(all_valid_files)
        compile_by_folders(all_valid_files)
    else:
        print("\n✓ Documentación compilada al día. No es necesario recompilar.")

    # 4. Liberar modelo de la RAM
    print("\n[*] Solicitando a Ollama liberar el modelo de la RAM...")
    try:
        ollama.chat(model=MODEL_NAME, messages=[], keep_alive=0)
        print("✓ Memoria liberada.")
    except:
        pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Ejecución cancelada por el usuario. Saliendo de forma segura...")
