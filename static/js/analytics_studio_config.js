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
            timeAxis: { column: 'dim_fecha', granularity: 'DAY' },
            breakdown: '',
            chartType: 'line'
        },
        'ots_by_movement_type': {
            baseTable: 'tareas',
            joins: [],
            filters: [{ column: 'dim_clase_mov', operator: 'isnotnull', value: '' }],
            metric: { column: 'met_tareas', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: 'dim_clase_mov',
            chartType: 'pie'
        },
        'ots_by_user_dual': {
            baseTable: 'tareas',
            joins: [],
            filters: [],
            metric: { column: 'met_tareas', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: 'dim_usuario',
            chartType: 'bar'
        },
        'inv_volumen_stats': {
            baseTable: 'movimientos',
            joins: [],
            filters: [],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha', granularity: 'DAY' },
            breakdown: 'dim_tipo_operacion',
            chartType: 'bar'
        },
        'inv_consumos_quick': {
            baseTable: 'movimientos',
            joins: [],
            filters: [{ column: 'met_movimientos', operator: 'isnotnull', value: '' }],
            metric: { column: 'met_cantidad', aggregation: 'SUM' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
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
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: 'dim_ce_coste',
            chartType: 'bar'
        },
        'inv_consumos_abc': {
            baseTable: 'movimientos',
            joins: [],
            filters: [],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: 'dim_texto_breve',
            chartType: 'bar'
        },
        'inv_dow_stats': {
            baseTable: 'movimientos',
            joins: [],
            filters: [],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha', granularity: 'DAY' },
            breakdown: '',
            chartType: 'line'
        },
        'inv_cmv_201_mensual': {
            baseTable: 'movimientos',
            joins: [],
            filters: [{ column: 'dim_cmv', operator: 'equals', value: '201', valueType: 'value' }],
            metric: { column: 'met_movimientos', aggregation: 'COUNT', label: 'Consumos 201' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: '__PLAN_VS_UNPLAN__',
            chartType: 'line'
        },
        'inv_cmv_261_221_mensual': {
            baseTable: 'movimientos',
            joins: [],
            filters: [{ column: 'dim_cmv', operator: 'in', value: '261,221', valueType: 'value' }],
            metric: { column: 'met_movimientos', aggregation: 'COUNT', label: 'Consumos 261/221' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: '__PLAN_VS_UNPLAN__',
            chartType: 'line'
        },
        'inv_pm_type_records': {
            baseTable: 'movimientos',
            joins: [],
            filters: [],
            metric: { column: 'met_cantidad', aggregation: 'SUM' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: 'dim_tipo_operacion',
            chartType: 'bar'
        },
        'inv_location_summary': {
            baseTable: 'movimientos',
            joins: [],
            filters: [],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
            breakdown: 'dim_alm',
            chartType: 'bar'
        },
        'inv_top_users': {
            baseTable: 'movimientos',
            joins: [],
            filters: [],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: 'dim_fecha', granularity: 'MONTH' },
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
            filters: [
                { column: 'dim_cmv', operator: 'in', value: '101, 305' },
                { column: 'dim_fecha', operator: 'contains', value: '2026' }
            ],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_consumos_prod': {
            baseTable: 'movimientos',
            joins: [],
            filters: [
                { column: 'dim_cmv', operator: 'in', value: '201' },
                { column: 'dim_fecha', operator: 'contains', value: '2026' }
            ],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_consumos_mant': {
            baseTable: 'movimientos',
            joins: [],
            filters: [
                { column: 'dim_cmv', operator: 'in', value: '261' },
                { column: 'dim_fecha', operator: 'contains', value: '2026' }
            ],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_rate_reabast': {
            baseTable: 'movimientos',
            joins: [],
            filters: [{ column: 'dim_fecha', operator: 'contains', value: '2026' }],
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
                { column: 'dim_fecha', operator: 'contains', value: '2026' }
            ],
            metric: { column: 'met_movimientos', aggregation: 'COUNT' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_rate_devolucion': {
            baseTable: 'movimientos',
            joins: [],
            filters: [{ column: 'dim_fecha', operator: 'contains', value: '2026' }],
            metric: { column: 'met_return_rate', aggregation: 'RETURN_RATE', format: 'percent' },
            timeAxis: { column: '', granularity: 'YEAR' },
            breakdown: '',
            chartType: 'kpi'
        },
        'inv_kpi_rate_eficiencia': {
            baseTable: 'movimientos',
            joins: [],
            filters: [{ column: 'dim_fecha', operator: 'contains', value: '2026' }],
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
                { column: 'dim_fecha', operator: 'contains', value: '2026' }
            ],
            metric: { column: 'dim_usuario', aggregation: 'COUNT_DISTINCT' },
            timeAxis: { column: '', granularity: 'MONTH' },
            breakdown: '',
            chartType: 'kpi'
        }
    };
