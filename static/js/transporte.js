let chartInstance = null;
let allTransporteData = [];
let currentChartGroup = 'mensual';

document.addEventListener("DOMContentLoaded", () => {
    loadData();
});

async function loadData() {
    try {
        const response = await fetch("/api/transporte/data");
        if (!response.ok) throw new Error("Error fetching data");
        const res = await response.json();
        
        allTransporteData = res.data;
        renderChart();
        renderTable(allTransporteData);
        loadPendingData();
    } catch (e) {
        console.error("Error cargando datos de transporte:", e);
    }
}

function getMonday(dateStr) {
    const d = new Date(dateStr);
    const day = d.getDay();
    const diff = d.getDate() - day + (day === 0 ? -6 : 1); 
    d.setDate(diff);
    return d.toISOString().split('T')[0];
}

function updateTransporteChartGroup(group) {
    currentChartGroup = group;
    renderChart();
}

async function loadPendingData() {
    const tbody = document.querySelector('#transportePendingTable tbody');
    const countSpan = document.getElementById('transportePendingCount');
    
    try {
        const response = await fetch('/api/transporte/pending');
        if (!response.ok) throw new Error('Error fetch pending');
        
        const json = await response.json();
        const data = json.data || [];
        
        tbody.innerHTML = '';
        countSpan.textContent = `${data.length} Pendientes`;
        
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 1.5rem; color: #10b981;">¡Todo al día! No hay entregas del año actual sin ingresar. 🎉</td></tr>';
            return;
        }

        // Agrupar por mes y luego por fecha
        const groupedByMonth = {};
        data.forEach(item => {
            const fecha = item.fecha || 'Sin Fecha';
            const mes = fecha.length >= 7 ? fecha.substring(0, 7) : 'Sin Mes';
            
            if (!groupedByMonth[mes]) groupedByMonth[mes] = { total: 0, fechas: {} };
            if (!groupedByMonth[mes].fechas[fecha]) groupedByMonth[mes].fechas[fecha] = [];
            
            groupedByMonth[mes].fechas[fecha].push(item);
            groupedByMonth[mes].total++;
        });

        const sortedMonths = Object.keys(groupedByMonth).sort((a, b) => b.localeCompare(a));
        
        const monthNames = {
            '01': 'Enero', '02': 'Febrero', '03': 'Marzo', '04': 'Abril',
            '05': 'Mayo', '06': 'Junio', '07': 'Julio', '08': 'Agosto',
            '09': 'Septiembre', '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre'
        };

        sortedMonths.forEach((mes, mIndex) => {
            const mesData = groupedByMonth[mes];
            
            let mesNombre = mes;
            if (mes.length === 7) {
                const [y, m] = mes.split('-');
                mesNombre = `${monthNames[m] || m} ${y}`;
            }

            // Month Header
            const monthHeader = document.createElement('tr');
            monthHeader.style.cursor = 'pointer';
            monthHeader.style.background = 'rgba(220, 38, 38, 0.15)';
            monthHeader.style.borderBottom = '1px solid rgba(239, 68, 68, 0.3)';
            
            monthHeader.innerHTML = `
                <td colspan="5" style="padding: 12px; font-weight: bold; color: #f87171; font-size: 1.05rem;">
                    <span style="display: inline-block; width: 20px; transition: transform 0.2s;" id="icon-month-${mIndex}">▶</span>
                    📅 ${mesNombre} <span style="font-size: 0.85rem; color: #fca5a5; margin-left: 10px; background: rgba(220,38,38,0.3); padding: 2px 8px; border-radius: 12px;">${mesData.total} ots pendientes</span>
                </td>
            `;
            tbody.appendChild(monthHeader);

            const sortedFechas = Object.keys(mesData.fechas).sort((a, b) => b.localeCompare(a));
            const allChildRows = [];

            sortedFechas.forEach((fecha, fIndex) => {
                const items = mesData.fechas[fecha];
                
                // Date Header
                const dateHeader = document.createElement('tr');
                dateHeader.style.cursor = 'pointer';
                dateHeader.style.background = 'rgba(239, 68, 68, 0.05)';
                dateHeader.style.borderBottom = '1px solid rgba(239, 68, 68, 0.1)';
                dateHeader.style.display = 'none'; 
                dateHeader.dataset.isDateHeader = "true";
                
                dateHeader.innerHTML = `
                    <td colspan="5" style="padding: 10px 12px 10px 30px; font-weight: bold; color: #fca5a5;">
                        <span style="display: inline-block; width: 20px; transition: transform 0.2s;" id="icon-date-${mIndex}-${fIndex}">▶</span>
                        📆 ${fecha} <span style="font-size: 0.8rem; color: #f87171; margin-left: 10px;">(${items.length} pendientes)</span>
                    </td>
                `;
                tbody.appendChild(dateHeader);
                allChildRows.push(dateHeader);

                // Items
                const itemRows = [];
                items.forEach(item => {
                    const tr = document.createElement('tr');
                    tr.style.display = 'none'; 
                    tr.style.background = 'rgba(0,0,0,0.2)';
                    tr.innerHTML = `
                        <td style="font-weight: 600; color: #f87171; padding-left: 55px;">${item.ot}</td>
                        <td>${item.gd}</td>
                        <td>${item.oc}</td>
                        <td style="text-align: center;">${item.bultos}</td>
                        <td style="text-align: right; color: var(--text-muted);">${item.fecha}</td>
                    `;
                    tbody.appendChild(tr);
                    itemRows.push(tr);
                    allChildRows.push(tr); 
                });

                // Date click
                dateHeader.onclick = (e) => {
                    e.stopPropagation();
                    const icon = document.getElementById(`icon-date-${mIndex}-${fIndex}`);
                    const isHidden = itemRows[0].style.display === 'none';
                    icon.style.transform = isHidden ? 'rotate(90deg)' : 'rotate(0deg)';
                    itemRows.forEach(row => {
                        row.style.display = isHidden ? 'table-row' : 'none';
                    });
                };
            });

            // Month click
            monthHeader.onclick = () => {
                const icon = document.getElementById(`icon-month-${mIndex}`);
                const firstDateHeader = allChildRows.find(r => r.dataset.isDateHeader === "true");
                if (!firstDateHeader) return;
                
                const isHidden = firstDateHeader.style.display === 'none';
                icon.style.transform = isHidden ? 'rotate(90deg)' : 'rotate(0deg)';
                
                if (isHidden) {
                    allChildRows.forEach(row => {
                        if (row.dataset.isDateHeader === "true") {
                            row.style.display = 'table-row';
                        }
                    });
                } else {
                    allChildRows.forEach(row => {
                        row.style.display = 'none';
                        if (row.dataset.isDateHeader === "true") {
                            const dateIcon = row.querySelector('span');
                            if(dateIcon) dateIcon.style.transform = 'rotate(0deg)';
                        }
                    });
                }
            };
        });

    } catch (e) {
        console.error("Error al cargar pendientes:", e);
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 1.5rem; color: #ef4444;">Error al cargar datos pendientes.</td></tr>';
        countSpan.textContent = 'Error';
    }
}

