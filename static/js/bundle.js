/* WMS-MM Auto-generated Bundle */

/* --- core_ui.js --- */
/**
 * MonitorWeb — Core UI Module (core_ui.js)
 *
 * Módulo de utilidades de UI compartidas por todas las vistas.
 * Debe cargarse ANTES de cualquier otro JS de dominio (deliveries.js,
 * inventory.js, analytics_proyecciones.js, etc.).
 *
 * Expone window.CoreUI con las funciones comunes para que los módulos
 * de dominio puedan delegar sin redefinir la lógica localmente.
 *
 * ── Funciones disponibles ──────────────────────────────────────────────
 *  CoreUI.openModal(id)              — Muestra un modal por su ID de elemento
 *  CoreUI.closeModal(id)             — Oculta un modal por su ID de elemento
 *  CoreUI.renderMaterialModal(opts)  — Rellena y abre un modal de lista de materiales
 *  CoreUI.populateAreaSelect(...)    — Rellena un <select> con áreas únicas de un array
 *  CoreUI.getData(id)                — Lee y parsea JSON embebido en un <script> o <span>
 * ──────────────────────────────────────────────────────────────────────
 */

window.CoreUI = (() => {

    // ── Modal helpers ──────────────────────────────────────────────────

    /**
     * Muestra un elemento modal añadiendo la clase CSS 'show'.
     * @param {string} id - ID del elemento DOM del modal.
     */
    function openModal(id) {
        const el = document.getElementById(id);
        if (el) el.classList.add('show');
    }

    /**
     * Oculta un elemento modal quitando la clase CSS 'show'.
     * @param {string} id - ID del elemento DOM del modal.
     */
    function closeModal(id) {
        const el = document.getElementById(id);
        if (el) el.classList.remove('show');
    }

    // ── Material modal renderer ────────────────────────────────────────

    /**
     * Rellena un modal de lista de materiales con los ítems proporcionados
     * y lo abre automáticamente.
     *
     * @param {object} opts
     * @param {string}   opts.modalId   - ID del elemento modal a abrir.
     * @param {string}   opts.titleId   - ID del elemento de título del modal.
     * @param {string}   opts.listId    - ID del elemento <ul> donde renderizar los ítems.
     * @param {string}   opts.title     - Texto del título a mostrar.
     * @param {Array}    opts.items     - Array de objetos { cod_mat, material, qty_fmt?, total_qty? }.
     * @param {string}  [opts.colorVar] - Variable CSS para el color del score (ej: '--naranja').
     * @param {string}  [opts.bgColor]  - Color de fondo inline para el score (ej: 'rgba(...)').
     */
    function renderMaterialModal({ modalId, titleId, listId, title, items, colorVar, bgColor }) {
        const titleEl = document.getElementById(titleId);
        const listEl  = document.getElementById(listId);

        if (titleEl) titleEl.innerHTML = title;

        if (!items || items.length === 0) {
            if (listEl) {
                listEl.innerHTML = '<li style="text-align:center; color:#64748b; font-style:italic; padding: 2rem;">No hay registros para esta selección.</li>';
            }
        } else {
            const html = items.map(mat => `
                <li>
                    <div>
                        <div class="name" style="font-size: 1rem;">
                            <span style="color:var(--primario);font-size:0.85rem;">[${mat.cod_mat}]</span> ${mat.material}
                        </div>
                    </div>
                    <div class="score" style="font-size: 1.1rem; ${colorVar ? `color: var(${colorVar});` : ''} ${bgColor ? `background: ${bgColor};` : ''}">
                        ${mat.qty_fmt || mat.total_qty || 0} req.
                    </div>
                </li>
            `).join('');
            if (listEl) listEl.innerHTML = html;
        }

        openModal(modalId);
    }

    // ── Area select populator ──────────────────────────────────────────

    /**
     * Rellena un elemento <select> con las áreas únicas encontradas en un array de datos.
     * No añade opciones si el select ya fue inicializado (más de 1 opción presente).
     *
     * @param {string} selectId  - ID del elemento <select>.
     * @param {Array}  data      - Array de objetos con la clave de área.
     * @param {string} [key]     - Nombre de la propiedad del área en cada objeto (default: 'area').
     */
    function populateAreaSelect(selectId, data, key = 'area') {
        const select = document.getElementById(selectId);
        if (!select || select.options.length > 1) return;

        const areaSet = new Set();
        data.forEach(item => {
            if (item[key] && item[key] !== 'Área Desconocida' && item[key] !== 'Desconocida') {
                areaSet.add(item[key]);
            }
        });

        Array.from(areaSet).sort().forEach(area => {
            const opt = document.createElement('option');
            opt.value = area;
            opt.textContent = area;
            select.appendChild(opt);
        });
    }

    // ── Data reader ───────────────────────────────────────────────────

    /**
     * Lee y parsea JSON embebido en el textContent de un elemento del DOM.
     * Usado para leer datos inyectados por Jinja2 como <script type="application/json">.
     *
     * @param {string} id - ID del elemento que contiene el JSON.
     * @returns {*} El dato parseado, o null si el elemento no existe o el JSON es inválido.
     */
    function getData(id) {
        const el = document.getElementById(id);
        if (!el) return null;
        try {
            const txt = el.textContent.trim();
            if (!txt) return null;
            return JSON.parse(txt);
        } catch (e) {
            console.warn(`[CoreUI] Error parseando JSON en #${id}:`, e);
            return null;
        }
    }

    // ── Public API ────────────────────────────────────────────────────

    return { openModal, closeModal, renderMaterialModal, populateAreaSelect, getData };

})();

// Alias globales directos para compatibilidad con handlers inline (onclick="openModal(...)")
window.openModal  = CoreUI.openModal.bind(CoreUI);
window.closeModal = CoreUI.closeModal.bind(CoreUI);


/* --- dashboard_api.js --- */
/**
 * MonitorWeb — Dashboard Core Logic
 */

// ── API MODULE ──────────────────────────────────────────────────────────

const DashboardAPI = {
    async _fetch(url, options = {}) {
        const res = await fetch(url, options);
        if (res.status === 401) {
            // Limpiar localStorage y redirigir
            localStorage.removeItem('monitorweb_token');
            window.location.href = '/login';
            return null;
        }
        return res;
    },

    async fetchKPIs(params) {
        const query = new URLSearchParams(params).toString();
        try {
            const res = await this._fetch(`/api/kpis?${query}`);
            return res ? await res.json() : null;
        } catch (e) {
            console.error("Error fetching KPIs:", e);
            return null;
        }
    },

    async fetchFilteredData(params) {
        const query = new URLSearchParams(params).toString();
        try {
            const res = await this._fetch(`/filter?${query}`);
            return res ? await res.json() : [];
        } catch (e) {
            console.error("Error fetching filtered data:", e);
            return [];
        }
    },

    async sync() {
        const res = await this._fetch('/sync', { method: 'POST' });
        return res ? await res.json() : { status: 'error', message: 'No autorizado' };
    },

    async checkSyncStatus() {
        try {
            const res = await this._fetch('/sync/status');
            return res ? await res.json() : { is_syncing: false };
        } catch (e) {
            return { is_syncing: false };
        }
    },

    async logout() {
        try {
            await fetch('/api/auth/logout', { method: 'POST' });
            localStorage.clear();
            window.location.reload();
        } catch (e) {
            window.location.reload();
        }
    }
};

// ── UI & MODAL HELPERS ──────────────────────────────────────────────────

const UI = {
    openPdfModal() {
        document.getElementById('pdfModal').classList.add('active');
    },
    closePdfModal() {
        document.getElementById('pdfModal').classList.remove('active');
        document.getElementById('pdfViewerFrame').src = "";
    },
    toggleMulti(id) {
        const el = document.getElementById(id);
        el.classList.toggle('show');
    },
    setBtnLoading(btn, text, isLoading) {
        if (!btn) return;
        if (isLoading) {
            btn.dataset.originalHtml = btn.innerHTML;
            btn.innerHTML = `⏳ ${text}...`;
            btn.disabled = true;
            btn.style.opacity = "0.7";
        } else {
            btn.innerHTML = btn.dataset.originalHtml || btn.innerHTML;
            btn.disabled = false;
            btn.style.opacity = "1";
        }
    }
};
// Global click listener for multiselects
document.addEventListener('click', (e) => {
    if (!e.target.closest('.multiselect')) {
        document.querySelectorAll('.checkboxes').forEach(c => c.classList.remove('show'));
    }
});



/* --- dashboard_core.js --- */
// ── RENDERERS ───────────────────────────────────────────────────────────

function renderTableRow(t) {
    const statusClass = t.estado_wms.includes('Contabilizado') ? 'status-tratada'
        : (t.estado_wms.includes('Abierta') ? 'status-abierta' : 'status-error');

    return `
        <tr class="row">
            <td data-label="Entrega / OT" style="font-weight:600;">
                ${t.entrega}
                ${t.has_ots ? '<span title="Contiene OT(s) asociada(s)" style="font-size:0.8rem; margin-left:5px;">🏷️</span>' : ''}
            </td>
            <td data-label="Fecha">${t.fe_carga}</td>
            <td data-label="Items" class="hide-mobile"><span class="status-badge" style="background:rgba(255,255,255,0.05);">📦 ${t.num_items} items</span></td>
            <td data-label="Área" class="hide-mobile"><span style="opacity:0.7;">${t.area_negocio}</span></td>
            <td data-label="Estado"><span class="status-badge ${statusClass}">${t.estado_wms}</span></td>
            <td data-label="Acciones">
                <form action="/generate-pdf" method="POST" onsubmit="updateLogoVal(document.activeElement);">
                    <input type="hidden" name="entrega" value="${t.entrega}">
                    <input type="hidden" name="include_logo" class="logo-hidden-input" value="true">
                    <div style="display:flex; gap:4px;">
                        <button type="submit" name="action" value="previsualizar" class="btn btn-small"
                            style="flex:1; padding:6px 10px;"
                            onclick="return pdfSubmit(this, 'pdfViewerFrame', true);" title="Ver en Pantalla">👁️ Ver</button> 
                        <button type="submit" name="action" value="descargar" class="btn btn-small"
                            style="flex:1; background:rgba(255,255,255,0.1); border:1px solid var(--border); padding:6px 10px;"
                            onclick="return pdfSubmit(this, 'downloadFrame', false);" title="Descargar como PDF">⬇️ PDF</button>
                    </div>
                </form>
            </td>
        </tr>`;
}

async function executeFilters() {
    const areaAll = document.getElementById('areaFilterAll')?.checked;
    const dateAll = document.getElementById('dateFilterAll')?.checked;
    
    const areaValues = areaAll ? '' : getCheckboxValues('area-cb');
    const dateValues = dateAll ? '' : getCheckboxValues('date-cb');
    const has_ots_filter = document.querySelector('input[name="ot-filter"]:checked')?.value || '';
    
    const params = {
        date: dateValues,
        entrega: document.getElementById('orderSearch').value,
        area: areaValues,
        centro: document.querySelector('input[name="centro-filter"]:checked')?.value || '',
        has_ots_filter: has_ots_filter
    };

    // Parallel fetch
    const [kpiData, tableData] = await Promise.all([
        DashboardAPI.fetchKPIs(params),
        DashboardAPI.fetchFilteredData(params)
    ]);

    // Update KPIs
    if (kpiData) {
        document.getElementById('kpiDeliveries').innerText = kpiData.kpi_deliveries;
        document.getElementById('kpiMaterials').innerText = kpiData.kpi_materials;

        // Nuevos sub-valores con texto descriptivo
        const updateSub = (id, val, text, icon) => {
            const el = document.getElementById(id);
            if (el) el.innerHTML = `${icon} <b>${val}</b> ${text}`;
        };

        updateSub('subDelAbierta', kpiData.sub_del_abierta, 'Entregas en curso', '🏷️');
        updateSub('subDelNoTratada', kpiData.sub_del_no_tratada, 'Entregas NO Tratadas', '⚠️');
        updateSub('subMatAbierta', kpiData.sub_mat_abierta, 'Picking en curso', '🏷️');
        updateSub('subMatNoTratada', kpiData.sub_mat_no_tratada, 'Pendientes por generar OT', '⚠️');

        // Nuevos SLA
        updateSub('subDelReunido', kpiData.sub_del_reunido, 'Reunido a tiempo', '✅');
        updateSub('subDelAtrasado', kpiData.sub_del_atrasado, 'Reunido Atrasado', '🕒');
        updateSub('subDelCritico', kpiData.sub_del_critico, 'OT Abierta atrasada', '🚨');

        updateSub('subMatReunido', kpiData.sub_mat_reunido, 'Reunido a tiempo', '✅');
        updateSub('subMatAtrasado', kpiData.sub_mat_atrasado, 'Reunido atrasado', '🕒');
        updateSub('subMatCritico', kpiData.sub_mat_critico, 'OT Abierta atrasada', '🚨');
    }

    // Update SLA Links so they respect current filters
    const queryStr = new URLSearchParams(params).toString();
    document.querySelectorAll('a[href^="/analytics/sla"]').forEach(link => {
        const url = new URL(link.href, window.location.origin);
        // Mantener el parametro type original (late/ontime)
        const type = url.searchParams.get('type') || 'late';
        link.href = `/analytics/sla?type=${type}&${queryStr}`;
    });

    // Update Table
    document.getElementById('transactionBody').innerHTML = tableData.map(renderTableRow).join('');
    filterTable();

    // Update SaaS Widgets with the new filters
    window.initSaaSWidgets = initSaaSWidgets;
    initSaaSWidgets(params);
}

// ── FILTER HELPERS ─────────────────────────────────────────────────────

let filterTimeout = null;
function applyFilters() {
    clearTimeout(filterTimeout);
    filterTimeout = setTimeout(executeFilters, 250);
}

function getCheckboxValues(className) {
    return Array.from(document.querySelectorAll('.' + className + ':checked')).map(cb => cb.value).join(',');
}

function toggleSelectAll(className, isChecked) {
    const boxes = document.querySelectorAll('.' + className);
    boxes.forEach(cb => cb.checked = isChecked);

    if (className === 'date-cb') {
        const selAll = document.getElementById('dateFilterAll');
        if (selAll) selAll.checked = isChecked;
    }
    if (className === 'area-cb') {
        const selAll = document.getElementById('areaFilterAll');
        if (selAll) selAll.checked = isChecked;
    }

    applyFilters();
}

function handleSmartCheckbox(cb, className, selectAllId, context) {
    const sel = document.getElementById(selectAllId);
    if (sel && sel.checked) {
        document.querySelectorAll('.' + className).forEach(box => box.checked = false);
        cb.checked = true;
        sel.checked = false;
    } else {
        const boxes = document.querySelectorAll('.' + className);
        const allChecked = Array.from(boxes).every(box => box.checked);
        const anyChecked = Array.from(boxes).some(box => box.checked);

        if (!anyChecked) {
            boxes.forEach(box => box.checked = true);
            if (sel) sel.checked = true;
        } else if (sel) {
            sel.checked = allChecked;
        }
    }

    applyFilters();
}

// ── TABLE UTILS ────────────────────────────────────────────────────────

function filterTable() {
    const queries = Array.from(document.querySelectorAll('.col-search')).map(i => i.value.toLowerCase());
    const rows = document.getElementById("transactionBody").getElementsByTagName("tr");

    for (let row of rows) {
        const cells = row.getElementsByTagName("td");
        let show = queries.every((q, idx) => !q || (cells[idx]?.textContent.toLowerCase().includes(q)));
        row.style.display = show ? "" : "none";
    }
}

let sortState = { col: -1, asc: true };
function sortTable(idx) {
    const body = document.getElementById("transactionBody");
    const rows = Array.from(body.getElementsByTagName("tr"));

    sortState.asc = (sortState.col === idx) ? !sortState.asc : true;
    sortState.col = idx;

    const isNumeric = (idx === 0 || idx === 2);
    rows.sort((a, b) => {
        let vA = a.cells[idx].innerText.trim();
        let vB = b.cells[idx].innerText.trim();
        if (isNumeric) {
            let nA = parseFloat(vA.replace(/[^\d.-]/g, '')) || 0;
            let nB = parseFloat(vB.replace(/[^\d.-]/g, '')) || 0;
            return sortState.asc ? (nA - nB) : (nB - nA);
        }
        return sortState.asc ? vA.localeCompare(vB) : vB.localeCompare(vA);
    });
    body.innerHTML = "";
    rows.forEach(r => body.appendChild(r));
}

// ── PDF & FORM HELPERS ──────────────────────────────────────────────────

function updateLogoVal(btn) {
    const includeLogo = document.getElementById('includeLogo').checked;
    const input = btn?.closest('form')?.querySelector('input[name="include_logo"]');
    if (input) input.value = includeLogo ? "true" : "false";
}

function pdfSubmit(btn, frameTarget, preview) {
    const form = btn.closest('form');
    if (!form) return true;

    let actionInput = form.querySelector('.action_hidden');
    if (!actionInput) {
        actionInput = document.createElement('input');
        actionInput.type = 'hidden'; actionInput.name = 'action';
        actionInput.className = 'action_hidden';
        form.appendChild(actionInput);
    }
    actionInput.value = btn.value;

    updateLogoVal(btn);
    form.target = frameTarget;
    if (preview) UI.openPdfModal();

    // Disable temporarily
    const orig = btn.innerHTML;
    setTimeout(() => {
        btn.disabled = true; btn.style.opacity = "0.5";
        setTimeout(() => { btn.disabled = false; btn.style.opacity = "1"; btn.innerHTML = orig; }, 5000);
    }, 10);
    return true;
}

function downloadBulk(action, btn) {
    if (!btn && typeof event !== 'undefined') btn = event.currentTarget;
    if (btn && btn.disabled) return;

    UI.setBtnLoading(btn, "Generando", true);
    setTimeout(() => UI.setBtnLoading(btn, "", false), 5000);

    const form = document.createElement('form');
    form.method = 'POST'; form.action = '/generate-pdf-bulk';
    form.target = (action === 'descargar') ? 'downloadFrame' : 'pdfViewerFrame';
    if (action !== 'descargar') UI.openPdfModal();

    const areaAll = document.getElementById('areaFilterAll')?.checked;
    const dateAll = document.getElementById('dateFilterAll')?.checked;

    const fields = {
        date:            dateAll ? '' : getCheckboxValues('date-cb'),
        entrega_query:   document.getElementById('orderSearch').value,
        area:            areaAll ? '' : getCheckboxValues('area-cb'),
        centro:          document.querySelector('input[name="centro-filter"]:checked')?.value || '',
        has_ots_filter:  document.querySelector('input[name="ot-filter"]:checked')?.value || '',
        include_logo:    document.getElementById('includeLogo').checked ? 'true' : 'false',
        action:          action || 'previsualizar'
    };

    Object.entries(fields).forEach(([name, value]) => {
        const input = document.createElement('input');
        input.type = 'hidden'; input.name = name; input.value = value;
        form.appendChild(input);
    });

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);

}

async function syncData(e, onlyPoll = false) {
    const btn = e ? e.currentTarget : document.querySelector('button[onclick*="syncData"]');
    if (btn && btn.disabled && !onlyPoll) return;

    if (!onlyPoll) {
        // UI Feedback inmediato ANTES de la petición
        UI.setBtnLoading(btn, "Iniciando", true);

        try {
            const res = await DashboardAPI.sync();
            if (res.status === 'success') {
                UI.setBtnLoading(btn, "Sincronizando", true);
                startSyncPolling(btn);
            } else {
                alert("❌ " + res.message);
                UI.setBtnLoading(btn, "", false);
            }
        } catch (err) {
            console.error("Sync error:", err);
            alert("❌ Error de conexión con el servidor.");
            UI.setBtnLoading(btn, "", false);
        }
    } else if (btn) {
        UI.setBtnLoading(btn, "Sincronizando", true);
        startSyncPolling(btn);
    }
}

function startSyncPolling(btn) {
    const poll = setInterval(async () => {
        const status = await DashboardAPI.checkSyncStatus();
        if (!status.is_syncing) {
            clearInterval(poll);
            UI.setBtnLoading(btn, "", false);

            // Eliminar banner si existe
            const banner = document.getElementById('globalSyncBanner');
            if (banner) banner.remove();

            console.log("Sincronización completada.");
            const notification = document.createElement('div');
            notification.style = "position:fixed; bottom:20px; right:20px; background:#5DBAA9; color:white; padding:12px 24px; border-radius:8px; z-index:9999; box-shadow:0 4px 12px rgba(0,0,0,0.3); animation: slideIn 0.3s ease-out;";
            notification.innerHTML = "✅ Sincronización completada. Los datos han sido actualizados.";
            document.body.appendChild(notification);
            setTimeout(() => {
                notification.style.animation = "slideOut 0.3s ease-in";
                setTimeout(() => document.body.removeChild(notification), 300);
            }, 4000);
        }
    }, 3000);
}

// ── EXPOSE GLOBALS ─────────────────────────────────────────────────────

window.closePdfModal = UI.closePdfModal;
window.toggleMulti = UI.toggleMulti;
window.toggleCheckbox = (id) => { const cb = document.getElementById(id); if (cb) cb.checked = !cb.checked; };
window.applyCentroFilter = (val) => {
    document.querySelectorAll('#areaCheckboxes label[data-centro]').forEach(lbl => {
        const areaCentro = lbl.getAttribute('data-centro');
        const cb = lbl.querySelector('input[type="checkbox"]');
        const match = !val || areaCentro === val;
        lbl.style.display = match ? '' : 'none';
        if (cb) cb.checked = match;
    });
    applyFilters();
};
window.sortTable = sortTable;
window.filterTable = filterTable;
window.syncData = syncData;
// window.logout removido para usar la función global definida en _logout.html
window.downloadBulk = downloadBulk;
window.applyFilters = applyFilters;
window.toggleSelectAll = toggleSelectAll;
window.handleSmartCheckbox = handleSmartCheckbox;
window.checkSelectAllState = (cls, id) => {
    const boxes = document.querySelectorAll(`.${cls}`);
    const anyChecked = Array.from(boxes).some(cb => cb.checked);
    if (!anyChecked) boxes.forEach(b => b.checked = true);
    const sel = document.getElementById(id);
    if (sel) sel.checked = Array.from(boxes).every(b => b.checked);
    applyFilters();
};

