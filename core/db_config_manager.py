"""
core/db_config_manager.py — Administrador de configuraciones dinámicas SaaS.

Esta capa es el punto de acceso a la configuración WMS en tiempo de ejecución.

Arquitectura (Pilar 3 — ORM):
  - Lee y escribe usando SQLAlchemy (models.py) → portátil a PostgreSQL.
  - Mantiene una caché en memoria para rendimiento ultra-rápido en hot paths
    (ej. map_wms_status() se llama por cada fila procesada).
  - La API pública (get_status_mapping, get_cost_center_mapping, etc.)
    no cambia → compatibilidad total con el resto del código.

Inicialización:
  - `init_config_db()`  → crea tablas via SQLAlchemy si no existen.
  - `seed_initial_config()` → inserta valores por defecto la primera vez.
  - `load_config_to_memory()` → rellena la caché desde la BD.
"""
import logging
from typing import Dict, Any, Optional, List

from sqlalchemy import inspect
from sqlalchemy.orm import Session

from .database import engine, get_session, Base
from .models import StatusMapping, CostCenterMapping, AppSetting, Holiday, ConfigQuery

logger = logging.getLogger("db-config")



# ─── INICIALIZACIÓN ────────────────────────────────────────────────────────────
def init_config_db():
    """
    Crea las tablas de configuración SaaS via SQLAlchemy si no existen.
    Idempotente: seguro llamarlo en cada startup.
    """
    Base.metadata.create_all(bind=engine)
    
    # Asegurar que exista la columna 'visual_state' en 'config_queries' para instalaciones existentes
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE config_queries ADD COLUMN visual_state TEXT"))
            conn.commit()
            logger.info("Columna 'visual_state' añadida a 'config_queries' exitosamente.")
    except Exception:
        # Ya existe la columna o la tabla no está creada aún (se creará con metadata.create_all)
        pass
        
    logger.debug("Tablas de configuración SaaS verificadas/creadas via ORM.")


