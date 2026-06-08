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
        
        let customMacros = '';
        if (visualState.baseTable === 'movimientos') {
            customMacros += '<option value="__PLAN_VS_UNPLAN__">Macro: Planificado vs Desplanificado</option>';
            customMacros += '<option value="__ABAST_VS_CONSUMO__">Macro: Abastecimiento vs Consumo</option>';
            customMacros += '<option value="__PROD_VS_MANT__">Macro: Producción vs Mantención</option>';
        }
        if (visualState.baseTable === 'entregas' || visualState.baseTable === 'movimientos' || visualState.baseTable === 'outbound_deliveries') {
            customMacros += '<option value="__AREA_EXPR__">Macro: Área de Negocio Compleja</option>';
        }

        bSelect.innerHTML = '<option value="">-- Sin Desglose --</option>' + renderOptions(colsObj) + customMacros;
        
        const isMacro = prevB && prevB.startsWith('__');
        if(prevB === '' || colsIds.includes(prevB) || isMacro) {
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
