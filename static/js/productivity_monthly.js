// ==========================================
// LÓGICA DE PRODUCTIVIDAD MENSUAL
// ==========================================

let productivityMonthlyTrendChartInst = null;

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
        const data = json.data;

        renderMonthlyKPI1(data.summary);
        renderMonthlyKPI2(data.shifts);
        renderMonthlyKPI3(data.heatmap);
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
            const found = shifts.find(t => t.fecha === f && t.turno === turno);
            return found ? found.total_actividad : 0;
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

