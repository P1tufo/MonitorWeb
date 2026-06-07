window.openDrilldownModal = async function(queryId, segmentLabel, materialId = null) {
    if (queryId === 'inv_cmv_201_mensual') {
        window.openCmv201Modal();
        return;
    }

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

// --- Custom Modal CMV 201 ---
window.currentCmv201PlanType = 'planificado';
window.currentCmv201Area = '';
window.cmv201MonthsAvailable = [];

window.openCmv201Modal = function() {
    const modal = document.getElementById('modalCmv201');
    if (!modal) return;
    if (window.openModal) window.openModal('modalCmv201');
    else modal.classList.add('show');
    
    document.getElementById('cmv201AreaDetailsContainer').style.display = 'none';
    document.getElementById('cmv201TableContainer').style.display = 'block';

    // Default to 'planificado' when opening
    window.loadCmv201Data('planificado');
};

window.loadCmv201Data = async function(planType) {
    window.currentCmv201PlanType = planType;
    // Update button styles
    const btnPlanificado = document.getElementById('btnPlanificado');
    const btnDesplanificado = document.getElementById('btnDesplanificado');
    
    if (planType === 'planificado') {
        btnPlanificado.className = 'btn btn-primary';
        btnDesplanificado.className = 'btn btn-secondary';
    } else {
        btnPlanificado.className = 'btn btn-secondary';
        btnDesplanificado.className = 'btn btn-primary';
    }

    const spinner = document.getElementById('cmv201Spinner');
    const container = document.getElementById('cmv201TableContainer');
    
    spinner.style.display = 'block';
    container.innerHTML = '';
    
    try {
        const year = new Date().getFullYear().toString();
        const res = await fetch(`/api/custom/cmv201_summary?plan_type=${planType}&year=${year}`);
        const data = await res.json();
        
        spinner.style.display = 'none';
        
        if (!data || data.length === 0) {
            container.innerHTML = '<div style="text-align:center; padding:20px; color:#94a3b8;">No se encontraron datos.</div>';
            return;
        }
        
        // Pivot the data to show areas as rows and months as columns
        const monthsSet = new Set();
        const areasData = {};
        
        data.forEach(row => {
            const area = row.area_negocio || 'Sin Área';
            const mes = row.mes || 'Sin Mes';
            monthsSet.add(mes);
            
            if (!areasData[area]) {
                areasData[area] = {};
            }
            areasData[area][mes] = row.cantidad;
        });
        
        const months = Array.from(monthsSet).sort();
        window.cmv201MonthsAvailable = months;
        
        let html = '<table class="mini-table" style="width: 100%; border-collapse: collapse;"><thead><tr>';
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: left;">Área de Negocio</th>`;
        months.forEach(m => {
            html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">${m}</th>`;
        });
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Total</th>`;
        html += '</tr></thead><tbody>';
        
        for (const [area, mesData] of Object.entries(areasData)) {
            html += `<tr style="transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'">`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; font-weight: bold;"><a href="javascript:void(0)" onclick="window.openCmv201AreaDetails('${area}')" style="color: var(--primary); text-decoration: none; border-bottom: 1px dashed var(--primary); padding-bottom: 2px;">${area}</a></td>`;
            
            let rowTotal = 0;
            months.forEach(m => {
                const val = mesData[m] || 0;
                rowTotal += val;
                html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">${val.toLocaleString('de-DE')}</td>`;
            });
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: var(--primario); text-align: right; font-weight: bold;">${rowTotal.toLocaleString('de-DE')}</td>`;
            html += '</tr>';
        }
        
        html += '</tbody></table>';
        container.innerHTML = html;
        
    } catch (e) {
        spinner.style.display = 'none';
        container.innerHTML = `<div style="color:var(--rojo); padding:20px; text-align:center;">Error al cargar datos: ${e.message}</div>`;
    }
};

window.openCmv201AreaDetails = function(area) {
    window.currentCmv201Area = area;
    document.getElementById('cmv201TableContainer').style.display = 'none';
    document.getElementById('cmv201AreaDetailsContainer').style.display = 'flex';
    document.getElementById('cmv201AreaTitle').innerText = `Detalles del Área: ${area}`;
    
    const select = document.getElementById('cmv201MonthSelect');
    select.innerHTML = '<option value="">Todos los meses</option>';
    window.cmv201MonthsAvailable.forEach(m => {
        const opt = document.createElement('option');
        opt.value = m;
        opt.innerText = m;
        select.appendChild(opt);
    });
    // Select the last month by default
    if (window.cmv201MonthsAvailable.length > 0) {
        select.value = window.cmv201MonthsAvailable[window.cmv201MonthsAvailable.length - 1];
    }
    
    window.loadCmv201AreaDetails();
};

