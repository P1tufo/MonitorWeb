    let studioChartInstance = null;
    let currentSchema = {};
    let currentQueryId = "";
    let studioBoundParams = null;
    let serverVisualState = null;
    
    // Estado del constructor visual
    let visualState = {
        baseTable: '',
        joins: [],
        filters: [],
        metric: { column: '', aggregation: 'COUNT' },
        timeAxis: { column: '', granularity: 'MONTH' },
        breakdown: '',
        secondMetric: null
    };

    // Mapeos predefinidos para inicialización visual intuitiva de todos los gráficos del sistema
    const defaultVisualStates = {
        'ots_daily_trend': {
            baseTable: 'warehouse_tasks',
            joins: [],
            filters: [],
            metric: { column: 'warehouse_tasks.numero_ot', aggregation: 'COUNT' },
            timeAxis: { column: 'warehouse_tasks.fe_creac', granularity: 'DAY' },
            breakdown: '',
            chartType: 'line'
        },
        'ots_by_movement_type': {
            baseTable: 'warehouse_tasks',
            joins: [],
            filters: [{ column: 'warehouse_tasks.cl_mov', operator: 'isnotnull', value: '' }],
            metric: { column: 'warehouse_tasks.numero_ot', aggregation: 'COUNT' },
            timeAxis: { column: 'warehouse_tasks.fe_creac', granularity: 'MONTH' },
            breakdown: 'warehouse_tasks.clase_mov',
            chartType: 'pie'
        },
        'ots_by_user_dual': {
            baseTable: 'warehouse_tasks',
            joins: [],
            filters: [],
            metric: { column: 'warehouse_tasks.numero_ot', aggregation: 'COUNT' },
            timeAxis: { column: 'warehouse_tasks.fe_creac', granularity: 'MONTH' },
            breakdown: 'warehouse_tasks.usuario',
            chartType: 'bar'
        },
        'inv_volumen_stats': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [],
            metric: { column: 'inventory_movements.material', aggregation: 'COUNT' },
            timeAxis: { column: 'inventory_movements.fe_contab', granularity: 'DAY' },
            breakdown: 'inventory_movements.tipo_operacion',
            chartType: 'bar'
        },
        'inv_consumos_quick': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [{ column: 'inventory_movements.material', operator: 'isnotnull', value: '' }],
            metric: { column: 'inventory_movements.cantidad', aggregation: 'SUM' },
            timeAxis: { column: 'inventory_movements.fe_contab', granularity: 'MONTH' },
            breakdown: 'inventory_movements.texto_breve_material',
            chartType: 'bar'
        },
        'vl_monthly_evolution': {
            baseTable: 'outbound_deliveries',
            joins: [],
            filters: [],
            metric: { column: 'outbound_deliveries.entrega', aggregation: 'COUNT' },
            timeAxis: { column: 'outbound_deliveries.fecha_carga', granularity: 'MONTH' },
            breakdown: '',
            chartType: 'line'
        },
        'vl_weekly_evolution': {
            baseTable: 'outbound_deliveries',
            joins: [],
            filters: [],
            metric: { column: 'outbound_deliveries.entrega', aggregation: 'COUNT' },
            timeAxis: { column: 'outbound_deliveries.fecha_carga', granularity: 'WEEK' },
            breakdown: '',
            chartType: 'line'
        },
        'vl_top_locations': {
            baseTable: 'outbound_deliveries',
            joins: [],
            filters: [],
            metric: { column: 'outbound_deliveries.entrega', aggregation: 'COUNT' },
            timeAxis: { column: 'outbound_deliveries.fecha_carga', granularity: 'MONTH' },
            breakdown: 'outbound_deliveries.ubicacion_bin',
            chartType: 'bar'
        },
        'inv_area_stats_prod': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [],
            metric: { column: 'inventory_movements.cantidad', aggregation: 'SUM' },
            timeAxis: { column: 'inventory_movements.fe_contab', granularity: 'MONTH' },
            breakdown: 'inventory_movements.ce_coste',
            chartType: 'bar'
        },
        'inv_consumos_abc': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [],
            metric: { column: 'inventory_movements.material', aggregation: 'COUNT' },
            timeAxis: { column: 'inventory_movements.fe_contab', granularity: 'MONTH' },
            breakdown: 'inventory_movements.texto_breve_material',
            chartType: 'bar'
        },
        'inv_dow_stats': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [],
            metric: { column: 'inventory_movements.material', aggregation: 'COUNT' },
            timeAxis: { column: 'inventory_movements.fe_contab', granularity: 'DAY' },
            breakdown: '',
            chartType: 'line'
        },
        'inv_pm_type_records': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [],
            metric: { column: 'inventory_movements.cantidad', aggregation: 'SUM' },
            timeAxis: { column: 'inventory_movements.fe_contab', granularity: 'MONTH' },
            breakdown: 'inventory_movements.tipo_operacion',
            chartType: 'bar'
        },
        'inv_location_summary': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [],
            metric: { column: 'inventory_movements.material', aggregation: 'COUNT' },
            timeAxis: { column: 'inventory_movements.fe_contab', granularity: 'MONTH' },
            breakdown: 'inventory_movements.alm',
            chartType: 'bar'
        },
        'inv_top_users': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [],
            metric: { column: 'inventory_movements.material', aggregation: 'COUNT' },
            timeAxis: { column: 'inventory_movements.fe_contab', granularity: 'MONTH' },
            breakdown: 'inventory_movements.usuario',
            chartType: 'bar'
        },
        'vl_sla_monthly_trend': {
            baseTable: 'outbound_deliveries',
            joins: [],
            filters: [{ column: 'outbound_deliveries.fecha_carga', operator: 'contains', value: '2026' }],
            metric: { column: 'outbound_deliveries.dias_retraso', aggregation: 'SLA_EFFICIENCY', format: 'percent' },
            timeAxis: { column: 'outbound_deliveries.fecha_carga', granularity: 'MONTH' },
            breakdown: '',
            secondMetric: { column: 'outbound_deliveries.entrega', aggregation: 'COUNT_DISTINCT', label: 'Materiales Solicitados' },
            chartType: 'line'
        },
        'vl_sla_area_monthly_trend': {
            baseTable: 'outbound_deliveries',
            joins: [],
            filters: [{ column: 'outbound_deliveries.fecha_carga', operator: 'contains', value: '2026' }],
            metric: { column: 'outbound_deliveries.dias_retraso', aggregation: 'SLA_EFFICIENCY', format: 'percent' },
            timeAxis: { column: 'outbound_deliveries.fecha_carga', granularity: 'MONTH' },
            breakdown: 'outbound_deliveries.area_negocio',
            chartType: 'line'
        },
        'vl_sla_trend': {
            baseTable: 'outbound_deliveries',
            joins: [],
            filters: [{ column: 'outbound_deliveries.fecha_carga', operator: 'contains', value: '2026' }],
            metric: { column: 'outbound_deliveries.dias_retraso', aggregation: 'SLA_EFFICIENCY', format: 'percent' },
            timeAxis: { column: 'outbound_deliveries.fecha_carga', granularity: 'WEEK' },
            breakdown: '',
            chartType: 'line'
        },
        'vl_sla_area_trend': {
            baseTable: 'outbound_deliveries',
            joins: [],
            filters: [{ column: 'outbound_deliveries.fecha_carga', operator: 'contains', value: '2026' }],
            metric: { column: 'outbound_deliveries.dias_retraso', aggregation: 'SLA_EFFICIENCY', format: 'percent' },
            timeAxis: { column: 'outbound_deliveries.fecha_carga', granularity: 'WEEK' },
            breakdown: 'outbound_deliveries.area_negocio',
            chartType: 'line'
        },
        'vl_top_authors': {
            baseTable: 'outbound_deliveries',
            joins: [],
            filters: [],
            metric: { column: 'outbound_deliveries.entrega', aggregation: 'COUNT' },
            timeAxis: { column: 'outbound_deliveries.fecha_carga', granularity: 'MONTH' },
            breakdown: 'outbound_deliveries.autor',
            chartType: 'bar'
        },
        
        // --- KPIS DEL SISTEMA (Tablas / Tarjetas Métricas) ---
        'vl_kpi_total': {
            baseTable: 'outbound_deliveries',
            joins: [],
            filters: [
                { column: 'outbound_deliveries.fecha_carga', operator: 'contains', value: '2026' },
                { column: 'outbound_deliveries.ubicacion_area', operator: 'isnotnull', value: '' },
                { column: 'outbound_deliveries.ubicacion_area', operator: 'notequals', value: 'PASAGG-752' }
            ],
            metric: { column: 'outbound_deliveries.entrega', aggregation: 'COUNT_DISTINCT' },
            timeAxis: { column: 'outbound_deliveries.fecha_carga', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'vl_kpi_eff': {
            baseTable: 'outbound_deliveries',
            joins: [],
            filters: [
                { column: 'outbound_deliveries.fecha_carga', operator: 'contains', value: '2026' },
                { column: 'outbound_deliveries.dias_retraso', operator: 'lessthan', value: '3' },
                { column: 'outbound_deliveries.ubicacion_area', operator: 'isnotnull', value: '' },
                { column: 'outbound_deliveries.ubicacion_area', operator: 'notequals', value: 'PASAGG-752' }
            ],
            metric: { column: 'outbound_deliveries.entrega', aggregation: 'COUNT_DISTINCT' },
            timeAxis: { column: 'outbound_deliveries.fecha_carga', granularity: 'MONTH' },
            breakdown: '',
            chartType: 'kpi'
        },
        'vl_kpi_ontime': {
            baseTable: 'outbound_deliveries',
            joins: [],
            filters: [
                { column: 'outbound_deliveries.fecha_carga', operator: 'contains', value: '2026' },
                { column: 'outbound_deliveries.dias_retraso', operator: 'lessthan', value: '3' },
                { column: 'outbound_deliveries.ubicacion_area', operator: 'isnotnull', value: '' },
                { column: 'outbound_deliveries.ubicacion_area', operator: 'notequals', value: 'PASAGG-752' }
            ],
            metric: { column: 'outbound_deliveries.entrega', aggregation: 'COUNT_DISTINCT' },
            timeAxis: { column: 'outbound_deliveries.fecha_carga', granularity: 'MONTH' },
            breakdown: '',
            chartType: 'kpi'
        },
        'vl_kpi_late': {
            baseTable: 'outbound_deliveries',
            joins: [],
            filters: [
                { column: 'outbound_deliveries.fecha_carga', operator: 'contains', value: '2026' },
                { column: 'outbound_deliveries.dias_retraso', operator: 'greaterthan', value: '2' },
                { column: 'outbound_deliveries.ubicacion_area', operator: 'isnotnull', value: '' },
                { column: 'outbound_deliveries.ubicacion_area', operator: 'notequals', value: 'PASAGG-752' }
            ],
            metric: { column: 'outbound_deliveries.entrega', aggregation: 'COUNT_DISTINCT' },
            timeAxis: { column: 'outbound_deliveries.fecha_carga', granularity: 'MONTH' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_ingresos': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [{ column: 'inventory_movements.tipo_operacion', operator: 'contains', value: 'Ingreso' }],
            metric: { column: 'inventory_movements.material', aggregation: 'COUNT' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_consumos_prod': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [{ column: 'inventory_movements.tipo_operacion', operator: 'contains', value: 'Centro Costo' }],
            metric: { column: 'inventory_movements.material', aggregation: 'COUNT' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_consumos_mant': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [{ column: 'inventory_movements.tipo_operacion', operator: 'contains', value: 'Orden/Reserva' }],
            metric: { column: 'inventory_movements.material', aggregation: 'COUNT' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_rate_reabast': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [{ column: 'inventory_movements.fe_contab', operator: 'contains', value: '2026' }],
            metric: { column: 'inventory_movements.tipo_operacion', aggregation: 'REPLENISHMENT_RATE', format: 'percent' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_traspasos': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [
                { column: 'inventory_movements.cmv', operator: 'in', value: '301, 303' },
                { column: 'inventory_movements.fe_contab', operator: 'contains', value: '2026' }
            ],
            metric: { column: 'inventory_movements.material', aggregation: 'COUNT' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_rate_devolucion': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [{ column: 'inventory_movements.fe_contab', operator: 'contains', value: '2026' }],
            metric: { column: 'inventory_movements.tipo_operacion', aggregation: 'RETURN_RATE', format: 'percent' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_rate_eficiencia': {
            baseTable: 'inventory_movements',
            joins: [],
            filters: [{ column: 'inventory_movements.fe_contab', operator: 'contains', value: '2026' }],
            metric: { column: 'inventory_movements.tipo_operacion', aggregation: 'INV_EFFICIENCY', format: 'percent' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'ots_kpi_pending': {
            baseTable: 'warehouse_tasks',
            joins: [],
            filters: [{ column: 'warehouse_tasks.fecha_conf', operator: 'isnull', value: '' }],
            metric: { column: 'warehouse_tasks.numero_ot', aggregation: 'COUNT' },
            timeAxis: { column: '', granularity: 'DAY' },
            breakdown: '',
            chartType: 'kpi'
        },
        'ots_kpi_users': {
            baseTable: 'warehouse_tasks',
            joins: [],
            filters: [
                { column: 'warehouse_tasks.usuario', operator: 'isnotnull', value: '' },
                { column: 'warehouse_tasks.fe_creac', operator: 'contains', value: '2026' }
            ],
            metric: { column: 'warehouse_tasks.usuario', aggregation: 'COUNT_DISTINCT' },
            timeAxis: { column: '', granularity: 'MONTH' },
            breakdown: '',
            chartType: 'kpi'
        }
    };

    async function openEditQueryModal(queryId, chartTitle) {
        console.log("Studio: Abriendo modal para", queryId);
        currentQueryId = queryId;
        studioBoundParams = null;
        const modal = document.getElementById('modalEditQuery');
        if(!modal) {
            alert("Error crítico: No se encontró el elemento modalEditQuery en el DOM");
            return;
        }

        document.getElementById('editQueryId').value = queryId;
        document.getElementById('editQueryTitle').innerHTML = `Studio de Analíticas &bull; ${chartTitle}`;
        
        const queryTextEl = document.getElementById('editQueryText');
        queryTextEl.value = "-- Cargando consulta...";
        queryTextEl.disabled = true;
        
        modal.classList.add('show');
        
        // Carga asíncrona de datos
        await loadSchema();

        try {
            const response = await fetch(`/api/queries/${queryId}`);
            if (!response.ok) throw new Error("Status: " + response.status);
            const data = await response.json();

            // Caso A: query sin constructor visual (no tiene visual_state ni defaultVisualStates)
            // La API expone sql_text directamente → cargar en textarea y preview sin builder.
            const hasDefault = !!defaultVisualStates[queryId];
            if (!data.visual_state && !hasDefault && data.sql_text) {
                queryTextEl.value = data.sql_text;
                setTimeout(() => runPreview(), 300);
                return;
            }

            // Caso B: query con constructor visual → flujo normal
            // El textarea se rellena vía syncVisualToSQL() → build_sql API
            queryTextEl.value = "";

            // Guardar el visual state del servidor si existe
            if (data.visual_state) {
                try {
                    serverVisualState = JSON.parse(data.visual_state);
                } catch (e) {
                    serverVisualState = null;
                }
            } else {
                serverVisualState = null;
            }

            // Inicializar el Constructor Visual (usa serverVisualState o defaultVisualStates)
            initVisualQuery(queryId);

            // Compilar el estado visual a SQL internamente y lanzar preview
            syncVisualToSQL();

            setTimeout(() => runPreview(), 300);
        } catch (err) {
            console.error("Studio Load Error:", err);
            queryTextEl.value = "";
        } finally {
            queryTextEl.disabled = false;
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
                for (const table of Object.keys(currentSchema)) {
                    html += `<div class="table-nav-item" onclick="previewTable('${table}', this)">
                                <i class="fas fa-table"></i> ${table}
                            </div>`;
                }
                listEl.innerHTML = html;
                const firstTable = Object.keys(currentSchema)[0];
                if (firstTable) previewTable(firstTable, listEl.querySelector('.table-nav-item'));
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
            const response = await fetch('/api/studio/preview', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query_id: 'internal', sql_text: `SELECT * FROM ${tableName} LIMIT 5` })
            });
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
        const sql = document.getElementById('editQueryText').value;
        const errorEl = document.getElementById('previewError');
        errorEl.style.display = 'none';
        try {
            const response = await fetch('/api/studio/preview', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query_id: 'preview', sql_text: sql, params: studioBoundParams })
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

    function renderPreviewChart(data) {
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

        const chartType = document.getElementById('studioChartType').value;
        const primaryColor = document.getElementById('studioPrimaryColor').value;
        const keys = Object.keys(data[0]);
        const isPercent = !!(visualState && visualState.metric && visualState.metric.format === 'percent');
        const PALETTE = ['#22c55e','#3b82f6','#f59e0b','#ef4444','#8b5cf6','#06b6d4','#ec4899','#5DBAA9','#EA7600'];

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
        
        visualState = JSON.parse(JSON.stringify(state)); // Deep clone
        
        // Poblar baseTable select
        const baseSelect = document.getElementById('qbBaseTable');
        baseSelect.innerHTML = Object.keys(currentSchema).map(t => `<option value="${t}">${t}</option>`).join('');
        baseSelect.value = visualState.baseTable;
        
        renderJoins();
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
        
        syncVisualToSQL();
    }

    function onBaseTableChange() {
        visualState.baseTable = document.getElementById('qbBaseTable').value;
        visualState.joins = []; // Limpiar joins al cambiar tabla base
        renderJoins();
        refreshQbColumns(false);
        onQbChange();
    }

    function getActiveTables() {
        let tables = [visualState.baseTable];
        visualState.joins.forEach(j => {
            if (j.table && !tables.includes(j.table)) tables.push(j.table);
        });
        return tables;
    }

    function getActiveColumns() {
        let cols = [];
        getActiveTables().forEach(t => {
            (currentSchema[t] || []).forEach(c => {
                cols.push(`${t}.${c}`);
            });
        });
        return cols;
    }

    function refreshQbColumns(forceState = false) {
        const cols = getActiveColumns();
        
        // Eje Y dropdown
        const ySelect = document.getElementById('qbMetricColumn');
        const prevY = forceState ? visualState.metric.column : (ySelect.value || visualState.metric.column);
        ySelect.innerHTML = cols.map(c => `<option value="${c}">${c}</option>`).join('');
        if(cols.includes(prevY)) {
            ySelect.value = prevY;
            visualState.metric.column = prevY;
        } else {
            visualState.metric.column = ySelect.value;
        }
        
        // Eje X dropdown
        const xSelect = document.getElementById('qbTimeColumn');
        const prevX = forceState ? visualState.timeAxis.column : (xSelect.value || visualState.timeAxis.column);
        xSelect.innerHTML = '<option value="">-- Sin Eje X (Total Acumulado) --</option>' + cols.map(c => `<option value="${c}">${c}</option>`).join('');
        if(prevX === '' || cols.includes(prevX)) {
            xSelect.value = prevX;
            visualState.timeAxis.column = prevX;
        } else {
            xSelect.value = '';
            visualState.timeAxis.column = '';
        }

        // Desglose dropdown
        const bSelect = document.getElementById('qbBreakdownColumn');
        const prevB = forceState ? visualState.breakdown : (bSelect.value !== undefined ? bSelect.value : visualState.breakdown);
        bSelect.innerHTML = '<option value="">-- Sin Desglose --</option>' + cols.map(c => `<option value="${c}">${c}</option>`).join('');
        if(prevB === '' || cols.includes(prevB)) {
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
            sm2Select.innerHTML = cols.map(c => `<option value="${c}">${c}</option>`).join('');
            if (cols.includes(prevSM)) sm2Select.value = prevSM;
        }
    }

    // JOINS
    function renderJoins() {
        const container = document.getElementById('qbJoinsContainer');
        container.innerHTML = '';
        
        visualState.joins.forEach((j, index) => {
            const joinRow = document.createElement('div');
            joinRow.className = 'qb-form-row';
            joinRow.innerHTML = `
                <select class="qb-select j-table" onchange="updateJoin(${index})">
                    ${Object.keys(currentSchema).map(t => `<option value="${t}" ${t === j.table ? 'selected' : ''}>${t}</option>`).join('')}
                </select>
                <span style="color:#64748b; font-size:0.8rem;">ON</span>
                <select class="qb-select j-left" onchange="updateJoin(${index})">
                    ${getActiveColumns().map(c => `<option value="${c}" ${c === j.onLeft ? 'selected' : ''}>${c}</option>`).join('')}
                </select>
                <span style="color:#64748b; font-size:0.8rem;">=</span>
                <select class="qb-select j-right" onchange="updateJoin(${index})">
                    ${(currentSchema[j.table] || []).map(c => `<option value="${j.table}.${c}" ${`${j.table}.${c}` === j.onRight ? 'selected' : ''}>${j.table}.${c}</option>`).join('')}
                </select>
                <div class="qb-trash-btn" onclick="removeJoin(${index})"><i class="fas fa-trash"></i></div>
            `;
            container.appendChild(joinRow);
        });
    }

    function addJoin() {
        const nextTable = Object.keys(currentSchema).find(t => t !== visualState.baseTable) || visualState.baseTable;
        visualState.joins.push({
            table: nextTable,
            onLeft: getActiveColumns()[0] || '',
            onRight: `${nextTable}.${(currentSchema[nextTable] || [])[0] || ''}`
        });
        renderJoins();
        refreshQbColumns();
        onQbChange();
    }

    function updateJoin(index) {
        const row = document.getElementById('qbJoinsContainer').children[index];
        const prevTable = visualState.joins[index].table;
        const newTable = row.querySelector('.j-table').value;
        
        visualState.joins[index].table = newTable;
        
        // Si cambió la tabla de join, re-renderizar para actualizar columnas del ON derecho
        if (prevTable !== newTable) {
            visualState.joins[index].onRight = `${newTable}.${(currentSchema[newTable] || [])[0] || ''}`;
            renderJoins();
        } else {
            visualState.joins[index].onLeft = row.querySelector('.j-left').value;
            visualState.joins[index].onRight = row.querySelector('.j-right').value;
        }
        
        refreshQbColumns();
        onQbChange();
    }

    function removeJoin(index) {
        visualState.joins.splice(index, 1);
        renderJoins();
        refreshQbColumns();
        onQbChange();
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
                        ${getActiveColumns().map(c => `<option value="${c}" ${c === f.compareColumn ? 'selected' : ''}>${c}</option>`).join('')}
                    </select>
                `;
            } else if (valueType === 'date_diff') {
                valControlsHtml = `
                    <span style="font-size:0.8rem; color:var(--text-muted); align-self:center; margin:0 5px;">vs</span>
                    <select class="qb-select f-comp-col" onchange="updateFilter(${index})">
                        <option value="" disabled ${!f.compareColumn ? 'selected' : ''}>-- Columna --</option>
                        ${getActiveColumns().map(c => `<option value="${c}" ${c === f.compareColumn ? 'selected' : ''}>${c}</option>`).join('')}
                    </select>
                    <span style="font-size:0.8rem; color:var(--text-muted); align-self:center; margin:0 5px;">diff ≤</span>
                    <input type="number" class="qb-input f-offset" style="width:70px;" value="${f.offsetValue || '0'}" placeholder="Días" oninput="updateFilter(${index})">
                    <span style="font-size:0.8rem; color:var(--text-muted); align-self:center; margin:0 2px;">días</span>
                `;
            }

            const filterRow = document.createElement('div');
            filterRow.className = 'qb-form-row';
            filterRow.style = 'display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 8px;';
            filterRow.innerHTML = `
                <select class="qb-select f-col" style="flex: 1; min-width: 140px;" onchange="updateFilter(${index})">
                    ${getActiveColumns().map(c => `<option value="${c}" ${c === f.column ? 'selected' : ''}>${c}</option>`).join('')}
                </select>
                
                <select class="qb-select f-op" style="width: 130px;" onchange="updateFilter(${index})">
                    ${operators.map(o => `<option value="${o.value}" ${o.value === f.operator ? 'selected' : ''}>${o.label}</option>`).join('')}
                </select>
                
                ${isNullVal ? '' : `
                <select class="qb-select f-type" style="width: 140px;" onchange="updateFilterType(${index}, this.value)">
                    <option value="value" ${valueType === 'value' ? 'selected' : ''}>Valor Fijo</option>
                    <option value="column" ${valueType === 'column' ? 'selected' : ''}>Otra Columna</option>
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
            column: getActiveColumns()[0] || '',
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
            visualState.filters[index].compareColumn = getActiveColumns()[1] || getActiveColumns()[0] || '';
            visualState.filters[index].value = '';
            visualState.filters[index].offsetValue = null;
        } else if (type === 'date_diff') {
            visualState.filters[index].compareColumn = getActiveColumns()[1] || getActiveColumns()[0] || '';
            visualState.filters[index].value = '';
            visualState.filters[index].offsetValue = '2';
        } else {
            visualState.filters[index].compareColumn = null;
            visualState.filters[index].value = '';
            visualState.filters[index].offsetValue = null;
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
                visualState.filters[index].compareColumn = compEl ? compEl.value : '';
                visualState.filters[index].offsetValue = offsetEl ? offsetEl.value : '0';
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

        syncVisualToSQL();
    }

    async function syncVisualToSQL() {
        try {
            const response = await fetch('/api/studio/build_sql', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(visualState)
            });
            const data = await response.json();
            if (data.status === 'success') {
                document.getElementById('editQueryText').value = data.sql_text;
                studioBoundParams = data.bound_params;
                runPreview();
            }
        } catch (e) {
            console.error("Error sincronizando editor visual a SQL:", e);
        }
    }
