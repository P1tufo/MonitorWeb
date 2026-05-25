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
                if (data.raw_data && data.raw_data.length > 0) {
                    const firstRow = data.raw_data[0];
                    const valCol = Object.keys(firstRow)[0];
                    val = firstRow[valCol];
                }
                widget.innerHTML = `<span style="font-size: 1.8rem; font-weight: 800; color: inherit;">${val.toLocaleString ? val.toLocaleString('de-DE') : val}</span>`;
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

                const grouped = {};
                data.raw_data.forEach(r => {
                    const area = r[areaKey];
                    if (!grouped[area]) grouped[area] = { labels: [], data: [], sum: 0, count: 0 };
                    grouped[area].labels.push(r[labelKey]);
                    grouped[area].data.push(r[numericKey]);
                    grouped[area].sum += r[numericKey];
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
                    title.innerHTML = `${area} <span style="color: ${statusColor}; margin-left: 8px; font-weight: bold;">Avg: ${avg}%</span>`;
                    title.style.cssText = 'font-size: 0.75rem; color: #94a3b8; margin-bottom: 8px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px; pointer-events: none;';
                    wrapper.appendChild(title);
                    
                    const canvasWrapper = document.createElement('div');
                    canvasWrapper.style.cssText = 'position: relative; height: 160px; width: 100%; pointer-events: none;';
                    const canvas = document.createElement('canvas');
                    canvasWrapper.appendChild(canvas);
                    wrapper.appendChild(canvasWrapper);
                    widget.appendChild(wrapper);

                    const chart = new Chart(canvas.getContext('2d'), {
                        type: 'line',
                        plugins: [ChartDataLabels],
                        data: {
                            labels: areaData.labels,
                            datasets: [
                                { label: area, data: areaData.data, borderColor: color, backgroundColor: 'transparent', borderWidth: 3, pointRadius: 2, tension: 0.3 },
                                { label: 'Meta (90%)', data: new Array(areaData.labels.length).fill(90), borderColor: 'rgba(255, 255, 255, 0.1)', borderWidth: 1, borderDash: [5, 5], pointRadius: 0, fill: false }
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
                    window.saasChartInstancesV2[`${queryId}_trellis`].push(chart);
                }
            } else {
                const canvas = document.createElement('canvas');
                widget.appendChild(canvas);
                
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
                                let dsFormat = data.dataset_formats ? data.dataset_formats[datasetLabel] : data.format;

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
                    
                    // Si tenemos meses ideales, el "Punto Ideal" comprobado es el promedio de esos meses.
                    // Si no, usamos el promedio global de volumen como punto base.
                    let baseCap = 0;
                    if (idealVols.length > 0) {
                        baseCap = idealVols.reduce((a, b) => a + b, 0) / idealVols.length;
                    } else {
                        const validVols = volData.map(Number).filter(n => !isNaN(n) && n > 0);
                        if (validVols.length > 0) {
                            baseCap = validVols.reduce((a, b) => a + b, 0) / validVols.length;
                        }
                    }
                    
                    // Proyección teórica-práctica para garantizar una escala lógica progresiva
                    const valIdeal = Math.floor(baseCap);
                    const valRisk = Math.floor(baseCap * 1.15); // +15% de exigencia
                    const valFail = Math.floor(baseCap * 1.30); // +30% de exigencia
                    
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

// Interceptar o inyectarnos en el update
document.addEventListener('DOMContentLoaded', () => {
    // Iniciar
    setTimeout(() => {
        initSaaSWidgetsV2();
    }, 500); // Pequeño delay para asegurar que el DOM y Chart.js estén listos
});

// Exponer globalmente
window.initSaaSWidgetsV2 = initSaaSWidgetsV2;

window.openDrilldownModal = async function(queryId, segmentLabel, materialId = null) {
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
        let html = '<table class="mini-table" style="width: 100%; border-collapse: collapse;"><thead><tr>';
        cols.forEach(c => html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: left;">${c}</th>`);
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
