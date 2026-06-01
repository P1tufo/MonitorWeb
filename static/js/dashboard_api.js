/**
 * MonitorWeb — Dashboard Core Logic
 */

// ── API MODULE ──────────────────────────────────────────────────────────

const DashboardAPI = {
    async _fetch(url, options = {}) {
        const res = await fetch(url, options);
        if (res.status === 401) {
            // Limpiar localStorage y redirigir
            localStorage.removeItem('monitorweb_token');
            window.location.href = '/login';
            return null;
        }
        return res;
    },

    async fetchKPIs(params) {
        const query = new URLSearchParams(params).toString();
        try {
            const res = await this._fetch(`/api/kpis?${query}`);
            return res ? await res.json() : null;
        } catch (e) {
            console.error("Error fetching KPIs:", e);
            return null;
        }
    },

    async fetchFilteredData(params) {
        const query = new URLSearchParams(params).toString();
        try {
            const res = await this._fetch(`/filter?${query}`);
            return res ? await res.json() : [];
        } catch (e) {
            console.error("Error fetching filtered data:", e);
            return [];
        }
    },

    async sync() {
        const res = await this._fetch('/sync', { method: 'POST' });
        return res ? await res.json() : { status: 'error', message: 'No autorizado' };
    },

    async checkSyncStatus() {
        try {
            const res = await this._fetch('/sync/status');
            return res ? await res.json() : { is_syncing: false };
        } catch (e) {
            return { is_syncing: false };
        }
    },

    async logout() {
        try {
            await fetch('/api/auth/logout', { method: 'POST' });
            localStorage.clear();
            window.location.reload();
        } catch (e) {
            window.location.reload();
        }
    }
};

// ── UI & MODAL HELPERS ──────────────────────────────────────────────────

const UI = {
    openPdfModal() {
        document.getElementById('pdfModal').classList.add('active');
    },
    closePdfModal() {
        document.getElementById('pdfModal').classList.remove('active');
        document.getElementById('pdfViewerFrame').src = "";
    },
    toggleMulti(id) {
        const el = document.getElementById(id);
        el.classList.toggle('show');
    },
    setBtnLoading(btn, text, isLoading) {
        if (!btn) return;
        if (isLoading) {
            btn.dataset.originalHtml = btn.innerHTML;
            btn.innerHTML = `⏳ ${text}...`;
            btn.disabled = true;
            btn.style.opacity = "0.7";
        } else {
            btn.innerHTML = btn.dataset.originalHtml || btn.innerHTML;
            btn.disabled = false;
            btn.style.opacity = "1";
        }
    }
};
// Global click listener for multiselects
document.addEventListener('click', (e) => {
    if (!e.target.closest('.multiselect')) {
        document.querySelectorAll('.checkboxes').forEach(c => c.classList.remove('show'));
    }
});