window.toggleSidebar = function () {
    const sidebar = document.querySelector('aside.filters');
    if (sidebar) {
        sidebar.classList.toggle('active');
        if (sidebar.classList.contains('active')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }
};



/* --- dashboard_saas.js --- */
// ── SAAS WIDGET ENGINE ──────────────────────────────────────────────────
window.saasChartInstances = {};

async function initSaaSWidgets(params = null) {
    const widgets = document.querySelectorAll('.saas-widget');
    if (!widgets.length) return;

    // Si no se pasan params explicitos, leer del DOM actual
    if (!params) {
        const areaAll = document.getElementById('areaFilterAll')?.checked;
        const dateAll = document.getElementById('dateFilterAll')?.checked;
        params = {
            date: dateAll ? '' : getCheckboxValues('date-cb'),
            area: areaAll ? '' : getCheckboxValues('area-cb'),
            centro: document.querySelector('input[name="centro-filter"]:checked')?.value || '',
            has_ots_filter: document.querySelector('input[name="ot-filter"]:checked')?.value || ''
        };
    }
    const queryStr = new URLSearchParams(params).toString();

    for (const widget of widgets) {
        const queryId = widget.getAttribute('data-query-id');
        if (!queryId) continue;

        // Mostrar spinner
        widget.innerHTML = `<div style="display:flex; justify-content:center; align-items:center; height:100%;"><span class="spinner" style="width:24px; height:24px; border:3px solid var(--primary); border-top-color:transparent; border-radius:50%; animation: spin 1s linear infinite;"></span></div>`;

        try {
            const res = await DashboardAPI._fetch(`/api/widget/data/${queryId}?${queryStr}`);
            if (!res || !res.ok) {
                widget.innerHTML = `<div style="color:var(--rojo); text-align:center; padding:20px;">Error cargando widget</div>`;
                continue;
            }
            const payload = await res.json();
            const data = payload.data; // List of records

            widget.innerHTML = ''; // Limpiar spinner

            if (widget.classList.contains('saas-trellis-widget')) {
                renderSaaSTrellis(widget, queryId, data);
            } else {
                renderSaaSChart(widget, queryId, data);
            }

            // Calculo Dinámico de la Capacidad (Ignorando meses/semanas parciales y filtros)
            if (queryId === 'vl_sla_monthly_trend' || queryId === 'vl_sla_trend') {
                let baselineData = data;
                
                // Si hay filtro de fechas, debemos buscar la info histórica completa para que la capacidad no se achique
                if (params && params.date) {
                    try {
                        const baselineParams = new URLSearchParams(params);
                        baselineParams.delete('date');
                        const resBaseline = await DashboardAPI._fetch(`/api/widget/data/${queryId}?${baselineParams.toString()}`);
                        if (resBaseline && resBaseline.ok) {
                            const baselinePayload = await resBaseline.json();
                            baselineData = baselinePayload.data || data;
                        }
                    } catch (e) { console.error("Baseline fetch error", e); }
                }

                const materials = baselineData.map(r => r["Materiales Solicitados"] || r["Materiales_Solicitados"] || r["material_count"]).filter(v => typeof v === 'number');
                if (materials.length > 0) {
                    const maxVol = Math.max(...materials);
                    // Ignorar periodos inconclusos
                    const validMaterials = materials.filter(v => v > maxVol * 0.5);
                    const avg = validMaterials.length > 0 
                                ? validMaterials.reduce((a, b) => a + b, 0) / validMaterials.length 
                                : materials.reduce((a, b) => a + b, 0) / materials.length;
                    
                    const idealMin = Math.floor(avg * 0.9);
                    const idealMax = Math.floor(avg * 1.15);
                    const estab = Math.floor(avg * 1.3);
                    const sobre = Math.floor(avg * 1.5);

                    const isWeek = queryId === 'vl_sla_trend';
                    const suffix = isWeek ? 'mats/sem' : 'mats/mes';
                    const formatK = (val) => val >= 1000 ? (val / 1000).toFixed(1) + 'k' : val.toString();

                    const elIdeal = document.getElementById(isWeek ? 'cap-ideal-val-week' : 'cap-ideal-val');
                    const elEstab = document.getElementById(isWeek ? 'cap-estab-val-week' : 'cap-estab-val');
                    const elSobre = document.getElementById(isWeek ? 'cap-sobre-val-week' : 'cap-sobre-val');
                    
                    if (elIdeal) elIdeal.innerHTML = `${formatK(idealMin)} - ${formatK(idealMax)} <small>${suffix}</small>`;
                    if (elEstab) elEstab.innerHTML = `~ ${formatK(estab)} <small>${suffix}</small>`;
                    if (elSobre) elSobre.innerHTML = `> ${formatK(sobre)} <small>${suffix}</small>`;
                }
            }
        } catch (e) {
            console.error(`Error inicializando widget ${queryId}:`, e);
            widget.innerHTML = `<div style="color:var(--rojo); text-align:center; padding:20px;">Excepción cargando widget</div>`;
        }
    }
}

function renderSaaSChart(container, queryId, data) {
    if (!data || !data.length) {
        container.innerHTML = `<div style="color:var(--text-muted); text-align:center; padding:20px;">Sin datos</div>`;
        return;
    }
    
    // Asumimos que la primera columna es el eje X (label), y el resto numéricas.
    // Opcionalmente podemos tener una columna de series (como area).
    // Por simplicidad, tomemos las keys del primer objeto:
    const keys = Object.keys(data[0]);
    // Extraemos label
    let labelKey = keys.find(k => k.toLowerCase().includes('label') || k.toLowerCase().includes('date') || k.toLowerCase().includes('week') || k.toLowerCase().includes('month'));
    if (!labelKey) labelKey = keys[0];

    // Extraemos numéricos
    const numericKeys = keys.filter(k => k !== labelKey && typeof data[0][k] === 'number');

    const labels = data.map(r => r[labelKey]);
    
    const colors = ["#5DBAA9", "#EA7600", "#10B981", "#3b82f6", "#8b5cf6", "#ec4899"];
    
    const datasets = numericKeys.map((nk, idx) => {
        const color = colors[idx % colors.length];
        return {
            label: nk.replace(/_/g, ' ').toUpperCase(),
            data: data.map(r => r[nk]),
            borderColor: color,
            backgroundColor: (idx === 0) ? `${color}1a` : 'transparent',
            borderWidth: 3,
            fill: (idx === 0 && queryId !== 'vl_weekly_evolution'),
            tension: 0.4,
            pointBackgroundColor: color,
            pointRadius: 3,
            yAxisID: idx === 0 ? 'y' : `y${idx}`
        };
    });

    const canvas = document.createElement('canvas');
    container.appendChild(canvas);

    const scales = {
        y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' }, position: 'left' },
        x: { grid: { display: false }, ticks: { color: '#94a3b8', maxRotation: 45, minRotation: 45, autoSkip: true, maxTicksLimit: 12 } }
    };

    // Crear ejes Y adicionales si hay más datasets (maximo 2 para no ensuciar)
    if (datasets.length > 1) {
        scales['y1'] = {
            beginAtZero: true,
            position: 'right',
            grid: { drawOnChartArea: false },
            ticks: { color: '#94a3b8' }
        };
        // Si hubiera más de 2 datasets (y2, y3...), Chartjs ignora config por defecto o los oculta si no se declaran.
    }

    window.saasChartInstances = window.saasChartInstances || {};
    if (window.saasChartInstances[queryId]) {
        window.saasChartInstances[queryId].destroy();
    }

    window.saasChartInstances[queryId] = new Chart(canvas.getContext('2d'), {
        type: 'line',
        plugins: [ChartDataLabels],
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: datasets.length > 1, labels: { color: '#94a3b8' } },
                datalabels: {
                    display: true,
                    color: (ctx) => ctx.dataset.borderColor,
                    align: 'top',
                    font: { weight: 'bold', size: 10 },
                    formatter: (v) => v > 0 ? (v % 1 !== 0 ? v.toFixed(1)+'%' : v.toLocaleString('de-DE')) : ''
                }
            },
            scales: scales
        }
    });
}

function renderSaaSTrellis(container, queryId, data) {
    if (!data || !data.length) return;
    
    // Asumir que tenemos columnas: area, label (X), y métricas
    const keys = Object.keys(data[0]);
    let areaKey = keys.find(k => k.toLowerCase() === 'area' || k.toLowerCase().includes('area') || k.toLowerCase() === 'categoria');
    if (!areaKey) return renderSaaSChart(container, queryId, data);

    // Configurar el contenedor principal para que funcione como grilla si no lo tiene
    container.style.display = 'grid';
    container.style.gridTemplateColumns = 'repeat(auto-fill, minmax(220px, 1fr))';
    container.style.gap = '15px';
    container.style.overflowY = 'auto';
    container.style.paddingRight = '5px';

    let labelKey = keys.find(k => k !== areaKey && (k.toLowerCase().includes('label') || k.toLowerCase().includes('date') || k.toLowerCase().includes('week')));
    if (!labelKey) labelKey = keys.find(k => k !== areaKey);

    const numericKey = keys.find(k => k !== areaKey && k !== labelKey && typeof data[0][k] === 'number');
    const matKey = keys.find(k => k !== areaKey && k !== labelKey && k !== numericKey && typeof data[0][k] === 'number');

    // Agrupar por área
    const grouped = {};
    data.forEach(r => {
        const area = r[areaKey];
        if (!grouped[area]) grouped[area] = { labels: [], data: [], sum: 0, count: 0, totalMats: 0 };
        grouped[area].labels.push(r[labelKey]);
        grouped[area].data.push(r[numericKey]);
        grouped[area].sum += r[numericKey];
        grouped[area].count += 1;
        if (matKey) grouped[area].totalMats += (r[matKey] || 0);
    });

    const premiumColors = ["#22c55e", "#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#ec4899"];
    let i = 0;

    window.saasChartInstances[`${queryId}_trellis`] = [];

    for (const [area, areaData] of Object.entries(grouped)) {
        const color = premiumColors[i % premiumColors.length];
        i++;
        const avg = areaData.count > 0 ? (areaData.sum / areaData.count).toFixed(1) : 0;
        
        let statusColor = '#ef4444';
        if (avg >= 95) statusColor = '#22c55e';
        else if (avg >= 85) statusColor = '#f59e0b';

        const wrapper = document.createElement('div');
        wrapper.className = 'trellis-item';
        wrapper.setAttribute('data-area', area);
        wrapper.style.cssText = 'background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 10px; height: 220px;';
        
        const title = document.createElement('h4');
        const matsHtml = matKey ? ` <span style="color:#94a3b8; font-weight:normal; font-size:0.7rem;">(${areaData.totalMats} mats)</span>` : '';
        title.innerHTML = `${area}${matsHtml} <span style="color: ${statusColor}; margin-left: 8px; font-weight: bold;">Avg: ${avg}%</span>`;
        title.style.cssText = 'font-size: 0.75rem; color: #94a3b8; margin-bottom: 8px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px;';
        wrapper.appendChild(title);
        
        const canvasWrapper = document.createElement('div');
        canvasWrapper.style.cssText = 'position: relative; height: 160px; width: 100%;';
        const canvas = document.createElement('canvas');
        canvasWrapper.appendChild(canvas);
        wrapper.appendChild(canvasWrapper);
        container.appendChild(wrapper);

        const chart = new Chart(canvas.getContext('2d'), {
            type: 'line',
            plugins: [ChartDataLabels],
            data: {
                labels: areaData.labels,
                datasets: [
                    { label: area, data: areaData.data, borderColor: color, backgroundColor: 'transparent', borderWidth: 3, pointRadius: 2, tension: 0.3 },
                    { label: 'Meta (95%)', data: new Array(areaData.labels.length).fill(95), borderColor: 'rgba(255, 255, 255, 0.1)', borderWidth: 1, borderDash: [5, 5], pointRadius: 0, fill: false }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    datalabels: { display: true, color: color, font: { size: 9, weight: 'bold' }, align: 'top', formatter: (v, ctx) => ctx.datasetIndex === 0 ? v + '%' : '' }
                },
                scales: {
                    y: { min: 0, max: 100, ticks: { display: false }, grid: { display: false } },
                    x: { ticks: { autoSkip: true, maxTicksLimit: 5, font: { size: 8 } }, grid: { display: false } }
                }
            }
        });
        window.saasChartInstances[`${queryId}_trellis`].push(chart);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Sincronizar estado inicial de radio buttons sin disparar recargas innecesarias
    const centroAll = document.getElementById('centroAll');
    if (centroAll) centroAll.checked = true;

    const otAll = document.querySelector('input[name="ot-filter"][value=""]');
    if (otAll) otAll.checked = true;

    // Solo verificamos el estado de sincronización, no forzamos recarga de filtros
    DashboardAPI.checkSyncStatus().then(status => {
        if (status.is_syncing) {
            syncData(null, true); // Iniciar solo el polling
        }
    });

    // Iniciar el motor SaaS    // Cargar widgets inmediatamente al iniciar
    initSaaSWidgets();
});

window.initSaaSWidgets = initSaaSWidgets;


/* --- saas_engine_core.js --- */
/**
 * Motor SaaS V2: Server-Driven UI Asíncrona
 * Lee contenedores con .saas-widget-v2 y renderiza gráficos o KPIs.
 */

window.saasChartInstancesV2 = {};

async function initSaaSWidgetsV2(params = null, rootElement = document) {
    const widgets = rootElement.querySelectorAll('.saas-widget-v2');
    if (!widgets.length) return;

    if (!params) {
        const areaAll = document.getElementById('chartAreaFilterAll')?.checked;
        const areaValues = areaAll ? '' : Array.from(document.querySelectorAll('.chart-area-cb:checked')).map(cb => cb.value).join(',');
        
        // Asumiendo que podemos tener filtro por año (por ahora estático, pero se preparará para la URL)
        params = {
            area: areaValues,
            year: new Date().getFullYear().toString()
        };
    }
    const queryStr = new URLSearchParams(params).toString();

    for (const widget of widgets) {
        const queryId = widget.getAttribute('data-query-id');
        if (!queryId) continue;

        // Spinner inicial
        widget.innerHTML = `<div style="display:flex; justify-content:center; align-items:center; height:100%;"><span class="spinner" style="width:24px; height:24px; border:3px solid var(--primary); border-top-color:transparent; border-radius:50%; animation: spin 1s linear infinite;"></span></div>`;

        try {
            const queryStr = new URLSearchParams(params).toString();
            const cacheBuster = `_t=${Date.now()}`;
            const finalQueryStr = queryStr ? `${queryStr}&${cacheBuster}` : cacheBuster;
            const res = await fetch(`/api/widget/${queryId}?${finalQueryStr}`);
            
            if (!res || !res.ok) {
                widget.innerHTML = `<div style="color:var(--rojo); font-size: 0.9rem;">Error API</div>`;
                continue;
            }
            const data = await res.json();
            
            widget.innerHTML = ''; // Limpiar spinner

            if (data.isEmpty) {
                widget.innerHTML = `<div style="color:var(--text-muted); font-size: 0.9rem;">Sin datos</div>`;
                continue;
            }
            
            if (data.legacy) {
                widget.innerHTML = `<div style="color:var(--naranja); font-size: 0.8rem; text-align: center; padding: 10px; border: 1px dashed rgba(255,255,255,0.1); border-radius: 8px;">Widget Legacy.<br>Requiere refactor en el Studio.</div>`;
                continue;
            }

            if (widget.classList.contains('saas-kpi')) {
                // Renderizar KPI Numérico
                let val = "0";
                if (data.datasets && data.datasets.length > 0 && data.datasets[0].data.length > 0) {
                    val = data.datasets[0].data[0];
                } else if (data.raw_data && data.raw_data.length > 0) {
                    const firstRow = data.raw_data[0];
                    // Try to avoid common dimension keys if falling back to raw_data
                    const valCol = Object.keys(firstRow).find(k => !['fecha', 'categoria', 'label'].includes(k.toLowerCase())) || Object.keys(firstRow)[0];
                    val = firstRow[valCol];
                }
                let displayVal = val.toLocaleString ? val.toLocaleString('de-DE') : val;
                if (data.format === 'percent') displayVal += '%';
                else if (data.format === 'currency') displayVal = '$' + displayVal;
                widget.innerHTML = `<span style="font-size: 1.8rem; font-weight: 800; color: inherit;">${displayVal}</span>`;
            } else if (widget.classList.contains('saas-trellis-widget')) {
                // Renderizar Trellis (Múltiples Minigráficos)
                if (!data.raw_data || !data.raw_data.length) {
                    widget.innerHTML = `<div style="color:var(--text-muted); text-align:center; padding:20px;">Sin datos estructurados para trellis</div>`;
                    continue;
                }
                const keys = Object.keys(data.raw_data[0]);
                let areaKey = keys.find(k => k.toLowerCase() === 'area' || k.toLowerCase().includes('area') || k.toLowerCase() === 'categoria' || k.toLowerCase() === '__area_expr__');
                if (!areaKey) areaKey = keys[0];

                widget.style.display = 'grid';
                widget.style.gridTemplateColumns = 'repeat(auto-fill, minmax(220px, 1fr))';
                widget.style.gap = '15px';
                widget.style.overflowY = 'auto';
                widget.style.paddingRight = '5px';

                let labelKey = keys.find(k => k !== areaKey && (k.toLowerCase().includes('fecha') || k.toLowerCase().includes('date') || k.toLowerCase().includes('week')));
                if (!labelKey) labelKey = keys.find(k => k !== areaKey);

                const numericKey = keys.find(k => k !== areaKey && k !== labelKey && typeof data.raw_data[0][k] === 'number');
                const effKey = keys.includes('efficiency') ? 'efficiency' : numericKey;
                const countKey = keys.includes('total_count') ? 'total_count' : (keys.includes('Materiales_Solicitados') ? 'Materiales_Solicitados' : null);

                const grouped = {};
                data.raw_data.forEach(r => {
                    const area = r[areaKey];
                    if (!grouped[area]) grouped[area] = { labels: [], data: [], counts: [], sum: 0, count: 0 };
                    grouped[area].labels.push(r[labelKey]);
                    grouped[area].data.push(r[effKey]);
                    if (countKey) grouped[area].counts.push(r[countKey]);
                    grouped[area].sum += r[effKey];
                    grouped[area].count += 1;
                });

                const premiumColors = ["#22c55e", "#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#ec4899"];
                let i = 0;

                if (!window.saasChartInstancesV2[`${queryId}_trellis`]) {
                    window.saasChartInstancesV2[`${queryId}_trellis`] = [];
                } else {
                    window.saasChartInstancesV2[`${queryId}_trellis`].forEach(c => c.destroy());
                    window.saasChartInstancesV2[`${queryId}_trellis`] = [];
                }

                for (const [area, areaData] of Object.entries(grouped)) {
                    const color = premiumColors[i % premiumColors.length];
                    i++;
                    const avg = areaData.count > 0 ? (areaData.sum / areaData.count).toFixed(1) : 0;
                    
                    let avgMatsText = '';
                    if (areaData.counts && areaData.counts.length > 0) {
                        const totalMats = areaData.counts.reduce((a, b) => a + b, 0);
                        const avgMats = (totalMats / areaData.counts.length).toFixed(0);
                        const suffix = queryId.includes('week') || queryId === 'vl_sla_area_trend' ? 'mats/sem' : 'mats/mes';
                        avgMatsText = ` | ~${avgMats} ${suffix}`;
                    }
                    
                    let statusColor = '#ef4444';
                    if (avg >= 90) statusColor = '#22c55e';
                    else if (avg >= 85) statusColor = '#f59e0b';

                    const wrapper = document.createElement('div');
                    wrapper.className = 'trellis-item';
                    wrapper.setAttribute('data-area', area);
                    wrapper.style.cssText = 'background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 10px; height: 220px; cursor: pointer;';
                    
                    wrapper.onclick = () => {
                        if (window.openDrilldownModal) window.openDrilldownModal(queryId, area);
                    };
                    
                    const title = document.createElement('h4');
                    title.innerHTML = `${area} <span style="color: ${statusColor}; margin-left: 8px; font-weight: bold;">Avg: ${avg}%${avgMatsText}</span>`;
                    title.style.cssText = 'font-size: 0.75rem; color: #94a3b8; margin-bottom: 8px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px; pointer-events: none;';
                    wrapper.appendChild(title);
                    
                    const canvasWrapper = document.createElement('div');
                    canvasWrapper.style.cssText = 'position: relative; height: 160px; width: 100%; pointer-events: none;';
                    const canvas = document.createElement('canvas');
                    canvasWrapper.appendChild(canvas);
                    wrapper.appendChild(canvasWrapper);
                    widget.appendChild(wrapper);

                    let chartDatasets = [
                        { label: area, data: areaData.data, borderColor: color, backgroundColor: 'transparent', borderWidth: 3, pointRadius: 2, tension: 0.3, yAxisID: 'y' },
                        { label: 'Meta (90%)', data: new Array(areaData.labels.length).fill(90), borderColor: 'rgba(255, 255, 255, 0.1)', borderWidth: 1, borderDash: [5, 5], pointRadius: 0, fill: false, yAxisID: 'y' }
                    ];

                    const chart = new Chart(canvas.getContext('2d'), {
                        type: 'line',
                        plugins: [ChartDataLabels],
                        data: {
                            labels: areaData.labels,
                            datasets: chartDatasets
                        },
                        options: {
                            responsive: true, maintainAspectRatio: false,
                            plugins: {
                                legend: { display: false },
                                datalabels: { display: true, color: color, font: { size: 9, weight: 'bold' }, align: 'top', formatter: (v, ctx) => ctx.datasetIndex === 0 ? v + '%' : '' }
                            },
                            scales: {
                                y: { min: 0, max: 100, ticks: { display: false }, grid: { display: false }, position: 'left' },
                                x: { ticks: { autoSkip: true, maxTicksLimit: 5, font: { size: 8 } }, grid: { display: false } }
                            }
                        }
                    });
                    window.saasChartInstancesV2[`${queryId}_trellis`].push(chart);
                }
            } else {
                const canvas = document.createElement('canvas');
                widget.appendChild(canvas);
                
                if (queryId === 'inv_cmv_201_mensual') {
                    const chartBox = widget.closest('.chart-box');
                    if (chartBox) {
                        chartBox.style.cursor = 'pointer';
                        chartBox.onclick = () => {
                            const modal = document.getElementById('modalCmv201');
                            if (modal) {
                                if (window.openModal) window.openModal('modalCmv201');
                                else modal.classList.add('show');
                                
                                if (window.loadCmv201Data) {
                                    window.loadCmv201Data('planificado');
                                }
                            }
                        };
                    }
                } else if (queryId === 'inv_cmv_261_221_mensual') {
                    const chartBox = widget.closest('.chart-box');
                    if (chartBox) {
                        chartBox.style.cursor = 'pointer';
                        chartBox.onclick = () => {
                            const modal = document.getElementById('modalCmv261');
                            if (modal) {
                                if (window.openModal) window.openModal('modalCmv261');
                                else modal.classList.add('show');
                                
                                if (window.loadCmv261Data) {
                                    window.loadCmv261Data('planificado');
                                }
                            }
                        };
                    }
                }

                // Limpiar instancia previa si existe
                if (window.saasChartInstancesV2[queryId]) {
                    window.saasChartInstancesV2[queryId].destroy();
                }

                // Actualizar título con el filtro activo (UI amigable)
                const h3 = widget.closest('.chart-box')?.querySelector('h3');
                if (h3) {
                    if (!h3.dataset.originalText) h3.dataset.originalText = h3.innerText.replace(/ \[Filtro: .*\]$/, '');
                    const fText = params.area ? params.area : 'Todas';
                    h3.innerText = `${h3.dataset.originalText} [Filtro: ${fText.substring(0,30)}${fText.length>30?'...':''}]`;
                }

                const options = {
                    responsive: true,
                    maintainAspectRatio: false,
                    onClick: (e, elements, chart) => {
                        if (queryId === 'inv_cmv_201_mensual') {
                            const modal = document.getElementById('modalCmv201');
                            if (modal) {
                                if (window.openModal) window.openModal('modalCmv201');
                                else modal.classList.add('show');
                                if (window.loadCmv201Data) {
                                    window.loadCmv201Data('planificado');
                                }
                            }
                            return;
                        }
                        if (queryId === 'inv_cmv_261_221_mensual') {
                            const modal = document.getElementById('modalCmv261');
                            if (modal) {
                                if (window.openModal) window.openModal('modalCmv261');
                                else modal.classList.add('show');
                                if (window.loadCmv261Data) {
                                    window.loadCmv261Data('planificado');
                                }
                            }
                            return;
                        }
                        if (!elements || !elements.length) return;
                        try {
                            const label = chart.data.labels[elements[0].index];
                            if (window.openDrilldownModal) {
                                window.openDrilldownModal(queryId, label);
                            }
                        } catch (err) {
                            console.error("Error onClick", err);
                        }
                    },
                    plugins: {
                        legend: { display: data.datasets.length > 1, labels: { color: '#94a3b8' } },
                        datalabels: {
                            display: true,
                            color: '#ffffff',
                            font: { weight: 'bold', size: 10 },
                            formatter: (v, ctx) => {
                                if (v <= 0) return '';
                                let datasetLabel = ctx.chart.data.datasets[ctx.datasetIndex].label;
                                let dsFormat = (data.dataset_formats && data.dataset_formats[datasetLabel]) ? data.dataset_formats[datasetLabel] : data.format;

                                if (dsFormat === 'percent' && (data.chartType === 'doughnut' || data.chartType === 'pie')) {
                                    let sum = 0;
                                    ctx.chart.data.datasets[0].data.forEach(d => { sum += d; });
                                    if (sum === 0) return '0%';
                                    return (v * 100 / sum).toFixed(1) + '%';
                                }
                                return dsFormat === 'percent' ? v.toFixed(1)+'%' : v.toLocaleString('de-DE');
                            }
                        }
                    },
                    scales: {
                        y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                    }
                };

                // Configuración de escalas duales si hay múltiples datasets
                if (data.datasets.length > 1 && data.chartType !== 'doughnut' && data.chartType !== 'pie') {
                    options.scales.y1 = {
                        beginAtZero: true,
                        position: 'right',
                        grid: { drawOnChartArea: false }, // avoid overlapping grid lines
                        ticks: { color: '#94a3b8' }
                    };
                    data.datasets[1].yAxisID = 'y1';
                }

                // Si es doughnut o pie, ocultamos las escalas
                if (data.chartType === 'doughnut' || data.chartType === 'pie') {
                    delete options.scales;
                }

                // Generar colores si el backend no los envió (simplificado)
                const colors = ["#5DBAA9", "#EA7600", "#3A5AAB", "#EAB308", "#EC4899", "#8B5CF6", "#10B981"];
                data.datasets.forEach((ds, i) => {
                    if (!ds.backgroundColor) {
                        if (data.chartType === 'pie' || data.chartType === 'doughnut') {
                            ds.backgroundColor = data.labels.map((_, idx) => colors[idx % colors.length]);
                            ds.borderColor = data.labels.map((_, idx) => colors[idx % colors.length]);
                            ds.borderWidth = 1;
                        } else {
                            ds.backgroundColor = data.chartType === 'line' ? 'transparent' : colors[i % colors.length];
                            ds.borderColor = colors[i % colors.length];
                            if (data.chartType === 'line') ds.borderWidth = 3;
                        }
                    }
                });

                window.saasChartInstancesV2[queryId] = new Chart(canvas.getContext('2d'), {
                    type: data.chartType || 'bar',
                    plugins: [ChartDataLabels],
                    data: {
                        labels: data.labels,
                        datasets: data.datasets
                    },
                    options: options
                });

                // Calculo Dinámico de la Capacidad Cruzada
                if ((queryId === 'vl_sla_monthly_trend' || queryId === 'vl_sla_trend') && data.datasets.length >= 2) {
                    
                    let slaDataset = data.datasets.find(d => d.label.includes('SLA') || d.label.toLowerCase() === 'valor') || data.datasets[0];
                    let volDataset = data.datasets.find(d => d !== slaDataset) || data.datasets[1];
                    
                    const slaData = slaDataset.data;
                    const volData = volDataset.data;
                    
                    let maxSla = Math.max(...slaData.map(Number).filter(n => !isNaN(n)));
                    if (maxSla === -Infinity || maxSla <= 0) maxSla = 90;
                    
                    let tIdeal = maxSla < 90 ? Math.floor(maxSla) : 90;
                    let tRisk = tIdeal - 5;
                    
                    let idealVols = [];
                    for (let i = 0; i < slaData.length; i++) {
                        let sla = parseFloat(slaData[i]);
                        let vol = parseFloat(volData[i]);
                        if (!isNaN(sla) && !isNaN(vol) && sla >= tIdeal) {
                            idealVols.push(vol);
                        }
                    }
                    
                    let baseCap = 0;
                    if (idealVols.length > 0) {
                        const maxV = Math.max(...idealVols);
                        const robustVols = idealVols.filter(v => v > maxV * 0.5); // Ignorar periodos parciales
                        baseCap = robustVols.length > 0 
                            ? robustVols.reduce((a, b) => a + b, 0) / robustVols.length
                            : idealVols.reduce((a, b) => a + b, 0) / idealVols.length;
                    } else {
                        const validVols = volData.map(Number).filter(n => !isNaN(n) && n > 0);
                        if (validVols.length > 0) {
                            const maxV = Math.max(...validVols);
                            const robustVols = validVols.filter(v => v > maxV * 0.5);
                            baseCap = robustVols.length > 0 
                                ? robustVols.reduce((a, b) => a + b, 0) / robustVols.length
                                : validVols.reduce((a, b) => a + b, 0) / validVols.length;
                        }
                    }
                    
                    const valIdeal = Math.floor(baseCap);
                    const valRisk = Math.floor(baseCap * 1.15);
                    const valFail = Math.floor(baseCap * 1.30);
                    
                    const isWeek = queryId === 'vl_sla_trend';
                    const suffix = isWeek ? 'mats/sem' : 'mats/mes';
                    
                    const elIdeal = document.getElementById(isWeek ? 'cap-ideal-val-week' : 'cap-ideal-val');
                    const elRisk = document.getElementById(isWeek ? 'cap-estab-val-week' : 'cap-estab-val');
                    const elFail = document.getElementById(isWeek ? 'cap-sobre-val-week' : 'cap-sobre-val');
                    
                    if (elIdeal) {
                        elIdeal.innerHTML = `~ ${valIdeal.toLocaleString('de-DE')} <small>${suffix}</small>`;
                        elIdeal.previousElementSibling.innerHTML = `Punto Ideal (≥${tIdeal}%)`;
                    }
                    if (elRisk) {
                        elRisk.innerHTML = `~ ${valRisk.toLocaleString('de-DE')} <small>${suffix}</small>`;
                        elRisk.previousElementSibling.innerHTML = `Estabilidad (${tRisk}-${tIdeal - 1}%)`;
                    }
                    if (elFail) {
                        elFail.innerHTML = `> ${valFail.toLocaleString('de-DE')} <small>${suffix}</small>`;
                        elFail.previousElementSibling.innerHTML = `Sobrecarga (<${tRisk}%)`;
                    }
                }
            }

        } catch (e) {
            console.error(`Error inicializando widget V2 ${queryId}:`, e);
            widget.innerHTML = `<div style="color:var(--rojo); font-size: 0.9rem;">Error V2</div>`;
        }
    }
}

