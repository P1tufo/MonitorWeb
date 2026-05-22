from __future__ import annotations

from typing import Optional

from sqlalchemy import String, Float, Integer, Boolean, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class WarehouseTask(Base):
    __tablename__ = "warehouse_tasks"

    numero_ot: Mapped[str] = mapped_column(String, primary_key=True)
    pos: Mapped[str] = mapped_column(String, primary_key=True)
    material: Mapped[Optional[str]] = mapped_column(String)
    texto_breve_material: Mapped[Optional[str]] = mapped_column(String)
    tp_proc: Mapped[Optional[str]] = mapped_column(String)
    ubic_proc: Mapped[Optional[str]] = mapped_column(String)
    ctd_teor_dsd: Mapped[Optional[float]] = mapped_column(Float)
    uma: Mapped[Optional[str]] = mapped_column(String)
    tp_dest: Mapped[Optional[str]] = mapped_column(String)
    ubic_dest: Mapped[Optional[str]] = mapped_column(String)
    fe_creac: Mapped[Optional[str]] = mapped_column(String)
    hora: Mapped[Optional[str]] = mapped_column(String)
    usuario: Mapped[Optional[str]] = mapped_column(String)
    lote: Mapped[Optional[str]] = mapped_column(String)
    cl_mov: Mapped[Optional[str]] = mapped_column(String)
    clase_mov: Mapped[Optional[str]] = mapped_column(String)
    doc_mat: Mapped[Optional[str]] = mapped_column(String)
    usuario_conf: Mapped[Optional[str]] = mapped_column(String)
    fecha_conf: Mapped[Optional[str]] = mapped_column(String)
    hor_conf: Mapped[Optional[str]] = mapped_column(String)
    ce: Mapped[Optional[str]] = mapped_column(String)
    entrega: Mapped[Optional[str]] = mapped_column(String, index=True)

    def __repr__(self) -> str:
        return f"<WarehouseTask {self.numero_ot}-{self.pos}>"


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    doc_mat: Mapped[str] = mapped_column(String, primary_key=True)
    ej_mat: Mapped[str] = mapped_column(String, primary_key=True)
    pos: Mapped[str] = mapped_column(String, primary_key=True)
    fe_contab: Mapped[Optional[str]] = mapped_column(String)
    alm: Mapped[Optional[str]] = mapped_column(String)
    ce: Mapped[Optional[str]] = mapped_column(String)
    cmv: Mapped[Optional[str]] = mapped_column(String)
    referencia: Mapped[Optional[str]] = mapped_column(String)
    texto_cab_documento: Mapped[Optional[str]] = mapped_column(String)
    texto_breve_material: Mapped[Optional[str]] = mapped_column(String)
    material: Mapped[Optional[str]] = mapped_column(String)
    cantidad: Mapped[Optional[float]] = mapped_column(Float)
    umb: Mapped[Optional[str]] = mapped_column(String)
    registrado: Mapped[Optional[str]] = mapped_column(String)
    hora: Mapped[Optional[str]] = mapped_column(String)
    usuario: Mapped[Optional[str]] = mapped_column(String)
    pedido: Mapped[Optional[str]] = mapped_column(String)
    pos_extra: Mapped[Optional[str]] = mapped_column(String)
    ce_coste: Mapped[Optional[str]] = mapped_column(String)
    importe_ml: Mapped[Optional[float]] = mapped_column(Float)
    mon: Mapped[Optional[str]] = mapped_column(String)
    proveedor: Mapped[Optional[str]] = mapped_column(String)
    tipo_operacion: Mapped[Optional[str]] = mapped_column(String)

    def __repr__(self) -> str:
        return f"<InventoryMovement {self.doc_mat}-{self.ej_mat}-{self.pos}>"


