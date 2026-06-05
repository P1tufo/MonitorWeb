"""
core/semantic_layer.py — Capa Semántica para aislar el frontend del esquema físico de BD.

Mantiene el catálogo de Datasets, Dimensiones y Métricas, junto con sus fórmulas de negocio.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

@dataclass
class Dimension:
    id: str
    label: str
    physical_column: str
    type: str = "string"  # string, date, number
    description: str = ""

@dataclass
class Metric:
    id: str
    label: str
    physical_column: str
    aggregation: str = "SUM"
    format: str = "number"  # number, percent
    is_complex_formula: bool = False
    formula_template: Optional[str] = None
    description: str = ""

@dataclass
class Dataset:
    id: str
    label: str
    physical_table: str
    dimensions: List[Dimension] = field(default_factory=list)
    metrics: List[Metric] = field(default_factory=list)


# ─── Catálogo de Datos ────────────────────────────────────────────────────────
DATASETS: Dict[str, Dataset] = {
    "entregas": Dataset(
        id="entregas",
        label="Entregas Salientes",
        physical_table="outbound_deliveries",
        dimensions=[
            Dimension(id="dim_area", label="Área de Negocio", physical_column="area_negocio"),
            Dimension(id="dim_fecha", label="Fecha de Registro", physical_column="creado_el", type="date"),
            Dimension(id="dim_material", label="Material", physical_column="material"),
            Dimension(id="dim_estado", label="Estado WMS", physical_column="estado_wms"),
            Dimension(id="dim_centro", label="Centro de Costo", physical_column="centro_costo"),
            Dimension(id="dim_autor", label="Autor", physical_column="autor"),
        ],
        metrics=[
            Metric(id="met_retraso", label="Días de Retraso", physical_column="dias_retraso", aggregation="AVG"),
            Metric(id="met_cantidad", label="Cantidad", physical_column="cantidad", aggregation="SUM"),
            Metric(
                id="met_sla_efficiency", 
                label="Eficiencia SLA", 
                physical_column="dias_retraso", 
                aggregation="SLA_EFFICIENCY",
                format="percent",
                is_complex_formula=True,
                formula_template="ROUND(SUM(CASE WHEN {col} <= 2 THEN 100.0 ELSE 0.0 END) / NULLIF(COUNT(*), 0), 1)"
            )
        ]
    ),
    "stock": Dataset(
        id="stock",
        label="Niveles de Stock",
        physical_table="stock_levels",
        dimensions=[
            Dimension(id="dim_material", label="Material", physical_column="material"),
            Dimension(id="dim_ubicacion", label="Ubicación Bin", physical_column="ubicacion_bin"),
        ],
        metrics=[
            Metric(id="met_disponible", label="Stock Disponible", physical_column="stock_disp", aggregation="SUM"),
        ]
    ),
    "tareas": Dataset(
        id="tareas",
        label="Tareas de Almacén (OT)",
        physical_table="warehouse_tasks",
        dimensions=[
            Dimension(id="dim_fecha", label="Fecha Creación", physical_column="fe_creac", type="date"),
            Dimension(id="dim_material", label="Material", physical_column="material"),
            Dimension(id="dim_usuario", label="Usuario", physical_column="usuario"),
        ],
        metrics=[
            Metric(id="met_cantidad", label="Cantidad Teórica", physical_column="ctd_teor_dsd", aggregation="SUM"),
        ]
    ),
    "movimientos": Dataset(
        id="movimientos",
        label="Movimientos de Inventario",
        physical_table="inventory_movements",
        dimensions=[
            Dimension(id="dim_fecha", label="Fecha Contable", physical_column="fe_contab", type="date"),
            Dimension(id="dim_material", label="Material", physical_column="material"),
            Dimension(id="dim_ceco", label="Centro de Costo", physical_column="ce_coste"),
            Dimension(id="dim_cmv", label="Clase de Movimiento", physical_column="cmv"),
            Dimension(id="dim_texto", label="Texto Cabecera", physical_column="texto_cab_documento"),
        ],
        metrics=[
            Metric(id="met_cantidad", label="Cantidad", physical_column="cantidad", aggregation="SUM"),
            Metric(
                id="met_avg_tx_per_day",
                label="Promedio Transacciones por Día",
                physical_column="fe_contab",
                aggregation="AVG_TX_PER_DAY",
                is_complex_formula=True,
                formula_template="ROUND(COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT substr({table}.fe_contab, 1, 10)), 0), 1)"
            ),
            Metric(
                id="met_replenishment_rate",
                label="Tasa Reabastecimiento",
                physical_column="tipo_operacion",
                aggregation="REPLENISHMENT_RATE",
                format="percent",
                is_complex_formula=True,
                formula_template="ROUND(SUM(CASE WHEN {col} LIKE '%Ingreso%' THEN 100.0 ELSE 0.0 END) / NULLIF(SUM(CASE WHEN {col} LIKE '%Centro Costo%' OR {col} LIKE '%Orden/Reserva%' THEN 1.0 ELSE 0.0 END), 0), 1)"
            ),
            Metric(
                id="met_return_rate",
                label="Tasa Devolución",
                physical_column="tipo_operacion",
                aggregation="RETURN_RATE",
                format="percent",
                is_complex_formula=True,
                formula_template="ROUND(SUM(CASE WHEN TRIM(cmv) IN ('202', '262') AND IFNULL(LOWER(texto_cab_documento), '') NOT LIKE '%cierre%' THEN 100.0 ELSE 0.0 END) / NULLIF(SUM(CASE WHEN {col} LIKE '%Centro Costo%' OR {col} LIKE '%Orden/Reserva%' THEN 1.0 ELSE 0.0 END), 0), 1)"
            ),
            Metric(
                id="met_unplanned_rate",
                label="Tasa Desplanificado",
                physical_column="cmv",
                aggregation="UNPLANNED_RATE",
                format="percent",
                is_complex_formula=True,
                formula_template="ROUND(SUM(CASE WHEN TRIM({col}) IN ('201', '261', '221') AND NOT ((TRIM({col}) = '201' AND (IFNULL({table}.referencia, '') GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR IFNULL({table}.referencia, '') GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR IFNULL({table}.texto_cab_documento, '') GLOB '*81[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*' OR IFNULL({table}.texto_cab_documento, '') GLOB '*081[0-9][0-9][0-9][0-9][0-9][0-9][0-9]*')) OR (TRIM({col}) = '261' AND ((IFNULL({table}.referencia, '') = '' AND IFNULL({table}.texto_cab_documento, '') = '') OR IFNULL({table}.texto_cab_documento, '') GLOB '*PGP*' OR IFNULL({table}.texto_cab_documento, '') GLOB '*PGE*' OR IFNULL({table}.referencia, '') GLOB '*PGP*' OR IFNULL({table}.referencia, '') GLOB '*PGE*'))) THEN 100.0 ELSE 0.0 END) / NULLIF(SUM(CASE WHEN TRIM({col}) IN ('201', '261', '221') THEN 1.0 ELSE 0.0 END), 0), 1)"
            ),
            Metric(
                id="met_inv_efficiency",
                label="Eficiencia Inventario",
                physical_column="fe_contab",
                aggregation="INV_EFFICIENCY",
                format="percent",
                is_complex_formula=True,
                formula_template="ROUND(SUM(CASE WHEN ABS(julianday(substr(registrado, 7, 4) || '-' || substr(registrado, 4, 2) || '-' || substr(registrado, 1, 2)) - julianday(substr(fe_contab, 7, 4) || '-' || substr(fe_contab, 4, 2) || '-' || substr(fe_contab, 1, 2))) <= 2 THEN 100.0 ELSE 0.0 END) / NULLIF(COUNT(*), 0), 1)"
            )
        ]
    )
}

# Mapa inverso: tabla_física -> dataset_id  (calculado una sola vez al importar)
_PHYSICAL_TABLE_TO_DATASET: Dict[str, str] = {
    ds.physical_table: ds_id for ds_id, ds in DATASETS.items()
}

# ─── Funciones Públicas ───────────────────────────────────────────────────────

def get_frontend_schema() -> Dict[str, Any]:
    """
    Genera un diccionario semántico para exponer a la UI (Studio).
    La UI usará esto en lugar de PRAGMA table_info.
    """
    schema = {}
    for ds_id, ds in DATASETS.items():
        schema[ds_id] = {
            "label": ds.label,
            "dimensions": [{"id": d.id, "label": d.label, "type": d.type} for d in ds.dimensions],
            "metrics": [{"id": m.id, "label": m.label, "aggregation": m.aggregation, "format": m.format} for m in ds.metrics]
        }
    return schema

def resolve_dataset_physical_table(dataset_id: str) -> str:
    """Devuelve la tabla física dado el ID del dataset."""
    ds = DATASETS.get(dataset_id)
    if not ds:
        raise ValueError(f"Dataset desconocido: {dataset_id}")
    return ds.physical_table

def resolve_physical_mapping(dataset_id: str, field_id: str) -> str:
    """
    Traduce un ID semántico (dim_area) a su columna física cualificada (outbound_deliveries.area_negocio).
    Si se le pasa un campo que ya es físico (fallback temporal para queries antiguas), 
    lo deja pasar si existe en el dataset.
    """
    ds = DATASETS.get(dataset_id)
    if not ds:
        return field_id # Fallback para consultas pre-existentes sin migrar
        
    for dim in ds.dimensions:
        if dim.id == field_id:
            return f"{ds.physical_table}.{dim.physical_column}"
    for met in ds.metrics:
        if met.id == field_id:
            return f"{ds.physical_table}.{met.physical_column}"
            
    # Fallback temporal: si no es un ID semántico, asumimos que es físico
    return field_id

def get_metric_formula(dataset_id: str, metric_id: str, table_alias: str = "", legacy_agg: str = "") -> Optional[str]:
    """
    Devuelve la fórmula compleja de una métrica si la tiene, inyectando la columna correcta.
    También soporta consultas legacy donde metric_id es la columna física y legacy_agg es la agregación.
    """
    ds = DATASETS.get(dataset_id)
    if not ds:
        return None
        
    for met in ds.metrics:
        is_match = False
        if met.id == metric_id:
            is_match = True
        elif legacy_agg and met.aggregation == legacy_agg and met.is_complex_formula:
            if metric_id == met.physical_column or metric_id.endswith(f".{met.physical_column}"):
                is_match = True
                
        if is_match and met.is_complex_formula:
            col_ref = f"{table_alias}.{met.physical_column}" if table_alias else met.physical_column
            table_ref = table_alias if table_alias else ds.physical_table
            # Reemplaza {col} y {table} en el template
            formula = met.formula_template.replace("{col}", col_ref).replace("{table}", table_ref)
            return formula
            
    return None


def get_formula_by_physical_table(physical_table: str, aggregation: str, metric_col: str = "") -> Optional[str]:
    """
    Reverse-lookup: dado una tabla física y el nombre de una agregación compleja
    (ej. 'SLA_EFFICIENCY', 'REPLENISHMENT_RATE'), devuelve la expresión SQL real.
    
    Esto permite que payloads legacy (sin datasetId) que provienen de la BD 
    sean resueltos correctamente sin crashear SQLite.
    
    Retorna None si la agregación es estándar o no se encuentra.
    """
    dataset_id = _PHYSICAL_TABLE_TO_DATASET.get(physical_table)
    if not dataset_id:
        return None

    ds = DATASETS[dataset_id]
    for met in ds.metrics:
        if met.aggregation == aggregation and met.is_complex_formula:
            table_ref = physical_table
            # Usar la columna física correcta de la métrica, no la que viene del payload
            col_ref = f"{table_ref}.{met.physical_column}"
            formula = met.formula_template.replace("{col}", col_ref).replace("{table}", table_ref)
            return formula

    return None

