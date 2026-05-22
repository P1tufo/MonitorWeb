const stackedTotalPlugin = {
    id: 'stackedTotal',
    afterDatasetsDraw: (chart) => {
        const { ctx, scales: { x, y } } = chart;
        chart.data.labels.forEach((label, i) => {
            let total = 0;
            chart.data.datasets.forEach(dataset => {
                const meta = chart.getDatasetMeta(chart.data.datasets.indexOf(dataset));
                if (!meta.hidden && dataset.data[i]) total += dataset.data[i];
            });
            if (total > 0) {
                let topY = y.bottom;
                for (let j = chart.data.datasets.length - 1; j >= 0; j--) {
                    const meta = chart.getDatasetMeta(j);
                    if (!meta.hidden && meta.data[i]) { topY = meta.data[i].y; break; }
                }
                ctx.save();
                ctx.textAlign = 'center'; ctx.fillStyle = '#f8f9fa';
                ctx.font = 'bold 12px Inter, sans-serif';
                ctx.fillText(total, x.getPixelForTick(i), topY - 8);
                ctx.restore();
            }
        });
    }
};

function initWeeklyChart(chartLabels, chartDatasets) {
    const ctx = document.getElementById('weeklyChart').getContext('2d');
    window.weeklyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartLabels,
            datasets: chartDatasets
        },
        plugins: [stackedTotalPlugin],
        options: {
            responsive: true, maintainAspectRatio: false,
            layout: {
                padding: {
                    top: 25,
                    bottom: 10
                }
            },
            plugins: {
                legend: { labels: { color: '#f8f9fa' } },
                tooltip: { mode: 'index', intersect: false }
            },
            scales: {
                y: { stacked: true, beginAtZero: true, grace: '15%', ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } },
                x: { stacked: true, ticks: { color: '#94a3b8' }, grid: { display: false } }
            }
        }
    });
}

// Selectores persistentes para evitar búsquedas repetitivas en el DOM
const getChartAreaCbs = () => document.querySelectorAll('.chart-area-cb');
const getAreaCbs = () => document.querySelectorAll('.area-cb');

function toggleChartSelectAll(isChecked) {
    // Si isChecked es falso, la lógica original parece que forzaba el true (o era un bug)
    // Pero seguiremos la recomendación de usar el valor de isChecked para simplificar.
    const chartAreaCbs = getChartAreaCbs();
    const areaCbs = getAreaCbs();
    
    chartAreaCbs.forEach(cb => cb.checked = isChecked);
    areaCbs.forEach(cb => cb.checked = isChecked);
    
    const selAreaAll = document.getElementById('areaFilterAll');
    if (selAreaAll) selAreaAll.checked = isChecked;
    
    updateChartVisibility();
    if (typeof applyFilters === 'function') applyFilters();
}

function updateChartVisibility() {
    const chartAreaCbs = getChartAreaCbs();
    const allChecked = chartAreaCbs.length > 0 && Array.from(chartAreaCbs).every(cb => cb.checked);
    
    const selAll = document.getElementById('chartAreaFilterAll');
    if (selAll) selAll.checked = allChecked;

    const selectedValues = Array.from(chartAreaCbs)
        .filter(cb => cb.checked)
        .map(cb => cb.value);

    if (window.weeklyChart) {
        window.weeklyChart.data.datasets.forEach((ds, i) => {
            window.weeklyChart.setDatasetVisibility(i, selectedValues.includes(ds.label));
        });
        window.weeklyChart.update();
    }
}


document.addEventListener('DOMContentLoaded', function() {
    const centroAll = document.getElementById('centroAll');
    if (centroAll) centroAll.checked = true;

    const otAll = document.querySelector('input[name="ot-filter"][value=""]');
    if (otAll) otAll.checked = true;

    document.querySelectorAll('.chart-area-cb').forEach(cb => cb.checked = true);
    const chartAll = document.getElementById('chartAreaFilterAll');
    if (chartAll) chartAll.checked = true;

    document.querySelectorAll('.area-cb').forEach(cb => cb.checked = true);
    const areaAll = document.getElementById('areaFilterAll');
    if (areaAll) areaAll.checked = true;

    // Load chart if data exists
    const labelsEl = document.getElementById('chart-data-labels');
    const datasetsEl = document.getElementById('chart-data-datasets');
    if (labelsEl && datasetsEl) {
        initWeeklyChart(JSON.parse(labelsEl.textContent), JSON.parse(datasetsEl.textContent));
    }
});
