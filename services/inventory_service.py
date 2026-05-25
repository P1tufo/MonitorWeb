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

    def get_full_context(self) -> Dict[str, Any]:
        """Genera el contexto base para el dashboard de Movimientos (Fase 3: SaaS)."""
        state = get_app_state()
        cached = state.get_cache("/analytics/inventory")
        if cached: return cached

        if not InventoryRepository(self.session).check_table_exists():
            return self._get_empty_context()

        try:
            cm_anio, cm_mes = self._get_latest_data_period()
            
            context = self._get_empty_context()
            context["cm_label"] = f"{cm_mes}/{cm_anio}"
            context["cm_anio"] = cm_anio
            context["cm_mes"] = cm_mes
            
            # Guardar en caché
            state.set_cache("/analytics/inventory", context)
            
            return context

        except Exception as e:
            logger.error(f"Error generando contexto Movimientos: {e}", exc_info=True)
            return self._get_empty_context()