// Sugerencias de Abastecimiento (MB5B + Consumos)
async function loadReplenishmentSuggestions(freq = 'all') {
    const tbody = document.getElementById('replenishment-body');
    if (!tbody) return;
    
    tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; padding: 2rem;"><span class="spinner" style="width:24px; height:24px; border:3px solid var(--primary); border-top-color:transparent; border-radius:50%; animation: spin 1s linear infinite; display:inline-block;"></span><br>Calculando inventario y autonomía...</td></tr>`;
    
    // Actualizar botones UI
    document.querySelectorAll('.freq-btn').forEach(btn => {
        if (btn.dataset.freq === freq) {
            btn.classList.remove('btn-outline');
            btn.classList.add('btn-primary');
        } else {
            btn.classList.add('btn-outline');
            btn.classList.remove('btn-primary');
        }
    });
    
    try {
        const res = await fetch(`/api/inventory/replenishment-suggestions?freq=${freq}`);
        if (!res.ok) throw new Error('Error en API');
        const json = await res.json();
        const data = json.data;
        
        if (!data || data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; padding: 2rem; color: var(--verde);">No hay sugerencias para este rango de frecuencia.</td></tr>`;
            return;
        }
        
        tbody.innerHTML = '';
        data.forEach(item => {
            const tr = document.createElement('tr');
            // Formatear números
            const stockActual = parseFloat(item.stock_actual).toLocaleString('de-DE');
            const usoMensual = parseFloat(item.consumo_mensual).toLocaleString('de-DE');
            
            // Formatear frecuencia legible
            let frecText = 'N/A';
            const m = parseFloat(item.frec_meses);
            if (m > 0) {
                const totalDays = Math.round(m * 30.4);
                if (totalDays < 30) {
                    frecText = `Cada ${totalDays} día${totalDays === 1 ? '' : 's'}`;
                } else {
                    const months = Math.floor(totalDays / 30.4);
                    const days = Math.round(totalDays % 30.4);
                    if (days === 0) {
                        frecText = `Cada ${months} mes${months === 1 ? '' : 'es'}`;
                    } else {
                        frecText = `Cada ${months} mes${months === 1 ? '' : 'es'} y ${days} día${days === 1 ? '' : 's'}`;
                    }
                }
            }
            
            // Destacar autonomía < 1
            const autoNum = parseFloat(item.autonomia_meses);
            const autoColor = autoNum < 0.5 ? 'var(--rojo)' : (autoNum < 1.0 ? 'var(--naranja)' : 'inherit');
            const autoText = autoNum < 0 ? 'Sin Stock' : autoNum.toFixed(2) + ' meses';
            
            // Etiqueta ABC
            let abcBadge = '';
            if (item.clasificacion_abc === 'A') {
                abcBadge = '<span style="background: rgba(var(--azul-rgb), 0.1); color: var(--azul); padding: 2px 8px; border-radius: 4px; font-weight: bold;">A</span>';
            } else if (item.clasificacion_abc === 'B') {
                abcBadge = '<span style="background: rgba(var(--verde-rgb), 0.1); color: var(--verde); padding: 2px 8px; border-radius: 4px; font-weight: bold;">B</span>';
            } else {
                abcBadge = '<span style="background: rgba(100, 116, 139, 0.1); color: #64748b; padding: 2px 8px; border-radius: 4px; font-weight: bold;">C</span>';
            }
            
            tr.innerHTML = `
                <td style="font-family: monospace; font-weight: bold;">${item.material}</td>
                <td style="white-space: normal; min-width: 200px;">${item.descripcion || 'Sin descripción'}</td>
                <td>${item.umb}</td>
                <td>${item.stock_inicial}</td>
                <td style="font-weight: bold;">${stockActual}</td>
                <td>${usoMensual}</td>
                <td><span style="background: rgba(0,0,0,0.05); padding: 4px 8px; border-radius: 4px; font-size: 0.85rem;">${frecText}</span></td>
                <td style="font-weight: bold; color: ${autoColor};">${autoText}</td>
                <td style="text-align: center;">${abcBadge}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error(err);
        tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 2rem; color: var(--rojo);">Ocurrió un error calculando las sugerencias.</td></tr>`;
    }
}

// Interceptar o inyectarnos en el update
document.addEventListener('DOMContentLoaded', () => {
    // Iniciar
    setTimeout(() => {
        initSaaSWidgetsV2();
        loadReplenishmentSuggestions();
        
        // Setup Filtros de Frecuencia
        document.querySelectorAll('.freq-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const f = e.target.dataset.freq;
                loadReplenishmentSuggestions(f);
            });
        });
    }, 500); // Pequeño delay para asegurar que el DOM y Chart.js estén listos
});

// Exponer globalmente
window.initSaaSWidgetsV2 = initSaaSWidgetsV2;
window.loadReplenishmentSuggestions = loadReplenishmentSuggestions;



