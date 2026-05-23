(() => {
    /**
     * MonitorWeb — Movimientos Analytics Logic
     * Requiere: core_ui.js cargado previamente (provee window.CoreUI)
     */

    const log = (msg, data = null) => {
        console.log(`[Inventory-JS] ${msg}`, data || '');
    };

    // ── UI HELPERS — delegados a CoreUI ─────────────────────────────────
    // CoreUI provee openModal, closeModal, renderMaterialModal y getData.
    // Se crean alias locales para mantener la misma interfaz de llamada
    // que el resto del módulo usaba.

    const UI = {
        openModal: (id) => CoreUI.openModal(id),
        closeModal: (id) => CoreUI.closeModal(id),
        renderMaterialModal: (opts) => CoreUI.renderMaterialModal(opts)
    };

    const getData = (id) => CoreUI.getData(id);

    const parseFormattedInt = (val) => {
        if (val === null || val === undefined) return 0;
        let s = val.toString().replace(/[^\d]/g, ''); // Remove everything except digits
        return parseInt(s) || 0;
    };

    // ── MODAL HANDLERS ──────────────────────────────────────────────────────

    window.openModalUbicacion = (name) => {
        const data = getData('data_ubic_mapping_inv') || {};
        UI.renderMaterialModal({ modalId: 'modalUbicacion', titleId: 'modalUbicacionTitle', listId: 'modalUbicacionList', title: `Ubicación: ${name}`, items: data[name] || [], colorVar: '--calipso' });
    };
    window.openModalUserInv = (name) => {
        const data = getData('data_user_mapping_inv') || {};
        UI.renderMaterialModal({ modalId: 'modalUser', titleId: 'modalUserTitle', listId: 'modalUserList', title: `Usuario: ${name}`, items: data[name] || [], colorVar: '--naranja', bgColor: 'rgba(234,118,0,0.1)' });
    };

    // ── CHARTS INITIALIZATION ──────────────────────────────────────────────

    document.addEventListener('DOMContentLoaded', () => {
        log('Initializing Inventory charts...');
        try {
            Chart.defaults.color = '#94a3b8';
            Chart.defaults.font.family = "'Outfit', sans-serif";
            if (typeof ChartDataLabels !== 'undefined') {
                Chart.register(ChartDataLabels);
            }
        } catch (e) { log('Error registering ChartDataLabels', e); }

        const doughnutOptions = {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { color: "#e2e8f0", padding: 20 } },
                datalabels: { color: '#fff', font: { weight: 'bold' }, formatter: v => v > 0 ? v : "" }
            }
        };

        // 1. ABC Chart
        try {
            const abcData = getData('data_abc') || {};
            const ctxABC = document.getElementById('abcPieChart');
            if (ctxABC) {
                new Chart(ctxABC, {
                    type: 'doughnut',
                    data: {
                        labels: ['A (80%)', 'B (15%)', 'C (5%)'],
                        datasets: [{ data: [abcData.A || 0, abcData.B || 0, abcData.C || 0], backgroundColor: ['#5DBAA9', '#EA7600', '#B46A5F'], borderWidth: 0 }]
                    },
                    options: doughnutOptions
                });
                log('ABC Chart rendered');
            }
        } catch (e) { log('Error rendering ABC Chart', e); }

        // 2. PM Chart
        try {
            const p201 = parseFormattedInt(getData('data_kpi_201_planned'));
            const u201 = parseFormattedInt(getData('data_kpi_201_unplanned'));
            const p261 = parseFormattedInt(getData('data_kpi_261_planned'));
            const u261 = parseFormattedInt(getData('data_kpi_261_unplanned'));

            const desplanificadoTotal = u201 + u261;

            const ctxPM = document.getElementById('pmDoughnutChart');
            if (ctxPM && (p201 > 0 || desplanificadoTotal > 0 || p261 > 0)) {
                new Chart(ctxPM, {
                    type: 'doughnut',
                    data: {
                        labels: ['Producción Planificada', 'Desplanificado', 'Mantención Planificada'],
                        datasets: [{ data: [p201, desplanificadoTotal, p261], backgroundColor: ['#5DBAA9', '#EA7600', '#64748b'], borderWidth: 0 }]
                    },
                    options: {
                        ...doughnutOptions,
                        plugins: {
                            ...doughnutOptions.plugins,
                            datalabels: {
                                formatter: (val, ctx) => {
                                    const total = ctx.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                                    return ((val * 100) / (total || 1)).toFixed(1) + '%';
                                },
                                color: '#fff', font: { weight: 'bold' }
                            }
                        }
                    }
                });
                log('PM Chart rendered');
            }
        } catch (e) { log('Error rendering PM Chart', e); }

        // 3. Planned vs Unplanned Trend Chart
        try {
            const pLabels = getData('data_planned_labels') || [];
            const pData = getData('data_planned_data') || [];
            const uData = getData('data_unplanned_data') || [];
            const ctxPlanned = document.getElementById('plannedTrendChart');

            if (ctxPlanned && pLabels.length > 0) {
                window.invPlannedTrendChart = new Chart(ctxPlanned, {
                    type: 'line',
                    data: {
                        labels: pLabels,
                        datasets: [
                            {
                                label: 'Consumos Planificados',
                                data: pData,
                                borderColor: '#5DBAA9',
                                backgroundColor: 'rgba(93, 186, 169, 0.1)',
                                borderWidth: 3,
                                tension: 0.3,
                                fill: true
                            },
                            {
                                label: 'Consumos Desplanificados',
                                data: uData,
                                borderColor: '#EA7600',
                                backgroundColor: 'rgba(234, 118, 0, 0.1)',
                                borderWidth: 3,
                                tension: 0.3,
                                fill: true
                            }
                        ]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        plugins: {
                            legend: { position: 'top', labels: { color: "#e2e8f0" } },
                            datalabels: {
                                display: true,
                                color: '#cbd5e1',
                                font: { weight: '600', size: 10 },
                                align: 'top',
                                formatter: v => v > 0 ? v : ""
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: { color: 'rgba(255,255,255,0.05)' }
                            },
                            x: { grid: { display: false } }
                        }
                    }
                });
                log('Planned Trend Chart rendered');
            }
        } catch (e) { log('Error rendering Planned Trend Chart', e); }

        // 4. DOW Chart
        try {
            const dowData = getData('data_dow') || [];
            const ctxDOW = document.getElementById('dowChart');
            if (ctxDOW && dowData.length > 0) {
                new Chart(ctxDOW, {
                    type: 'bar',
                    data: {
                        labels: ['Lun', 'Mar', 'Mie', 'Jue', 'Vie'],
                        datasets: [{ data: dowData.slice(0, 5), backgroundColor: 'rgba(243, 208, 28, 0.7)', borderRadius: 4 }]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        plugins: { legend: { display: false }, datalabels: { anchor: 'end', align: 'top' } },
                        scales: { y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } }, x: { grid: { display: false } } }
                    }
                });
                log('DOW Chart rendered');
            }
        } catch (e) { log('Error rendering DOW Chart', e); }

        // 5. Trend Chart
        try {
            const labels = getData('data_trend_labels');
            const ctxTrend = document.getElementById('trendChart');
            if (ctxTrend && labels && labels.length > 0) {
                window.invTrendChart = new Chart(ctxTrend, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [
                            { label: 'Abastecimiento', data: getData('data_trend_entradas'), borderColor: '#5DBAA9', tension: 0.3, fill: false },
                            { label: 'Producción', data: getData('data_trend_salidas_prod'), borderColor: '#EA7600', tension: 0.3, fill: false },
                            { label: 'Mantención', data: getData('data_trend_salidas_mant'), borderColor: '#64748b', borderDash: [5, 5], tension: 0.3, fill: false }
                        ]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        plugins: { legend: { position: 'top' }, datalabels: { display: true, color: '#cbd5e1', font: { weight: '600', size: 10 }, align: 'top', formatter: v => v > 0 ? v : "" } },
                        scales: { y: { grid: { color: 'rgba(255,255,255,0.05)' } }, x: { grid: { display: false } } }
                    }
                });
                log('Trend Chart rendered');
            }
        } catch (e) { log('Error rendering Trend Chart', e); }
        
        // Buscador de ubicaciones dinámico — dos tablas separadas
        const ubicInput = document.getElementById('ubic-search-input');
        const ubicResults = document.getElementById('ubic-results-body');
        const ubicStockBody = document.getElementById('ubic-stock-body');
        const ubicDesc = document.getElementById('ubic-material-desc');
        let ubicTimer;

        if (ubicInput) {
            ubicInput.addEventListener('input', (e) => {
                clearTimeout(ubicTimer);
                const val = e.target.value.trim();

                const loadingHistorial = `<tr><td colspan="2" style="text-align:center;color:#38bdf8;padding:1.5rem;"><i class="fas fa-spinner fa-spin"></i> Buscando...</td></tr>`;
                const loadingStock    = `<tr><td colspan="3" style="text-align:center;color:#38bdf8;padding:1.5rem;"><i class="fas fa-spinner fa-spin"></i> Buscando...</td></tr>`;

                if (val.length < 3) {
                    if (ubicResults)   ubicResults.innerHTML   = `<tr><td colspan="2" style="text-align:center;color:#94a3b8;padding:1.5rem;">Digita al menos 3 caracteres...</td></tr>`;
                    if (ubicStockBody) ubicStockBody.innerHTML = `<tr><td colspan="3" style="text-align:center;color:#94a3b8;padding:1.5rem;">Digita al menos 3 caracteres...</td></tr>`;
                    if (ubicDesc) ubicDesc.innerText = '';
                    return;
                }

                if (ubicResults)   ubicResults.innerHTML   = loadingHistorial;
                if (ubicStockBody) ubicStockBody.innerHTML = loadingStock;
                if (ubicDesc) ubicDesc.innerText = '';

                ubicTimer = setTimeout(async () => {
                    try {
                        const response = await fetch(`/api/ubicaciones/${encodeURIComponent(val)}`);
                        if (!response.ok) throw new Error('Network error');
                        const data = await response.json();

                        if (data.length === 0) {
                            if (ubicResults)   ubicResults.innerHTML   = `<tr><td colspan="2" style="text-align:center;color:#ef4444;padding:1.5rem;">Sin resultados para "${val}"</td></tr>`;
                            if (ubicStockBody) ubicStockBody.innerHTML = `<tr><td colspan="3" style="text-align:center;color:#ef4444;padding:1.5rem;">Sin stock registrado para "${val}"</td></tr>`;
                            return;
                        }

                        // Descripción del material
                        if (ubicDesc) {
                            const matDesc = data[0].texto_breve_material || '';
                            ubicDesc.innerText = matDesc ? `🏷️ ${matDesc}` : '';
                        }

                        // ── Tabla 1: Stock Actual (solo filas con stock real) ──
                        const stockRows = data.filter(r => r.stock_disp !== null && r.stock_disp !== undefined);
                        if (ubicStockBody) {
                            if (stockRows.length === 0) {
                                ubicStockBody.innerHTML = `<tr><td colspan="3" style="text-align:center;color:#94a3b8;padding:1.5rem;">Sin stock actual registrado</td></tr>`;
                            } else {
                                ubicStockBody.innerHTML = stockRows.map(r => {
                                    const cant    = Number(r.stock_disp).toLocaleString('es-CL');
                                    const um      = r.umb || '-';
                                    const ubicAct = r.ubic_actual || '-';
                                    return `
                                        <tr>
                                            <td style="font-weight:600;color:#EA7600;">${ubicAct}</td>
                                            <td style="color:#5DBAA9;font-weight:600;">${cant}</td>
                                            <td style="color:#cbd5e1;">${um}</td>
                                        </tr>`;
                                }).join('');
                            }
                        }

                        // ── Tabla 2: Historial de Ubicaciones (todas las filas con ubicación) ──
                        if (ubicResults) {
                            const histRows = data.filter(r => r.ubic_dest);
                            if (histRows.length === 0) {
                                ubicResults.innerHTML = `<tr><td colspan="2" style="text-align:center;color:#94a3b8;padding:1.5rem;">Sin historial registrado</td></tr>`;
                            } else {
                                ubicResults.innerHTML = histRows.map(r => {
                                    const fechaFmt = r.fecha || '-';
                                    return `
                                        <tr>
                                            <td style="font-weight:600;color:#e2e8f0;">${r.ubic_dest}</td>
                                            <td style="color:#94a3b8;">${fechaFmt}</td>
                                        </tr>`;
                                }).join('');
                            }
                        }

                    } catch (error) {
                        if (ubicResults)   ubicResults.innerHTML   = `<tr><td colspan="2" style="text-align:center;color:#ef4444;padding:1.5rem;">Error de conexión.</td></tr>`;
                        if (ubicStockBody) ubicStockBody.innerHTML = `<tr><td colspan="3" style="text-align:center;color:#ef4444;padding:1.5rem;">Error de conexión.</td></tr>`;
                        log('Error fetching ubicaciones', error);
                    }
                }, 500);
            });
        }
    });

})();

