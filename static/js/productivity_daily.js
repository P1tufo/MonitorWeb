// static/js/productivity.js

let productivityTrendChartInst = null;

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
        const data = json.data;

        renderKPI1(data.summary);
        renderKPI2(data.trend);
        renderKPI3(data.gaps);
        renderKPI4(data.heatmap);
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
        const found = trend.find(t => t.franja_horaria === h);
        return found ? found.total_actividad : 0;
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

