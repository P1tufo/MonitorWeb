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
from typing import Any, Dict, List, Optional

from sqlalchemy import inspect
from sqlalchemy.orm import Session

from .database import Base, engine, get_session
from .models import AppSetting, ConfigQuery, CostCenterMapping, Holiday, StatusMapping

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
        # ── Consultas SQL (Seed JSON) ──────────────────────────────────────────
        import json
        import os
        widgets_path = os.path.join(os.path.dirname(__file__), "seed_data", "widgets.json")
        if os.path.exists(widgets_path):
            with open(widgets_path, "r", encoding="utf-8") as f:
                seed_widgets = json.load(f)
            for w in seed_widgets:
                if not session.query(ConfigQuery).filter_by(query_id=w["query_id"]).first():
                    session.add(ConfigQuery(query_id=w["query_id"], visual_state=w["visual_state"]))


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


def get_query_visual_state(query_id: str) -> str:
    """
    Recupera el visual_state JSON de una query. Es la API preferida para
    obtener consultas que deben compilarse dinámicamente.
    """
    try:
        with get_session() as session:
            row = session.query(ConfigQuery).filter_by(query_id=query_id).first()
            return row.visual_state or "" if row else ""
    except Exception:
        return ""
