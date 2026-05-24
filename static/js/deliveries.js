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

        window.initSaaSWidgets({
            date: dateValues,
            area: areaValues,
            centro: centroValue,
            has_ots_filter: otsValue
        });
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
    updateDeliveriesAnalytics();
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
    updateDeliveriesAnalytics();
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