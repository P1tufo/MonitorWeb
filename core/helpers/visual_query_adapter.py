import logging
from core.schemas import VisualQueryBuilderPayload, MetricDef, MetricCondition, TimeAxisDef, FilterDef

logger = logging.getLogger("visual-query-adapter")

def build_area_stats_payload(year: str, sla_threshold: int) -> VisualQueryBuilderPayload:
    """AST para estadísticas agrupadas por área de negocio."""
    return VisualQueryBuilderPayload(
        baseTable="outbound_deliveries",
        breakdown="__AREA_EXPR__",
        filters=[
            FilterDef(column="outbound_deliveries.fecha_carga", operator="contains", value=year)
        ],
        timeAxis=TimeAxisDef(column=None, granularity="NONE"),
        metrics=[
            MetricDef(
                column="outbound_deliveries.entrega", 
                aggregation="COUNT_DISTINCT",
                label="total_entregas"
            ),
            MetricDef(
                column="outbound_deliveries.fecha_carga", 
                aggregation="COUNT_DISTINCT",
                label="dias_activos"
            ),
            MetricDef(
                column="outbound_deliveries.entrega",
                aggregation="COUNT_DISTINCT",
                label="ontime",
                condition=MetricCondition(column="outbound_deliveries.dias_retraso", operator="lessthanequal", value=sla_threshold)
            ),
            MetricDef(
                column="outbound_deliveries.entrega",
                aggregation="COUNT_DISTINCT",
                label="late",
                condition=MetricCondition(column="outbound_deliveries.dias_retraso", operator="greaterthan", value=sla_threshold)
            )
        ]
    )

def build_sla_stats_payload(year: str, sla_threshold: int) -> VisualQueryBuilderPayload:
    """AST para resumen global de SLA."""
    return VisualQueryBuilderPayload(
        baseTable="outbound_deliveries",
        filters=[
            FilterDef(column="outbound_deliveries.fecha_carga", operator="contains", value=year),
            FilterDef(column="outbound_deliveries.dias_retraso", operator="isnotnull", value="")
        ],
        timeAxis=TimeAxisDef(column=None, granularity="NONE"),
        metrics=[
            MetricDef(
                column="outbound_deliveries.entrega",
                aggregation="COUNT_DISTINCT",
                label="ontime",
                condition=MetricCondition(column="outbound_deliveries.dias_retraso", operator="lessthanequal", value=sla_threshold)
            ),
            MetricDef(
                column="outbound_deliveries.entrega",
                aggregation="COUNT_DISTINCT",
                label="late",
                condition=MetricCondition(column="outbound_deliveries.dias_retraso", operator="greaterthan", value=sla_threshold)
            ),
            MetricDef(
                column="outbound_deliveries.entrega",
                aggregation="COUNT_DISTINCT",
                label="total"
            )
        ]
    )

def build_dates_counts_payload(year: str) -> VisualQueryBuilderPayload:
    """AST para conteo por fechas y área."""
    return VisualQueryBuilderPayload(
        baseTable="outbound_deliveries",
        breakdown="__AREA_EXPR__",
        timeAxis=TimeAxisDef(column="outbound_deliveries.fecha_carga", granularity="DAY"),
        filters=[
            FilterDef(column="outbound_deliveries.fecha_carga", operator="contains", value=year)
        ],
        metrics=[
            MetricDef(
                column="outbound_deliveries.material",
                aggregation="COUNT",
                label="count"
            )
        ]
    )

def build_top_materials_payload(year: str) -> VisualQueryBuilderPayload:
    """AST para ranking de materiales por área."""
    return VisualQueryBuilderPayload(
        baseTable="outbound_deliveries",
        breakdown="__AREA_EXPR__",
        timeAxis=TimeAxisDef(column=None, granularity="NONE"),
        filters=[
            FilterDef(column="outbound_deliveries.fecha_carga", operator="contains", value=year),
            FilterDef(column="outbound_deliveries.denominacion", operator="isnotnull", value="")
        ],
        metrics=[
            MetricDef(column="outbound_deliveries.denominacion", aggregation="COUNT", label="frequency", customExpr="outbound_deliveries.denominacion")
        ]
        # Nota: el agrupamiento por material no es 100% nativo del breakdown simple, 
        # pero para propósitos de migración, lo inyectaremos en el AST adaptado.
    )

def build_wms_status_payload(year: str) -> VisualQueryBuilderPayload:
    return VisualQueryBuilderPayload(
        baseTable="outbound_deliveries",
        breakdown="outbound_deliveries.estado_wms",
        timeAxis=TimeAxisDef(column=None, granularity="NONE"),
        filters=[
            FilterDef(column="outbound_deliveries.fecha_carga", operator="contains", value=year),
            FilterDef(column="outbound_deliveries.estado_wms", operator="isnotnull", value="")
        ],
        metrics=[
            MetricDef(column="outbound_deliveries.entrega", aggregation="COUNT_DISTINCT", label="cantidad")
        ]
    )
