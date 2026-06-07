import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.cache_decorator import analytics_cache
from core.state import get_cache_manager
from core.utils import sanitize_for_json
from core.wms_config import COST_CENTER_MAPPING
from repositories import InventoryRepository

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
        except Exception:
            return fallback


    def _get_empty_context(self) -> Dict[str, Any]:
        return {
            "cm_label": "N/A", "cm_anio": "", "cm_mes": "",
            "volumen_data": [], "inv_top_materials": [], "top_users": [],
            "abc_counts": {"A": 0, "B": 0, "C": 0}, "trend_labels": [],
            "inv_ubicaciones_mapping": {}, "inv_area_material_mapping": {},
            "inv_user_material_mapping": {}, "dow_material_mapping": {},
            "pm_material_mapping": {}, "trend_salidas_prod": [], "trend_salidas_mant": [],
            "abc_mapping": {}, "dow_distribution": [0]*7, "dow_distribution_cm": [0]*7,
            "inv_area_stats_json": [], "scatter_data": [], "alerts": [], "combos": [],
            "top_ubicaciones_quick": [], "top_materials_quick": []
        }

    @analytics_cache(key_prefix="inventory")
    def get_full_context(self) -> Dict[str, Any]:
        """Genera el contexto base para el dashboard de Movimientos (Fase 3: SaaS)."""
        cache = get_cache_manager()
        cached = cache.get_cache("/analytics/inventory")
        if cached:
            return cached

        if not InventoryRepository(self.session).check_table_exists():
            return self._get_empty_context()

        try:
            cm_anio, cm_mes = self._get_latest_data_period()

            context = self._get_empty_context()
            context["cm_label"] = f"{cm_mes}/{cm_anio}"
            context["cm_anio"] = cm_anio
            context["cm_mes"] = cm_mes

            try:
                # Calcular las estadisticas de eficiencia
                query_stats = """
                SELECT
                    substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) as mes,
                    CASE
                        WHEN tipo_operacion LIKE '%Ingreso%' THEN 'Ingresos'
                        ELSE 'Consumos'
                    END as tipo,
                    COUNT(*) as volumen_mensual,
                    ROUND(SUM(CASE WHEN ABS(julianday(substr(registrado, 7, 4) || '-' || substr(registrado, 4, 2) || '-' || substr(registrado, 1, 2)) - julianday(substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) || '-' || substr(fe_contab, 1, 2))) <= 2 THEN 100.0 ELSE 0.0 END) / NULLIF(COUNT(*), 0), 1) as eficiencia
                FROM inventory_movements
                WHERE substr(fe_contab, 7, 4) IN ('2024', '2025', '2026')
                GROUP BY mes, tipo
                HAVING mes IS NOT NULL AND length(mes) = 7
                ORDER BY mes, tipo
                """
                df_stats = pd.read_sql_query(query_stats, self.session.connection().connection)

                ingresos_stats = {"ideal": 0, "estabilidad": 0, "sobrecarga": 0}
                consumos_stats = {"ideal": 0, "estabilidad": 0, "sobrecarga": 0}

                import numpy as np
                for tipo_name, stats_dict in [('Ingresos', ingresos_stats), ('Consumos', consumos_stats)]:
                    df_tipo = df_stats[df_stats['tipo'] == tipo_name]
                    if not df_tipo.empty:
                        vol = df_tipo['volumen_mensual']
                        stats_dict["ideal"] = int(np.percentile(vol, 40))
                        stats_dict["estabilidad"] = int(np.percentile(vol, 70))
                        stats_dict["sobrecarga"] = int(np.percentile(vol, 90))
                    else:
                        stats_dict["ideal"] = 0
                        stats_dict["estabilidad"] = 0
                        stats_dict["sobrecarga"] = 0

                context["ingresos_eff_stats"] = ingresos_stats
                context["consumos_eff_stats"] = consumos_stats

                # Calcular estadisticas SEMANALES
                query_weekly_stats = """
                SELECT
                    strftime('%Y-%W', substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) || '-' || substr(fe_contab, 1, 2)) as semana,
                    CASE
                        WHEN tipo_operacion LIKE '%Ingreso%' THEN 'Ingresos'
                        ELSE 'Consumos'
                    END as tipo,
                    COUNT(*) as volumen_semanal,
                    ROUND(SUM(CASE WHEN ABS(julianday(substr(registrado, 7, 4) || '-' || substr(registrado, 4, 2) || '-' || substr(registrado, 1, 2)) - julianday(substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) || '-' || substr(fe_contab, 1, 2))) <= 2 THEN 100.0 ELSE 0.0 END) / NULLIF(COUNT(*), 0), 1) as eficiencia
                FROM inventory_movements
                WHERE substr(fe_contab, 7, 4) IN ('2024', '2025', '2026')
                GROUP BY semana, tipo
                HAVING semana IS NOT NULL
                ORDER BY semana, tipo
                """
                df_weekly = pd.read_sql_query(query_weekly_stats, self.session.connection().connection)
                ingresos_weekly = {"ideal": 0, "estabilidad": 0, "sobrecarga": 0}
                consumos_weekly = {"ideal": 0, "estabilidad": 0, "sobrecarga": 0}

                for tipo_name, stats_dict in [('Ingresos', ingresos_weekly), ('Consumos', consumos_weekly)]:
                    df_tipo = df_weekly[df_weekly['tipo'] == tipo_name]
                    if not df_tipo.empty:
                        vol = df_tipo['volumen_semanal']
                        stats_dict["ideal"] = int(np.percentile(vol, 40))
                        stats_dict["estabilidad"] = int(np.percentile(vol, 70))
                        stats_dict["sobrecarga"] = int(np.percentile(vol, 90))
                    else:
                        stats_dict["ideal"] = 0
                        stats_dict["estabilidad"] = 0
                        stats_dict["sobrecarga"] = 0

                context["ingresos_eff_stats_weekly"] = ingresos_weekly
                context["consumos_eff_stats_weekly"] = consumos_weekly

            except Exception as e_stats:
                logger.error(f"Error calculando estadisticas de eficiencia: {e_stats}")
                context["ingresos_eff_stats"] = {"ideal": 0, "estabilidad": 0, "sobrecarga": 0}
                context["consumos_eff_stats"] = {"ideal": 0, "estabilidad": 0, "sobrecarga": 0}
                context["ingresos_eff_stats_weekly"] = {"ideal": 0, "estabilidad": 0, "sobrecarga": 0}
                context["consumos_eff_stats_weekly"] = {"ideal": 0, "estabilidad": 0, "sobrecarga": 0}

            # Guardar en caché
            cache.set_cache("/analytics/inventory", context)

            return context
        except Exception as e:
            logger.error(f"Error generando contexto Movimientos: {e}", exc_info=True)
            return self._get_empty_context()