/* --- saas_engine_drilldown.js --- */
window.openDrilldownModal = async function(queryId, segmentLabel, materialId = null) {
    if (queryId === 'inv_cmv_201_mensual') {
        window.openCmv201Modal();
        return;
    }

    const modal = document.getElementById('drilldownModal');
    if (!modal) return;
    
    let backBtnHtml = '';
    if (materialId) {
        document.getElementById('drilldownModalTitle').innerText = `📊 Áreas para: ${materialId}`;
        backBtnHtml = `<button onclick="window.openDrilldownModal('${queryId}', '${segmentLabel}')" style="margin-bottom: 15px; padding: 5px 15px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: white; border-radius: 4px; cursor: pointer; transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">⬅ Volver a Materiales</button>`;
    } else {
        document.getElementById('drilldownModalTitle').innerText = `📊 Detalles: ${segmentLabel}`;
    }

    document.getElementById('drilldownSpinner').style.display = 'block';
    document.getElementById('drilldownTableContainer').innerHTML = backBtnHtml;
    modal.classList.add('active');
    
    try {
        let url = `/api/widget/${queryId}/drilldown?segment=${encodeURIComponent(segmentLabel)}`;
        if (materialId) {
            url += `&material=${encodeURIComponent(materialId)}`;
        }
        const res = await fetch(url);
        const data = await res.json();
        
        document.getElementById('drilldownSpinner').style.display = 'none';
        
        if (data.detail) {
            document.getElementById('drilldownTableContainer').innerHTML += `<div style="text-align:center; padding:20px; color:var(--naranja);">${data.detail}<br><small>(Abre el Studio y publica el gráfico para actualizarlo al nuevo motor)</small></div>`;
            return;
        }

        if (!data || data.length === 0) {
            document.getElementById('drilldownTableContainer').innerHTML += '<div style="text-align:center; padding:20px; color:#94a3b8;">No se encontraron detalles.</div>';
            return;
        }
        
        const cols = Object.keys(data[0]);
        let html = '<table class="mini-table" id="drilldownModalTable" style="width: 100%; border-collapse: collapse;"><thead><tr>';
        cols.forEach((c, i) => html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: left; cursor: pointer; white-space: nowrap;" onclick="window.sortDrilldownTable(${i})" title="Clic para ordenar">${c} ↕</th>`);
        html += '</tr><tr class="filter-row">';
        cols.forEach(c => html += `<th style="padding: 4px;"><input type="text" class="col-filter" placeholder="🔍 Filtrar..." onkeyup="window.filterDrilldownTable()" style="width: 100%; min-width: 60px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 4px; border-radius: 4px; font-size: 0.8rem;"></th>`);
        html += '</tr></thead><tbody>';
        
        data.forEach(row => {
            const isClickable = !materialId && row['Material'];
            const trStyle = isClickable ? 'cursor: pointer; transition: background 0.2s;' : '';
            const onClickAttr = isClickable ? `onclick="window.openDrilldownModal('${queryId}', '${segmentLabel}', '${row['Material']}')" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'"` : '';
            
            html += `<tr style="${trStyle}" ${onClickAttr}>`;
            cols.forEach(c => html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9;">${row[c] !== null ? row[c] : ''}</td>`);
            html += '</tr>';
        });
        html += '</tbody></table>';
        
        document.getElementById('drilldownTableContainer').innerHTML += html;
        
    } catch (e) {
        document.getElementById('drilldownSpinner').style.display = 'none';
        document.getElementById('drilldownTableContainer').innerHTML += `<div style="color:var(--rojo); padding:20px; text-align:center;">Error al cargar detalles: ${e.message}</div>`;
    }
};

// --- Drilldown Table Utilities ---
window.sortDrilldownTable = function(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("drilldownModalTable");
    if(!table) return;
    switching = true;
    dir = "asc"; 
    while (switching) {
        switching = false;
        rows = table.querySelectorAll("tbody tr");
        for (i = 0; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            let valX = x.innerText.trim().toLowerCase();
            let valY = y.innerText.trim().toLowerCase();
            
            if (!isNaN(parseFloat(valX)) && !isNaN(parseFloat(valY))) {
                valX = parseFloat(valX);
                valY = parseFloat(valY);
            }

            if (dir == "asc") {
                if (valX > valY) { shouldSwitch = true; break; }
            } else if (dir == "desc") {
                if (valX < valY) { shouldSwitch = true; break; }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount ++; 
        } else {
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
};

window.filterDrilldownTableTimer = null;
window.filterDrilldownTable = function() {
    clearTimeout(window.filterDrilldownTableTimer);
    window.filterDrilldownTableTimer = setTimeout(() => {
        var table = document.getElementById("drilldownModalTable");
        if(!table) return;
        var inputs = Array.from(table.querySelectorAll("thead .col-filter"));
        var activeFilters = inputs.map((inp, idx) => ({ value: inp.value.toLowerCase(), index: idx })).filter(f => f.value);
        
        var trs = table.querySelectorAll("tbody tr");
        
        // Use requestAnimationFrame for smoother UI if there are many rows
        let i = 0;
        const chunk = 100;
        
        function processChunk() {
            let end = Math.min(i + chunk, trs.length);
            for (; i < end; i++) {
                let tr = trs[i];
                let display = '';
                if (activeFilters.length > 0) {
                    let tds = tr.getElementsByTagName("td");
                    for (let f of activeFilters) {
                        let td = tds[f.index];
                        if (td && td.textContent.toLowerCase().indexOf(f.value) === -1) {
                            display = 'none';
                            break;
                        }
                    }
                }
                tr.style.display = display;
            }
            if (i < trs.length) {
                requestAnimationFrame(processChunk);
            }
        }
        processChunk();
    }, 300);
};

// --- Custom Modal CMV 201 ---
window.currentCmv201PlanType = 'planificado';
window.currentCmv201Area = '';
window.cmv201MonthsAvailable = [];

window.openCmv201Modal = function() {
    const modal = document.getElementById('modalCmv201');
    if (!modal) return;
    if (window.openModal) window.openModal('modalCmv201');
    else modal.classList.add('show');
    
    document.getElementById('cmv201AreaDetailsContainer').style.display = 'none';
    document.getElementById('cmv201TableContainer').style.display = 'block';

    // Default to 'planificado' when opening
    window.loadCmv201Data('planificado');
};

window.loadCmv201Data = async function(planType) {
    window.currentCmv201PlanType = planType;
    // Update button styles
    const btnPlanificado = document.getElementById('btnPlanificado');
    const btnDesplanificado = document.getElementById('btnDesplanificado');
    
    if (planType === 'planificado') {
        btnPlanificado.className = 'btn btn-primary';
        btnDesplanificado.className = 'btn btn-secondary';
    } else {
        btnPlanificado.className = 'btn btn-secondary';
        btnDesplanificado.className = 'btn btn-primary';
    }

    const spinner = document.getElementById('cmv201Spinner');
    const container = document.getElementById('cmv201TableContainer');
    
    spinner.style.display = 'block';
    container.innerHTML = '';
    
    try {
        const year = new Date().getFullYear().toString();
        const res = await fetch(`/api/custom/cmv201_summary?plan_type=${planType}&year=${year}`);
        const data = await res.json();
        
        spinner.style.display = 'none';
        
        if (!data || data.length === 0) {
            container.innerHTML = '<div style="text-align:center; padding:20px; color:#94a3b8;">No se encontraron datos.</div>';
            return;
        }
        
        // Pivot the data to show areas as rows and months as columns
        const monthsSet = new Set();
        const areasData = {};
        
        data.forEach(row => {
            const area = row.area_negocio || 'Sin Área';
            const mes = row.mes || 'Sin Mes';
            monthsSet.add(mes);
            
            if (!areasData[area]) {
                areasData[area] = {};
            }
            areasData[area][mes] = row.cantidad;
        });
        
        const months = Array.from(monthsSet).sort();
        window.cmv201MonthsAvailable = months;
        
        let html = '<table class="mini-table" style="width: 100%; border-collapse: collapse;"><thead><tr>';
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: left;">Área de Negocio</th>`;
        months.forEach(m => {
            html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">${m}</th>`;
        });
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Total</th>`;
        html += '</tr></thead><tbody>';
        
        for (const [area, mesData] of Object.entries(areasData)) {
            html += `<tr style="transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'">`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; font-weight: bold;"><a href="javascript:void(0)" onclick="window.openCmv201AreaDetails('${area}')" style="color: var(--primary); text-decoration: none; border-bottom: 1px dashed var(--primary); padding-bottom: 2px;">${area}</a></td>`;
            
            let rowTotal = 0;
            months.forEach(m => {
                const val = mesData[m] || 0;
                rowTotal += val;
                html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">${val.toLocaleString('de-DE')}</td>`;
            });
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: var(--primario); text-align: right; font-weight: bold;">${rowTotal.toLocaleString('de-DE')}</td>`;
            html += '</tr>';
        }
        
        html += '</tbody></table>';
        container.innerHTML = html;
        
    } catch (e) {
        spinner.style.display = 'none';
        container.innerHTML = `<div style="color:var(--rojo); padding:20px; text-align:center;">Error al cargar datos: ${e.message}</div>`;
    }
};

window.openCmv201AreaDetails = function(area) {
    window.currentCmv201Area = area;
    document.getElementById('cmv201TableContainer').style.display = 'none';
    document.getElementById('cmv201AreaDetailsContainer').style.display = 'flex';
    document.getElementById('cmv201AreaTitle').innerText = `Detalles del Área: ${area}`;
    
    const select = document.getElementById('cmv201MonthSelect');
    select.innerHTML = '<option value="">Todos los meses</option>';
    window.cmv201MonthsAvailable.forEach(m => {
        const opt = document.createElement('option');
        opt.value = m;
        opt.innerText = m;
        select.appendChild(opt);
    });
    // Select the last month by default
    if (window.cmv201MonthsAvailable.length > 0) {
        select.value = window.cmv201MonthsAvailable[window.cmv201MonthsAvailable.length - 1];
    }
    
    window.loadCmv201AreaDetails();
};

window.backToCmv201Summary = function() {
    document.getElementById('cmv201AreaDetailsContainer').style.display = 'none';
    document.getElementById('cmv201TableContainer').style.display = 'block';
};

window.onCmv201MonthChange = function() {
    window.loadCmv201AreaDetails();
};

window.loadCmv201AreaDetails = async function() {
    const area = window.currentCmv201Area;
    const mes = document.getElementById('cmv201MonthSelect').value;
    const planType = window.currentCmv201PlanType;
    const year = new Date().getFullYear().toString();
    
    const spinner = document.getElementById('cmv201AreaDetailsSpinner');
    const container = document.getElementById('cmv201AreaDetailsTableContainer');
    
    spinner.style.display = 'block';
    container.innerHTML = '';
    
    try {
        let url = `/api/custom/cmv201_area_details?plan_type=${planType}&area=${encodeURIComponent(area)}&year=${year}`;
        if (mes) {
            url += `&mes=${encodeURIComponent(mes)}`;
        }
        
        const res = await fetch(url);
        const data = await res.json();
        spinner.style.display = 'none';
        
        if (!data || data.length === 0) {
            container.innerHTML = '<div style="text-align:center; padding:20px; color:#94a3b8;">No se encontraron materiales para esta selección.</div>';
            return;
        }
        
        let html = '<table class="mini-table" style="width: 100%; border-collapse: collapse;"><thead><tr>';
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: left;">Material</th>`;
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Veces Solicitado</th>`;
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Promedio Retiro</th>`;
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Frecuencia (Días)</th>`;
        html += '</tr></thead><tbody>';
        
        data.forEach(row => {
            html += `<tr style="transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'">`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9;"><span style="color:var(--primario);font-size:0.85rem;">[${row.material}]</span> ${row.texto_breve_material || ''}</td>`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">${row.frecuencia}</td>`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">${row.promedio_retiro}</td>`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">Cada ${row.dias_frecuencia}</td>`;
            html += '</tr>';
        });
        
        html += '</tbody></table>';
        container.innerHTML = html;
        
    } catch (e) {
        spinner.style.display = 'none';
        container.innerHTML = `<div style="color:var(--rojo); padding:20px; text-align:center;">Error al cargar datos: ${e.message}</div>`;
    }
};

// --- Custom Modal CMV 261 ---
window.currentCmv261PlanType = 'planificado';
window.currentCmv261Area = '';
window.cmv261MonthsAvailable = [];

window.openCmv261Modal = function() {
    const modal = document.getElementById('modalCmv261');
    if (!modal) return;
    if (window.openModal) window.openModal('modalCmv261');
    else modal.classList.add('show');
    
    document.getElementById('cmv261AreaDetailsContainer').style.display = 'none';
    document.getElementById('cmv261TableContainer').style.display = 'block';

    // Default to 'planificado' when opening
    window.loadCmv261Data('planificado');
};

window.loadCmv261Data = async function(planType) {
    window.currentCmv261PlanType = planType;
    const btnPlanificado = document.getElementById('btnCmv261Planificado');
    const btnDesplanificado = document.getElementById('btnCmv261Desplanificado');
    
    if (planType === 'planificado') {
        btnPlanificado.className = 'btn btn-primary';
        btnDesplanificado.className = 'btn btn-secondary';
    } else {
        btnPlanificado.className = 'btn btn-secondary';
        btnDesplanificado.className = 'btn btn-primary';
    }

    const spinner = document.getElementById('cmv261Spinner');
    const container = document.getElementById('cmv261TableContainer');
    
    spinner.style.display = 'block';
    container.innerHTML = '';
    
    try {
        const year = new Date().getFullYear().toString();
        const res = await fetch(`/api/custom/cmv261_summary?plan_type=${planType}&year=${year}`);
        const data = await res.json();
        
        spinner.style.display = 'none';
        
        if (!data || data.length === 0) {
            container.innerHTML = '<div style="text-align:center; padding:20px; color:#94a3b8;">No se encontraron datos.</div>';
            return;
        }
        
        const monthsSet = new Set();
        const areasData = {};
        
        data.forEach(row => {
            const area = row.area_negocio || 'Sin Área';
            const mes = row.mes || 'Sin Mes';
            monthsSet.add(mes);
            
            if (!areasData[area]) {
                areasData[area] = {};
            }
            areasData[area][mes] = row.cantidad;
        });
        
        const months = Array.from(monthsSet).sort();
        window.cmv261MonthsAvailable = months;
        
        let html = '<table class="mini-table" style="width: 100%; border-collapse: collapse;"><thead><tr>';
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: left;">Área de Negocio</th>`;
        months.forEach(m => {
            html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">${m}</th>`;
        });
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Total</th>`;
        html += '</tr></thead><tbody>';
        
        for (const [area, mesData] of Object.entries(areasData)) {
            html += `<tr style="transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'">`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; font-weight: bold;"><a href="javascript:void(0)" onclick="window.openCmv261AreaDetails('${area}')" style="color: var(--primary); text-decoration: none; border-bottom: 1px dashed var(--primary); padding-bottom: 2px;">${area}</a></td>`;
            
            let rowTotal = 0;
            months.forEach(m => {
                const val = mesData[m] || 0;
                rowTotal += val;
                html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">${val.toLocaleString('de-DE')}</td>`;
            });
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: var(--primario); text-align: right; font-weight: bold;">${rowTotal.toLocaleString('de-DE')}</td>`;
            html += '</tr>';
        }
        
        html += '</tbody></table>';
        container.innerHTML = html;
        
    } catch (e) {
        spinner.style.display = 'none';
        container.innerHTML = `<div style="color:var(--rojo); padding:20px; text-align:center;">Error al cargar datos: ${e.message}</div>`;
    }
};

window.openCmv261AreaDetails = function(area) {
    window.currentCmv261Area = area;
    document.getElementById('cmv261TableContainer').style.display = 'none';
    document.getElementById('cmv261AreaDetailsContainer').style.display = 'flex';
    document.getElementById('cmv261AreaTitle').innerText = `Detalles del Área: ${area}`;
    
    const select = document.getElementById('cmv261MonthSelect');
    select.innerHTML = '<option value="">Todos los meses</option>';
    window.cmv261MonthsAvailable.forEach(m => {
        const opt = document.createElement('option');
        opt.value = m;
        opt.innerText = m;
        select.appendChild(opt);
    });
    // Select the last month by default
    if (window.cmv261MonthsAvailable.length > 0) {
        select.value = window.cmv261MonthsAvailable[window.cmv261MonthsAvailable.length - 1];
    }
    
    window.loadCmv261AreaDetails();
};

window.backToCmv261Summary = function() {
    document.getElementById('cmv261AreaDetailsContainer').style.display = 'none';
    document.getElementById('cmv261TableContainer').style.display = 'block';
};

window.onCmv261MonthChange = function() {
    window.loadCmv261AreaDetails();
};

window.loadCmv261AreaDetails = async function() {
    const area = window.currentCmv261Area;
    const mes = document.getElementById('cmv261MonthSelect').value;
    const planType = window.currentCmv261PlanType;
    const year = new Date().getFullYear().toString();
    
    const spinner = document.getElementById('cmv261AreaDetailsSpinner');
    const container = document.getElementById('cmv261AreaDetailsTableContainer');
    
    spinner.style.display = 'block';
    container.innerHTML = '';
    
    try {
        let url = `/api/custom/cmv261_area_details?plan_type=${planType}&area=${encodeURIComponent(area)}&year=${year}`;
        if (mes) {
            url += `&mes=${encodeURIComponent(mes)}`;
        }
        
        const res = await fetch(url);
        const data = await res.json();
        spinner.style.display = 'none';
        
        if (!data || data.length === 0) {
            container.innerHTML = '<div style="text-align:center; padding:20px; color:#94a3b8;">No se encontraron materiales para esta selección.</div>';
            return;
        }
        
        let html = '<table class="mini-table" style="width: 100%; border-collapse: collapse;"><thead><tr>';
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: left;">Material</th>`;
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Veces Solicitado</th>`;
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Promedio Retiro</th>`;
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Frecuencia (Días)</th>`;
        html += '</tr></thead><tbody>';
        
        data.forEach(row => {
            html += `<tr style="transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'">`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9;"><span style="color:var(--primario);font-size:0.85rem;">[${row.material}]</span> ${row.texto_breve_material || ''}</td>`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">${row.frecuencia}</td>`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">${row.promedio_retiro}</td>`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">Cada ${row.dias_frecuencia}</td>`;
            html += '</tr>';
        });
        
        html += '</tbody></table>';
        container.innerHTML = html;
        
    } catch (e) {
        spinner.style.display = 'none';
        container.innerHTML = `<div style="color:var(--rojo); padding:20px; text-align:center;">Error al cargar datos: ${e.message}</div>`;
    }
};


/* --- deliveries.js --- */
(() => {
/**
 * MonitorWeb — Entregas Analytics Logic
 * Requiere: core_ui.js cargado previamente (provee window.CoreUI)
 */

// ── UI HELPERS — delegados a CoreUI ────────────────────────────────────
// openModal/closeModal ya están expuestos en window por core_ui.js.
// Usamos CoreUI directamente para renderMaterialModal dentro de este módulo.

const UI = {
    openModal: (id) => CoreUI.openModal(id),
    closeModal: (id) => CoreUI.closeModal(id),
    renderMaterialModal: (opts) => CoreUI.renderMaterialModal(opts)
};

const getData = (id) => CoreUI.getData(id);

// ── MODAL CONTROLLERS ───────────────────────────────────────────────────

let currentModalContext = { area: null, weekday: null };

window.toggleModalFilter = (type, isCurrentMonth) => {
    if (type === 'area' && currentModalContext.area) {
        openModalArea(currentModalContext.area, isCurrentMonth);
    } else if (type === 'weekday' && currentModalContext.weekday) {
        openModalWeekday(currentModalContext.weekday, isCurrentMonth);
    }
};

function openModalWeekday(dayName, isCurrentMonth = false) {
    currentModalContext.weekday = dayName;
    const dataSrc = isCurrentMonth ? 'data_weekday_mapping_cm' : 'data_weekday_mapping';
    const items = (getData(dataSrc) || {})[dayName] || [];
    
    const btnYr = document.getElementById('btnWeekdayToggleYear');
    const btnCm = document.getElementById('btnWeekdayToggleMonth');
    if (btnYr && btnCm) {
        if (isCurrentMonth) { btnCm.classList.add('active'); btnYr.classList.remove('active'); }
        else { btnYr.classList.add('active'); btnCm.classList.remove('active'); }
    }

    UI.renderMaterialModal({
        modalId: 'modalWeekday',
        titleId: 'modalWeekdayTitle',
        listId: 'modalWeekdayList',
        title: `Día: ${dayName} ${isCurrentMonth ? '(Mes)' : '(Año)'}`,
        items: items,
        colorVar: '--naranja',
        bgColor: 'rgba(234,118,0,0.15)'
    });
}

function openModalUbicacion(name) {
    const items = (getData('data_ubic_mapping') || {})[name] || [];
    UI.renderMaterialModal({
        modalId: 'modalUbicacion',
        titleId: 'modalUbicacionTitle',
        listId: 'modalUbicacionList',
        title: `Materiales retirados desde: ${name}`,
        items: items,
        colorVar: '--calipso'
    });
}

function openModalArea(name, isCurrentMonth = false) {
    currentModalContext.area = name;
    const dataSrc = isCurrentMonth ? 'data_area_mapping_cm' : 'data_area_mapping';
    const items = (getData(dataSrc) || {})[name] || [];
    
    const btnYr = document.getElementById('btnAreaToggleYear');
    const btnCm = document.getElementById('btnAreaToggleMonth');
    if (btnYr && btnCm) {
        if (isCurrentMonth) { btnCm.classList.add('active'); btnYr.classList.remove('active'); }
        else { btnYr.classList.add('active'); btnCm.classList.remove('active'); }
    }

    UI.renderMaterialModal({
        modalId: 'modalArea',
        titleId: 'modalAreaTitle',
        listId: 'modalAreaList',
        title: `Área: ${name} ${isCurrentMonth ? '(Mes)' : '(Año)'}`,
        items: items,
        colorVar: '--calipso'
    });
}

function openModalUser(name) {
    const items = (getData('data_user_mapping') || {})[name] || [];
    UI.renderMaterialModal({
        modalId: 'modalUser',
        titleId: 'modalUserTitle',
        listId: 'modalUserList',
        title: `Top Materiales solicitados por: ${name}`,
        items: items,
        colorVar: '--naranja',
        bgColor: 'rgba(234,118,0,0.15)'
    });
}

// Global for charts
window.openModalArea = openModalArea;
window.openModalUser = openModalUser;
window.openModalUbicacion = openModalUbicacion;

// ── VIEW SWITCHER ───────────────────────────────────────────────────────

window.switchVLView = (view) => {
    const operative = document.getElementById('vl-operative-charts');
    const historical = document.getElementById('vl-historical-charts');
    
    // Labels and KPIs
    // Switch containers
    if (view === 'historical') {
        operative.style.display = 'none';
        historical.style.display = 'block';
    } else {
        operative.style.display = 'block';
        historical.style.display = 'none';
    }

    
    window.dispatchEvent(new Event('resize'));
    
    // Forzar redibujado de gráficos para asegurar que tomen el tamaño del contenedor
    if (window.slaTrendChart) window.slaTrendChart.resize();
    if (window.slaAreaTrendChart) window.slaAreaTrendChart.resize();
    if (window.weeklyTrendChart) window.weeklyTrendChart.resize();
    if (window.monthlyTrendChart) window.monthlyTrendChart.resize();
    if (window.slaMonthlyTrendChart) window.slaMonthlyTrendChart.resize();
    if (window.slaMonthlyTrellisCharts) {
        window.slaMonthlyTrellisCharts.forEach(c => c.resize());
    }
};

// ── CHARTS INITIALIZATION ──────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Outfit', sans-serif";
    Chart.register(ChartDataLabels);

    const areaStats = getData('data_area_stats') || [];





    // 4. Intensidad de Entregas (Stacked Bar)
    const labelsVL = getData('data_chart_labels_vl') || [];
    const datasetsVL = getData('data_chart_datasets_vl') || [];
    const ctxIntensidad = document.getElementById('intensidadChart');

    if (ctxIntensidad && labelsVL.length > 0) {
        // Stacked Total Plugin
        const stackedTotalPlugin = {
            id: 'stackedTotal',
            afterDatasetsDraw: (chart) => {
                const { ctx, scales: { x, y } } = chart;
                const datasets = chart.data.datasets;
                if (!datasets.length) return;

                chart.data.labels.forEach((label, i) => {
                    let total = 0;
                    let lastVisibleY = y.bottom;
                    let foundVisible = false;

                    // Calcular total y encontrar el punto más alto
                    for (let j = 0; j < datasets.length; j++) {
                        const meta = chart.getDatasetMeta(j);
                        if (!meta.hidden && datasets[j].data[i]) {
                            total += datasets[j].data[i];
                            if (meta.data[i]) {
                                lastVisibleY = Math.min(lastVisibleY, meta.data[i].y);
                                foundVisible = true;
                            }
                        }
                    }

                    if (foundVisible && total > 0) {
                        ctx.save();
                        // Estilo premium para el total
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'bottom';
                        ctx.fillStyle = '#ffffff';
                        ctx.font = 'bold 11px Inter, sans-serif';
                        
                        // Sombra para contraste
                        ctx.shadowColor = 'rgba(0,0,0,0.9)';
                        ctx.shadowBlur = 3;
                        ctx.shadowOffsetY = 1;

                        const posX = chart.getDatasetMeta(0).data[i].x;
                        ctx.fillText(total, posX, lastVisibleY - 5);
                        ctx.restore();
                    }
                });
            }
        };

        window.intensidadChart = new Chart(ctxIntensidad.getContext('2d'), {
            type: 'bar',
            data: { labels: labelsVL, datasets: datasetsVL },
            plugins: [stackedTotalPlugin],
            options: {
                responsive: true, maintainAspectRatio: false,
                layout: { padding: { top: 25, bottom: 10 } },
                plugins: {
                    legend: { display: false }, // Too many areas, better use the filter
                    tooltip: { mode: 'index', intersect: false },
                    datalabels: { display: false }
                },
                scales: {
                    y: { stacked: true, beginAtZero: true, grace: '15%', ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                    x: { stacked: true, ticks: { color: '#94a3b8' }, grid: { display: false } }
                }
            }
        });
    }

    // 5. Monthly Trend Chart (Historical) - Migrado a SaaS Widget (dashboard.js)

    // 6. Weekly Trend Chart (Historical) - Migrado a SaaS Widget (dashboard.js)

    // 9. SLA Trend Chart (Historical) - Migrado a SaaS Widget (dashboard.js)

    // 10. SLA Trend by Area (Trellis Chart / Small Multiples) - Migrado a SaaS Widget (dashboard.js)

    // 11. Monthly SLA Trend Chart (ANNUAL VIEW) - Migrado a SaaS Widget (dashboard.js)

    // 12. Monthly SLA Trend by Area (ANNUAL TRELLIS) - Migrado a SaaS Widget (dashboard.js)

    // Inicializar vista por defecto
    const viewSelect = document.getElementById('vl-view-select');
    if (viewSelect) {
        window.switchVLView(viewSelect.value);
    }
});

// ── HELPERS FOR INTENSIDAD CHART ───────────────────────────────────────

window.toggleMulti = (id) => {
    const el = document.getElementById(id);
    if (el) el.style.display = el.style.display === 'none' ? 'block' : 'none';
};


function updateDeliveriesAnalytics() {
    const selected = Array.from(document.querySelectorAll('.chart-area-cb:checked')).map(cb => cb.value);
    
    // 1. Recalculate KPIs
    const areaStats = getData('data_area_stats') || [];
    const globalDays = getData('data_total_dias_activos') || 0;
    
    let totalVol = 0;
    let totalOntime = 0;
    let totalLate = 0;
    let bestArea = "N/A";
    let maxVol = -1;

    areaStats.forEach(s => {
        if (selected.includes(s.area)) {
            totalVol += (s.total_entregas || 0);
            totalOntime += (s.ontime || 0);
            totalLate += (s.late || 0);
            if (s.total_entregas > maxVol) {
                maxVol = s.total_entregas;
                bestArea = s.area;
            }
        }
    });

    const avg = globalDays > 0 ? (totalVol / globalDays).toFixed(1) : 0;
    const eff = totalVol > 0 ? ((totalOntime / totalVol) * 100).toFixed(1) : 0;

    // Update DOM KPIs
    const elTotal = document.getElementById('vl-kpi-total');
    const elAvg = document.getElementById('vl-kpi-avg');
    const elBest = document.getElementById('vl-kpi-best');
    const elEff = document.getElementById('vl-kpi-eff');
    const elOntime = document.getElementById('vl-kpi-ontime');
    const elLate = document.getElementById('vl-kpi-late');

    if (elTotal) elTotal.innerText = totalVol.toLocaleString('de-DE');
    if (elAvg) elAvg.innerText = avg + " / día";
    if (elBest) elBest.innerText = bestArea;
    if (elEff) elEff.innerText = eff + "%";
    if (elOntime) elOntime.innerText = totalOntime.toLocaleString('de-DE');
    if (elLate) elLate.innerText = totalLate.toLocaleString('de-DE');

    // 3. Filter Lists
    document.querySelectorAll('.rank-list li[data-area]').forEach(li => {
        const area = li.getAttribute('data-area');
        const show = selected.includes(area) || area === 'MIXTO';
        li.style.display = show ? '' : 'none';
    });

    document.querySelectorAll('.materials-grid .area-card[data-area]').forEach(card => {
        const area = card.getAttribute('data-area');
        card.style.display = selected.includes(area) ? '' : 'none';
    });

    // 3. Filter Trellis Charts (Small Multiples)
    document.querySelectorAll('#sla-trellis-container > div[data-area]').forEach(wrapper => {
        const area = wrapper.getAttribute('data-area');
        wrapper.style.display = selected.includes(area) ? '' : 'none';
    });
    
    document.querySelectorAll('#sla-monthly-trellis-container > div[data-area]').forEach(wrapper => {
        const area = wrapper.getAttribute('data-area');
        wrapper.style.display = selected.includes(area) ? '' : 'none';
    });

    // 4. Update Global Trend Charts (Ahora son SaaS Widgets manejados por dashboard.js)
    if (typeof window.initSaaSWidgets === 'function') {
        const areaAll = document.getElementById('chartAreaFilterAll')?.checked;
        const areaValues = areaAll ? '' : selected.join(',');
        
        // Conservar los filtros globales actuales de la UI
        const dateAll = document.getElementById('dateFilterAll')?.checked;
        const dateValues = dateAll ? '' : (typeof getCheckboxValues === 'function' ? getCheckboxValues('date-cb') : '');
        const centroValue = document.querySelector('input[name="centro-filter"]:checked')?.value || '';
        const otsValue = document.querySelector('input[name="ot-filter"]:checked')?.value || '';

        try {
            window.initSaaSWidgets({
                date: dateValues,
                area: areaValues,
                centro: centroValue,
                has_ots_filter: otsValue
            });
        } catch (e) {
            console.error("Legacy widget error:", e);
        }
    }
}



window.toggleChartSelectAll = (isChecked) => {
    const boxes = document.querySelectorAll('.chart-area-cb');
    const selAll = document.getElementById('chartAreaFilterAll');
    
    if (!isChecked) {
        // If user tries to uncheck "All", we force it back to "All" (No empty selection)
        boxes.forEach(cb => cb.checked = true);
        if (selAll) selAll.checked = true;
    } else {
        boxes.forEach(cb => cb.checked = true);
    }
    window.updateDeliveriesAnalytics();
    if (window.initSaaSWidgetsV2) window.initSaaSWidgetsV2();
};

window.handleSmartCheckbox = (cb) => {
    const boxes = document.querySelectorAll('.chart-area-cb');
    const selAll = document.getElementById('chartAreaFilterAll');

    if (selAll && selAll.checked) {
        // Rule: If "All" was checked and we click one, uncheck "All" and keep only this one
        boxes.forEach(b => b.checked = false);
        cb.checked = true;
        selAll.checked = false;
    } else {
        const anyChecked = Array.from(boxes).some(b => b.checked);
        if (!anyChecked) {
            // Rule: Cannot be empty, reset to "All"
            boxes.forEach(b => b.checked = true);
            if (selAll) selAll.checked = true;
        } else {
            const allCheckedNow = Array.from(boxes).every(b => b.checked);
            if (selAll) selAll.checked = allCheckedNow;
        }
    }

    window.updateDeliveriesAnalytics();
    if (window.initSaaSWidgetsV2) window.initSaaSWidgetsV2();
};


// Close multi-select if clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.multiselect')) {
        const boxes = document.getElementById('chartAreaCheckboxes');
        if (boxes) boxes.style.display = 'none';
    }
});

