from sqlalchemy.orm import Session
from sqlalchemy import text
import pandas as pd
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from core.utils import sanitize_for_json
from core.state import get_app_state
from repositories import InventoryRepository
from core.wms_config import COST_CENTER_MAPPING

logger = logging.getLogger("services-inventory")

class InventoryService:
    def __init__(self, session: Session):
        self.session = session

    def fmt_num(self, val):
        try:
            return f"{int(float(val)):,}".replace(",", ".")
        except (ValueError, TypeError):
            return "0"


    def _get_latest_data_period(self) -> Tuple[str, str]:
        now = datetime.now()
        fallback = (str(now.year), f"{now.month:02d}")
        try:
            res = self.session.execute(text(
                "SELECT substr(fe_contab,7,4), substr(fe_contab,4,2) FROM inventory_movements "
                "WHERE fe_contab IS NOT NULL AND length(fe_contab)>=10 "
                "AND substr(fe_contab,7,4) GLOB '[0-9][0-9][0-9][0-9]' "
                "AND substr(fe_contab,4,2) GLOB '[0-9][0-9]' "
                "ORDER BY substr(fe_contab,7,4) DESC, substr(fe_contab,4,2) DESC LIMIT 1"
            )).fetchone()
            if res and str(res[0]).isdigit() and str(res[1]).isdigit():
                return (str(res[0]), str(res[1]))
            return fallback
        except:
            return fallback


    def _prepare_volume_kpis(self, anio, mes) -> Dict[str, Any]:
        vol_stats = InventoryRepository(self.session).get_volumen_stats()
        vol_data = sanitize_for_json(vol_stats)
        
        def sum_by_type(data, keyword):
            return sum(
                r.get('total_qty', r.get('qty', 0))
                for r in data
                if keyword in str(r.get('tipo_operacion', ''))
            )


        raw_ing = sum_by_type(vol_data, 'Ingreso')
        raw_prod = sum_by_type(vol_data, 'Centro Costo')
        raw_mant = sum_by_type(vol_data, 'Orden/Reserva')
        
        cm_filter = "substr(fe_contab,4,2)=? AND substr(fe_contab,7,4)=?"
        vol_cm = pd.read_sql(f"SELECT tipo_operacion, COUNT(material) as qty FROM inventory_movements WHERE {cm_filter} GROUP BY tipo_operacion", self.session.connection().connection, params=(mes, anio))
        cm_data = sanitize_for_json(vol_cm)
        
        cm_ing  = sum_by_type(cm_data, 'Ingreso')
        cm_prod = sum_by_type(cm_data, 'Centro Costo')
        cm_mant = sum_by_type(cm_data, 'Orden/Reserva')

        
        # 2. Cálculos Adicionales (Traspasos y Devoluciones)
        q_trasp = "SELECT COUNT(*) FROM inventory_movements WHERE TRIM(cmv) IN ('301', '303')"
        raw_trasp = self.session.execute(text(q_trasp)).fetchone()[0] or 0
        cm_trasp = self.session.execute(text(f"{q_trasp} AND substr(fe_contab,4,2)=:mes AND substr(fe_contab,7,4)=:anio"), {"mes": str(mes).zfill(2), "anio": str(anio)}).fetchone()[0] or 0

        q_dev = "SELECT COUNT(*) FROM inventory_movements WHERE TRIM(cmv) IN ('202', '262')"
        raw_dev = self.session.execute(text(q_dev)).fetchone()[0] or 0
        cm_dev = self.session.execute(text(f"{q_dev} AND substr(fe_contab,4,2)=:mes AND substr(fe_contab,7,4)=:anio"), {"mes": str(mes).zfill(2), "anio": str(anio)}).fetchone()[0] or 0

        total_cons = raw_prod + raw_mant
        rate_dev = round((raw_dev / total_cons * 100), 1) if total_cons > 0 else 0
        total_cons_cm = cm_prod + cm_mant
        cm_rate_dev = round((cm_dev / total_cons_cm * 100), 1) if total_cons_cm > 0 else 0

        import numpy as np
        
        # 3. Eficiencia de bodega
        q_eff = "SELECT fe_contab, registrado FROM inventory_movements WHERE fe_contab IS NOT NULL AND registrado IS NOT NULL AND length(fe_contab) >= 10 AND length(registrado) >= 10"
        df_eff = pd.read_sql(q_eff, self.session.connection().connection)
        
        rate_eficiencia = 0
        if not df_eff.empty:
            CHILEAN_HOLIDAYS = [
                '2024-01-01', '2024-03-29', '2024-03-30', '2024-05-01', '2024-05-21', 
                '2024-06-09', '2024-06-20', '2024-07-16', '2024-08-15', '2024-09-18', 
                '2024-09-19', '2024-09-20', '2024-10-12', '2024-10-27', '2024-10-31', 
                '2024-11-01', '2024-12-08', '2024-12-25',
                '2025-01-01', '2025-04-18', '2025-04-19', '2025-05-01', '2025-05-21', 
                '2025-06-20', '2025-07-16', '2025-08-15', '2025-09-18', '2025-09-19', 
                '2025-10-12', '2025-10-31', '2025-11-01', '2025-12-08', '2025-12-25',
                '2026-01-01', '2026-04-03', '2026-04-04', '2026-05-01', '2026-05-21',
                '2026-06-21', '2026-07-16', '2026-08-15', '2026-09-18', '2026-09-19',
                '2026-10-12', '2026-10-31', '2026-11-01', '2026-12-08', '2026-12-25'
            ]
            def parse_date(ds): return pd.to_datetime(ds, format='mixed', dayfirst=True, errors='coerce')
            df_eff['f_dt'] = parse_date(df_eff['fe_contab']).dt.date
            df_eff['r_dt'] = parse_date(df_eff['registrado']).dt.date
            df_eff = df_eff.dropna()
            if not df_eff.empty:
                diffs = np.busday_count(list(df_eff['f_dt']), list(df_eff['r_dt']), holidays=CHILEAN_HOLIDAYS)
                eff_count = (diffs <= 2).sum()
                rate_eficiencia = round((eff_count / len(df_eff)) * 100, 1)

        result_kpis = {
            "kpi_ingresos": self.fmt_num(raw_ing),
            "kpi_consumos_prod": self.fmt_num(raw_prod),
            "kpi_consumos_mant": self.fmt_num(raw_mant),
            "kpi_ingresos_cm": self.fmt_num(cm_ing),
            "cm_cons_prod": int(cm_prod),
            "cm_cons_mant": int(cm_mant),
            "kpi_cons_prod_cm": self.fmt_num(cm_prod),
            "kpi_cons_mant_cm": self.fmt_num(cm_mant),
            "cm_cons_total": int(cm_prod + cm_mant),
            "rate_reabast": round((raw_ing / total_cons * 100), 1) if total_cons > 0 else 0,
            "cm_rate_reabast": round((cm_ing / total_cons_cm * 100), 1) if total_cons_cm > 0 else 0,
            "kpi_traspasos": self.fmt_num(raw_trasp), "kpi_traspasos_cm": self.fmt_num(cm_trasp), 
            "rate_devolucion": rate_dev, "kpi_devoluciones": self.fmt_num(raw_dev),
            "cm_rate_devolucion": cm_rate_dev, "kpi_devoluciones_cm": self.fmt_num(cm_dev),
            "rate_eficiencia": rate_eficiencia
        }

        # Sobrescribir con KPIs dinámicos de config_queries (Analytics Studio) si existen
        try:
            from core.query_engine import get_bound_params_from_visual_state, extract_metric_value

            dynamic_kpi_mapping = {
                "inv_kpi_ingresos": ("kpi_ingresos", True, False),
                "inv_kpi_consumos_prod": ("kpi_consumos_prod", True, False),
                "inv_kpi_consumos_mant": ("kpi_consumos_mant", True, False),
                "inv_kpi_rate_reabast": ("rate_reabast", False, True),
                "inv_kpi_traspasos": ("kpi_traspasos", True, False),
                "inv_kpi_rate_devolucion": ("rate_devolucion", False, True),
                "inv_kpi_rate_eficiencia": ("rate_eficiencia", False, True)
            }

            yr_mask = f"%{anio}"

            # Primero leemos los valores absolutos dinámicos por si cambian los denominadores/numeradores
            for query_id, (key, is_fmt, is_pct) in dynamic_kpi_mapping.items():
                res = self.session.execute(
                    text("SELECT sql_text, visual_state FROM config_queries WHERE query_id = :qid"),
                    {"qid": query_id}
                ).fetchone()
                if res:
                    sql, visual_state = res
                    # Desde Fase 1, sql_text puede ser NULL si la query fue migrada
                    # a visual_state. Solo ejecutamos si hay SQL disponible.
                    if not sql:
                        if visual_state:
                            logger.debug(
                                f"KPI dinámico '{query_id}' tiene visual_state pero sql_text es NULL. "
                                f"Pendiente de compilación en tiempo real (Fase 3)."
                            )
                        continue
                    params = ()
                    if sql.count("?") > 0:
                        params = tuple(get_bound_params_from_visual_state(visual_state))
                        if len(params) != sql.count("?"):
                            params = (yr_mask,) if sql.count("?") == 1 else ()
                    df_dyn = pd.read_sql(sql, self.session.connection().connection, params=params)
                    if not df_dyn.empty:
                        val = extract_metric_value(df_dyn, str(anio))
                        if val is not None and not pd.isna(val):
                            if is_pct:
                                result_kpis[key] = round(float(val), 1)
                            else:
                                raw_val = int(val)
                                result_kpis[key] = self.fmt_num(raw_val) if is_fmt else raw_val

                                # Actualizar variables internas para el recalculo de tasas por fallback
                                if key == "kpi_ingresos":
                                    raw_ing = raw_val
                                elif key == "kpi_consumos_prod":
                                    raw_prod = raw_val
                                elif key == "kpi_consumos_mant":
                                    raw_mant = raw_val
                                elif key == "kpi_traspasos":
                                    raw_trasp = raw_val
                                elif key == "kpi_devoluciones":
                                    raw_dev = raw_val

            # Recalcular tasas por fallback si no fueron modificadas por un query dinámico
            total_cons_updated = raw_prod + raw_mant
            active_queries = [
                row[0] for row in self.session.execute(
                    text("SELECT query_id FROM config_queries WHERE sql_text IS NOT NULL AND sql_text != ''")
                ).fetchall()
            ]

            if "inv_kpi_rate_reabast" not in active_queries:
                result_kpis["rate_reabast"] = round((raw_ing / total_cons_updated * 100), 1) if total_cons_updated > 0 else 0

            if "inv_kpi_rate_devolucion" not in active_queries:
                result_kpis["rate_devolucion"] = round((raw_dev / total_cons_updated * 100), 1) if total_cons_updated > 0 else 0

        except Exception as ex:
            logger.error(f"Error al aplicar KPIs dinámicos de Movimientos: {ex}")

        return result_kpis



    def _prepare_abc_analytics(self, anio, mes) -> Dict[str, Any]:
        mat_consumos = InventoryRepository(self.session).get_material_consumos_abc()
        if mat_consumos.empty:
            return {"abc_counts": {"A": 0, "B": 0, "C": 0}, "inv_top_materials": []}
        
        total = mat_consumos['qty'].sum()
        mat_consumos['cum_perc'] = mat_consumos['qty'].cumsum() / total
        mat_consumos['abc'] = mat_consumos['cum_perc'].apply(lambda p: 'A' if p <= 0.8 else ('B' if p <= 0.95 else 'C'))
        
        # Ranking mensual
        mat_cm = pd.read_sql(
            "SELECT material as cod_mat, COUNT(material) as qty_cm FROM inventory_movements WHERE cmv IN('261','201') AND substr(fe_contab,4,2)=? AND substr(fe_contab,7,4)=? GROUP BY cod_mat", 
            self.session.connection().connection, params=(mes, anio)
        ).set_index('cod_mat')['qty_cm'].to_dict()
        
        top_mats = sanitize_for_json(mat_consumos.head(100))
        for m in top_mats:
            m['qty_cm'] = int(mat_cm.get(m['cod_mat'], 0))
            m['qty_fmt'] = self.fmt_num(m['qty'])
            
        return {
            "abc_counts": mat_consumos.groupby('abc')['qty'].sum().to_dict(),
            "inv_top_materials": top_mats,
            "top_materials_quick": top_mats[:10]
        }


    def _prepare_area_analytics(self, anio, mes) -> Dict[str, Any]:
        """Estadísticas de consumo por área con promedios diarios robustos."""
        logger.debug(f"Calculando promedios Movimientos para periodo: {mes}/{anio}")
        
        # Asegurar parámetros limpios
        p_mes = str(mes).zfill(2)
        p_anio = str(anio)

        # 1. Obtener días activos (Divisores)
        d_yr = self.session.execute(text("SELECT COUNT(DISTINCT fe_contab) FROM inventory_movements WHERE TRIM(cmv)='201'")).fetchone()[0] or 1
        d_cm = self.session.execute(text("SELECT COUNT(DISTINCT fe_contab) FROM inventory_movements WHERE TRIM(cmv)='201' AND substr(fe_contab,4,2)=:mes AND substr(fe_contab,7,4)=:anio"), {"mes": p_mes, "anio": p_anio}).fetchone()[0] or 1

        # 2. Consulta consolidada (Conteo de Transacciones/Retiros)
        query = """
            SELECT 
                UPPER(TRIM(COALESCE(m.business_area, i.ce_coste, 'MIXTO'))) as area_raw,
                COUNT(*) as count_val,
                COUNT(CASE WHEN substr(i.fe_contab,4,2) = ? AND substr(i.fe_contab,7,4) = ? THEN 1 END) as count_cm
            FROM inventory_movements i
            LEFT JOIN config_cost_center_mapping m ON i.ce_coste LIKE m.center_code || '%'
            WHERE TRIM(i.cmv) = '201'
            GROUP BY area_raw
        """
        df = pd.read_sql(query, self.session.connection().connection, params=(p_mes, p_anio))
        
        if df.empty:
            return {"inv_area_stats_json": [], "inv_area_stats": []}

        # Normalización con COST_CENTER_MAPPING
        def normalize_area(val):
            v = str(val).upper()
            for code, name in COST_CENTER_MAPPING.items():
                if code.upper() in v: return name
            return v

        df['area'] = df['area_raw'].apply(normalize_area)
        
        # Re-agrupar por el nombre normalizado (ya que varios códigos pueden mapear a la misma área)
        area_stats = df.groupby('area').agg({
            'count_val': 'sum',
            'count_cm': 'sum'
        }).reset_index()
        
        # Calcular promedios (dividiendo por 12 meses como aproximación anual si es necesario)
        area_stats['total_qty'] = (area_stats['count_val'] / 12.0).round(1)
        area_stats = area_stats.sort_values(by='total_qty', ascending=False)
            
        return {
            "inv_area_stats_json": sanitize_for_json(area_stats),
            "inv_area_stats": sanitize_for_json(area_stats)
        }


    def _prepare_trend_analytics(self, anio, mes) -> Dict[str, Any]:
        try:
            anio_int = int(anio)
        except (ValueError, TypeError):
            logger.warning(f"_prepare_trend_analytics: valor de año inválido '{anio}', usando año actual.")
            anio_int = datetime.now().year
        trend_df = InventoryRepository(self.session).get_trend_stats(str(anio_int - 1))
        total_dias = InventoryRepository(self.session).get_total_active_days()
        # Distribución Semanal (Año - Promediada)
        dow_df = InventoryRepository(self.session).get_dow_stats()
        dow_dist = [0] * 5
        num_semanas = max(int(total_dias) / 5, 1) # Aproximación de semanas laborales
        
        if not dow_df.empty:
            # Redistribuir Sabado(5) y Domingo(6) al Lunes(0)
            dow_df['dow_adj'] = dow_df['dow'].apply(lambda d: 0 if int(d) >= 5 else int(d))
            dow_adj_stats = dow_df.groupby('dow_adj')['qty'].sum().to_dict()
            for d in range(5):
                # Calcular promedio diario para ese DOW
                total_dia = dow_adj_stats.get(d, 0)
                dow_dist[d] = round(total_dia / num_semanas, 1)

        # Distribución Semanal (Mes Actual - Promediada por días activos del mes)
        d_cm = self.session.execute(text("SELECT COUNT(DISTINCT fe_contab) FROM inventory_movements WHERE TRIM(cmv)='201' AND substr(fe_contab,4,2)=:mes AND substr(fe_contab,7,4)=:anio"), {"mes": str(mes).zfill(2), "anio": str(anio)}).fetchone()[0] or 1
        num_semanas_cm = max(d_cm / 5.0, 1)

        cm_filter = "substr(fe_contab,4,2)=? AND substr(fe_contab,7,4)=?"
        dow_cm_df = pd.read_sql(
            f"SELECT CAST(strftime('%w', substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) || '-' || substr(fe_contab, 1, 2)) AS INTEGER) as dow, COUNT(*) as qty FROM inventory_movements WHERE {cm_filter} AND TRIM(cmv)='201' GROUP BY dow",
            self.session.connection().connection, params=(str(mes).zfill(2), str(anio))
        )
        
        dow_dist_cm = [0] * 5
        if not dow_cm_df.empty:
            dow_cm_df['dow_adj'] = dow_cm_df['dow'].apply(lambda d: 0 if int(d) >= 5 else int(d))
            dow_adj_cm = dow_cm_df.groupby('dow_adj')['qty'].sum().to_dict()
            for d in range(5):
                total_dia_cm = dow_adj_cm.get(d, 0)
                dow_dist_cm[d] = round(total_dia_cm / num_semanas_cm, 1)

        # Weekly Trend Data (Últimas 24 semanas)
        weekly_query = """
            SELECT strftime('%Y-%W', substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) || '-' || substr(fe_contab, 1, 2)) as week_sort,
            SUM(CASE WHEN cmv = '101' THEN 1 ELSE 0 END) as entradas,
            SUM(CASE WHEN cmv = '201' THEN 1 ELSE 0 END) as salidas_prod,
            SUM(CASE WHEN cmv = '261' THEN 1 ELSE 0 END) as salidas_mant
            FROM inventory_movements 
            WHERE length(fe_contab) >= 10 AND substr(fe_contab, 7, 4) >= ?
            GROUP BY week_sort ORDER BY week_sort ASC
        """
        trend_weekly_df = pd.read_sql(weekly_query, self.session.connection().connection, params=(str(int(anio)-1),))
        trend_weekly_df = trend_weekly_df.dropna(subset=['week_sort']).sort_values('week_sort').tail(24)

        return {
            "trend_labels": trend_df['periodo'].tolist() if not trend_df.empty else [],
            "trend_entradas": trend_df['entradas'].tolist() if not trend_df.empty else [],
            "trend_salidas_prod": trend_df['salidas_prod'].tolist() if not trend_df.empty else [],
            "trend_salidas_mant": trend_df['salidas_mant'].tolist() if not trend_df.empty else [],
            "trend_labels_weekly": trend_weekly_df['week_sort'].tolist() if not trend_weekly_df.empty else [],
            "trend_entradas_weekly": trend_weekly_df['entradas'].tolist() if not trend_weekly_df.empty else [],
            "trend_salidas_prod_weekly": trend_weekly_df['salidas_prod'].tolist() if not trend_weekly_df.empty else [],
            "trend_salidas_mant_weekly": trend_weekly_df['salidas_mant'].tolist() if not trend_weekly_df.empty else [],
            "dow_distribution": dow_dist,
            "dow_distribution_cm": dow_dist_cm,
            "total_dias_activos": int(total_dias)
        }


    def _prepare_user_location_analytics(self, anio, mes) -> Dict[str, Any]:
        """Estadísticas detalladas de usuarios y ubicaciones con actividad mensual."""
        p_mes = str(mes).zfill(2)
        p_anio = str(anio)
        
        # 1. Top Ubicaciones con desglose mensual
        query_loc = """
            SELECT COALESCE(alm, 'S/U') as ubi, 
                   COUNT(*) as total_qty,
                   COUNT(CASE WHEN substr(fe_contab,4,2)=? AND substr(fe_contab,7,4)=? THEN 1 END) as qty_cm
            FROM inventory_movements
            WHERE TRIM(cmv) = '201' AND ubi IS NOT NULL AND ubi != 'S/U'
            GROUP BY ubi
            ORDER BY total_qty DESC
            LIMIT 10
        """
        loc_stats = pd.read_sql(query_loc, self.session.connection().connection, params=(p_mes, p_anio))
        loc_records = sanitize_for_json(loc_stats)
        for r in loc_records:
            r['total_qty_fmt'] = self.fmt_num(r['total_qty'])

        # 2. Top Usuarios con desglose mensual
        query_user = """
            SELECT usuario as user, 
                   SUM(CASE WHEN TRIM(cmv) IN ('201', '261', '221') 
                       AND NOT (
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%CIERRE%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%REGU%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%DEV%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%ERROR%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%ANUL%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%CONSUM%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%RECLA%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%DUPLI%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%DIFEREN%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%NO CORRESP%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%CIERRE%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%REGU%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%DEV%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%ERROR%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%ANUL%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%CONSUM%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%RECLA%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%DUPLI%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%DIFEREN%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%NO CORRESP%'
                       ) THEN 1 ELSE 0 END) as qty,
                   SUM(CASE WHEN TRIM(cmv) IN ('201', '261') 
                       AND substr(fe_contab,4,2)=? AND substr(fe_contab,7,4)=? 
                       AND NOT (
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%CIERRE%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%REGU%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%DEV%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%ERROR%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%ANUL%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%CONSUM%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%RECLA%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%DUPLI%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%DIFEREN%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%NO CORRESP%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%CIERRE%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%REGU%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%DEV%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%ERROR%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%ANUL%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%CONSUM%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%RECLA%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%DUPLI%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%DIFEREN%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%NO CORRESP%'
                       ) THEN 1 ELSE 0 END) as qty_cm,
                   SUM(CASE WHEN TRIM(cmv) IN ('202', '262', '102', '302', '304') 
                       AND NOT (
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%CIERRE%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%REGU%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%DEV%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%ERROR%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%ANUL%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%CONSUM%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%RECLA%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%DUPLI%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%DIFEREN%' OR
                           UPPER(COALESCE(texto_cab_documento, '')) LIKE '%NO CORRESP%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%CIERRE%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%REGU%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%DEV%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%ERROR%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%ANUL%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%CONSUM%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%RECLA%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%DUPLI%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%DIFEREN%' OR
                           UPPER(COALESCE(referencia, '')) LIKE '%NO CORRESP%'
                       ) THEN 1 ELSE 0 END) as anulaciones
            FROM inventory_movements
            WHERE TRIM(cmv) IN ('201', '261', '202', '262', '102', '302', '304') AND usuario IS NOT NULL
            GROUP BY usuario
            ORDER BY qty DESC
            LIMIT 15
        """
        user_stats = pd.read_sql(query_user, self.session.connection().connection, params=(p_mes, p_anio))
        user_records = sanitize_for_json(user_stats)
        for u in user_records:
            u['qty_fmt'] = self.fmt_num(u.get('qty', 0))
            q = u.get('qty', 0) or 1
            u['error_rate'] = round((u.get('anulaciones', 0) / q) * 100, 1)

        return {"top_users": user_records, "top_ubicaciones_quick": loc_records}


    def _prepare_planned_consumption_trend(self) -> Dict[str, Any]:
        """Calcula la tendencia de consumos Planificados vs Desplanificados (CMV 201)."""
        import re
        import pandas as pd
        
        query = """
            SELECT 
                substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) as periodo,
                fe_contab,
                cmv,
                COALESCE(texto_cab_documento, '') as txt_cab,
                COALESCE(referencia, '') as ref
            FROM inventory_movements
            WHERE cmv IN ('201', '261')
            AND UPPER(COALESCE(texto_cab_documento, '')) NOT LIKE '%CIERRE%'
            AND UPPER(COALESCE(referencia, '')) NOT LIKE '%CIERRE%'
            AND fe_contab IS NOT NULL AND length(fe_contab) >= 10
        """
        try:
            df = pd.read_sql(query, self.session.connection().connection)
            logger.debug(f"Planned Trend: {len(df)} registros recuperados para CMV 201 y 261")
            
            if df.empty:
                return {"planned_labels": [], "planned_data": [], "unplanned_data": [], "kpi_201_planned": 0, "kpi_201_unplanned": 0, "kpi_261_planned": 0, "kpi_261_unplanned": 0}
                
            # Regex para detectar órdenes que empiecen por 81 o 081 con 9-10 dígitos
            prog = re.compile(r'(^|\D)(81\d{7,8}|081\d{6,7})($|\D)')
            
            def classify(row):
                txt = row['txt_cab'].strip()
                ref = row['ref'].strip()
                combined = f"{txt} {ref}"
                
                if row['cmv'] == '201':
                    return 1 if prog.search(combined) else 0
                else: # 261
                    # Desplanificado si tiene algún texto
                    return 0 if (txt != '' or ref != '') else 1

            df['is_planned'] = df.apply(classify, axis=1)
            
            # Agrupar por periodo
            trend = df.groupby('periodo').agg(
                total_rows=('is_planned', 'count'),
                planned_count=('is_planned', 'sum')
            ).reset_index()
            
            trend['unplanned_count'] = trend['total_rows'] - trend['planned_count']
            trend_monthly = trend.sort_values(by='periodo').tail(24) # Últimos 24 meses
            
            # Agrupar por semana
            df['week_sort'] = df['fe_contab'].apply(lambda x: pd.to_datetime(x, format='mixed', dayfirst=True).strftime('%Y-%W') if pd.notna(x) else None)
            trend_w = df.dropna(subset=['week_sort']).groupby('week_sort').agg(
                total_rows=('is_planned', 'count'),
                planned_count=('is_planned', 'sum')
            ).reset_index()
            trend_w['unplanned_count'] = trend_w['total_rows'] - trend_w['planned_count']
            trend_weekly = trend_w.sort_values(by='week_sort').tail(24)
            
            total_201_planned = int(len(df[(df['cmv'] == '201') & (df['is_planned'] == 1)]))
            total_201_unplanned = int(len(df[(df['cmv'] == '201') & (df['is_planned'] == 0)]))
            total_261_planned = int(len(df[(df['cmv'] == '261') & (df['is_planned'] == 1)]))
            total_261_unplanned = int(len(df[(df['cmv'] == '261') & (df['is_planned'] == 0)]))
            
            return {
                "planned_labels": trend_monthly['periodo'].tolist(),
                "planned_data": trend_monthly['planned_count'].tolist(),
                "unplanned_data": trend_monthly['unplanned_count'].tolist(),
                "planned_labels_weekly": trend_weekly['week_sort'].tolist() if not trend_weekly.empty else [],
                "planned_data_weekly": trend_weekly['planned_count'].tolist() if not trend_weekly.empty else [],
                "unplanned_data_weekly": trend_weekly['unplanned_count'].tolist() if not trend_weekly.empty else [],
                "kpi_201_planned": total_201_planned,
                "kpi_201_unplanned": total_201_unplanned,
                "kpi_261_planned": total_261_planned,
                "kpi_261_unplanned": total_261_unplanned
            }
        except Exception as e:
            logger.error(f"Error en _prepare_planned_consumption_trend: {e}")
            return {"planned_labels": [], "planned_data": [], "unplanned_data": [], "kpi_201_planned": 0, "kpi_201_unplanned": 0, "kpi_261_planned": 0, "kpi_261_unplanned": 0}

    def _get_empty_context(self) -> Dict[str, Any]:
        return {
            "kpi_ingresos": "0", "kpi_consumos_prod": "0", "kpi_consumos_mant": "0",
            "volumen_data": [], "inv_top_materials": [], "top_users": [],
            "abc_counts": {"A": 0, "B": 0, "C": 0}, "trend_labels": [], "cm_label": "N/A",
            "inv_ubicaciones_mapping": {}, "inv_area_material_mapping": {},
            "inv_user_material_mapping": {}, "dow_material_mapping": {},
            "pm_material_mapping": {}, "trend_salidas_prod": [], "trend_salidas_mant": [],
            "abc_mapping": {}, "dow_distribution": [0]*7, "dow_distribution_cm": [0]*7,
            "inv_area_stats_json": [], "scatter_data": [], "alerts": [], "combos": [],
            "cm_rate_devolucion": 0, "kpi_devoluciones_cm": "0"
        }


    def get_full_context(self) -> Dict[str, Any]:
        """Genera el contexto de datos para el dashboard de Movimientos con caché."""
        state = get_app_state()
        cached = state.get_cache("/analytics/inventory")
        if cached: return cached


        if not InventoryRepository(self.session).check_table_exists():
            return self._get_empty_context()

        try:
            cm_anio, cm_mes = self._get_latest_data_period()
            
            # 1. Preparar sub-contextos
            vol_ctx = self._prepare_volume_kpis(cm_anio, cm_mes)
            area_ctx = self._prepare_area_analytics(cm_anio, cm_mes)
            abc_ctx = self._prepare_abc_analytics(cm_anio, cm_mes)
            user_loc_ctx = self._prepare_user_location_analytics(cm_anio, cm_mes)
            trend_ctx = self._prepare_trend_analytics(cm_anio, cm_mes)
            from routes.analytics_proyecciones import get_proyecciones_context
            proy_ctx = get_proyecciones_context()

            # 2. Generar Mapeos Detallados para Modales
            ubic_map_df = InventoryRepository(self.session).get_location_material_summary()
            ubic_mapping = {}
            if not ubic_map_df.empty:
                for u in ubic_map_df['ubi'].unique():
                    mats = ubic_map_df[ubic_map_df['ubi'] == u].head(50).to_dict(orient="records")
                    for m in mats: m['qty_fmt'] = self.fmt_num(m['total_qty'])
                    ubic_mapping[u] = mats

            area_map_df = InventoryRepository(self.session).get_area_material_mapping_201()
            area_mapping = {}
            if not area_map_df.empty:
                for a in area_map_df['area'].unique():
                    mats = area_map_df[area_map_df['area'] == a].head(50).to_dict(orient="records")
                    for m in mats: m['qty_fmt'] = self.fmt_num(m['qty'])
                    area_mapping[a] = mats

            user_names = [u['user'] for u in user_loc_ctx.get('top_users', [])]
            user_map_df = InventoryRepository(self.session).get_user_material_mapping(tuple(user_names))
            user_mapping = {}
            if not user_map_df.empty:
                for u in user_map_df['user'].unique():
                    mats = user_map_df[user_map_df['user'] == u].head(50).to_dict(orient="records")
                    for m in mats: m['qty_fmt'] = self.fmt_num(m['total_qty'])
                    user_mapping[u] = mats

            # ABC Mapping
            abc_mapping = {}
            if abc_ctx.get('inv_top_materials', []):
                abc_mats = pd.DataFrame(abc_ctx.get('inv_top_materials', []))
                if not abc_mats.empty:
                    for cat in ['A', 'B', 'C']:
                        abc_mapping[cat] = abc_mats[abc_mats['abc'] == cat].head(50).to_dict(orient="records")

            # PM Mapping
            pm_map_df = InventoryRepository(self.session).get_pm_type_material_records()
            pm_mapping = {}
            if not pm_map_df.empty:
                for t in pm_map_df['type'].unique():
                    mats = pm_map_df[pm_map_df['type'] == t].head(50).to_dict(orient="records")
                    for m in mats: m['qty_fmt'] = self.fmt_num(m['qty'])
                    pm_mapping[t] = mats

            # 3. Planificados vs Desplanificados (Nuevo gráfico solicitado)
            planned_ctx = self._prepare_planned_consumption_trend()

            # 4. Consolidar Contexto Final
            context = {
                **vol_ctx,
                **area_ctx,
                **abc_ctx,
                **user_loc_ctx,
                **trend_ctx,
                **planned_ctx,
                "cm_label": f"{cm_mes}/{cm_anio}",
                "volumen_data": [],
                "inv_ubicaciones_mapping": ubic_mapping,
                "inv_area_material_mapping": area_mapping,
                "inv_user_material_mapping": user_mapping,
                "abc_mapping": abc_mapping,
                "pm_material_mapping": pm_mapping,
                "scatter_data": proy_ctx.get("scatter_data", []),
                "alerts": proy_ctx.get("alerts", []),
                "combos": proy_ctx.get("combos", [])
            }
            
            # Guardar en caché y snapshot de BD
            state.set_cache("/analytics/inventory", context)
            try:
                from routes.deliveries import save_analytics_snapshot
                save_analytics_snapshot(self.session, "inventory", context)
            except Exception: pass
            
            return context

        except Exception as e:
            logger.error(f"Error generando contexto Movimientos: {e}", exc_info=True)
            return self._get_empty_context()


