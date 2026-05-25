import pandas as pd
from typing import Final, Tuple
from sqlalchemy import text
from core.wms_config import get_setting
from .base import BaseRepository

class InventoryRepository(BaseRepository):
    """Repositorio para el dominio de Inventario (ex-Movimientos)."""

    # ── Constantes de CMV (configurables vía config_settings) ────────────────
    def get_cmv_prod(self) -> str:
        return get_setting("CMV_PROD", "201")

    def get_cmv_mant(self) -> str:
        return get_setting("CMV_MANT", "261")

    def get_cmv_consumos(self) -> Tuple[str, ...]:
        return (self.get_cmv_prod(), self.get_cmv_mant())

    def get_cmv_reversas(self) -> Tuple[str, ...]:
        rev_str = get_setting("CMV_REVERSAS", "202,262,102,302,304")
        return tuple(r.strip() for r in rev_str.split(","))

    def check_table_exists(self) -> bool:
        try:
            res = self.session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='inventory_movements'")).fetchone()
            return res is not None
        except Exception:
            return False

    # ── SQL de fallback: constantes privadas nombradas ────────────────────────
    # Si config_queries no tiene una query personalizada para el query_id dado,
    # se usa este SQL hardcodeado como fallback explícito.
    # El flujo es siempre: config_queries BD → fallback de constante de clase.
    # No hay dict intermedio ni override opaco de _sql().