// Expose update function to window for any other use
window.updateDeliveriesAnalytics = updateDeliveriesAnalytics;

})();

/* --- consumos.js --- */
document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('material-grid');
    if(grid) {
        // Obsoleto: Antes se generaban 25 celdas. Ahora se usa un textarea.
    }

    // Cerrar modal de tendencia con Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const modal = document.getElementById('modal-tendencia-material');
            if (modal && modal.classList.contains('is-open')) {
                cerrarTendenciaMaterial();
            }
        }
    });
});

function handlePaste(e) {
    // Obsoleto: El textarea maneja el pegado de múltiples líneas nativamente.
}

function limpiarGrilla() {
    const textarea = document.getElementById('material-grid-textarea');
    if(textarea) textarea.value = '';
    const container = document.getElementById('materiales-results-container');
    if(container) container.style.display = 'none';
}

function formatearDinero(valor) {
    if(valor == null || isNaN(valor)) return '$0';
    return '$' + parseFloat(valor).toLocaleString('de-DE');
}

function formatearNumero(valor) {
    if(valor == null || isNaN(valor)) return '0';
    return parseFloat(valor).toLocaleString('de-DE');
}

function filterTable(tableId) {
    const table = document.getElementById(tableId);
    if(!table) return;
    
    const inputs = table.querySelectorAll('thead .filter-row input');
    const tbody = table.querySelector('tbody');
    if(!tbody) return;
    
    const rows = tbody.querySelectorAll('tr');
    
    rows.forEach(row => {
        // Ignorar fila de "No hay datos"
        if(row.cells.length === 1 && row.cells[0].colSpan > 1) return;
        
        let show = true;
        inputs.forEach((input, index) => {
            const filterVal = input.value.toLowerCase().trim();
            if(filterVal) {
                const cell = row.cells[index];
                if(cell) {
                    const cellText = cell.textContent.toLowerCase();
                    if(!cellText.includes(filterVal)) {
                        show = false;
                    }
                }
            }
        });
        row.style.display = show ? '' : 'none';
    });
}

// Renderizador Vanilla JS para las tablas
function renderVanillaTable(tbodyId, data, columns, onRowClick = null) {
    const tbody = document.querySelector(`#${tbodyId} tbody`);
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="${columns.length}" style="text-align: center; color: var(--text-muted); padding: 20px;">No hay datos para mostrar</td></tr>`;
        return;
    }

    data.forEach(row => {
        const tr = document.createElement('tr');
        if (onRowClick) {
            tr.style.cursor = 'pointer';
            tr.title = 'Click para ver tendencia mensual';
            tr.addEventListener('click', () => onRowClick(row));
            tr.addEventListener('mouseenter', () => tr.style.background = 'rgba(99,102,241,0.08)');
            tr.addEventListener('mouseleave', () => tr.style.background = '');
        }
        columns.forEach(col => {
            const td = document.createElement('td');
            if (col.className) td.className = col.className;
            if (col.style) td.style.cssText = col.style;
            
            let val = row[col.data];
            if (col.render) {
                val = col.render(val, row);
            }
            td.innerHTML = val || '';
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
}

async function buscarPorCeCo() {
    let ceco = document.getElementById('ceco-search-input').value.trim();
    if(!ceco) {
        alert("Por favor ingresa un Centro de Costo.");
        return;
    }
    
    ceco = ceco.toUpperCase();
    document.getElementById('ceco-search-input').value = ceco; // Reflejar en la UI

    try {
        const res = await fetch(`/api/consumos/ceco/${encodeURIComponent(ceco)}`);
        if(!res.ok) {
            let errDetail = `HTTP ${res.status}`;
            try {
                const errData = await res.json();
                if(errData.detail) errDetail = errData.detail;
            } catch(e) {}
            throw new Error(`Error en la consulta: ${errDetail}`);
        }
        const data = await res.json();

        document.getElementById('ceco-results-container').style.display = 'block';

        const sumMes = data.mes_actual.reduce((acc, row) => acc + (row.costo_total || 0), 0);
        const sumHist = data.historico.reduce((acc, row) => acc + (row.costo_total || 0), 0);

        document.getElementById('th-costo-mes').innerHTML = `Costo Total (${formatearDinero(sumMes)})`;
        document.getElementById('th-costo-hist').innerHTML = `Costo Total (${formatearDinero(sumHist)})`;

        const cecoCols = [
            { data: 'material' },
            { data: 'descripcion' },
            { data: 'umb' },
            { data: 'cantidad_total', render: formatearNumero, style: "text-align: right;" },
            { 
                data: 'precio_unitario', 
                render: formatearDinero,
                style: "text-align: right;" 
            },
            { data: 'costo_total', render: formatearDinero, style: "text-align: right;" }
        ];

        renderVanillaTable('table-ceco-mes', data.mes_actual, cecoCols, (row) => abrirTendenciaMaterial(row.material, '', row.descripcion, ceco));
        renderVanillaTable('table-ceco-hist', data.historico, cecoCols, (row) => abrirTendenciaMaterial(row.material, '', row.descripcion, ceco));

    } catch (err) {
        console.error(err);
        alert(`Ocurrió un error al buscar el CeCo (${ceco}). Detalle: ${err.message}`);
    }
}

async function buscarPorMateriales() {
    const textarea = document.getElementById('material-grid-textarea');
    if(!textarea) return;
    
    const text = textarea.value;
    const materiales = text.split(/[\r\n\t,]+/).map(v => v.trim().toUpperCase()).filter(v => v);

    if(materiales.length === 0) {
        alert("Por favor ingresa al menos un material en las celdas.");
        return;
    }

    try {
        const res = await fetch('/api/consumos/materiales', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ materiales: materiales })
        });
        
        if(!res.ok) {
            let errDetail = `HTTP ${res.status}`;
            try {
                const errData = await res.json();
                if(errData.detail) errDetail = errData.detail;
            } catch(e) {}
            throw new Error(`Error en la consulta: ${errDetail}`);
        }
        const json = await res.json();

        document.getElementById('materiales-results-container').style.display = 'block';

        const sumMat = json.data.reduce((acc, row) => acc + (row.costo_total || 0), 0);
        const sumMatMes = json.data.reduce((acc, row) => acc + (row.costo_mes || 0), 0);
        document.getElementById('th-costo-mat').innerHTML = `Costo Anual (${formatearDinero(sumMat)})`;
        document.getElementById('th-costo-mes-mat').innerHTML = `Costo Este Mes (${formatearDinero(sumMatMes)})`;

        const matCols = [
            { data: 'material' },
            { data: 'descripcion' },
            { data: 'umb' },
            { data: 'area_negocio' },
            { data: 'cantidad_mes', render: formatearNumero, style: "text-align: right;" },
            { data: 'costo_mes', render: formatearDinero, style: "text-align: right;" },
            { data: 'cantidad_total', render: formatearNumero, style: "text-align: right;" },
            { 
                data: 'precio_unitario', 
                render: formatearDinero,
                style: "text-align: right;" 
            },
            { data: 'costo_total', render: formatearDinero, style: "text-align: right;" }
        ];

        renderVanillaTable(
            'table-materiales',
            json.data,
            matCols,
            (row) => abrirTendenciaMaterial(row.material, row.area_negocio, row.descripcion)
        );

    } catch (err) {
        console.error(err);
        alert(`Ocurrió un error al analizar los materiales. Detalle: ${err.message}`);
    }
}

// ─── Tendencia Mensual por Material ───────────────────────────────────────────
let _tendenciaChart = null;

async function abrirTendenciaMaterial(material, areaNegocio, descripcion, ceco = '') {
    const modal = document.getElementById('modal-tendencia-material');
    modal.classList.add('is-open');
    document.body.style.overflow = 'hidden'; // Evitar scroll de fondo

    document.getElementById('tendencia-modal-title').textContent = `📈 ${material}`;
    let subtitle = `${descripcion || material}`;
    if (ceco) {
        subtitle += ` — CeCo: ${ceco}`;
    } else {
        subtitle += ` — Área: ${areaNegocio || 'Todas'}`;
    }
    document.getElementById('tendencia-modal-subtitle').textContent = subtitle;
    document.getElementById('tendencia-precio-unitario').textContent = 'Cargando...';
    document.getElementById('tendencia-total-anual').textContent = 'Cargando...';
    document.getElementById('tendencia-total-anual-label').textContent = 'Total Anual';
    document.getElementById('tendencia-avg-cant').textContent = '';
    document.getElementById('tendencia-min-cant').textContent = '';
    document.getElementById('tendencia-max-cant').textContent = '';

    try {
        const res = await fetch('/api/consumos/materiales/tendencia', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ material, area_negocio: areaNegocio || '', ceco: ceco || '' })
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        // KPIs
        const currentYearStr = data.current_year;
        
        let totalAnual = 0;
        data.labels.forEach((label, idx) => {
            if (label.endsWith(currentYearStr)) {
                totalAnual += data.cantidad[idx];
            }
        });

        const totalCant = data.cantidad.reduce((a, b) => a + b, 0);
        const avgCant = data.cantidad.length ? (totalCant / data.cantidad.length) : 0;
        const maxCant = data.cantidad.length ? Math.max(...data.cantidad) : 0;
        const minCant = data.cantidad.length ? Math.min(...data.cantidad) : 0;

        document.getElementById('tendencia-precio-unitario').textContent = formatearDinero(data.precio_unitario);
        document.getElementById('tendencia-total-anual-label').textContent = `Total Anual (${currentYearStr})`;
        document.getElementById('tendencia-total-anual').textContent = totalAnual.toLocaleString('de-DE');
        document.getElementById('tendencia-avg-cant').textContent = avgCant.toFixed(1).replace('.', ',');
        document.getElementById('tendencia-min-cant').textContent = minCant.toLocaleString('de-DE');
        document.getElementById('tendencia-max-cant').textContent = maxCant.toLocaleString('de-DE');

        // Destruir chart anterior si existe
        if (_tendenciaChart) { _tendenciaChart.destroy(); _tendenciaChart = null; }

        const ctx = document.getElementById('chart-tendencia-material').getContext('2d');
        _tendenciaChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Cantidad Retirada',
                    data: data.cantidad,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99,102,241,0.12)',
                    borderWidth: 2.5,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointBackgroundColor: '#6366f1',
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: ctx => `Cantidad: ${ctx.parsed.y.toLocaleString('de-DE')}`
                        }
                    }
                },
                scales: {
                    x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                    y: {
                        grid: { color: 'rgba(255,255,255,0.05)' },
                        ticks: { color: '#94a3b8', callback: v => v.toLocaleString('de-DE') },
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (err) {
        console.error(err);
        document.getElementById('tendencia-total-cant').textContent = 'Error al cargar';
    }
}

function cerrarTendenciaMaterial() {
    const modal = document.getElementById('modal-tendencia-material');
    modal.classList.remove('is-open');
    document.body.style.overflow = '';
    if (_tendenciaChart) { _tendenciaChart.destroy(); _tendenciaChart = null; }
}


/* --- transporte.js --- */
let chartInstance = null;
let allTransporteData = [];
let currentChartGroup = 'mensual';

document.addEventListener("DOMContentLoaded", () => {
    loadData();
});

async function loadData() {
    try {
        const response = await fetch("/api/transporte/data");
        if (!response.ok) throw new Error("Error fetching data");
        const res = await response.json();
        
        allTransporteData = res.data;
        renderChart();
        renderTable(allTransporteData);
        loadPendingData();
    } catch (e) {
        console.error("Error cargando datos de transporte:", e);
    }
}

function getMonday(dateStr) {
    const d = new Date(dateStr);
    const day = d.getDay();
    const diff = d.getDate() - day + (day === 0 ? -6 : 1); 
    d.setDate(diff);
    return d.toISOString().split('T')[0];
}

function updateTransporteChartGroup(group) {
    currentChartGroup = group;
    renderChart();
}

async function loadPendingData() {
    const tbody = document.querySelector('#transportePendingTable tbody');
    const countSpan = document.getElementById('transportePendingCount');
    
    try {
        const response = await fetch('/api/transporte/pending');
        if (!response.ok) throw new Error('Error fetch pending');
        
        const json = await response.json();
        const data = json.data || [];
        
        tbody.innerHTML = '';
        countSpan.textContent = `${data.length} Pendientes`;
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 1.5rem; color: #10b981;">¡Todo al día! No hay entregas del año actual sin ingresar. 🎉</td></tr>';
            return;
        }

        // Agrupar por mes y luego por fecha
        const groupedByMonth = {};
        data.forEach(item => {
            const fecha = item.fecha || 'Sin Fecha';
            const mes = fecha.length >= 7 ? fecha.substring(0, 7) : 'Sin Mes';
            
            if (!groupedByMonth[mes]) groupedByMonth[mes] = { total: 0, fechas: {} };
            if (!groupedByMonth[mes].fechas[fecha]) groupedByMonth[mes].fechas[fecha] = [];
            
            groupedByMonth[mes].fechas[fecha].push(item);
            groupedByMonth[mes].total++;
        });

        const sortedMonths = Object.keys(groupedByMonth).sort((a, b) => b.localeCompare(a));
        
        const monthNames = {
            '01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril',
            '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto',
            '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'
        };

        sortedMonths.forEach((mes, mIndex) => {
            const mesData = groupedByMonth[mes];
            
            let mesNombre = mes;
            if (mes.length === 7) {
                const [y, m] = mes.split('-');
                mesNombre = `${monthNames[m] || m} ${y}`;
            }

            // Month Header
            const monthHeader = document.createElement('tr');
            monthHeader.style.cursor = 'pointer';
            monthHeader.style.background = 'rgba(220, 38, 38, 0.15)';
            monthHeader.style.borderBottom = '1px solid rgba(239, 68, 68, 0.3)';
            
            monthHeader.innerHTML = `
                <td colspan="5" style="padding: 12px; font-weight: bold; color: #f87171; font-size: 1.05rem;">
                    <span style="display: inline-block; width: 20px; transition: transform 0.2s;" id="icon-month-${mIndex}">▶</span>
                    📅 ${mesNombre} <span style="font-size: 0.85rem; color: #fca5a5; margin-left: 10px; background: rgba(220,38,38,0.3); padding: 2px 8px; border-radius: 12px;">${mesData.total} ots pendientes</span>
                </td>
            `;
            tbody.appendChild(monthHeader);

            const sortedFechas = Object.keys(mesData.fechas).sort((a, b) => b.localeCompare(a));
            const allChildRows = [];

            sortedFechas.forEach((fecha, fIndex) => {
                const items = mesData.fechas[fecha];
                
                // Date Header
                const dateHeader = document.createElement('tr');
                dateHeader.style.cursor = 'pointer';
                dateHeader.style.background = 'rgba(239, 68, 68, 0.05)';
                dateHeader.style.borderBottom = '1px solid rgba(239, 68, 68, 0.1)';
                dateHeader.style.display = 'none'; 
                dateHeader.dataset.isDateHeader = "true";
                
                dateHeader.innerHTML = `
                    <td colspan="5" style="padding: 10px 12px 10px 30px; font-weight: bold; color: #fca5a5;">
                        <span style="display: inline-block; width: 20px; transition: transform 0.2s;" id="icon-date-${mIndex}-${fIndex}">▶</span>
                        📆 ${fecha} <span style="font-size: 0.8rem; color: #f87171; margin-left: 10px;">(${items.length} pendientes)</span>
                    </td>
                `;
                tbody.appendChild(dateHeader);
                allChildRows.push(dateHeader);

                // Items
                const itemRows = [];
                items.forEach(item => {
                    const tr = document.createElement('tr');
                    tr.style.display = 'none'; 
                    tr.style.background = 'rgba(0,0,0,0.2)';
                    tr.innerHTML = `
                        <td style="font-weight: 600; color: #f87171; padding-left: 55px;">${item.ot}</td>
                        <td>${item.gd}</td>
                        <td>${item.oc}</td>
                        <td style="text-align: center;">${item.bultos}</td>
                        <td style="text-align: right; color: var(--text-muted);">${item.fecha}</td>
                    `;
                    tbody.appendChild(tr);
                    itemRows.push(tr);
                    allChildRows.push(tr); 
                });

                // Date click
                dateHeader.onclick = (e) => {
                    e.stopPropagation();
                    const icon = document.getElementById(`icon-date-${mIndex}-${fIndex}`);
                    const isHidden = itemRows[0].style.display === 'none';
                    icon.style.transform = isHidden ? 'rotate(90deg)' : 'rotate(0deg)';
                    itemRows.forEach(row => {
                        row.style.display = isHidden ? 'table-row' : 'none';
                    });
                };
            });

            // Month click
            monthHeader.onclick = () => {
                const icon = document.getElementById(`icon-month-${mIndex}`);
                const firstDateHeader = allChildRows.find(r => r.dataset.isDateHeader === "true");
                if (!firstDateHeader) return;
                
                const isHidden = firstDateHeader.style.display === 'none';
                icon.style.transform = isHidden ? 'rotate(90deg)' : 'rotate(0deg)';
                
                if (isHidden) {
                    allChildRows.forEach(row => {
                        if (row.dataset.isDateHeader === "true") {
                            row.style.display = 'table-row';
                        }
                    });
                } else {
                    allChildRows.forEach(row => {
                        row.style.display = 'none';
                        if (row.dataset.isDateHeader === "true") {
                            const dateIcon = row.querySelector('span');
                            if(dateIcon) dateIcon.style.transform = 'rotate(0deg)';
                        }
                    });
                }
            };
        });

    } catch (e) {
        console.error("Error al cargar pendientes:", e);
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 1.5rem; color: #ef4444;">Error al cargar datos pendientes.</td></tr>';
        countSpan.textContent = 'Error';
    }
}

function renderChart() {
    const ctx = document.getElementById('transporteChart').getContext('2d');
    
    if (chartInstance) {
        chartInstance.destroy();
    }

    // Filtrar solo 2025 en adelante para el gráfico
    const chartData = allTransporteData.filter(d => d.fecha >= '2025-01-01');

    // Agrupar los datos
    const groupedData = {};
    chartData.forEach(d => {
        let key = '';
        if (currentChartGroup === 'mensual') {
            key = d.fecha.substring(0, 7); // YYYY-MM
        } else {
            key = getMonday(d.fecha); // YYYY-MM-DD del lunes de la semana
        }
        
        if (!groupedData[key]) {
            groupedData[key] = { entregas: 0, bultos: 0 };
        }
        groupedData[key].entregas += d.total_entregas;
        groupedData[key].bultos += (d.total_bultos || 0);
    });

    // Ordenar las llaves
    const sortedKeys = Object.keys(groupedData).sort();
    
    // Formatear etiquetas
    const labels = sortedKeys.map(k => {
        if (currentChartGroup === 'mensual') {
            const [y, m] = k.split('-');
            const date = new Date(Date.UTC(y, m - 1, 1));
            return date.toLocaleDateString('es-ES', { month: 'short', year: 'numeric' });
        } else {
            return `Semana del ${k}`;
        }
    });
    
    const counts = sortedKeys.map(k => groupedData[k].entregas);
    const bultosCounts = sortedKeys.map(k => groupedData[k].bultos);

    // Registrar el plugin de datalabels globalmente o en la instancia
    Chart.register(ChartDataLabels);

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: currentChartGroup === 'mensual' ? 'Entregas por Mes' : 'Entregas por Semana',
                    data: counts,
                    borderColor: '#5DBAA9',
                    backgroundColor: 'rgba(93, 186, 169, 0.2)',
                    borderWidth: 2,
                    pointBackgroundColor: '#5DBAA9',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#5DBAA9',
                    fill: true,
                    tension: 0.4,
                    yAxisID: 'y'
                },
                {
                    label: currentChartGroup === 'mensual' ? 'Bultos por Mes' : 'Bultos por Semana',
                    data: bultosCounts,
                    borderColor: '#EA7600',
                    backgroundColor: 'rgba(234, 118, 0, 0.1)',
                    borderWidth: 2,
                    pointBackgroundColor: '#EA7600',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#EA7600',
                    fill: true,
                    tension: 0.4,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#e2e8f0' }
                },
                datalabels: {
                    color: '#ffffff',
                    backgroundColor: 'rgba(0,0,0,0.6)',
                    borderRadius: 4,
                    font: {
                        weight: 'bold',
                        size: 11
                    },
                    padding: 4,
                    align: 'top',
                    offset: 5,
                    formatter: Math.round
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: '#5DBAA9' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    beginAtZero: true,
                    grid: { drawOnChartArea: false },
                    ticks: { color: '#EA7600' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });
}

function renderTable(data) {
    const tbody = document.querySelector("#transporteTable tbody");
    tbody.innerHTML = "";

    if (data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color: #94a3b8;">No hay datos de transporte. Ejecuta la sincronización global desde el panel de control.</td></tr>`;
        return;
    }

    // Mostrar solo los últimos 25 para la tabla como se solicitó
    const latestData = [...data].reverse().slice(0, 25);

    latestData.forEach(row => {
        const tr = document.createElement("tr");
        
        let pdfBtn = `<span style="color: #94a3b8;">No disponible</span>`;
        if (row.has_pdf) {
            pdfBtn = `<button onclick="openPdfViewer('/api/transporte/pdf/${row.pdf_filename}')" class="btn btn-small" style="background: rgba(93, 186, 169, 0.1); color: #5DBAA9; border: none; padding: 4px 12px; border-radius: 4px; font-weight: 600; cursor: pointer;">Ver PDF</button>`;
        }

        tr.innerHTML = `
            <td><strong>${row.fecha}</strong></td>
            <td style="text-align: center;">${row.total_entregas}</td>
            <td style="text-align: center; color: var(--naranja); font-weight: bold;">${row.total_bultos || 0}</td>
            <td style="text-align: right;">${pdfBtn}</td>
        `;
        tbody.appendChild(tr);
    });
}

