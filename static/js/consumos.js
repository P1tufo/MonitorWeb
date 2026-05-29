document.addEventListener('DOMContentLoaded', () => {
    // Generar 25 celdas tipo Excel
    const grid = document.getElementById('material-grid');
    if(grid) {
        for(let i=0; i<25; i++) {
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'excel-cell';
            input.dataset.index = i;
            
            // Estilos en línea para simular celda
            input.style.border = '1px solid var(--border)';
            input.style.background = 'rgba(0,0,0,0.2)';
            input.style.color = 'var(--text)';
            input.style.padding = '8px';
            input.style.borderRadius = '4px';
            input.style.width = '100%';
            input.style.fontSize = '0.9rem';
            input.style.outline = 'none';

            // Soportar pegado múltiple
            input.addEventListener('paste', handlePaste);
            grid.appendChild(input);
        }
    }
});

function handlePaste(e) {
    e.preventDefault();
    const paste = (e.clipboardData || window.clipboardData).getData('text');
    // Separar por salto de línea o tab
    const values = paste.split(/[\r\n\t]+/).map(v => v.trim()).filter(v => v);
    
    const startIndex = parseInt(e.target.dataset.index);
    const inputs = document.querySelectorAll('.excel-cell');
    
    for(let i=0; i<values.length; i++) {
        const targetIndex = startIndex + i;
        if(targetIndex < inputs.length) {
            inputs[targetIndex].value = values[i];
        } else {
            break; // No hay más celdas disponibles
        }
    }
}

function limpiarGrilla() {
    document.querySelectorAll('.excel-cell').forEach(input => input.value = '');
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
function renderVanillaTable(tbodyId, data, columns) {
    const tbody = document.querySelector(`#${tbodyId} tbody`);
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    if (data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="${columns.length}" style="text-align: center; color: var(--text-muted); padding: 20px;">No hay datos para mostrar</td></tr>`;
        return;
    }

    data.forEach(row => {
        const tr = document.createElement('tr');
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
            { data: 'cantidad_total', render: formatearNumero, style: "text-align: right;" },
            { 
                data: 'costo_total', 
                render: (val, row) => formatearDinero(row.cantidad_total && row.cantidad_total !== 0 ? val / row.cantidad_total : 0),
                style: "text-align: right;" 
            },
            { data: 'costo_total', render: formatearDinero, style: "text-align: right;" }
        ];

        renderVanillaTable('table-ceco-mes', data.mes_actual, cecoCols);
        renderVanillaTable('table-ceco-hist', data.historico, cecoCols);

    } catch (err) {
        console.error(err);
        alert(`Ocurrió un error al buscar el CeCo (${ceco}). Detalle: ${err.message}`);
    }
}

async function buscarPorMateriales() {
    const inputs = document.querySelectorAll('.excel-cell');
    const materiales = Array.from(inputs).map(i => i.value.trim().toUpperCase()).filter(v => v);

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
        document.getElementById('th-costo-mat').innerHTML = `Costo Total (${formatearDinero(sumMat)})`;
        document.getElementById('th-costo-mes-mat').innerHTML = `Costo Este Mes (${formatearDinero(sumMatMes)})`;

        const matCols = [
            { data: 'material' },
            { data: 'descripcion' },
            { data: 'area_negocio' },
            { data: 'cantidad_mes', render: formatearNumero, style: "text-align: right;" },
            { data: 'costo_mes', render: formatearDinero, style: "text-align: right;" },
            { data: 'cantidad_total', render: formatearNumero, style: "text-align: right;" },
            { 
                data: 'costo_total', 
                render: (val, row) => formatearDinero(row.cantidad_total && row.cantidad_total !== 0 ? val / row.cantidad_total : 0),
                style: "text-align: right;" 
            },
            { data: 'costo_total', render: formatearDinero, style: "text-align: right;" }
        ];

        renderVanillaTable('table-materiales', json.data, matCols);

    } catch (err) {
        console.error(err);
        alert(`Ocurrió un error al analizar los materiales. Detalle: ${err.message}`);
    }
}