def seed_initial_config():
    """
    Inserta los valores por defecto si las tablas están vacías.
    Se ejecuta solo en el primer arranque (idempotente por INSERT OR IGNORE vía merge).
    """
    with get_session() as session:
        logger.debug("Verificando configuraciones iniciales (SaaS ORM Seed)...")

        logger.debug("Poblando BD con configuraciones iniciales (SaaS ORM Migration)...")

        # ── Mapeo de estados ──────────────────────────────────────────────────
        initial_statuses = [
            StatusMapping(code="000", label="---"),
            StatusMapping(code="A0A", label="NO Tratada"),
            StatusMapping(code="BCA", label="OT Abierta"),
            StatusMapping(code="C0A", label="OT Abierta"),
            StatusMapping(code="CCA", label="OT Abierta"),
            StatusMapping(code="CCC", label="Contabilizado"),
            StatusMapping(code="00C", label="Contabilizado Cero"),
            StatusMapping(code="CA",  label="OT Abierta"),
            StatusMapping(code="AA",  label="NO Tratada"),
            StatusMapping(code="BA",  label="OT Abierta"),
        ]
        for obj in initial_statuses:
            if not session.query(StatusMapping).filter_by(code=obj.code).first():
                session.add(obj)

        # ── Centros de costo ──────────────────────────────────────────────────
        initial_cost_centers = [
            CostCenterMapping(center_code="TMCHO1", business_area="VIGAS"),
            CostCenterMapping(center_code="TMCHO2", business_area="REMANUFACTURA"),
            CostCenterMapping(center_code="TSCHO1", business_area="ASERRADERO"),
            CostCenterMapping(center_code="MOLTR1", business_area="MOLDURAS"),
            CostCenterMapping(center_code="PATRU1", business_area="LINEA 1"),
            CostCenterMapping(center_code="PATRU2", business_area="LINEA 2"),
            CostCenterMapping(center_code="PAGEN1", business_area="PLANTA_ENERGIA"),
            CostCenterMapping(center_code="PATAV1", business_area="RANURADO"),
        ]
        for obj in initial_cost_centers:
            if not session.query(CostCenterMapping).filter_by(center_code=obj.center_code).first():
                session.add(obj)

        # ── Settings de procesamiento ─────────────────────────────────────────
        initial_settings = [
            AppSetting(key="HEADER_DENSITY_THRESHOLD", value="0.5",   type="float"),
            AppSetting(key="HEADER_MIN_COLS",          value="5",     type="int"),
            AppSetting(key="HEADER_SCAN_LIMIT",        value="50",    type="int"),
            AppSetting(key="DEFAULT_ENCODING",         value="utf-8", type="str"),
            AppSetting(key="DEFAULT_SEPARATOR",        value="\t",    type="str"),
            AppSetting(key="MAX_COLUMN_BUFFER",        value="100",   type="int"),
            AppSetting(key="CMV_PROD",                 value="201",   type="str"),
            AppSetting(key="CMV_MANT",                 value="261",   type="str"),
            AppSetting(key="CMV_PROD_REV",             value="202",   type="str"),
            AppSetting(key="CMV_MANT_REV",             value="262",   type="str"),
            AppSetting(key="CMV_REVERSAS",             value="202,262,102,302,304", type="str"),
            AppSetting(key="ONEDRIVE_PATH",            value="/Users/christianykelly/Library/CloudStorage/OneDrive-ARAUCO/Escritorio/Transacciones", type="str"),
            AppSetting(key="DIR_DELIVERIES",                value="VL06O", type="str"),
            AppSetting(key="DIR_STOCK",                 value="LX02",  type="str"),
            AppSetting(key="DIR_TASKS",                 value="LT22",  type="str"),
            AppSetting(key="DIR_MOVEMENTS",                 value="MB51",  type="str"),
            AppSetting(key="DIR_LX02_PENDIENTES",       value="LX02_Pendientes",  type="str"),
            AppSetting(key="SLA_THRESHOLD",            value="2",     type="int"),
            AppSetting(key="AREA_DEFAULT",             value="OTRO",  type="str"),
        ]
        for obj in initial_settings:
            if not session.query(AppSetting).filter_by(key=obj.key).first():
                session.add(obj)

        # ── Feriados ──────────────────────────────────────────────────────────
        holiday_dates = [
            # 2024
            "2024-01-01","2024-03-29","2024-03-30","2024-05-01","2024-05-21",
            "2024-06-09","2024-06-20","2024-06-29","2024-07-16","2024-08-15",
            "2024-09-18","2024-09-19","2024-09-20","2024-10-12","2024-10-27",
            "2024-10-31","2024-11-01","2024-12-08","2024-12-25",
            # 2025
            "2025-01-01","2025-04-18","2025-04-19","2025-05-01","2025-05-21",
            "2025-06-20","2025-06-29","2025-07-16","2025-08-15","2025-09-18",
            "2025-09-19","2025-10-12","2025-10-31","2025-11-01","2025-12-08","2025-12-25",
            # 2026
            "2026-01-01","2026-04-03","2026-04-04","2026-05-01","2026-05-21",
            "2026-06-20","2026-06-29","2026-07-16","2026-08-15","2026-09-18",
            "2026-09-19","2026-10-12","2026-10-31","2026-11-01","2026-12-08","2026-12-25",
        ]
        for d in holiday_dates:
            if not session.query(Holiday).filter_by(date_str=d).first():
                session.add(Holiday(date_str=d))

        # ── Consultas SQL ─────────────────────────────────────────────────────
        initial_queries = [
            ConfigQuery(
                query_id="inv_volumen_stats",
                sql_text="SELECT tipo_operacion, COUNT(material) as total_qty, COUNT(*) as num_tx FROM inventory_movements GROUP BY tipo_operacion ORDER BY total_qty DESC"
            ),
            ConfigQuery(
                query_id="inv_area_stats_prod",
                sql_text="SELECT COALESCE(ce_coste, 'OTRO') as area, COUNT(material) as num_tx, SUM(cantidad) as sum_qty, COUNT(DISTINCT fe_contab) as active_days FROM inventory_movements WHERE cmv = ? GROUP BY area ORDER BY num_tx DESC"
            ),
            ConfigQuery(
                query_id="inv_consumos_abc",
                sql_text="SELECT material as cod_mat, texto_breve_material as material, COUNT(material) as qty FROM inventory_movements WHERE cmv IN (?, ?) AND material IS NOT NULL AND material != '' GROUP BY cod_mat, material ORDER BY qty DESC"
            ),
            # ── Entregas (Nuevas dinámicas) ───────────────────────────────────
            ConfigQuery(
                query_id="vl_monthly_evolution",
                sql_text="""SELECT 
                    substr(fecha_carga,7,4) as year,
                    substr(fecha_carga,4,2) as month,
                    substr(fecha_carga,7,4) || '-' || substr(fecha_carga,4,2) as label,
                    COUNT(DISTINCT entrega) as entregas,
                    COUNT(DISTINCT fecha_carga) as dias_activos
                FROM outbound_deliveries
                WHERE fecha_carga IS NOT NULL AND fecha_carga != ''
                GROUP BY year, month
                ORDER BY year ASC, month ASC"""
            ),
            ConfigQuery(
                query_id="vl_weekly_evolution",
                sql_text="""SELECT 
                    week_sort,
                    MAX(week_label) as label,
                    COUNT(DISTINCT entrega) as entregas
                FROM outbound_deliveries
                WHERE week_sort IS NOT NULL AND week_sort != ''
                GROUP BY week_sort
                ORDER BY week_sort ASC"""
            ),
            ConfigQuery(
                query_id="vl_top_locations",
                sql_text="""SELECT 
                    {AREA_EXPR} as area, 
                    v.ubicacion_bin as ubicacion, 
                    v.material, 
                    v.denominacion as texto_breve_de_material,
                    COUNT(*) as num_items 
                FROM outbound_deliveries v
                WHERE v.ubicacion_bin IS NOT NULL AND v.ubicacion_bin != '' AND v.fecha_carga LIKE ?
                GROUP BY area, v.ubicacion_bin, v.material, texto_breve_de_material 
                HAVING area IS NOT NULL
                ORDER BY num_items DESC 
                LIMIT 100"""
            ),
            ConfigQuery(
                query_id="inv_dow_stats",
                sql_text="SELECT CAST(strftime('%w', substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) || '-' || substr(fe_contab, 1, 2)) AS INTEGER) as dow, COUNT(material) as qty FROM inventory_movements WHERE cmv IN (?, ?) AND length(fe_contab) >= 10 GROUP BY dow"
            ),
            ConfigQuery(
                query_id="inv_pm_type_records",
                sql_text="SELECT CASE WHEN cmv = ? THEN 'Producción' ELSE 'Mantención' END as type, material as cod_mat, texto_breve_material as material, COUNT(material) as qty FROM inventory_movements WHERE cmv IN (?, ?) GROUP BY type, cod_mat, material ORDER BY qty DESC"
            ),
            ConfigQuery(
                query_id="inv_area_material_prod",
                sql_text="SELECT COALESCE(ce_coste, 'OTRO') as area, material as cod_mat, texto_breve_material as material, COUNT(*) as qty FROM inventory_movements WHERE cmv = ? GROUP BY area, cod_mat, material ORDER BY qty DESC"
            ),
            ConfigQuery(
                query_id="inv_location_summary",
                sql_text="SELECT COALESCE(alm, 'S/U') as ubi, material as cod_mat, texto_breve_material as material, COUNT(*) as total_qty FROM inventory_movements WHERE alm IS NOT NULL AND alm != '' GROUP BY ubi, cod_mat, material ORDER BY total_qty DESC"
            ),
            ConfigQuery(
                query_id="inv_top_users",
                sql_text="""SELECT usuario as user, COUNT(material) as qty 
                FROM inventory_movements 
                WHERE usuario IS NOT NULL AND usuario != '' 
                GROUP BY user ORDER BY qty DESC LIMIT 10"""
            ),
            # ── Nuevas consultas SLA (Deliveries) ──────────────────────────────
            ConfigQuery(
                query_id="vl_sla_monthly_trend",
                sql_text="""SELECT 
  substr(outbound_deliveries.fecha_carga, 7, 4) || '-' || substr(outbound_deliveries.fecha_carga, 4, 2) AS fecha,
  ROUND(SUM(CASE WHEN outbound_deliveries.dias_retraso <= 2 THEN 100.0 ELSE 0.0 END) / COUNT(*), 1) AS valor,
  COUNT(DISTINCT outbound_deliveries.entrega) AS Materiales_Solicitados
FROM (SELECT entrega, MAX(outbound_deliveries.dias_retraso) as dias_retraso, fecha_carga FROM outbound_deliveries WHERE outbound_deliveries.dias_retraso IS NOT NULL GROUP BY entrega) AS outbound_deliveries
WHERE outbound_deliveries.fecha_carga LIKE ?
GROUP BY fecha
ORDER BY fecha ASC;""",
                visual_state='{"baseTable": "outbound_deliveries", "joins": [], "filters": [{"column": "outbound_deliveries.fecha_carga", "operator": "contains", "value": "2026"}], "metric": {"column": "outbound_deliveries.dias_retraso", "aggregation": "SLA_EFFICIENCY", "format": "percent"}, "timeAxis": {"column": "outbound_deliveries.fecha_carga", "granularity": "MONTH"}, "breakdown": "", "secondMetric": {"column": "outbound_deliveries.entrega", "aggregation": "COUNT_DISTINCT", "label": "Materiales Solicitados"}, "chartType": "line"}'
            ),
            ConfigQuery(
                query_id="vl_sla_area_monthly_trend",
                sql_text="""SELECT 
                    substr(v.fecha_carga,7,4) || '-' || substr(v.fecha_carga,4,2) as month_sort,
                    MAX(substr(v.fecha_carga,4,2) || '-' || substr(v.fecha_carga,7,4)) as label,
                    {AREA_EXPR} as area,
                    (SUM(CASE WHEN v.dias_retraso <= ? THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as efficiency
                FROM outbound_deliveries v
                WHERE v.fecha_carga IS NOT NULL AND v.fecha_carga != ''
                GROUP BY month_sort, area ORDER BY month_sort ASC""",
                visual_state='{"baseTable": "outbound_deliveries", "joins": [], "filters": [{"column": "outbound_deliveries.fecha_carga", "operator": "contains", "value": "2026"}], "metric": {"column": "outbound_deliveries.dias_retraso", "aggregation": "SLA_EFFICIENCY", "format": "percent"}, "timeAxis": {"column": "outbound_deliveries.fecha_carga", "granularity": "MONTH"}, "breakdown": "outbound_deliveries.area_negocio", "chartType": "line"}'
            ),
            ConfigQuery(
                query_id="vl_sla_trend",
                sql_text="""SELECT 
                    v.week_sort, MAX(v.week_label) as label, COUNT(*) as material_count,
                    (SUM(CASE WHEN v.dias_retraso <= ? THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as efficiency
                FROM outbound_deliveries v
                WHERE v.week_sort IS NOT NULL AND v.week_sort != ''
                GROUP BY v.week_sort ORDER BY v.week_sort ASC""",
                visual_state='{"baseTable": "outbound_deliveries", "joins": [], "filters": [{"column": "outbound_deliveries.fecha_carga", "operator": "contains", "value": "2026"}], "metric": {"column": "outbound_deliveries.dias_retraso", "aggregation": "SLA_EFFICIENCY", "format": "percent"}, "timeAxis": {"column": "outbound_deliveries.fecha_carga", "granularity": "WEEK"}, "breakdown": "", "chartType": "line"}'
            ),
            ConfigQuery(
                query_id="vl_sla_area_trend",
                sql_text="""SELECT 
                    v.week_sort, MAX(v.week_label) as label, {AREA_EXPR} as area,
                    (SUM(CASE WHEN v.dias_retraso <= ? THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as efficiency
                FROM outbound_deliveries v
                WHERE v.week_sort IS NOT NULL AND v.week_sort != ''
                GROUP BY v.week_sort, area ORDER BY v.week_sort ASC""",
                visual_state='{"baseTable": "outbound_deliveries", "joins": [], "filters": [{"column": "outbound_deliveries.fecha_carga", "operator": "contains", "value": "2026"}], "metric": {"column": "outbound_deliveries.dias_retraso", "aggregation": "SLA_EFFICIENCY", "format": "percent"}, "timeAxis": {"column": "outbound_deliveries.fecha_carga", "granularity": "WEEK"}, "breakdown": "outbound_deliveries.area_negocio", "chartType": "line"}'
            ),
            ConfigQuery(
                query_id="vl_top_authors",
                sql_text="""SELECT autor as name, COUNT(DISTINCT entrega) as entregas, COUNT(*) as num_lineas,
                (SELECT {AREA_EXPR} FROM outbound_deliveries v WHERE v.autor=outbound_deliveries.autor AND v.fecha_carga LIKE ? GROUP BY 1 ORDER BY COUNT(*) DESC LIMIT 1) as area
                FROM outbound_deliveries 
                WHERE fecha_carga LIKE ?
                GROUP BY autor ORDER BY entregas DESC LIMIT 5"""
            ),
            ConfigQuery(
                query_id="inv_consumos_quick",
                sql_text="""SELECT material as cod_mat, texto_breve_material as material, COUNT(material) as qty 
                FROM inventory_movements WHERE cmv IN (?, ?) AND material IS NOT NULL AND material != '' 
                GROUP BY cod_mat, material ORDER BY qty DESC LIMIT 8"""
            ),
            # ── Gestión de OTs ──────────────────────────────────────────────────
            ConfigQuery(
                query_id="ia_predictive_movements",
                sql_text="""SELECT 
                    fe_contab, ce_coste, material, texto_breve_material, cantidad, cmv
                FROM inventory_movements 
                WHERE cmv IN ('201', '261') AND length(fe_contab) >= 10"""
            ),
            ConfigQuery(
                query_id="inv_historial_ubicaciones",
                sql_text="""SELECT 
                    l.ubicacion as ubic_dest,
                    MAX(l.fecha) as fecha,
                    MAX(l.texto_breve_material) as texto_breve_material,
                    SUM(l.stock_disp) as stock_disp,
                    MAX(l.umb) as umb,
                    MAX(l.ubic_actual) as ubic_actual
                FROM (
                    SELECT 
                        w.ubic_dest as ubicacion, 
                        COALESCE(w.fecha_conf, w.fe_creac) as fecha, 
                        w.texto_breve_material as texto_breve_material,
                        NULL as stock_disp,
                        NULL as umb,
                        NULL as ubic_actual
                    FROM warehouse_tasks w
                    WHERE UPPER(TRIM(w.material)) = ?
                      AND w.tp_dest NOT LIKE '9%'
                      AND w.ubic_dest IS NOT NULL
                      AND TRIM(w.ubic_dest) != ''

                    UNION ALL

                    SELECT 
                        s.ubicacin as ubicacion,
                        NULL as fecha,
                        s.texto_breve_de_material as texto_breve_material,
                        CAST(REPLACE(s.stock_disp, ',', '.') AS REAL) as stock_disp,
                        s.umb as umb,
                        s.ubicacin as ubic_actual
                    FROM stock_levels s
                    WHERE UPPER(TRIM(s.material)) = ?
                      AND s.ubicacin IS NOT NULL
                      AND TRIM(s.ubicacin) != ''
                ) l
                GROUP BY l.ubicacion
                ORDER BY fecha DESC"""
            ),
            ConfigQuery(
                query_id="ots_list_pending",
                sql_text="""SELECT 
                    numero_ot,
                    material,
                    texto_breve_material as material_name,
                    clase_mov,
                    ctd_teor_dsd as qty,
                    ubic_proc as source,
                    ubic_dest as dest,
                    fe_creac || ' ' || hora as created_at,
                    usuario as creator
                FROM warehouse_tasks
                WHERE (fecha_conf IS NULL OR fecha_conf = '')
                ORDER BY substr(fe_creac, 7, 4) ASC, substr(fe_creac, 4, 2) ASC, substr(fe_creac, 1, 2) ASC, hora ASC"""
            ),
            ConfigQuery(
                query_id="inv_non_palletized_summary",
                sql_text="""SELECT 
                    m.usuario as user,
                    m.cmv as clase_mov,
                    COUNT(p.material) as count,
                    MIN(substr(m.fe_contab, 7, 4) || '-' || substr(m.fe_contab, 4, 2) || '-' || substr(m.fe_contab, 1, 2) || ' ' || m.hora) as oldest,
                    MAX(substr(m.fe_contab, 7, 4) || '-' || substr(m.fe_contab, 4, 2) || '-' || substr(m.fe_contab, 1, 2) || ' ' || m.hora) as newest
                FROM lx02_pendientes p
                JOIN (
                    SELECT doc_mat, usuario, cmv, MAX(fe_contab) as fe_contab, MAX(hora) as hora 
                    FROM inventory_movements 
                    GROUP BY doc_mat, usuario, cmv
                ) m ON p.otcuanto = m.doc_mat
                WHERE CAST(REPLACE(p.stock_disp, ',', '.') AS REAL) != 0
                GROUP BY m.usuario, m.cmv
                ORDER BY clase_mov ASC, newest DESC"""
            ),
            ConfigQuery(
                query_id="ots_daily_trend",
                sql_text="""SELECT 
                    d.date as label,
                    substr(d.date, 7, 4) || '-' || substr(d.date, 4, 2) || '-' || substr(d.date, 1, 2) as sort_key,
                    (SELECT COUNT(*) FROM warehouse_tasks WHERE fe_creac = d.date) as created,
                    (SELECT COUNT(*) FROM warehouse_tasks WHERE fecha_conf = d.date) as confirmed
                FROM (
                    SELECT fe_creac as date FROM warehouse_tasks WHERE fe_creac IS NOT NULL AND fe_creac != ''
                    UNION
                    SELECT fecha_conf as date FROM warehouse_tasks WHERE fecha_conf IS NOT NULL AND fecha_conf != ''
                ) d
                WHERE substr(d.date, 7, 4) || '-' || substr(d.date, 4, 2) >= strftime('%Y-%m', 'now', 'start of month', '-1 month')
                ORDER BY sort_key ASC"""
            ),
            ConfigQuery(
                query_id="ots_by_movement_type",
                sql_text="""SELECT 
                    clase_mov as type,
                    COUNT(*) as count
                FROM warehouse_tasks
                WHERE cl_mov IS NOT NULL
                AND substr(fe_creac, 7, 4) || '-' || substr(fe_creac, 4, 2) >= strftime('%Y-%m', 'now', 'start of month', '-1 month')
                GROUP BY type
                ORDER BY count DESC"""
            ),
            ConfigQuery(
                query_id="ots_by_user_dual",
                sql_text="""SELECT 
                    u.user,
                    (SELECT COUNT(*) FROM warehouse_tasks WHERE usuario = u.user AND substr(fe_creac, 7, 4) || '-' || substr(fe_creac, 4, 2) >= strftime('%Y-%m', 'now', 'start of month', '-1 month')) as created,
                    (SELECT COUNT(*) FROM warehouse_tasks WHERE usuario_conf = u.user AND substr(fecha_conf, 7, 4) || '-' || substr(fecha_conf, 4, 2) >= strftime('%Y-%m', 'now', 'start of month', '-1 month')) as confirmed
                FROM (
                    SELECT usuario as user FROM warehouse_tasks WHERE usuario IS NOT NULL AND usuario != ''
                    UNION
                    SELECT usuario_conf as user FROM warehouse_tasks WHERE usuario_conf IS NOT NULL AND usuario_conf != ''
                ) u
                GROUP BY u.user
                HAVING created > 0 OR confirmed > 0
                ORDER BY (created + confirmed) DESC
                LIMIT 10"""
            ),
            # ── KPIs del Sistema ──────────────────────────────────────────────
            ConfigQuery(
                query_id="vl_kpi_total",
                sql_text="SELECT COUNT(DISTINCT entrega) as total_qty FROM outbound_deliveries WHERE substr(fecha_carga, 7, 4) = (SELECT MAX(substr(fecha_carga, 7, 4)) FROM outbound_deliveries)"
            ),
            ConfigQuery(
                query_id="vl_kpi_eff",
                sql_text="SELECT ROUND(SUM(CASE WHEN outbound_deliveries.dias_retraso <= 2 THEN 100.0 ELSE 0.0 END) / COUNT(*), 1) as valor FROM (SELECT entrega, MAX(outbound_deliveries.dias_retraso) as dias_retraso, fecha_carga FROM outbound_deliveries WHERE outbound_deliveries.dias_retraso IS NOT NULL GROUP BY entrega) AS outbound_deliveries WHERE (outbound_deliveries.fecha_carga LIKE ?)",
                visual_state='{"baseTable": "outbound_deliveries", "joins": [], "filters": [{"column": "outbound_deliveries.fecha_carga", "operator": "contains", "value": "2026"}], "metric": {"column": "outbound_deliveries.dias_retraso", "aggregation": "SLA_EFFICIENCY", "format": "percent"}, "timeAxis": {"column": "", "granularity": "MONTH"}, "breakdown": "", "chartType": "kpi"}'
            ),
            ConfigQuery(
                query_id="vl_kpi_ontime",
                sql_text="SELECT COUNT(DISTINCT outbound_deliveries.entrega) as valor FROM outbound_deliveries WHERE (outbound_deliveries.dias_retraso IS NOT NULL AND outbound_deliveries.dias_retraso < 3) AND (outbound_deliveries.fecha_carga LIKE ?)",
                visual_state='{"baseTable": "outbound_deliveries", "joins": [], "filters": [{"column": "outbound_deliveries.fecha_carga", "operator": "contains", "value": "2026"}, {"column": "outbound_deliveries.dias_retraso", "operator": "lessthan", "value": "3"}], "metric": {"column": "outbound_deliveries.entrega", "aggregation": "COUNT_DISTINCT"}, "timeAxis": {"column": "", "granularity": "MONTH"}, "breakdown": "", "chartType": "kpi"}'
            ),
            ConfigQuery(
                query_id="vl_kpi_late",
                sql_text="SELECT COUNT(DISTINCT outbound_deliveries.entrega) as valor FROM outbound_deliveries WHERE (outbound_deliveries.dias_retraso IS NOT NULL AND outbound_deliveries.dias_retraso > 2) AND (outbound_deliveries.fecha_carga LIKE ?)",
                visual_state='{"baseTable": "outbound_deliveries", "joins": [], "filters": [{"column": "outbound_deliveries.fecha_carga", "operator": "contains", "value": "2026"}, {"column": "outbound_deliveries.dias_retraso", "operator": "greaterthan", "value": "2"}], "metric": {"column": "outbound_deliveries.entrega", "aggregation": "COUNT_DISTINCT"}, "timeAxis": {"column": "", "granularity": "MONTH"}, "breakdown": "", "chartType": "kpi"}'
            ),
            ConfigQuery(
                query_id="inv_kpi_ingresos",
                sql_text="SELECT SUM(total_qty) as total_qty FROM (SELECT tipo_operacion, COUNT(material) as total_qty FROM inventory_movements GROUP BY tipo_operacion) WHERE tipo_operacion LIKE '%Ingreso%'"
            ),
            ConfigQuery(
                query_id="inv_kpi_consumos_prod",
                sql_text="SELECT SUM(total_qty) as total_qty FROM (SELECT tipo_operacion, COUNT(material) as total_qty FROM inventory_movements GROUP BY tipo_operacion) WHERE tipo_operacion LIKE '%Centro Costo%'"
            ),
            ConfigQuery(
                query_id="inv_kpi_consumos_mant",
                sql_text="SELECT SUM(total_qty) as total_qty FROM (SELECT tipo_operacion, COUNT(material) as total_qty FROM inventory_movements GROUP BY tipo_operacion) WHERE tipo_operacion LIKE '%Orden/Reserva%'"
            ),
            ConfigQuery(
                query_id="inv_kpi_rate_reabast",
                sql_text="SELECT ROUND(SUM(CASE WHEN inventory_movements.tipo_operacion LIKE '%Ingreso%' THEN 1.0 ELSE 0.0 END) * 100.0 / COALESCE(NULLIF(SUM(CASE WHEN inventory_movements.tipo_operacion LIKE '%Centro Costo%' OR inventory_movements.tipo_operacion LIKE '%Orden/Reserva%' THEN 1.0 ELSE 0.0 END), 0), 1), 1) as valor FROM inventory_movements WHERE (inventory_movements.fe_contab LIKE ?)",
                visual_state='{"baseTable": "inventory_movements", "joins": [], "filters": [{"column": "inventory_movements.fe_contab", "operator": "contains", "value": "2026"}], "metric": {"column": "inventory_movements.tipo_operacion", "aggregation": "REPLENISHMENT_RATE", "format": "percent"}, "timeAxis": {"column": "", "granularity": "YEAR"}, "breakdown": "", "chartType": "kpi"}'
            ),
            ConfigQuery(
                query_id="inv_kpi_traspasos",
                sql_text="SELECT COUNT(*) as total_qty FROM inventory_movements WHERE TRIM(cmv) IN ('301', '303') AND (inventory_movements.fe_contab LIKE ?)",
                visual_state='{"baseTable": "inventory_movements", "joins": [], "filters": [{"column": "inventory_movements.cmv", "operator": "in", "value": "301, 303"}, {"column": "inventory_movements.fe_contab", "operator": "contains", "value": "2026"}], "metric": {"column": "inventory_movements.material", "aggregation": "COUNT"}, "timeAxis": {"column": "", "granularity": "YEAR"}, "breakdown": "", "chartType": "kpi"}'
            ),
            ConfigQuery(
                query_id="inv_kpi_rate_devolucion",
                sql_text="SELECT ROUND(SUM(CASE WHEN TRIM(cmv) IN ('202', '262') THEN 1.0 ELSE 0.0 END) * 100.0 / COALESCE(NULLIF(SUM(CASE WHEN inventory_movements.tipo_operacion LIKE '%Centro Costo%' OR inventory_movements.tipo_operacion LIKE '%Orden/Reserva%' THEN 1.0 ELSE 0.0 END), 0), 1), 1) as valor FROM inventory_movements WHERE (inventory_movements.fe_contab LIKE ?)",
                visual_state='{"baseTable": "inventory_movements", "joins": [], "filters": [{"column": "inventory_movements.fe_contab", "operator": "contains", "value": "2026"}], "metric": {"column": "inventory_movements.tipo_operacion", "aggregation": "RETURN_RATE", "format": "percent"}, "timeAxis": {"column": "", "granularity": "YEAR"}, "breakdown": "", "chartType": "kpi"}'
            ),
            ConfigQuery(
                query_id="inv_kpi_rate_eficiencia",
                sql_text="SELECT ROUND(SUM(CASE WHEN (julianday(substr(registrado, 7, 4) || '-' || substr(registrado, 4, 2) || '-' || substr(registrado, 1, 2)) - julianday(substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) || '-' || substr(fe_contab, 1, 2))) <= 3.0 THEN 100.0 ELSE 0.0 END) / COUNT(*), 1) as valor FROM inventory_movements WHERE fe_contab IS NOT NULL AND registrado IS NOT NULL AND length(fe_contab) >= 10 AND length(registrado) >= 10 AND (inventory_movements.fe_contab LIKE ?)",
                visual_state='{"baseTable": "inventory_movements", "joins": [], "filters": [{"column": "inventory_movements.fe_contab", "operator": "contains", "value": "2026"}], "metric": {"column": "inventory_movements.tipo_operacion", "aggregation": "INV_EFFICIENCY", "format": "percent"}, "timeAxis": {"column": "", "granularity": "YEAR"}, "breakdown": "", "chartType": "kpi"}'
            ),
            ConfigQuery(
                query_id="ots_kpi_pending",
                sql_text="SELECT COUNT(*) as total_qty FROM warehouse_tasks WHERE fecha_conf IS NULL OR fecha_conf = ''"
            ),
            ConfigQuery(
                query_id="ots_kpi_users",
                sql_text="SELECT COUNT(DISTINCT warehouse_tasks.usuario) as valor FROM warehouse_tasks WHERE (warehouse_tasks.usuario IS NOT NULL AND warehouse_tasks.usuario != '') AND (warehouse_tasks.fe_creac LIKE ?)",
                visual_state='{"baseTable": "warehouse_tasks", "joins": [], "filters": [{"column": "warehouse_tasks.usuario", "operator": "isnotnull", "value": ""}, {"column": "warehouse_tasks.fe_creac", "operator": "contains", "value": "2026"}], "metric": {"column": "warehouse_tasks.usuario", "aggregation": "COUNT_DISTINCT"}, "timeAxis": {"column": "", "granularity": "MONTH"}, "breakdown": "", "chartType": "kpi"}'
            ),
        ]
        for obj in initial_queries:
            if not session.query(ConfigQuery).filter_by(query_id=obj.query_id).first():
                session.add(obj)