window.switchInventarioView = (view) => {
    const getData = (id) => {
        const el = document.getElementById(id);
        return el ? JSON.parse(el.textContent) : null;
    };

    if (window.invPlannedTrendChart) {
        if (view === 'historical') {
            window.invPlannedTrendChart.data.labels = getData('data_planned_labels_weekly') || [];
            window.invPlannedTrendChart.data.datasets[0].data = getData('data_planned_data_weekly') || [];
            window.invPlannedTrendChart.data.datasets[1].data = getData('data_unplanned_data_weekly') || [];
        } else {
            window.invPlannedTrendChart.data.labels = getData('data_planned_labels') || [];
            window.invPlannedTrendChart.data.datasets[0].data = getData('data_planned_data') || [];
            window.invPlannedTrendChart.data.datasets[1].data = getData('data_unplanned_data') || [];
        }
        window.invPlannedTrendChart.update();
    }

    if (window.invTrendChart) {
        if (view === 'historical') {
            window.invTrendChart.data.labels = getData('data_trend_labels_weekly') || [];
            window.invTrendChart.data.datasets[0].data = getData('data_trend_entradas_weekly') || [];
            window.invTrendChart.data.datasets[1].data = getData('data_trend_salidas_prod_weekly') || [];
            window.invTrendChart.data.datasets[2].data = getData('data_trend_salidas_mant_weekly') || [];
        } else {
            window.invTrendChart.data.labels = getData('data_trend_labels') || [];
            window.invTrendChart.data.datasets[0].data = getData('data_trend_entradas') || [];
            window.invTrendChart.data.datasets[1].data = getData('data_trend_salidas_prod') || [];
            window.invTrendChart.data.datasets[2].data = getData('data_trend_salidas_mant') || [];
        }
        window.invTrendChart.update();
    }
};

