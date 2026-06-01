
// ─── Modal de Movimientos de Usuario ──────────────────────────────────────────

let currentDailyUsuario = '';
let currentDailyDate = '';

async function abrirDetalleUsuario(usuario) {
    const modal = document.getElementById('modal-user-movements');
    if (!modal) return;
    
    const dp = document.getElementById('productivity-date-picker');
    const date = dp ? dp.value : '';
    if (!date || !usuario) return;

    currentDailyUsuario = usuario;
    currentDailyDate = date;

    modal.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    
    document.getElementById('user-movs-title').textContent = `👤 Detalle Diario: ${usuario}`;
    document.getElementById('user-movs-subtitle').textContent = `Cargando operaciones del ${date}...`;
    
    document.getElementById('daily-level1').classList.remove('is-hidden');
    document.getElementById('daily-level2').classList.remove('is-active');

    const tbody = document.querySelector('#table-daily-level1 tbody');
    tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; padding: 2rem; color: var(--text-muted);">Cargando...</td></tr>';

    try {
        const res = await fetch(`/api/v1/analytics/productivity/user-movements-summary?date=${date}&usuario=${usuario}`);
        if (!res.ok) throw new Error("Error al obtener resumen");
        
        const json = await res.json();
        const data = json.data || [];
        
        document.getElementById('user-movs-subtitle').textContent = `Resumen de Operaciones (${date})`;
        
        tbody.innerHTML = '';
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; padding: 2rem; color: var(--text-muted);">No hay operaciones registradas.</td></tr>';
            return;
        }

        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.style.cursor = 'pointer';
            tr.addEventListener('click', () => cargarNivel2Diario(row.operacion));
            tr.addEventListener('mouseenter', () => tr.style.background = 'rgba(255,255,255,0.05)');
            tr.addEventListener('mouseleave', () => tr.style.background = '');
            
            tr.innerHTML = `
                <td><span style="background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem;">${row.origen}</span></td>
                <td><strong style="color: var(--calipso);">${row.operacion}</strong> <span style="font-size:0.8rem; color:var(--text-muted); float:right;">(Ver detalle 👉)</span></td>
                <td style="text-align: right; font-weight: bold; font-size: 1.1rem;">${row.cantidad || 0}</td>
            `;
            tbody.appendChild(tr);
        });

    } catch (e) {
        console.error(e);
        document.getElementById('user-movs-subtitle').textContent = `Error al cargar.`;
        tbody.innerHTML = `<tr><td colspan="3" style="text-align: center; padding: 2rem; color: #ef4444;">${e.message}</td></tr>`;
    }
}

async function cargarNivel2Diario(operacion) {
    document.getElementById('daily-level1').classList.add('is-hidden');
    document.getElementById('daily-level2').classList.add('is-active');
    
    document.getElementById('daily-level2-title').textContent = `Detalle: ${operacion}`;
    
    const tbody = document.querySelector('#table-user-movements tbody');
    tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 2rem; color: var(--text-muted);">Cargando registros...</td></tr>';

    try {
        const res = await fetch(`/api/v1/analytics/productivity/user-movements-details?date=${currentDailyDate}&usuario=${currentDailyUsuario}&operacion=${encodeURIComponent(operacion)}`);
        if (!res.ok) throw new Error("Error al obtener detalle");
        
        const json = await res.json();
        const data = json.data || [];
        
        tbody.innerHTML = '';
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 2rem; color: var(--text-muted);">No hay detalle disponible.</td></tr>';
            return;
        }

        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td style="color: var(--text-muted);">${row.hora}</td>
                <td><span style="background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem;">${row.origen}</span></td>
                <td><strong style="color: var(--calipso);">${row.operacion}</strong> ${row.cmv !== '-' ? `(CMV ${row.cmv})` : ''}</td>
                <td>${row.material || '-'}</td>
                <td>${row.descripcion || '-'}</td>
                <td style="text-align: right; font-weight: bold;">${row.cantidad || 0}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error(e);
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 2rem; color: #ef4444;">${e.message}</td></tr>`;
    }
}

function volverNivel1Diario() {
    document.getElementById('daily-level2').classList.remove('is-active');
    document.getElementById('daily-level1').classList.remove('is-hidden');
}

function cerrarDetalleUsuario() {
    const modal = document.getElementById('modal-user-movements');
    if (modal) {
        modal.classList.remove('is-open');
        document.body.style.overflow = '';
    }
}

// ─── Modal de Movimientos Mensuales ──────────────────────────────────────────

let currentMonthlyUsuario = '';
let currentMonthlyDate = '';

