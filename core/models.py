"""
core/models.py — Modelos ORM SQLAlchemy para el esquema de configuración SaaS.

Estos modelos representan las tablas de configuración dinámica (Pilar 2):
  - config_status_mapping      → Mapeo de estados WMS a etiquetas visuales.
  - config_cost_center_mapping → Mapeo de centros de costo a áreas de negocio.
  - app_settings               → Parámetros de procesamiento configurables.
  - config_holidays            → Feriados para cálculo de SLA.
  - config_queries             → Consultas SQL gestionadas via UI.

Separación de esquemas:
  - Datos transaccionales (vl06o, mb51, lx02, lt22) → gestionados via sqlite3 plano.
  - Datos de configuración SaaS → gestionados via SQLAlchemy (estos modelos).
"""
from __future__ import annotations

from sqlalchemy import String, Float, Integer, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


# ─── CONFIGURACIÓN: MAPEO DE ESTADOS ─────────────────────────────────────────
class StatusMapping(Base):
    """
    Mapea códigos internos del WMS (ej. 'CCC') a etiquetas legibles por humanos.
    Editable desde el panel SaaS en /settings.
    """
    __tablename__ = "config_status_mapping"

    code: Mapped[str] = mapped_column(String(20), primary_key=True)
    label: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f"<StatusMapping code={self.code!r} label={self.label!r}>"


# ─── CONFIGURACIÓN: CENTROS DE COSTO ─────────────────────────────────────────
class CostCenterMapping(Base):
    """
    Asocia un código de centro de costo del WMS con un Área de Negocio.
    Permite clasificar entregas/movimientos sin hardcodear los prefijos en el código.
    """
    __tablename__ = "config_cost_center_mapping"

    center_code: Mapped[str] = mapped_column(String(30), primary_key=True)
    business_area: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f"<CostCenterMapping {self.center_code!r} → {self.business_area!r}>"


# ─── CONFIGURACIÓN: PARÁMETROS GLOBALES ──────────────────────────────────────
class AppSetting(Base):
    """
    Parámetros de comportamiento del sistema.
    El campo `type` (float/int/bool/str) permite deserialización correcta.
    """
    __tablename__ = "app_settings"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False, default="str")

    def typed_value(self):
        """Retorna el valor con el tipo Python correcto."""
        converters = {
            "float": float,
            "int": int,
            "bool": lambda v: v.lower() in ("true", "1"),
            "str": str,
        }
        return converters.get(self.type, str)(self.value)

    def __repr__(self) -> str:
        return f"<AppSetting {self.key!r}={self.value!r} ({self.type})>"


# ─── CONFIGURACIÓN: FERIADOS ──────────────────────────────────────────────────
class Holiday(Base):
    """
    Días no hábiles para el cálculo de SLA (días de retraso).
    Se carga en memoria por `get_holidays()` en db_config_manager.
    Administrable via /settings sin reiniciar la app.
    """
    __tablename__ = "config_holidays"

    date_str: Mapped[str] = mapped_column(String(10), primary_key=True)  # ISO: YYYY-MM-DD

    def __repr__(self) -> str:
        return f"<Holiday {self.date_str!r}>"


# ─── CONFIGURACIÓN: CONSULTAS SQL ─────────────────────────────────────────────
class ConfigQuery(Base):
    """
    Almacena el estado visual (JSON) de las consultas del Analytics Studio.

    Arquitectura de transición:
      - `visual_state` (Text, JSON) → FUENTE DE VERDAD. Almacena el payload
        estructurado del Visual Query Builder (VisualQueryBuilderPayload).
        El SQL se compila en tiempo de ejecución por api_build_sql, no se persiste.
      - `sql_text` (Text, nullable) → DEPRECADO. Mantenido solo como fallback
        de compatibilidad para queries que aún no tienen visual_state migrado.
        Será eliminado en la Fase 2 de la refactorización.

    Regla: el sistema debe preferir siempre `visual_state` sobre `sql_text`.
    """
    __tablename__ = "config_queries"

    query_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    # DEPRECADO: nullable=True para permitir la migración progresiva hacia visual_state.
    sql_text: Mapped[str] = mapped_column(Text, nullable=True)
    visual_state: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<ConfigQuery id={self.query_id!r}>"
