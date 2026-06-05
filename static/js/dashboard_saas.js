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
