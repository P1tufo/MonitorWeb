/**
 * Docs Explorer - Diagnóstico y Renderizado
 */
 
console.log("!!! CARGANDO DOCS_EXPLORER.JS !!!");
 
const initDocs = async () => {
    const treeRoot = document.getElementById('docs-tree-root');
    const contentView = document.getElementById('docs-content-view');
 
    if (!treeRoot || !contentView) {
        console.error("CRÍTICO: No se encuentran los contenedores en el DOM.");
        return;
    }
 
    treeRoot.innerHTML = '<div style="padding:10px; color:#5DBAA9;"><i class="fas fa-sync fa-spin"></i> Conectando con API...</div>';
 
    try {
        console.log("Llamando a /api/docs/tree...");
        const res = await fetch('/api/docs/tree');
        if (!res.ok) throw new Error("Error HTTP: " + res.status);
        
        const data = await res.json();
        console.log("Datos del árbol recibidos:", data);
 
        if (!data || data.length === 0) {
            treeRoot.innerHTML = '<div style="padding:10px; color:#94a3b8;">No se encontraron archivos.</div>';
            return;
        }
 
        treeRoot.innerHTML = ''; // Limpiar cargando
        
        // Función de renderizado interno con soporte para expandir/colapsar carpetas
        const renderNodes = (nodes, container, level = 0) => {
            nodes.forEach(node => {
                const row = document.createElement('div');
                row.className = 'tree-item-row';
                row.style.paddingLeft = (level * 15 + 10) + 'px';
                
                let icon = node.is_dir ? '📁' : '📄';
                if (node.has_doc) {
                    if (node.path === 'docs/documentacion_global.md') {
                        icon = '📝';
                    } else {
                        icon = '✅';
                    }
                }
 
                row.innerHTML = `${icon} <span style="color:${node.has_doc ? '#5DBAA9' : '#94a3b8'}">${node.name}</span>`;
                container.appendChild(row);
 
                if (node.is_dir) {
                    // Dar un estilo ligeramente diferente a las carpetas en el árbol
                    row.innerHTML = `📁 <span style="color: #e2e8f0; font-weight: 500;">${node.name}</span>`;
                    
                    // Crear contenedor para los hijos de esta carpeta
                    const childrenContainer = document.createElement('div');
                    childrenContainer.className = 'tree-children-container';
                    childrenContainer.style.display = 'none'; // Inicia colapsado por defecto
                    childrenContainer.style.borderLeft = '1px dashed rgba(255,255,255,0.08)';
                    childrenContainer.style.marginLeft = (level * 15 + 18) + 'px';
                    childrenContainer.style.paddingLeft = '5px';
                    container.appendChild(childrenContainer);
 
                    // Renderizar hijos de forma recursiva dentro de su propio contenedor
                    if (node.children && node.children.length > 0) {
                        renderNodes(node.children, childrenContainer, level + 1);
                    }
 
                    // Alternar expandir/colapsar al hacer click en la carpeta
                    row.onclick = (e) => {
                        e.stopPropagation();
                        const isCollapsed = childrenContainer.style.display === 'none';
                        childrenContainer.style.display = isCollapsed ? 'block' : 'none';
                        
                        // Cambiar el ícono de carpeta abierta/cerrada
                        const folderIcon = isCollapsed ? '📂' : '📁';
                        row.innerHTML = `${folderIcon} <span style="color: #5DBAA9; font-weight: 600;">${node.name}</span>`;
                        
                        // Si se vuelve a colapsar, restaurar color normal
                        if (!isCollapsed) {
                            row.innerHTML = `📁 <span style="color: #e2e8f0; font-weight: 500;">${node.name}</span>`;
                        }
                    };
                } else {
                    // Click en archivo: cargar documentación
                    row.onclick = (e) => {
                        e.stopPropagation();
                        
                        // Quitar clase activa de todas las filas y ponérsela a esta
                        document.querySelectorAll('.tree-item-row').forEach(r => r.classList.remove('active'));
                        row.classList.add('active');
 
                        loadFile(node.path);
                        
                        // Si estamos en móvil, hacer scroll suave hasta el visor de contenidos
                        if (window.innerWidth <= 768) {
                            const scrollTarget = document.getElementById('docs-content-view');
                            if (scrollTarget) {
                                scrollTarget.scrollIntoView({ behavior: 'smooth' });
                            }
                        }
                    };
                }
            });
        };
 
        renderNodes(data, treeRoot);
 
    } catch (err) {
        console.error("Fallo en loadTree:", err);
        treeRoot.innerHTML = `<div style="color:#B46A5F; padding:10px;">Error: ${err.message}</div>`;
    }
};
 
const loadFile = async (path) => {
    const contentView = document.getElementById('docs-content-view');
    contentView.innerHTML = `<div style="padding:40px; text-align:center;"><i class="fas fa-spinner fa-spin fa-2x"></i><br>Cargando ${path}...</div>`;
 
    try {
        const res = await fetch(`/api/docs/content/${encodeURIComponent(path)}`);
        if (!res.ok) throw new Error("Error HTTP: " + res.status);
        
        const data = await res.json();
        
        let out = '';
        if (data && data.doc) {
            // Usar marked si está disponible, si no texto plano
            out = typeof marked !== 'undefined' && marked.parse ? marked.parse(data.doc) : `<pre style="white-space:pre-wrap;">${data.doc}</pre>`;
        } else {
            out = '<div style="color:#94a3b8; padding:20px;">No se encontró contenido documentado para este archivo.</div>';
        }
 
        contentView.innerHTML = `<div style="padding:20px; line-height:1.6;">${out}</div>`;
    } catch (err) {
        console.error("Error al cargar archivo:", err);
        contentView.innerHTML = `
            <div style="background: rgba(180,106,95,0.1); border: 1px solid rgba(180,106,95,0.3); color: #B46A5F; padding: 24px; border-radius: 12px; text-align: center;">
                <i class="fas fa-exclamation-triangle fa-2x" style="margin-bottom:15px;"></i>
                <h3 style="margin-bottom:10px;">No se pudo cargar la documentación</h3>
                <p style="font-size:0.9rem; opacity:0.8; margin-bottom:15px;">
                    El archivo solicitado no tiene una caché válida. Esto puede ocurrir si el archivo aún no ha sido analizado por el motor de IA o si hubo un cambio reciente.
                </p>
                <div style="display:flex; justify-content:center; gap:10px;">
                    <button class="btn btn-small" onclick="initDocs()" style="background:rgba(255,255,255,0.1); border:1px solid var(--border);">🔄 Reintentar</button>
                </div>
            </div>`;
    }
 
};
 
// Ejecutar al cargar y cuando se haga click en la pestaña
document.addEventListener('DOMContentLoaded', initDocs);
window.addEventListener('load', () => {
    const btn = document.getElementById('btn-docs');
    if (btn) {
        btn.addEventListener('click', () => {
            console.log("Pestaña Docs clickeada, refrescando...");
            initDocs();
        });
    }
});