function openPdfViewer(url) {
    const modal = document.getElementById('modalPdfViewer');
    const iframe = document.getElementById('pdfIframe');
    if (modal && iframe) {
        iframe.src = url;
        modal.classList.add('active');
    }
}

function closePdfViewer() {
    const modal = document.getElementById('modalPdfViewer');
    const iframe = document.getElementById('pdfIframe');
    if (modal && iframe) {
        modal.classList.remove('active');
        iframe.src = ""; // Stop loading or viewing the PDF when closed
    }
}

let transporteSearchTimeout = null;

async function searchTransporte() {
    const input = document.getElementById('transporteSearchInput').value.trim();
    const loading = document.getElementById('transporteSearchLoading');
    const table = document.getElementById('transporteSearchTable');
    const tbody = table.querySelector('tbody');
    const noResults = document.getElementById('transporteSearchNoResults');

    if (input.length < 3) {
        table.style.display = 'none';
        noResults.style.display = 'none';
        return;
    }

    if (transporteSearchTimeout) {
        clearTimeout(transporteSearchTimeout);
    }

    loading.style.display = 'inline-block';

    transporteSearchTimeout = setTimeout(async () => {
        try {
            const res = await fetch(`/api/transporte/search?q=${encodeURIComponent(input)}`);
            const json = await res.json();

            tbody.innerHTML = '';

            if (!res.ok || !json.data || json.data.length === 0) {
                table.style.display = 'none';
                noResults.style.display = 'block';
            } else {
                noResults.style.display = 'none';
                table.style.display = 'table';

                json.data.forEach(item => {
                    const tr = document.createElement('tr');
                    tr.className = 'row';
                    tr.innerHTML = `
                        <td>${item.fecha}</td>
                        <td style="font-weight: 600; color: var(--calipso);">${item.ot}</td>
                        <td>${item.gd}</td>
                        <td>${item.oc}</td>
                        <td>${item.proveedor}</td>
                        <td style="text-align: center; color: var(--naranja); font-weight: bold;">${item.bultos}</td>
                    `;
                    tbody.appendChild(tr);
                });
            }
        } catch (e) {
            console.error("Error searching transporte", e);
        } finally {
            loading.style.display = 'none';
        }
    }, 400); // 400ms debounce
}


/* --- tasks.js --- */
(() => {
    /**
     * MonitorWeb — Warehouse Tasks (OTs) Analytics Logic
     */

    const log = (msg, data = null) => {
        console.log(`[Tasks-JS] ${msg}`, data || '');
    };

    const getData = (id) => {
        const el = document.getElementById(id);
        if (!el) return null;
        try {
            return JSON.parse(el.textContent);
        } catch (e) {
            log(`Error parsing ${id}`, e);
            return null;
        }
    };

    document.addEventListener('DOMContentLoaded', () => {
        log('Initializing OT charts with high-contrast text and premium styling...');

        // 1. Trend Chart (Line)
        try {
            const labels = getData('data_ots_trend_labels') || [];
            const createdData = getData('data_ots_trend_created') || [];
            const confirmedData = getData('data_ots_trend_confirmed') || [];
            const ctx = document.getElementById('otsTrendChart');
            if (ctx && labels.length > 0) {
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Creadas',
                                data: createdData,
                                borderColor: '#5DBAA9',
                                backgroundColor: 'rgba(93, 186, 169, 0.1)',
                                borderWidth: 3,
                                tension: 0.3,
                                fill: true
                            },
                            {
                                label: 'Confirmadas',
                                data: confirmedData,
                                borderColor: '#EA7600',
                                backgroundColor: 'rgba(234, 118, 0, 0.1)',
                                borderWidth: 3,
                                tension: 0.3,
                                fill: true
                            }
                        ]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                display: true,
                                labels: {
                                    color: '#f8fafc',
                                    font: { family: 'Outfit', size: 12, weight: '600' }
                                }
                            },
                            tooltip: {
                                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                                titleColor: '#f8fafc',
                                bodyColor: '#cbd5e1',
                                borderColor: 'rgba(255, 255, 255, 0.1)',
                                borderWidth: 1,
                                padding: 10,
                                bodyFont: { family: 'Outfit', size: 12 },
                                titleFont: { family: 'Outfit', size: 12, weight: 'bold' }
                            },
                            datalabels: {
                                display: true,
                                align: 'top',
                                anchor: 'end',
                                color: '#ffffff',
                                offset: 4,
                                font: {
                                    family: 'Outfit',
                                    weight: 'bold',
                                    size: 11
                                },
                                formatter: (val) => val
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: { color: 'rgba(255,255,255,0.08)' },
                                ticks: {
                                    color: '#cbd5e1',
                                    font: { family: 'Outfit', size: 11 }
                                }
                            },
                            x: {
                                grid: { display: false },
                                ticks: {
                                    color: '#cbd5e1',
                                    font: { family: 'Outfit', size: 11 }
                                }
                            }
                        }
                    },
                    plugins: [ChartDataLabels]
                });
            }
        } catch (e) { log('Error in Trend Chart', e); }


        // 3. User Chart (Bar)
        try {
            const labels = getData('data_ots_user_labels') || [];
            const createdData = getData('data_ots_user_created') || [];
            const confirmedData = getData('data_ots_user_confirmed') || [];
            const ctx = document.getElementById('otsUserChart');
            if (ctx && labels.length > 0) {
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Creadas',
                                data: createdData,
                                backgroundColor: 'rgba(93, 186, 169, 0.7)',
                                borderRadius: 6
                            },
                            {
                                label: 'Confirmadas',
                                data: confirmedData,
                                backgroundColor: 'rgba(234, 118, 0, 0.7)',
                                borderRadius: 6
                            }
                        ]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        indexAxis: 'y',
                        plugins: {
                            legend: {
                                display: true,
                                labels: {
                                    color: '#f8fafc',
                                    font: { family: 'Outfit', size: 12, weight: '600' }
                                }
                            },
                            tooltip: {
                                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                                titleColor: '#f8fafc',
                                bodyColor: '#cbd5e1',
                                borderColor: 'rgba(255, 255, 255, 0.1)',
                                borderWidth: 1,
                                padding: 10,
                                bodyFont: { family: 'Outfit', size: 12 },
                                titleFont: { family: 'Outfit', size: 12, weight: 'bold' }
                            },
                            datalabels: {
                                display: false
                            }
                        },
                        scales: {
                            x: {
                                beginAtZero: true,
                                grid: { color: 'rgba(255,255,255,0.08)' },
                                ticks: {
                                    color: '#cbd5e1',
                                    font: { family: 'Outfit', size: 11 }
                                }
                            },
                            y: {
                                grid: { display: false },
                                ticks: {
                                    color: '#cbd5e1',
                                    font: { family: 'Outfit', size: 11 }
                                }
                            }
                        }
                    }
                });
            }
        } catch (e) { log('Error in User Chart', e); }
    });

})();


/* --- inventory.js --- */
(() => {
    /**
     * MonitorWeb — Movimientos Analytics Logic
     * Requiere: core_ui.js cargado previamente (provee window.CoreUI)
     */

    const log = (msg, data = null) => {
        console.log(`[Inventory-JS] ${msg}`, data || '');
    };

    // ── UI HELPERS — delegados a CoreUI ─────────────────────────────────
    // CoreUI provee openModal, closeModal, renderMaterialModal y getData.
    // Se crean alias locales para mantener la misma interfaz de llamada
    // que el resto del módulo usaba.

    const UI = {
        openModal: (id) => CoreUI.openModal(id),
        closeModal: (id) => CoreUI.closeModal(id),
        renderMaterialModal: (opts) => CoreUI.renderMaterialModal(opts)
    };

    const getData = (id) => CoreUI.getData(id);

    const parseFormattedInt = (val) => {
        if (val === null || val === undefined) return 0;
        let s = val.toString().replace(/[^\d]/g, ''); // Remove everything except digits
        return parseInt(s) || 0;
    };

    // ── MODAL HANDLERS ──────────────────────────────────────────────────────

    window.openModalUbicacion = (name) => {
        const data = getData('data_ubic_mapping_inv') || {};
        UI.renderMaterialModal({ modalId: 'modalUbicacion', titleId: 'modalUbicacionTitle', listId: 'modalUbicacionList', title: `Ubicación: ${name}`, items: data[name] || [], colorVar: '--calipso' });
    };
    window.openModalUserInv = (name) => {
        const data = getData('data_user_mapping_inv') || {};
        UI.renderMaterialModal({ modalId: 'modalUser', titleId: 'modalUserTitle', listId: 'modalUserList', title: `Usuario: ${name}`, items: data[name] || [], colorVar: '--naranja', bgColor: 'rgba(234,118,0,0.15)' });
    };

    document.addEventListener('DOMContentLoaded', () => {
        // Los gráficos asíncronos ahora son dibujados y manejados por saas_engine.js
        // (Fase 3: Analytics Studio SDUI).
        log('Inventory module loaded. Awaiting SaaS Widgets...');

        // Exponer función de switch de vista
        window.switchInventarioView = (view) => {
            const gran = view === 'historical' ? 'WEEK' : '';
            
            // Obtener valores actuales
            const areaAll = document.getElementById('chartAreaFilterAll')?.checked;
            const areaValues = areaAll ? '' : Array.from(document.querySelectorAll('.chart-area-cb:checked')).map(cb => cb.value).join(',');
            
            const params = {
                area: areaValues,
                year: new Date().getFullYear().toString()
            };
            if (gran) params.granularity = gran;
            
            const invTab = document.getElementById('tab-inventory');
            if (invTab && window.initSaaSWidgetsV2) {
                window.initSaaSWidgetsV2(params, invTab);
            }
        };

        // Buscador de ubicaciones dinámico — dos tablas separadas
        const ubicInput = document.getElementById('ubic-search-input');
        const ubicResults = document.getElementById('ubic-results-body');
        const ubicStockBody = document.getElementById('ubic-stock-body');
        const ubicDesc = document.getElementById('ubic-material-desc');
        let ubicTimer;

        if (ubicInput) {
            ubicInput.addEventListener('input', (e) => {
                clearTimeout(ubicTimer);
                const val = e.target.value.trim();

                const loadingHistorial = `<tr><td colspan="2" style="text-align:center;color:#38bdf8;padding:1.5rem;"><i class="fas fa-spinner fa-spin"></i> Buscando...</td></tr>`;
                const loadingStock    = `<tr><td colspan="3" style="text-align:center;color:#38bdf8;padding:1.5rem;"><i class="fas fa-spinner fa-spin"></i> Buscando...</td></tr>`;

                if (val.length < 3) {
                    if (ubicResults)   ubicResults.innerHTML   = `<tr><td colspan="2" style="text-align:center;color:#94a3b8;padding:1.5rem;">Digita al menos 3 caracteres...</td></tr>`;
                    if (ubicStockBody) ubicStockBody.innerHTML = `<tr><td colspan="3" style="text-align:center;color:#94a3b8;padding:1.5rem;">Digita al menos 3 caracteres...</td></tr>`;
                    if (ubicDesc) ubicDesc.innerText = '';
                    return;
                }

                if (ubicResults)   ubicResults.innerHTML   = loadingHistorial;
                if (ubicStockBody) ubicStockBody.innerHTML = loadingStock;
                if (ubicDesc) ubicDesc.innerText = '';

                ubicTimer = setTimeout(async () => {
                    try {
                        const response = await fetch(`/api/ubicaciones/${encodeURIComponent(val)}`);
                        if (!response.ok) throw new Error('Network error');
                        const data = await response.json();

                        if (data.length === 0) {
                            if (ubicResults)   ubicResults.innerHTML   = `<tr><td colspan="2" style="text-align:center;color:#ef4444;padding:1.5rem;">Sin resultados para "${val}"</td></tr>`;
                            if (ubicStockBody) ubicStockBody.innerHTML = `<tr><td colspan="3" style="text-align:center;color:#ef4444;padding:1.5rem;">Sin stock registrado para "${val}"</td></tr>`;
                            return;
                        }

                        // Descripción del material
                        if (ubicDesc) {
                            const matDesc = data[0].texto_breve_material || '';
                            ubicDesc.innerText = matDesc ? `🏷️ ${matDesc}` : '';
                        }

                        // ── Tabla 1: Stock Actual (solo filas con stock real) ──
                        const stockRows = data.filter(r => r.stock_disp !== null && r.stock_disp !== undefined);
                        if (ubicStockBody) {
                            if (stockRows.length === 0) {
                                ubicStockBody.innerHTML = `<tr><td colspan="3" style="text-align:center;color:#94a3b8;padding:1.5rem;">Sin stock actual registrado</td></tr>`;
                            } else {
                                ubicStockBody.innerHTML = stockRows.map(r => {
                                    const cant    = Number(r.stock_disp).toLocaleString('es-CL');
                                    const um      = r.umb || '-';
                                    const ubicAct = r.ubic_actual || '-';
                                    return `
                                        <tr>
                                            <td style="font-weight:600;color:#EA7600;">${ubicAct}</td>
                                            <td style="color:#5DBAA9;font-weight:600;">${cant}</td>
                                            <td style="color:#cbd5e1;">${um}</td>
                                        </tr>`;
                                }).join('');
                            }
                        }

                        // ── Tabla 2: Historial de Ubicaciones (todas las filas con ubicación) ──
                        if (ubicResults) {
                            const histRows = data.filter(r => r.ubic_dest);
                            if (histRows.length === 0) {
                                ubicResults.innerHTML = `<tr><td colspan="2" style="text-align:center;color:#94a3b8;padding:1.5rem;">Sin historial registrado</td></tr>`;
                            } else {
                                ubicResults.innerHTML = histRows.map(r => {
                                    const fechaFmt = r.fecha || '-';
                                    return `
                                        <tr>
                                            <td style="font-weight:600;color:#e2e8f0;">${r.ubic_dest}</td>
                                            <td style="color:#94a3b8;">${fechaFmt}</td>
                                        </tr>`;
                                }).join('');
                            }
                        }

                    } catch (error) {
                        if (ubicResults)   ubicResults.innerHTML   = `<tr><td colspan="2" style="text-align:center;color:#ef4444;padding:1.5rem;">Error de conexión.</td></tr>`;
                        if (ubicStockBody) ubicStockBody.innerHTML = `<tr><td colspan="3" style="text-align:center;color:#ef4444;padding:1.5rem;">Error de conexión.</td></tr>`;
                        log('Error fetching ubicaciones', error);
                    }
                }, 500);
            });
        }
    });

})();

// Funciones obsoletas de filtrado han sido eliminadas por el rediseño SaaS.

/* --- analytics_proyecciones.js --- */
(() => {
/**
 * MonitorWeb — IA Predictiva Analytics Logic
 * Requiere: core_ui.js cargado previamente (provee window.CoreUI)
 */

// ── UI HELPERS — delegados a CoreUI ────────────────────────────────────
// openModal/closeModal ya están en window por core_ui.js.
// populateAreaSelect y getData también son provistos por CoreUI.

const UI = {
    openModal: (id) => CoreUI.openModal(id),
    closeModal: (id) => CoreUI.closeModal(id),
    populateAreaSelect: (selectId, data, key) => CoreUI.populateAreaSelect(selectId, data, key)
};

const getData = (id) => CoreUI.getData(id);

// ── RENDERERS ───────────────────────────────────────────────────────────

function renderAlerts() {
    const allAlerts = getData('data_alerts') || [];
    const filterText = document.getElementById('searchAlertsInput').value.toLowerCase();
    const filterArea = document.getElementById('areaAlertsSelect')?.value || 'all';
    
    const html = allAlerts
        .filter(alert => {
            const matchText = alert.material.toLowerCase().includes(filterText);
            const matchArea = filterArea === 'all' || alert.area === filterArea;
            return matchText && matchArea;
        })
        .map(alert => `
            <tr>
                <td data-label="Score"><span class="badge-${alert.color}">${alert.score}%</span></td>
                <td data-label="Material" style="font-weight: 600;">${alert.material}</td>
                <td data-label="Área" style="color:#e2e8f0;">${alert.area}</td>
                <td data-label="Cant. Promedio" style="color:#e2e8f0;">${alert.avg_qty} unds</td>
                <td data-label="Mes Actual" style="color:#38bdf8; font-weight: 600;">${alert.curr_month}</td>
                <td data-label="Intervalo Promedio" style="color:#94a3b8;">Cada ${alert.avg_interval} días</td>
                <td data-label="Días de Retraso" style="color:#ef4444;">Hace ${alert.days_since} días</td>
            </tr>
        `).join('');

    document.getElementById('modalAlertsBody').innerHTML = html || '<tr><td colspan="7" style="text-align:center; color:#64748b;">No hay coincidencias.</td></tr>';
}

function renderCombos(filterText = "") {
    const allCombos = getData('data_combos') || [];
    const lowerFilter = filterText.toLowerCase();
    
    const html = allCombos
        .filter(c => c.mat_a.toLowerCase().includes(lowerFilter) || c.mat_b.toLowerCase().includes(lowerFilter))
        .map(c => `
            <div class="combo-card">
                <div class="materials">
                    <span class="mat-name" title="${c.mat_a}">${c.mat_a}</span>
                    <span class="arrow">➔</span>
                    <span class="mat-name" title="${c.mat_b}">${c.mat_b}</span>
                </div>
                <div class="prob">${c.probability}</div>
            </div>
        `).join('');

    document.getElementById('modalCombosList').innerHTML = html || '<p style="text-align:center; color:#64748b;">No hay coincidencias.</p>';
}

function renderScatter() {
    const allScatter = getData('data_scatter') || [];
    const filterText = document.getElementById('searchScatterInput').value.toLowerCase();
    const filterCategory = document.getElementById('categoryScatterSelect').value;
    const filterArea = document.getElementById('areaScatterSelect').value;
    
    const html = allScatter
        .filter(item => {
            const matchText = item.name.toLowerCase().includes(filterText);
            const matchCategory = filterCategory === 'all' || item.category === filterCategory;
            const matchArea = filterArea === 'all' || item.area_clean === filterArea;
            return matchText && matchCategory && matchArea;
        })
        .map(item => {
            let catColor = item.category === "Corredor" ? "info" : (item.category === "Elefante" ? "warning" : (item.category === "Crítico" ? "danger" : "info"));
            return `
                <tr>
                    <td data-label="Categoría"><span class="badge-${catColor}">${item.category}</span></td>
                    <td data-label="Material" style="font-weight: 600;">${item.name}</td>
                    <td data-label="Área Frecuente" style="color:#e2e8f0;">${item.area || "Varias Áreas"}</td>
                    <td data-label="Frecuencia Total" style="color:#94a3b8;">${item.x} veces</td>
                    <td data-label="Volumen Promedio" style="color:#94a3b8;">${item.y} unidades</td>
                    <td data-label="Mes Actual" style="color:#38bdf8; font-weight: 600;">${item.curr_month}</td>
                </tr>
            `;
        }).join('');

    document.getElementById('modalScatterBody').innerHTML = html || '<tr><td colspan="6" style="text-align:center; color:#64748b;">No hay coincidencias.</td></tr>';
}

// ── MODAL CONTROLLERS ───────────────────────────────────────────────────

function openModalAlerts() {
    UI.populateAreaSelect('areaAlertsSelect', getData('data_alerts') || []);
    document.getElementById('searchAlertsInput').value = '';
    if(document.getElementById('areaAlertsSelect')) document.getElementById('areaAlertsSelect').value = 'all';
    renderAlerts();
    UI.openModal('modalAlerts');
}

function openModalCombos() {
    document.getElementById('searchCombosInput').value = '';
    renderCombos();
    UI.openModal('modalCombos');
}

function openModalScatter() {
    UI.populateAreaSelect('areaScatterSelect', getData('data_scatter') || [], 'area_clean');
    document.getElementById('searchScatterInput').value = '';
    document.getElementById('categoryScatterSelect').value = 'all';
    document.getElementById('areaScatterSelect').value = 'all';
    renderScatter();
    UI.openModal('modalScatter');
}

// Global functions for inline handlers
window.openModalAlerts = openModalAlerts;
window.openModalCombos = openModalCombos;
window.openModalScatter = openModalScatter;
window.filterAlerts = renderAlerts;
window.filterCombos = () => renderCombos(document.getElementById('searchCombosInput').value);
window.filterScatter = renderScatter;

// ── CHARTS INITIALIZATION ──────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Outfit', sans-serif";

    const scatterRaw = getData('data_scatter') || [];
    
    const datasetsConfig = {
        'Corredor': { bg: 'rgba(93, 186, 169, 0.6)', border: '#5DBAA9' },
        'Elefante': { bg: 'rgba(234, 118, 0, 0.6)', border: '#EA7600' },
        'Crítico':  { bg: 'rgba(239, 68, 68, 0.6)', border: '#ef4444' },
        'Tortuga':  { bg: 'rgba(100, 116, 139, 0.6)', border: '#64748b' }
    };

    const chartDatasets = Object.keys(datasetsConfig).map(key => ({
        label: key,
        data: scatterRaw.filter(p => p.category === key).map(p => ({ x: p.x, y: p.y, label: p.name })),
        backgroundColor: datasetsConfig[key].bg,
        borderColor: datasetsConfig[key].border,
        pointRadius: 6,
        pointHoverRadius: 8
    }));

    const ctxScatter = document.getElementById('scatterChart');
    if (ctxScatter) {
        new Chart(ctxScatter.getContext('2d'), {
            type: 'scatter',
            data: { datasets: chartDatasets },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom', labels: { color: "#e2e8f0" } },
                    tooltip: { callbacks: { label: (ctx) => `${ctx.raw.label} (Freq: ${ctx.raw.x}, Vol: ${ctx.raw.y})` } },
                    datalabels: { display: false }
                },
                scales: {
                    x: { title: { display: true, text: 'Frecuencia de Salidas' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                    y: { title: { display: true, text: 'Volumen Físico Promedio' }, grid: { color: 'rgba(255,255,255,0.05)' }, type: 'logarithmic' }
                }
            }
        });
    }
});

})();

