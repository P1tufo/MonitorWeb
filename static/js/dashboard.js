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
            window.location.href = '/login';
        } catch (e) {
            window.location.href = '/login';
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

// ── RENDERERS ───────────────────────────────────────────────────────────

function renderTableRow(t) {
    const statusClass = t.estado_wms.includes('Contabilizado') ? 'status-tratada'
        : (t.estado_wms.includes('Abierta') ? 'status-abierta' : 'status-error');

    return `
        <tr class="row">
            <td style="font-weight:600;">
                ${t.entrega}
                ${t.has_ots ? '<span title="Contiene OT(s) asociada(s)" style="font-size:0.8rem; margin-left:5px;">🏷️</span>' : ''}
            </td>
            <td>${t.fe_carga}</td>
            <td><span class="status-badge" style="background:rgba(255,255,255,0.05);">📦 ${t.num_items} items</span></td>
            <td><span style="opacity:0.7;">${t.area_negocio}</span></td>
            <td><span class="status-badge ${statusClass}">${t.estado_wms}</span></td>
            <td>
                <form action="/generate-pdf" method="post" onsubmit="updateLogoVal(document.activeElement);">
                    <input type="hidden" name="entrega" value="${t.entrega}">
                    <input type="hidden" name="include_logo" class="logo-hidden" value="true">
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

    // Update Table
    document.getElementById('transactionBody').innerHTML = tableData.map(renderTableRow).join('');
    filterTable();
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
window.logout = () => DashboardAPI.logout();
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
});

