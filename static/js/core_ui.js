/**
 * MonitorWeb — Core UI Module (core_ui.js)
 *
 * Módulo de utilidades de UI compartidas por todas las vistas.
 * Debe cargarse ANTES de cualquier otro JS de dominio (deliveries.js,
 * inventory.js, analytics_proyecciones.js, etc.).
 *
 * Expone window.CoreUI con las funciones comunes para que los módulos
 * de dominio puedan delegar sin redefinir la lógica localmente.
 *
 * ── Funciones disponibles ──────────────────────────────────────────────
 *  CoreUI.openModal(id)              — Muestra un modal por su ID de elemento
 *  CoreUI.closeModal(id)             — Oculta un modal por su ID de elemento
 *  CoreUI.renderMaterialModal(opts)  — Rellena y abre un modal de lista de materiales
 *  CoreUI.populateAreaSelect(...)    — Rellena un <select> con áreas únicas de un array
 *  CoreUI.getData(id)                — Lee y parsea JSON embebido en un <script> o <span>
 * ──────────────────────────────────────────────────────────────────────
 */

window.CoreUI = (() => {

    // ── Modal helpers ──────────────────────────────────────────────────

    /**
     * Muestra un elemento modal añadiendo la clase CSS 'show'.
     * @param {string} id - ID del elemento DOM del modal.
     */
    function openModal(id) {
        const el = document.getElementById(id);
        if (el) el.classList.add('show');
    }

    /**
     * Oculta un elemento modal quitando la clase CSS 'show'.
     * @param {string} id - ID del elemento DOM del modal.
     */
    function closeModal(id) {
        const el = document.getElementById(id);
        if (el) el.classList.remove('show');
    }

    // ── Material modal renderer ────────────────────────────────────────

    /**
     * Rellena un modal de lista de materiales con los ítems proporcionados
     * y lo abre automáticamente.
     *
     * @param {object} opts
     * @param {string}   opts.modalId   - ID del elemento modal a abrir.
     * @param {string}   opts.titleId   - ID del elemento de título del modal.
     * @param {string}   opts.listId    - ID del elemento <ul> donde renderizar los ítems.
     * @param {string}   opts.title     - Texto del título a mostrar.
     * @param {Array}    opts.items     - Array de objetos { cod_mat, material, qty_fmt?, total_qty? }.
     * @param {string}  [opts.colorVar] - Variable CSS para el color del score (ej: '--naranja').
     * @param {string}  [opts.bgColor]  - Color de fondo inline para el score (ej: 'rgba(...)').
     */
    function renderMaterialModal({ modalId, titleId, listId, title, items, colorVar, bgColor }) {
        const titleEl = document.getElementById(titleId);
        const listEl  = document.getElementById(listId);

        if (titleEl) titleEl.innerHTML = title;

        if (!items || items.length === 0) {
            if (listEl) {
                listEl.innerHTML = '<li style="text-align:center; color:#64748b; font-style:italic; padding: 2rem;">No hay registros para esta selección.</li>';
            }
        } else {
            const html = items.map(mat => `
                <li>
                    <div>
                        <div class="name" style="font-size: 1rem;">
                            <span style="color:var(--primario);font-size:0.85rem;">[${mat.cod_mat}]</span> ${mat.material}
                        </div>
                    </div>
                    <div class="score" style="font-size: 1.1rem; ${colorVar ? `color: var(${colorVar});` : ''} ${bgColor ? `background: ${bgColor};` : ''}">
                        ${mat.qty_fmt || mat.total_qty || 0} req.
                    </div>
                </li>
            `).join('');
            if (listEl) listEl.innerHTML = html;
        }

        openModal(modalId);
    }

    // ── Area select populator ──────────────────────────────────────────

    /**
     * Rellena un elemento <select> con las áreas únicas encontradas en un array de datos.
     * No añade opciones si el select ya fue inicializado (más de 1 opción presente).
     *
     * @param {string} selectId  - ID del elemento <select>.
     * @param {Array}  data      - Array de objetos con la clave de área.
     * @param {string} [key]     - Nombre de la propiedad del área en cada objeto (default: 'area').
     */
    function populateAreaSelect(selectId, data, key = 'area') {
        const select = document.getElementById(selectId);
        if (!select || select.options.length > 1) return;

        const areaSet = new Set();
        data.forEach(item => {
            if (item[key] && item[key] !== 'Área Desconocida' && item[key] !== 'Desconocida') {
                areaSet.add(item[key]);
            }
        });

        Array.from(areaSet).sort().forEach(area => {
            const opt = document.createElement('option');
            opt.value = area;
            opt.textContent = area;
            select.appendChild(opt);
        });
    }

    // ── Data reader ───────────────────────────────────────────────────

    /**
     * Lee y parsea JSON embebido en el textContent de un elemento del DOM.
     * Usado para leer datos inyectados por Jinja2 como <script type="application/json">.
     *
     * @param {string} id - ID del elemento que contiene el JSON.
     * @returns {*} El dato parseado, o null si el elemento no existe o el JSON es inválido.
     */
    function getData(id) {
        const el = document.getElementById(id);
        if (!el) return null;
        try {
            const txt = el.textContent.trim();
            if (!txt) return null;
            return JSON.parse(txt);
        } catch (e) {
            console.warn(`[CoreUI] Error parseando JSON en #${id}:`, e);
            return null;
        }
    }

    // ── Public API ────────────────────────────────────────────────────

    return { openModal, closeModal, renderMaterialModal, populateAreaSelect, getData };

})();

// Alias globales directos para compatibilidad con handlers inline (onclick="openModal(...)")
window.openModal  = CoreUI.openModal.bind(CoreUI);
window.closeModal = CoreUI.closeModal.bind(CoreUI);