/* --- docs_explorer.js --- */
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


/* --- productivity_daily.js --- */
// static/js/productivity.js

let productivityTrendChartInst = null;
let currentDailyData = null;
let selectedDailyUsers = [];

function toggleDailyUserFilter() {
    const d = document.getElementById('daily-user-filter-dropdown');
    if(d) {
        d.style.display = (d.style.display === 'none' || d.style.display === '') ? 'block' : 'none';
    }
}

function renderDailyUserCheckboxes(summary) {
    const list = document.getElementById('daily-user-filter-list');
    if (!list) return;
    list.innerHTML = '';
    if (!summary || summary.length === 0) return;
    const users = summary.map(s => s.usuario).sort();
    users.forEach(u => {
        const lbl = document.createElement('label');
        lbl.style.cssText = "display: block !important; cursor: pointer !important; margin: 4px 0 !important; white-space: nowrap !important; text-align: left !important;";
        const chk = document.createElement('input');
        chk.type = 'checkbox';
        chk.className = 'daily-user-cb';
        chk.value = u;
        chk.style.cssText = "margin: 0 8px 0 0 !important; padding: 0 !important; vertical-align: middle !important; display: inline-block !important; width: auto !important;";
        chk.checked = selectedDailyUsers.length === 0 || selectedDailyUsers.includes(u);
        chk.onchange = onDailyUserCheckboxChange;
        
        const span = document.createElement('span');
        span.textContent = u || "Desconocido";
        span.style.cssText = "color: #ffffff !important; font-size: 14px !important; visibility: visible !important; vertical-align: middle !important; display: inline-block !important; padding: 0 !important; margin: 0 !important;";
        
        lbl.appendChild(chk);
        lbl.appendChild(span);
        list.appendChild(lbl);
    });
    const allChk = document.getElementById('daily-user-filter-all');
    if(allChk) allChk.checked = selectedDailyUsers.length === 0;
}

function toggleAllDailyUsers() {
    const allChk = document.getElementById('daily-user-filter-all');
    if(allChk && allChk.checked) {
        selectedDailyUsers = [];
    } else {
        selectedDailyUsers = ['__none__'];
    }
    const cbs = document.querySelectorAll('.daily-user-cb');
    cbs.forEach(c => c.checked = (selectedDailyUsers.length === 0));
    renderFilteredDaily();
}

function onDailyUserCheckboxChange() {
    const cbs = document.querySelectorAll('.daily-user-cb');
    const checked = Array.from(cbs).filter(c => c.checked).map(c => c.value);
    
    if(checked.length === cbs.length || checked.length === 0) {
        selectedDailyUsers = [];
        const allChk = document.getElementById('daily-user-filter-all');
        if(allChk) allChk.checked = true;
        cbs.forEach(c => c.checked = true);
    } else {
        selectedDailyUsers = checked;
        const allChk = document.getElementById('daily-user-filter-all');
        if(allChk) allChk.checked = false;
    }
    renderFilteredDaily();
}

function renderFilteredDaily() {
    if (!currentDailyData) return;
    let sum = currentDailyData.summary || [];
    let trn = currentDailyData.trend || [];
    let gps = currentDailyData.gaps || [];
    let htm = currentDailyData.heatmap || [];
    
    if (selectedDailyUsers.length > 0 && selectedDailyUsers[0] !== '__none__') {
        sum = sum.filter(x => selectedDailyUsers.includes(x.usuario));
        trn = trn.filter(x => selectedDailyUsers.includes(x.usuario));
        gps = gps.filter(x => selectedDailyUsers.includes(x.usuario));
        htm = htm.filter(x => selectedDailyUsers.includes(x.usuario));
    } else if (selectedDailyUsers.length > 0 && selectedDailyUsers[0] === '__none__') {
        sum = []; trn = []; gps = []; htm = [];
    }
    
    renderKPI1(sum);
    renderKPI2(trn);
    renderKPI3(gps);
    renderKPI4(htm);
}

// Colores institucionales de MonitorWeb
const COLORS = [
    '#5DBAA9', '#EA7600', '#BFB800', '#B46A5F', '#5142f5', '#F3D01C',
    '#34d399', '#f87171', '#60a5fa', '#fbbf24', '#a78bfa'
];

document.addEventListener("DOMContentLoaded", () => {
    // Escuchar cambios de pestaña para inicializar productividad si se abre
    // Esto se maneja usando la función switchSubTab ya existente en dashboard.js (o similar)
    // Inicializar fecha a "Ayer"
    const today = new Date();
    today.setDate(today.getDate() - 1);
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    const dateStr = `${yyyy}-${mm}-${dd}`;
    
    const dp = document.getElementById('productivity-date-picker');
    if(dp) {
        dp.value = dateStr;
    }
});

// Intercepción al abrir la sub-pestaña
// Si `switchSubTab` es global y la pestaña se llama `productividad`, 
// podemos atar un hook si existe, pero lo más fácil es simplemente cargar los datos si se cliquea.
window.switchSubTab = function(tabId, btn) {
    try {
        // Fallback si no está definida globalmente
        document.querySelectorAll('.sub-tab-content').forEach(el => el.style.display = 'none');
        const target = document.getElementById('sub-tab-' + tabId);
        if (target) target.style.display = 'block';

        if (btn) {
            document.querySelectorAll('.sub-tab-btn').forEach(b => {
                b.classList.remove('active');
                b.style.background = 'rgba(255,255,255,0.02)';
                b.style.borderColor = 'rgba(255,255,255,0.05)';
                b.style.color = '#cbd5e1';
                const badge = b.querySelector('span');
                if (badge) {
                    badge.style.background = 'rgba(255,255,255,0.1)';
                    badge.style.color = '#94a3b8';
                    badge.style.borderColor = 'rgba(255,255,255,0.2)';
                }
            });

            btn.classList.add('active');
            
            if (tabId === 'ots-pendientes') {
                btn.style.background = 'rgba(93, 186, 169, 0.15)';
                btn.style.borderColor = 'rgba(93, 186, 169, 0.4)';
                btn.style.color = '#5DBAA9';
                const badge = btn.querySelector('span');
                if (badge) {
                    badge.style.background = 'rgba(93, 186, 169, 0.2)';
                    badge.style.color = '#5DBAA9';
                    badge.style.borderColor = 'rgba(93, 186, 169, 0.3)';
                }
            } else if (tabId === 'movs-no-paletizados') {
                btn.style.background = 'rgba(239, 68, 68, 0.08)';
                btn.style.borderColor = 'rgba(239, 68, 68, 0.2)';
                btn.style.color = '#f87171';
                const badge = btn.querySelector('span');
                if (badge) {
                    badge.style.background = 'rgba(239, 68, 68, 0.15)';
                    badge.style.color = '#f87171';
                    badge.style.borderColor = 'rgba(239, 68, 68, 0.3)';
                }
            } else if (tabId === 'productividad') {
                btn.style.background = 'rgba(52, 211, 153, 0.08)';
                btn.style.borderColor = 'rgba(52, 211, 153, 0.2)';
                btn.style.color = '#34d399';
            }
        }
        
        if (tabId === 'productividad') {
            loadProductivityData();
        }
    } catch (err) {
        console.error("Error en switchSubTab:", err);
    }
};

function changeProductivityDate(offset) {
    const dp = document.getElementById('productivity-date-picker');
    if (!dp || dp.options.length === 0 || !dp.value) return;
    
    // In a select where options are sorted DESC (newest first),
    // next day (offset=1) means going UP in index (older dates are higher index).
    // Wait, typically offset=1 (Next) means newer date. If it's sorted DESC, newer dates are at lower indices.
    // So offset=1 means newIndex = selectedIndex - 1.
    // offset=-1 (Prev) means newIndex = selectedIndex + 1.
    let newIndex = dp.selectedIndex - offset;
    
    // Limit bounds
    if (newIndex < 0) newIndex = 0;
    if (newIndex >= dp.options.length) newIndex = dp.options.length - 1;
    
    if (newIndex !== dp.selectedIndex) {
        dp.selectedIndex = newIndex;
        loadProductivityData();
    }
}

function changeProductivityMonth(offsetMonths) {
    const mp = document.getElementById('productivity-month-picker');
    if (!mp || !mp.value) return;
    
    const parts = mp.value.split('-');
    const year = parseInt(parts[0], 10);
    const month = parseInt(parts[1], 10);
    
    // JS Date handles month overflow automatically (e.g. 13 -> Jan next year)
    const newDate = new Date(year, month - 1 + offsetMonths, 1);
    
    const yyyy = newDate.getFullYear();
    const mm = String(newDate.getMonth() + 1).padStart(2, '0');
    
    mp.value = `${yyyy}-${mm}`;
    loadMonthlyProductivityData();
}

async function loadProductivityData() {
    const tbody = document.getElementById('productivity-summary-tbody');
    const gapsContainer = document.getElementById('productivity-gaps-container');
    const heatmapContainer = document.getElementById('productivity-heatmap-container');

    try {
        const dp = document.getElementById('productivity-date-picker');
        if(!dp) {
            tbody.innerHTML = '<tr><td colspan="6" style="color:red;">Error: date picker no encontrado</td></tr>';
            return;
        }
        const targetDate = dp.value;

        // Loading states
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #5DBAA9; padding: 1rem;">[DEBUG] Iniciando fetch para ' + targetDate + '...</td></tr>';
        gapsContainer.innerHTML = '';
        gapsContainer.style.display = 'none';
        heatmapContainer.innerHTML = '<div style="text-align: center; color: #5DBAA9; padding: 2rem;">[DEBUG] Iniciando heatmap...</div>';

        const res = await fetch(`/api/v1/analytics/productivity?date=${targetDate}`);
        if (!res.ok) throw new Error("Fallo en la red (Status: " + res.status + ")");
        
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #5DBAA9; padding: 1rem;">[DEBUG] Fetch OK. Procesando JSON...</td></tr>';
        
        const json = await res.json();
        currentDailyData = json.data;

        // Limpiar selección al cambiar de fecha si se desea, o mantenerla si coincide
        // Por ahora la mantenemos, pero actualizamos los checkboxes con los usuarios del día
        renderDailyUserCheckboxes(currentDailyData.summary);
        
        renderFilteredDaily();
    } catch (e) {
        console.error("Error al cargar productividad:", e);
        if(tbody) tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #ef4444; padding: 1rem;">Error: ' + e.message + '</td></tr>';
        if(heatmapContainer) heatmapContainer.innerHTML = '<div style="text-align: center; color: #ef4444; padding: 2rem;">Error: ' + e.message + '</div>';
    }
}

function renderKPI1(summary) {
    const tbody = document.getElementById('productivity-summary-tbody');
    tbody.innerHTML = '';

    if (!summary || summary.length === 0) {
        const dp = document.getElementById('productivity-date-picker');
        const targetDate = dp ? dp.value : 'desconocida';
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #f59e0b; padding: 1rem;"><i class="fas fa-search"></i> Sin movimientos en esta fecha (' + targetDate + '). Revisa el formato o elige otro día.</td></tr>';
        return;
    }

    // Calcular máximo para la barra de progreso
    const maxMovs = Math.max(...summary.map(s => s.total_actividad || 0));

    summary.forEach(row => {
        const pct = maxMovs > 0 ? ((row.total_actividad / maxMovs) * 100).toFixed(1) : 0;
        
        let barColor = '#5DBAA9'; // Verde/Calipso por defecto
        if (pct < 30) barColor = '#ef4444'; // Rojo si muy bajo
        else if (pct < 60) barColor = '#f59e0b'; // Ámbar si medio

        let timeStr = '-';
        if (row.tiempo_total_minutos) {
            const h = Math.floor(row.tiempo_total_minutos / 60);
            const m = row.tiempo_total_minutos % 60;
            timeStr = h > 0 ? `${h}h ${m}m` : `${m}m`;
        }

        const tr = document.createElement('tr');
        tr.className = "loaded";
        tr.style.cursor = 'pointer';
        tr.title = "Ver detalle de movimientos";
        tr.addEventListener('click', () => abrirDetalleUsuario(row.usuario));
        tr.addEventListener('mouseenter', () => tr.style.background = 'rgba(255,255,255,0.05)');
        tr.addEventListener('mouseleave', () => tr.style.background = '');
        tr.innerHTML = `
            <td style="font-weight: 700; color: var(--calipso);">${row.usuario}</td>
            <td style="font-weight: 800; font-size: 1.1rem; color: #f8f9fa;">${row.total_actividad}</td>
            <td>
                <div style="width: 100%; background: rgba(255,255,255,0.1); border-radius: 4px; height: 12px; overflow: hidden; margin-top: 4px;" title="${pct}% del máximo">
                    <div style="width: ${pct}%; background: ${barColor}; height: 100%; border-radius: 4px; transition: width 0.5s;"></div>
                </div>
            </td>
            <td style="color: #94a3b8;">${row.primer_movimiento || '-'}</td>
            <td style="color: #94a3b8;">${row.ultimo_movimiento || '-'}</td>
            <td style="font-weight: 600; color: #34d399;" title="${row.tiempo_total_minutos || 0} min">${timeStr}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderKPI2(trend) {
    const ctx = document.getElementById('productivityTrendChart');
    if (!ctx) return;

    if (productivityTrendChartInst) {
        productivityTrendChartInst.destroy();
    }

    if (!trend || trend.length === 0) {
        return;
    }

    // Preparar Data (Horas X, Movimientos Y)
    const horasSet = new Set(trend.map(t => t.franja_horaria));
    const horas = Array.from(horasSet).sort();
    
    const data = horas.map(h => {
        const filtered = trend.filter(t => t.franja_horaria === h);
        return filtered.reduce((acc, curr) => acc + curr.total_actividad, 0);
    });

    const datasets = [{
        label: 'Movimientos del Equipo',
        data: data,
        borderColor: '#34d399',
        backgroundColor: '#34d39933',
        borderWidth: 3,
        tension: 0.3,
        fill: true,
        pointRadius: 5,
        pointBackgroundColor: '#34d399'
    }];

    productivityTrendChartInst = new Chart(ctx, {
        type: 'line',
        data: {
            labels: horas.map(h => h + ':00'),
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#e2e8f0', usePointStyle: true } }
            },
            scales: {
                x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' }, beginAtZero: true }
            }
        }
    });
}

function renderKPI3(gaps) {
    const container = document.getElementById('productivity-gaps-container');
    container.innerHTML = '';

    if (!gaps || gaps.length === 0) {
        container.style.display = 'none';
        return;
    }

    // Filtrar baches "normales" (colación entre 13:00 y 14:00 aprox).
    // Asumiremos que si la hora_anterior es >= 13:00 y <= 13:59 y hueco es <= 90 mins, es colación
    const isColacion = (h_ant, min) => {
        const h = parseInt(h_ant.substring(0, 2), 10);
        return (h >= 12 && h <= 14) && min <= 90;
    };

    let countAlerts = 0;
    
    const header = document.createElement('h4');
    header.style.color = '#fbbf24';
    header.style.marginTop = '0';
    header.style.marginBottom = '10px';
    header.innerHTML = `<i class="fas fa-exclamation-triangle"></i> Períodos sin Actividad Sistémica (>180 min)`;
    
    const listWrapper = document.createElement('div');
    listWrapper.style.display = 'flex';
    listWrapper.style.flexWrap = 'wrap';
    listWrapper.style.gap = '10px';

    gaps.forEach(g => {
        const isLunch = isColacion(g.hora_anterior, g.hueco_minutos);
        countAlerts++;

        const h = Math.floor(g.hueco_minutos / 60);
        const m = g.hueco_minutos % 60;
        const timeStr = h > 0 ? `${h}h ${m}m` : `${m}m`;

        const card = document.createElement('div');
        card.style.background = isLunch ? 'rgba(255,255,255,0.05)' : 'rgba(234, 118, 0, 0.1)';
        card.style.border = isLunch ? '1px solid rgba(255,255,255,0.1)' : '1px solid rgba(234, 118, 0, 0.3)';
        card.style.borderRadius = '8px';
        card.style.padding = '10px 15px';
        card.style.minWidth = '250px';
        card.style.flex = '1';

        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                <strong style="color: var(--calipso);">${g.usuario}</strong>
                <span style="font-weight: 700; color: ${isLunch ? '#94a3b8' : '#ea7600'}; background: ${isLunch ? 'rgba(255,255,255,0.1)' : 'rgba(234, 118, 0, 0.2)'}; padding: 2px 8px; border-radius: 4px; font-size: 0.85rem;" title="${g.hueco_minutos} min">
                    ${timeStr}
                </span>
            </div>
            <div style="font-size: 0.85rem; color: #cbd5e1;">
                De <b>${g.hora_anterior}</b> a <b>${g.hora_actual}</b>
            </div>
            ${isLunch ? '<div style="font-size: 0.75rem; color: #64748b; margin-top: 4px;"><i class="fas fa-utensils"></i> Posible Colación</div>' : ''}
        `;
        listWrapper.appendChild(card);
    });

    if (countAlerts > 0) {
        container.appendChild(header);
        container.appendChild(listWrapper);
        container.style.display = 'block';
    }
}

function renderKPI4(heatmapData) {
    const container = document.getElementById('productivity-heatmap-container');
    container.innerHTML = '';

    if (!heatmapData || heatmapData.length === 0) {
        container.innerHTML = '<div style="text-align: center; color: #64748b; padding: 2rem;">Sin datos para Heatmap en esta fecha.</div>';
        return;
    }

    // 1. Obtener lista única de horas y usuarios
    const horasSet = new Set();
    const userMap = {}; // { 'usuario1': { '08': 5, '09': 10 } }
    
    let maxMovs = 0;

    heatmapData.forEach(d => {
        horasSet.add(d.franja_horaria);
        if (!userMap[d.usuario]) userMap[d.usuario] = {};
        userMap[d.usuario][d.franja_horaria] = {
            total: d.cantidad_movimientos,
            gen: d.generados,
            conf: d.confirmados
        };
        if (d.cantidad_movimientos > maxMovs) maxMovs = d.cantidad_movimientos;
    });

    const horas = Array.from(horasSet).sort();
    const usuarios = Object.keys(userMap).sort();

    // 2. Crear Tabla de Heatmap HTML
    const table = document.createElement('table');
    table.style.width = '100%';
    table.style.borderCollapse = 'collapse';
    table.style.color = '#e2e8f0';
    table.style.fontSize = '0.85rem';

    // Cabecera (Horas)
    const thead = document.createElement('thead');
    const headRow = document.createElement('tr');
    
    const thUser = document.createElement('th');
    thUser.textContent = 'Usuario';
    thUser.style.textAlign = 'left';
    thUser.style.padding = '8px';
    thUser.style.borderBottom = '1px solid rgba(255,255,255,0.1)';
    headRow.appendChild(thUser);

    horas.forEach(h => {
        const th = document.createElement('th');
        th.textContent = h + ':00';
        th.style.textAlign = 'center';
        th.style.padding = '8px';
        th.style.borderBottom = '1px solid rgba(255,255,255,0.1)';
        headRow.appendChild(th);
    });
    thead.appendChild(headRow);
    table.appendChild(thead);

    // Cuerpo
    const tbody = document.createElement('tbody');
    
    // Función para color (Escala Calipso) #5DBAA9
    const getColor = (val, max) => {
        if (!val || val === 0) return 'rgba(255,255,255,0.02)';
        const opacity = 0.2 + (0.8 * (val / max)); // min 0.2, max 1.0
        return `rgba(93, 186, 169, ${opacity})`;
    };

    usuarios.forEach(u => {
        const tr = document.createElement('tr');
        
        const tdName = document.createElement('td');
        tdName.textContent = u;
        tdName.style.padding = '8px';
        tdName.style.fontWeight = '600';
        tdName.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
        tr.appendChild(tdName);

        horas.forEach(h => {
            const td = document.createElement('td');
            const valObj = userMap[u][h];
            const val = valObj ? valObj.total : 0;
            const gen = valObj ? valObj.gen : 0;
            const conf = valObj ? valObj.conf : 0;
            
            td.style.padding = '2px';
            td.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
            
            const cellBlock = document.createElement('div');
            cellBlock.style.background = getColor(val, maxMovs);
            cellBlock.style.color = val > 0 ? (val > (maxMovs/2) ? '#000' : '#fff') : 'transparent';
            cellBlock.style.padding = '8px 4px';
            cellBlock.style.borderRadius = '4px';
            cellBlock.style.textAlign = 'center';
            cellBlock.style.fontWeight = '700';
            cellBlock.textContent = val;
            cellBlock.title = `${u} a las ${h}:00 - ${val} Total (${gen} Gen / ${conf} Conf)`;
            
            td.appendChild(cellBlock);
            tr.appendChild(td);
        });

        tbody.appendChild(tr);
    });

    table.appendChild(tbody);
    container.appendChild(table);
}



/* --- productivity_monthly.js --- */
// ==========================================
// LÓGICA DE PRODUCTIVIDAD MENSUAL
// ==========================================

let productivityMonthlyTrendChartInst = null;
let currentMonthlyData = null;
let selectedMonthlyUsers = [];

function toggleMonthlyUserFilter() {
    const d = document.getElementById('monthly-user-filter-dropdown');
    if(d) {
        d.style.display = (d.style.display === 'none' || d.style.display === '') ? 'block' : 'none';
    }
}

function renderMonthlyUserCheckboxes(summary) {
    const list = document.getElementById('monthly-user-filter-list');
    if (!list) return;
    list.innerHTML = '';
    if (!summary || summary.length === 0) return;
    const users = summary.map(s => s.usuario).sort();
    users.forEach(u => {
        const lbl = document.createElement('label');
        lbl.style.cssText = "display: block !important; cursor: pointer !important; margin: 4px 0 !important; white-space: nowrap !important; text-align: left !important;";
        const chk = document.createElement('input');
        chk.type = 'checkbox';
        chk.className = 'monthly-user-cb';
        chk.value = u;
        chk.style.cssText = "margin: 0 8px 0 0 !important; padding: 0 !important; vertical-align: middle !important; display: inline-block !important; width: auto !important;";
        chk.checked = selectedMonthlyUsers.length === 0 || selectedMonthlyUsers.includes(u);
        chk.onchange = onMonthlyUserCheckboxChange;
        
        const span = document.createElement('span');
        span.textContent = u || "Desconocido";
        span.style.cssText = "color: #ffffff !important; font-size: 14px !important; visibility: visible !important; vertical-align: middle !important; display: inline-block !important; padding: 0 !important; margin: 0 !important;";
        
        lbl.appendChild(chk);
        lbl.appendChild(span);
        list.appendChild(lbl);
    });
    const allChk = document.getElementById('monthly-user-filter-all');
    if(allChk) allChk.checked = selectedMonthlyUsers.length === 0;
}