async function abrirDetalleMensualUsuario(usuario) {
    const modal = document.getElementById('modal-monthly-user-movements');
    if (!modal) return;
    
    const dp = document.getElementById('productivity-month-picker');
    const month = dp ? dp.value : '';
    if (!month || !usuario) return;

    currentMonthlyUsuario = usuario;
    currentMonthlyDate = month;

    modal.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    
    document.getElementById('monthly-user-movs-title').textContent = `👤 Resumen Mensual: ${usuario}`;
    document.getElementById('monthly-user-movs-subtitle').textContent = `Cargando operaciones de ${month}...`;
    
    // Mostrar Nivel 1, ocultar Nivel 2
    document.getElementById('monthly-level1').classList.remove('is-hidden');
    document.getElementById('monthly-level2').classList.remove('is-active');

    const tbody = document.querySelector('#table-monthly-level1 tbody');
    tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; padding: 2rem; color: var(--text-muted);">Cargando...</td></tr>';

    try {
        const res = await fetch(`/api/v1/analytics/productivity/user-movements-monthly-summary?month=${month}&usuario=${usuario}`);
        if (!res.ok) throw new Error("Error al obtener resumen");
        
        const json = await res.json();
        const data = json.data || [];
        
        document.getElementById('monthly-user-movs-subtitle').textContent = `Resumen de Operaciones (${month})`;
        
        tbody.innerHTML = '';
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; padding: 2rem; color: var(--text-muted);">No hay operaciones registradas.</td></tr>';
            return;
        }

        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.style.cursor = 'pointer';
            tr.addEventListener('click', () => cargarNivel2Mensual(row.operacion));
            tr.addEventListener('mouseenter', () => tr.style.background = 'rgba(255,255,255,0.05)');
            tr.addEventListener('mouseleave', () => tr.style.background = '');
            
            tr.innerHTML = `
                <td><span style="background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem;">${row.origen}</span></td>
                <td><strong style="color: var(--calipso);">${row.operacion}</strong> <span style="font-size:0.8rem; color:var(--text-muted); float:right;">(Ver detalle 👉)</span></td>
                <td style="text-align: right; font-weight: bold; font-size: 1.1rem;">${row.cantidad || 0}</td>
            `;
            tbody.appendChild(tr);
        });

    } catch (e) {
        console.error(e);
        document.getElementById('monthly-user-movs-subtitle').textContent = `Error al cargar.`;
        tbody.innerHTML = `<tr><td colspan="3" style="text-align: center; padding: 2rem; color: #ef4444;">${e.message}</td></tr>`;
    }
}

async function cargarNivel2Mensual(operacion) {
    document.getElementById('monthly-level1').classList.add('is-hidden');
    document.getElementById('monthly-level2').classList.add('is-active');
    
    document.getElementById('level2-title').textContent = `Detalle: ${operacion}`;
    
    const tbody = document.querySelector('#table-monthly-level2 tbody');
    tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 2rem; color: var(--text-muted);">Cargando registros...</td></tr>';

    try {
        const res = await fetch(`/api/v1/analytics/productivity/user-movements-monthly-details?month=${currentMonthlyDate}&usuario=${currentMonthlyUsuario}&operacion=${encodeURIComponent(operacion)}`);
        if (!res.ok) throw new Error("Error al obtener detalle");
        
        const json = await res.json();
        const data = json.data || [];
        
        tbody.innerHTML = '';
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 2rem; color: var(--text-muted);">No hay detalle disponible.</td></tr>';
            return;
        }

        data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td style="color: var(--text-muted);">${row.fecha}</td>
                <td style="color: var(--text-muted);">${row.hora}</td>
                <td><span style="background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px; font-size: 0.8rem;">${row.origen}</span></td>
                <td><strong style="color: var(--calipso);">${row.operacion}</strong> ${row.cmv !== '-' ? `(CMV ${row.cmv})` : ''}</td>
                <td>${row.material || '-'}</td>
                <td>${row.descripcion || '-'}</td>
                <td style="text-align: right; font-weight: bold;">${row.cantidad || 0}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error(e);
        tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 2rem; color: #ef4444;">${e.message}</td></tr>`;
    }
}

function volverNivel1Mensual() {
    document.getElementById('monthly-level2').classList.remove('is-active');
    document.getElementById('monthly-level1').classList.remove('is-hidden');
}

function cerrarDetalleMensualUsuario() {
    const modal = document.getElementById('modal-monthly-user-movements');
    if (modal) {
        modal.classList.remove('is-open');
        document.body.style.overflow = '';
    }
}