window.toggleMultiInv = (id) => {
    const el = document.getElementById(id);
    if (el) el.style.display = el.style.display === 'none' ? 'block' : 'none';
};

window.toggleAllInvAreas = (checkbox) => {
    const boxes = document.querySelectorAll('.inv-chart-area-cb');
    boxes.forEach(b => b.checked = checkbox.checked);
    if (!checkbox.checked) {
        setTimeout(() => {
            checkbox.checked = true;
            boxes.forEach(b => b.checked = true);
            window.updateInventoryAnalytics();
        }, 100);
    } else {
        window.updateInventoryAnalytics();
    }
};

window.updateInventoryAnalytics = () => {
    const selected = Array.from(document.querySelectorAll('.inv-chart-area-cb:checked')).map(cb => cb.value);
    
    // Si desmarcan todo, forzar a seleccionar todo para no romper la vista
    if (selected.length === 0) {
        document.querySelectorAll('.inv-chart-area-cb').forEach(b => b.checked = true);
        const selAll = document.getElementById('invSelectAllAreas');
        if (selAll) selAll.checked = true;
        return window.updateInventoryAnalytics();
    } else {
        const boxes = document.querySelectorAll('.inv-chart-area-cb');
        const selAll = document.getElementById('invSelectAllAreas');
        if (selAll) selAll.checked = (selected.length === boxes.length);
    }

    // 1. Recalcular KPI Consumo Producción (201)
    const areaStatsJsonStr = document.getElementById('data_inv_area_stats_json');
    if (areaStatsJsonStr && areaStatsJsonStr.textContent) {
        try {
            const areaStats = JSON.parse(areaStatsJsonStr.textContent);
            let totalConsumo = 0;
            areaStats.forEach(s => {
                if (selected.includes(s.area)) {
                    totalConsumo += (s.count_val || 0);
                }
            });
            
            // Actualizar KPI en el DOM
            const kpiCards = document.querySelectorAll('.stat-card');
            kpiCards.forEach(card => {
                const title = card.querySelector('h3');
                if (title && title.textContent.includes('Consumo Producción (201)')) {
                    const valEl = card.querySelector('.value');
                    if (valEl) {
                        valEl.innerText = totalConsumo.toLocaleString('de-DE');
                    }
                }
            });
        } catch (e) {}
    }

    // 2. Filtrar listas (Top Consumidos y Top Usuarios)
    document.querySelectorAll('.rank-list li[data-area]').forEach(li => {
        const area = li.getAttribute('data-area');
        const show = selected.includes(area) || area === 'MIXTO';
        li.style.display = show ? '' : 'none';
    });
};

document.addEventListener('click', (e) => {
    if (!e.target.closest('.multiselect')) {
        const boxes = document.getElementById('invAreaCheckboxes');
        if (boxes) boxes.style.display = 'none';
    }
});