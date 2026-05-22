(() => {
    /**
     * MonitorWeb — Warehouse Tasks (OTs) Analytics Logic
     */

    const log = (msg, data = null) => {
        console.log(`[Tasks-JS] ${msg}`, data || '');
    };

    const getData = (id) => {
        const el = document.getElementById(id);
        if (!el) return null;
        try {
            return JSON.parse(el.textContent);
        } catch (e) {
            log(`Error parsing ${id}`, e);
            return null;
        }
    };

    document.addEventListener('DOMContentLoaded', () => {
        log('Initializing OT charts with high-contrast text and premium styling...');

        // 1. Trend Chart (Line)
        try {
            const labels = getData('data_ots_trend_labels') || [];
            const createdData = getData('data_ots_trend_created') || [];
            const confirmedData = getData('data_ots_trend_confirmed') || [];
            const ctx = document.getElementById('otsTrendChart');
            if (ctx && labels.length > 0) {
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Creadas',
                                data: createdData,
                                borderColor: '#5DBAA9',
                                backgroundColor: 'rgba(93, 186, 169, 0.1)',
                                borderWidth: 3,
                                tension: 0.3,
                                fill: true
                            },
                            {
                                label: 'Confirmadas',
                                data: confirmedData,
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
                            legend: {
                                display: true,
                                labels: {
                                    color: '#f8fafc',
                                    font: { family: 'Outfit', size: 12, weight: '600' }
                                }
                            },
                            tooltip: {
                                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                                titleColor: '#f8fafc',
                                bodyColor: '#cbd5e1',
                                borderColor: 'rgba(255, 255, 255, 0.1)',
                                borderWidth: 1,
                                padding: 10,
                                bodyFont: { family: 'Outfit', size: 12 },
                                titleFont: { family: 'Outfit', size: 12, weight: 'bold' }
                            },
                            datalabels: {
                                display: true,
                                align: 'top',
                                anchor: 'end',
                                color: '#ffffff',
                                offset: 4,
                                font: {
                                    family: 'Outfit',
                                    weight: 'bold',
                                    size: 11
                                },
                                formatter: (val) => val
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: { color: 'rgba(255,255,255,0.08)' },
                                ticks: {
                                    color: '#cbd5e1',
                                    font: { family: 'Outfit', size: 11 }
                                }
                            },
                            x: {
                                grid: { display: false },
                                ticks: {
                                    color: '#cbd5e1',
                                    font: { family: 'Outfit', size: 11 }
                                }
                            }
                        }
                    },
                    plugins: [ChartDataLabels]
                });
            }
        } catch (e) { log('Error in Trend Chart', e); }


        // 3. User Chart (Bar)
        try {
            const labels = getData('data_ots_user_labels') || [];
            const createdData = getData('data_ots_user_created') || [];
            const confirmedData = getData('data_ots_user_confirmed') || [];
            const ctx = document.getElementById('otsUserChart');
            if (ctx && labels.length > 0) {
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            {
                                label: 'Creadas',
                                data: createdData,
                                backgroundColor: 'rgba(93, 186, 169, 0.7)',
                                borderRadius: 6
                            },
                            {
                                label: 'Confirmadas',
                                data: confirmedData,
                                backgroundColor: 'rgba(234, 118, 0, 0.7)',
                                borderRadius: 6
                            }
                        ]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        indexAxis: 'y',
                        plugins: {
                            legend: {
                                display: true,
                                labels: {
                                    color: '#f8fafc',
                                    font: { family: 'Outfit', size: 12, weight: '600' }
                                }
                            },
                            tooltip: {
                                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                                titleColor: '#f8fafc',
                                bodyColor: '#cbd5e1',
                                borderColor: 'rgba(255, 255, 255, 0.1)',
                                borderWidth: 1,
                                padding: 10,
                                bodyFont: { family: 'Outfit', size: 12 },
                                titleFont: { family: 'Outfit', size: 12, weight: 'bold' }
                            },
                            datalabels: {
                                display: false
                            }
                        },
                        scales: {
                            x: {
                                beginAtZero: true,
                                grid: { color: 'rgba(255,255,255,0.08)' },
                                ticks: {
                                    color: '#cbd5e1',
                                    font: { family: 'Outfit', size: 11 }
                                }
                            },
                            y: {
                                grid: { display: false },
                                ticks: {
                                    color: '#cbd5e1',
                                    font: { family: 'Outfit', size: 11 }
                                }
                            }
                        }
                    }
                });
            }
        } catch (e) { log('Error in User Chart', e); }
    });

})();