function toggleAllMonthlyUsers() {
    const allChk = document.getElementById('monthly-user-filter-all');
    if(allChk && allChk.checked) {
        selectedMonthlyUsers = [];
    } else {
        selectedMonthlyUsers = ['__none__'];
    }
    const cbs = document.querySelectorAll('.monthly-user-cb');
    cbs.forEach(c => c.checked = (selectedMonthlyUsers.length === 0));
    renderFilteredMonthly();
}

function onMonthlyUserCheckboxChange() {
    const cbs = document.querySelectorAll('.monthly-user-cb');
    const checked = Array.from(cbs).filter(c => c.checked).map(c => c.value);
    
    if(checked.length === cbs.length || checked.length === 0) {
        selectedMonthlyUsers = [];
        const allChk = document.getElementById('monthly-user-filter-all');
        if(allChk) allChk.checked = true;
        cbs.forEach(c => c.checked = true);
    } else {
        selectedMonthlyUsers = checked;
        const allChk = document.getElementById('monthly-user-filter-all');
        if(allChk) allChk.checked = false;
    }
    renderFilteredMonthly();
}

function renderFilteredMonthly() {
    if (!currentMonthlyData) return;
    let sum = currentMonthlyData.summary || [];
    let sft = currentMonthlyData.shifts || [];
    let htm = currentMonthlyData.heatmap || [];
    
    if (selectedMonthlyUsers.length > 0 && selectedMonthlyUsers[0] !== '__none__') {
        sum = sum.filter(x => selectedMonthlyUsers.includes(x.usuario));
        sft = sft.filter(x => selectedMonthlyUsers.includes(x.usuario));
        htm = htm.filter(x => selectedMonthlyUsers.includes(x.usuario));
    } else if (selectedMonthlyUsers.length > 0 && selectedMonthlyUsers[0] === '__none__') {
        sum = []; sft = []; htm = [];
    }
    
    renderMonthlyKPI1(sum);
    renderMonthlyKPI2(sft);
    renderMonthlyKPI3(htm);
}

document.addEventListener("DOMContentLoaded", async () => {
    // Inicializar mes a "Mes actual"
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const monthStr = `${yyyy}-${mm}`;
    
    const mp = document.getElementById('productivity-month-picker');
    if(mp) {
        mp.value = monthStr;
    }
    
    // Inicializar Fechas Diarias (Select)
    const dp = document.getElementById('productivity-date-picker');
    if (dp) {
        try {
            const res = await fetch('/api/v1/analytics/productivity/available-dates');
            if (res.ok) {
                const json = await res.json();
                const dates = json.data;
                
                dp.innerHTML = '';
                if (dates && dates.length > 0) {
                    dates.forEach(d => {
                        const opt = document.createElement('option');
                        opt.value = d;
                        opt.textContent = d;
                        dp.appendChild(opt);
                    });
                    dp.selectedIndex = 0; // Seleccionar el más reciente
                } else {
                    dp.innerHTML = '<option value="">Sin datos disponibles</option>';
                }
            }
        } catch (e) {
            console.error("Error cargando fechas disponibles:", e);
            dp.innerHTML = '<option value="">Error cargando fechas</option>';
        }
    }
});

async function loadMonthlyProductivityData() {
    const tbody = document.getElementById('productivity-monthly-summary-tbody');
    const heatmapContainer = document.getElementById('productivity-monthly-heatmap-container');

    try {
        const mp = document.getElementById('productivity-month-picker');
        if(!mp) return;
        const targetMonth = mp.value;

        // Loading states
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #5DBAA9; padding: 1rem;"><i class="fas fa-spinner fa-spin"></i> Cargando datos mensuales para ' + targetMonth + '...</td></tr>';
        heatmapContainer.innerHTML = '<div style="text-align: center; color: #5DBAA9; padding: 2rem;"><i class="fas fa-spinner fa-spin"></i> Cargando mapa de calor mensual...</div>';

        const res = await fetch(`/api/v1/analytics/productivity/monthly?month=${targetMonth}`);
        if (!res.ok) throw new Error("Fallo en la red (Status: " + res.status + ")");
        
        const json = await res.json();
        currentMonthlyData = json.data;

        renderMonthlyUserCheckboxes(currentMonthlyData.summary);
        renderFilteredMonthly();
    } catch (e) {
        console.error("Error al cargar productividad mensual:", e);
        if(tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #ef4444; padding: 1rem;">Error: ' + e.message + '</td></tr>';
        if(heatmapContainer) heatmapContainer.innerHTML = '<div style="text-align: center; color: #ef4444; padding: 2rem;">Error: ' + e.message + '</div>';
    }
}

function renderMonthlyKPI1(summary) {
    const tbody = document.getElementById('productivity-monthly-summary-tbody');
    tbody.innerHTML = '';

    if (!summary || summary.length === 0) {
        const mp = document.getElementById('productivity-month-picker');
        const targetMonth = mp ? mp.value : 'desconocido';
        tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: #f59e0b; padding: 1rem;"><i class="fas fa-search"></i> Sin movimientos en este mes (${targetMonth}).</td></tr>`;
        return;
    }

    const maxMovs = Math.max(...summary.map(s => s.total_actividad || 0));

    summary.forEach(row => {
        const pct = maxMovs > 0 ? ((row.total_actividad / maxMovs) * 100).toFixed(1) : 0;
        let barColor = '#5DBAA9';
        if (pct < 30) barColor = '#ef4444';
        else if (pct < 60) barColor = '#f59e0b';

        const tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        tr.title = "Ver desglose de operaciones";
        tr.addEventListener('click', () => abrirDetalleMensualUsuario(row.usuario));
        tr.addEventListener('mouseenter', () => tr.style.background = 'rgba(255,255,255,0.05)');
        tr.addEventListener('mouseleave', () => tr.style.background = '');
        tr.innerHTML = `
            <td style="font-weight: 700; color: var(--calipso);">${row.usuario}</td>
            <td style="font-weight: 800; font-size: 1.1rem; color: #f8f9fa;">${row.total_actividad}</td>
            <td>
                <div style="width: 100%; background: rgba(255,255,255,0.1); border-radius: 4px; height: 12px; overflow: hidden; margin-top: 4px;" title="${pct}% del máximo">
                    <div style="width: ${pct}%; background: ${barColor}; height: 100%; border-radius: 4px; transition: width 0.5s;"></div>
                </div>
            </td>
            <td style="color: #94a3b8; font-weight: 600;">${row.dias_trabajados} días</td>
            <td style="font-weight: 700; color: #34d399;">${row.promedio_actividad_dia}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderMonthlyKPI2(shifts) {
    const ctx = document.getElementById('productivityMonthlyTrendChart');
    if (!ctx) return;

    if (productivityMonthlyTrendChartInst) {
        productivityMonthlyTrendChartInst.destroy();
    }

    if (!shifts || shifts.length === 0) {
        return;
    }

    // Preparar Data (Días X, Movimientos Y, Apilados por Turno)
    const turnosSet = ['Mañana', 'Tarde', 'Noche'];
    const fechasSet = new Set(shifts.map(t => t.fecha));
    const fechas = Array.from(fechasSet).sort((a, b) => {
        const aParts = a.split('.');
        const bParts = b.split('.');
        return new Date(aParts[2], aParts[1]-1, aParts[0]) - new Date(bParts[2], bParts[1]-1, bParts[0]);
    });

    const colorMap = {
        'Mañana': '#3b82f6', // Blue
        'Tarde': '#f59e0b',  // Amber
        'Noche': '#8b5cf6'   // Purple
    };

    const datasets = turnosSet.map(turno => {
        const data = fechas.map(f => {
            const filtered = shifts.filter(t => t.fecha === f && t.turno === turno);
            return filtered.reduce((acc, curr) => acc + curr.total_actividad, 0);
        });

        return {
            label: turno,
            data: data,
            backgroundColor: colorMap[turno] + 'ee',
            hoverBackgroundColor: colorMap[turno],
            borderWidth: 0,
            borderRadius: 4
        };
    });

    const labelsX = fechas.map(d => d.split('.')[0]); // Mostrar solo el número del día

    productivityMonthlyTrendChartInst = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labelsX,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: '#e2e8f0', usePointStyle: true } },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                x: { 
                    stacked: true, 
                    grid: { color: 'rgba(255,255,255,0.05)' }, 
                    ticks: { color: '#94a3b8' },
                    title: { display: true, text: 'Día del Mes', color: '#64748b' }
                },
                y: { 
                    stacked: true, 
                    grid: { color: 'rgba(255,255,255,0.05)' }, 
                    ticks: { color: '#94a3b8' }, 
                    beginAtZero: true 
                }
            }
        }
    });
}

function renderMonthlyKPI3(heatmapData) {
    const container = document.getElementById('productivity-monthly-heatmap-container');
    container.innerHTML = '';

    if (!heatmapData || heatmapData.length === 0) {
        container.innerHTML = '<div style="text-align: center; color: #64748b; padding: 2rem;">Sin datos para Heatmap Mensual en este mes.</div>';
        return;
    }

    const DIAS_SEMANA = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    
    const userMap = {};
    const userTotals = {};
    let maxMovs = 0;

    heatmapData.forEach(d => {
        if (!userMap[d.usuario]) {
            userMap[d.usuario] = {};
            userTotals[d.usuario] = 0;
        }
        userMap[d.usuario][d.dia_semana] = {
            total: d.cantidad_movimientos,
            gen: d.generados,
            conf: d.confirmados
        };
        userTotals[d.usuario] += d.cantidad_movimientos;
        if (d.cantidad_movimientos > maxMovs) maxMovs = d.cantidad_movimientos;
    });

    const usuarios = Object.keys(userMap).sort();

    const table = document.createElement('table');
    table.style.width = '100%';
    table.style.borderCollapse = 'collapse';
    table.style.color = '#e2e8f0';
    table.style.fontSize = '0.85rem';

    // Cabecera
    const thead = document.createElement('thead');
    const headRow = document.createElement('tr');
    
    const thUser = document.createElement('th');
    thUser.textContent = 'Usuario';
    thUser.style.textAlign = 'left';
    thUser.style.padding = '8px';
    thUser.style.borderBottom = '1px solid rgba(255,255,255,0.1)';
    headRow.appendChild(thUser);

    const thTotal = document.createElement('th');
    thTotal.textContent = 'Total Mes';
    thTotal.style.textAlign = 'center';
    thTotal.style.padding = '8px';
    thTotal.style.borderBottom = '1px solid rgba(255,255,255,0.1)';
    headRow.appendChild(thTotal);

    // Iterar del Lunes (1) al Domingo (0)
    const ordenDias = [1, 2, 3, 4, 5, 6, 0];
    
    ordenDias.forEach(idx => {
        const th = document.createElement('th');
        th.textContent = DIAS_SEMANA[idx];
        th.style.textAlign = 'center';
        th.style.padding = '8px';
        th.style.borderBottom = '1px solid rgba(255,255,255,0.1)';
        headRow.appendChild(th);
    });
    thead.appendChild(headRow);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    
    const getColor = (val, max) => {
        if (!val || val === 0) return 'rgba(255,255,255,0.02)';
        const opacity = 0.2 + (0.8 * (val / max));
        return `rgba(234, 118, 0, ${opacity})`; // Usaremos Naranja para mensual para diferenciar
    };

    usuarios.forEach(u => {
        const tr = document.createElement('tr');
        
        const tdName = document.createElement('td');
        tdName.textContent = u;
        tdName.style.padding = '8px';
        tdName.style.fontWeight = '600';
        tdName.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
        tr.appendChild(tdName);

        const tdTotal = document.createElement('td');
        tdTotal.textContent = userTotals[u];
        tdTotal.style.padding = '8px';
        tdTotal.style.fontWeight = '800';
        tdTotal.style.textAlign = 'center';
        tdTotal.style.color = '#f59e0b';
        tdTotal.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
        tr.appendChild(tdTotal);

        ordenDias.forEach(idx => {
            const td = document.createElement('td');
            const valObj = userMap[u][idx];
            const val = valObj ? valObj.total : 0;
            const gen = valObj ? valObj.gen : 0;
            const conf = valObj ? valObj.conf : 0;
            
            td.style.padding = '2px';
            td.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
            
            const cellBlock = document.createElement('div');
            cellBlock.style.background = getColor(val, maxMovs);
            cellBlock.style.color = val > 0 ? (val > (maxMovs/2) ? '#fff' : '#e2e8f0') : 'transparent';
            cellBlock.style.padding = '8px 4px';
            cellBlock.style.borderRadius = '4px';
            cellBlock.style.textAlign = 'center';
            cellBlock.style.fontWeight = '700';
            cellBlock.textContent = val;
            cellBlock.title = `${u} - ${DIAS_SEMANA[idx]}: ${val} Total (${gen} Gen / ${conf} Conf)`;
            
            td.appendChild(cellBlock);
            tr.appendChild(td);
        });

        tbody.appendChild(tr);
    });

    table.appendChild(tbody);
    container.appendChild(table);
}



/* --- productivity_modals.js --- */

// ─── Modal de Movimientos de Usuario ──────────────────────────────────────────

let currentDailyUsuario = '';
let currentDailyDate = '';

async function abrirDetalleUsuario(usuario) {
    const modal = document.getElementById('modal-user-movements');
    if (!modal) return;
    
    const dp = document.getElementById('productivity-date-picker');
    const date = dp ? dp.value : '';
    if (!date || !usuario) return;

    currentDailyUsuario = usuario;
    currentDailyDate = date;

    modal.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    
    document.getElementById('user-movs-title').textContent = `👤 Detalle Diario: ${usuario}`;
    document.getElementById('user-movs-subtitle').textContent = `Cargando operaciones del ${date}...`;
    
    document.getElementById('daily-level1').classList.remove('is-hidden');
    document.getElementById('daily-level2').classList.remove('is-active');

    const tbody = document.querySelector('#table-daily-level1 tbody');
    tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; padding: 2rem; color: var(--text-muted);">Cargando...</td></tr>';

    try {
        const res = await fetch(`/api/v1/analytics/productivity/user-movements-summary?date=${date}&usuario=${usuario}`);
        if (!res.ok) throw new Error("Error al obtener resumen");
        
        const json = await res.json();
        const data = json.data || [];
        
        document.getElementById('user-movs-subtitle').textContent = `Resumen de Operaciones (${date})`;
        
        tbody.innerHTML = '';
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; padding: 2rem; color: var(--text-muted);">No hay operaciones registradas.</td></tr>';
            return;
        }

        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.style.cursor = 'pointer';
            tr.addEventListener('click', () => cargarNivel2Diario(row.operacion));
            tr.addEventListener('mouseenter', () => tr.style.background = 'rgba(255,255,255,0.05)');
            tr.addEventListener('mouseleave', () => tr.style.background = '');
            
            tr.innerHTML = `
                <td><span style="background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem;">${row.origen}</span></td>
                <td><strong style="color: var(--calipso);">${row.operacion}</strong> <span style="font-size:0.8rem; color:var(--text-muted); float:right;">(Ver detalle 👉)</span></td>
                <td style="text-align: right; font-weight: bold; font-size: 1.1rem;">${row.cantidad || 0}</td>
            `;
            tbody.appendChild(tr);
        });

    } catch (e) {
        console.error(e);
        document.getElementById('user-movs-subtitle').textContent = `Error al cargar.`;
        tbody.innerHTML = `<tr><td colspan="3" style="text-align: center; padding: 2rem; color: #ef4444;">${e.message}</td></tr>`;
    }
}

async function cargarNivel2Diario(operacion) {
    document.getElementById('daily-level1').classList.add('is-hidden');
    document.getElementById('daily-level2').classList.add('is-active');
    
    document.getElementById('daily-level2-title').textContent = `Detalle: ${operacion}`;
    
    const tbody = document.querySelector('#table-user-movements tbody');
    tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 2rem; color: var(--text-muted);">Cargando registros...</td></tr>';

    try {
        const res = await fetch(`/api/v1/analytics/productivity/user-movements-details?date=${currentDailyDate}&usuario=${currentDailyUsuario}&operacion=${encodeURIComponent(operacion)}`);
        if (!res.ok) throw new Error("Error al obtener detalle");
        
        const json = await res.json();
        const data = json.data || [];
        
        tbody.innerHTML = '';
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 2rem; color: var(--text-muted);">No hay detalle disponible.</td></tr>';
            return;
        }

        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td style="color: var(--text-muted);">${row.hora}</td>
                <td><span style="background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem;">${row.origen}</span></td>
                <td><strong style="color: var(--calipso);">${row.operacion}</strong> ${row.cmv !== '-' ? `(CMV ${row.cmv})` : ''}</td>
                <td>${row.material || '-'}</td>
                <td>${row.descripcion || '-'}</td>
                <td style="text-align: right; font-weight: bold;">${row.cantidad || 0}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error(e);
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 2rem; color: #ef4444;">${e.message}</td></tr>`;
    }
}

function volverNivel1Diario() {
    document.getElementById('daily-level2').classList.remove('is-active');
    document.getElementById('daily-level1').classList.remove('is-hidden');
}

function cerrarDetalleUsuario() {
    const modal = document.getElementById('modal-user-movements');
    if (modal) {
        modal.classList.remove('is-open');
        document.body.style.overflow = '';
    }
}

// ─── Modal de Movimientos Mensuales ──────────────────────────────────────────

let currentMonthlyUsuario = '';
let currentMonthlyDate = '';

async function abrirDetalleMensualUsuario(usuario) {
    const modal = document.getElementById('modal-monthly-user-movements');
    if (!modal) return;
    
    const dp = document.getElementById('productivity-month-picker');
    const month = dp ? dp.value : '';
    if (!month || !usuario) return;

    currentMonthlyUsuario = usuario;
    currentMonthlyDate = month;

    modal.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    
    document.getElementById('monthly-user-movs-title').textContent = `👤 Resumen Mensual: ${usuario}`;
    document.getElementById('monthly-user-movs-subtitle').textContent = `Cargando operaciones de ${month}...`;
    
    // Mostrar Nivel 1, ocultar Nivel 2
    document.getElementById('monthly-level1').classList.remove('is-hidden');
    document.getElementById('monthly-level2').classList.remove('is-active');

    const tbody = document.querySelector('#table-monthly-level1 tbody');
    tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; padding: 2rem; color: var(--text-muted);">Cargando...</td></tr>';

    try {
        const res = await fetch(`/api/v1/analytics/productivity/user-movements-monthly-summary?month=${month}&usuario=${usuario}`);
        if (!res.ok) throw new Error("Error al obtener resumen");
        
        const json = await res.json();
        const data = json.data || [];
        
        document.getElementById('monthly-user-movs-subtitle').textContent = `Resumen de Operaciones (${month})`;
        
        tbody.innerHTML = '';
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; padding: 2rem; color: var(--text-muted);">No hay operaciones registradas.</td></tr>';
            return;
        }

        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.style.cursor = 'pointer';
            tr.addEventListener('click', () => cargarNivel2Mensual(row.operacion));
            tr.addEventListener('mouseenter', () => tr.style.background = 'rgba(255,255,255,0.05)');
            tr.addEventListener('mouseleave', () => tr.style.background = '');
            
            tr.innerHTML = `
                <td><span style="background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem;">${row.origen}</span></td>
                <td><strong style="color: var(--calipso);">${row.operacion}</strong> <span style="font-size:0.8rem; color:var(--text-muted); float:right;">(Ver detalle 👉)</span></td>
                <td style="text-align: right; font-weight: bold; font-size: 1.1rem;">${row.cantidad || 0}</td>
            `;
            tbody.appendChild(tr);
        });

    } catch (e) {
        console.error(e);
        document.getElementById('monthly-user-movs-subtitle').textContent = `Error al cargar.`;
        tbody.innerHTML = `<tr><td colspan="3" style="text-align: center; padding: 2rem; color: #ef4444;">${e.message}</td></tr>`;
    }
}

async function cargarNivel2Mensual(operacion) {
    document.getElementById('monthly-level1').classList.add('is-hidden');
    document.getElementById('monthly-level2').classList.add('is-active');
    
    document.getElementById('level2-title').textContent = `Detalle: ${operacion}`;
    
    const tbody = document.querySelector('#table-monthly-level2 tbody');
    tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 2rem; color: var(--text-muted);">Cargando registros...</td></tr>';

    try {
        const res = await fetch(`/api/v1/analytics/productivity/user-movements-monthly-details?month=${currentMonthlyDate}&usuario=${currentMonthlyUsuario}&operacion=${encodeURIComponent(operacion)}`);
        if (!res.ok) throw new Error("Error al obtener detalle");
        
        const json = await res.json();
        const data = json.data || [];
        
        tbody.innerHTML = '';
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 2rem; color: var(--text-muted);">No hay detalle disponible.</td></tr>';
            return;
        }

        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td style="color: var(--text-muted);">${row.fecha}</td>
                <td style="color: var(--text-muted);">${row.hora}</td>
                <td><span style="background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem;">${row.origen}</span></td>
                <td><strong style="color: var(--calipso);">${row.operacion}</strong> ${row.cmv !== '-' ? `(CMV ${row.cmv})` : ''}</td>
                <td>${row.material || '-'}</td>
                <td>${row.descripcion || '-'}</td>
                <td style="text-align: right; font-weight: bold;">${row.cantidad || 0}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error(e);
        tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 2rem; color: #ef4444;">${e.message}</td></tr>`;
    }
}

function volverNivel1Mensual() {
    document.getElementById('monthly-level2').classList.remove('is-active');
    document.getElementById('monthly-level1').classList.remove('is-hidden');
}

function cerrarDetalleMensualUsuario() {
    const modal = document.getElementById('modal-monthly-user-movements');
    if (modal) {
        modal.classList.remove('is-open');
        document.body.style.overflow = '';
    }
}