window.backToCmv201Summary = function() {
    document.getElementById('cmv201AreaDetailsContainer').style.display = 'none';
    document.getElementById('cmv201TableContainer').style.display = 'block';
};

window.onCmv201MonthChange = function() {
    window.loadCmv201AreaDetails();
};

window.loadCmv201AreaDetails = async function() {
    const area = window.currentCmv201Area;
    const mes = document.getElementById('cmv201MonthSelect').value;
    const planType = window.currentCmv201PlanType;
    const year = new Date().getFullYear().toString();
    
    const spinner = document.getElementById('cmv201AreaDetailsSpinner');
    const container = document.getElementById('cmv201AreaDetailsTableContainer');
    
    spinner.style.display = 'block';
    container.innerHTML = '';
    
    try {
        let url = `/api/custom/cmv201_area_details?plan_type=${planType}&area=${encodeURIComponent(area)}&year=${year}`;
        if (mes) {
            url += `&mes=${encodeURIComponent(mes)}`;
        }
        
        const res = await fetch(url);
        const data = await res.json();
        spinner.style.display = 'none';
        
        if (!data || data.length === 0) {
            container.innerHTML = '<div style="text-align:center; padding:20px; color:#94a3b8;">No se encontraron materiales para esta selección.</div>';
            return;
        }
        
        let html = '<table class="mini-table" style="width: 100%; border-collapse: collapse;"><thead><tr>';
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: left;">Material</th>`;
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Veces Solicitado</th>`;
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Promedio Retiro</th>`;
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Frecuencia (Días)</th>`;
        html += '</tr></thead><tbody>';
        
        data.forEach(row => {
            html += `<tr style="transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'">`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9;"><span style="color:var(--primario);font-size:0.85rem;">[${row.material}]</span> ${row.texto_breve_material || ''}</td>`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">${row.frecuencia}</td>`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">${row.promedio_retiro}</td>`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">Cada ${row.dias_frecuencia}</td>`;
            html += '</tr>';
        });
        
        html += '</tbody></table>';
        container.innerHTML = html;
        
    } catch (e) {
        spinner.style.display = 'none';
        container.innerHTML = `<div style="color:var(--rojo); padding:20px; text-align:center;">Error al cargar datos: ${e.message}</div>`;
    }
};

// --- Custom Modal CMV 261 ---
window.currentCmv261PlanType = 'planificado';
window.currentCmv261Area = '';
window.cmv261MonthsAvailable = [];

window.openCmv261Modal = function() {
    const modal = document.getElementById('modalCmv261');
    if (!modal) return;
    if (window.openModal) window.openModal('modalCmv261');
    else modal.classList.add('show');
    
    document.getElementById('cmv261AreaDetailsContainer').style.display = 'none';
    document.getElementById('cmv261TableContainer').style.display = 'block';

    // Default to 'planificado' when opening
    window.loadCmv261Data('planificado');
};

window.loadCmv261Data = async function(planType) {
    window.currentCmv261PlanType = planType;
    const btnPlanificado = document.getElementById('btnCmv261Planificado');
    const btnDesplanificado = document.getElementById('btnCmv261Desplanificado');
    
    if (planType === 'planificado') {
        btnPlanificado.className = 'btn btn-primary';
        btnDesplanificado.className = 'btn btn-secondary';
    } else {
        btnPlanificado.className = 'btn btn-secondary';
        btnDesplanificado.className = 'btn btn-primary';
    }

    const spinner = document.getElementById('cmv261Spinner');
    const container = document.getElementById('cmv261TableContainer');
    
    spinner.style.display = 'block';
    container.innerHTML = '';
    
    try {
        const year = new Date().getFullYear().toString();
        const res = await fetch(`/api/custom/cmv261_summary?plan_type=${planType}&year=${year}`);
        const data = await res.json();
        
        spinner.style.display = 'none';
        
        if (!data || data.length === 0) {
            container.innerHTML = '<div style="text-align:center; padding:20px; color:#94a3b8;">No se encontraron datos.</div>';
            return;
        }
        
        const monthsSet = new Set();
        const areasData = {};
        
        data.forEach(row => {
            const area = row.area_negocio || 'Sin Área';
            const mes = row.mes || 'Sin Mes';
            monthsSet.add(mes);
            
            if (!areasData[area]) {
                areasData[area] = {};
            }
            areasData[area][mes] = row.cantidad;
        });
        
        const months = Array.from(monthsSet).sort();
        window.cmv261MonthsAvailable = months;
        
        let html = '<table class="mini-table" style="width: 100%; border-collapse: collapse;"><thead><tr>';
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: left;">Área de Negocio</th>`;
        months.forEach(m => {
            html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">${m}</th>`;
        });
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Total</th>`;
        html += '</tr></thead><tbody>';
        
        for (const [area, mesData] of Object.entries(areasData)) {
            html += `<tr style="transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'">`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; font-weight: bold;"><a href="javascript:void(0)" onclick="window.openCmv261AreaDetails('${area}')" style="color: var(--primary); text-decoration: none; border-bottom: 1px dashed var(--primary); padding-bottom: 2px;">${area}</a></td>`;
            
            let rowTotal = 0;
            months.forEach(m => {
                const val = mesData[m] || 0;
                rowTotal += val;
                html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">${val.toLocaleString('de-DE')}</td>`;
            });
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: var(--primario); text-align: right; font-weight: bold;">${rowTotal.toLocaleString('de-DE')}</td>`;
            html += '</tr>';
        }
        
        html += '</tbody></table>';
        container.innerHTML = html;
        
    } catch (e) {
        spinner.style.display = 'none';
        container.innerHTML = `<div style="color:var(--rojo); padding:20px; text-align:center;">Error al cargar datos: ${e.message}</div>`;
    }
};