class OutboundDelivery(Base):
    __tablename__ = "outbound_deliveries"

    entrega: Mapped[int] = mapped_column(Integer, primary_key=True)
    pos_: Mapped[int] = mapped_column(Integer, primary_key=True)
    material: Mapped[Optional[str]] = mapped_column(String)
    denominacion: Mapped[Optional[str]] = mapped_column(String)
    cantidad: Mapped[Optional[str]] = mapped_column(String)
    umb: Mapped[Optional[str]] = mapped_column(String)
    fecha_carga: Mapped[Optional[str]] = mapped_column(String)
    fecha_sm_real: Mapped[Optional[str]] = mapped_column(String)
    creado_el: Mapped[Optional[str]] = mapped_column(String)
    autor: Mapped[Optional[str]] = mapped_column(String)
    centro_costo: Mapped[Optional[str]] = mapped_column(String)
    centro: Mapped[Optional[str]] = mapped_column(String)
    area_negocio: Mapped[Optional[str]] = mapped_column(String)
    ubicacion_bin: Mapped[Optional[str]] = mapped_column(String)
    ubicacion_area: Mapped[Optional[str]] = mapped_column(String)
    estado_wms: Mapped[Optional[str]] = mapped_column(String)
    dias_retraso: Mapped[Optional[int]] = mapped_column(Integer)
    week_sort: Mapped[Optional[str]] = mapped_column(String, index=True)
    week_label: Mapped[Optional[str]] = mapped_column(String)
    referencia: Mapped[Optional[str]] = mapped_column(String)
    ops: Mapped[Optional[str]] = mapped_column(String)
    mm: Mapped[Optional[str]] = mapped_column(String)
    c: Mapped[Optional[str]] = mapped_column(String)
    source_file: Mapped[Optional[str]] = mapped_column(String)
    ingested_at: Mapped[Optional[str]] = mapped_column(String)
    fecha_sm_real_1: Mapped[Optional[str]] = mapped_column(String)
    ubicacion_bin_1: Mapped[Optional[str]] = mapped_column(String)

    __table_args__ = (
        Index("idx_delivery_pos", "entrega", "pos_"),
    )

    def __repr__(self) -> str:
        return f"<OutboundDelivery {self.entrega}-{self.pos_}>"


class StockLevel(Base):
    __tablename__ = "stock_levels"

    material: Mapped[str] = mapped_column(String, primary_key=True)
    lote: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    alm_: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    denominacion: Mapped[Optional[str]] = mapped_column(String)
    tp_: Mapped[Optional[str]] = mapped_column(String)
    ubicacion_bin: Mapped[Optional[str]] = mapped_column(String, primary_key=True)
    stock_disp: Mapped[Optional[str]] = mapped_column(String)
    umb: Mapped[Optional[str]] = mapped_column(String)
    week_sort: Mapped[Optional[str]] = mapped_column(String)
    week_label: Mapped[Optional[str]] = mapped_column(String)
    source_file: Mapped[Optional[str]] = mapped_column(String)
    ingested_at: Mapped[Optional[str]] = mapped_column(String)

    def __repr__(self) -> str:
        return f"<StockLevel {self.material}-{self.lote}-{self.ubicacion_bin}>"


class Lx02Pendiente(Base):
    __tablename__ = "lx02_pendientes"

    material: Mapped[Optional[str]] = mapped_column(String)
    lote: Mapped[Optional[str]] = mapped_column(String)
    alm_: Mapped[Optional[str]] = mapped_column(String)
    denominacion: Mapped[Optional[str]] = mapped_column(String)
    tp_: Mapped[Optional[str]] = mapped_column(String)
    ubicacion_bin: Mapped[Optional[str]] = mapped_column(String)
    stock_disp: Mapped[Optional[str]] = mapped_column(String)
    umb: Mapped[Optional[str]] = mapped_column(String)
    otcuanto: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    week_sort: Mapped[Optional[str]] = mapped_column(String)
    week_label: Mapped[Optional[str]] = mapped_column(String)
    source_file: Mapped[Optional[str]] = mapped_column(String)
    ingested_at: Mapped[Optional[str]] = mapped_column(String)

    def __repr__(self) -> str:
        return f"<Lx02Pendiente {self.otcuanto}>"


class SyncManifest(Base):
    __tablename__ = "sync_manifest"

    file_path: Mapped[str] = mapped_column(String, primary_key=True)
    last_modified: Mapped[Optional[float]] = mapped_column(Float)
    file_size: Mapped[Optional[int]] = mapped_column(Integer)
    processed_at: Mapped[Optional[str]] = mapped_column(String)
    row_count: Mapped[Optional[int]] = mapped_column(Integer)


class AnalyticsSnapshot(Base):
    __tablename__ = "analytics_snapshots"

    key: Mapped[str] = mapped_column(String, primary_key=True)
    data: Mapped[Optional[str]] = mapped_column(Text)
    updated_at: Mapped[Optional[str]] = mapped_column(String)


class AutorAreaMapping(Base):
    __tablename__ = "autor_area_mapping"

    autor: Mapped[str] = mapped_column(String, primary_key=True)
    area_negocio: Mapped[str] = mapped_column(String, primary_key=True)
    frequency: Mapped[Optional[int]] = mapped_column(Integer)