# ─── CARGA EN CACHÉ ────────────────────────────────────────────────────────────
def load_config_to_memory(session=None):
    """Deprecated. No-op for backwards compatibility."""
    pass

def _ensure_loaded():
    pass

# ─── API PÚBLICA (sin cambios para el resto del sistema) ──────────────────────
def get_setting(key: str, default: Any = None) -> Any:
    try:
        with get_session() as session:
            setting = session.query(AppSetting).filter_by(key=key).first()
            return setting.typed_value() if setting else default
    except Exception:
        return default


def get_status_mapping() -> Dict[str, str]:
    try:
        with get_session() as session:
            return {row.code: row.label for row in session.query(StatusMapping).all()}
    except Exception:
        return {}


def get_cost_center_mapping() -> Dict[str, str]:
    try:
        with get_session() as session:
            return {row.center_code: row.business_area for row in session.query(CostCenterMapping).all()}
    except Exception:
        return {}


def get_holidays() -> List[str]:
    try:
        with get_session() as session:
            return [row.date_str for row in session.query(Holiday).all()]
    except Exception:
        return []


def get_query(query_id: str) -> str:
    """
    Recupera el SQL asociado a una query_id.

    Estrategia de transición (Fase 1):
      - Si la fila tiene `visual_state`, el SQL debe compilarse en tiempo de
        ejecución via api_build_sql. Este método devuelve `sql_text` solo como
        fallback para queries que aún no han sido migradas a visual_state.
      - En la Fase 2, este método será eliminado y todos los consumidores
        deberán usar get_query_visual_state() + api_build_sql.

    DEPRECADO: Usar get_query_visual_state() para nuevos consumidores.
    """
    try:
        with get_session() as session:
            row = session.query(ConfigQuery).filter_by(query_id=query_id).first()
            if not row:
                return ""
            # Preferir sql_text solo si no existe visual_state (compatibilidad)
            return row.sql_text or ""
    except Exception:
        return ""


def get_query_visual_state(query_id: str) -> str:
    """
    Recupera el visual_state JSON de una query. Es la API preferida para
    nuevos consumidores en el Analytics Studio.

    Retorna el string JSON del VisualQueryBuilderPayload, o "" si no existe.
    """
    try:
        with get_session() as session:
            row = session.query(ConfigQuery).filter_by(query_id=query_id).first()
            return row.visual_state or "" if row else ""
    except Exception:
        return ""