function renderChart() {
    const ctx = document.getElementById('transporteChart').getContext('2d');
    
    if (chartInstance) {
        chartInstance.destroy();
    }

    // Filtrar solo 2025 en adelante para el gráfico
    const chartData = allTransporteData.filter(d => d.fecha >= '2025-01-01');

    // Agrupar los datos
    const groupedData = {};
    chartData.forEach(d => {
        let key = '';
        if (currentChartGroup === 'mensual') {
            key = d.fecha.substring(0, 7); // YYYY-MM
        } else {
            key = getMonday(d.fecha); // YYYY-MM-DD del lunes de la semana
        }
        
        if (!groupedData[key]) {
            groupedData[key] = { entregas: 0, bultos: 0 };
        }
        groupedData[key].entregas += d.total_entregas;
        groupedData[key].bultos += (d.total_bultos || 0);
    });

    // Ordenar las llaves
    const sortedKeys = Object.keys(groupedData).sort();
    
    // Formatear etiquetas
    const labels = sortedKeys.map(k => {
        if (currentChartGroup === 'mensual') {
            const [y, m] = k.split('-');
            const date = new Date(Date.UTC(y, m - 1, 1));
            return date.toLocaleDateString('es-ES', { month: 'short', year: 'numeric' });
        } else {
            return `Semana del ${k}`;
        }
    });
    
    const counts = sortedKeys.map(k => groupedData[k].entregas);
    const bultosCounts = sortedKeys.map(k => groupedData[k].bultos);

    // Registrar el plugin de datalabels globalmente o en la instancia
    Chart.register(ChartDataLabels);

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: currentChartGroup === 'mensual' ? 'Entregas por Mes' : 'Entregas por Semana',
                    data: counts,
                    borderColor: '#5DBAA9',
                    backgroundColor: 'rgba(93, 186, 169, 0.2)',
                    borderWidth: 2,
                    pointBackgroundColor: '#5DBAA9',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#5DBAA9',
                    fill: true,
                    tension: 0.4,
                    yAxisID: 'y'
                },
                {
                    label: currentChartGroup === 'mensual' ? 'Bultos por Mes' : 'Bultos por Semana',
                    data: bultosCounts,
                    borderColor: '#EA7600',
                    backgroundColor: 'rgba(234, 118, 0, 0.1)',
                    borderWidth: 2,
                    pointBackgroundColor: '#EA7600',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#EA7600',
                    fill: true,
                    tension: 0.4,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#e2e8f0' }
                },
                datalabels: {
                    color: '#ffffff',
                    backgroundColor: 'rgba(0,0,0,0.6)',
                    borderRadius: 4,
                    font: {
                        weight: 'bold',
                        size: 11
                    },
                    padding: 4,
                    align: 'top',
                    offset: 5,
                    formatter: Math.round
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    beginAtZero: true,
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: '#5DBAA9' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    beginAtZero: true,
                    grid: { drawOnChartArea: false },
                    ticks: { color: '#EA7600' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' }
                }
            }
        }
    });
}