window.openCmv261AreaDetails = function(area) {
    window.currentCmv261Area = area;
    document.getElementById('cmv261TableContainer').style.display = 'none';
    document.getElementById('cmv261AreaDetailsContainer').style.display = 'flex';
    document.getElementById('cmv261AreaTitle').innerText = `Detalles del Área: ${area}`;
    
    const select = document.getElementById('cmv261MonthSelect');
    select.innerHTML = '<option value="">Todos los meses</option>';
    window.cmv261MonthsAvailable.forEach(m => {
        const opt = document.createElement('option');
        opt.value = m;
        opt.innerText = m;
        select.appendChild(opt);
    });
    // Select the last month by default
    if (window.cmv261MonthsAvailable.length > 0) {
        select.value = window.cmv261MonthsAvailable[window.cmv261MonthsAvailable.length - 1];
    }
    
    window.loadCmv261AreaDetails();
};

window.backToCmv261Summary = function() {
    document.getElementById('cmv261AreaDetailsContainer').style.display = 'none';
    document.getElementById('cmv261TableContainer').style.display = 'block';
};

window.onCmv261MonthChange = function() {
    window.loadCmv261AreaDetails();
};

window.loadCmv261AreaDetails = async function() {
    const area = window.currentCmv261Area;
    const mes = document.getElementById('cmv261MonthSelect').value;
    const planType = window.currentCmv261PlanType;
    const year = new Date().getFullYear().toString();
    
    const spinner = document.getElementById('cmv261AreaDetailsSpinner');
    const container = document.getElementById('cmv261AreaDetailsTableContainer');
    
    spinner.style.display = 'block';
    container.innerHTML = '';
    
    try {
        let url = `/api/custom/cmv261_area_details?plan_type=${planType}&area=${encodeURIComponent(area)}&year=${year}`;
        if (mes) {
            url += `&mes=${encodeURIComponent(mes)}`;
        }
        
        const res = await fetch(url);
        const data = await res.json();
        spinner.style.display = 'none';
        
        if (!data || data.length === 0) {
            container.innerHTML = '<div style="text-align:center; padding:20px; color:#94a3b8;">No se encontraron materiales para esta selección.</div>';
            return;
        }
        
        let html = '<table class="mini-table" style="width: 100%; border-collapse: collapse;"><thead><tr>';
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: left;">Material</th>`;
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Veces Solicitado</th>`;
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Promedio Retiro</th>`;
        html += `<th style="padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); color: var(--primary); text-align: right;">Frecuencia (Días)</th>`;
        html += '</tr></thead><tbody>';
        
        data.forEach(row => {
            html += `<tr style="transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'">`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9;"><span style="color:var(--primario);font-size:0.85rem;">[${row.material}]</span> ${row.texto_breve_material || ''}</td>`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">${row.frecuencia}</td>`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">${row.promedio_retiro}</td>`;
            html += `<td style="padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; text-align: right;">Cada ${row.dias_frecuencia}</td>`;
            html += '</tr>';
        });
        
        html += '</tbody></table>';
        container.innerHTML = html;
        
    } catch (e) {
        spinner.style.display = 'none';
        container.innerHTML = `<div style="color:var(--rojo); padding:20px; text-align:center;">Error al cargar datos: ${e.message}</div>`;
    }
};
