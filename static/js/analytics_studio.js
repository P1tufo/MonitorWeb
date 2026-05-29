    // Scope modular para evitar fugas de estado entre widgets
    const AnalyticsStudioManager = {
        instances: {},
        getVisualState(queryId) {
            if (!this.instances[queryId]) {
                this.instances[queryId] = {
                    baseTable: '', joins: [], filters: [],
                    metric: { column: '', aggregation: 'COUNT' },
                    timeAxis: { column: '', granularity: 'MONTH' },
                    breakdown: '', secondMetric: null
                };
            }
            return this.instances[queryId];
        },
        setVisualState(queryId, state) {
            this.instances[queryId] = state;
        }
    };

    let studioChartInstance = null;
    let currentSchema = {};
    let currentQueryId = "";
    let serverVisualState = null;
    let visualState = null; // Puntero al estado activo del modal

    // Mapeos predefinidos para inicialización visual intuitiva de todos los gráficos del sistema
    const defaultVisualStates = {
        'ots_daily_trend': {
            baseTable: 'tareas',
            joins: [],
            filters: [],
            metric: { column: 'met_tareas', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha_creac', granularity: 'DAY' },
            breakdown: '',
            chartType: 'line'
        },
        'ots_by_movement_type': {
            baseTable: 'tareas',
            joins: [],
            filters: [{ column: 'dim_clase_mov', operator: 'isnotnull', value: '' }],
            metric: { column: 'met_tareas', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha_creac', granularity: 'MONTH' },
            breakdown: 'dim_clase_mov',
            chartType: 'pie'
        },
        'ots_by_user_dual': {
            baseTable: 'tareas',
            joins: [],
            filters: [],
            metric: { column: 'met_tareas', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha_creac', granularity: 'MONTH' },
            breakdown: 'dim_usuario',
            chartType: 'bar'
        },
        'inv_volumen_stats': {
            baseTable: 'movimientos',
            joins: [],
            filters: [],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha_contab', granularity: 'DAY' },
            breakdown: 'dim_tipo_operacion',
            chartType: 'bar'
        },
        'inv_consumos_quick': {
            baseTable: 'movimientos',
            joins: [],
            filters: [{ column: 'met_movimientos', operator: 'isnotnull', value: '' }],
            metric: { column: 'met_cantidad', aggregation: 'SUM' },
            timeAxis: { column: 'dim_fecha_contab', granularity: 'MONTH' },
            breakdown: 'dim_texto_breve',
            chartType: 'bar'
        },
        'vl_monthly_evolution': {
            baseTable: 'entregas',
            joins: [],
            filters: [],
            metric: { column: 'met_entregas', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: '',
            chartType: 'line'
        },
        'vl_weekly_evolution': {
            baseTable: 'entregas',
            joins: [],
            filters: [],
            metric: { column: 'met_entregas', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha', granularity: 'WEEK' },
            breakdown: '',
            chartType: 'line'
        },
        'vl_top_locations': {
            baseTable: 'entregas',
            joins: [],
            filters: [],
            metric: { column: 'met_entregas', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: 'dim_ubic_bin',
            chartType: 'bar'
        },
        'inv_area_stats_prod': {
            baseTable: 'movimientos',
            joins: [],
            filters: [],
            metric: { column: 'met_cantidad', aggregation: 'SUM' },
            timeAxis: { column: 'dim_fecha_contab', granularity: 'MONTH' },
            breakdown: 'dim_ce_coste',
            chartType: 'bar'
        },
        'inv_consumos_abc': {
            baseTable: 'movimientos',
            joins: [],
            filters: [],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha_contab', granularity: 'MONTH' },
            breakdown: 'dim_texto_breve',
            chartType: 'bar'
        },
        'inv_dow_stats': {
            baseTable: 'movimientos',
            joins: [],
            filters: [],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha_contab', granularity: 'DAY' },
            breakdown: '',
            chartType: 'line'
        },
        'inv_pm_type_records': {
            baseTable: 'movimientos',
            joins: [],
            filters: [],
            metric: { column: 'met_cantidad', aggregation: 'SUM' },
            timeAxis: { column: 'dim_fecha_contab', granularity: 'MONTH' },
            breakdown: 'dim_tipo_operacion',
            chartType: 'bar'
        },
        'inv_location_summary': {
            baseTable: 'movimientos',
            joins: [],
            filters: [],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha_contab', granularity: 'MONTH' },
            breakdown: 'dim_alm',
            chartType: 'bar'
        },
        'inv_top_users': {
            baseTable: 'movimientos',
            joins: [],
            filters: [],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha_contab', granularity: 'MONTH' },
            breakdown: 'dim_usuario',
            chartType: 'bar'
        },
        'vl_sla_monthly_trend': {
            baseTable: 'entregas',
            joins: [],
            filters: [{ column: 'dim_fecha', operator: 'contains', value: '2026' }],
            metric: { column: 'met_sla_efficiency', aggregation: 'SLA_EFFICIENCY', format: 'percent' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: '',
            secondMetric: { column: 'met_entregas', aggregation: 'COUNT_DISTINCT', label: 'Materiales Solicitados' },
            chartType: 'line'
        },
        'vl_sla_area_monthly_trend': {
            baseTable: 'entregas',
            joins: [],
            filters: [{ column: 'dim_fecha', operator: 'contains', value: '2026' }],
            metric: { column: 'met_sla_efficiency', aggregation: 'SLA_EFFICIENCY', format: 'percent' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: 'dim_area',
            secondMetric: { column: 'met_entregas', aggregation: 'COUNT', label: 'Materiales_Solicitados' },
            chartType: 'line'
        },
        'vl_sla_trend': {
            baseTable: 'entregas',
            joins: [],
            filters: [{ column: 'dim_fecha', operator: 'contains', value: '2026' }],
            metric: { column: 'met_sla_efficiency', aggregation: 'SLA_EFFICIENCY', format: 'percent' },
            timeAxis: { column: 'dim_fecha', granularity: 'WEEK' },
            breakdown: '',
            chartType: 'line'
        },
        'vl_sla_area_trend': {
            baseTable: 'entregas',
            joins: [],
            filters: [{ column: 'dim_fecha', operator: 'contains', value: '2026' }],
            metric: { column: 'met_sla_efficiency', aggregation: 'SLA_EFFICIENCY', format: 'percent' },
            timeAxis: { column: 'dim_fecha', granularity: 'WEEK' },
            breakdown: 'dim_area',
            chartType: 'line'
        },
        'vl_top_authors': {
            baseTable: 'entregas',
            joins: [],
            filters: [],
            metric: { column: 'met_entregas', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: 'dim_autor',
            chartType: 'bar'
        },
        
        // --- KPIS DEL SISTEMA (Tablas / Tarjetas Métricas) ---
        'vl_kpi_total': {
            baseTable: 'entregas',
            joins: [],
            filters: [
                { column: 'dim_fecha', operator: 'contains', value: '2026' },
                { column: 'dim_ubic_area', operator: 'isnotnull', value: '' },
                { column: 'dim_ubic_area', operator: 'notequals', value: 'PASAGG-752' }
            ],
            metric: { column: 'met_entregas', aggregation: 'COUNT_DISTINCT' },
            timeAxis: { column: 'dim_fecha', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'vl_kpi_eff': {
            baseTable: 'entregas',
            joins: [],
            filters: [
                { column: 'dim_fecha', operator: 'contains', value: '2026' },
                { column: 'met_retraso', operator: 'lessthan', value: '3' },
                { column: 'dim_ubic_area', operator: 'isnotnull', value: '' },
                { column: 'dim_ubic_area', operator: 'notequals', value: 'PASAGG-752' }
            ],
            metric: { column: 'met_entregas', aggregation: 'COUNT_DISTINCT' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: '',
            chartType: 'kpi'
        },
        'vl_kpi_ontime': {
            baseTable: 'entregas',
            joins: [],
            filters: [
                { column: 'dim_fecha', operator: 'contains', value: '2026' },
                { column: 'met_retraso', operator: 'lessthan', value: '3' },
                { column: 'dim_ubic_area', operator: 'isnotnull', value: '' },
                { column: 'dim_ubic_area', operator: 'notequals', value: 'PASAGG-752' }
            ],
            metric: { column: 'met_entregas', aggregation: 'COUNT_DISTINCT' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: '',
            chartType: 'kpi'
        },
        'vl_kpi_late': {
            baseTable: 'entregas',
            joins: [],
            filters: [
                { column: 'dim_fecha', operator: 'contains', value: '2026' },
                { column: 'met_retraso', operator: 'greaterthan', value: '2' },
                { column: 'dim_ubic_area', operator: 'isnotnull', value: '' },
                { column: 'dim_ubic_area', operator: 'notequals', value: 'PASAGG-752' }
            ],
            metric: { column: 'met_entregas', aggregation: 'COUNT_DISTINCT' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_ingresos': {
            baseTable: 'movimientos',
            joins: [],
            filters: [{ column: 'dim_tipo_operacion', operator: 'contains', value: 'Ingreso' }],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_consumos_prod': {
            baseTable: 'movimientos',
            joins: [],
            filters: [{ column: 'dim_tipo_operacion', operator: 'contains', value: 'Centro Costo' }],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_consumos_mant': {
            baseTable: 'movimientos',
            joins: [],
            filters: [{ column: 'dim_tipo_operacion', operator: 'contains', value: 'Orden/Reserva' }],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_rate_reabast': {
            baseTable: 'movimientos',
            joins: [],
            filters: [{ column: 'dim_fecha_contab', operator: 'contains', value: '2026' }],
            metric: { column: 'met_replenishment_rate', aggregation: 'REPLENISHMENT_RATE', format: 'percent' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_traspasos': {
            baseTable: 'movimientos',
            joins: [],
            filters: [
                { column: 'dim_cmv', operator: 'in', value: '301, 303' },
                { column: 'dim_fecha_contab', operator: 'contains', value: '2026' }
            ],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_rate_devolucion': {
            baseTable: 'movimientos',
            joins: [],
            filters: [{ column: 'dim_fecha_contab', operator: 'contains', value: '2026' }],
            metric: { column: 'met_return_rate', aggregation: 'RETURN_RATE', format: 'percent' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_rate_eficiencia': {
            baseTable: 'movimientos',
            joins: [],
            filters: [{ column: 'dim_fecha_contab', operator: 'contains', value: '2026' }],
            metric: { column: 'met_inv_efficiency', aggregation: 'INV_EFFICIENCY', format: 'percent' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'ots_kpi_pending': {
            baseTable: 'tareas',
            joins: [],
            filters: [{ column: 'warehouse_tasks.fecha_conf', operator: 'isnull', value: '' }],
            metric: { column: 'met_tareas', aggregation: 'COUNT' },
            timeAxis: { column: '', granularity: 'DAY' },
            breakdown: '',
            chartType: 'kpi'
        },
        'ots_kpi_users': {
            baseTable: 'tareas',
            joins: [],
            filters: [
                { column: 'dim_usuario', operator: 'isnotnull', value: '' },
                { column: 'dim_fecha_creac', operator: 'contains', value: '2026' }
            ],
            metric: { column: 'dim_usuario', aggregation: 'COUNT_DISTINCT' },
            timeAxis: { column: '', granularity: 'MONTH' },
            breakdown: '',
            chartType: 'kpi'
        }
    };

    async function openEditQueryModal(queryId, chartTitle) {
        console.log("Studio: Abriendo modal para", queryId);
        currentQueryId = queryId;
        const modal = document.getElementById('modalEditQuery');
        if(!modal) {
            alert("Error crítico: No se encontró el elemento modalEditQuery en el DOM");
            return;
        }

        document.getElementById('editQueryId').value = queryId;
        document.getElementById('editQueryTitle').innerHTML = `Studio de Analíticas &bull; ${chartTitle}`;
        
        modal.classList.add('show');
        
        // Carga asíncrona de datos
        await loadSchema();

        try {
            const response = await fetch(`/api/queries/${queryId}`);
            if (!response.ok) throw new Error("Status: " + response.status);
            const data = await response.json();

            // Fallbacks legacy eliminados (Fase 1: No más SQL crudo).
            // Todo debe procesarse a través del visual_state.

            // Caso B: query con constructor visual → flujo normal
            if (data.visual_state) {
                try {
                    serverVisualState = JSON.parse(data.visual_state);
                } catch (e) {
                    serverVisualState = null;
                }
            } else {
                serverVisualState = null;
            }

            // Inicializar el Constructor Visual
            initVisualQuery(queryId);

            setTimeout(() => runPreview(), 300);
        } catch (err) {
            console.error("Studio Load Error:", err);
        }

    }

    async function loadSchema() {
        if (Object.keys(currentSchema).length > 0) return;
        try {
            const response = await fetch('/api/studio/schema');
            if (!response.ok) return;
            currentSchema = await response.json();
            
            const listEl = document.getElementById('dbSchemaList');
            if (listEl) {
                let html = '';
                for (const ds_id of Object.keys(currentSchema)) {
                    html += `<div class="table-nav-item" onclick="previewTable('${ds_id}', this)">
                                <i class="fas fa-cube"></i> ${currentSchema[ds_id].label}
                            </div>`;
                }
                listEl.innerHTML = html;
                const firstDataset = Object.keys(currentSchema)[0];
                if (firstDataset) previewTable(firstDataset, listEl.querySelector('.table-nav-item'));
            }
        } catch (err) { console.error("Schema fetch fail", err); }
    }

    async function previewTable(tableName, el) {
        document.querySelectorAll('.table-nav-item').forEach(item => item.classList.remove('active'));
        if(el) el.classList.add('active');
        const previewEl = document.getElementById('dbTablePreview');
        if (!previewEl) return;
        previewEl.innerHTML = '<div style="text-align:center; padding: 20px;"><i class="fas fa-spinner fa-spin"></i></div>';
        try {
            const response = await fetch(`/api/studio/preview_table/${tableName}`);
            const data = await response.json();
            let html = `<h4 style="color: var(--primary); font-size: 0.9rem; margin-bottom:10px;">${tableName}</h4>`;
            if (data.length > 0) {
                const cols = Object.keys(data[0]);
                html += `<div class="table-responsive"><table class="mini-table"><thead><tr>${cols.map(c=>`<th>${c}</th>`).join('')}</tr></thead><tbody>`;
                html += data.map(row => `<tr>${cols.map(c=>`<td>${row[c]}</td>`).join('')}</tr>`).join('');
                html += `</tbody></table></div>`;
            }
            previewEl.innerHTML = html;
        } catch (e) { previewEl.innerHTML = "Error preview"; }
    }

    async function runPreview() {
        const errorEl = document.getElementById('previewError');
        errorEl.style.display = 'none';
        
        let payload = { query_id: 'preview' };
        payload.visual_state = JSON.stringify(visualState);
        
        try {
            const response = await fetch('/api/studio/preview', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            if (data.error) {
                errorEl.innerHTML = `<b>Error SQL:</b><br><small>${data.error}</small>`;
errorEl.style.display = 'block';
                return;
            }
            renderPreviewChart(data);
        } catch (err) { console.error(err); }
    }

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

    function closeEditQueryModal() { document.getElementById('modalEditQuery').classList.remove('show'); }

    function showConfirmPublish() {
        const overlay = document.getElementById('confirmPublishOverlay');
        overlay.style.display = 'flex';
        setTimeout(() => {
            document.getElementById('confirmPublishCard').style.transform = 'scale(1)';
        }, 10);
    }

    function hideConfirmPublish() {
        document.getElementById('confirmPublishCard').style.transform = 'scale(0.9)';
        setTimeout(() => {
            document.getElementById('confirmPublishOverlay').style.display = 'none';
        }, 150);
    }

    async function executePublishQuery() {
        const queryId = document.getElementById('editQueryId').value;
        const visualStateJson = JSON.stringify(visualState);

        // Botón de confirmación
        const confirmBtn = document.querySelector('#confirmPublishOverlay button[onclick*="executePublishQuery"]');
        const originalHtml = confirmBtn.innerHTML;
        confirmBtn.disabled = true;
        confirmBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Publicando...';

        try {
            const response = await fetch('/api/settings/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                // Solo se envía visual_state. El SQL se compila en tiempo de ejecución.
                // sql_text ya no se persiste desde la UI (Fase 1 del plan de refactorización).
                body: JSON.stringify({
                    query_id: queryId,
                    visual_state: visualStateJson
                })
            });
            if (response.ok) {
                confirmBtn.style.background = '#22c55e';
                confirmBtn.innerHTML = '<i class="fas fa-check-circle"></i> ¡Publicado!';
                setTimeout(() => {
                    hideConfirmPublish();
                    closeEditQueryModal();
                    location.reload();
                }, 800);
            } else {
                const errData = await response.json();
                alert("Error al guardar: " + (errData.detail || "Error en el servidor"));
                confirmBtn.disabled = false;
                confirmBtn.innerHTML = originalHtml;
            }
        } catch (e) {
            alert("Error de red al guardar cambios");
            confirmBtn.disabled = false;
            confirmBtn.innerHTML = originalHtml;
        }
    }



    // ─── LÓGICA DEL CONSTRUCTOR VISUAL (QB) ──────────────────────────────────
    function initVisualQuery(queryId) {
        let state;
        if (serverVisualState) {
            state = serverVisualState;
        } else {
            state = defaultVisualStates[queryId] || {
                baseTable: Object.keys(currentSchema)[0] || '',
                joins: [],
                filters: [],
                metric: { column: '', aggregation: 'COUNT' },
                timeAxis: { column: '', granularity: 'MONTH' },
                breakdown: '',
                chartType: 'bar'
            };
        }
        
        // Encapsular en el scope modular
        AnalyticsStudioManager.setVisualState(queryId, JSON.parse(JSON.stringify(state)));
        visualState = AnalyticsStudioManager.getVisualState(queryId);
        
        // Poblar baseTable select (ahora Dataset Semántico)
        const baseSelect = document.getElementById('qbBaseTable');
        baseSelect.innerHTML = Object.keys(currentSchema).map(t => `<option value="${t}">${currentSchema[t].label}</option>`).join('');
        baseSelect.value = visualState.baseTable;
        
        renderFilters();
        renderFilters();
        
        // Configurar Ejes forzando los valores del estado mapeado
        refreshQbColumns(true);
        
        document.getElementById('qbMetricAgg').value = visualState.metric.aggregation;
        if (!visualState.metric.format) {
            visualState.metric.format = 'number';
        }
        document.getElementById('qbMetricFormat').value = visualState.metric.format;
        document.getElementById('qbTimeGranularity').value = visualState.timeAxis.granularity;
        
        // Auto-seleccionar tipo de gráfico según definición original
        if (visualState.chartType) {
            document.getElementById('studioChartType').value = visualState.chartType;
        }

        // Restaurar estado de Segunda Métrica
        const smEnabled = !!(visualState.secondMetric && visualState.secondMetric.column);
        const smCheckbox = document.getElementById('qbSecondMetricEnabled');
        const smPanel = document.getElementById('qbSecondMetricPanel');
        if (smCheckbox) smCheckbox.checked = smEnabled;
        if (smPanel) smPanel.style.display = smEnabled ? 'block' : 'none';
        if (smEnabled && visualState.secondMetric) {
            const smAggEl = document.getElementById('qbSecondMetricAgg');
            const smLabelEl = document.getElementById('qbSecondMetricLabel');
            if (smAggEl) smAggEl.value = visualState.secondMetric.aggregation || 'COUNT_DISTINCT';
            if (smLabelEl) smLabelEl.value = visualState.secondMetric.label || '';
        }
        
        runPreview();
    }

    function onBaseTableChange() {
        visualState.baseTable = document.getElementById('qbBaseTable').value;
        visualState.joins = []; // Limpiar joins al cambiar tabla base
        renderJoins();
        refreshQbColumns(false);
        onQbChange();
    }

    function getActiveTables() {
        // En la capa semántica, los datasets son autocontenidos. No se exponen joins físicos.
        return [visualState.baseTable];
    }

    function getActiveColumns() {
        let cols = [];
        const ds_id = visualState.baseTable;
        const ds = currentSchema[ds_id];
        if (ds) {
            (ds.dimensions || []).forEach(d => cols.push({ id: d.id, label: `Dimensión: ${d.label}` }));
            (ds.metrics || []).forEach(m => cols.push({ id: m.id, label: `Métrica: ${m.label}` }));
        }
        return cols;
    }

    function refreshQbColumns(forceState = false) {
        const colsObj = getActiveColumns();
        const colsIds = colsObj.map(c => c.id);
        const renderOptions = (items) => items.map(c => `<option value="${c.id}">${c.label}</option>`).join('');
        
        // Eje Y dropdown
        const ySelect = document.getElementById('qbMetricColumn');
        const prevY = forceState ? visualState.metric.column : (ySelect.value || visualState.metric.column);
        ySelect.innerHTML = renderOptions(colsObj);
        if(colsIds.includes(prevY)) {
            ySelect.value = prevY;
            visualState.metric.column = prevY;
        } else {
            visualState.metric.column = ySelect.value;
        }
        
        // Eje X dropdown
        const xSelect = document.getElementById('qbTimeColumn');
        const prevX = forceState ? visualState.timeAxis.column : (xSelect.value || visualState.timeAxis.column);
        xSelect.innerHTML = '<option value="">-- Sin Eje X (Total Acumulado) --</option>' + renderOptions(colsObj);
        if(prevX === '' || colsIds.includes(prevX)) {
            xSelect.value = prevX;
            visualState.timeAxis.column = prevX;
        } else {
            xSelect.value = '';
            visualState.timeAxis.column = '';
        }

        // Desglose dropdown
        const bSelect = document.getElementById('qbBreakdownColumn');
        const prevB = forceState ? visualState.breakdown : (bSelect.value !== undefined ? bSelect.value : visualState.breakdown);
        bSelect.innerHTML = '<option value="">-- Sin Desglose --</option>' + renderOptions(colsObj);
        if(prevB === '' || colsIds.includes(prevB)) {
            bSelect.value = prevB;
            visualState.breakdown = prevB;
        } else {
            bSelect.value = '';
            visualState.breakdown = '';
        }

        // Segunda Métrica dropdown (mismas columnas que la métrica principal)
        const sm2Select = document.getElementById('qbSecondMetricColumn');
        if (sm2Select) {
            const prevSM = forceState
                ? (visualState.secondMetric ? visualState.secondMetric.column : '')
                : (sm2Select.value || '');
            sm2Select.innerHTML = renderOptions(colsObj);
            if (colsIds.includes(prevSM)) sm2Select.value = prevSM;
        }
    }



    // FILTROS (WHERE)
    const operators = [
        { value: 'equals', label: 'es igual a' },
        { value: 'notequals', label: 'no es igual a' },
        { value: 'greaterthan', label: 'mayor que' },
        { value: 'lessthan', label: 'menor que' },
        { value: 'greaterthanequal', label: 'mayor o igual a' },
        { value: 'lessthanequal', label: 'menor o igual a' },
        { value: 'contains', label: 'contiene' },
        { value: 'notcontains', label: 'no contiene' },
        { value: 'in', label: 'está en (valores separados por coma)' },
        { value: 'isnull', label: 'es nulo / vacío' },
        { value: 'isnotnull', label: 'no es nulo' }
    ];

    function renderFilters() {
        const container = document.getElementById('qbFiltersContainer');
        container.innerHTML = '';
        
        visualState.filters.forEach((f, index) => {
            const isNullVal = ['isnull', 'isnotnull'].includes(f.operator);
            const valueType = f.valueType || 'value';
            
            // Generar HTML dinámico de controles de valor según su tipo
            let valControlsHtml = '';
            if (isNullVal) {
                valControlsHtml = '';
            } else if (valueType === 'value') {
                valControlsHtml = `
                    <input type="text" class="qb-input f-val" value="${f.value || ''}" placeholder="Valor..." oninput="updateFilter(${index})">
                `;
            } else if (valueType === 'column') {
                valControlsHtml = `
                    <select class="qb-select f-comp-col" onchange="updateFilter(${index})">
                        <option value="" disabled ${!f.compareColumn ? 'selected' : ''}>-- Columna --</option>
                        ${getActiveColumns().map(c => `<option value="${c.id}" ${c.id === f.compareColumn ? 'selected' : ''}>${c.label}</option>`).join('')}
                    </select>
                `;
            } else if (valueType === 'date_diff') {
                // En capa semántica, listamos todo por simplicidad
                const colOptions = [
                    `<option value="today" ${f.compareColumn === 'today' ? 'selected' : ''}>📅 Hoy (DATE('now'))</option>`,
                    ...getActiveColumns().map(c => `<option value="${c.id}" ${c.id === f.compareColumn ? 'selected' : ''}>${c.label}</option>`)
                ].join('');
                valControlsHtml = `
                    <span style="font-size:0.8rem; color:var(--text-muted); align-self:center; margin:0 5px;">vs</span>
                    <select class="qb-select f-comp-col" onchange="updateFilter(${index})" style="min-width:160px;">
                        ${colOptions}
                    </select>
                    <select class="qb-select f-op-diff" onchange="updateFilter(${index})" style="width:90px;">
                        <option value="lessthanequal" ${(f.diffOp||'lessthanequal')==='lessthanequal'?'selected':''}>diff ≤</option>
                        <option value="greaterthan"   ${(f.diffOp||'')==='greaterthan'?'selected':''}>diff ></option>
                        <option value="equals"        ${(f.diffOp||'')==='equals'?'selected':''}>diff =</option>
                    </select>
                    <input type="number" class="qb-input f-offset" style="width:65px;" value="${f.offsetValue ?? '2'}" placeholder="Días" oninput="updateFilter(${index})">
                    <span style="font-size:0.8rem; color:var(--text-muted); align-self:center; margin:0 2px;">días</span>
                `;
            }

            const filterRow = document.createElement('div');
            filterRow.className = 'qb-form-row';
            filterRow.style = 'display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 8px;';

            // Para date_diff, el operador principal no tiene sentido → mostrar label fijo
            const opControl = (valueType === 'date_diff')
                ? `<span class="qb-select" style="width:130px; display:flex; align-items:center; justify-content:center;
                       font-size:0.78rem; color:var(--text-muted); border:1px dashed var(--border); border-radius:6px; cursor:default;">
                       📅 diferencia
                   </span>
                   <input type="hidden" class="f-op" value="${f.operator || 'greaterthan'}">`
                : `<select class="qb-select f-op" style="width: 130px;" onchange="updateFilter(${index})">
                       ${operators.map(o => `<option value="${o.value}" ${o.value === f.operator ? 'selected' : ''}>${o.label}</option>`).join('')}
                   </select>`;

            filterRow.innerHTML = `
                <select class="qb-select f-col" style="flex: 1; min-width: 140px;" onchange="updateFilter(${index})">
                    ${getActiveColumns().map(c => `<option value="${c.id}" ${c.id === f.column ? 'selected' : ''}>${c.label}</option>`).join('')}
                </select>
                
                ${opControl}
                
                ${isNullVal ? '' : `
                <select class="qb-select f-type" style="width: 140px;" onchange="updateFilterType(${index}, this.value)">
                    <option value="value"     ${valueType === 'value'     ? 'selected' : ''}>Valor Fijo</option>
                    <option value="column"    ${valueType === 'column'    ? 'selected' : ''}>Otra Columna</option>
                    <option value="date_diff" ${valueType === 'date_diff' ? 'selected' : ''}>Diferencia Fechas</option>
                </select>
                `}
                
                <div class="f-val-container" style="display: flex; gap: 6px; align-items: center; flex: 2; min-width: 200px;">
                    ${valControlsHtml}
                </div>
                
                <div class="qb-trash-btn" onclick="removeFilter(${index})"><i class="fas fa-trash"></i></div>
            `;

            container.appendChild(filterRow);
        });
    }

    function addFilter() {
        visualState.filters.push({
            column: (getActiveColumns()[0] || {}).id || '',
            operator: 'equals',
            value: '',
            valueType: 'value',
            compareColumn: null,
            offsetValue: null
        });
        renderFilters();
        onQbChange();
    }

    function updateFilterType(index, type) {
        visualState.filters[index].valueType = type;
        if (type === 'column') {
            visualState.filters[index].compareColumn = (getActiveColumns()[1] || getActiveColumns()[0] || {}).id || '';
            visualState.filters[index].value = '';
            visualState.filters[index].offsetValue = null;
            visualState.filters[index].diffOp = null;
        } else if (type === 'date_diff') {
            // Por defecto comparar contra Hoy — el caso más frecuente
            visualState.filters[index].compareColumn = 'today';
            visualState.filters[index].value = '';
            visualState.filters[index].offsetValue = '2';
            visualState.filters[index].diffOp = 'lessthanequal';
        } else {
            visualState.filters[index].compareColumn = null;
            visualState.filters[index].value = '';
            visualState.filters[index].offsetValue = null;
            visualState.filters[index].diffOp = null;
        }
        renderFilters();
        onQbChange();
    }

    function updateFilter(index) {
        const row = document.getElementById('qbFiltersContainer').children[index];
        visualState.filters[index].column = row.querySelector('.f-col').value;
        
        const prevOp = visualState.filters[index].operator;
        const newOp = row.querySelector('.f-op').value;
        visualState.filters[index].operator = newOp;
        
        if (['isnull', 'isnotnull'].includes(newOp)) {
            visualState.filters[index].value = '';
            visualState.filters[index].valueType = 'value';
            visualState.filters[index].compareColumn = null;
            visualState.filters[index].offsetValue = null;
        } else {
            const typeEl = row.querySelector('.f-type');
            const valueType = typeEl ? typeEl.value : 'value';
            visualState.filters[index].valueType = valueType;
            
            if (valueType === 'value') {
                const valEl = row.querySelector('.f-val');
                visualState.filters[index].value = valEl ? valEl.value : '';
            } else if (valueType === 'column') {
                const compEl = row.querySelector('.f-comp-col');
                visualState.filters[index].compareColumn = compEl ? compEl.value : '';
            } else if (valueType === 'date_diff') {
                const compEl = row.querySelector('.f-comp-col');
                const offsetEl = row.querySelector('.f-offset');
                const diffOpEl = row.querySelector('.f-op-diff');
                visualState.filters[index].compareColumn = compEl ? compEl.value : 'today';
                visualState.filters[index].offsetValue = offsetEl ? offsetEl.value : '2';
                visualState.filters[index].diffOp = diffOpEl ? diffOpEl.value : 'lessthanequal';
            }
        }
        
        if (['isnull', 'isnotnull'].includes(newOp) || ['isnull', 'isnotnull'].includes(prevOp)) {
            renderFilters();
        }
        
        onQbChange();
    }

    function removeFilter(index) {
        visualState.filters.splice(index, 1);
        renderFilters();
        onQbChange();
    }

    // Handler: toggle de la Segunda Métrica
    function onSecondMetricToggle() {
        const enabled = document.getElementById('qbSecondMetricEnabled').checked;
        const panel = document.getElementById('qbSecondMetricPanel');
        if (panel) panel.style.display = enabled ? 'block' : 'none';
        if (!enabled) visualState.secondMetric = null;
        onQbChange();
    }

    // Sincronización a SQL y simulación automática
    function onQbChange() {
        // Actualizar métricas y ejes del estado
        visualState.metric.column = document.getElementById('qbMetricColumn').value;
        visualState.metric.aggregation = document.getElementById('qbMetricAgg').value;
        visualState.metric.format = document.getElementById('qbMetricFormat').value;
        
        visualState.timeAxis.column = document.getElementById('qbTimeColumn').value;
        visualState.timeAxis.granularity = document.getElementById('qbTimeGranularity').value;
        
        visualState.breakdown = document.getElementById('qbBreakdownColumn').value;

        // Segunda métrica: leer si el checkbox está activo y no hay breakdown
        const smCheckbox = document.getElementById('qbSecondMetricEnabled');
        const smPanel = document.getElementById('qbSecondMetricPanel');
        const smDisabledNote = document.getElementById('qbSecondMetricDisabledNote');
        const hasBreakdown = !!visualState.breakdown;

        if (hasBreakdown) {
            // Si hay desglose, ocultar el panel y deshabilitar la segunda métrica
            if (smCheckbox) smCheckbox.disabled = true;
            if (smPanel) smPanel.style.display = 'none';
            if (smDisabledNote) smDisabledNote.style.display = 'block';
            visualState.secondMetric = null;
        } else {
            if (smCheckbox) smCheckbox.disabled = false;
            if (smDisabledNote) smDisabledNote.style.display = 'none';
            const smEnabled = smCheckbox && smCheckbox.checked;
            if (smPanel) smPanel.style.display = smEnabled ? 'block' : 'none';
            if (smEnabled) {
                visualState.secondMetric = {
                    column: document.getElementById('qbSecondMetricColumn').value || '',
                    aggregation: document.getElementById('qbSecondMetricAgg').value || 'COUNT_DISTINCT',
                    label: document.getElementById('qbSecondMetricLabel').value || ''
                };
            } else {
                visualState.secondMetric = null;
            }
        }

    }
