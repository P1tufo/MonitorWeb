/**
 * MonitorWeb — SLA Audit Table Logic
 */

function openPdfModal() {
    const modal = document.getElementById('pdfModal');
    if (modal) modal.classList.add('active');
}

function closePdfModal() {
    const modal = document.getElementById('pdfModal');
    if (modal) {
        modal.classList.remove('active');
        const frame = document.getElementById('pdfViewerFrame');
        if (frame) frame.src = "";
    }
}

function pdfSubmit(btn, frameTarget, preview) {
    const form = btn.closest('form');
    if (!form) return true;

    let actionInput = form.querySelector('.action_hidden');
    if (!actionInput) {
        actionInput = document.createElement('input');
        actionInput.type = 'hidden';
        actionInput.name = 'action';
        actionInput.className = 'action_hidden';
        form.appendChild(actionInput);
    }
    actionInput.value = btn.value;

    form.target = frameTarget;
    if (preview) openPdfModal();

    const orig = btn.innerHTML;
    // Debounce/Status feedback
    setTimeout(() => {
        btn.disabled = true;
        btn.style.opacity = "0.5";
        btn.innerHTML = "⏳...";
        setTimeout(() => {
            btn.disabled = false;
            btn.style.opacity = "1";
            btn.innerHTML = orig;
        }, 3000);
    }, 10);
    
    return true;
}

// Expose to window for inline handlers
window.pdfSubmit = pdfSubmit;
window.closePdfModal = closePdfModal;
