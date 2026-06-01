    function renderPreviewChart(payload) {
        let data = payload;
        if (payload && !Array.isArray(payload) && payload.raw_data) {
            data = payload.raw_data;
        }
        
        const canvas = document.getElementById('studioPreviewChart');
        const tableContainer = document.getElementById('studioTableContainer');
        const trellisContainer = document.getElementById('studioTrellisContainer');
        const tableControls = document.getElementById('studioTableControls');

        // Reset
        canvas.style.display = 'none';
        tableContainer.style.display = 'none';
        trellisContainer.style.display = 'none';
        trellisContainer.innerHTML = '';
        tableControls.style.display = 'none';
        if (studioChartInstance) { studioChartInstance.destroy(); studioChartInstance = null; }

        if (!data || data.length === 0 || !window.Chart) {
            tableContainer.innerHTML = '<div style="text-align:center;padding:50px;color:#64748b;"><i class="fas fa-inbox" style="font-size:2rem;display:block;margin-bottom:12px;"></i>No hay datos para mostrar</div>';
            tableContainer.style.display = 'block';
            return;
        }

        let chartType = document.getElementById('studioChartType').value;
        const primaryColor = document.getElementById('studioPrimaryColor').value;
        const keys = Object.keys(data[0]);
        const isPercent = !!(visualState && visualState.metric && visualState.metric.format === 'percent');
        const PALETTE = ['#22c55e','#3b82f6','#f59e0b','#ef4444','#8b5cf6','#06b6d4','#ec4899','#5DBAA9','#EA7600'];

        // Si la consulta devuelve una sola columna (ej. COUNT puro), forzar KPI si no es tabla
        if (keys.length === 1 && chartType !== 'table') {
            chartType = 'kpi';
        }

        // ─── TABLE ─────────────────────────────────────────────────────────────
        if (chartType === 'table') {
            tableControls.style.display = 'block';
            tableContainer.style.display = 'block';
            let html = '<table class="mini-table"><thead><tr>' + keys.map(k => `<th>${k}</th>`).join('') + '</tr></thead><tbody>';
            html += data.map(row => '<tr>' + keys.map(k => `<td>${row[k]}</td>`).join('') + '</tr>').join('');
            html += '</tbody></table>';
            tableContainer.innerHTML = html;
            return;
        }

        if (chartType === 'kpi') {
            tableContainer.style.display = 'block';
            const kpiRow = data[data.length - 1]; // Tomar el registro más reciente para visualizar el periodo activo!
            const kpiKey = keys.find(k => k === 'valor') || keys.find(k => typeof kpiRow[k] === 'number') || keys[keys.length - 1];
            const kpiValue = kpiRow[kpiKey];
            
            // Determinar si hay un periodo temporal (ej: 'fecha') o categoría en las otras columnas para dar contexto
            let subtitle = "";
            const otherKeys = keys.filter(k => k !== kpiKey);
            if (otherKeys.length > 0) {
                subtitle = otherKeys.map(k => `${k}: <strong style="color: #fff;">${kpiRow[k]}</strong>`).join(' | ');
            }
            
            const isPercent = (visualState && visualState.metric && visualState.metric.format === 'percent');
            const formattedVal = (typeof kpiValue === 'number' ? kpiValue.toLocaleString() : kpiValue) + (isPercent ? '%' : '');
            
            tableContainer.innerHTML = `
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 270px; background: radial-gradient(circle, rgba(93, 186, 169, 0.08) 0%, rgba(7, 10, 19, 0.4) 100%); border: 2px dashed rgba(93, 186, 169, 0.3); border-radius: 16px; padding: 30px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);">
                    <div style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; color: #94a3b8; margin-bottom: 12px; font-weight: 600;">${kpiKey}</div>
                    <div style="font-size: 4.8rem; font-weight: 800; color: ${primaryColor}; text-shadow: 0 0 25px ${primaryColor}66; line-height: 1; font-family: 'Outfit', sans-serif;">${formattedVal}</div>
                    ${subtitle ? `<div style="font-size: 0.85rem; color: #94a3b8; margin-top: 15px; background: rgba(255,255,255,0.03); padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">${subtitle}</div>` : ''}
                    <div style="font-size: 0.8rem; color: #64748b; margin-top: 20px; text-align: center;"><i class="fas fa-info-circle" style="color: var(--primary);"></i> Tarjeta de Métrica KPI compilada en tiempo real</div>
                </div>
            `;
            return;
        }

        canvas.style.display = 'block';
        
        // Lógica de Desglose/Series múltiples
        // Si hay una columna llamada 'categoria' y 'fecha' en los resultados
        const hasCategory = keys.includes('categoria') && keys.includes('fecha') && keys.includes('valor');
        
        let labels = [];
        let datasets = [];

        if (hasCategory) {
            // Agrupar datos por categoría
            labels = [...new Set(data.map(row => row.fecha || 'N/A'))].sort();
            const categories = [...new Set(data.map(row => row.categoria || 'Total'))];
            
            categories.forEach((cat, idx) => {
                const catData = labels.map(lbl => {
                    const found = data.find(row => row.fecha === lbl && row.categoria === cat);
                    return found ? found.valor : 0;
                });
                
                const colors = ['#5DBAA9', '#ff9f43', '#54a0ff', '#5f27cd', '#ff6b6b', '#10ac84'];
                const color = colors[idx % colors.length];

                datasets.push({
                    label: cat,
                    data: catData,
                    backgroundColor: color + '33',
                    borderColor: color,
                    borderWidth: 2,
                    tension: 0.4,
                    fill: false
                });
            });
        } else {
            labels = data.map(row => row[keys[0]] || 'N/A');
            const colors = ['#5DBAA9', '#ff9f43', '#54a0ff', '#5f27cd', '#ff6b6b', '#10ac84'];
            let colorIdx = 0;
            for (let i = 1; i < keys.length; i++) {
                const key = keys[i];
                if (typeof data[0][key] === 'number') {
                    const color = colorIdx === 0 ? primaryColor : colors[colorIdx % colors.length];
                    const isSecondary = colorIdx > 0;
                    colorIdx++;
                    datasets.push({
                        label: key,
                        data: data.map(row => row[key]),
                        backgroundColor: color + '33',
                        borderColor: color,
                        borderWidth: isSecondary ? 2 : 3,
                        borderDash: isSecondary ? [5, 5] : [],
                        tension: 0.4,
                        fill: isSecondary ? false : (chartType === 'line' ? true : false),
                        yAxisID: isSecondary ? 'y1' : 'y'
                    });
                }
            }
        }
        
        if (studioChartInstance) studioChartInstance.destroy();
        const ctx = canvas.getContext('2d');

        // Determinar si se necesita eje Y secundario
        const hasSecondAxis = datasets.length > 1 && datasets[1] && datasets[1].yAxisID === 'y1';
        const isHorizontal = chartType === 'horizontalBar';
        const scalesConfig = chartType === 'pie' ? {} : {
            x: { grid: { display: false }, ticks: { color: '#64748b' } },
            y: {
                beginAtZero: true,
                position: 'left',
                grid: { color: 'rgba(255,255,255,0.05)' },
                ticks: { color: '#94a3b8' }
            },
            ...(hasSecondAxis ? {
                y1: {
                    beginAtZero: true,
                    position: 'right',
                    grid: { drawOnChartArea: false },
                    ticks: { color: '#64748b' }
                }
            } : {})
        };

        studioChartInstance = new Chart(ctx, {
            type: chartType === 'pie' ? 'pie' : (chartType === 'line' ? 'line' : 'bar'), 
            data: { labels, datasets },
            options: { 
                indexAxis: isHorizontal ? 'y' : 'x',
                responsive: true, 
                maintainAspectRatio: false, 
                plugins: { 
                    legend: { display: true, labels: { color: '#94a3b8', font: { size: 10 } } }
                },
                scales: scalesConfig
            }
        });
    }