function renderTable(data) {
    const tbody = document.querySelector("#transporteTable tbody");
    tbody.innerHTML = "";

    if (data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color: #94a3b8;">No hay datos de transporte. Ejecuta la sincronización global desde el panel de control.</td></tr>`;
        return;
    }

    // Mostrar solo los últimos 25 para la tabla como se solicitó
    const latestData = [...data].reverse().slice(0, 25);

    latestData.forEach(row => {
        const tr = document.createElement("tr");
        
        let pdfBtn = `<span style="color: #94a3b8;">No disponible</span>`;
        if (row.has_pdf) {
            pdfBtn = `<button onclick="openPdfViewer('/api/transporte/pdf/${row.pdf_filename}')" class="btn btn-small" style="background: rgba(93, 186, 169, 0.1); color: #5DBAA9; border: none; padding: 4px 12px; border-radius: 4px; font-weight: 600; cursor: pointer;">Ver PDF</button>`;
        }

        tr.innerHTML = `
            <td><strong>${row.fecha}</strong></td>
            <td style="text-align: center;">${row.total_entregas}</td>
            <td style="text-align: center; color: var(--naranja); font-weight: bold;">${row.total_bultos || 0}</td>
            <td style="text-align: right;">${pdfBtn}</td>
        `;
        tbody.appendChild(tr);
    });
}

function openPdfViewer(url) {
    const modal = document.getElementById('modalPdfViewer');
    const iframe = document.getElementById('pdfIframe');
    if (modal && iframe) {
        iframe.src = url;
        modal.classList.add('active');
    }
}

function closePdfViewer() {
    const modal = document.getElementById('modalPdfViewer');
    const iframe = document.getElementById('pdfIframe');
    if (modal && iframe) {
        modal.classList.remove('active');
        iframe.src = ""; // Stop loading or viewing the PDF when closed
    }
}

let transporteSearchTimeout = null;

async function searchTransporte() {
    const input = document.getElementById('transporteSearchInput').value.trim();
    const loading = document.getElementById('transporteSearchLoading');
    const table = document.getElementById('transporteSearchTable');
    const tbody = table.querySelector('tbody');
    const noResults = document.getElementById('transporteSearchNoResults');

    if (input.length < 3) {
        table.style.display = 'none';
        noResults.style.display = 'none';
        return;
    }

    if (transporteSearchTimeout) {
        clearTimeout(transporteSearchTimeout);
    }

    loading.style.display = 'inline-block';

    transporteSearchTimeout = setTimeout(async () => {
        try {
            const res = await fetch(`/api/transporte/search?q=${encodeURIComponent(input)}`);
            const json = await res.json();

            tbody.innerHTML = '';

            if (!res.ok || !json.data || json.data.length === 0) {
                table.style.display = 'none';
                noResults.style.display = 'block';
            } else {
                noResults.style.display = 'none';
                table.style.display = 'table';

                json.data.forEach(item => {
                    const tr = document.createElement('tr');
                    tr.className = 'row';
                    tr.innerHTML = `
                        <td>${item.fecha}</td>
                        <td style="font-weight: 600; color: var(--calipso);">${item.ot}</td>
                        <td>${item.gd}</td>
                        <td>${item.oc}</td>
                        <td>${item.proveedor}</td>
                        <td style="text-align: center; color: var(--naranja); font-weight: bold;">${item.bultos}</td>
                    `;
                    tbody.appendChild(tr);
                });
            }
        } catch (e) {
            console.error("Error searching transporte", e);
        } finally {
            loading.style.display = 'none';
        }
    }, 400); // 400ms debounce
}
