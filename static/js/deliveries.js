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

    // 5. Monthly Trend Chart (Historical)
    const monthlyLabels = getData('data_monthly_labels') || [];
    const monthlyData = getData('data_monthly_data') || [];
    const ctxMonthly = document.getElementById('monthlyTrendChart');

    if (ctxMonthly && monthlyLabels.length > 0) {
        window.monthlyTrendChart = new Chart(ctxMonthly.getContext('2d'), {
            type: 'line',
            plugins: [ChartDataLabels],
            data: {
                labels: monthlyLabels,
                datasets: [{
                    label: 'Entregas por Mes',
                    data: monthlyData,
                    borderColor: '#5DBAA9',
                    backgroundColor: 'rgba(93, 186, 169, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#5DBAA9',
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    datalabels: {
                        color: '#ffffff',
                        align: 'top',
                        font: { weight: 'bold' },
                        formatter: v => v.toLocaleString('de-DE')
                    }
                },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    // 6. Weekly Trend Chart (Historical)
    const weeklyLabels = getData('data_weekly_labels') || [];
    const weeklyData = getData('data_weekly_data') || [];
    const ctxWeekly = document.getElementById('weeklyTrendChart');

    if (ctxWeekly && weeklyLabels.length > 0) {
        window.weeklyTrendChart = new Chart(ctxWeekly.getContext('2d'), {
            type: 'line',
            plugins: [ChartDataLabels],
            data: {
                labels: weeklyLabels,
                datasets: [{
                    label: 'Entregas por Semana',
                    data: weeklyData,
                    borderColor: '#EA7600',
                    backgroundColor: 'rgba(234, 118, 0, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.3,
                    pointBackgroundColor: '#EA7600',
                    pointRadius: 2,
                    pointHoverRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    datalabels: {
                        display: true,
                        color: '#ffffff',
                        align: 'top',
                        font: { weight: 'bold', size: 10 },
                        formatter: v => v > 0 ? v : ''
                    }
                },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } },
                    x: { 
                        grid: { display: false },
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45,
                            autoSkip: true,
                            maxTicksLimit: 20
                        }
                    }
                }
            }
        });
    }

    // 9. SLA Trend Chart (Historical)
    const slaTrendLabels = getData('data_sla_trend_labels') || [];
    const slaTrendData = getData('data_sla_trend_data') || [];
    const slaTrendCount = getData('data_sla_trend_count') || [];
    const ctxSlaTrend = document.getElementById('slaTrendChart');

    if (ctxSlaTrend && slaTrendLabels.length > 0) {
        window.slaTrendChart = new Chart(ctxSlaTrend.getContext('2d'), {
            type: 'line',
            plugins: [ChartDataLabels],
            data: {
                labels: slaTrendLabels,
                datasets: [
                    {
                        label: 'Eficiencia % On-Time',
                        data: slaTrendData,
                        borderColor: '#22c55e',
                        backgroundColor: 'rgba(34, 197, 94, 0.1)',
                        borderWidth: 3, fill: true, tension: 0.4,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Materiales Solicitados',
                        data: slaTrendCount,
                        borderColor: '#EA7600',
                        backgroundColor: 'transparent',
                        borderWidth: 2, borderDash: [5, 5], tension: 0.4,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: {
                    legend: { display: true, position: 'top', labels: { color: '#94a3b8', boxWidth: 12 } },
                    datalabels: { 
                        display: true,
                        color: (ctx) => ctx.dataset.borderColor,
                        align: (ctx) => ctx.datasetIndex === 0 ? 'top' : 'bottom',
                        font: { weight: 'bold', size: 10 },
                        formatter: (v, ctx) => ctx.datasetIndex === 0 ? v + '%' : v.toLocaleString('de-DE')
                    }
                },
                scales: {
                    y: { 
                        min: 0, max: 100, 
                        title: { display: true, text: 'Eficiencia %', color: '#22c55e', font: { weight: 'bold' } },
                        ticks: { color: '#22c55e' },
                        grid: { color: 'rgba(34, 197, 94, 0.1)' } 
                    },
                    y1: {
                        type: 'linear', display: true, position: 'right',
                        beginAtZero: true,
                        grace: '10%',
                        title: { display: true, text: 'Cant. Materiales', color: '#EA7600', font: { weight: 'bold' } },
                        ticks: { color: '#EA7600' },
                        grid: { drawOnChartArea: false }
                    },
                    x: { grid: { display: false }, ticks: { autoSkip: true, maxTicksLimit: 12 } }
                }
            }
        });
    }

    // 10. SLA Trend by Area (Trellis Chart / Small Multiples)
    const slaAreaLabels = getData('data_sla_area_labels') || [];
    const slaAreaDatasets = getData('data_sla_area_datasets') || [];
    const trellisContainer = document.getElementById('sla-trellis-container');
    
    if (trellisContainer && slaAreaLabels.length > 0) {
        trellisContainer.innerHTML = ''; // Limpiar
        window.slaTrellisCharts = [];
        
        const premiumColors = ["#22c55e", "#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#ec4899"];
        
        slaAreaDatasets.forEach((ds, i) => {
            const color = premiumColors[i % premiumColors.length];
            
            // Usar el promedio calculado en el servidor (más fiable)
            const avg = ds.avg_kpi || 0;
            let statusColor = '#ef4444'; // Red
            if (avg >= 95) statusColor = '#22c55e'; // Green
            else if (avg >= 85) statusColor = '#f59e0b'; // Amber/Yellow

            // 1. Crear elemento contenedor
            const wrapper = document.createElement('div');
            wrapper.className = 'trellis-item';
            wrapper.style.cssText = 'background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 10px; height: 220px;';
            
            const title = document.createElement('h4');
            title.innerHTML = `${ds.label} <span style="color: ${statusColor}; margin-left: 8px; font-weight: bold;">Avg: ${avg}%</span>`;
            title.style.cssText = 'font-size: 0.75rem; color: #94a3b8; margin-bottom: 8px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px;';
            wrapper.appendChild(title);
            
            const canvasWrapper = document.createElement('div');
            canvasWrapper.style.cssText = 'position: relative; height: 160px; width: 100%;';
            const canvas = document.createElement('canvas');
            canvasWrapper.appendChild(canvas);
            wrapper.appendChild(canvasWrapper);
            
            trellisContainer.appendChild(wrapper);
            
            // 2. Inicializar Mini Chart
            const chart = new Chart(canvas.getContext('2d'), {
                type: 'line',
                plugins: [ChartDataLabels],
                data: {
                    labels: slaAreaLabels,
                    datasets: [
                        {
                            label: ds.label,
                            data: ds.data,
                            borderColor: color,
                            backgroundColor: 'transparent',
                            borderWidth: 3,
                            pointRadius: 2,
                            tension: 0.3
                        },
                        {
                            label: 'Meta (95%)',
                            data: new Array(slaAreaLabels.length).fill(95),
                            borderColor: 'rgba(255, 255, 255, 0.1)',
                            borderWidth: 1,
                            borderDash: [5, 5],
                            pointRadius: 0,
                            fill: false
                        }
                    ]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        datalabels: { 
                            display: true, 
                            color: color, 
                            font: { size: 9, weight: 'bold' },
                            align: 'top',
                            formatter: (v, ctx) => ctx.datasetIndex === 0 ? v + '%' : ''
                        },
                        tooltip: { enabled: true }
                    },
                    scales: {
                        y: { min: 0, max: 100, ticks: { display: false }, grid: { display: false } },
                        x: { ticks: { autoSkip: true, maxTicksLimit: 5, font: { size: 8 } }, grid: { display: false } }
                    }
                }
            });
            window.slaTrellisCharts.push(chart);
        });
    }

    // 11. Monthly SLA Trend Chart (ANNUAL VIEW)
    const slaMonthlyLabels = getData('data_sla_monthly_labels') || [];
    const slaMonthlyData = getData('data_sla_monthly_data') || [];
    const slaMonthlyCount = getData('data_sla_monthly_count') || [];
    const ctxSlaMonthly = document.getElementById('slaMonthlyTrendChart');
    if (ctxSlaMonthly && slaMonthlyLabels.length > 0) {
        window.slaMonthlyTrendChart = new Chart(ctxSlaMonthly.getContext('2d'), {
            type: 'line',
            plugins: [ChartDataLabels],
            data: {
                labels: slaMonthlyLabels,
                datasets: [
                    {
                        label: 'Eficiencia % On-Time',
                        data: slaMonthlyData,
                        borderColor: '#10B981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        borderWidth: 3, fill: true, tension: 0.4,
                        yAxisID: 'y'
                    },
                    {
                        label: 'Materiales Solicitados',
                        data: slaMonthlyCount,
                        borderColor: '#38bdf8',
                        backgroundColor: 'transparent',
                        borderWidth: 2, borderDash: [5, 5], tension: 0.4,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: {
                    legend: { display: true, position: 'top', labels: { color: '#94a3b8', boxWidth: 12 } },
                    datalabels: { 
                        display: true,
                        color: (ctx) => ctx.dataset.borderColor,
                        align: (ctx) => ctx.datasetIndex === 0 ? 'top' : 'bottom',
                        font: { weight: 'bold', size: 10 },
                        formatter: (v, ctx) => ctx.datasetIndex === 0 ? v + '%' : v.toLocaleString('de-DE')
                    }
                },
                scales: {
                    y: { 
                        min: 0, max: 100, 
                        title: { display: true, text: 'Eficiencia %', color: '#10B981', font: { weight: 'bold' } },
                        ticks: { color: '#10B981' },
                        grid: { color: 'rgba(16, 185, 129, 0.1)' } 
                    },
                    y1: {
                        type: 'linear', display: true, position: 'right',
                        beginAtZero: true,
                        grace: '10%',
                        title: { display: true, text: 'Cant. Materiales', color: '#38bdf8', font: { weight: 'bold' } },
                        ticks: { color: '#38bdf8' },
                        grid: { drawOnChartArea: false }
                    },
                    x: { grid: { display: false }, ticks: { autoSkip: true, maxTicksLimit: 12 } }
                }
            }
        });
    }

    // 12. Monthly SLA Trend by Area (ANNUAL TRELLIS)
    const slaAreaMonthlyLabels = getData('data_sla_area_monthly_labels') || [];
    const slaAreaMonthlyDatasets = getData('data_sla_area_monthly_datasets') || [];
    const trellisMonthlyContainer = document.getElementById('sla-monthly-trellis-container');
    
    if (trellisMonthlyContainer && slaAreaMonthlyLabels.length > 0) {
        trellisMonthlyContainer.innerHTML = '';
        window.slaMonthlyTrellisCharts = [];
        const premiumColors = ["#22c55e", "#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#ec4899"];
        
        slaAreaMonthlyDatasets.forEach((ds, i) => {
            const color = premiumColors[i % premiumColors.length];
            const avg = ds.avg_kpi || 0;
            let statusColor = '#ef4444'; // Red
            if (avg >= 95) statusColor = '#22c55e'; // Green
            else if (avg >= 85) statusColor = '#f59e0b'; // Amber/Yellow

            const wrapper = document.createElement('div');
            wrapper.style.cssText = 'background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 10px; height: 220px;';
            const title = document.createElement('h4');
            title.innerHTML = `${ds.label} <span style="color: ${statusColor}; margin-left: 8px; font-weight: bold;">Avg: ${avg}%</span>`;
            title.style.cssText = 'font-size: 0.75rem; color: #94a3b8; margin-bottom: 8px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px;';
            wrapper.appendChild(title);
            
            const canvasWrapper = document.createElement('div');
            canvasWrapper.style.cssText = 'position: relative; height: 160px; width: 100%;';
            const canvas = document.createElement('canvas');
            canvasWrapper.appendChild(canvas);
            wrapper.appendChild(canvasWrapper);
            trellisMonthlyContainer.appendChild(wrapper);
            
            const chart = new Chart(canvas.getContext('2d'), {
                type: 'line',
                plugins: [ChartDataLabels],
                data: {
                    labels: slaAreaMonthlyLabels,
                    datasets: [
                        { label: ds.label, data: ds.data, borderColor: color, borderWidth: 3, pointRadius: 2, tension: 0.3 },
                        { label: 'Meta', data: new Array(slaAreaMonthlyLabels.length).fill(95), borderColor: 'rgba(255, 255, 255, 0.1)', borderWidth: 1, borderDash: [5, 5], pointRadius: 0, fill: false }
                    ]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        datalabels: { 
                            display: true, color: color, font: { size: 9, weight: 'bold' }, align: 'top',
                            formatter: (v, ctx) => ctx.datasetIndex === 0 ? v + '%' : ''
                        }
                    },
                    scales: {
                        y: { min: 0, max: 100, ticks: { display: false }, grid: { display: false } },
                        x: { ticks: { autoSkip: true, maxTicksLimit: 6, font: { size: 8 } }, grid: { display: false } }
                    }
                }
            });
            window.slaMonthlyTrellisCharts.push(chart);
        });
    }

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
    if (!window.intensidadChart) return;
    const selected = Array.from(document.querySelectorAll('.chart-area-cb:checked')).map(cb => cb.value);
    
    // 1. Update Intensity Chart Visibility
    window.intensidadChart.data.datasets.forEach((ds, i) => {
        window.intensidadChart.setDatasetVisibility(i, selected.includes(ds.label));
    });
    window.intensidadChart.update();

    // 2. Recalculate KPIs
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

    // 4. Update Area Mix Chart (Filter categories)
    if (window.areaMixChart) {
        const filteredStats = areaStats.filter(s => selected.includes(s.area));
        window.areaMixChart.data.labels = filteredStats.map(s => s.area);
        window.areaMixChart.data.datasets[0].data = filteredStats.map(s => s.promedio_diario);
        window.areaMixChart.data.datasets[1].data = filteredStats.map(s => s.promedio_diario_cm || 0);
        window.areaMixChart.update();
    }

    // 5. Update Week Heat Chart
    const weekdayRaw = getData('data_weekday_raw') || [];
    if (window.weekHeatChart && weekdayRaw.length > 0) {
        const daysMap = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'};
        const sums = {'Lunes':0, 'Martes':0, 'Miércoles':0, 'Jueves':0, 'Viernes':0};
        const counts = {'Lunes':0, 'Martes':0, 'Miércoles':0, 'Jueves':0, 'Viernes':0};
        const sumsCM = {'Lunes':0, 'Martes':0, 'Miércoles':0, 'Jueves':0, 'Viernes':0};
        const countsCM = {'Lunes':0, 'Martes':0, 'Miércoles':0, 'Jueves':0, 'Viernes':0};
        
        const currentMonth = new Date().getMonth() + 1;

        weekdayRaw.forEach(r => {
            if (selected.includes(r.area)) {
                try {
                    const p = r.fe_carga.split('-');
                    const d = new Date(p[2], p[1]-1, p[0]);
                    let wd = (d.getDay() + 6) % 7; 
                    let dayName = daysMap[wd];
                    if (dayName === 'Sábado' || dayName === 'Domingo') dayName = 'Lunes';
                    if (sums[dayName] !== undefined) {
                        sums[dayName] += r.count;
                        counts[dayName]++;
                        if (parseInt(p[1]) === currentMonth) {
                            sumsCM[dayName] += r.count;
                            countsCM[dayName]++;
                        }
                    }
                } catch(e){}
            }
        });
        
        const labels = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'];
        window.weekHeatChart.data.datasets[0].data = labels.map(l => counts[l] > 0 ? Math.round(sums[l]/counts[l]) : 0);
        window.weekHeatChart.data.datasets[1].data = labels.map(l => countsCM[l] > 0 ? Math.round(sumsCM[l]/countsCM[l]) : 0);
        window.weekHeatChart.update();
    }

    // 6. Filter Locations List
    document.querySelectorAll('.rank-list li[data-area]').forEach(li => {
        const area = li.getAttribute('data-area');
        // Solicitadores list also has data-area, this handles both
        li.style.display = (selected.includes(area) || area === 'MIXTO') ? '' : 'none';
    });
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