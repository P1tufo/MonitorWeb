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
        let html = '<table class="mini-table" id="drilldownModalTable" style="width: 100%; border-collapse: collapse;"><thead><tr>';
        cols.forEach((c, i) => html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: left; cursor: pointer; white-space: nowrap;" onclick="window.sortDrilldownTable(${i})" title="Clic para ordenar">${c} ↕</th>`);
        html += '</tr><tr class="filter-row">';
        cols.forEach(c => html += `<th style="padding: 4px;"><input type="text" class="col-filter" placeholder="🔍 Filtrar..." onkeyup="window.filterDrilldownTable()" style="width: 100%; min-width: 60px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 4px; border-radius: 4px; font-size: 0.8rem;"></th>`);
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

// --- Drilldown Table Utilities ---
window.sortDrilldownTable = function(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("drilldownModalTable");
    if(!table) return;
    switching = true;
    dir = "asc"; 
    while (switching) {
        switching = false;
        rows = table.querySelectorAll("tbody tr");
        for (i = 0; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            let valX = x.innerText.trim().toLowerCase();
            let valY = y.innerText.trim().toLowerCase();
            
            if (!isNaN(parseFloat(valX)) && !isNaN(parseFloat(valY))) {
                valX = parseFloat(valX);
                valY = parseFloat(valY);
            }

            if (dir == "asc") {
                if (valX > valY) { shouldSwitch = true; break; }
            } else if (dir == "desc") {
                if (valX < valY) { shouldSwitch = true; break; }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount ++; 
        } else {
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
};

window.filterDrilldownTableTimer = null;
window.filterDrilldownTable = function() {
    clearTimeout(window.filterDrilldownTableTimer);
    window.filterDrilldownTableTimer = setTimeout(() => {
        var table = document.getElementById("drilldownModalTable");
        if(!table) return;
        var inputs = Array.from(table.querySelectorAll("thead .col-filter"));
        var activeFilters = inputs.map((inp, idx) => ({ value: inp.value.toLowerCase(), index: idx })).filter(f => f.value);
        
        var trs = table.querySelectorAll("tbody tr");
        
        // Use requestAnimationFrame for smoother UI if there are many rows
        let i = 0;
        const chunk = 100;
        
        function processChunk() {
            let end = Math.min(i + chunk, trs.length);
            for (; i < end; i++) {
                let tr = trs[i];
                let display = '';
                if (activeFilters.length > 0) {
                    let tds = tr.getElementsByTagName("td");
                    for (let f of activeFilters) {
                        let td = tds[f.index];
                        if (td && td.textContent.toLowerCase().indexOf(f.value) === -1) {
                            display = 'none';
                            break;
                        }
                    }
                }
                tr.style.display = display;
            }
            if (i < trs.length) {
                requestAnimationFrame(processChunk);
            }
        }
        processChunk();
    }, 300);
};
