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
