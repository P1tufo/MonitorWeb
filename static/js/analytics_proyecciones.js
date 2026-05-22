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