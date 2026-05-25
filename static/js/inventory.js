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
        UI.renderMaterialModal({ modalId: 'modalUser', titleId: 'modalUserTitle', listId: 'modalUserList', title: `Usuario: ${name}`, items: data[name] || [], colorVar: '--naranja', bgColor: 'rgba(234,118,0,0.15)' });
    };

    document.addEventListener('DOMContentLoaded', () => {
        // Los gráficos asíncronos ahora son dibujados y manejados por saas_engine.js
        // (Fase 3: Analytics Studio SDUI).
        log('Inventory module loaded. Awaiting SaaS Widgets...');

        // Exponer función de switch de vista
        window.switchInventarioView = (view) => {
            const gran = view === 'historical' ? 'WEEK' : '';
            
            // Obtener valores actuales
            const areaAll = document.getElementById('chartAreaFilterAll')?.checked;
            const areaValues = areaAll ? '' : Array.from(document.querySelectorAll('.chart-area-cb:checked')).map(cb => cb.value).join(',');
            
            const params = {
                area: areaValues,
                year: new Date().getFullYear().toString()
            };
            if (gran) params.granularity = gran;
            
            const invTab = document.getElementById('tab-inventory');
            if (invTab && window.initSaaSWidgetsV2) {
                window.initSaaSWidgetsV2(params, invTab);
            }
        };

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

// Funciones obsoletas de filtrado han sido eliminadas por el rediseño SaaS.